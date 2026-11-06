# Spec Delta

## MODIFIED Requirements

### Requirement: Primary README usage and test examples
The primary repository README SHALL permanently contain simple usage examples for every implementation and a copy-and-pasteable example of running all tests across all implementations, including required setup, cross-language integration, and packaged CLI checks. Maintenance changes SHALL keep these examples current as implementations and test commands evolve. For the existing TypeScript/Node.js and Python implementations, the primary usage demos SHALL show JSON piped through their existing CLIs before inline library/API programs. Inline library/API examples SHALL remain available lower in the README as secondary examples. The CLI guidance SHALL identify the JSON output record's `digest` as the full Merkle root and distinguish it from the shortened display label and current UTC calculation metadata.

#### Scenario: Use and verify the implementations
- **WHEN** a reader follows the primary README from a clean checkout with the documented runtimes
- **THEN** they can run a simple example for each implementation and execute all implementations' tests using the supplied commands

#### Scenario: Add an implementation or change test commands
- **WHEN** maintenance adds an implementation or changes how its tests run
- **THEN** the same change updates the primary README usage and all-tests examples

#### Scenario: Find stdin hashing before library programs
- **WHEN** a reader reaches the primary README's usage section after setup
- **THEN** runnable stdin JSON pipeline examples for both existing CLIs appear before any inline Node or Python API programs
- **AND** the inline API programs remain below those demos as clearly secondary examples

#### Scenario: Identify the full root from CLI output
- **WHEN** a reader runs either primary CLI demo with `{"b":2,"a":1}`
- **THEN** it emits a JSON record with full SHA-256 `digest` `d331f806a7ada5308a00a03f350fd885f492ee54ea4d621af24ef45ba9b88559`
- **AND** adjacent guidance explains that `digest` is the full root, prefix length affects only the label, and CLI UTC metadata varies with calculation time rather than using the secondary API example's fixed clock
