# Spec Delta

## REMOVED Requirements

### Requirement: Visual review of changed PNG assets
**Reason**: Image content is deliberately outside automated review.
**Migration**: Skip image bytes; retain changed path metadata and review README text.

### Requirement: Bounded PNG review input
**Reason**: Images are no longer fetched or supplied to the model.
**Migration**: Remove image budgets; retain text-context limits.

### Requirement: PNG validation without privileged raster execution
**Reason**: No image validation is requested or required.
**Migration**: Remove PNG parsing; preserve credential and object-mode boundaries.

### Requirement: Preserve image review isolation and freshness
**Reason**: Image transport is removed; ordinary review isolation and freshness still apply.
**Migration**: Use the existing text-only tool-free reviewer with revision checks.
