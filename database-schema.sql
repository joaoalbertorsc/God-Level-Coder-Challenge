
CREATE TABLE brands (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

INSERT INTO brands (id, name) VALUES (1, 'Arca');

CREATE TABLE sub_brands (
    id SERIAL PRIMARY KEY,
    brand_id INTEGER NOT NULL REFERENCES brands(id),
    name VARCHAR(255) NOT NULL
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    brand_id INTEGER NOT NULL REFERENCES brands(id),
    name VARCHAR(255) NOT NULL,
    type CHAR(1) NOT NULL -- 'P' for product, 'I' for item
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    brand_id INTEGER NOT NULL REFERENCES brands(id),
    sub_brand_id INTEGER REFERENCES sub_brands(id),
    category_id INTEGER REFERENCES categories(id),
    name VARCHAR(255) NOT NULL,
    pos_uuid VARCHAR(255)
);

CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    brand_id INTEGER NOT NULL REFERENCES brands(id),
    sub_brand_id INTEGER REFERENCES sub_brands(id),
    category_id INTEGER REFERENCES categories(id),
    name VARCHAR(255) NOT NULL,
    pos_uuid VARCHAR(255)
);

CREATE TABLE option_groups (
    id SERIAL PRIMARY KEY,
    brand_id INTEGER NOT NULL REFERENCES brands(id),
    name VARCHAR(255) NOT NULL
);

CREATE TABLE stores (
    id SERIAL PRIMARY KEY,
    brand_id INTEGER NOT NULL REFERENCES brands(id),
    sub_brand_id INTEGER REFERENCES sub_brands(id),
    name VARCHAR(255) NOT NULL,
    city VARCHAR(255),
    state VARCHAR(2),
    district VARCHAR(255),
    address_street VARCHAR(255),
    address_number VARCHAR(255),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    is_active BOOLEAN,
    is_own BOOLEAN,
    creation_date DATE,
    created_at TIMESTAMP
);

CREATE TABLE channels (
    id SERIAL PRIMARY KEY,
    brand_id INTEGER NOT NULL REFERENCES brands(id),
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    type CHAR(1) -- 'P' for presencial, 'D' for delivery
);

CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    customer_name VARCHAR(255),
    email VARCHAR(255),
    phone_number VARCHAR(255),
    cpf VARCHAR(14),
    birth_date DATE,
    gender CHAR(2),
    agree_terms BOOLEAN,
    receive_promotions_email BOOLEAN,
    registration_origin VARCHAR(255),
    created_at TIMESTAMP
);

CREATE TABLE payment_types (
    id SERIAL PRIMARY KEY,
    brand_id INTEGER NOT NULL REFERENCES brands(id),
    description VARCHAR(255) NOT NULL
);

CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    store_id INTEGER REFERENCES stores(id),
    customer_id INTEGER REFERENCES customers(id),
    channel_id INTEGER REFERENCES channels(id),
    sub_brand_id INTEGER REFERENCES sub_brands(id),
    customer_name VARCHAR(255),
    created_at TIMESTAMP,
    sale_status_desc VARCHAR(255),
    total_amount_items DECIMAL(10, 2),
    total_discount DECIMAL(10, 2),
    total_increase DECIMAL(10, 2),
    delivery_fee DECIMAL(10, 2),
    service_tax_fee DECIMAL(10, 2),
    total_amount DECIMAL(10, 2),
    value_paid DECIMAL(10, 2),
    production_seconds INTEGER,
    delivery_seconds INTEGER,
    discount_reason VARCHAR(255),
    people_quantity INTEGER,
    origin VARCHAR(255)
);

CREATE TABLE product_sales (
    id SERIAL PRIMARY KEY,
    sale_id INTEGER REFERENCES sales(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER,
    base_price DECIMAL(10, 2),
    total_price DECIMAL(10, 2),
    observations TEXT
);

CREATE TABLE item_product_sales (
    id SERIAL PRIMARY KEY,
    product_sale_id INTEGER REFERENCES product_sales(id),
    item_id INTEGER REFERENCES items(id),
    option_group_id INTEGER REFERENCES option_groups(id),
    quantity INTEGER,
    additional_price DECIMAL(10, 2),
    price DECIMAL(10, 2),
    amount INTEGER,
    observations TEXT
);

CREATE TABLE item_item_product_sales (
    id SERIAL PRIMARY KEY,
    item_product_sale_id INTEGER REFERENCES item_product_sales(id),
    item_id INTEGER REFERENCES items(id),
    option_group_id INTEGER REFERENCES option_groups(id),
    quantity INTEGER,
    additional_price DECIMAL(10, 2),
    price DECIMAL(10, 2)
);

CREATE TABLE delivery_sales (
    id SERIAL PRIMARY KEY,
    sale_id INTEGER REFERENCES sales(id),
    courier_name VARCHAR(255),
    courier_phone VARCHAR(255),
    courier_type VARCHAR(255),
    delivery_type VARCHAR(255),
    status VARCHAR(255),
    delivery_fee DECIMAL(10, 2),
    courier_fee DECIMAL(10, 2)
);

CREATE TABLE delivery_addresses (
    id SERIAL PRIMARY KEY,
    sale_id INTEGER REFERENCES sales(id),
    delivery_sale_id INTEGER REFERENCES delivery_sales(id),
    street VARCHAR(255),
    number VARCHAR(255),
    complement VARCHAR(255),
    neighborhood VARCHAR(255),
    city VARCHAR(255),
    state VARCHAR(2),
    postal_code VARCHAR(10),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8)
);

CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    sale_id INTEGER REFERENCES sales(id),
    payment_type_id INTEGER REFERENCES payment_types(id),
    value DECIMAL(10, 2),
    is_online BOOLEAN
);
