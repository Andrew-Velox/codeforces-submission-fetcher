# Contributing to Codeforces Submission Fetcher

Thank you for your interest in contributing! Here are some guidelines to help you get started.

## How to Contribute

### Reporting Issues

- Use the GitHub issue tracker to report bugs
- Include detailed steps to reproduce the issue
- Provide your Python version and operating system
- Include any error messages or logs

### Suggesting Features

- Open an issue with the "enhancement" label
- Describe the feature and why it would be useful
- Consider backward compatibility

### Code Contributions

1. **Fork the repository**
   ```bash
   git clone https://github.com/Andrew-Velox/codeforces-submission-fetcher.git
   cd codeforces-submission-fetcher
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add type hints where appropriate
   - Include docstrings for new functions
   - Update tests if needed

4. **Test your changes**
   ```bash
   python -m flake8 CF_FETCH.py
   python CF_FETCH.py  # Test basic functionality
   ```

5. **Commit and push**
   ```bash
   git add .
   git commit -m "Add: your feature description"
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Use a clear title and description
   - Reference any related issues
   - Include screenshots if applicable

## Code Style

- Follow PEP 8 guidelines
- Use type hints for function parameters and return values
- Write clear, descriptive variable names
- Add comments for complex logic
- Keep functions focused and single-purpose

## Development Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Install development tools:
   ```bash
   pip install flake8 pylint black
   ```

3. Format code before committing:
   ```bash
   black CF_FETCH.py setup.py
   ```

## Testing

Since this tool requires API credentials, testing can be challenging. When contributing:

- Test the import functionality: `python -c "import CF_FETCH"`
- Test with mock data when possible
- Document any manual testing steps
- Consider edge cases (empty responses, network errors, etc.)

## Documentation

- Update README.md if you add new features
- Add docstrings to new functions
- Update type hints
- Include examples in docstrings where helpful

## Questions?

Feel free to open an issue if you have any questions about contributing!
