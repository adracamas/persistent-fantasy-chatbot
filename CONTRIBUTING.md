# Contributing to Persistent Fantasy Chatbot

Thank you for your interest in contributing to the Persistent Fantasy Chatbot project! This document provides guidelines and instructions for contributing.

## 🤝 Ways to Contribute

- **🐛 Bug Reports**: Report bugs or issues you encounter
- **💡 Feature Requests**: Suggest new features or improvements
- **🔧 Code Contributions**: Fix bugs or implement new features
- **📚 Documentation**: Improve documentation, examples, or tutorials
- **🧪 Testing**: Help test on different systems and hardware configurations

## 🚀 Quick Start for Developers

### Prerequisites
- Python 3.8+
- Git
- NVIDIA GPU (recommended for development)
- 20GB+ storage for models and dependencies

### Development Setup
```bash
# 1. Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/persistent-fantasy-chatbot.git
cd persistent-fantasy-chatbot

# 2. Create development environment
python -m venv dev_env
source dev_env/bin/activate  # Windows: dev_env\Scripts\activate

# 3. Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. Setup pre-commit hooks (optional)
pip install pre-commit
pre-commit install

# 5. Run tests
python -m pytest tests/

# 6. Start development
python fantasy_chatbot.py  # Test locally
```

### Development Dependencies
Create a `requirements-dev.txt` file with:
```txt
pytest>=7.0.0
black>=22.0.0
flake8>=5.0.0
mypy>=1.0.0
pre-commit>=2.20.0
```

## 📝 Code Style Guidelines

### Python Code Style
- **Black**: Code formatting with black formatter
- **PEP 8**: Follow Python style guidelines
- **Type Hints**: Use type hints for function parameters and return values
- **Docstrings**: Use Google-style docstrings

```python
def example_function(param: str, count: int = 1) -> List[str]:
    """
    Example function demonstrating code style.

    Args:
        param: A string parameter for the function.
        count: Number of times to repeat the string (default: 1).

    Returns:
        A list of repeated strings.

    Raises:
        ValueError: If count is negative.
    """
    if count < 0:
        raise ValueError("Count must be non-negative")
    
    return [param] * count
```

### File Naming
- Use snake_case for Python files
- Use descriptive names that indicate functionality
- Keep file sizes reasonable (split large files if needed)

## 🏗️ Architecture Guidelines

### Core Principles
1. **Separation of Concerns**: Keep UI, logic, and data layers separate
2. **Memory Management**: Optimize for GPU memory usage
3. **Error Handling**: Graceful degradation for hardware limitations
4. **User Experience**: Prioritize ease of use and installation

### Key Components
- `fantasy_chatbot.py`: Main CLI interface
- `local_llm.py`: AI model integration and God-like prompts
- `memory_system.py`: Persistent storage and vector search
- `web_interface.py`: FastAPI web server
- `pinokio.js`: Pinokio package configuration

### Adding New Features

1. **Feature Planning**
   - Create an issue for discussion
   - Consider hardware compatibility
   - Plan memory usage implications
   - Design user interface changes

2. **Implementation**
   - Follow existing code patterns
   - Add comprehensive error handling
   - Include configuration options
   - Update documentation

3. **Testing**
   - Test on multiple hardware configurations
   - Verify memory usage is reasonable
   - Test installation process
   - Validate user experience

## 🧪 Testing Guidelines

### Test Categories
- **Unit Tests**: Individual function testing
- **Integration Tests**: Component interaction testing
- **Hardware Tests**: GPU/CPU compatibility testing
- **Installation Tests**: Pinokio and manual installation

### Running Tests
```bash
# Run all tests
python -m pytest

# Run specific test category
python -m pytest tests/unit/
python -m pytest tests/integration/

# Run with coverage
python -m pytest --cov=fantasy_chatbot tests/

# Test hardware compatibility
python test_components.py
```

### Test Hardware Configurations
- RTX 5070 (12GB VRAM) - Primary target
- RTX 3060 (8GB VRAM) - Minimum GPU
- CPU-only mode - Fallback testing
- Various RAM configurations (8GB, 16GB, 32GB)

## 🐛 Reporting Bugs

### Bug Report Template
```markdown
**Bug Description**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Run command '...'
2. See error

**Expected Behavior**
What you expected to happen.

**Hardware Configuration**
- GPU: [e.g., RTX 5070, CPU only]
- RAM: [e.g., 16GB]
- OS: [e.g., Windows 11, Ubuntu 20.04]
- Python Version: [e.g., 3.9]

**Additional Context**
Any other context about the problem.
Logs, screenshots, etc.
```

### Common Issues to Report
- GPU memory errors
- Model download failures
- Installation problems
- Performance issues
- Memory system bugs
- Web interface errors

## 💡 Feature Requests

### Feature Request Template
```markdown
**Feature Description**
Clear description of the proposed feature.

**Problem Statement**
What problem does this feature solve?

**Proposed Solution**
How might we implement this feature?

**Hardware Considerations**
How does this affect GPU memory usage?
Any hardware requirements?

**User Experience Impact**
How does this change the user experience?
Installation implications?

**Alternative Solutions**
Any alternative approaches considered?
```

## 📚 Documentation Contributions

### Documentation Types
- **API Documentation**: Function and class documentation
- **User Guides**: Step-by-step usage instructions
- **Developer Guides**: Technical implementation details
- **Troubleshooting**: Common problems and solutions

### Documentation Standards
- Include code examples where relevant
- Use clear, concise language
- Include hardware requirements for features
- Provide installation instructions
- Add troubleshooting sections

## 🔧 Development Workflow

### Git Workflow
1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** changes: `git commit -m 'Add amazing feature'`
4. **Push** to branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Commit Message Format
```
type(scope): brief description

Longer description if needed.

Fixes #123
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Build process or auxiliary tool changes

### Pull Request Guidelines
- **Clear Title**: Describe what the PR does
- **Detailed Description**: Explain changes and rationale
- **Screenshots**: For UI changes
- **Testing**: Verify changes work across configurations
- **Documentation**: Update docs if needed

## 🏷️ Release Process

### Version Numbering
We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

### Release Checklist
- [ ] Update version in setup.py
- [ ] Update CHANGELOG.md
- [ ] Test on all supported hardware
- [ ] Update Pinokio package
- [ ] Create GitHub release
- [ ] Update documentation

## 📞 Getting Help

### Communication Channels
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Pinokio Community**: Installation and usage support

### Before Asking for Help
1. Check existing issues and discussions
2. Search the documentation
3. Try basic troubleshooting steps
4. Test on different hardware if possible

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation

Thank you for helping make the Persistent Fantasy Chatbot better!

---

*This contributing guide is a living document. Please suggest improvements via GitHub issues.*