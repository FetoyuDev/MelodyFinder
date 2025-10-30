# Contributing to MelodyFinder

Thank you for your interest in contributing to MelodyFinder! We welcome contributions from everyone.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Translation Contributions](#translation-contributions)

## 📜 Code of Conduct

Be respectful, inclusive, and considerate of others. We're all here to make MelodyFinder better.

## 🚀 Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/MelodyFinder.git`
3. Add upstream remote: `git remote add upstream https://github.com/FetoyuDev/MelodyFinder.git`
4. Create a new branch: `git checkout -b feature/your-feature-name`

## 💻 Development Setup

### Prerequisites

- Python 3.8 or higher
- Git

### Installation

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/MelodyFinder.git
cd MelodyFinder

# Install dependencies
pip install PyQt6 requests pypresence

# Run the application
python init.py
```

## 🤝 How to Contribute

### Reporting Bugs

- Use the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.md)
- Include detailed steps to reproduce
- Provide your environment details
- Attach screenshots if applicable

### Suggesting Features

- Use the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.md)
- Clearly describe the feature and its benefits
- Provide examples or mockups if possible

### Code Contributions

1. **Find an issue** to work on or create a new one
2. **Comment** on the issue to let others know you're working on it
3. **Fork and create a branch** from `main`
4. **Make your changes** following our coding standards
5. **Test thoroughly** to ensure nothing breaks
6. **Submit a pull request**

## 🎨 Coding Standards

### Python Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise

### Example

```python
def format_time(seconds: float) -> str:
    """
    Format seconds into MM:SS format.
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted string in MM:SS format
    """
    minutes, secs = divmod(int(seconds), 60)
    return f"{minutes:02d}:{secs:02d}"
```

### Code Organization

- Keep related functionality together
- Use descriptive file and module names
- Separate UI code from business logic
- Maintain the portable core architecture

### UI Guidelines

- Follow existing PyQt6 patterns
- Maintain consistent spacing and layout
- Support both light and dark themes
- Ensure responsive design

## 📝 Commit Guidelines

### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```
feat: add playlist support

Implemented playlist creation and management with drag-and-drop support.

Closes #123
```

```
fix: resolve Discord RPC connection timeout

Added retry logic and better error handling for Discord presence updates.

Fixes #456
```

## 🔄 Pull Request Process

1. **Update your branch** with the latest changes from `main`:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Ensure your code**:
   - Follows coding standards
   - Includes no unnecessary files
   - Works on Windows, macOS, and Linux (if possible)
   - Doesn't break existing functionality

3. **Create a descriptive PR**:
   - Reference related issues
   - Describe what changed and why
   - Include screenshots for UI changes
   - List any breaking changes

4. **Respond to feedback**:
   - Be open to suggestions
   - Make requested changes promptly
   - Keep the conversation focused

5. **Wait for review**:
   - Maintainers will review your PR
   - CI checks must pass
   - At least one approval is required

### PR Template

```markdown
## Description
Brief description of changes

## Related Issue
Closes #<issue-number>

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe how you tested your changes

## Screenshots
If applicable

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tested on multiple platforms (if possible)
```

## 🌍 Translation Contributions

We support multiple languages: English, Portuguese, Spanish, and Italian.

### Adding Translations

1. **Update** `languages_manager/languages_manager.py`:
   ```python
   'your_key': {
       'en': 'English text',
       'pt': 'Texto em português',
       'es': 'Texto en español',
       'it': 'Testo in italiano'
   }
   ```

2. **Create documentation** in `guides/<language>/`:
   - `README.md` - Main guide
   - `configs-help.md` - Configuration help

3. **Test** your translations in the UI

### Adding a New Language

1. Add language code to `languages_manager.py`
2. Translate all existing strings
3. Create documentation in `guides/<language>/`
4. Update main README.md with new language link
5. Test thoroughly

## 🐛 Debugging Tips

- Use Python's built-in debugger: `import pdb; pdb.set_trace()`
- Check console output for PyQt warnings
- Test with different audio formats
- Verify Discord RPC connection separately

## 📚 Resources

- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [Discord Rich Presence](https://discord.com/developers/docs/rich-presence/how-to)
- [Python Best Practices](https://docs.python-guide.org/)

## ❓ Questions?

- Open a [Discussion](https://github.com/FetoyuDev/MelodyFinder/discussions)
- Join our [Discord server](https://discord.com)
- Check existing [Issues](https://github.com/FetoyuDev/MelodyFinder/issues)

## 🙏 Thank You!

Every contribution, no matter how small, makes MelodyFinder better. We appreciate your time and effort!

---

Happy coding! 🎵
