# Ourapy Project Instructions

## Meta Instructions - IMPORTANT
- **Continuously improve these instructions** as we develop the library
- **Proactively suggest updates** when you notice:
  - Repeated patterns that should be documented
  - Better ways to accomplish tasks
  - Outdated practices that need updating
  - Missing guidelines that would improve consistency
- **Remove or update** instructions that no longer apply
- **Add new sections** as we explore new features or adopt new practices
- **Track significant changes** in the Change Log section at the bottom
- Consider these instructions as living documentation that evolves with the project

### When to Update CLAUDE.md
- After implementing a new feature that introduces patterns
- When we establish a new best practice through experience
- After resolving issues that could be prevented with better guidelines
- When external dependencies or tools change
- During code reviews when we identify improvement opportunities
- When adopting new state-of-the-art practices

### Context File Strategy
**Session Startup Protocol**: When detecting context loss (new session, after auto-compact, or when asked about something I should know but don't), immediately read all context files in one batch:
1. PROJECT_STATE.md - Current status and active work
2. ARCHITECTURE.md - Technical decisions and critical context  
3. SESSION_NOTES.md - Recent development history
4. WORKSPACE_NOTES.md - Project workspace notes and guidelines

**During Session**: Keep these files updated as work progresses, but don't re-read unless detecting another context loss event (WHICH SHOULD BE RARE).

**Mid-Session Re-reading Threshold**: Only re-read context files when ALL conditions met:
- Confidence I should know the answer: >85%
- Confidence in my actual answer: <25%
- Messages since last context read: >20
- Alternative: Ask explicitly "Should I re-read context files?" when uncertain

**Optimization**: Read all relevant context files at once rather than piecemeal to minimize token overhead.

## Code Style
- Use 4 spaces for indentation (Python PEP 8)
- Always run flake8 before considering any task complete
- Maximum line length: 100 characters
- Use type hints for all function parameters and return values

## Testing
- Write tests for all new functionality
- Run pytest before marking any task as complete
- Test files should mirror the source structure in the tests/ directory
- Use descriptive test names that explain what's being tested

## Error Handling
- Use the custom exception hierarchy in oura_api_client.exceptions
- Always provide meaningful error messages
- Implement retry logic for transient failures (5xx, timeouts, connection errors)

## Git Workflow
- Never commit directly unless explicitly asked
- Always check git status before making changes
- Create descriptive commit messages explaining the "why" not just the "what"

## Documentation
- Update docstrings for any modified functions
- Use Google-style docstrings
- Include usage examples for public APIs

## Project-Specific Commands
- Lint: `flake8 oura_api_client/ tests/`
- Test (parallel): `python -m pytest tests/ -n auto -v`
- Test (sequential): `python -m pytest tests/ -v`
- Test (specific): `python -m pytest tests/test_specific.py::TestClass::test_method -v`
- Type check: `mypy oura_api_client/` (if available)

## API Design Principles
- Keep the client interface simple and intuitive
- Use Pydantic models for all API responses
- Maintain backward compatibility when possible

## Common Patterns
- All API endpoints should go through the `_make_request` method
- Use the `build_query_params` utility for consistent parameter handling
- Follow the existing endpoint module pattern for new features

## Debugging Test Failures
**IMPORTANT**: Use systematic approaches when tests fail, especially in CI environments.

### Local Debugging Strategy
1. **Use parallel execution**: `pytest -n auto` for faster feedback
2. **Target specific failures**: `pytest -x --tb=short` (stop on first failure)
3. **Re-run only failed tests**: `pytest --lf` (last failed)
4. **Isolate by class/method**: `pytest tests/test_file.py::TestClass::test_method`
5. **Use short tracebacks**: `--tb=short` or `--tb=line` for cleaner output

### CI Failure Investigation
- **Timeouts ≠ No failures**: Test timeouts can mask actual test failures
- **Ask for specific error output** when remote logs aren't accessible
- **Don't assume environmental issues** without evidence
- **Test locally first** with the same conditions when possible

### Common Patterns to Watch For
- Mock incompatibilities after refactoring (e.g., `raise_for_status` vs `response.ok`)
- Import errors from new dependencies
- Pydantic model validation failures from API changes

## Change Log
### 2025-06-21
- Added Meta Instructions section to ensure continuous improvement of guidelines
- Added parallel testing with pytest-xdist for faster local development
- Added comprehensive debugging section with systematic test failure approaches
- Updated project commands to use parallel testing by default
- Added context file strategy with threshold-based re-reading to minimize token waste
- Implemented session continuity system with PROJECT_STATE.md, ARCHITECTURE.md, SESSION_NOTES.md
- Initial creation with sections for code style, testing, error handling, git workflow, documentation, commands, API design, and common patterns