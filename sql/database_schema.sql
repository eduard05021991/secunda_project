CREATE TABLE buildings (
    id SERIAL PRIMARY KEY,
    address VARCHAR(255) NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL
);

CREATE TABLE activities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    parent_id INTEGER REFERENCES activities(id) ON DELETE CASCADE,
    level INTEGER NOT NULL DEFAULT 1,
    CONSTRAINT max_level CHECK (level <= 3)
);

CREATE TABLE organizations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    building_id INTEGER REFERENCES buildings(id) ON DELETE RESTRICT
);

CREATE TABLE phone_numbers (
    id SERIAL PRIMARY KEY,
    organization_id INTEGER REFERENCES organizations(id) ON DELETE CASCADE,
    phone_number VARCHAR(20) NOT NULL
);

CREATE TABLE organization_activities (
    organization_id INTEGER REFERENCES organizations(id) ON DELETE CASCADE,
    activity_id INTEGER REFERENCES activities(id) ON DELETE CASCADE,
    PRIMARY KEY (organization_id, activity_id)
);
