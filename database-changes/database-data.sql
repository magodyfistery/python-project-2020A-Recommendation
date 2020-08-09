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
