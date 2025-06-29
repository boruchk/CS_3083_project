#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors


def calculatePrice(theFlight):
	remaining_seats = theFlight['remaining_seats']
	base_price = theFlight['base_price']
	airplane_id = theFlight['airplane_id']
	price = base_price

	cursor = conn.cursor()
	airplaneQuery = 'SELECT * ' \
		'FROM Airplane ' \
		'WHERE ID = %s'
	cursor.execute(airplaneQuery, (airplane_id,))
	thePlane = cursor.fetchone()
	if thePlane:
		seat_count = thePlane['seat_count']
		seat_ratio = 1 - remaining_seats/seat_count
		if seat_ratio > 0.5:
			multiplier = (base_price/remaining_seats) * seat_ratio
			price = base_price * multiplier
		else:
			price = base_price
		price = round(price, 2)
		
	return price


def findFlight(airline_name, flight_number, departure_datetime):
	cursor = conn.cursor()
	flightQuery = 'SELECT * ' \
		'FROM Flight ' \
		'WHERE airline_name = %s AND flight_number = %s AND departure_datetime = %s;'
	cursor.execute(flightQuery, (airline_name, flight_number, departure_datetime,))
	theFlight = cursor.fetchone()
	cursor.close()
	return theFlight


#Initialize the app from Flask
app = Flask(__name__)


#Configure MySQL
conn = pymysql.connect(host='localhost',
		       						 port = 3306,
                       user='root',
                       password='',
                       db='Project',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


#Define a route to landingPage function
@app.route('/',methods=['GET', 'POST'])
def landingPage():
	departureDate = request.args.get('departureDate')
	returnDate = request.args.get('returnDate')
	roundTrip = request.args.get('roundTrip')
	departureAirport = request.args.get('departureAirports')
	arrivalAirport = request.args.get('arrivalAirports')

	cursor = conn.cursor()
	cityQuery = 'SELECT DISTINCT city FROM Airport'
	airportQuery = 'SELECT name FROM Airport'
	flightQuery = 'SELECT * ' \
		'FROM Flight ' \
		'WHERE departure_datetime >= %s and ' \
			'departure_datetime < DATE_ADD(%s, INTERVAL 1 DAY) and ' \
			'departure_airport_name = %s and ' \
			'arrival_datetime >= %s and ' \
			'arrival_airport_name = %s and ' \
			'remaining_seats > 0'
		
	cursor.execute(cityQuery)
	departureCities = cursor.fetchall()
	cursor.execute(airportQuery)
	departureAirports = cursor.fetchall()
	cursor.execute(cityQuery)
	arrivalCities = cursor.fetchall()
	cursor.execute(airportQuery)
	arrivalAirports = cursor.fetchall()
	
	departureFlights = []
	returnFlights = []
	originFlightsError=''
	returnFlightsError=''
	if departureDate and departureAirport and arrivalAirport:
		cursor.execute(flightQuery, (departureDate, 
																	departureDate,
																	departureAirport, 
																	departureDate, 
																	arrivalAirport))
		departureFlights = cursor.fetchall()

		if roundTrip and returnDate and departureAirport and arrivalAirport:
			cursor.execute(flightQuery, (returnDate, 
																		returnDate,
																		arrivalAirport, 
																		returnDate, 
																		departureAirport))
			returnFlights = cursor.fetchall()
		if not returnFlights:
			returnFlightsError = 'No return flights for that date'
	else:
		originFlightsError = 'No flights for those choices'
	
	error = None
	cursor.close()
	return render_template('index.html', 
												departureCities=departureCities,
												departureAirports=departureAirports,
												arrivalCities=arrivalCities,
												arrivalAirports=arrivalAirports,
												departureFlights=departureFlights,
												returnFlights=returnFlights, 
												originFlightsError=originFlightsError,
												returnFlightsError=returnFlightsError,
												error=error)


@app.route('/dashboardCustomer')
def dashboardCustomer():
	if session.get('user_type') != 'customer':
		return redirect(url_for('loginCustomer'))
	
	email = session.get('username')
	name = 'Customer'
	purchasedFlights = []
	userQuery = 'SELECT * FROM Customer WHERE email = %s;'
	cursor = conn.cursor()
	cursor.execute(userQuery, (email,))
	user = cursor.fetchone()
	cursor.close()

	if user:
		name = user['name']
		flightQuery = 'SELECT * ' \
		'FROM Ticket natural join Flight ' \
		'WHERE customer_email = %s;'
		cursor = conn.cursor()
		cursor.execute(flightQuery, (email,))
		purchasedFlights = cursor.fetchall()
		cursor.close()

	return render_template('dashboardCustomer.html', name=name, purchasedFlights=purchasedFlights)


@app.route('/commentAndRate', methods=['GET', 'POST'])
def commentAndRate():
	if 'username' not in session:
		return redirect(url_for('landingPage'))
	
	cursor = conn.cursor()
	ticket_id = request.args.get('ticket_id')
	ticketQuery = 'SELECT * FROM Ticket WHERE ID = %s;;'
	cursor.execute(ticketQuery, (ticket_id,))
	ticket = cursor.fetchone()
	cursor.close()

	if ticket:
		return render_template('commentAndRate.html', ticket=ticket, ticket_id=ticket_id)
	else:
		return redirect(url_for('dashboardCustomer'))


@app.route('/submitCommentAndRate', methods=['GET', 'POST'])
def submitComment():
	if 'username' not in session:
		return redirect(url_for('landingPage'))

	ticket_id = request.form.get('ticket_id')
	comment = request.form.get('comment')
	rating = request.form.get('rating')
	cursor = conn.cursor()
	commentQuery = 'UPDATE Ticket SET comments = %s, rating = %s WHERE ID = %s;'
	cursor.execute(commentQuery, (comment, rating, ticket_id,))
	cursor.close()
	if cursor.rowcount == 1:
		print('updated comment and rating')
		conn.commit()
	else:
		print('unable to update')
		conn.rollback()

	return redirect(url_for('dashboardCustomer'))


@app.route('/dashboardStaff')
def dashboardStaff():
	if session.get('user_type') != 'staff':
		return redirect(url_for('loginStaff'))
	
	username = session.get('username')
	name = 'Staff'
	workFlights = []
	userQuery = 'SELECT * FROM staff WHERE username = %s;'
	cursor = conn.cursor()
	cursor.execute(userQuery, (username,))
	user = cursor.fetchone()
	cursor.close()

	if user:
		name = user['first_name']
		airline = user['works_for']
		# default to view the flights in the next 30 days
		flightQuery = 'SELECT * FROM flight WHERE departure_datetime > CURRENT_DATE() and departure_datetime < CURRENT_DATE() + INTERVAL 30 DAY and airline_name = %s; '
		cursor = conn.cursor()
		cursor.execute(flightQuery, (airline, ))
		workFlights = cursor.fetchall()
		cursor.close()

	return render_template('dashboardStaff.html', name=name, workFlights=workFlights)


@app.route('/purchase')
def purchase():
	error = None
	airline_name = request.args.get('airline_name')
	flight_number = request.args.get('flight_number')
	departure_datetime = request.args.get('departure_datetime')

	if 'username' not in session:
		error = 'Please log in before purchasing a ticket'
		next_url = url_for('purchase', flight_number=flight_number)
		return render_template('loginCustomer.html', next=next_url, error=error)
	else:
		theFlight = findFlight(airline_name, flight_number, departure_datetime)
		if theFlight is None:
			error = "Flight not found."
			return render_template('purchase.html', error=error)

		price = calculatePrice(theFlight)
		return render_template('purchase.html', theFlight=theFlight, price=price)


@app.route('/processCard', methods=['POST'])
def process_card():
	error = None
	if 'username' not in session:
		error = 'Please log in before purchasing a ticket'
		return render_template('loginCustomer.html')
	
	card_type = request.form.get('card_type')
	card_number = request.form.get('card_number', '').strip()
	exp_date = request.form.get('exp_date')
	airline_name = request.form.get('airline_name')
	flight_number = request.form.get('flight_number')
	departure_datetime = request.form.get('departure_datetime')
	price = request.form.get('price')

	allowed_cards = ['Amex', 'Visa', 'MasterCard', 'Discover']
	if card_type not in allowed_cards or not card_number.isdigit():
		error = 'Invalid card details please try again. Please make sure to use numbers for your cc number'
		return render_template('purchase.html',
												flight_number=flight_number,
												card_number=card_number,
												exp_date=exp_date,
												error=error)
	
	email = session.get('username')
	createTicket = 'INSERT INTO ticket(' \
		'customer_email, flight_number, departure_datetime, airline_name, ' \
		'sold_price, card_type, card_number, exp_date, ' \
		'purchase_datetime, comments, rating)' \
		'values (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), null, null);'
	cursor = conn.cursor()
	flight = findFlight(airline_name, flight_number, departure_datetime)
	if flight:
		ticketValues = (email, flight_number, flight['departure_datetime'], flight['airline_name'], 
										price, card_type, card_number, exp_date)
		cursor.execute(createTicket, ticketValues)
		if cursor.rowcount == 1:
			conn.commit()
			updateFlightQuery = 'UPDATE Flight ' \
				'SET remaining_seats = remaining_seats - 1 ' \
				'WHERE airline_name = %s ' \
				'AND flight_number = %s ' \
				'AND departure_datetime = %s ' \
				'AND remaining_seats > 0;'
			cursor.execute(updateFlightQuery, (airline_name, flight_number, departure_datetime,))
			if cursor.rowcount == 1:
				conn.commit()
				print('successfully updated flight seat count')
			else:
				conn.rollback()
				print('could not update flight seat count')
		else:
			conn.rollback()

	cursor.close()
	return redirect(url_for('landingPage'))


@app.route('/loginCustomer')
def loginCustomer():
	next_url = request.args.get('next')
	return render_template('loginCustomer.html', next=next_url)


@app.route('/loginStaff')
def loginStaff():
	return render_template('loginStaff.html')


#Authenticates the customer login
@app.route('/loginAuthCustomer', methods=['GET', 'POST'])
def loginAuthCustomer():
	email = request.form.get('email', '').strip()
	password = request.form.get('password', '').strip()
	next_url = request.form.get('next')

	cursor = conn.cursor()
	query = 'SELECT email, password FROM Customer WHERE email = %s and password = %s'
	cursor.execute(query, (email, password))
	data = cursor.fetchone()
	cursor.close()

	error = None
	if(data):
		session['username'] = email
		session['user_type'] = 'customer'
		print(next_url)
		if next_url == 'None' or next_url is None:
			return redirect(url_for('landingPage'))
		else:
			return redirect(next_url)
	else:
		error = 'Invalid login or username'
		return render_template('loginCustomer.html', error=error)
	

#Authenticates the staff login
@app.route('/loginAuthStaff', methods=['GET', 'POST'])
def loginAuthStaff():
	username = request.form.get('username', '').strip()
	password = request.form.get('password', '').strip()

	cursor = conn.cursor()
	query = 'SELECT username, password FROM staff WHERE username = %s and password = %s'
	cursor.execute(query, (username, password))
	data = cursor.fetchone()
	cursor.close()

	error = None
	if(data):
		session['username'] = username
		session['user_type'] = 'staff'
		return redirect(url_for('landingPage'))
	else:
		error = 'Invalid login or username'
		return render_template('loginStaff.html', error=error)


@app.route('/registerCustomer')
def registerCustomer():
	return render_template('registerCustomer.html')


@app.route('/registerStaff')
def registerStaff():
	return render_template('registerStaff.html')


#Authenticates the customer registeration
@app.route('/registerCustomerAuth', methods=['GET', 'POST'])
def registerCustomerAuth():
	email = request.form.get('email', '').strip()
	name = request.form.get('name', '').strip()
	password = request.form.get('password', '').strip()
	dob = request.form.get('date_of_birth')
	phone_number = request.form.get('phone_number', '').strip()
	passport_number = request.form.get('passport_number', '').strip()
	passport_exp = request.form.get('passport_exp')
	passport_ctry = request.form.get('passport_ctry', '').strip()
	bldg_number = request.form.get('bldg_number', '').strip()
	street_name = request.form.get('street_name', '').strip()
	city = request.form.get('city', '').strip()
	state = request.form.get('state', '').strip()

	cursor = conn.cursor()
	# check if email/username already exists as a customer or staff 
	customer_query = 'SELECT email FROM Customer WHERE email = %s'
	staff_query = 'SELECT username FROM Staff WHERE username = %s'
	cursor.execute(customer_query, (email))
	customer = cursor.fetchone()
	cursor.execute(staff_query, (email))
	staff = cursor.fetchone()

	error = None
	if(customer or staff):
		error = "User already exists. Please use a different email address"
		return render_template('registerCustomer.html', error = error)
	else:
		ins = 'INSERT INTO Customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, (email, name, password, 
											 bldg_number, street_name, city, state, 
											 phone_number, 
											 passport_number, passport_exp, passport_ctry, 
											 dob))
		conn.commit()
		cursor.close()
		session['username'] = email
		session['user_type'] = 'customer'
		return redirect(url_for('landingPage'))
	

#Authenticates the staff registeration
@app.route('/registerStaffAuth', methods=['GET', 'POST'])
def registerStaffAuth():
	username = request.form.get('username', '').strip()
	password = request.form.get('password', '').strip()
	first_name = request.form.get('first_name', '').strip()
	last_name = request.form.get('last_name', '').strip()
	dob = request.form.get('date_of_birth')
	email = request.form.get('email', '').strip()
	works_for = request.form.get('works_for', '').strip()

	cursor = conn.cursor()
	# check if email/username already exists as a customer or staff 
	customer_query = 'SELECT email FROM Customer WHERE email = %s'
	staff_query = 'SELECT username FROM Staff WHERE username = %s'
	cursor.execute(customer_query, (email))
	customer = cursor.fetchone()
	cursor.execute(staff_query, (email))
	staff = cursor.fetchone()

	error = None
	if(customer or staff):
		error = "User already exists. Please select another username"
		return render_template('registerStaff.html', error = error)
	else:
		ins = 'INSERT INTO Staff VALUES(%s, %s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, (username, password, 
											 first_name, last_name, dob, 
											 email, works_for))
		conn.commit()
		cursor.close()
		session['username'] = username
		session['user_type'] = 'staff'
		return redirect(url_for('landingPage'))


@app.route('/logout')
def logout():
	if 'username' in session:
		session.pop('username')
		session.pop('user_type')
	return redirect('/')


app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
