CREATE TABLE IF NOT EXISTS user(user_id INTEGER PRIMARY KEY AUTOINCREMENT, user_name VARCHAR(30), user_hash VARCHAR(64), user_email VARCHAR(100));
CREATE TABLE IF NOT EXISTS server(server_id INTEGER PRIMARY KEY AUTOINCREMENT, server_name VARCHAR(100), server_creator_id INT NOT NULL);
CREATE TABLE IF NOT EXISTS channel(channel_id INTEGER PRIMARY KEY AUTOINCREMENT, channel_name VARCHAR(100), channel_server_id INT NOT NULL);
CREATE TABLE IF NOT EXISTS message(message_id INTEGER PRIMARY KEY AUTOINCREMENT, message_writer_id INT NOT NULL, message_content TEXT, message_channel_id INT NOT NULL);

CREATE TABLE IF NOT EXISTS membership(user_id INTEGER, server_id INTEGER);
CREATE TABLE IF NOT EXISTS friendship(friend1_id INTEGER, friend2_id INTEGER);