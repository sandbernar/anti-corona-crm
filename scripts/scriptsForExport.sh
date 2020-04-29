### Flight
sudo -i -u postgres psql anti_corona_crm -c 'COPY ( SELECT 
	id,
	created_date,
	first_name,
	second_name,
	patronymic_name,
	gender,
	dob,
	iin,
	pass_num,
	telephone,
	email,
	is_found::text,
	is_infected::text,
	(SELECT name FROM "Region" WHERE "Region".id="Patient".region_id) AS region,
	(SELECT name FROM "PatientStatus" WHERE "PatientStatus".id="Patient".status_id) AS status,
	(SELECT name FROM "Hospital" WHERE "Hospital".id="Patient".hospital_id) AS hospital,
	(SELECT name FROM "Country" WHERE "Country".id=(SELECT country_id FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1)) AS home_country,
	(SELECT state FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_state,
	(SELECT county FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_county,
	(SELECT city FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_city,
	(SELECT street FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_street,
	(SELECT house FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_house,
	(SELECT flat FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_flat,
	(SELECT building FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_building,
	(SELECT lat FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_lat, 
	(SELECT lng FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_lng,
	(SELECT name FROM "Country" WHERE "Country".id="Patient".citizenship_id) AS citizenship,
	(SELECT name FROM "Country" WHERE "Country".id="Patient".country_of_residence_id) AS country_of_residence,
	(SELECT name FROM "TravelType" WHERE "TravelType".id="Patient".travel_type_id) AS travel_type,
	job,
	job_position,
	(SELECT name FROM "Country" WHERE "Country".id=(SELECT country_id FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1)) AS job_country,
	(SELECT state FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_state,
	(SELECT county FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_county,
	(SELECT city FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_city,
	(SELECT street FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_street,
	(SELECT house FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_house,
	(SELECT flat FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_flat,
	(SELECT building FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_building,
	(SELECT lat FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_lat, 
	(SELECT lng FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_lng,
	(SELECT infected_patient_id FROM "ContactedPersons" WHERE "ContactedPersons".contacted_patient_id="Patient".id LIMIT 1) AS infected_patient_id,
	(SELECT name FROM "Country" WHERE "Country".id=(SELECT country_id FROM "VisitedCountry" WHERE "VisitedCountry".patient_id="Patient".id LIMIT 1)) AS visited_country,
	(SELECT from_date FROM "VisitedCountry" WHERE "VisitedCountry".patient_id="Patient".id LIMIT 1) AS visited_from_date,
	(SELECT to_date FROM "VisitedCountry" WHERE "VisitedCountry".patient_id="Patient".id LIMIT 1) AS visited_to_date,

	(SELECT seat FROM "FlightTravel" WHERE "FlightTravel".patient_id="Patient".id LIMIT 1) AS flight_seat,
	(SELECT code FROM "FlightCode" WHERE "FlightCode".id=(SELECT flight_code_id FROM "FlightTravel" WHERE "FlightTravel".patient_id="Patient".id LIMIT 1) LIMIT 1) AS flight_code,
	(SELECT date FROM "FlightCode" WHERE "FlightCode".id=(SELECT flight_code_id FROM "FlightTravel" WHERE "FlightTravel".patient_id="Patient".id LIMIT 1) LIMIT 1) AS flight_date,
	(SELECT name FROM "Country" WHERE "Country".id=(SELECT from_country_id FROM "FlightCode" WHERE "FlightCode".id=(SELECT flight_code_id FROM "FlightTravel" WHERE "FlightTravel".patient_id="Patient".id  LIMIT 1)  LIMIT 1)) AS flight_from_country,
	(SELECT from_city FROM "FlightCode" WHERE "FlightCode".id=(SELECT flight_code_id FROM "FlightTravel" WHERE "FlightTravel".patient_id="Patient".id LIMIT 1) LIMIT 1) AS flight_from_city,
	(SELECT name FROM "Country" WHERE "Country".id=(SELECT to_country_id FROM "FlightCode" WHERE "FlightCode".id=(SELECT flight_code_id FROM "FlightTravel" WHERE "FlightTravel".patient_id="Patient".id LIMIT 1) LIMIT 1)) AS flight_to_country,
	(SELECT to_city FROM "FlightCode" WHERE "FlightCode".id=(SELECT flight_code_id FROM "FlightTravel" WHERE "FlightTravel".patient_id="Patient".id LIMIT 1) LIMIT 1) AS flight_to_city
 FROM "Patient" WHERE created_date>=$$2020-04-24$$ AND travel_type_id=1) TO STDOUT WITH CSV HEADER ' > FlightTravel.csv


### Train
sudo -i -u postgres psql anti_corona_crm -c 'COPY ( SELECT 
	id,
	created_date,
	first_name,
	second_name,
	patronymic_name,
	gender,
	dob,
	iin,
	pass_num,
	telephone,
	email,
	is_found::text,
	is_infected::text,
	(SELECT name FROM "Region" WHERE "Region".id="Patient".region_id) AS region,
	(SELECT name FROM "PatientStatus" WHERE "PatientStatus".id="Patient".status_id) AS status,
	(SELECT name FROM "Hospital" WHERE "Hospital".id="Patient".hospital_id) AS hospital,
	(SELECT name FROM "Country" WHERE "Country".id=(SELECT country_id FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1)) AS home_country,
	(SELECT state FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_state,
	(SELECT county FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_county,
	(SELECT city FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_city,
	(SELECT street FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_street,
	(SELECT house FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_house,
	(SELECT flat FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_flat,
	(SELECT building FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_building,
	(SELECT lat FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_lat, 
	(SELECT lng FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_lng,
	(SELECT name FROM "Country" WHERE "Country".id="Patient".citizenship_id) AS citizenship,
	(SELECT name FROM "Country" WHERE "Country".id="Patient".country_of_residence_id) AS country_of_residence,
	(SELECT name FROM "TravelType" WHERE "TravelType".id="Patient".travel_type_id) AS travel_type,
	job,
	job_position,
	(SELECT name FROM "Country" WHERE "Country".id=(SELECT country_id FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1)) AS job_country,
	(SELECT state FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_state,
	(SELECT county FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_county,
	(SELECT city FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_city,
	(SELECT street FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_street,
	(SELECT house FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_house,
	(SELECT flat FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_flat,
	(SELECT building FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_building,
	(SELECT lat FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_lat, 
	(SELECT lng FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_lng,
	(SELECT infected_patient_id FROM "ContactedPersons" WHERE "ContactedPersons".contacted_patient_id="Patient".id LIMIT 1) AS infected_patient_id,
	(SELECT name FROM "Country" WHERE "Country".id=(SELECT country_id FROM "VisitedCountry" WHERE "VisitedCountry".patient_id="Patient".id LIMIT 1)) AS visited_country,
	(SELECT from_date FROM "VisitedCountry" WHERE "VisitedCountry".patient_id="Patient".id LIMIT 1) AS visited_from_date,
	(SELECT to_date FROM "VisitedCountry" WHERE "VisitedCountry".patient_id="Patient".id LIMIT 1) AS visited_to_date,

	(SELECT departure_date FROM "Train" WHERE "Train".id=(SELECT train_id FROM "TrainTravel" WHERE "TrainTravel".patient_id="Patient".id LIMIT 1) LIMIT 1) AS train_departure_date,
	(SELECT arrival_date FROM "Train" WHERE "Train".id=(SELECT train_id FROM "TrainTravel" WHERE "TrainTravel".patient_id="Patient".id LIMIT 1) LIMIT 1) AS train_arrival_date,
	(SELECT name FROM "Country" WHERE "Country".id=(SELECT from_country_id FROM "Train" WHERE "Train".id=(SELECT train_id FROM "TrainTravel" WHERE "TrainTravel".patient_id="Patient".id LIMIT 1) LIMIT 1)) AS train_from_country,
	(SELECT from_city FROM "Train" WHERE "Train".id=(SELECT train_id FROM "TrainTravel" WHERE "TrainTravel".patient_id="Patient".id LIMIT 1) LIMIT 1) AS train_from_city,
	(SELECT name FROM "Country" WHERE "Country".id=(SELECT to_country_id FROM "Train" WHERE "Train".id=(SELECT train_id FROM "TrainTravel" WHERE "TrainTravel".patient_id="Patient".id LIMIT 1) LIMIT 1)) AS train_to_country,
	(SELECT to_city FROM "Train" WHERE "Train".id=(SELECT train_id FROM "TrainTravel" WHERE "TrainTravel".patient_id="Patient".id LIMIT 1) LIMIT 1) AS train_to_city,
	(SELECT wagon FROM "TrainTravel" WHERE "TrainTravel".patient_id="Patient".id LIMIT 1) AS train_wagon,
	(SELECT seat FROM "TrainTravel" WHERE "TrainTravel".patient_id="Patient".id LIMIT 1) AS train_seat
 FROM "Patient" WHERE created_date>=$$2020-04-24$$ AND travel_type_id=2) TO STDOUT WITH CSV HEADER ' > TrainTravel.csv


### VariousTravel
sudo -i -u postgres psql anti_corona_crm -c 'COPY ( SELECT 
	id,
	created_date,
	first_name,
	second_name,
	patronymic_name,
	gender,
	dob,
	iin,
	pass_num,
	telephone,
	email,
	is_found::text,
	is_infected::text,
	(SELECT name FROM "Region" WHERE "Region".id="Patient".region_id) AS region,
	(SELECT name FROM "PatientStatus" WHERE "PatientStatus".id="Patient".status_id) AS status,
	(SELECT name FROM "Hospital" WHERE "Hospital".id="Patient".hospital_id) AS hospital,
	(SELECT name FROM "Country" WHERE "Country".id=(SELECT country_id FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1)) AS home_country,
	(SELECT state FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_state,
	(SELECT county FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_county,
	(SELECT city FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_city,
	(SELECT street FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_street,
	(SELECT house FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_house,
	(SELECT flat FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_flat,
	(SELECT building FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_building,
	(SELECT lat FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_lat, 
	(SELECT lng FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_lng,
	(SELECT name FROM "Country" WHERE "Country".id="Patient".citizenship_id) AS citizenship,
	(SELECT name FROM "Country" WHERE "Country".id="Patient".country_of_residence_id) AS country_of_residence,
	(SELECT name FROM "TravelType" WHERE "TravelType".id="Patient".travel_type_id) AS travel_type,
	job,
	job_position,
	(SELECT name FROM "Country" WHERE "Country".id=(SELECT country_id FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1)) AS job_country,
	(SELECT state FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_state,
	(SELECT county FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_county,
	(SELECT city FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_city,
	(SELECT street FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_street,
	(SELECT house FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_house,
	(SELECT flat FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_flat,
	(SELECT building FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_building,
	(SELECT lat FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_lat, 
	(SELECT lng FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_lng,
	(SELECT infected_patient_id FROM "ContactedPersons" WHERE "ContactedPersons".contacted_patient_id="Patient".id LIMIT 1) AS infected_patient_id,
	(SELECT name FROM "Country" WHERE "Country".id=(SELECT country_id FROM "VisitedCountry" WHERE "VisitedCountry".patient_id="Patient".id LIMIT 1)) AS visited_country,
	(SELECT from_date FROM "VisitedCountry" WHERE "VisitedCountry".patient_id="Patient".id LIMIT 1) AS visited_from_date,
	(SELECT to_date FROM "VisitedCountry" WHERE "VisitedCountry".patient_id="Patient".id LIMIT 1) AS visited_to_date,

	(SELECT date FROM "VariousTravel" WHERE "VariousTravel".patient_id="Patient".id LIMIT 1) AS various_travel_date,
	(SELECT name FROM "BorderControl" WHERE "BorderControl".id=(SELECT border_control_id FROM "VariousTravel" WHERE "VariousTravel".patient_id="Patient".id LIMIT 1) LIMIT 1) AS various_travel_blockpost
 FROM "Patient" WHERE created_date>=$$2020-04-24$$ AND travel_type_id >= 3 AND travel_type_id <= 5) TO STDOUT WITH CSV HEADER ' > VariousTravel.csv

### Local
sudo -i -u postgres psql anti_corona_crm -c 'COPY ( SELECT 
	id,
	created_date,
	first_name,
	second_name,
	patronymic_name,
	gender,
	dob,
	iin,
	pass_num,
	telephone,
	email,
	is_found::text,
	is_infected::text,
	(SELECT name FROM "Region" WHERE "Region".id="Patient".region_id) AS region,
	(SELECT name FROM "PatientStatus" WHERE "PatientStatus".id="Patient".status_id) AS status,
	(SELECT name FROM "Hospital" WHERE "Hospital".id="Patient".hospital_id) AS hospital,
	(SELECT name FROM "Country" WHERE "Country".id=(SELECT country_id FROM "Address" WHERE "Address".id="Patient".home_address_id)) AS home_country,
	(SELECT state FROM "Address" WHERE "Address".id="Patient".home_address_id) AS home_state,
	(SELECT county FROM "Address" WHERE "Address".id="Patient".home_address_id) AS home_county,
	(SELECT city FROM "Address" WHERE "Address".id="Patient".home_address_id) AS home_city,
	(SELECT street FROM "Address" WHERE "Address".id="Patient".home_address_id) AS home_street,
	(SELECT house FROM "Address" WHERE "Address".id="Patient".home_address_id) AS home_house,
	(SELECT flat FROM "Address" WHERE "Address".id="Patient".home_address_id) AS home_flat,
	(SELECT building FROM "Address" WHERE "Address".id="Patient".home_address_id) AS home_building,
	(SELECT lat FROM "Address" WHERE "Address".id="Patient".home_address_id) AS home_lat, 
	(SELECT lng FROM "Address" WHERE "Address".id="Patient".home_address_id) AS home_lng,
	(SELECT name FROM "Country" WHERE "Country".id="Patient".citizenship_id) AS citizenship,
	(SELECT name FROM "Country" WHERE "Country".id="Patient".country_of_residence_id) AS country_of_residence,
	(SELECT name FROM "TravelType" WHERE "TravelType".id="Patient".travel_type_id) AS travel_type,
	job,
	job_position,
	(SELECT name FROM "Country" WHERE "Country".id=(SELECT country_id FROM "Address" WHERE "Address".id="Patient".job_address_id)) AS job_country,
	(SELECT state FROM "Address" WHERE "Address".id="Patient".job_address_id) AS job_state,
	(SELECT county FROM "Address" WHERE "Address".id="Patient".job_address_id) AS job_county,
	(SELECT city FROM "Address" WHERE "Address".id="Patient".job_address_id) AS job_city,
	(SELECT street FROM "Address" WHERE "Address".id="Patient".job_address_id) AS job_street,
	(SELECT house FROM "Address" WHERE "Address".id="Patient".job_address_id) AS job_house,
	(SELECT flat FROM "Address" WHERE "Address".id="Patient".job_address_id) AS job_flat,
	(SELECT building FROM "Address" WHERE "Address".id="Patient".job_address_id) AS job_building,
	(SELECT lat FROM "Address" WHERE "Address".id="Patient".job_address_id) AS job_lat, 
	(SELECT lng FROM "Address" WHERE "Address".id="Patient".job_address_id) AS job_lng,
	(SELECT infected_patient_id FROM "ContactedPersons" WHERE "ContactedPersons".contacted_patient_id="Patient".id) AS infected_patient_id,
	(SELECT name FROM "Country" WHERE "Country".id=(SELECT country_id FROM "VisitedCountry" WHERE "VisitedCountry".patient_id="Patient".id LIMIT 1)) AS visited_country,
	(SELECT from_date FROM "VisitedCountry" WHERE "VisitedCountry".patient_id="Patient".id LIMIT 1) AS visited_from_date,
	(SELECT to_date FROM "VisitedCountry" WHERE "VisitedCountry".patient_id="Patient".id LIMIT 1) AS visited_to_date
 FROM "Patient" WHERE created_date>=$$2020-04-24$$ AND travel_type_id = 6) TO STDOUT WITH CSV HEADER ' > Local.csv


### OldDataTravel
sudo -i -u postgres psql anti_corona_crm -c 'COPY ( SELECT 
	id,
	created_date,
	first_name,
	second_name,
	patronymic_name,
	gender,
	dob,
	iin,
	pass_num,
	telephone,
	email,
	is_found::text,
	is_infected::text,
	(SELECT name FROM "Region" WHERE "Region".id="Patient".region_id) AS region,
	(SELECT name FROM "PatientStatus" WHERE "PatientStatus".id="Patient".status_id) AS status,
	(SELECT name FROM "Hospital" WHERE "Hospital".id="Patient".hospital_id) AS hospital,
	(SELECT name FROM "Country" WHERE "Country".id=(SELECT country_id FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1)) AS home_country,
	(SELECT state FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_state,
	(SELECT county FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_county,
	(SELECT city FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_city,
	(SELECT street FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_street,
	(SELECT house FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_house,
	(SELECT flat FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_flat,
	(SELECT building FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_building,
	(SELECT lat FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_lat, 
	(SELECT lng FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_lng,
	(SELECT name FROM "Country" WHERE "Country".id="Patient".citizenship_id) AS citizenship,
	(SELECT name FROM "Country" WHERE "Country".id="Patient".country_of_residence_id) AS country_of_residence,
	(SELECT name FROM "TravelType" WHERE "TravelType".id="Patient".travel_type_id) AS travel_type,
	job,
	job_position,
	(SELECT name FROM "Country" WHERE "Country".id=(SELECT country_id FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1)) AS job_country,
	(SELECT state FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_state,
	(SELECT county FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_county,
	(SELECT city FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_city,
	(SELECT street FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_street,
	(SELECT house FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_house,
	(SELECT flat FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_flat,
	(SELECT building FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_building,
	(SELECT lat FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_lat, 
	(SELECT lng FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_lng,
	(SELECT infected_patient_id FROM "ContactedPersons" WHERE "ContactedPersons".contacted_patient_id="Patient".id LIMIT 1) AS infected_patient_id,
	(SELECT name FROM "Country" WHERE "Country".id=(SELECT country_id FROM "VisitedCountry" WHERE "VisitedCountry".patient_id="Patient".id LIMIT 1)) AS visited_country,
	(SELECT from_date FROM "VisitedCountry" WHERE "VisitedCountry".patient_id="Patient".id LIMIT 1) AS visited_from_date,
	(SELECT to_date FROM "VisitedCountry" WHERE "VisitedCountry".patient_id="Patient".id LIMIT 1) AS visited_to_date,

	(SELECT path FROM "OldDataTravel" WHERE "OldDataTravel".patient_id="Patient".id LIMIT 1) AS old_data_travel
 FROM "Patient" WHERE created_date>=$$2020-04-24$$ AND travel_type_id = 7) TO STDOUT WITH CSV HEADER ' > OldDataTravel.csv


### BlockPostTravel
sudo -i -u postgres psql anti_corona_crm -c 'COPY ( SELECT 
	id,
	created_date,
	first_name,
	second_name,
	patronymic_name,
	gender,
	dob,
	iin,
	pass_num,
	telephone,
	email,
	is_found::text,
	is_infected::text,
	(SELECT name FROM "Region" WHERE "Region".id="Patient".region_id) AS region,
	(SELECT name FROM "PatientStatus" WHERE "PatientStatus".id="Patient".status_id) AS status,
	(SELECT name FROM "Hospital" WHERE "Hospital".id="Patient".hospital_id) AS hospital,
	(SELECT name FROM "Country" WHERE "Country".id=(SELECT country_id FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1)) AS home_country,
	(SELECT state FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_state,
	(SELECT county FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_county,
	(SELECT city FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_city,
	(SELECT street FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_street,
	(SELECT house FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_house,
	(SELECT flat FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_flat,
	(SELECT building FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_building,
	(SELECT lat FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_lat, 
	(SELECT lng FROM "Address" WHERE "Address".id="Patient".home_address_id LIMIT 1) AS home_lng,
	(SELECT name FROM "Country" WHERE "Country".id="Patient".citizenship_id) AS citizenship,
	(SELECT name FROM "Country" WHERE "Country".id="Patient".country_of_residence_id) AS country_of_residence,
	(SELECT name FROM "TravelType" WHERE "TravelType".id="Patient".travel_type_id) AS travel_type,
	job,
	job_position,
	(SELECT name FROM "Country" WHERE "Country".id=(SELECT country_id FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1)) AS job_country,
	(SELECT state FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_state,
	(SELECT county FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_county,
	(SELECT city FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_city,
	(SELECT street FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_street,
	(SELECT house FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_house,
	(SELECT flat FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_flat,
	(SELECT building FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_building,
	(SELECT lat FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_lat, 
	(SELECT lng FROM "Address" WHERE "Address".id="Patient".job_address_id LIMIT 1) AS job_lng,
	(SELECT infected_patient_id FROM "ContactedPersons" WHERE "ContactedPersons".contacted_patient_id="Patient".id LIMIT 1) AS infected_patient_id,
	(SELECT name FROM "Country" WHERE "Country".id=(SELECT country_id FROM "VisitedCountry" WHERE "VisitedCountry".patient_id="Patient".id LIMIT 1)) AS visited_country,
	(SELECT from_date FROM "VisitedCountry" WHERE "VisitedCountry".patient_id="Patient".id LIMIT 1) AS visited_from_date,
	(SELECT to_date FROM "VisitedCountry" WHERE "VisitedCountry".patient_id="Patient".id LIMIT 1) AS visited_to_date,

	(SELECT date FROM "BlockpostTravel" WHERE "BlockpostTravel".patient_id="Patient".id LIMIT 1) AS blockpost_travel_date,
	(SELECT name FROM "Region" WHERE "Region".id=(SELECT region_id FROM "BlockpostTravel" WHERE "BlockpostTravel".patient_id="Patient".id LIMIT 1)) AS blockpost_travel_region
 FROM "Patient" WHERE created_date>=$$2020-04-24$$ AND travel_type_id = 8) TO STDOUT WITH CSV HEADER ' > BlockPostTravel.csv
	