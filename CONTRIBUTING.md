# Contributing to KrishiMitra

Thank you for your interest in contributing to KrishiMitra! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help create a welcoming environment for all contributors

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/krishimitra.git`
3. Follow the [SETUP.md](SETUP.md) guide to set up your development environment
4. Create a feature branch: `git checkout -b feature/your-feature-name`

## Development Workflow

### 1. Before You Start

- Check existing issues and pull requests to avoid duplication
- Create an issue to discuss major changes before implementing
- Review the [design.md](design.md) and [requirements.md](requirements.md) documents

### 2. Making Changes

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Make your changes
# Write tests for your changes
# Update documentation if needed

# Run tests
pytest

# Run linters
ruff check src/ tests/
mypy src/

# Format code
ruff format src/ tests/
```

### 3. Commit Guidelines

We follow conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(voice): add support for Punjabi language

Implemented STT and TTS support for Punjabi language using
ElevenLabs voice profiles.

Closes #123
```

```
fix(monitoring): correct NDVI calculation for edge cases

Fixed calculation error when satellite data has missing values.
Added unit tests to prevent regression.
```

### 4. Pull Request Process

1. Update documentation for any user-facing changes
2. Add tests for new functionality
3. Ensure all tests pass: `pytest`
4. Ensure code is formatted: `ruff format src/ tests/`
5. Ensure no linting errors: `ruff check src/ tests/`
6. Update CHANGELOG.md with your changes
7. Push to your fork and create a pull request

Pull Request Template:
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests pass locally
- [ ] No new warnings introduced
```

## Code Style Guidelines

### Python Style

- Follow PEP 8 guidelines
- Use type hints for function signatures
- Maximum line length: 120 characters
- Use descriptive variable names
- Add docstrings for all public functions and classes

Example:
```python
def calculate_ndvi(
    nir_band: np.ndarray,
    red_band: np.ndarray
) -> np.ndarray:
    """
    Calculate Normalized Difference Vegetation Index (NDVI).
    
    Args:
        nir_band: Near-infrared band values
        red_band: Red band values
    
    Returns:
        NDVI values ranging from -1 to 1
    
    Raises:
        ValueError: If input arrays have different shapes
    """
    if nir_band.shape != red_band.shape:
        raise ValueError("Input arrays must have the same shape")
    
    return (nir_band - red_band) / (nir_band + red_band + 1e-8)
```

### Database Models

- Use descriptive table and column names
- Add indexes for frequently queried columns
- Include created_at and updated_at timestamps
- Add proper foreign key constraints
- Use UUIDs for primary keys

### API Endpoints

- Use RESTful conventions
- Include proper error handling
- Add request/response validation
- Document with OpenAPI/Swagger
- Include rate limiting

## Testing Guidelines

### Unit Tests

- Test individual functions and methods
- Mock external dependencies
- Aim for 80%+ code coverage
- Use descriptive test names

Example:
```python
@pytest.mark.unit
def test_calculate_ndvi_with_valid_inputs():
    """Test NDVI calculation with valid input arrays"""
    nir = np.array([0.8, 0.7, 0.9])
    red = np.array([0.2, 0.3, 0.1])
    
    result = calculate_ndvi(nir, red)
    
    assert result.shape == nir.shape
    assert np.all(result >= -1) and np.all(result <= 1)
```

### Integration Tests

- Test interactions between components
- Use test database
- Test API endpoints end-to-end
- Test external service integrations

### Property-Based Tests

- Use Hypothesis for property-based testing
- Test invariants and properties
- Generate random test cases

Example:
```python
from hypothesis import given, strategies as st

@given(
    risk_score=st.floats(min_value=0, max_value=100),
    threshold=st.floats(min_value=0, max_value=100)
)
def test_alert_triggering_property(risk_score, threshold):
    """Alert should trigger if and only if risk_score > threshold"""
    should_alert = risk_score > threshold
    actual_alert = trigger_alert(risk_score, threshold)
    assert actual_alert == should_alert
```

## Documentation

### Code Documentation

- Add docstrings to all public functions, classes, and modules
- Use Google-style docstrings
- Include examples for complex functions
- Document exceptions and edge cases

### User Documentation

- Update README.md for user-facing changes
- Update SETUP.md for setup/configuration changes
- Add examples and tutorials for new features
- Keep documentation in sync with code

## Database Migrations

### Creating Migrations

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Add field to farmer model"

# Review the generated migration file
# Edit if necessary to handle data migrations

# Test the migration
alembic upgrade head
alembic downgrade -1
alembic upgrade head
```

### Migration Guidelines

- One migration per logical change
- Include both upgrade and downgrade
- Test migrations on sample data
- Document complex migrations
- Never edit existing migrations in main branch

## Security

### Reporting Security Issues

- Do NOT open public issues for security vulnerabilities
- Email security concerns to: security@krishimitra.example.com
- Include detailed description and steps to reproduce

### Security Best Practices

- Never commit secrets or API keys
- Use environment variables for sensitive data
- Validate and sanitize all user inputs
- Use parameterized queries to prevent SQL injection
- Implement proper authentication and authorization
- Keep dependencies up to date

## Performance

### Performance Guidelines

- Profile code before optimizing
- Use database indexes appropriately
- Implement caching for expensive operations
- Use async/await for I/O operations
- Batch database operations when possible
- Monitor query performance

## Review Process

### For Contributors

- Respond to review comments promptly
- Be open to feedback and suggestions
- Update PR based on review feedback
- Request re-review after making changes

### For Reviewers

- Be constructive and respectful
- Focus on code quality and maintainability
- Check for security issues
- Verify tests are adequate
- Ensure documentation is updated

## Questions?

- Check existing documentation
- Search closed issues
- Ask in discussions
- Contact maintainers

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to KrishiMitra! 🌾
