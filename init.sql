DO
$$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'memcoadmin') THEN
      CREATE ROLE memcoadmin WITH LOGIN PASSWORD 'memcopassword';
      ALTER ROLE memcoadmin CREATEDB;
   END IF;
END
$$;

DO
$$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'memcodatabase') THEN
      CREATE DATABASE memcodatabase OWNER memcoadmin;
   END IF;
END
$$;
