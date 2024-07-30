DO $$ 
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'db_user') THEN
        CREATE USER db_user WITH PASSWORD 'db_password';
    END IF;
END
$$;

DO $$ 
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'driver_db') THEN
        CREATE DATABASE driver_db;
    END IF;
END
$$;

GRANT ALL PRIVILEGES ON DATABASE driver_db TO db_user;