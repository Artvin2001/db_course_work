


--new

create table if not exists users
(
	id int not null primary key,
	login varchar(20),
	password varchar(30),
	permission int
);

create table if not exists countries
(
	id int not null primary key,
	name varchar(45),
	continent varchar(16),
	capital varchar(25),
	population float CHECK(population > 0),
	image varchar(45),
	descr text
);

create table if not exists climate
(
	id int not null primary key,
	id_country int,
	foreign key (id_country) references countries(id),
	tur_month varchar(16),
	day_temp int,
	night_temp int,
	water_temp int
);

create table if not exists cities
(
	id int not null primary key,
	id_country int,
	foreign key (id_country) references countries(id),
	name varchar(30),
    population float CHECK(population > 0),
	sight varchar(40)
);

create table if not exists hotels
(
	id int not null primary key,
	id_country int,
	foreign key (id_country) references countries(id),
	name varchar(60),
	stars int check(stars > 0),
	beach bool, 
	all_inc bool
);

create table if not exists rooms
(
	id int not null primary key,
	id_hotel int,
	foreign key (id_hotel) references hotels(id),
	name varchar(45),
	capacity int CHECK(capacity > 0),
	floor int,
	price int
);

--countries
insert into countries(id, name, continent, capital, population, image, descr)
values
    (0, 'Испания', 'Европа', 'Мадрид', 47.3, 'C:\AtozBot\img\spain.jpg', 'Страна в Южной Европе'),
	(1, 'Объединенные Арабские Эмираты', 'Азия', 'Абу-Даби', 9.9, 'C:\AtozBot\img\uae.jpg', 'Государство в восточной части Аравийского полуострова'),
	(2, 'Греция', 'Европа', 'Афины', 10.6, 'C:\AtozBot\img\greece.jpg', 'Прекрасная страна на берегу Средиземного моря'),
	(3, 'Индонезия', 'Азия', 'Джакарта', 275.4, 'C:\AtozBot\img\indonesia.jpg', 'Сказка среди пальм, песка, улыбчивых людей и ярких храмов'),
	(4, 'Мексика', 'Северная Америка', 'Мехико', 129.8, 'C:\AtozBot\img\mexico.jpg', 'Удивительная страна, сохранившая наследие древних цивилизаций');

insert into countries(id, name, continent, capital, population, image, descr)
values
    (5, 'Швеция', 'Европа', 'Стокгольм', 10.4,'C:\AtozBot\img\sweden.jpg', 'Швеция - это страна бескрайних лесов и величественных озёр, многочисленных островов вдоль Балтийского побережья и уютных городов'),
	(6, 'Япония', 'Азия', 'Токио', 125.4, 'C:\AtozBot\img\japan.jpg', 'Япония – одно из самых развитых государств мира с тысячелетней историей, самобытной культурой и традициями'),
	(7, 'Мальдивы', 'Азия', 'Мале', 0.379, 'C:\AtozBot\img\maldives.jpg', 'Мальдивы - это удивительный архипелаг в Индийском океане'),
	(8, 'Китай', 'Азия', 'Пекин', 1442.9, 'C:\AtozBot\img\china.jpg', 'Китай является одной из самых удивительных и загадочных стран мира'),
	(9, 'Тайланд', 'Азия', 'Бангкок', 66.1, 'C:\AtozBot\img\tailand.jpg', 'Тайланд — страна жаркого солнца, ласкового моря и невероятного драйва');

insert into countries(id, name, continent, capital, population, image, descr)
values
    (10, 'Италия', 'Европа', 'Рим', 59.2, 'C:\AtozBot\img\italy.jpg', 'Крупное государство на юге Европы.'),
	(11, 'Норвегия', 'Европа', 'Осло', 5.42, 'C:\AtozBot\img\norvegiya.jpg', 'Страна контрастов и острых ощущений'),
	(12, 'Чехия', 'Европа', 'Прага', 10.7, 'C:\AtozBot\img\chezh.jpg', 'Небольшая страна в самом центре Европы'),
	(13, 'Южная Корея', 'Азия', 'Сеул', 51.26, 'C:\AtozBot\img\southkorea.jpg', 'Страна белоснежных пляжей и целебных минеральных источников'),
	(14, 'Сейшелы', 'Африка', 'Виктория', 0.99, 'C:\AtozBot\img\seychelles.jpg', 'Островное государство в Восточной Африке'); 

insert into countries(id, name, continent, capital, population, image, descr)
values
    (15, 'Вьетнам', 'Азия', 'Ханой', 99.4, 'C:\AtozBot\img\vietnam.jpg', 'Государство в Юго-Восточной Азии'),
	(16, 'Малайзия', 'Азия', 'Куала-Лумпур', 32.7, 'C:\AtozBot\img\malaisia.jpg', 'Страна контрастов и острых ощущений'),
	(17, 'Камбоджа', 'Азия', 'Пномпень', 17.3, 'C:\AtozBot\img\cambodia.jpg', 'Удивительное место на краю света'),
	(18, 'Мьянма', 'Азия', 'Нейпидо', 54.4, 'C:\AtozBot\img\mianma.jpg', 'Место с богатой историей'),
	(19, 'Филиппины', 'Азия', 'Манила', 109.9, 'C:\AtozBot\img\filipin.jpg', 'Чистое море, снорклинг, дайвинг, пляжный отдых'),
	(20, 'Сингапур', 'Азия', 'Сингапур', 5.8, 'C:\AtozBot\img\singapour.jpg', 'Азиатское чудо'); 

insert into countries(id, name, continent, capital, population, image, descr)
values
    (21, 'Франция', 'Европа', 'Париж', 67.4, 'C:\AtozBot\img\france.jpg', 'Идеальное место для романтического путешествия'),
	(22, 'Россия', 'Европа', 'Москва', 145.4, 'C:\AtozBot\img\russia.jpg', 'Самая большая страна в мире'),
	(23, 'Великобритания', 'Европа', 'Лондон', 67, 'C:\AtozBot\img\britain.jpg', 'Расположенно на одноимённом острове'),
	(24, 'Германия', 'Европа', 'Берлин', 83.3, 'C:\AtozBot\img\germany.jpg', 'Удивительная страна с тысячелетней историей'),
	(25, 'Швейцария', 'Европа', 'Цюрих', 8.5, 'C:\AtozBot\img\swiss.jpg', 'Государство в Центральной Европе');

insert into countries(id, name, continent, capital, population, image, descr)
values
    (26, 'Черногория', 'Европа', 'Подгорица', 0.62, 'C:\AtozBot\img\chern.jpg', 'Государство в Юго-Восточной Европе'),
	(27, 'Финляндия', 'Европа', 'Хельсинки', 5.5, 'C:\AtozBot\img\finland.jpg', 'Страна великолепных густых лесов'),
	(28, 'Австрия', 'Европа', 'Вена', 9, 'C:\AtozBot\img\austria.jpg', 'один из главных центров европейской культуры'),
	(29, 'Дания', 'Европа', 'Копенгаген', 5.8, 'C:\AtozBot\img\danish.jpg', 'Самая южная из стран Скандинавии'),
	(30, 'Монако', 'Европа', 'Монте-Карло', 0.03, 'C:\AtozBot\img\monaco.jpg', 'Карликовое государство');

insert into countries(id, name, continent, capital, population, image, descr)
values
    (31, 'Нидерланды', 'Европа', 'Амстердам', 17.6, 'C:\AtozBot\img\niderlands.jpg', 'Необычное место'),
	(32, 'Люксембург', 'Европа', 'Люксембург', 0.64, 'C:\AtozBot\img\lux.jpg', 'Удивительное государство'),
	(33, 'Болгария', 'Европа', 'София', 6.8, 'C:\AtozBot\img\bolgaria.jpg', 'Государство в Юго-Восточной Европе'),
	(34, 'Бельгия', 'Европа', 'Брюссель', 11.26, 'C:\AtozBot\img\belgium.jpg', 'Это драгоценный камень Европы'),
	(35, 'Исландия', 'Европа', 'Рейкьявик', 0.3, 'C:\AtozBot\img\island.jpg', 'Страна с удивительной природой');

--climate
insert into climate (id, id_country, tur_month, day_temp, night_temp, water_temp)
values
   (0, 0, 'Август', 30, 22, 25),
   (1, 1, 'Ноябрь', 30, 18, 25),
   (2, 2, 'Июль', 31, 23, 26);

insert into climate (id, id_country, tur_month, day_temp, night_temp, water_temp)
values
   (3, 3, 'Июнь', 31, 23, 30),
   (4, 4, 'Декабрь', 28, 21, 27),
   (5, 5, 'Июль', 23, 13, 18),
   (6, 6, 'Май', 22, 15, 17),
   (7, 7, 'Февраль', 30, 25, 28),
   (8, 8, 'Май', 25, 13, 15),
   (9, 9, 'Январь', 31, 22, 28); 
   
 --cities
insert into cities (id, id_country, name, population, sight)
values
   (0, 0, 'Мадрид', 3.26,'Королевский дворец в Мадриде'),
   (1, 1, 'Дубай', 3.33, 'Бурдж-Халифа'),
   (2, 2, 'Афины', 0.66, 'Афинский акрополь');
 
insert into cities (id, id_country, name, population, sight)
values
   (3, 3, 'Джакарта', 10.56,'Зоопарк Рагунан'),
   (4, 4, 'Мехико', 9.1, 'Кафедральный собор в Мехико'),
   (5, 5, 'Стокгольм', 1.98, 'Стокгольмская ратуша');

insert into cities (id, id_country, name, population, sight)
values
   (6, 6, 'Токио', 14,'Императорский дворец Токио'),
   (7, 7, 'Мале', 0.13, 'Пятничная мечеть'),
   (8, 8, 'Пекин', 21.89, 'Запретный город'),
   (9, 9, 'Бангкок', 5.67, 'Ват Пхра Кео');
 
insert into cities (id, id_country, name, population, sight)
values
   (10, 10, 'Рим', 2.7,'Колизей'),
   (11, 11, 'Осло', 0.69, 'Оперный театр'),
   (12, 12, 'Прага', 1.2, 'Карлов мост'),
   (13, 13, 'Сеул', 9.68, 'Кенбоккун'),
   (14, 14, 'Виктория', 0.024, 'Монумент свободы');

insert into cities (id, id_country, name, population, sight)
values
   (15, 15, 'Хошимин', 9.27,'Собор Сайгонской Богоматери'),
   (16, 16, 'Куала-Лумпур', 1.9, 'Мечеть Джамек'),
   (17, 17, 'Пномпень', 2.5, 'Серебряная пагода'),
   (18, 18, 'Нейпидо', 1.16, 'Золотая пагода'),
   (19, 19, 'Манила', 1.84, 'Форт Сантьяго'),
   (20, 20, 'Сингапур', 5.86, 'Ботанический сад');

insert into cities (id, id_country, name, population, sight)
values
   (21, 21, 'Париж', 2.14,'Эйфелева башня'),
   (22, 22, 'Москва', 12.6, 'Московский Кремль'),
   (23, 23, 'Лондон', 8.9, 'Биг-Бен'),
   (24, 24, 'Берлин', 3.6, 'Брвнденбургские ворота'),
   (25, 25, 'Цюрих', 0.43, 'Гроссмюнстер');

insert into cities (id, id_country, name, population, sight)
values
   (26, 26, 'Подгорица', 0.17,'Монастырь Дайбабе'),
   (27, 27, 'Хельсинки', 0.65, 'Собор Святого Николая'),
   (28, 28, 'Вена', 1.9, 'Венская опера'),
   (29, 29, 'Копенгаген', 0.79, 'Парк Тиволи'),
   (30, 30, 'Монте-Карло', 0.002, 'Казино');

insert into cities (id, id_country, name, population, sight)
values
   (31, 31, 'Амстердам', 0.87,'Аудекерк'),
   (32, 32, 'Люксембург', 0.64, 'Дворец великих герцогов'),
   (33, 33, 'София', 1.2, 'Храм Александра Невского'),
   (34, 34, 'Брюссель', 0.18, 'Базилика Сакре-Кер'),
   (35, 35, 'Рейкьявик', 0.13, 'Хатльгримскиркья');

-- hotels
insert into hotels(id, id_country, name, stars, beach, all_inc)
values
    (0, 1, 'Rixos Bab Al Bahr', 5, true, false),
	(1, 1, 'Atlantis - The Palm', 5, true, false),
	(3, 0, 'Sol Costa Daurada', 4, false, false),
	(4, 0, 'Best San Diego', 4, false, true);

insert into hotels(id, id_country, name, stars, beach, all_inc)
values
    (5, 2, 'Grecotel Creta Palace', 5, true, true),
	(6, 2, 'Pilot Beach Resort', 5, true, true),
	(7, 3, 'Intercontinental Bali Resort', 5, true, false),
	(2, 3, 'The Apurva Kempinski Bali', 5, true, true);	

insert into hotels(id, id_country, name, stars, beach, all_inc)
values
    (8, 4, 'Iberostar Parasio del Mar', 4, true, true),
	(9, 4, 'Grand Riviera Princess', 4, true, true),
	(10, 5, 'Victory Hotel', 4, false, false),
	(11, 5, 'Comfort Hotel Xpress Stockholm Central', 3, false, false);

insert into hotels(id, id_country, name, stars, beach, all_inc)
values
    (12, 6, 'Tokyo Dome Hotel', 4, false, false),
	(13, 6, 'Sequence Suidobashi Tokyo', 3, false, false),
	(14, 7, 'Sheraton Maldives Full Moon Resort & SPA', 5, true, true),
	(15, 7, 'Heritance Aarah - All Inclusive', 5, true, true);

insert into hotels(id, id_country, name, stars, beach, all_inc)
values
    (16, 8, 'Resort Intime Sanya', 5, true, true),
	(17, 8, 'Shangri-La Beijing', 5, false, false),
	(18, 9, 'Pattaya Park Beach Resort', 3, true, true),
	(19, 9, 'Hilton Phuket Arcadia Resort & SPA', 5, true, true);

-- rooms
COPY rooms FROM 'C:/AtozBot/rooms.csv' delimiter ',';
--
   
   
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

--roles
create role user_role;

grant select on countries to user_role;
grant select on cities to user_role;
grant select on climate to user_role;
grant select on hotels to user_role;
grant select on rooms to user_role;

create role moderator_role;

grant select on countries to moderator_role;
grant select on cities to moderator_role;
grant select, update on climate to moderator_role;
grant select, update, insert on hotels to moderator_role;
grant select, update, insert on rooms to moderator_role;

create role administrator_role with login createrole;

grant select on countries to administrator_role;
grant select on cities to administrator_role;
grant select, update on climate to administrator_role;
grant select, update, insert on hotels to administrator_role;
grant select, update, insert on rooms to administrator_role;
grant select, insert, update (permission), delete on users to administrator_role; 

create or replace function func_insert_user() 
returns trigger
as
$body$
begin
	execute format('CREATE ROLE %I LOGIN PASSWORD %L',
	cast(new.login as name), 
	cast(new.password as varchar));
	
	IF new.permission = 0 then
	    execute format('GRANT ADMINISTRATOR_ROLE TO %I',
	    cast(new.login as name));
	END IF;
	IF new.permission = 1 then
	    execute format('GRANT MODERATOR_ROLE TO %I',
	    cast(new.login as name));
	ELSE
	    execute format('GRANT USER_ROLE TO %I',
	    cast(new.login as name));  
	END IF;
	
	return new;
end;
$body$
language plpgsql;

create trigger trig_after_insert_user after insert on users
for each row execute function func_insert_user() ;

create or replace function func_update_user() 
returns trigger
as
$body$
begin
	IF new.permission = 1 then
		EXECUTE FORMAT('REVOKE user_role form
		%I', cast(new.login as name));
		
		EXECUTE FORMAT('GRANT moderator_role to %I',
		cast(new.login as name));
	ELSE
		EXECUTE FORMAT('REVOKE moderator_role from %I',
		cast(new.login as name));
		
		EXECUTE FORMAT('GRANT user_role to %I',
		cast(new.login as name));
	END IF;
	
	return new;
end;
$body$
language plpgsql;

create trigger trig_update_user after update on users
for each row execute function func_update_user();

create or replace function func_delete_user() 
returns trigger
as
$body$
begin
	EXECUTE FORMAT('DROP ROLE %I',
	cast(old.login as name));
	
	return old;
end;
$body$
language plpgsql;

create trigger trig_before_delete_user after delete on users
for each row execute function func_delete_user();
   
create or replace function get_price (days int, id_in int)
returns int as
'
declare res int;
begin
   select price
   into res
   from rooms
   where id = id_in;
   res = res * days;
   return res;
end;
' language plpgsql;

select get_price(5, 2);

create or replace function func_correct_id()
returns trigger
as
$body$
begin
    update users
	set id = id - 1
	where users.id > old.id;
	return new;
end;
$body$
language plpgsql;

create trigger trig_delete_user_id after delete on users
for each row execute function func_correct_id();

create or replace function func_price()
returns trigger
as
$body$
begin
    if new.capacity != old.capacity  and old.price = new.price then
        update rooms
	    set price = price + 100 * (new.capacity - old.capacity);
	end if;
	return new;
end;
$body$
language plpgsql;

create trigger trig_update_room after update on rooms
for each row execute function func_price();