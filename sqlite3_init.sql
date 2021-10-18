CREATE TABLE IF NOT EXISTS user(user_id INT PRIMARY KEY NOT NULL, user_name VARCHAR(30), user_hash VARCHAR(64), user_email VARCHAR(100));
CREATE TABLE IF NOT EXISTS server(server_id INT PRIMARY KEY NOT NULL, server_name VARCHAR(100));
CREATE TABLE IF NOT EXISTS channel(channel_id INT PRIMARY KEY NOT NULL, channel_name VARCHAR(100));
CREATE TABLE IF NOT EXISTS message(message_id INT PRIMARY KEY NOT NULL, message_writer_id INT NOT NULL, message_content TEXT);

INSERT INTO user VALUES (1,"toto","toto","toto@gmail.com");