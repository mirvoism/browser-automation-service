# Contributing to AI Browser Automation

Thank you for your interest in contributing! This project provides visual AI browser automation for both cloud (Google Gemini) and local (Mac Studio) environments.

## 🚀 Getting Started

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/ai-browser-automation.git
   cd ai-browser-automation
   ```

2. **Choose Your Environment**
   
   **For Google Gemini development:**
   ```bash
   pip install -r requirements.txt
   cp .env.example .env
   # Add your GOOGLE_API_KEY to .env
   ```
   
   **For Mac Studio development:**
   ```bash
   pip install -r requirements-macstudio.txt
   # Ensure access to Mac Studio endpoint
   ```

3. **Install Development Dependencies**
   ```bash
   pip install -r requirements-dev.txt  # If available
   playwright install
   ```

## 🎯 How to Contribute

### Types of Contributions

1. **🐛 Bug Fixes**
   - Fix existing functionality
   - Improve error handling
   - Performance optimizations

2. **✨ New Features**
   - Additional automation examples
   - New model integrations
   - Enhanced anti-bot capabilities

3. **📚 Documentation**
   - Improve setup guides
   - Add usage examples
   - API documentation

4. **🧪 Testing**
   - Unit tests for core functions
   - Integration tests for automation flows
   - Performance benchmarks

### Development Guidelines

#### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings for all functions and classes
- Keep functions focused and small

#### File Organization
```
├── examples/                    # Basic examples (Gemini)
├── examples/*_macstudio.py     # Mac Studio examples
├── production_*.py             # Production-ready code
├── anti_bot_*.py              # Anti-bot specific features
├── docs/                      # Documentation
└── tests/                     # Test files (when added)
```

#### Example Code Structure
```python
"""
Module description here
"""

from browser_use.llm.openai.chat import ChatOpenAI
from browser_use import Agent
import asyncio

async def example_function():
    """
    Clear description of what this function does.
    
    Returns:
        Description of return value
    """
    # Implementation here
    pass

if __name__ == "__main__":
    asyncio.run(example_function())
```

## 🔧 Development Workflow

### Before Making Changes

1. **Create an Issue**
   - Describe the problem or feature request
   - Get feedback from maintainers
   - Discuss implementation approach

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-description
   ```

### Making Changes

1. **Write Code**
   - Follow the guidelines above
   - Test your changes thoroughly
   - Add comments for complex logic

2. **Test Both Versions**
   - Test with Google Gemini (if applicable)
   - Test with Mac Studio (if applicable)
   - Ensure backward compatibility

3. **Update Documentation**
   - Update README if needed
   - Add/update docstrings
   - Update setup guides if necessary

### Submitting Changes

1. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: descriptive commit message"
   ```
   
   **Commit Message Format:**
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation
   - `refactor:` for code refactoring
   - `test:` for tests

2. **Push and Create PR**
   ```bash
   git push origin your-branch-name
   ```
   - Create a Pull Request on GitHub
   - Fill out the PR template
   - Link to related issues

## 🧪 Testing Guidelines

### Manual Testing Checklist

**For Gemini Version:**
- [ ] Basic Google search works
- [ ] API key validation works
- [ ] Error handling for invalid keys
- [ ] Playwright browser launches

**For Mac Studio Version:**
- [ ] LLM connection test passes
- [ ] Model switching works
- [ ] Production agent functions
- [ ] Anti-bot features work

### Adding New Examples

When adding new automation examples:

1. **Create both versions** (if applicable)
   - `examples/new_example.py` (Gemini)
   - `examples/new_example_macstudio.py` (Mac Studio)

2. **Include proper error handling**
   ```python
   try:
       result = await agent.run()
       print("Success:", result)
   except Exception as e:
       print("Error:", e)
   finally:
       await agent.close()
   ```

3. **Add documentation**
   - Comment complex parts
   - Add usage instructions
   - Include expected outputs

## 📝 Pull Request Guidelines

### PR Checklist

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Manual testing completed
- [ ] No sensitive data (API keys, etc.)
- [ ] Clear commit messages
- [ ] PR description explains changes

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Testing
- [ ] Tested with Google Gemini
- [ ] Tested with Mac Studio
- [ ] Manual testing completed

## Additional Notes
Any additional context or considerations
```

## 🤝 Community Guidelines

### Be Respectful
- Welcome newcomers
- Be constructive in feedback
- Help others learn

### Communication
- Use GitHub Issues for bug reports
- Use Discussions for questions
- Be clear and concise

### Quality Focus
- Prioritize working code over clever code
- Document your changes
- Test thoroughly

## 🎯 Priority Areas for Contribution

### High Priority
1. **Anti-bot improvements** - Better evasion techniques
2. **Error handling** - More robust error recovery
3. **Documentation** - Better setup guides and examples
4. **Testing** - Automated test suite

### Medium Priority
1. **Performance optimization** - Faster execution
2. **New model support** - Additional LLM integrations
3. **Browser profiles** - Specialized configurations
4. **Monitoring tools** - Better debugging and logging

### Future Goals
1. **GUI interface** - Visual task builder
2. **Cloud deployment** - Docker/Kubernetes support
3. **Plugin system** - Extensible architecture
4. **Multi-platform** - Windows/Linux support

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and community help
- **Code Review**: Maintainers will review all PRs

Thank you for contributing to making browser automation more accessible and reliable! 🚀 