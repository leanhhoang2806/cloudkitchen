CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


CREATE TABLE Seller_Info (
    id UUID DEFAULT uuid_generate_v4(),
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address VARCHAR(255),
    zipcode VARCHAR(15) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id)
);

CREATE TABLE Buyer_Info (
    id UUID DEFAULT uuid_generate_v4(),
    name VARCHAR(255),
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    address VARCHAR(255),
    seller_id UUID DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id)
);

CREATE TABLE Dish (
    id UUID DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    s3_path VARCHAR(255),
    seller_id UUID NOT NULL,
    is_featured BOOLEAN DEFAULT FALSE,
    status VARCHAR(50) DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (seller_id) REFERENCES Seller_Info(id),
    PRIMARY KEY (id)
);

CREATE TABLE Orders (
    id UUID DEFAULT uuid_generate_v4(),
    buyer_id UUID NOT NULL,
    dish_id UUID NOT NULL,
    seller_id UUID NOT NULL,
    status VARCHAR(50) DEFAULT 'WAITING_FOR_SELLER_CONFIRM',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (buyer_id) REFERENCES Buyer_Info(id),
    FOREIGN KEY (dish_id) REFERENCES Dish(id),
    PRIMARY KEY (id)
);

CREATE TABLE Purchases (
    id UUID DEFAULT uuid_generate_v4(),
    order_id UUID NOT NULL,
    dish_id UUID NOT NULL,
    quantity INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES Orders(id),
    FOREIGN KEY (dish_id) REFERENCES Dish(id),
    PRIMARY KEY (id)
);


CREATE TABLE Payments (
    id UUID DEFAULT uuid_generate_v4(),
    email VARCHAR(255) NOT NULL,
    picture_upload_limit INT NOT NULL,
    dishes_to_feature_limit INT NOT NULL,
    seller_id UUID NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (seller_id) REFERENCES Seller_Info(id),

    PRIMARY KEY (id)
);


CREATE TABLE Featured_dish (
    id UUID DEFAULT uuid_generate_v4(),
    dish_id UUID NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (dish_id) REFERENCES Dish(id),
    PRIMARY KEY (id)
);