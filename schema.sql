CREATE TABLE users (id SERIAL PRIMARY KEY, username VARCHAR(255), password_hash VARCHAR(95), full_name VARCHAR(255), email_address VARCHAR(255), is_administrator BOOLEAN);
CREATE INDEX users_username_index ON users (username);

CREATE TABLE topics (id SERIAL PRIMARY KEY, name VARCHAR(255));
CREATE INDEX topics_name_index ON topics (name);

CREATE TABLE message_chains (id SERIAL PRIMARY KEY, name VARCHAR(255), topic_id INTEGER REFERENCES topics(id), user_id INTEGER REFERENCES users(id));
CREATE INDEX message_chains_name_index ON message_chains (name);
CREATE INDEX message_chains_topic_id_index ON message_chains (topic_id);
CREATE INDEX message_chains_user_id_index ON message_chains (user_id);

CREATE TABLE messages (id SERIAL PRIMARY KEY, content TEXT, message_chain_id INTEGER REFERENCES message_chains(id), user_id INTEGER REFERENCES users(id));

CREATE TABLE message_replies (message_id INTEGER REFERENCES messages(id), replied_message_id INTEGER REFERENCES messages(id));
CREATE INDEX message_replies_index ON message_replies (message_id, replied_message_id);
