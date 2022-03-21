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
   