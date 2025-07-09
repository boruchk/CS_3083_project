SELECT * FROM Flight WHERE departure_datetime > NOW();

SELECT * FROM Flight WHERE status='delayed';

SELECT name FROM Customer WHERE email IN (SELECT DISTINCT customer_email FROM Ticket);

SELECT * FROM Airplane WHERE airline_name='JetBlue';