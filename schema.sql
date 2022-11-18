CREATE TABLE users (id SERIAL PRIMARY KEY, username VARCHAR(255) UNIQUE, password_hash VARCHAR(95), is_administrator BOOLEAN);

CREATE TABLE topics (id SERIAL PRIMARY KEY, name VARCHAR(255) UNIQUE);

CREATE TABLE message_chains (id SERIAL PRIMARY KEY, name VARCHAR(255), topic_id INTEGER REFERENCES topics(id) ON DELETE CASCADE, user_id INTEGER REFERENCES users(id), UNIQUE (topic_id, name));
CREATE INDEX message_chains_user_id_index ON message_chains (user_id);

CREATE TABLE messages (id SERIAL PRIMARY KEY, content TEXT, message_chain_id INTEGER REFERENCES message_chains(id) ON DELETE CASCADE, user_id INTEGER REFERENCES users(id));

CREATE TABLE message_replies (message_id INTEGER REFERENCES messages(id) ON DELETE CASCADE, replied_message_id INTEGER REFERENCES messages(id), UNIQUE (message_id, replied_message_id));
