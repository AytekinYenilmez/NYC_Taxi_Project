# Contributing to NYC Taxi Analytics Pipeline

Thank you for your interest in contributing to the NYC Taxi Analytics Pipeline! This document provides guidelines for contributing to the project.

## 🤝 How to Contribute

### Reporting Issues
- Check existing issues before creating a new one
- Use the issue template and provide detailed information
- Include error messages, system information, and steps to reproduce

### Suggesting Features
- Open an issue with the "enhancement" label
- Clearly describe the feature and its benefits
- Discuss the implementation approach

### Code Contributions

#### Setup Development Environment
1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/NYC_Taxi_Project.git`
3. Create a virtual environment: `python -m venv venv`
4. Install dependencies: `pip install -r requirements.txt`
5. Install development dependencies: `pip install pytest black flake8`

#### Development Workflow
1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes with proper documentation
3. Write tests for new functionality
4. Run tests: `pytest`
5. Format code: `black .`
6. Check code style: `flake8`
7. Commit with descriptive messages
8. Push and create a pull request

## 📝 Code Standards

### Python Code Style
- Follow PEP 8 guidelines
- Use Black for code formatting
- Add type hints where appropriate
- Write docstrings for all functions and classes

### Documentation
- Update README.md for significant changes
- Add inline comments for complex logic
- Document any new configuration options
- Include examples in docstrings

### Testing
- Write unit tests for new functions
- Ensure all tests pass before submitting
- Include integration tests for workflow changes
- Test with different data sizes and edge cases

## 🚀 Pull Request Process

1. **Pre-submission Checklist:**
   - [ ] Code follows project style guidelines
   - [ ] Tests pass locally
   - [ ] Documentation updated
   - [ ] Commit messages are descriptive
   - [ ] No unnecessary files included

2. **Pull Request Requirements:**
   - Clear title and description
   - Reference related issues
   - Include testing instructions
   - Add screenshots for UI changes

3. **Review Process:**
   - Maintainers will review within 48 hours
   - Address feedback promptly
   - Keep the PR updated with main branch

## 🏗️ Project Structure Guidelines

### Adding New Features
- Place utilities in `utils/` directory
- Add new workflows to `flows/` directory
- Update templates in `templates/` directory
- Document in appropriate README sections

### File Organization
- Keep related functionality together
- Use descriptive file and function names
- Separate configuration from logic
- Maintain consistent import ordering

## 🧪 Testing Guidelines

### Test Coverage
- Aim for >80% code coverage
- Test both success and failure scenarios
- Include performance tests for large datasets
- Mock external dependencies

### Test Structure
```python
def test_function_name():
    # Arrange
    input_data = create_test_data()
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    assert result == expected_output
```

## 📚 Documentation Guidelines

### Code Documentation
- Use clear, concise docstrings
- Include parameter types and return values
- Provide usage examples
- Document any assumptions or limitations

### README Updates
- Keep installation instructions current
- Update feature lists for new functionality
- Include troubleshooting for common issues
- Maintain accurate project structure

## 🎯 Priority Areas

We welcome contributions in these areas:

### High Priority
- Performance optimizations for large datasets
- Additional visualization types
- Enhanced error handling and logging
- Cloud deployment configurations

### Medium Priority
- Interactive dashboards
- Additional data sources
- Machine learning model integration
- API development

### Low Priority
- UI/UX improvements
- Additional output formats
- Code refactoring
- Documentation improvements

## 🤔 Questions?

- Check existing issues and discussions
- Create an issue for questions
- Contact maintainers for complex topics
- Join project discussions

## 🏆 Recognition

Contributors will be:
- Listed in project credits
- Mentioned in release notes
- Invited to join the maintainer team (active contributors)

Thank you for helping make this project better! 🙏
