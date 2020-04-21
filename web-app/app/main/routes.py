# -*- encoding: utf-8 -*-
"""
License: MIT
"""

from app.main import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager, db
from app import constants as c
from jinja2 import TemplateNotFound
from flask import jsonify
import time
import json
from functools import wraps
from flask import redirect, request, current_app
import math
from functools import lru_cache


from app.main.patients.models import Patient, PatientStatus
from app.main.models import Region, Infected_Country_Category, Address
from app.main.hospitals.models import Hospital, Hospital_Type

from datetime import datetime
from app.main.forms import TableSearchForm
import json
import requests
from flask_babelex import _
from sqlalchemy import exc


import math
from sqlalchemy import text
import geohash
import uuid

@blueprint.route('/index', methods=['GET'])
@login_required
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login_blueprint.login'))

    q = Patient.query

    if not current_user.is_admin:
        q = q.filter_by(region_id=current_user.region_id)

    last_five_patients = []
    for p in q.order_by(Patient.id.desc()).limit(5).all():
        last_five_patients.append(p)

    # coordinates_patients = []
    # for p in q.all():
    #     if p.home_address.lat:
    #         coordinates_patients.append(p)

    patients = q.all()
    regions_list = Region.query.all()

    regions = dict()
    in_hospital_id = PatientStatus.query.filter_by(value=c.in_hospital[0]).first().id

    for region in regions_list:
        patient_region_query = Patient.query.filter_by(region_id=region.id)

        found_count = patient_region_query.filter_by(is_found=True).count()
        infected_count = patient_region_query.filter_by(is_infected=True).count()

        regions[region.name] = (found_count, infected_count)

    return route_template('index', last_five_patients=last_five_patients, regions=regions, constants=c)


@blueprint.route('/<template>')
def route_template(template, **kwargs):
    if not current_user.is_authenticated:
        return redirect(url_for('login_blueprint.login'))
    try:
        q = Patient.query

        if not current_user.is_admin:
            q = q.filter_by(region_id=current_user.region_id)

        # Total Patients
        total = q.filter_by().count()

        # Is Found
        is_found = q.filter_by(is_found=True).count()
        ratio = 0 if total == 0 else is_found / total
        is_found_str = str("{}/{} ({}%)".format(is_found, total, format(ratio * 100, '.2f')))

        # In Hospital
        in_hospital_status_id = PatientStatus.query.filter_by(value=c.in_hospital[0]).first().id
        in_hospital = q.filter_by(status_id=in_hospital_status_id).count()
        ratio = 0 if is_found == 0 else in_hospital / is_found
        in_hospital_str = str("{}/{} ({}%)".format(in_hospital,
                                                   is_found, format(ratio * 100, '.2f')))

        # Is Infected
        is_infected = q.filter_by(is_infected=True).count()
        ratio = 0 if total == 0 else is_infected / total
        is_infected_str = str("{}/{} ({}%)".format(is_infected, total, format(ratio * 100, '.2f')))

        return render_template(template + '.html', total_kz_patients=str(total), is_found_str=is_found_str,
                               in_hospital_str=in_hospital_str, is_infected_str=is_infected_str, **kwargs)

    except TemplateNotFound:
        return render_template('errors/error-404.html'), 404

    # except:
        # return render_template('error-500.html'), 500


@blueprint.route("/get_hospital_by_region", methods=['POST'])
def get_hospital_by_region():
    if not current_user.is_authenticated:
        return redirect(url_for('login_blueprint.login'))

    region_id = request.form.get("region_id")
    hospital_type_id = request.form.get("hospital_type_id")

    hospitals = Hospital.query.filter_by(region_id=int(
        region_id), hospital_type_id=int(hospital_type_id))

    hospitals_options = "".join(
        ["<option value='{}'>{}</option>".format(h.id, h.name) for h in hospitals])

    return json.dumps(hospitals_options, ensure_ascii=False)


@blueprint.route('/countries_categories')
@login_required
def countries_categories():
    if not current_user.is_authenticated:
        return redirect(url_for('login_blueprint.login'))

    categories = Infected_Country_Category.query.all()

    return route_template('countries_categories', categories=categories)


@blueprint.route("/help", methods=['POST'])
@login_required
def help_route():
    return render_template('help.html')

# move to another dir


def support_jsonp(f):
    """Wraps JSONified output for JSONP"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + str(f().data.decode("utf-8")) + ')'
            return current_app.response_class(content, mimetype='application/json')
        else:
            return f(*args, **kwargs)
    return decorated_function


# def deg2num(lat_deg, lon_deg, zoom):
#     lat_rad = math.radians(lat_deg)
#     n = 2.0 ** zoom
#     xtile = int((lon_deg + 180.0) / 360.0 * n)
#     ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
#     return (xtile, ytile)

# def num2deg(xtile, ytile, zoom):
#     n = 2.0 ** zoom
#     lon_deg = xtile / n * 360.0 - 180.0
#     lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
#     lat_deg = math.degrees(lat_rad)
#     return (lat_deg, lon_deg)

@blueprint.route("/patients_content_by_id", methods=['POST'])
def patients_content_by_id():
    if not current_user.is_authenticated:
        return redirect(url_for('login_blueprint.login'))
    ids = request.get_json()
    if not "ids" in ids:
        return render_template('errors/error-400.html'), 400

    ids = ids["ids"]

    q = Patient.query

    response = []

    for i in ids:
        p = None
        try:
            p = q.filter_by(id=i).first()
        except exc.SQLAlchemyError:
            return render_template('errors/error-400.html'), 400
        if not p:
            continue
        is_found = "Нет"
        is_infected = "Нет"
        if p.is_found:
            is_found = "Да"
        if p.is_infected:
            is_infected = "Да"
        response.append({
            "id": i,
            "balloonContent": '<a href="/patient_profile?id=' + str(p.id) + '">' + repr(p) + '</a><br><strong>Регион</strong>:' + repr(p.region) + '<br><strong>Адрес</strong>: ' + repr(p.home_address) + '<br><strong>Найден</strong>: ' + is_found + '<br><strong>Инфицирован</strong>: ' + is_infected + '<br><strong>Статус</strong>:' + p.status.name + '<br>',
            "clusterCaption": repr(p)
        })

    return jsonify(response)

def is_geohash_in_bounding_box(current_geohash, bbox_coordinates):
    """Checks if the box of a geohash is inside the bounding box

    :param current_geohash: a geohash
    :param bbox_coordinates: bounding box coordinates
    :return: true if the the center of the geohash is in the bounding box
    """

    coordinates = geohash.decode(current_geohash)
    geohash_in_bounding_box = (bbox_coordinates[0] <= coordinates[0] <= bbox_coordinates[2]) and (
            bbox_coordinates[1] <= coordinates[1] <= bbox_coordinates[3])
    return geohash_in_bounding_box

def compute_geohash_tiles(bbox_coordinates, precision):
    """Computes all geohash tile in the given bounding box

    :param bbox_coordinates: the bounding box coordinates of the geohashes
    :return: a list of geohashes
    """

    checked_geohashes = set()
    geohash_stack = set()
    geohashes = []
    center_latitude = (bbox_coordinates[0] + bbox_coordinates[2]) / 2
    center_longitude = (bbox_coordinates[1] + bbox_coordinates[3]) / 2

    center_geohash = geohash.encode(center_latitude, center_longitude, precision=precision)
    geohashes.append(center_geohash)
    geohash_stack.add(center_geohash)
    checked_geohashes.add(center_geohash)
    while len(geohash_stack) > 0:
        current_geohash = geohash_stack.pop()
        neighbors = geohash.neighbors(current_geohash)
        for neighbor in neighbors:
            if neighbor not in checked_geohashes and is_geohash_in_bounding_box(neighbor, bbox_coordinates):
                geohashes.append(neighbor)
                geohash_stack.add(neighbor)
                checked_geohashes.add(neighbor)
    return geohashes

def support_jsonp(f):
    """Wraps JSONified output for JSONP"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + str(f().data.decode("utf-8")) + ')'
            return current_app.response_class(content, mimetype='application/json')
        else:
            return f(*args, **kwargs)
    return decorated_function

@blueprint.route("/patients_within_tiles")
@login_required
@support_jsonp
def patients_within_tiles():
    if not current_user.is_authenticated:
        return redirect(url_for('login_blueprint.login'))
    if not "bbox" in request.args or not "zoom" in request.args:
        return render_template('errors/error-400.html'), 400
    latlng = request.args["bbox"].split(',')
    bbox_x1 = float(latlng[0])
    bbox_y1 = float(latlng[1])
    bbox_x2 = float(latlng[2])
    bbox_y2 = float(latlng[3])

    zoom = int(request.args["zoom"])

    precision = 2
    if zoom >= 17:
        precision = 8
    elif zoom >= 15:
        precision = 7
    elif zoom >= 13:
        precision = 6
    elif zoom >= 11:
        precision = 5
    elif zoom >= 8:
        precision = 4
    elif zoom >= 6:
        precision = 3
    elif zoom >= 3:
        precision = 2
    
    hashes = compute_geohash_tiles((bbox_x1, bbox_y1, bbox_x2, bbox_y2), precision)

    coordinates_patients = {
        "type": "FeatureCollection",
        "features": []
    }

    for h in range(len(hashes)):
        sql = text("""
            SELECT SUM(1) FROM "Address" WHERE geohash LIKE '{0}%'
        """.format(hashes[h]))
        m = db.engine.execute(sql)
        for a in m:
            for z in a:
                c = z
        if c:
            lat, lon = geohash.decode(hashes[h])
            coordinates_patients["features"].append(
                {
                    "type": 'Cluster',
                    "id": uuid.uuid1(),
                    "number": c,
                    "geometry": {
                        "type": 'Point',
                        "coordinates": [lat, lon]
                    },
                    "properties": {
                        "balloonContent": "идет загрузка...",
                        "clusterCaption": "идет загрузка...",
                        "iconContent": c,
                    }
                }
            )
    return jsonify(coordinates_patients)
