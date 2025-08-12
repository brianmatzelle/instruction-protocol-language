## MCP-Lang: Natural-Language Programming Rules for MCP Execution

This document is the authoritative ruleset the agent will follow when interpreting and executing MCP-Lang programs. It defines syntax, semantics, execution model, state, logging, and error handling. It is designed for small, linear programs that orchestrate Model Context Protocol (MCP) tool commands with clear piping of results.

### Design goals
- **Simplicity**: Linear, readable, low ceremony. No branching by default.
- **Deterministic piping**: Each function consumes the prior return and produces the next.
- **MCP-first**: Steps translate to concrete MCP tool calls and transformations.
- **Explorable state**: The agent maintains a canonical program state and logs it.
- **Extensible**: Conventions can grow with new syntax while preserving backward compatibility.

---

## Core Syntax

### Program purpose
- A line starting with `#` states the purpose of the program. It sets global intent and informs tool selection, prompts, and validations.

Example:
- `# Provision an Ubuntu container, install Xpra, and expose a secured session.`

### Functions (vertical sequence)
- A function is declared by a leading marker on a new line:
  - Decimal numerals: `1.`, `2.`, `3.`, ...
  - Lowercase letters: `a.`, `b.`, ...
  - Roman numerals: `i.`, `ii.`, `iii.`, ...
  - Hyphen bullets: `-`
- All function markers are equivalent for ordering; choose one style and keep it consistent within a block.
- The program executes functions top-to-bottom. Returns are piped from each function to the next.
- A function body is natural language describing the action to take and the expected return.

Example:
- `1. Build a Docker image for Xpra.`
- `2. Run the container and confirm Xpra session is reachable.`

### Context
- A `context:` subsection beneath a function defines parameter requirements and hints used to resolve arguments for MCP tool calls.
- Context may reference prior returns implicitly (see Execution Model) and can add constraints, defaults, or schemas.
- Indent `context:` contents by two spaces or a tab for readability.

Example:
- `2. Run the container`
  - `context:`
    - `image: result.imageId`
    - `ports: [10000:10000/tcp]`

### Returns `()` (horizontal embedding)
- Parentheses denote a return expression or an inline evaluation that yields a value.
- Inline returns may appear within descriptive text to compute or refine values without creating a new vertical step.
- The final value of a function is the canonical return for piping; it should be representable as a JSON-like structure.

Examples:
- `1. Build the image (return { imageId, tag })`
- `2. Verify session (return { sessionUrl, isHealthy: true })`

### Horizontal context `*{ }*`
- An inline contextual block `*{ ... }*` supplies additional constraints, assumptions, or environmental notes. It is not executed but informs tool choice, prompts, and validation.

Examples:
- `Use Debian base *{ prefer slim images; x86_64 }*`
- `Network is firewalled *{ outbound 443 only }*`

### TODO breakpoints
- `TODO` marks an intentional stop point. On encountering `TODO`, execution halts and the agent emits a structured state/log for inspection.
- Use as a save point or a testing breakpoint.

Example:
- `3. Configure TLS for Xpra. TODO: verify cert issuance flow before proceeding.`

---

## Execution Model

### Linear flow and piping
- Execution proceeds top-to-bottom through functions.
- The return of function `n` becomes the implicit input for function `n+1`.
- If a function declares `context:`, the implicit input is merged with the context to form the call arguments for MCP commands.

### Implicit input and program state
- Let `S_n` be the program state after function `n`.
  - `S_0` is empty aside from derived intent from the `#` purpose line.
  - The function `n` receives `(S_{n-1}, priorReturn)` as available inputs.
  - After execution, `priorReturn` is updated to the function's return, and `S_n` is updated by merging `S_{n-1}` with any new bindings discovered.
- A function should return one JSON-like value: object, array, string, number, boolean, or null. Objects are preferred for named data.

### MCP command invocation
- The agent maps a function's description and context to one or more MCP tool calls:
  - Select the most relevant MCP tool by capability and the `#` purpose.
  - Construct arguments from `context:` first, then fill gaps from `priorReturn` and `S_{n-1}`.
  - Pass non-interactive flags and defaults where applicable.
  - Execute and capture the full machine-readable result and key human signals (stdout/stderr snippets).
- If multiple MCP calls are required, they must remain conceptually atomic within the function: produce a single final return.

### Idempotency and side effects
- Where feasible, functions should be idempotent: re-running yields the same result state.
- On unavoidable side effects (e.g., provisioning), return explicit identifiers (IDs, URLs, versions) so subsequent steps can detect prior completion.

### Validation
- Each function should validate critical assumptions before returning. Encode validation results in the return value (e.g., `isHealthy`, `exists`, `status`).

---

## Context and Binding Rules

### Parameter resolution order
1. Explicit values in `context:`
2. Fields from `priorReturn`
3. Fields from accumulated `S_{n-1}`
4. Derivations obtained by lightweight inline evaluation `()`
5. If unresolved, raise a Resolution Needed error and halt (see Errors)

### Naming and addressing
- When not explicitly named, the prior return is available as `it` conceptually for resolution logic.
- Returns should use descriptive field names so later functions can reference them in `context:` (e.g., `imageId`, `sessionUrl`).

### Inline evaluation
- Inline `()` may request transformations or computations over available inputs. The agent performs these without introducing a new vertical function.

Example:
- `Set tag to (lowercase(repoName) + ":latest")`

### Horizontal context precedence
- `*{ }*` blocks inform tool selection, defaults, and safety constraints but never override explicit `context:` values.

---

## TODO and Logging

### TODO behavior
- On `TODO`, immediately stop execution and print a structured state snapshot:
  - `programPurpose`: text from `#`
  - `functionIndex`: the index (or marker) where the TODO was encountered
  - `priorReturn`: last successful return value
  - `state`: current merged program state
  - `notes`: any `*{ }*` currently in scope

### Logging
- For each function, log:
  - `marker`: e.g., `1.` or `ii.`
  - `title`: the function’s one-line description
  - `contextResolved`: final arguments after resolution
  - `calls`: list of MCP calls with tool name, args, summarized outputs
  - `return`: final JSON-like value
  - `timing`: start, end, duration
  - `warnings`: non-fatal issues

---

## Errors and Recovery

### Resolution Needed
- If required inputs cannot be resolved via the rules above, halt with a `Resolution Needed` error including:
  - Missing fields
  - Where they were expected to come from (`context`, `priorReturn`, or `state`)
  - Suggestions for next steps or an edit to add/clarify `context:`

### Tool Failure
- On MCP tool errors, retry once if safe and idempotent. Otherwise, halt with a structured error including stdout/stderr excerpts and suggested remediation.

### Partial Results
- If a function performed partial side effects before failing, return a best-effort partial state with `status: "partial"` and identifiers to allow resumption.

---

## Canonical Return Shapes

Prefer objects with explicit fields:
- Success example: `{ imageId, tag, buildLogRef, status: "built" }`
- Check example: `{ sessionUrl, isHealthy, probe: { code, latencyMs } }`
- Provision example: `{ vmId, region, status: "ready" }`

Arrays are acceptable when the semantic unit is a list. Include a `count` if useful.

Strings/numbers are acceptable for leaf values, but avoid for multi-field outcomes.

---

## Minimal Examples

### Example 1: Simple two-step flow

# Build and verify Xpra image

1. Build the Docker image for Xpra (return { imageId, tag })
  context:
    base: "debian:bookworm-slim"
    dockerfilePath: "./Dockerfile-xpra"
    buildArgs:
      xpraVersion: "latest"

2. Run a container and probe the session (return { sessionUrl, isHealthy })
  context:
    image: imageId
    ports: ["10000:10000/tcp"]
  *{ prefer non-root user; health check timeout 30s }*

### Example 2: TODO breakpoint

# Prepare TLS for Xpra

a. Request a certificate (return { orderId, dnsChallenges })

b. Configure DNS for challenges. TODO: inspect issued records before proceeding

---

## Extension Conventions

- New syntax must remain human-readable and backward compatible.
- Prefer declarative hints over imperative commands; the agent decides the concrete MCP calls.
- When adding features (conditionals, loops, parallelism), introduce them as scoped blocks with explicit constraints rather than implicit behavior.
- Propose new markers sparingly, and document resolution and precedence rules clearly.

---

## Agent Checklist (at runtime)

- Read `#` to establish purpose and constraints.
- For each function in order:
  - Merge `context:` with `priorReturn` and state.
  - Honor `*{ }*` as non-binding constraints.
  - Select appropriate MCP tools; construct non-interactive, reproducible calls.
  - Validate critical outcomes; produce a single canonical return value.
  - Update state, log details.
  - Stop immediately on `TODO`, Resolution Needed, or unrecoverable tool errors.
- Emit final return and full log upon completion.

---

## Versioning

- This document is versioned by date and commit in the repository history. Changes should include a short changelog at the bottom.

Changelog:
- 2025-08-12: Initial version.
