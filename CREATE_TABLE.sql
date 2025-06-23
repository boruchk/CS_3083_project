CREATE TABLE Customer(
	email VARCHAR(255),
	name VARCHAR(255),
	password VARCHAR(255),
	bldg_number VARCHAR(255),
	street_name VARCHAR(255),
	city VARCHAR(255),
	state VARCHAR(255),
	phone_number VARCHAR(10),
	passport_number VARCHAR(255),
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

CREATE TABLE Airport(
	name VARCHAR(255),
	city VARCHAR(255),
	country VARCHAR(255),
	type VARCHAR(255),
	PRIMARY KEY (name)
);

CREATE TABLE Airplane(
	airline_name VARCHAR(255),
	ID VARCHAR(255),
	seat_count INT,
	manufacturer VARCHAR(255),
	manufacture_date DATE,
	PRIMARY KEY (airline_name, ID),
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
  airline_name VARCHAR(255),
  flight_number VARCHAR(255),
  departure_datetime DATETIME,
  departure_airport_name VARCHAR(255),
  arrival_datetime DATETIME,
  arrival_airport_name VARCHAR(255),
  base_price FLOAT(10, 2),
  airplane_id VARCHAR(255),
  remaining_seats INT,
  status VARCHAR(255),
  PRIMARY KEY (airline_name, flight_number, departure_datetime),
  FOREIGN KEY (departure_airport_name) REFERENCES Airport(name),
  FOREIGN KEY (arrival_airport_name) REFERENCES Airport(name),
  FOREIGN KEY (airline_name, airplane_id) REFERENCES Airplane(airline_name, ID)
);

CREATE TABLE Ticket(
	ID INT AUTO_INCREMENT,
	customer_email VARCHAR(255),
	airline_name VARCHAR(255),
	flight_number VARCHAR(255),
  departure_datetime DATETIME,
	sold_price FLOAT(10, 2),
	card_type VARCHAR(255),
	card_number CHAR(19),
	exp_date DATE,
	purchase_datetime DATETIME,
	comments VARCHAR(1000),
	rating FLOAT(2,1),
	PRIMARY KEY (ID),
  FOREIGN KEY (customer_email) REFERENCES Customer(email),
  FOREIGN KEY (airline_name, flight_number, departure_datetime)
    REFERENCES Flight(airline_name, flight_number, departure_datetime)
);

CREATE TABLE blog(
	blog_post varchar(500),
	username varchar(50),
	ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
	FOREIGN KEY (username) REFERENCES user(username)
);