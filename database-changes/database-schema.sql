CREATE DATABASE shop;

USE shop;

CREATE TABLE category(
    id_category int NOT NULL AUTO_INCREMENT,
    category_name varchar(255),
    info varchar(255),
    PRIMARY KEY (id_category)
);
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

/*
Cambios por: Danny Díaz el 07-08-2020
Nota: Corrección de integridad
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

/*
Cambios por: Danny Díaz el 07-08-2020
Nota: Adición de tablas city y country con sus respectivos constraints. Adición del campo id_country en user con su constraint.
*/
CREATE TABLE `shop`.`country` ( `id` INT UNSIGNED NOT NULL AUTO_INCREMENT , `name` VARCHAR(255) NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;
CREATE TABLE `shop`.`city` ( `id_country` INT UNSIGNED NOT NULL , `name` VARCHAR(255) NOT NULL ) ENGINE = InnoDB;
ALTER TABLE `city` ADD PRIMARY KEY(id_country, name);
ALTER TABLE `city` ADD INDEX(`id_country`);
ALTER TABLE `city` ADD CONSTRAINT `fk_city_country` FOREIGN KEY (`id_country`) REFERENCES `country`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE `user` ADD `id_country` INT UNSIGNED NOT NULL AFTER `fullname`;

UPDATE `user` SET `id_country` = '1' WHERE `user`.`username` = 'user1';

ALTER TABLE `user` ADD INDEX(`id_country`);

UPDATE `user` SET `city` = 'Quito' WHERE `user`.`username` = 'user1';

ALTER TABLE `user` ADD INDEX(`city`);

ALTER TABLE `user` CHANGE `city` `city` VARCHAR(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL;

ALTER TABLE `city` CHANGE `name` `name` VARCHAR(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL;

ALTER TABLE `user` ADD CONSTRAINT `fk_user_country_city` FOREIGN KEY (`id_country`, `city`) REFERENCES `city`(`id_country`, `name`) ON DELETE RESTRICT ON UPDATE CASCADE;

/*Cambios por: Ronny Jaramillo 12-08-2020
Nota: cambio nombre del campo 'status' a 'pstatus' 
y del campo 'description' a 'pdescription' de la tabla 'processing_status'*/
CREATE TABLE user_product_rating(
    username_user varchar(30) NOT NULL,
    id_product int NOT NULL,
    rating float(3,2),
    id_processing_status int,
    FOREIGN KEY (username_user) REFERENCES user(username),
    FOREIGN KEY (id_product) REFERENCES product(id_product),
    FOREIGN KEY (id_processing_status) REFERENCES processing_status(id_processing_status)
);
ALTER TABLE `user_product_rating` ENGINE = INNODB;
ALTER TABLE `user_product_rating` ADD CONSTRAINT `fk_rating_user` FOREIGN KEY (`username_user`) REFERENCES `user`(`username`) ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE `user_product_rating` ADD CONSTRAINT `fk_rating_product` FOREIGN KEY (`id_product`) REFERENCES `product`(`id_product`) ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE `user_product_rating` ADD CONSTRAINT `fk_rating_processing` FOREIGN KEY (`id_processing_status`) REFERENCES `processing_status`(`id_processing_status`) ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE TABLE processing_status(
    id_processing_status int,
    pstatus varchar(256),
    pdescription varchar(256)
    PRIMARY KEY (id_processing_status)
);