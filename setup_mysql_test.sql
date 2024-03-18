-- A script that prepares a MySQL server for the project

-- Create the database hbnb_test_db if it does not exist
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create user with password
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Grant all privileges to the user on the database
GRANT ALL PRIVILEGES ON `hbnb_test_db`.* TO 'hbnb_test'@'localhost';

-- Grant the user SELECT privilege on the database performance_schema
GRANT SELECT ON `performance_schema`.* TO 'hbnb_test'@'localhost';

-- Flush privileges to apply changes
FLUSH PRIVILEGES;
