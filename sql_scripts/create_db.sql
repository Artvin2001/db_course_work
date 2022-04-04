create table if not exists climate
(
	id int not null primary key,
	tur_month varchar(16),
	day_temp int,
	night_temp int,
	water_temp int
);

create table if not exists information
(
	id int not null primary key,
	capital varchar(25),
	population float CHECK(population > 0),
	image varchar(45),
	descr text
);

create table if not exists countries
(
	id int not null primary key,
	id_info int,
	foreign key (id_info) references information(id),
	name varchar(45),
	continent varchar(16)
);

insert into climate (id, tur_month, day_temp, night_temp, water_temp)
values
   (0, 'Август', 30, 22, 25),
   (1, 'Ноябрь', 30, 18, 25),
   (2, 'Июль', 31, 23, 26);
 
insert into countries(id, id_info, name, continent)
values
    (0, 3, 'Испания', 'Европа'),
	(1, 2, 'Объединенные Арабские Эмираты', 'Азия'),
	(2, 0, 'Греция', 'Европа'),
	(3, 4, 'Индонезия', 'Азия'),
	(4, 1, 'Мексика', 'Северная Америка');
	
insert into information(id, capital, population, image, descr)
values
   (0, 'Афины', 10.6, 'C:\AtozBot\img\greece.jpg', 'Прекрасная страна на берегу Средиземного моря'),
   (1, 'Мехико', 129.8, 'C:\AtozBot\img\mexico.jpg', 'Удивительная страна, сохранившая наследие древних цивилизаций'),
   (2, 'Абу-Даби', 9.9, 'C:\AtozBot\img\uae.jpg', 'Государство в восточной части Аравийского полуострова'),
   (3, 'Мадрид', 47.3, 'C:\AtozBot\img\spain.jpg', 'Страна в Южной Европе'),
   (4, 'Джакарта', 275.4, 'C:\AtozBot\img\indonesia.jpg', 'Сказка среди пальм, песка, улыбчивых людей и ярких храмов');
 
insert into information(id, capital, population, image, descr)
values
(5, 'Мале', 0.379, 'C:\AtozBot\img\maldives.jpg', 'Мальдивы - это удивительный архипелаг в Индийском океане'),
(6, 'Бангкок', 66.1, 'C:\AtozBot\img\tailand.jpg', 'Тайланд — страна жаркого солнца, ласкового моря и невероятного драйва'),
(7,'Стокгольм', 10.4,'C:\AtozBot\img\sweden.jpg', 'Швеция - это страна бескрайних лесов и величественных озёр, многочисленных островов вдоль Балтийского побережья и уютных городов'),
(8, 'Пекин', 1442.9, 'C:\AtozBot\img\china.jpg', 'Китай является одной из самых удивительных и загадочных стран мира'),
(9, 'Токио', 125.4, 'C:\AtozBot\img\japan.jpg', 'Япония – одно из самых развитых государств мира с тысячелетней историей, самобытной культурой и традициями');

insert into countries(id, id_info, name, continent)
values
    (5, 7, 'Швеция', 'Европа'),
	(6, 9, 'Япония', 'Азия'),
	(7, 5, 'Мальдивы', 'Азия'),
	(8, 8, 'Китай', 'Азия'),
	(9, 6, 'Тайланд', 'Азия');
   
   
create or replace function get_id_info(name_in char)
returns int as
'select id_info
from countries
where name = name_in;'
language sql;

create or replace function get_info_by_name(name_in char)
returns table
(
	out_id int,
	out_capital varchar,
	out_population float,
	out_image varchar,
	out_descr text
)
as
'
select * 
from information
where id = 
    (select id_info
	 from countries
	 where name = name_in
	);
'
language sql;

select * from get_info_by_name('Греция');
   