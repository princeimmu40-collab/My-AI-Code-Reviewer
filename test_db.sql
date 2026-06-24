-- test_db.sql
-- క్రియేట్ టేబుల్
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(50)
);

-- ఒక చిన్న తప్పు ఇక్కడ ఉంది (కోడ్ రివ్యూ బాట్ దీన్ని పట్టుకుంటుందో లేదో చూద్దాం)
INSERT INTO users VALUES (1, 'Test User', 'test@example.com');
