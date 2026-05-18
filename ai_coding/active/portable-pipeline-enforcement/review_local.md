# Local AI review — 2026-05-18T08:32:17.625963+00:00

> PARSING NOTE: No VERDICT line found in model output. Treating as FAIL (fail-safe).

This pull request introduces a comprehensive Git hook system to enforce adherence to the `CLAUDE.md` guidelines within the repository. The hooks ensure that developers follow the specified processes for task management, artifact creation, and commit practices, thereby improving code quality and consistency.

### Highlights

* **Git Hook Implementation**: Implements `pre-commit`, `commit-msg`, and `post-commit` hooks to enforce `CLAUDE.md` guidelines.
* **Artifact Enforcement**: The `pre-commit` hook ensures that all required task-folder artifacts (`PROGRESS.md`, `STATUS`, `disagreements.log`, `diff.patch`, `review_local.md`) are present on disk and staged for commit.
* **Trailer Validation**: The `commit-msg` hook validates the presence and correctness of `CLAUDE-TRAILER` and `CLAUDE-TRAILER-STATUS` trailers in commit messages, ensuring proper attribution and status tracking.
* **Task Routing**: The `post-commit` hook automatically routes committed diffs into the appropriate task folders, streamlining the workflow.
* **Cross-Platform Support**: Includes both PowerShell (`install-hooks.ps1`) and shell (`install-hooks.sh`) scripts for installing the hooks, ensuring compatibility across different operating systems.

### Changelog

* **tools/hooks/commit-msg**
  * Added a new hook to validate commit message trailers.
  * Ensures `CLAUDE-TRAILER` and `CLAUDE-TRAILER-STATUS` trailers are present and correctly formatted.
  * Validates that the `CLAUDE-TRAILER-STATUS` trailer matches the `STATUS` file content.
* **tools/hooks/post-commit**
  * Added a new hook to route committed diffs into task folders.
  * Automatically creates task directories and moves diffs based on commit messages.
  * Ensures task folders are properly initialized with required files.
* **tools/hooks/pre-commit**
  * Added a new hook to enforce artifact presence and status consistency.
  * Validates that all required task-folder artifacts are present and staged.
  * Checks for valid `STATUS` file values and `review_local.md` verdict consistency.
* **tools/install-hooks.ps1**
  * Added a PowerShell script to install Git hooks.
  * Ensures the `core.hooksPath` is set to `tools/hooks`.
  * Includes error handling for missing hooks or outdated Git versions.
* **tools/install-hooks.sh**
  * Added a shell script to install Git hooks.
  * Ensures the `core.hooksPath` is set to `tools/hooks`.
  * Includes error handling for missing hooks or outdated Git versions.

### Note

This pull request introduces a new system for managing task-related artifacts and commit messages. It is crucial to run the `install-hooks.sh` or `install-hooks.ps1` script after cloning the repository to enable the hooks. The hooks enforce strict adherence to `CLAUDE.md` guidelines, ensuring consistency and quality in the codebase.
