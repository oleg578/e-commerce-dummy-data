# PostgreSQL Docker Compose Upgrade Plan

## Notes

- User initially used PostgreSQL 16 in docker-compose.
- User requested upgrade to latest Postgres, which resulted in 17.x being pulled.
- Container failed to start: data directory was initialized by version 16, not compatible with 17.x.
- User chose to upgrade to PostgreSQL 17 specifically.
- Existing data volume may need to be removed or migrated for compatibility.

## Task List

- [x] Update docker-compose.yml to use postgres:latest
- [x] Identify container startup failure due to data directory version mismatch
- [ ] Update docker-compose.yml to use postgres:17
- [ ] Remove or migrate existing data volume to resolve incompatibility
- [ ] Restart container and verify successful startup
- [ ] Verify schema initialization and table creation

## Current Goal

Upgrade to PostgreSQL 17 and resolve startup issue