# Security Configuration

## Local Development

Keep local credentials in the ignored `.env` file. Never commit `.env`, JWT
secrets, passwords, or deployment credentials. Use a unique local JWT secret
and admin password rather than values copied from documentation.

## Shared or Production Deployment

Before deployment:

1. Generate a new random `JWT_SECRET` of at least 32 characters.
2. Set a unique strong `ADMIN_PASSWORD` that is not the admin email and
   restrict access to it.
3. Provide `JWT_SECRET`, `ADMIN_EMAIL`, and `ADMIN_PASSWORD` through the
   deployment secret manager.
4. Set `APP_ENV=production` and `APP_DEBUG=false`.
5. Rotate credentials immediately if they are exposed or shared.

The API refuses to start in production when required credentials are missing,
too short, or still use development defaults.

The guard is implemented in `src/config.py` and runs during FastAPI startup.
Its behavior is covered by `tests/test_security_config.py`; local development
continues to permit development-only defaults for convenience.
