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
y del campo 'description' a 'pdescription' de la tabla 'processing_status'
Nota 2 (Danny Díaz): se cambió el orden de instrucciones debido a errores que provocaba por dependencias
*/

CREATE TABLE processing_status(
    id_processing_status int,
    pstatus varchar(256),
    pdescription varchar(256)
);




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



/*Cambios por: Danny Díaz 16-08-2020
Nota: Las instrucciones anteriores no crearon las FK de forma correcta, se realizó una adecuación
luego de cambiar el ENGINE de processing_status, e igualar los tipos de datos de id_processing_status,
finalmente agregando indices que sostengan las FK, en la interfaz de PHPMyAdmin se evidenciaba que no se crearon
de forma correcta sobre todo por la diferencia de tipo de dato de la clave de processing_status
*/



//////// correcciones de claves PK y FK  //////
DROP TABLE user_product_rating;

CREATE TABLE user_product_rating(
    username_user varchar(30) NOT NULL,
    id_product int NOT NULL,
    rating float(3,2),
    id_processing_status int NOT NULL
);
ALTER TABLE `user_product_rating` ENGINE = INNODB;

ALTER TABLE `user_product_rating` ADD INDEX(`username_user`);
ALTER TABLE `user_product_rating` ADD INDEX(`id_product`);
ALTER TABLE `user_product_rating` ADD INDEX(`id_processing_status`);

ALTER TABLE `user_product_rating` ADD CONSTRAINT `fk_rating_user` FOREIGN KEY (`username_user`) REFERENCES `user`(`username`) ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE `user_product_rating` ADD CONSTRAINT `fk_rating_product` FOREIGN KEY (`id_product`) REFERENCES `product`(`id_product`) ON DELETE RESTRICT ON UPDATE CASCADE;


DROP TABLE processing_status;

CREATE TABLE processing_status(
    id_processing_status int,
    pstatus varchar(256),
    pdescription varchar(256)
);
ALTER TABLE `processing_status` ADD PRIMARY KEY(id_processing_status);

ALTER TABLE `processing_status` ENGINE = INNODB;
ALTER TABLE `processing_status` CHANGE `id_processing_status` `id_processing_status` INT(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `user_product_rating` ADD CONSTRAINT `fk_rating_processing` FOREIGN KEY (`id_processing_status`) REFERENCES `processing_status`(`id_processing_status`) ON DELETE RESTRICT ON UPDATE CASCADE;
//////// fin de correcciones de claves PK y FK  //////


ALTER TABLE `user` ADD `id` INT UNSIGNED NOT NULL AUTO_INCREMENT FIRST, ADD UNIQUE (`id`);


/*
Cambios por: Danny Díaz 23-08-2020
Nota: Panel de administración con roles
*/
CREATE TABLE `shop`.`role` ( `id` INT UNSIGNED NOT NULL AUTO_INCREMENT , `name` VARCHAR(32) NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;
CREATE TABLE `shop`.`user_role` ( `id_role` INT UNSIGNED NOT NULL , `username_user` VARCHAR(30) NOT NULL , INDEX (`id_role`), INDEX (`username_user`)) ENGINE = InnoDB;
ALTER TABLE `user_role` ADD CONSTRAINT `fk_user_role_role` FOREIGN KEY (`id_role`) REFERENCES `role`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE; ALTER TABLE `user_role` ADD CONSTRAINT `fk_user_role_user` FOREIGN KEY (`username_user`) REFERENCES `user`(`username`) ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE `user_role` ADD PRIMARY KEY(id_role, username_user);

ALTER TABLE `product` CHANGE `product_name` `product_name` VARCHAR(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL, CHANGE `price` `price` FLOAT(10,2) NULL DEFAULT '0', CHANGE `avgrating` `avgrating` FLOAT(2,1) NULL DEFAULT '0';


/*
Cambios por: Ronny Jaramillo 28-08-2020
Nota: Eliminación de la tabla 'processing_status' y todos las las referencias de sus campos que se tengan en otras tablas.
*/
DROP TABLE processing_status;

DROP TABLE user_product_rating;

CREATE TABLE user_product_rating(
    username_user varchar(30) NOT NULL,
    id_product int NOT NULL,
    rating float(3,2)
);
ALTER TABLE `user_product_rating` ENGINE = INNODB;

ALTER TABLE `user_product_rating` ADD INDEX(`username_user`);
ALTER TABLE `user_product_rating` ADD INDEX(`id_product`);

ALTER TABLE `user_product_rating` ADD CONSTRAINT `fk_rating_user` FOREIGN KEY (`username_user`) REFERENCES `user`(`username`) ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE `user_product_rating` ADD CONSTRAINT `fk_rating_product` FOREIGN KEY (`id_product`) REFERENCES `product`(`id_product`) ON DELETE RESTRICT ON UPDATE CASCADE;

/* Si al irse al template 'my_account', no aparece nada en pantalla y aparece un error en el log
acerca de SQL que diga ONLY_FULL_GROUP_BY, ejecutar esta línea en la base de datos.*/
SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));
/*ó*/
SET @@sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
/*
Cambios por: Danny Díaz 26-08-2020
Nota: Inicio de noticias
*/


CREATE TABLE `shop`.`news` ( `id` INT UNSIGNED NOT NULL AUTO_INCREMENT , `author_user` VARCHAR(30) NOT NULL , `publish_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , `title` VARCHAR(30) NOT NULL , `description` VARCHAR(140) NOT NULL , `url` TEXT NOT NULL , `content_html` TEXT NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;
ALTER TABLE `news` ADD INDEX(`author_user`);
ALTER TABLE `news` ADD CONSTRAINT `fk_news_user` FOREIGN KEY (`author_user`) REFERENCES `user`(`username`) ON DELETE RESTRICT ON UPDATE CASCADE;
CREATE TABLE `shop`.`news_category` ( `id` TINYINT UNSIGNED NOT NULL AUTO_INCREMENT , `name` VARCHAR(20) NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;
ALTER TABLE `news` ADD `id_news_category` TINYINT NOT NULL AFTER `content_html`, ADD INDEX (`id_news_category`);
ALTER TABLE `news_category` CHANGE `id` `id` TINYINT(4) UNSIGNED NOT NULL AUTO_INCREMENT;

ALTER TABLE `news` CHANGE `id_news_category` `id_news_category` TINYINT(4) UNSIGNED NOT NULL;
ALTER TABLE `news` ADD CONSTRAINT `fk_news_category` FOREIGN KEY (`id_news_category`) REFERENCES `news_category`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE TABLE `shop`.`source` ( `id_news` INT UNSIGNED NOT NULL , `url` TEXT NOT NULL , `name` VARCHAR(20) NOT NULL , PRIMARY KEY (`id_news`, `name`)) ENGINE = InnoDB;

ALTER TABLE `source` ADD INDEX(`id_news`);
ALTER TABLE `source` ADD CONSTRAINT `fk_source_news` FOREIGN KEY (`id_news`) REFERENCES `news`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;
CREATE TABLE `shop`.`user_view_news` ( `id_news` INT UNSIGNED NOT NULL , `username_user` VARCHAR(30) NOT NULL , `date_view` DATE NOT NULL , PRIMARY KEY (`id_news`, `username_user`)) ENGINE = InnoDB;
ALTER TABLE `user_view_news` ADD INDEX(`username_user`);
ALTER TABLE `user_view_news` ADD INDEX(`id_news`);
ALTER TABLE `user_view_news` ADD CONSTRAINT `fk_view_news` FOREIGN KEY (`id_news`) REFERENCES `news`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE; ALTER TABLE `user_view_news` ADD CONSTRAINT `fk_view_user` FOREIGN KEY (`username_user`) REFERENCES `user`(`username`) ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE `user_view_news` CHANGE `date_view` `date_view` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP;



/*
Cambios por: Danny Díaz 29-08-2020
Nota: Fin de noticias
*/

ALTER TABLE `user_view_news` DROP PRIMARY KEY, ADD PRIMARY KEY(id_news, username_user, date_view);
