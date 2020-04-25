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
from math import *

from app.main.patients.models import Patient, PatientStatus
from app.main.models import Region, Infected_Country_Category, Address
from app.main.hospitals.models import Hospital, Hospital_Type

from datetime import datetime
from app.main.forms import TableSearchForm
import json
import requests
from flask_babelex import _
from sqlalchemy import exc

import uuid
import os
from functools import lru_cache
import math
from sqlalchemy import text
import geohash

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


@blueprint.route("/patients_content_by_id", methods=['POST'])
def patients_content_by_id():
    if not current_user.is_authenticated:
        return redirect(url_for('login_blueprint.login'))
    req = request.get_json()
    if not "lat_lon" in req:
        return render_template('errors/error-400.html'), 400
    print("lat lon", req["lat_lon"][0])
    lat_lon = req["lat_lon"][0]

    q = Patient.query

    response = []

    p = None
    try:
        p = q.join(Address, Patient.home_address_id == Address.id).filter(Address.lat == str(lat_lon[0])).filter(Address.lng == str(lat_lon[1])).first()
    except exc.SQLAlchemyError as err:
        print(err)
        return render_template('errors/error-400.html'), 400
    if not p:
        return jsonify({})
    print(p)
    is_found = "Нет"
    is_infected = "Нет"
    if p.is_found:
        is_found = "Да"
    if p.is_infected:
        is_infected = "Да"
    response.append({
        "id": uuid.uuid1(),
        "balloonContent": '<a href="/patient_profile?id=' + str(p.id) + '">' + 'test' + '</a>',
        # "balloonContent": '<a href="/patient_profile?id=' + str(p.id) + '">' + repr(p) + '</a><br><strong>Регион</strong>:' + repr(p.region) + '<br><strong>Адрес</strong>: ' + repr(p.home_address) + '<br><strong>Найден</strong>: ' + is_found + '<br><strong>Инфицирован</strong>: ' + is_infected + '<br><strong>Статус</strong>:' + p.status.name + '<br>',
        "clusterCaption": repr(p)
    })

    return jsonify(response)


def get_ttl_hash(seconds=3600):
    """Return the same value withing `seconds` time period"""
    return round(time.time() / seconds)


@lru_cache()
def getR(bbox_x1, bbox_y1, bbox_x2, bbox_y2, ttl_hash=None):
    del ttl_hash
    r = jsonify(type="FeatureCollection", features=[i.serialize for i in Patient.query.join(Address, Patient.home_address_id == Address.id).filter(Address.lng != None).filter(Address.lat >= bbox_x1).filter(
        Address.lat <= bbox_x2).filter(Address.lng >= bbox_y1).filter(Address.lng <= bbox_y2)])
    return r


"""
ObjectLoadingManager solution
"""
# @blueprint.route("/patients_within_tiles")
# @login_required
# @support_jsonp
# def patients_within_tiles():
#     if not current_user.is_authenticated:
#         return redirect(url_for('login_blueprint.login'))
#     if not "bbox" in request.args:
#         return render_template('errors/error-400.html'), 400
#     latlng = request.args["bbox"].split(',')
#     bbox_x1 = float(latlng[0])
#     bbox_y1 = float(latlng[1])
#     bbox_x2 = float(latlng[2])
#     bbox_y2 = float(latlng[3])
#     r = getR(bbox_x1, bbox_y1, bbox_x2, bbox_y2, ttl_hash=get_ttl_hash())
#     return r

Address.bounds = classmethod(lambda s: (s.lat, s.lng))


def is_bound(lat, lng, xMin, yMin, xMax, yMax):
    a = (lng - yMax) * (lng - yMin) < 0
    b = (lat - xMax) * (lng - xMin) < 0
    return a and b
# meta.Session.query(User).filter(calc_distance(User.coords(), (my_lat, my_long)) < 5


def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)


def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)


class Point:
    def __init__(self, x, y, zoom):
        self.x = x
        self.y = y
        self.x_tile, self.y_tile = deg2num(self.x, self.y, zoom)

    def convert_to_deg(self, zoom):
        pass


class Helper:
    def __init__(self, x1, y1, x2, y2, zoom):
        self.zoom = zoom

        self.bbox_sw = Point(x1, y1, self.zoom)
        self.bbox_ne = Point(x2, y2, self.zoom)

        self.bbox_nw = Point(x2, y1, self.zoom)
        self.bbox_se = Point(x1, y2, self.zoom)

        self.w = self.bbox_se.x_tile - self.bbox_nw.x_tile + 1
        self.h = self.bbox_se.y_tile - self.bbox_nw.y_tile + 1

        print("map", self.w * self.h)



def center_geolocation(geolocations):
    """
    Provide a relatively accurate center lat, lon returned as a list pair, given
    a list of list pairs.
    ex: in: geolocations = ((lat1,lon1), (lat2,lon2),)
        out: (center_lat, center_lon)
    """


    x = 0
    y = 0
    z = 0

    for lat, lon in geolocations:
        lat = float(lat) * pi / 180
        lon = float(lon) * pi / 180
        x += cos(lat) * cos(lon)
        y += cos(lat) * sin(lon)
        z += sin(lat)

    x = float(x / len(geolocations))
    y = float(y / len(geolocations))
    z = float(z / len(geolocations))

    return (atan2(y, x) * 180 / pi, atan2(z, sqrt(x * x + y * y)) * 180 / pi)


def is_geohash_in_bounding_box(current_geohash, bbox_coordinates):
    """Checks if the box of a geohash is inside the bounding box

    :param current_geohash: a geohash
    :param bbox_coordinates: bounding box coordinates
    :return: true if the the center of the geohash is in the bounding box
    """

    coordinates = geohash.decode(current_geohash)
    # print(coordinates)
    # print(bbox_coordinates)
    geohash_in_bounding_box = (bbox_coordinates[0] <= coordinates[0] <= bbox_coordinates[2]) and (
            bbox_coordinates[1] <= coordinates[1] <= bbox_coordinates[3])
    return geohash_in_bounding_box

def build_geohash_box(current_geohash):
    """Returns a GeoJSON Polygon for a given geohash

    :param current_geohash: a geohash
    :return: a list representation of th polygon
    """

    b = geohash.bbox(current_geohash)
    polygon = [(b['w'], b['s']), (b['w'], b['n']), (b['e'], b['n']), (b['e'], b['s'],), (b['w'], b['s'])]
    return polygon

def compute_geohash_tiles(bbox_coordinates, precision):
    """Computes all geohash tile in the given bounding box

    :param bbox_coordinates: the bounding box coordinates of the geohashes
    :return: a list of geohashes
    """

    checked_geohashes = set()
    geohash_stack = set()
    geohashes = []
    # get center of bounding box, assuming the earth is flat ;)
    center_latitude = (bbox_coordinates[0] + bbox_coordinates[2]) / 2
    center_longitude = (bbox_coordinates[1] + bbox_coordinates[3]) / 2

    # print()
    center_geohash = geohash.encode(center_latitude, center_longitude, precision=precision)
    geohashes.append(center_geohash)
    geohash_stack.add(center_geohash)
    checked_geohashes.add(center_geohash)
    while len(geohash_stack) > 0:
        current_geohash = geohash_stack.pop()
        neighbors = geohash.neighbors(current_geohash)
        # print("n", neighbors)
        for neighbor in neighbors:
            if neighbor not in checked_geohashes and is_geohash_in_bounding_box(neighbor, bbox_coordinates):
                geohashes.append(neighbor)
                geohash_stack.add(neighbor)
                checked_geohashes.add(neighbor)
    return geohashes

# a = compute_geohash_tiles((51.13465311335619, 71.33693818721773, 51.16855323117143, 71.40929345760347))

# 4 0 0 4
# 0 0 4 4
# se x1 se y1 nw x2 nw y2
# sw x2 y1 x1 y2
# 51.16855323117143,71.33693818721773, 51.13465311335619,71.40929345760347
# 51.13465311335619, 71.33693818721773, 51.16855323117143, 71.40929345760347
# 51.13465311335619, 71.33693818721773, 51.16855323117143, 71.40929345760347

"""
RemoteObjectManager solution
"""
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

    """
    bbox_x1, bbox_y1 == sw geohash
    bbox_x2, bbox_y2 == ne geohash
    precision == table
    """

    zoom = int(request.args["zoom"])

    # hehe
    distance = 2
    if zoom == 17:
        distance = 0.001
    elif zoom == 16:
        distance = 0.002
    elif zoom == 15:
        distance = 0.003
    elif zoom == 14:
        distance = 0.008
    elif zoom == 13:
        distance = 0.009
    elif zoom == 12:
        distance = 0.01
    elif zoom == 11:
        distance = 0.02
    elif zoom == 10:
        distance = 0.07
    elif zoom == 9:
        distance = 0.09
    elif zoom == 8:
        distance = 0.5
    elif zoom == 7:
        distance = 0.5
    elif zoom == 6:
        distance = 1
    elif zoom == 5:
        distance = 2
    elif zoom == 4:
        distance = 3
    elif zoom == 3:
        distance = 4
    elif zoom == 2:
        distance = 10
    elif zoom == 1:
        distance = 50
    

    # hashes = compute_geohash_tiles((bbox_x1, bbox_y1, bbox_x2, bbox_y2), precision)
    # print(hashes)
    # print(len(hashes))

    coordinates_patients = {
        "type": "FeatureCollection",
        "features": []
    }

    # Connect to our PostgreSQL

    # ppp = time.time()
    # for h in range(len(hashes)):
        # c = Patient.query.join(Address, Patient.home_address_id == Address.id).filter(Address.geohash.ilike(f'{h}%')).count()
        # start_time = time.time()
        # c = Address.query.filter(Address.geohash.ilike(f'{hashes[h]}%')).count()
        # c = Address.query.filter(Address.geohash.like(f'{hashes[h]}%')).count()
    # sql = text("""
    # SELECT
    #   ST_NumGeometries(gc) as num_geometries,
    #   ST_X(ST_Centroid(gc)) AS X, 
    #   ST_Y(ST_Centroid(gc)) AS Y
    # FROM (
    #   SELECT unnest(ST_ClusterWithin(geom, 0.0035)) AS gc FROM (
    #   SELECT DISTINCT ON (geom) geom FROM "Address"
    #     WHERE geom && ST_MakeEnvelope(%s, %s, %s, %s, 4326)) AS points
    # ) f;
    # """ % (bbox_y1, bbox_x1, bbox_y2, bbox_x2))
    sql = text("""
    SELECT row_number() over () AS id,
      ST_NumGeometries(gc),
      ST_X(ST_Centroid(gc)) AS X,
      ST_Y(ST_Centroid(gc)) AS Y
    FROM (
      SELECT unnest(ST_ClusterWithin(geom, %s)) gc
      FROM (
        SELECT * FROM "Address" WHERE geom && ST_MakeEnvelope(%s, %s, %s, %s, 4326)
      ) AS points
    ) f;
    """ % (str(distance), bbox_y1, bbox_x1, bbox_y2, bbox_x2))
    # sql = text("""
    #     SELECT SUM(1) FROM "Address" WHERE geohash LIKE '{0}%'
    # """.format(hashes[h]))
    m = db.engine.execute(sql)
    for a in m:
        print(a[1])
        # 1 numbers
        # 2 lon
        # 3 lat
        # for z in a:
            # print(z)
            # c = z
        # print(c)
        # process_time = time.time() - start_time
        # print("sql query time", process_time)
        # w = time.time()
        # if c:
        #     # print(q.count())
        #     lat, lon = geohash.decode(hashes[h])
        count = int(a[1])
        if count == 1:
            coordinates_patients["features"].append(
                 {
                    "type": 'Feature',
                    "geometry": {
                        "type": 'Point',
                        "coordinates": [a[3], a[2]]
                    },
                    "id": uuid.uuid1(),
                    "options": {
                        "preset": 'islands#blueIcon'
                    }
                },
            )
        else:
            coordinates_patients["features"].append(
                {
                    "type": 'Cluster',
                    "id": uuid.uuid1(),
                    # "bbox": [[bbox_x1, bbox_y1], [bbox_x2, bbox_y2]],
                    "number": int(a[1]),
                    "geometry": {
                        "type": 'Point',
                        "coordinates": [a[3], a[2]]
                    },
                    "properties": {
                        "balloonContent": "идет загрузка...",
                        "clusterCaption": "идет загрузка...",
                        "iconContent": int(a[1]),
                    }
                }
            )
        # process_time = time.time() - w
        # print("append time", process_time)
        
    # process_time = time.time() - ppp
    # print("loop time", process_time)
    # Post.query.filter(Post.title.ilike(f'%{some_phrase}%'))

    # [17, 18] precision 8
#     [15,16] precision 7
# [13,14] precision 6
# [11, 12] precision 5
# [8, 10] precision 4
# [6, 7] precision 3
# [3, 5] precision 2

    # zoom = 9

    # helper = Helper(bbox_x1, bbox_y1, bbox_x2, bbox_y2, zoom)

    """
    получаю sw ne, sw < ne

    нужно сразу конвертнуть в nw sw
    """

    # tiles = request.args["tiles"].split(',')
    # xMin = int(tiles[0])
    # yMin = int(tiles[1])
    # xMax = int(tiles[2])
    # yMax = int(tiles[3])


    # z = 0
    # xMinI = xMin
    # yMinI = yMin


    # for current_y in range(helper.h):
    #     for current_x in range(helper.w):
    #         a = helper.bbox_nw.x_tile + current_x
    #         b = helper.bbox_nw.y_tile + current_y
    #         c = helper.bbox_nw.x_tile + current_x + 1
    #         d = helper.bbox_nw.y_tile + current_y + 1
    #         x1, y1 = num2deg(a, b, zoom)
    #         x2, y2 = num2deg(c, d, zoom)
    #         q = Patient.query.join(Address, Patient.home_address_id == Address.id).filter(Address.lng != None).filter(
    #             Address.lat >= x2).filter(Address.lat <= x1).filter(Address.lng >= y1).filter(Address.lng <= y2)

            # q = Patient.query
            # print(q[0].lat)
            # lat, lng = 0
            # if q is not None:
            #     for i in q:
            #         lat = i.home_address.lat
            #         lng = i.home_address.lng
            #         break
            #     print("count", lat, lng)

# deg2num(51.16681,71.41296,4)
# const lng = (lnglat[0] - bounds['_ne']['lng']) * (lnglat[0] - bounds['_sw']['lng']) < 0;
#     const lat = (lnglat[1] - bounds['_ne']['lat']) * (lnglat[1] - bounds['_sw']['lat']) < 0;
#     return lng && lat;

# (lng - yMaxLng) * (lng - yMinLng) < 0
# (lat - xMaxLat) * (lng - xMatLng) < 0
            # print("first", q.first())


            # c = q.count()
            # if c > 0:
            #     latlon = center_geolocation(((x2, y1), (x1, y2)))
            #     print(c)
            #     p = q.first()
            #     coordinates_patients["features"].append(
            #         {
            #             "type": 'Cluster',
            #             "id": uuid.uuid1(),
            #             # "bbox": [[bbox_x1, bbox_y1], [bbox_x2, bbox_y2]],
            #             "number": c,
            #             "geometry": {
            #                 "type": 'Point',
            #                 "coordinates": [latlon[1], latlon[0]]
            #             },
            #             "properties": {
            #                 "balloonContent": "идет загрузка...",
            #                 "clusterCaption": "идет загрузка...",
            #                 "iconContent": c,
            #             }
            #         }
            #     )
            #     z += 1

    """
    для каждого tile расчитать его lat lng относительно зума
    для каждого получить количество
    установить точку на середину этого тайла
    """
    # q = Patient.query.join(Address, Patient.home_address_id == Address.id).filter(Address.lng != None).filter(Address.lat >= bbox_x1).filter(
    #     Address.lat <= bbox_x2).filter(Address.lng >= bbox_y1).filter(Address.lng <= bbox_y2)

    # for p in q:
    #     xPatient, yPatinent = deg2num(p.home_address.lat, p.home_address.lng, zoom)
    #     t = (xPatient - xMin) * x + (yPatinent - yMin)
    #     if t < 0 or t >= len(coordinates_patients["features"]):
    #         continue
    #     coordinates_patients["features"][t]["geometry"]["coordinates"][0] = p.home_address.lat
    #     coordinates_patients["features"][t]["geometry"]["coordinates"][1] = p.home_address.lng
    #     coordinates_patients["features"][t]["number"] += 1
    #     coordinates_patients["features"][t]["properties"]["iconContent"] += 1

    return jsonify(coordinates_patients)

 # worldwide tiles
    # tiles = request.args["tiles"].split(',')
    # xMin = int(tiles[0])
    # yMin = int(tiles[1])
    # xMax = int(tiles[2])
    # yMax = int(tiles[3])

    # zoom = int(request.args["zoom"])

    # coordinates_patients = {
    #     "type": "FeatureCollection",
    #     "features": []
    # }

    # tiles x1, y1, x2, y2
    # x = xMax - xMin + 1
    # y = yMax - yMin + 1

    # z = 0
    # for i in range(x):
    #     for v in range(y):
    #         coordinates_patients["features"].append(
    #             {
    #                 "type": 'Cluster',
    #                 "id": z,
    #                 # "bbox": [[2, yMin], [bbox_x2, bbox_y2]],
    #                 "number": 0,
    #                 "geometry": {
    #                     "type": 'Point',
    #                     "coordinates": [0, 0]
    #                 },
    #                 "properties": {
    #                     "iconContent": 0
    #                 }
    #             }
    #         )
    #         z += 1

    """
    for each patient get tiles => get x y tiles
        tile = (x - xMin + 1) * (yMin - 1)
        tiles[tile]["geometry"] = cords
        tiles[tile]["number"] += 1
        id = i
    """
    # start_time = time.time()

    # process_time = time.time() - start_time
    # print("sql query time", process_time)

    # q = Patient.query.join(Address, Patient.home_address_id == Address.id).filter(Address.lng != None).filter(Address.lat >= bbox_x1).filter(
    #     Address.lat <= bbox_x2).filter(Address.lng >= bbox_y1).filter(Address.lng <= bbox_y2)
    # start_time = time.time()
    # for p in q:
    #     color = "green"
    #     if p.is_infected == True:
    #         color = "red"

    #     coordinates_patients["features"].append(
    #         {
    #             "type": "Feature",
    #             "id": p.id,
    #             "geometry": {"type": "Point", "coordinates": [p.home_address.lat, p.home_address.lng]},
    #             "properties": {
    #                 "balloonContent": "идет загрузка...",
    #                 "clusterCaption": "идет загрузка...",
    #                 # "hintContent": "Текст подсказки"
    #             },
    #             "options": {
    #                 "preset": "islands#icon",
    #                 "iconColor": color
    #             }
    #         }
    #     )
    # xPatient, yPatinent = deg2num(p.home_address.lat, p.home_address.lng, zoom)
    # if xPatient >= xMin and yPatinent >= yMin and xPatient <= xMax and yPatinent <= yMax:
    #     t = (xPatient - xMin) * x + (yPatinent - yMin)
    #     print(t, xPatient, yPatinent, xMin, xMax, yMin, yMax)
    #     if t < 0 or t >= len(coordinates_patients["features"]):
    #         continue
    #     coordinates_patients["features"][t]["geometry"]["coordinates"][0] = p.home_address.lat
    #     coordinates_patients["features"][t]["geometry"]["coordinates"][1] = p.home_address.lng
    #     coordinates_patients["features"][t]["number"] += 1
    #     coordinates_patients["features"][t]["properties"]["iconContent"] += 1
    # process_time = time.time() - start_time
    # print("loop", process_time, len(coordinates_patients["features"]))
