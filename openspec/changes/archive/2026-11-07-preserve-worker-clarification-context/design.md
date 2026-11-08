# Design

## Context

See `proposal.md` for the existing contract and issue #23. `Worker.context()` drops
all bot comments and truncates human discussion to ten 4,000-character entries.
`save()` edits one App-authored state comment; `execute()` replaces its message
with generic triage/attempt status before constructing context. `pause_phase()`
also routes planning, implementation and existing-PR repair questions through
`save("needs-information", ...)`.

An offline reproduction at `/tmp/opencode/reproduce_clarification_context.py`
asks a question, appends “Agreed. Please proceed as you suggest”, starts another
worker and saves triage status. The owner answer survives in model context but
the assertion that the original question survives fails. No model/API call is made.

## Goals / Non-Goals

**Goals:** Restore the existing question/answer lifecycle across status updates,
restarts and multiple clarification rounds using the current bounded state record.

**Non-Goals:** Change #23's README text, add conversational authorization, reset
attempts on bot activity, create a new chat service or alter merge/review gates.

## Decisions

### Preserve questions where all needs-information paths converge

Add optional clarification history to the existing durable issue state. Capture
the complete question when `save()` records needs-information, before replacing
the generic current message. Record text, asked revision, run link and the observed
human-comment cursor so subsequent answers can be interpreted in order. Deduplicate
identical revision/question records; a second distinct question must retain the
first question rather than overwrite it. Keep history through triage, ready,
implementation, blocked/retry and PR repair so later phases can interpret the same
owner answers. Human answers remain native issue comments, not duplicated storage.

Loading legacy state without history remains valid. If that state is currently
needs-information, seed its known question before any status save; use unknown
position when its original comment cursor cannot be recovered. Never reconstruct
an erased question from a generic status message or treat unrelated bot text as
worker-authored history. Validate optional history before sending it to a model.

Taking only a transient snapshot of `state.message` would fix one run but lose the
question after an interrupted status save. Durable question history avoids that
failure without adding separate issue comments or another persistence mechanism.

### Supply complete question/answer evidence through shared context paths

Provide preserved questions and human comments with author/ID/order information
as explicitly untrusted task data. Replace silent ten-comment/4,000-character
clipping for this discussion with complete bounded inclusion: exceeding the
existing ceiling must stop with a concrete context-limit diagnostic, not leave
“yes” without the question or omit a newer qualification.

Use the same retained clarification evidence in initial/resumed triage, the
plan/implement/complete context, and existing-PR repair. Repair currently supplies
the issue state inside its metadata discussion; expose the clarification evidence
consistently without changing material issue revision or independent-review
freshness rules. Neither prior worker messages nor quoted instructions can
authorize tools, credentials, retries, implementation or merges.

### Reuse existing limits and authorization

Keep the 60,000-character state-comment limit and the shared per-request
90,000-character serialized-task guard. Check a candidate state before publishing
it; do not silently trim history to make it fit. If history cannot fit, retain the
last valid record and report the capacity blocker rather than fabricate context.
No new context window or database is necessary for this repository's small threads.

Bot question/history/status changes remain excluded from issue revision identity.
Human replies still trigger re-triage, and implementation still needs `ready` or
the existing eligible retry mechanism. Reading “agreed” must not reset attempts
or launch implementation without authorization. Unchanged events must remain
deduplicated; genuine unanswered ambiguity must still pause.

## Risks / Trade-offs

- Old question already erased → preserve only recoverable text; request explicit
  clarification rather than invent historical conversation.
- Long conversations exceed bounded state/input → fail explicitly without dropping
  antecedents or granting a larger budget; record the actual ceiling in operations docs.
- Spoofed history or prompt injection → accept state only from the configured worker
  identity, validate shape and treat all question/answer text as data, never policy.

## Migration Plan

Implement in a separate apply phase, first adding failing lifecycle regressions.
Update worker policy/operations documentation with retained context and limits.
After local verification, owner publication goes through current-head CI and
independent review and manual rebase merge. Verify a fresh controlled issue can
answer a worker question with a short reply, await `ready`, and reach its linked
PR without asking the already-answered question again. Record real evidence before
claiming hosted acceptance; do not modify issue #23 as part of this planning task.
