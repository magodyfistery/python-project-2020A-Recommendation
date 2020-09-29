El orden de ejecución importa, primero se crea el catálogo con id inicial igual a 1 (truncar la tabla si el id se genera automáticamente desde otro número)


---------------------------PROCESSING_STATUS-------------------------
---------------------------No es necesario---------------------------
/*INSERT INTO `processing_status` (`id_processing_status`, `pstatus`, `pdescription`) VALUES (NULL, 'PENDING', 'Requiere incorporación');
*/

---------------------------CATEGORY-------------------------
insert into category values (0,'Computers','This category contains various computers.');
insert into category values (0,'Accesories','This category offers anything about accesories for various devices.');
insert into category values (0,'Smartphones','This category contains various smartphones.');
insert into category values (0,'Audio','This category contains audio products.');


--------------------------PRODUCT---------------------------
insert into product values (0,1,'iMac Core i3 Apple',499.99,'images/computers/1.png',0);
insert into product values (0,1,'Dell All-in-one i5 2.50Ghz',599.99,'images/computers/2.png',0);
insert into product values (0,2,'LeadsaiL Wireless Computer Mouse',29.99,'images/accesories/3.png',0);
insert into product values (0,2,'NPET K10 Gaming Keyboard USB',39.99,'images/accesories/4.png',0);
insert into product values (0,3,'Moto G8 Play',199.99,'images/smartphones/5.png',0);
insert into product values (0,3,'Samsung Galaxy A70',159.99,'images/smartphones/6.png',0);
insert into product values (0,1,'HP i7 7th Generation',699.99,'images/computers/7.png',0);
insert into product values (0,1,'Acer i3 2.6GHz 4GB RAM',799.99,'images/computers/8.png',0);
insert into product values (0,1,'Dell i5 8th Generation',799.99,'images/computers/9.png',0);
insert into product values (0,4,'Focusrite Scarlett Solo',117.99,'images/audio/6.png',0);
insert into product values (0,4,'Z606 5.1 Surround Sound Speaker System',129.99,'images/audio/5.png',0);
insert into product values (0,1,'HP Compaq Prodesk 4300 Pro Slim',179.95,'images/computers/10.png',0);
insert into product values (0,1,'Lenovo Legion Tower 5 Gaming',1389.00,'images/computers/11.png',0);
insert into product values (0,1,'Dell PowerEdge T40 Business Tower Server Desktop',1049.00,'images/computers/12.png',0);
insert into product values (0,2,'VicTsing MM057 2.4G Wireless Mouse',9.99,'images/accesories/5.png',0);
insert into product values (0,2,'VicTsing Computer Wireless Mouse, 2.4G',9.99,'images/accesories/6.png',0);
insert into product values (0,2,'VicTsing mm057 2.4G Wireless Portable',10.99,'images/accesories/7.png',0);
insert into product values (0,2,'Logitech MK270 Wireless Keyboard',58.36,'images/accesories/8.png',0);
insert into product values (0,2,'Perixx Periboard-512 Ergonomic Split',39.99,'images/accesories/9.png',0);
insert into product values (0,2,'Redragon K552 Mechanical Gaming',37.99,'images/accesories/10.png',0);
insert into product values (0,3,'Apple iPhone 8, 64GB, Gold ',300.00,'images/smartphones/7.png',0);
insert into product values (0,3,'Apple iPhone 11, 64GB, Black ',659.99,'images/smartphones/8.png',0);
insert into product values (0,3,'Samsung Galaxy S20 Ultra 5G Factory Unlocked',1199.99,'images/smartphones/9.png',0);
insert into product values (0,4,'AmazonBasics 3.5 mm Male to Male Stereo',6.38,'images/audio/7.png',0);
insert into product values (0,4,'TEWELL Computer Speaker, HD 24W',49.99,'images/audio/8.png',0);
insert into product values (0,4,'VIZIO SB2920-C6 29-Inch 2.0',117.99,'images/audio/9.png',0);
insert into product values (0,4,'PreSonus AudioBox USB 96 2x2 USB ',99.95,'images/audio/10.png',0);
insert into product values (0,4,'Polk Audio T15 100 Watt Home Theater ',69.99,'images/audio/11.png',0);
insert into product values (0,4,'SAMSUNG HW-T450 2.1ch Soundbar ',147.99,'images/audio/12.png',0);
insert into product values (0,4,'Skar Audio RP-2000.1D Monoblock Class D',99.95,'images/audio/13.png',0);
insert into product values (0,3,'Samsung Galaxy A20s A207M/DS',168.99,'images/smartphones/10.png',0);
insert into product values (0,3,'Pixel 4 - Clearly White - 64GB ',549.00,'images/smartphones/11.png',0);
insert into product values (0,3,'Moto G7 with Alexa Hands-Free – Unlocked ',199.99,'images/smartphones/12.png',0);
insert into product values (0,3,'Samsung Galaxy Note20 5G Factory Unlocked',799.00,'images/smartphones/13.png',0);
insert into product values (0,3,'TCL 10L, Unlocked Android Smartphone',249.99,'images/smartphones/14.png',0);
---------------------------COUNTRY-------------------------
INSERT INTO `country` (`id`, `name`) VALUES (NULL, 'Ecuador'), (NULL, 'United States');

---------------------------CITY-------------------------
INSERT INTO `city` (`id_country`, `name`) VALUES ('1', 'Quito'), ('1', 'Guayaquil');
INSERT INTO `city` (`id_country`, `name`) VALUES ('1', 'Cuenca'), ('1', 'Loja');
INSERT INTO `city` (`id_country`, `name`) VALUES ('1', 'Ambato'), ('1', 'Ibarra');
INSERT INTO `city` (`id_country`, `name`) VALUES ('2', 'Boston'), ('2', 'New York');
INSERT INTO `city` (`id_country`, `name`) VALUES ('2', 'Salt Lake City'), ('2', 'Detroit');
INSERT INTO `city` (`id_country`, `name`) VALUES ('2', 'Chicago'), ('2', 'New Jersey');


---------------------------ROLE-------------------------
INSERT INTO `role` (`id`, `name`) VALUES (NULL, 'ADMIN'), (NULL, 'EMPLOYEE');
INSERT INTO `role` (`id`, `name`) VALUES (NULL, 'NEWS_WRITER');

---------------------------USER-------------------------
insert into user values (0,'user1','Juan López',1, 'Quito', 'juan.lopez@gmail.com','0a041b9462caa4a31bac3567e0b6e6fd9100787db2ab433d96f6d178cabfce90');
insert into user values (0,'user2','Hernán Paredes',1, 'Quito', 'hernan01@hotmail.com','6025d18fe48abd45168528f18a82e265dd98d421a7084aa09f61b341703901a3');
insert into user values (0,'user3','Ana Carrión',1, 'Quito', 'anita_99@hotmail.com','5860faf02b6bc6222ba5aca523560f0e364ccd8b67bee486fe8bf7c01d492ccb');
INSERT INTO `user` (`id`, `username`, `fullname`, `id_country`, `city`, `email`, `passwd`) VALUES (NULL, 'user_writer', 'Juan Rulfo', '2', 'Boston', 'writer@shop.com', '05d2fae99137b000835d07d06cbec12210acdeca65d7f70721973672514ffccc')

---------------------------USER_ROLE-------------------------
INSERT INTO `user_role` (`id_role`, `username_user`) VALUES ('1', 'user1'), ('2', 'user2');
INSERT INTO `user_role` (`id_role`, `username_user`) VALUES ('3', 'user_writer');


---------------------------NEWS_CATEGORY-------------------------
INSERT INTO `news_category` (`id`, `name`) VALUES (NULL, 'POLITICS');
INSERT INTO `news_category` (`id`, `name`) VALUES (NULL, 'ECONOMY');


---------------------------NEWS-------------------------
INSERT INTO `news` (`id`, `author_user`, `publish_date`, `title`, `description`, `url`, `content_html`, `id_news_category`) VALUES (NULL, 'user_writer', CURRENT_TIMESTAMP, 'Toque de queda, teletrabajo', 'Policías realizan controles en Carapungo, norte de Quito, para prevenir el brote del covid-19.', 'https://www.elcomercio.com/actualidad/excepcion-pandemia-cambios-movilidad-teletrabajo.html', 'El 12 de septiembre de 2020 terminará el estado de excepción en Ecuador y, pese a que supera los 100 000 contagios y las 10 000 muertes por covid-19, no será renovado, informó este miércoles 26 de agosto del 2020 la ministra de Gobierno, María Paula Romo. “La Corte Constitucional dictaminó que el actual estado de excepción será el último, sobre la calamidad pública por la pandemia del covid-19”, señaló Romo en su cuenta de Twitter. Después de la culminación del actual estado de excepción no habrá restricción en dos medidas: libertad de tránsito y libertad de asociación, puntualizó este miércoles Juan Zapata, director general del Servicio Integrado de Seguridad ECU-911. Esto rige desde el 13 de septiembre 2020. Los cambios son dos: Toque de queda Tras la finalización del estado de excepción regresa la libertad para movilizarse en el país a cualquier hora. No habrá toque de queda en el Ecuador ni controles policiales para que se cumpla esta medida. Reuniones No habrá restricciones en el derecho a la libre asociación. Las reuniones estarán permitidas. El Gobierno informó que desde el 13 de septiembre arrancará una nueva etapa para afrontar la pandemia del covid-19: la autorregulación. Por ello el Gobierno Nacional presentó la campaña \'Yo me cuido\', que tiene como objetivo crear conciencia en la ciudadanía sobre la necesidad de protegerse, es decir, mantener los protocolos de bioseguridad: lavado de manos, distanciamiento social, uso obligatorio de la mascarilla y evitar aglomeraciones. En cuanto al teletrabajo, Zapata dijo que se seguirá privilegiando dicha modalidad laboral conforme a lo establecido por el Ministerio de Trabajo. El uso de playas, espacios públicos y la movilidad de vehículos es competencia de los Gobiernos Autónomos Descentralizados (GAD), por lo que serán las autoridades locales las que decidan cómo proceder en ese ámbito, agregó. En aquellos cantones donde no hay esta figura será el Gobierno Nacional el que tome las resoluciones. “Hay que coordinar con la Asociación de Municipalidades Ecuatorianas (AME) para que las ordenanzas vayan en la misma línea de la semaforización, es decir, que no sean diferentes y que generen complicaciones a nivel nacional”, dijo Zapata. De igual manera, señaló que el Comité de Operaciones de Emergencia (COE) seguirá actuando sin la necesidad de que rija un estado de excepción, es decir que, se seguirán generando resoluciones, pero con la base legal ordinaria.', '1');
INSERT INTO `news` (`id`, `author_user`, `publish_date`, `title`, `description`, `url`, `content_html`, `id_news_category`) VALUES (NULL, 'user_writer', CURRENT_TIMESTAMP, 'Noticia 2', 'Descripción ingenios y atrayente', 'https://google.com', '<p> Hola </p>', '1'), (NULL, 'user_writer', CURRENT_TIMESTAMP, 'Noticia 3', 'Impactante', 'https://google.com', '<li> ol </ol>', '2');

---------------------------SOURCE-------------------------
INSERT INTO `source` (`id_news`, `url`, `name`) VALUES ('1', 'https://www.elcomercio.com/actualidad/excepcion-pandemia-cambios-movilidad-teletrabajo.html', 'El comercio');

---------------------------USER_VIEW_NEWS-------------------------
INSERT INTO `user_view_news` (`id_news`, `username_user`, `date_view`) VALUES ('1', 'user3', CURRENT_TIMESTAMP);

---------------------------ORDERS-------------------------
insert into orders values (0, 'user1', '2020-01-01 10:10:10', 2999.95);
insert into orders values (0, 'user1', '2020-01-01 11:11:11', 29.99);
insert into orders values (0, 'user1', '2020-01-01 12:12:12', 159.99);
insert into orders values (0, 'user1', '2020-08-29 00:52:45',  199.99);
insert into orders values (0, 'user1', '2020-08-29 01:04:45',  199.99);
insert into orders values (0, 'user1', '2020-01-01 01:05:12', 159.99);
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
--5-- rating average
-- select avg(rating) from user_product_rating where id_product=12 group by id_product;
--6-- update average
-- update product set avgrating=3.00 where id_product=12;
---------------------------ORDER_DETAILS-------------------------
insert into order_details values (0,1,2,5,2999.95);
insert into order_details values (0,2,3,1,29.99);
insert into order_details values (0,3,6,1,59.99);
insert into order_details values (0,4,5,1,199.99);
insert into order_details values (0,5,5,1,199.99);
insert into order_details values (0,6,6,1,159.99);


---------------------------USER_PRODUCT_RATING-------------------------
--Ingresar ratings usuario-producto manualmente únicamente si se ingresaron órdenes y detalles_ordenes
--manualmente de los mismos usuarios con los mismos productos, de lo contrario, existirá inconsistencia.
INSERT INTO `user_product_rating` (`username_user`, `id_product`, `rating`) VALUES ('user1', '2', '5'), ('user1', '3', '4'), ('user1', '6', '2'),('user1','5', NULL);
 