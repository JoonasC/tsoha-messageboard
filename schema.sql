CREATE TABLE users (id SERIAL PRIMARY KEY, username VARCHAR(255) UNIQUE, password_hash VARCHAR(102), is_administrator BOOLEAN);

CREATE TABLE topics (id SERIAL PRIMARY KEY, name VARCHAR(255) UNIQUE);

CREATE TABLE message_chains (id SERIAL PRIMARY KEY, name VARCHAR(255), topic_id INTEGER REFERENCES topics(id) ON DELETE CASCADE, user_id INTEGER REFERENCES users(id), UNIQUE (topic_id, name));
CREATE INDEX message_chains_user_id_index ON message_chains (user_id);

CREATE TABLE messages (id SERIAL PRIMARY KEY, content TEXT, message_chain_id INTEGER REFERENCES message_chains(id) ON DELETE CASCADE, user_id INTEGER REFERENCES users(id));

CREATE TABLE message_replies (message_id INTEGER REFERENCES messages(id) ON DELETE CASCADE, replied_message_id INTEGER REFERENCES messages(id), UNIQUE (message_id, replied_message_id));

INSERT INTO users (username, password_hash, is_administrator) VALUES ('admin', 'pbkdf2:sha256:260000$bh9ql8veT1evAcNC$ffbebe2a680a2ea69d97942d4b93416d48aadcf22b8dde61a598266f1ee09bd9', TRUE)
