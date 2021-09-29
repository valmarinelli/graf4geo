CREATE TABLE data(
	Time VARCHAR(255) not null,
	Sol_V DOUBLE PRECISION not null,
	Sol_I DOUBLE PRECISION not null,
	Bat_V DOUBLE PRECISION not null,
	Chg_I DOUBLE PRECISION not null,
	Load_V DOUBLE PRECISION not null,
	Load_I DOUBLE PRECISION not null,
	Load_W DOUBLE PRECISION not null,
	Bat_T DOUBLE PRECISION not null,
	Bat_Chg DOUBLE PRECISION not null,
	primary key(Time)
);

