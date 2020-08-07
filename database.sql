CREATE TABLE product (
    id_product int NOT NULL AUTO_INCREMENT,
    id_category int NOT NULL,
    product_name varchar(255),
    price float(10,2),
    img_path varchar(255),
    avgrating float(2,1),
    PRIMARY KEY (id_product),
    FOREIGN KEY (id_category) REFERENCES category(id_category)
);
--insert into product values (0,1,'Computer1',399.99,'static/images/computers/1.png',4.0);
CREATE TABLE category(
    id_category int NOT NULL AUTO_INCREMENT,
    category_name varchar(255),
    info varchar(255),
    PRIMARY KEY (id_category)
);
-- insert into category values (0,'Computers','This is about computers.');
CREATE TABLE user(
    username varchar(30) NOT NULL,    
    fullname varchar(255),
    city varchar(255),
    email varchar(255),
    passwd varchar(255),
    PRIMARY KEY (username)
);
-- insert into user values ('user1','FirstName SecondName', 'UIO', 'example@domain.com','123');
CREATE TABLE orders(
    id_order int NOT NULL AUTO_INCREMENT,
    username_user varchar(30) NOT NULL,
    order_date datetime,
    total float(10,2),
    PRIMARY KEY (id_order),  
    FOREIGN KEY (username_user) REFERENCES user(username)
);
-- insert into orders values (0, 'user1', '2020-01-01 10:10:10', 0); 
-- orders.total -> calculado
CREATE TABLE order_details(
    detail_number int NOT NULL AUTO_INCREMENT,
    id_order int NOT NULL,
    id_product int NOT NULL,
    quantity int,
    subtotal float(10,2),
    PRIMARY KEY (detail_number),
    FOREIGN KEY (id_order) REFERENCES orders(id_order),
    FOREIGN KEY (id_product) REFERENCES product(id_product)
);
-- insert into order_details values (0,1,1,10,3999.90);
-- best sellers: select id_product from order_details order by quantity desc limit 3;


