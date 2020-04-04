# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from app.main import blueprint

from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from flask_babelex import _

from app import login_manager, db
from app import constants as c
from jinja2 import TemplateNotFound

from app.main.models import Region, Foreign_Country, Infected_Country_Category, TravelType, BorderControl, VariousTravel
from app.main.patients.models import Patient, PatientStatus, ContactedPersons
from app.main.hospitals.models import Hospital, Hospital_Type, Hospital_Nomenklatura
from app.main.flights.models import FlightCode, FlightTravel

from app.main.new_patients.forms import PatientForm, UpdateProfileForm, AddFlightFromExcel
from app.main.forms import TableSearchForm

from app.main.routes import route_template

from datetime import datetime
from flask_uploads import UploadSet
from flask import jsonify

import pandas as pd
import numpy as np
import math, json, re, itertools
import nltk
import dateutil.parser
import requests

from multiprocessing.pool import ThreadPool as threadpool
from app.main.util import get_regions, get_regions_choices, get_flight_code
from app.login.util import hash_pass
from sqlalchemy import func

def prepare_patient_form(patient_form):
    if not patient_form.region_id.choices:
        patient_form.region_id.choices = get_regions_choices(current_user, False)
        patient_form.hospital_region_id.choices = get_regions_choices(current_user, False)

    if not patient_form.travel_type.choices:
        patient_form.travel_type.choices = [ (typ.value, typ.name) for typ in TravelType.query.all() ]

    # Flight Travel
    if not patient_form.flight_arrival_date.choices:
        dates = np.unique([f.date for f in FlightCode.query.all()])
        patient_form.flight_arrival_date.choices = [(date, date) for date in dates]
    
    if not patient_form.flight_code_id.choices:
        if patient_form.flight_arrival_date.choices:
            first_date = patient_form.flight_arrival_date.choices[0][0]
            patient_form.flight_code_id.choices = [(f.id,"{}, {} - {}".format(
                f.code, f.from_city, f.to_city)) for f in FlightCode.query.filter_by(date=first_date).all()]
        else:
            patient_form.flight_code_id.choices = []

    t_ids = {}
    for typ in TravelType.query.all():
        t_ids[typ.value] = typ.id

    travel_id_form = [(t_ids[c.by_auto_type[0]], patient_form.auto_border_id),
                      (t_ids[c.by_foot_type[0]], patient_form.foot_border_id),
                      (t_ids[c.by_sea_type[0]], patient_form.sea_border_id)]
    # Various Travel
    for typ_id, typ_select in travel_id_form:
        if not typ_select.choices:
            borders = BorderControl.query.filter_by(travel_type_id = typ_id).all()
            typ_select.choices =[(b.id, b.name) for b in borders]

    return patient_form

@blueprint.route('/add_new_patient', methods=['GET', 'POST'])
def add_new_patient():
    if not current_user.is_authenticated:
        return redirect(url_for('login_blueprint.login'))

    patient_form = PatientForm()
    patient_form = prepare_patient_form(patient_form)

    hospitals = Hospital.query.all()
    if not patient_form.hospital_id.choices:
        patient_form.hospital_id.choices = [ (-1, c.no_hospital) ] + [(h.id, h.name) for h in hospitals]

    patient_statuses = PatientStatus.query.all()
    if not patient_form.patient_status.choices:
        patient_form.patient_status.choices = [(s.value, s.name) for s in patient_statuses]

    hospital_types = Hospital_Type.query.all()
    hospital_types = [(h.id, h.name) for h in hospital_types]

    if 'create' in request.form:
        new_dict = request.form.to_dict(flat=True)

        new_dict['dob'] = datetime.strptime(request.form['dob'], '%Y-%m-%d')

        status = request.form.get("patient_status", c.no_status[0])
        new_dict['status_id'] = PatientStatus.query.filter_by(value=status).first().id
        new_dict['is_found'] = int(new_dict['is_found']) == 1
        new_dict['is_infected'] = int(new_dict['is_infected']) == 1

        travel_type = TravelType.query.filter_by(value=new_dict['travel_type']).first()
        travel_type = None if travel_type is None else travel_type
        
        del new_dict['travel_type']
        new_dict['travel_id'] = None

        if travel_type:
            new_dict['travel_type_id'] = travel_type.id

            if travel_type.value == c.flight_type[0]:
                flight_travel = FlightTravel(flight_code_id=new_dict['flight_code_id'])
                flight_travel.seat = new_dict.get('flight_seat', None)

                db.session.add(flight_travel)
                db.session.commit()
                new_dict['travel_id'] = flight_travel.id
                del new_dict['flight_code_id']
            else:
                border_form_key = None

                if travel_type.value == c.by_auto_type[0]:
                    border_form_key = 'auto_border_id'
                elif travel_type.value == c.by_foot_type[0]:
                    border_form_key = 'foot_border_id'
                elif travel_type.value == c.by_sea_type[0]:
                    border_form_key = 'sea_border_id'
                
                if border_form_key:
                    various_travel = VariousTravel(date=new_dict['arrival_date'], 
                                                    border_control_id=new_dict[border_form_key])

                    db.session.add(various_travel)
                    db.session.commit()

                    new_dict['travel_id'] = various_travel.id

        # else we can create the user
        patient = Patient(**new_dict)
        patient.is_contacted_person = False
        
        lat_lng = get_lat_lng([(patient.home_address, Region.query.filter_by(id=patient.region_id).first().name)])[0]

        patient.address_lat = lat_lng[0]
        patient.address_lng = lat_lng[1]

        db.session.add(patient)
        db.session.commit()

        return jsonify({"patient_id": patient.id})
    else:
        return route_template( 'patients/add_person', form=patient_form, hospital_types=hospital_types, added=False, error_msg=None, c=c)

def get_lat_lng(patients):
    lat_lng = []
    for patient in patients:
        lat = None
        lng = None

        if not pd.isnull(patient[0]):
            home_address = patient[0].replace(".", ". ")
            region_name = patient[1]

            address_query = home_address

            params = dict(
                apiKey='S25QEDJvW3PCpRvVMoFmIJBHL01xokVyinW8F5Fj0pw',
            )

            home_address = re.sub(r"([0-9]+(\.[0-9]+)?)",r" \1 ", home_address).strip()
            # parsed_address = {k: v for (v, k) in parse_address(patient.home_address)}

            address_query = home_address

            params['q'] = "{}, {}".format(address_query, region_name)

            url = "https://geocode.search.hereapi.com/v1/geocode"


            resp = requests.get(url=url, params=params)
            data = resp.json()
                       
            if len(data["items"]):
                item = data["items"][0]

                item = item["position"]

                lat = item["lat"]
                lng = item["lng"]
            
        lat_lng.append((lat, lng))

    return lat_lng
