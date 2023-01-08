BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Pizza" (
	"PizzaName"	TEXT,
	"TwentyFive"	INTEGER,
	"Thirty"	INTEGER,
	"ThirtyFive"	INTEGER,
	"image"	TEXT,
	"caption"	TEXT
);
CREATE TABLE IF NOT EXISTS "Customers" (
	"User_id"	INTEGER,
	"Name"	TEXT,
	"Last_time_of_using"	INTEGER,
	"Last_sum_of_order"	TEXT,
	"Total_sum_of_orders"	NUMERIC
);
CREATE TABLE IF NOT EXISTS "admin" (
	"ID_of_chat"	INTEGER,
	"Phone"	TEXT
);
CREATE TABLE IF NOT EXISTS "Token" (
	"Bot_Token"	TEXT,
	"Pay_Token"	TEXT
);
CREATE TABLE IF NOT EXISTS "Shops" (
	"Address"	TEXT
);
INSERT INTO Pizza VALUES ('Четыре сыра',489,739,889,'c1b205fe56e54b60a17911e5ae3ba7c3_1875x1875.png','Сыр блю чиз, смесь сыров чеддер и пармезан, моцарелла, фирменный соус альфредо');
INSERT INTO Pizza VALUES ('Ветчина и сыр',329,539,649,'06c75b36952747a694a169662cb3267b_584x584.png','Ветчина, моцарелла, фирменный соус альфредо');
INSERT INTO Pizza VALUES ('Маргарита',389,599,729,'13599e4aa568443ca2ac2c93f37e6df7_584x584.png','Увеличенная порция моцареллы, томаты, итальянские травы, фирменный томатный соус');
INSERT INTO Pizza VALUES ('Мясная',489,739,889,'5f11f129fd7448ef90d3057730f739d9_584x584.png','Цыпленок, ветчина, пикантная пепперони, острая чоризо, моцарелла, фирменный томатный соус');
INSERT INTO Pizza VALUES ('Пепперони фреш',299,519,639,'a55f23f650344e1bb5bd43c7fc6e82fc_584x584.png','Пикантная пепперони, увеличенная порция моцареллы, томаты, фирменный томатный соус');
INSERT INTO Pizza VALUES ('Домашняя',439,669,829,'f18ea4dd3cb64521a4bcf885fdc9f097_584x584.png','Пикантная пепперони, ветчина, маринованные огурчики, томаты, моцарелла, фирменный томатный соус');
INSERT INTO Pizza VALUES ('Цыплёнок барбекю',489,739,889,'03696708a015402c96b8875fcd98b19e_584x584.png','Цыпленок, бекон, соус барбекю, красный лук, моцарелла, фирменный томатный соус');
INSERT INTO Pizza VALUES ('Песто',489,739,889,'2a8c59ed778243b0b024ca6a5426c747_584x584.png','Цыпленок, соус песто, кубики брынзы, томаты, моцарелла, фирменный соус альфредо');
INSERT INTO Customers VALUES (345553465,'Саша',NULL,'0',NULL);
INSERT INTO Customers VALUES (1490752843,'Арсений',NULL,'0',NULL);
INSERT INTO admin VALUES (1490752843,'89645188008');
INSERT INTO Token VALUES ('5656237171:AAHstiKeRWN88t1874TtAhXRzEalLw6xrSc','401643678:TEST:71ebed0e-415b-46e4-bd71-c1a5df2666bd');
INSERT INTO Shops VALUES ('Адрес номер 1');
INSERT INTO Shops VALUES ('Адрес номер 2');
INSERT INTO Shops VALUES ('Адрес номер 3');
COMMIT;
