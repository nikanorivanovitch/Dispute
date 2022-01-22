CREATE TABLE IF NOT EXISTS user(
                                    user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                    user_name VARCHAR(30), 
                                    user_hash VARCHAR(64), 
                                    user_email VARCHAR(100), 
                                    user_discriminant INTEGER, 
                                    user_picture_token VARCHAR(64)
                                );

CREATE TABLE IF NOT EXISTS server(
                                    server_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                    server_name VARCHAR(100), 
                                    server_creator_id INT NOT NULL
                                );

CREATE TABLE IF NOT EXISTS channel(
                                    channel_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                    channel_name VARCHAR(100), 
                                    channel_server_id INT NOT NULL
                                );

CREATE TABLE IF NOT EXISTS message(
                                    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    message_timestamp INTEGER NOT NULL,
                                    message_sender_id INT NOT NULL,
                                    message_content TEXT,
                                    message_channel_id INT NOT NULL
                                );

CREATE TABLE IF NOT EXISTS membership(user_id INTEGER, server_id INTEGER);
CREATE TABLE IF NOT EXISTS friendship(friend1_id INTEGER, friend2_id INTEGER);
CREATE TABLE IF NOT EXISTS roles(role_id INTEGER, role_name VARCHAR(50), role_color VARCHAR(6));

CREATE TABLE IF NOT EXISTS pending_friend_request(sender_id INTEGER, receiver_id INTEGER);
CREATE TABLE IF NOT EXISTS pending_server_request(sender_id INTEGER, receiver_id INTEGER);
CREATE TABLE IF NOT EXISTS pending_ping(user_id INTEGER, channel_id INTEGER);

CREATE TABLE IF NOT EXISTS files(file_token VARCHAR(64), file_extension VARCHAR(5));

