CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


CREATE TABLE PROFILE (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR(100),
    address VARCHAR(255),
    email VARCHAR(100) NOT NULL,
    contact VARCHAR(20),
    profile_picture_s3_path VARCHAR(255)
);
