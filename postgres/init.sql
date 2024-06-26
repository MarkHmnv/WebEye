-- Create main development database
CREATE DATABASE devdb;
GRANT ALL PRIVILEGES ON DATABASE devdb TO devuser;

-- Create test database
CREATE DATABASE webeye_test_db;
GRANT ALL PRIVILEGES ON DATABASE webeye_test_db TO devuser;