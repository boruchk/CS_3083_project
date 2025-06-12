CREATE TABLE Customer(
	email VARCHAR(255),
	name VARCHAR(255),
	password VARCHAR(255),
	bldg_number INT,
	street_name VARCHAR(255),
	city VARCHAR(255),
	state VARCHAR(255),
	phone_number VARCHAR(10),
	passport_number INT,
	passport_exp DATE,
	passport_country VARCHAR(255),
	date_of_birth DATE,
	PRIMARY KEY (email)
);

CREATE TABLE Airline(
  name VARCHAR(255),
  city VARCHAR(255),
  country VARCHAR(255),
  type VARCHAR(255),
  PRIMARY KEY (name)
);

CREATE TABLE Airport (
	name VARCHAR(255),
	city VARCHAR(255),
	country VARCHAR(255),
	type VARCHAR(255),
	PRIMARY KEY (name)
);

CREATE TABLE Airplane (
	ID INT AUTO_INCREMENT,
	seat_count INT,
	manufacturer VARCHAR(255),
	manufacture_date DATE,
	airline_name VARCHAR(255),
	PRIMARY KEY (ID),
	FOREIGN KEY (airline_name) REFERENCES Airline(name)
);

CREATE TABLE Staff(
  username VARCHAR(255),
  password VARCHAR(255),
  first_name VARCHAR(255),
  last_name VARCHAR(255),
  date_of_birth DATE,
  email VARCHAR(255),
  works_for VARCHAR(255),
  PRIMARY KEY (username),
  FOREIGN KEY (works_for) REFERENCES Airline(name)
);

CREATE TABLE Phone_Number(
  username VARCHAR(255),
  phone_number VARCHAR(10),
  PRIMARY KEY (username, phone_number),
  FOREIGN KEY (username) REFERENCES Staff(username)
);

CREATE TABLE Flight(
  flight_number INT,
  departure_datetime DATETIME,
  airline_name VARCHAR(255),
  departure_airport_name VARCHAR(255),
  arrival_datetime DATETIME,
  arrival_airport_name VARCHAR(255),
  base_price FLOAT(10, 2),
  airplane_id INT,
  remaining_seats INT,
  status VARCHAR(255),
  PRIMARY KEY (flight_number, departure_datetime, airline_name),
  FOREIGN KEY (airline_name) REFERENCES Airline(name),
  FOREIGN KEY (departure_airport_name) REFERENCES Airport(name),
  FOREIGN KEY (arrival_airport_name) REFERENCES Airport(name),
  FOREIGN KEY (airplane_id) REFERENCES Airplane(ID)
);

CREATE TABLE Ticket(
	ID INT AUTO_INCREMENT,
	customer_email VARCHAR(255),
	flight_number INT,
  departure_datetime DATETIME,
	airline VARCHAR(255),
	sold_price FLOAT(10, 2),
	card_type VARCHAR(255),
	card_number CHAR(19),
	exp_date DATE,
	purchase_datetime DATETIME,
	comments VARCHAR(1000),
	rating FLOAT(2,1),
	PRIMARY KEY (ID),
  FOREIGN KEY (customer_email) REFERENCES Customer(email),
  FOREIGN KEY (flight_number, departure_datetime, airline)
    REFERENCES Flight(flight_number, departure_datetime, airline_name)
);

CREATE TABLE User(
	username varchar(50),
	password varchar(50),
	PRIMARY KEY(username)
);

CREATE TABLE blog(
	blog_post varchar(500),
	username varchar(50),
	ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
	FOREIGN KEY (username) REFERENCES user(username)
);