drop table if EXISTS t_house;
CREATE TABLE IF NOT EXISTS t_house (
		Id int auto_increment,
		webName varchar(255),
		houseName varchar(255),
		villageName varchar(255),
		houseNote varchar(255),
		houseTotalPrice varchar(255),
		houseUnitPrice varchar(255),
		houseAge varchar(255),
		houseArea varchar(255),
		houseSquare varchar(255),
		houseLink varchar(255),
		houseImg varchar(255),
		primary key(Id)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8;