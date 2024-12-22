-- Users table
CREATE TABLE IF NOT EXISTS user (
    id VARCHAR(50) PRIMARY KEY,
    password VARCHAR(255) NOT NULL
);

-- Tasks table
CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    due_date DATE NOT NULL,
    priority ENUM('High', 'Medium', 'Low') NOT NULL,
    created_by VARCHAR(50) NOT NULL,
    FOREIGN KEY (created_by) REFERENCES user (id)
);

-- Tokens table
CREATE TABLE IF NOT EXISTS tokens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    token VARCHAR(255) UNIQUE NOT NULL,
    user_id VARCHAR(50) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user (id)
);

-- Insert initial data into users table
INSERT INTO user (id, password) VALUES ('test', 'password123');

-- Insert initial data into tasks table
INSERT INTO tasks (title, description, due_date, priority, created_by)
VALUES ('Learn Flask', 'Build a Flask project', '2024-12-31', 'High', 'test');




