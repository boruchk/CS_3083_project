INSERT INTO Airline(name, city, country, type)
	values ('JetBlue', 'New York', 'United States', 'international'),
	('Spirit', 'Miami', 'United States', 'international');

INSERT INTO Airport(name, city, country, type)
	values ('JFK', 'New York', 'United States', 'international'),
	('LGA', 'New York', 'United States', 'international'),
	('LAX', 'Los Angeles', 'United States', 'international'),
	('PVG', 'Shanghai', 'China', 'international');

INSERT INTO Customer(email, name, password, bldg_number, street_name, city, state, phone_number, passport_number, passport_exp, passport_country, date_of_birth)
	values ('bu2016@nyu.edu', 'Barut Ural', 'password', '6', 'MetroTech', 'Brooklyn', 'NY', '1234567891', '157390212', '2027-06-11', 'United States', '2002-02-03'),
	('dmb9588@nyu.edu', 'Dylan Blake', 'abc123', '6', 'MetroTech', 'Brooklyn', 'NY', '2384934392', '34827354', '2027-07-30', 'United States', '2003-07-12'),
	('bk2780@nyu.edu', 'Boruch Khazanovich', '1234', '6', 'MetroTech', 'Brooklyn', 'NY', '8439573452', '3242384', '2029-01-11', 'United States', '2004-11-01');

INSERT INTO Airplane(airline_name, ID, seat_count, manufacturer, manufacture_date)
	values ('JetBlue', 'A325', 250, 'Airbus', '2005-01-15'),
	('JetBlue', 'A380', 525, 'Airbus', '2010-04-01'),
	('JetBlue', 'A345', 350, 'Airbus', '2001-06-03'),
	('Spirit', 'B532', 375, 'Boeing', '2007-09-05');

INSERT INTO Staff(username, password, first_name, last_name, date_of_birth, email, works_for)
	values ('jbstaff1', 'pswd12345', 'John', 'Doe', '1995-06-11', 'jdwork@email.com', 'JetBlue'),
	('spiritstaff1', 'pswd78910', 'Mark', 'Smith', '1999-05-15', 'marks@email.com', 'Spirit'),
	('sarausername', 'hello12345', 'Sara', 'Chase', '2001-01-29', 'sarac@email.com', 'JetBlue');

INSERT INTO Phone_number(username, phone_number)
	values ('jbstaff1', '7181111234'),
	('jbstaff1', '7181115678'),
	('spiritstaff1', '7182229876'),
	('sarausername', '7183337654');

INSERT INTO Flight(airline_name, flight_number, departure_datetime, departure_airport_name, arrival_datetime, arrival_airport_name, base_price, airplane_id, remaining_seats, status)
	values ('JetBlue','1234', '2025-06-14 08:00:00.00', 'JFK', '2025-06-14 16:00:00.00', 'LAX', 200.00, 'A325', 52, 'on time');

INSERT INTO Ticket(customer_email, flight_number, departure_datetime, airline_name, sold_price, card_type, card_number, exp_date, purchase_datetime, comments, rating)
	values ('bu2016@nyu.edu', '1234', '2025-06-14 08:00:00.00', 'JetBlue', 250.00, 'Visa', '4111111111111111', '2027-06-11', '2025-06-10 12:00:00.00', null, null);