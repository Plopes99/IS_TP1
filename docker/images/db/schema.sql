CREATE TABLE public.imported_documents (
	id              serial PRIMARY KEY,
	file_name       VARCHAR(250) UNIQUE NOT NULL,
	xml             XML NOT NULL,
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Criação da tabela airplane_disasters
CREATE TABLE airplane_disasters (
    id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(255) NOT NULL,
    accidents_types VARCHAR(255),
    damage_types VARCHAR(255)
);

-- Criação da tabela countries
CREATE TABLE countries (
    id INT PRIMARY KEY AUTO_INCREMENT,
    country_name VARCHAR(255) NOT NULL,
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES airplane_disasters(id)
);

-- Criação da tabela disasters
CREATE TABLE disasters (
    id INT PRIMARY KEY AUTO_INCREMENT,
    date DATE,
    aircraft_type VARCHAR(255),
    operator VARCHAR(255),
    fatalities INT,
    country_id INT,
    FOREIGN KEY (country_id) REFERENCES countries(id)
);
