# PostgreSQL Docker Compose and Schema Initialization Plan

## Notes

- User wants a PostgreSQL database via docker-compose with:
  - Database: shop
  - User: shop
  - Password: admin

- The docker-compose.yml is located in ./db/
- The PostgreSQL version should be 16 (stable)
- The SQL schema file is named E-Commerce-Example.sql and is also in ./db/
- The SQL file should be mounted as an initialization script for the database container

## Task List

- [x] Create docker-compose.yml for PostgreSQL with specified credentials
- [x] Move docker-compose.yml to ./db/
- [x] Update PostgreSQL image to version 16
- [x] Ensure E-Commerce-Example.sql is in ./db/
- [x] Update docker-compose.yml to mount E-Commerce-Example.sql as /docker-entrypoint-initdb.d/init.sql
- [ ] Start PostgreSQL container and initialize schema
- [ ] Verify tables are created successfully

## Current Goal

Start PostgreSQL container and initialize schema
