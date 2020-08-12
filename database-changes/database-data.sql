---------------------------CATEGORY-------------------------
insert into category values (0,'Computers','This is about computers.');
insert into category values (0,'Accesories','This is about accesories.');
insert into category values (0,'Smartphones','This is about smartphones.');
insert into category values (0,'Audio','This is about audio.');

--------------------------PRODUCT---------------------------
insert into product values (0,1,'Computer1',499.99,'images/computers/1.png',3.0);
insert into product values (0,1,'Computer2',599.99,'images/computers/2.png',4.0);
insert into product values (0,2,'Mouse1',29.99,'images/accesories/3.png',5.0);
insert into product values (0,2,'Keyboard1',39.99,'images/accesories/4.png',2.0);
insert into product values (0,3,'Smartphone1',199.99,'images/smartphones/5.png',3.0);
insert into product values (0,3,'Smartphone2',159.99,'images/smartphones/6.png',5.0);
insert into product values (0,1,'Computer3',699.99,'images/computers/7.png',4.0);
insert into product values (0,1,'Computer4',799.99,'images/computers/8.png',3.0);

---------------------------USER-------------------------
insert into user values ('user1','FirstName SecondName',1, 'Quito', 'example@domain.com','123');

---------------------------ORDERS-------------------------
insert into orders values (0, 'user1', '2020-01-01 10:10:10', 0);
insert into orders values (0, 'user1', '2020-01-01 11:11:11', 0);
insert into orders values (0, 'user1', '2020-01-01 12:12:12', 0);
insert into orders values (0,'user2','2020-02-02 10:10:10', 0);
insert into orders values (0,'user2','2020-02-02 10:10:10', 0);
insert into orders values (0,'user2','2020-02-02 10:10:10', 0);
insert into orders values (0,'user3','2020-02-02 10:10:10', 0);
insert into orders values (0,'user3','2020-02-02 10:10:10', 0);
insert into orders values (0,'user3','2020-02-02 10:10:10', 0);
-- Todos los productos adquiridos por un usuario
-- select * from product where id_product in (select id_product from order_details where id_order in (select id_order from orders where username_user='user2') order by quantity desc);

-- Todos los productos de un usuario agrupados  por cantidad
-- select id_product, sum(quantity) from order_details where id_order in (select id_order from orders where username_user='user2') group by id_product order by sum(quantity) desc;

-- Producto más comprado por un usuario
-- select id_product, sum(quantity) from order_details where id_order in (select id_order from orders where username_user='user2') group by id_product order by sum(quantity) desc limit 1;

-- Categoria del producto más comprado por un usuario
-- R: no soportado en versión de mi base de datos.
-- En mi caso, implementaré múltiples querys en el código de manera temporal.
-- select * from category where id_category in (select id_category from product where id_product in (select id_product, sum(quantity) from order_details where id_order in (select id_order from orders where username_user='user2') group by id_product order by sum(quantity) desc limit 1));

--1-- Todo order_details de un usuario
--  select * from order_details where id_order in (select id_order from orders where username_user='user2');
--2-- Todo nombre de producto adquirido por un usuario
-- select product_name from product where id_product in (select id_product from order_details where id_order in (select id_order from orders where username_user='user2'));
--3-- Campos order_number,product_name,quantity,date,total de un usuario
-- select orders.id_order, product.product_name, order_details.quantity, orders.order_date, order_details.subtotal from orders, product, order_details where orders.username_user='user1' and orders.id_order=order_details.id_order and order_details.id_product=product.id_product;
--4-- Punto 3 con rating
-- select product.id_product, orders.id_order, product.product_name, order_details.quantity, orders.order_date, order_details.subtotal, user_product_rating.rating from orders, product, order_details, user_product_rating where orders.username_user='user3' and orders.id_order=order_details.id_order and order_details.id_product=product.id_product and user_product_rating.username_user = 'user3' and user_product_rating.id_product=product.id_product group by product.product_name;
---------------------------ORDER_DETAILS-------------------------
insert into order_details values (0,1,1,10,3999.90);
insert into order_details values (0,2,3,20,3999.90);
insert into order_details values (0,3,6,40,3999.90);
insert into order_details values (0,1,2,100,3999.90);
insert into order_details values (0,2,4,5,3999.90);
insert into order_details values (0,3,7,500,3999.90);

---------------------------COUNTRY-------------------------
INSERT INTO `country` (`id`, `name`) VALUES (NULL, 'Ecuador'), (NULL, 'United States');

---------------------------CITY-------------------------
INSERT INTO `city` (`id_country`, `name`) VALUES ('1', 'Quito'), ('1', 'Guayaquil');
INSERT INTO `city` (`id_country`, `name`) VALUES ('2', 'Boston'), ('2', 'New York');
