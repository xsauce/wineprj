CREATE TABLE wineprj.product (
	pid VARCHAR(36) NOT NULL,
	name VARCHAR(100) NOT NULL,
	img_url TEXT NULL,
	parent_id VARCHAR(36) NULL,
	description TEXT NULL,
	volume SMALLINT NULL,
	price DOUBLE NULL,
	brand VARCHAR(50) NULL,
	country VARCHAR(50) NULL,
	area VARCHAR(100) NULL,
	grape_sort VARCHAR(50) NULL,
	scene VARCHAR(20) NULL,
	wine_level VARCHAR(50) NULL,
	sort VARCHAR(50) NULL,
	created_at DATETIME NOT NULL,
	updated_at TIMESTAMP NOT NULL,
	CONSTRAINT product_PK PRIMARY KEY (pid)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8
COLLATE=utf8_general_ci;