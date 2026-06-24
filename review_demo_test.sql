-- ఈ SQL ఫైల్‌లో కొన్ని తప్పులు ఉన్నాయి:
-- 1. 'id' కి Primary Key లేదు.
-- 2. టేబుల్ నేమ్ 'users' (lowercase) అని ఉండాలి, కానీ 'USERS' అని ఉంది.
-- 3. 'email' కాలమ్ కి UNIQUE కన్‌స్ట్రైంట్ లేదు (ఇది ఉండటం మంచిది).

CREATE TABLE USERS_demo (
    id INT primary key,
    name VARCHAR(100),
    email VARCHAR(100),
    created_at TIMESTAMP
);

-- ప్రైమరీ కీ లేకుండా డేటాను ఇన్సర్ట్ చేయడం వల్ల డూప్లికేట్ ఎంట్రీలు వచ్చే ప్రమాదం ఉంది.
INSERT INTO USERS_demo (id, name, email) VALUES (1, 'Alice', 'alice@example.com');
INSERT INTO USERS_demo (id, name, email) VALUES (1, 'Bob', 'bob@example.com'); -- ఇది డూప్లికేట్ ఐడి, ప్రైమరీ కీ లేకపోవడం వల్ల ఇది రన్ అవుతుంది!
