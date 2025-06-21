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
- Test: `python -m pytest tests/ -v`
- Type check: `mypy oura_api_client/` (if available)

## API Design Principles
- Keep the client interface simple and intuitive
- Use Pydantic models for all API responses
- Maintain backward compatibility when possible

## Common Patterns
- All API endpoints should go through the `_make_request` method
- Use the `build_query_params` utility for consistent parameter handling
- Follow the existing endpoint module pattern for new features

## Change Log
### 2025-06-21
- Added Meta Instructions section to ensure continuous improvement of guidelines
- Initial creation with sections for code style, testing, error handling, git workflow, documentation, commands, API design, and common patterns