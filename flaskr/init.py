#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors


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
	if 'username' in session:
		user_type = session['user_type']
		if user_type == 'customer':
			return redirect(url_for('dashboardCustomer'))
		elif user_type == 'staff':
			return redirect(url_for('dashboardStaff'))
	
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
			'arrival_airport_name = %s'
		
	cursor.execute(cityQuery)
	departureCities = cursor.fetchall()
	cursor.execute(airportQuery)
	departureAirports = cursor.fetchall()
	cursor.execute(cityQuery)
	arrivalCities = cursor.fetchall()
	cursor.execute(airportQuery)
	arrivalAirports = cursor.fetchall()
	
	departureFlights = []
	error = None
	if departureDate and departureAirport and arrivalAirport:
		cursor.execute(flightQuery, (departureDate, 
																	departureDate,
																	departureAirport, 
																	departureDate, 
																	arrivalAirport))
		departureFlights = cursor.fetchall()
		if not departureFlights:
			error = 'No flights for those choices'

	returnFlights = []
	if roundTrip and returnDate and departureAirport and arrivalAirport:
		cursor.execute(flightQuery, (returnDate, 
																	returnDate,
																	arrivalAirport, 
																	returnDate, 
																	departureAirport))
		returnFlights = cursor.fetchall()
		if not returnFlights:
			error = 'No return flights for that date'
	
	cursor.close()
	return render_template('index.html', 
												departureCities=departureCities,
												departureAirports=departureAirports,
												arrivalCities=arrivalCities,
												arrivalAirports=arrivalAirports,
												departureFlights=departureFlights,
												returnFlights=returnFlights, 
												error=error)

# FOR BARUT AND DYLAN
@app.route('/dashboardCustomer')
def dashboardCustomer():
    if session.get('user_type') != 'customer':
        return redirect(url_for('login'))
    return render_template('dashboardCustomer.html')


@app.route('/staffDashboard')
def staffDashboard():
    if session.get('user_type') != 'customer':
        return redirect(url_for('login'))
    return render_template('staffDashboard.html')


@app.route('/purchase')
def purchase():
	error = None
	if 'username' not in session:
		error = 'Please log in before purchasing a ticket'
		return render_template('login.html', error=error)
	else:
		flight_number = request.args.get('flight_number')
		departure_datetime = request.args.get('departure_datetime')

		cursor = conn.cursor()
		flightQuery = 'SELECT * ' \
			'FROM Flight ' \
			'WHERE flight_number = %s'
		cursor.execute(flightQuery, (flight_number,))
		theFlight = cursor.fetchone()
		if theFlight is None:
			error = "Flight not found."
			return render_template('purchase.html', error=error)

		return render_template('purchase.html', theFlight=theFlight)


@app.route('/loginCustomer')
def loginCustomer():
	return render_template('loginCustomer.html')


@app.route('/loginStaff')
def loginStaff():
	return render_template('loginStaff.html')


#Authenticates the customer login
@app.route('/loginAuthCustomer', methods=['GET', 'POST'])
def loginAuthCustomer():
	email = request.form['email']
	password = request.form['password']

	cursor = conn.cursor()
	query = 'SELECT email, password FROM Customer WHERE email = %s and password = %s'
	cursor.execute(query, (email, password))
	data = cursor.fetchone()
	cursor.close()

	error = None
	if(data):
		session['username'] = email
		session['user_type'] = 'customer'
		return redirect(url_for('landingPage'))
	else:
		error = 'Invalid login or username'
		return render_template('loginCustomer.html', error=error)
	

#Authenticates the staff login
@app.route('/loginAuthStaff', methods=['GET', 'POST'])
def loginAuthStaff():
	username = request.form['username']
	password = request.form['password']

	cursor = conn.cursor()
	query = 'SELECT username, password FROM user WHERE username = %s and password = %s'
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
	email = request.form['email']
	name = request.form['name']
	password = request.form['password']
	dob = request.form['date_of_birth']
	phone_number = request.form['phone_number']
	passport_number = request.form['passport_number']
	passport_exp = request.form['passport_exp']
	passport_ctry = request.form['passport_ctry']
	bldg_number = request.form['bldg_number']
	street_name = request.form['street_name']
	city = request.form['city']
	state = request.form['state']

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
	username = request.form['username']
	password = request.form['password']
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	dob = request.form['date_of_birth']
	email = request.form['email']
	works_for = request.form['works_for']

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
