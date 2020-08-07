

CREATE DATABASE shop;

USE shop;

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
CREATE TABLE category(
    id_category int NOT NULL AUTO_INCREMENT,
    category_name varchar(255),
    info varchar(255),
    PRIMARY KEY (id_category)
);
CREATE TABLE user(
    username varchar(30) NOT NULL,    
    fullname varchar(255),
    city varchar(255),
    email varchar(255),
    passwd varchar(255),
    PRIMARY KEY (username)
);
CREATE TABLE orders(
    id_order int NOT NULL AUTO_INCREMENT,
    username_user varchar(30) NOT NULL,
    order_date datetime,
    total float(10,2),
    PRIMARY KEY (id_order),  
    FOREIGN KEY (username_user) REFERENCES user(username)
);
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

-- orders.total -> calculado
-- best sellers: select id_product from order_details order by quantity desc limit 3;


/*
Cambios por: Danny Díaz el 07-08-2020
Nota: corrección de integridad
*/
ALTER TABLE `product` ENGINE = INNODB;
ALTER TABLE `user` ENGINE = INNODB;
ALTER TABLE `category` ENGINE = INNODB;
ALTER TABLE `orders` ENGINE = INNODB;
ALTER TABLE `order_details` ENGINE = INNODB;
ALTER TABLE `product` ADD CONSTRAINT `fk_producto_categoria` FOREIGN KEY (`id_category`) REFERENCES `category`(`id_category`) ON DELETE RESTRICT ON UPDATE RESTRICT;
ALTER TABLE `order_details` ADD CONSTRAINT `fk_order_details_product` FOREIGN KEY (`id_product`) REFERENCES `product`(`id_product`) ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE `order_details` ADD CONSTRAINT `fk_order_details_order` FOREIGN KEY (`id_order`) REFERENCES `orders`(`id_order`) ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE `orders` ADD CONSTRAINT `fk_orders_user` FOREIGN KEY (`username_user`) REFERENCES `user`(`username`) ON DELETE RESTRICT ON UPDATE CASCADE;


