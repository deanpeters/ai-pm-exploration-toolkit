# Authentication Directory

This directory contains authentication-related files for the AI PM Toolkit web dashboard.

## Files (Auto-generated at runtime)

- `auth_config.json` - Authentication configuration with secret key
- `users.json` - User database with hashed passwords  
- `sessions.json` - Active user sessions

## Security Notice

**These files are automatically generated and should NOT be committed to version control.**

They contain:
- Secret keys for session signing
- Password hashes
- Active session data
- User information

## Template Files

- `auth_config.json.template` - Shows the structure for configuration
- Use this as a reference for manual configuration if needed

## Development Setup

The toolkit will automatically:
1. Generate secure random secret keys on first run
2. Create default user accounts
3. Handle session management

No manual configuration required for development use.