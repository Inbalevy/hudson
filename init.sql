-- Create the Template table
CREATE TABLE Template (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  url VARCHAR(255) NOT NULL,
  state BOOLEAN DEFAULT FALSE,
  creation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the Environment table
CREATE TABLE Environment (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  template_id INTEGER REFERENCES Template(id),
  status VARCHAR(20) CHECK (status IN ('CREATING', 'ACTIVE', 'DESTROYING', 'DESTROYED')) DEFAULT 'CREATING'
);
