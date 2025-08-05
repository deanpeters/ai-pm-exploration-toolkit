# 🔨 Development Documentation

Documentation for contributors, maintainers, and developers working on the AI PM Toolkit.

## Development Guides

### 🤝 [CONTRIBUTING.md](CONTRIBUTING.md)
Guidelines for contributing to the AI PM Toolkit project, including code standards and submission process.

### 📝 [DOCUMENTATION.md](DOCUMENTATION.md)
Documentation standards, style guides, and best practices for maintaining project documentation.

## Implementation History

### 📁 [completion-reports/](completion-reports/)
Detailed implementation reports and completion summaries for major project phases:

- **[PRODUCTION_UPGRADE.md](completion-reports/PRODUCTION_UPGRADE.md)** - Transformation from prototype to production installer
- **[PM_TRANSFORMATION_COMPLETE.md](completion-reports/PM_TRANSFORMATION_COMPLETE.md)** - User guidance refactor from programmer-centric to PM-centric
- **[DOCUMENTATION_AUDIT_COMPLETE.md](completion-reports/DOCUMENTATION_AUDIT_COMPLETE.md)** - Comprehensive documentation audit and improvements
- **[LEARNING_GUIDE_COMPLETE.md](completion-reports/LEARNING_GUIDE_COMPLETE.md)** - HTML5 interactive learning guide implementation

## Development Setup

### Prerequisites
- Python 3.8+
- Node.js 16+ (for web components)
- Docker & Docker Compose (for workflow tools)
- Git

### Development Workflow
1. Clone the repository
2. Read `CONTRIBUTING.md` for setup instructions
3. Follow documentation standards in `DOCUMENTATION.md`
4. Submit PRs following the contribution guidelines

## Architecture Overview

The toolkit follows a modular architecture:

```
├── installer.py          # Main production installer
├── toolkit.yaml          # Tool manifest and configuration
├── docs/                 # User documentation
├── learning-guide/       # Interactive learning platform
├── playbooks/           # Deep-dive tool guides
├── workflow-tools/      # Docker configurations
└── dev/                 # Development documentation
```

## Maintenance

- **Tool Updates**: Modify `toolkit.yaml` and test with installer
- **Documentation**: Follow standards in `DOCUMENTATION.md`
- **Learning Content**: Update `/learning-guide/` files
- **Platform Support**: Test across macOS, Linux, Windows

---

**Contributing?** Start with `CONTRIBUTING.md` and join our development community!