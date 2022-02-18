CREATE TABLE data(
	Time VARCHAR(255) not null,
	Sol_V FLOAT not null,
	Sol_I FLOAT not null,
	Bat_V FLOAT not null,
	Chg_I FLOAT not null,
	Load_V FLOAT not null,
	Load_I FLOAT not null,
	Load_W FLOAT not null,
	Bat_T FLOAT not null,
	Dev_T FLOAT not null,
	Bat_Chg FLOAT not null,
	Dev_ID VARCHAR(10) not null,
	primary key(Time,Dev_ID)
) PARTITION BY RANGE (Time);

