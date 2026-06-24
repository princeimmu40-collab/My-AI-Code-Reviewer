-- database_schema.sql
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(100) -- ఇక్కడ ఇండెక్స్ లేదు, సెర్చ్ స్లో అవుతుంది
);

-- ఇది ఒక రిపోర్టింగ్ క్వెరీ, కానీ దీనికి ఆప్టిమైజేషన్ అవసరం
SELECT name FROM users WHERE email = 'test@example.com';
