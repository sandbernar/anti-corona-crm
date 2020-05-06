import os
import re

import psycopg2
import pandas as pd

from app import create_app, db
from app import constants as C
from app.main.models import (Region, Country, Infected_Country_Category, JobCategory, 
                            TravelType, BorderControl, VariousTravel, Address, VisitedCountry)
from app.main.patients.models import ContactedPersons, Patient, State, PatientState
from app.main.hospitals.models import Hospital, Hospital_Type
from app.main.flights_trains.models import FlightTravel, FlightCode
from config import config_dict

# Database logging
psqlConn = psycopg2.connect(dbname=os.getenv("DATABASE_NAME"),
                            user=os.getenv("DATABASE_USER"),
                            password=os.getenv("DATABASE_PASSWORD"),
                            host=os.getenv("DATABASE_HOST"))

psqlConn.autocommit = True
psqlCursor = psqlConn.cursor()

def psqlQuery(query_message):
    """
    Function that queries PostgreSQL
    If SELECT returns key-value paired objects
    """
    psqlCursor.execute(query_message)
    # print(query_message)
    try:
        columns = [col.name for col in psqlCursor.description]
        returnValue = []
        for row in psqlCursor:
            pairs = list(zip(columns, row))
            obj = {}
            for pair in pairs:
                obj[pair[0]] = pair[1]
            returnValue.append(obj)
    except Exception:
        returnValue = None
    return returnValue

createSchemeQuery = "CREATE SCHEMA logging;"
createTableQuery = """
CREATE TABLE IF NOT EXISTS logging.t_history (
    id serial,
    tstamp timestamp DEFAULT now(),
    schemaname text,
    tabname text,
    operation text,
    new_val json,
    old_val json
);
"""
createTriggerQuery = """
CREATE OR REPLACE FUNCTION change_trigger() RETURNS trigger AS $$
    BEGIN
        IF TG_OP = 'INSERT'
        THEN
            INSERT INTO logging.t_history (tabname, schemaname, operation, new_val)
                    VALUES (TG_RELNAME, TG_TABLE_SCHEMA, TG_OP, row_to_json(NEW));
            RETURN NEW;
        ELSIF TG_OP = 'UPDATE'
        THEN
            INSERT INTO logging.t_history (tabname, schemaname, operation, new_val, old_val)
                    VALUES (TG_RELNAME, TG_TABLE_SCHEMA, TG_OP,
                            row_to_json(NEW), row_to_json(OLD));
            RETURN NEW;
        ELSIF TG_OP = 'DELETE'
        THEN
            INSERT INTO logging.t_history (tabname, schemaname, operation, old_val)
                    VALUES (TG_RELNAME, TG_TABLE_SCHEMA, TG_OP, row_to_json(OLD));
            RETURN OLD;
        END IF;
    END;
$$ LANGUAGE 'plpgsql' SECURITY DEFINER;
"""

createExtensionQuery = "CREATE EXTENSION postgis;"
addGeomColumnQuery = "SELECT AddGeometryColumn('Address', 'geom', 4326, 'Point',2);"
createGeomTriggerQuery = """
CREATE OR REPLACE FUNCTION add_geom() RETURNS trigger AS
    $$
    BEGIN
    IF TG_OP = 'UPDATE' THEN
        IF NEW.lng IS DISTINCT FROM OLD.lng OR NEW.lat IS DISTINCT FROM OLD.lat THEN
            UPDATE "Address" SET geom = ST_SetSRID(ST_MakePoint(NEW.lng, NEW.lat), 4326) WHERE id=NEW.id;
        END IF;
    ELSE 
        UPDATE "Address" SET geom = ST_SetSRID(ST_MakePoint(NEW.lng, NEW.lat), 4326) WHERE id=NEW.id;
    END IF;
    RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
"""
addGeomTriggerQuery = 'CREATE TRIGGER add_geom_trigger AFTER INSERT OR UPDATE ON "Address" FOR EACH ROW EXECUTE PROCEDURE add_geom();'

# logging.history trigger
try:
    psqlCursor.execute(createSchemeQuery)
    psqlCursor.execute(createTableQuery)
    psqlCursor.execute(createTriggerQuery)
except Exception as e:
    print(e)


# POSTGIS EXTENSION
try:
    psqlCursor.execute(createExtensionQuery)
    try: # ADD GEOM COLUMN
        psqlCursor.execute(addGeomColumnQuery)
        try: # CREATE TRIGGER FUNCTION add_geom
            psqlCursor.execute(createGeomTriggerQuery)
            try: # ADD TRIGGER TO ADDRESS
                psqlCursor.execute(addGeomTriggerQuery)
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)

        psqlQuery('UPDATE "Address" SET geom = ST_SetSRID(ST_MakePoint(lng, lat), 4326);')
    except Exception as e:
        print(e)
except Exception as e:
    print(e)

createSetPatientStateTriggerQuery = """
CREATE OR REPLACE FUNCTION set_patient_state() RETURNS trigger AS
    $$
    DECLARE dead_state_count INTEGER;
    DECLARE found_state_count INTEGER;
    DECLARE infected_state_count INTEGER;
    DECLARE last_infected_state_id INTEGER;
    DECLARE last_infected_state_dd TIMESTAMP;
    DECLARE healty_state_count INTEGER;
    DECLARE last_healty_state_id INTEGER;
    DECLARE last_healty_state_dd TIMESTAMP;
    DECLARE hosp_state_count INTEGER;
    DECLARE last_hosp_state_id INTEGER;
    DECLARE last_hosp_state_dd TIMESTAMP;
    DECLARE home_state_count INTEGER;
    DECLARE last_home_state_id INTEGER;
    DECLARE last_home_state_dd TIMESTAMP;
    DECLARE patient_in_hospital BOOLEAN;
    DECLARE patient_is_home BOOLEAN;
    DECLARE state_val varchar;
    BEGIN
    state_val = (SELECT value FROM "State" WHERE id=NEW.state_id);
    dead_state_count = (SELECT count(*) FROM "PatientState" WHERE patient_id=NEW.patient_id AND state_id=(SELECT id FROM "State" WHERE value='dead'));
    found_state_count = (SELECT count(*) FROM "PatientState" WHERE patient_id=NEW.patient_id AND state_id=(SELECT id FROM "State" WHERE value='found'));
    
    infected_state_count = (SELECT count(*) FROM "PatientState" WHERE patient_id=NEW.patient_id AND state_id=(SELECT id FROM "State" WHERE value='infected'));
    last_infected_state_id = (SELECT id FROM "PatientState" WHERE patient_id=NEW.patient_id AND state_id=(SELECT id FROM "State" WHERE value='infected') ORDER BY detection_date DESC);
    last_infected_state_dd = (SELECT detection_date FROM "PatientState" WHERE patient_id=NEW.patient_id AND state_id=(SELECT id FROM "State" WHERE value='infected') ORDER BY detection_date DESC);
    
    healty_state_count = (SELECT count(*) FROM "PatientState" WHERE patient_id=NEW.patient_id AND state_id=(SELECT id FROM "State" WHERE value='recovery'));
    last_healty_state_id = (SELECT id FROM "PatientState" WHERE patient_id=NEW.patient_id AND state_id=(SELECT id FROM "State" WHERE value='recovery') ORDER BY detection_date DESC);
    last_healty_state_dd = (SELECT detection_date FROM "PatientState" WHERE patient_id=NEW.patient_id AND state_id=(SELECT id FROM "State" WHERE value='recovery') ORDER BY detection_date DESC);
    
    hosp_state_count = (SELECT count(*) FROM "PatientState" WHERE patient_id=NEW.patient_id AND state_id=(SELECT id FROM "State" WHERE value='hospitalized'));
    last_hosp_state_id = (SELECT id FROM "PatientState" WHERE patient_id=NEW.patient_id AND state_id=(SELECT id FROM "State" WHERE value='hospitalized') ORDER BY detection_date DESC);
    last_hosp_state_dd = (SELECT detection_date FROM "PatientState" WHERE patient_id=NEW.patient_id AND state_id=(SELECT id FROM "State" WHERE value='hospitalized') ORDER BY detection_date DESC);
    
    home_state_count = (SELECT count(*) FROM "PatientState" WHERE patient_id=NEW.patient_id AND state_id=(SELECT id FROM "State" WHERE value='is_home'));
    last_home_state_id = (SELECT id FROM "PatientState" WHERE patient_id=NEW.patient_id AND state_id=(SELECT id FROM "State" WHERE value='is_home') ORDER BY detection_date DESC);
    last_home_state_dd = (SELECT detection_date FROM "PatientState" WHERE patient_id=NEW.patient_id AND state_id=(SELECT id FROM "State" WHERE value='is_home') ORDER BY detection_date DESC);

    -- dead
    IF state_val='dead' AND dead_state_count > 0 THEN
        UPDATE "Patient" SET is_dead=true WHERE id=NEW.patient_id;
        UPDATE "Patient" SET in_hospital=false WHERE id=NEW.patient_id;
        UPDATE "Patient" SET is_home=false WHERE id=NEW.patient_id;
        UPDATE "Patient" SET is_infected=false WHERE id=NEW.patient_id;
        UPDATE "Patient" SET is_healthy=false WHERE id=NEW.patient_id;
    END IF;

    -- found
    IF state_val='found' AND found_state_count > 0 THEN
        UPDATE "Patient" SET is_found=true WHERE id=NEW.patient_id;
    END IF;

    -- infected
    IF state_val='infected' AND infected_state_count > 0 THEN
        IF dead_state_count > 0 THEN
            -- pass infected
        ELSIF healty_state_count > 0 AND last_healty_state_dd > last_infected_state_dd THEN
            -- pass infected
        ELSIF healty_state_count > 0 AND last_healty_state_dd == last_infected_state_dd AND last_healty_state_id > last_infected_state_id THEN
            -- pass infected
        ELSE
            UPDATE "Patient" SET is_infected=true WHERE id=NEW.patient_id;
            UPDATE "Patient" SET is_healthy=false WHERE id=NEW.patient_id;
        END IF;
    END IF;

    -- is_home
    IF state_val='is_home' AND home_state_count > 0 THEN
        IF dead_state_count > 0 THEN
            -- pass is_home
        ELSIF hosp_state_count > 0 AND last_hosp_state_dd > last_home_state_dd THEN
            -- pass is_home
        ELSIF hosp_state_count > 0 AND last_hosp_state_dd == last_home_state_dd AND last_hosp_state_id > last_home_state_id THEN
            -- pass is_home
        ELSIF healty_state_count > 0 AND last_healty_state_dd > last_home_state_dd THEN
            -- pass is_home
        ELSIF healty_state_count > 0 AND last_healty_state_dd == last_home_state_dd AND last_healty_state_id > last_home_state_id THEN
            -- pass is_home
        ELSE
            UPDATE "Patient" SET is_home=true WHERE id=NEW.patient_id;
            UPDATE "Patient" SET in_hospital=false WHERE id=NEW.patient_id;
            UPDATE "Patient" SET is_healthy=false WHERE id=NEW.patient_id;
        END IF;
    END IF;

    -- in_hospital
    IF state_val='hospitalized' AND home_state_count > 0 THEN
        IF dead_state_count > 0 THEN
            -- pass in_hospital
        ELSIF home_state_count > 0 AND last_home_state_dd > last_hosp_state_dd THEN
            -- pass in_hospital
        ELSIF home_state_count > 0 AND last_home_state_dd == last_hosp_state_dd AND last_home_state_id > last_hosp_state_id THEN
            -- pass in_hospital
        ELSIF healty_state_count > 0 AND last_healty_state_dd > last_hosp_state_dd THEN
            -- pass in_hospital
        ELSIF healty_state_count > 0 AND last_healty_state_dd == last_hosp_state_dd AND last_healty_state_id > last_hosp_state_id THEN
            -- pass in_hospital
        ELSE
            UPDATE "Patient" SET in_hospital=true WHERE id=NEW.patient_id;
            UPDATE "Patient" SET in_hospital=false WHERE id=NEW.patient_id;
            UPDATE "Patient" SET is_healthy=false WHERE id=NEW.patient_id;
        END IF;
    END IF;

    -- is_healthy
    IF state_val='recovery' AND healty_state_count > 0 THEN
        patient_in_hospital = (SELECT in_hospital FROM "Patient" WHERE id=NEW.patient_id);
        patient_is_home = (SELECT is_home FROM "Patient" WHERE id=NEW.patient_id);
        IF patient_in_hospital = true OR patient_is_home = true THEN
            -- pass is_healthy
        ELSE
            UPDATE "Patient" SET is_healthy=true WHERE id=NEW.patient_id;
            UPDATE "Patient" SET in_hospital=false WHERE id=NEW.patient_id;
            UPDATE "Patient" SET is_home=false WHERE id=NEW.patient_id;
        END IF;
    END IF;

    RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
"""
addSetPatientStateTriggerQuery = 'CREATE TRIGGER set_patient_state_trigger AFTER INSERT OR UPDATE ON "PatientState" FOR EACH ROW EXECUTE PROCEDURE set_patient_state();'
# logging.history trigger
try:
    psqlCursor.execute(createSetPatientStateTriggerQuery)
    psqlCursor.execute(addSetPatientStateTriggerQuery)
except Exception as e:
    print(e)
print("init log done.")

#############################
#   Application Database    #
#############################

def initialize_db(db):
    df = pd.read_excel(C.hospitals_list_xlsx)
    df = df.drop_duplicates()

    # Add states: dead, infected, healthy
    for state in C.states:
        dbState = State.query.filter_by(name=state[1]).first()
        if dbState:
            dbState.value = state[0]
            db.session.add(dbState)
        else:
            tmpState = State(value=state[0], name=state[1])
            db.session.add(tmpState)


    # Add travel types
    for typ in C.travel_types:
        if not TravelType.query.filter_by(value=typ[0], name=typ[1]).first():
            travel_type = TravelType(value=typ[0], name=typ[1])
            db.session.add(travel_type)        

    for cat in C.country_category:
        if not Infected_Country_Category.query.filter_by(name=cat).first():
            country_cat = Infected_Country_Category(name=cat)
            db.session.add(country_cat)

    for country in C.code_country_list:
        if not Country.query.filter_by(code=country[0], name=country[1]).first():
            new_country = Country(code=country[0], name=country[1])
            db.session.add(new_country)

    for job_category in C.job_categories:
        if not JobCategory.query.filter_by(value=job_category[0], name=job_category[1]).first():
            j_category = JobCategory(value=job_category[0], name=job_category[1])
            db.session.add(j_category)   

    for n in df.region.unique():
        if not Region.query.filter_by(name=n).first():
            region = Region(name=n)
            db.session.add(region)

    if not Region.query.filter_by(name=C.out_of_rk).first():
        region = Region(name=C.out_of_rk)
        db.session.add(region)

    for n in list(df.TIPMO.unique()) + C.hospital_additional_types:
        if not pd.isna(n):
            if not Hospital_Type.query.filter_by(name=n).first():
                typ = Hospital_Type(name=n)
                db.session.add(typ)

    
    db.session.commit()

    # We need to get ids of TravelType for by auto and by foot types
    q = TravelType.query

    foot_auto_type_ids = [q.filter_by(value = C.by_auto_type[0]).first().id,
                            q.filter_by(value = C.by_foot_type[0]).first().id]
    for type_id in foot_auto_type_ids:
        for border_name in C.by_earth_border:
            if not BorderControl.query.filter_by(travel_type_id=type_id, name=border_name).first():
                border = BorderControl(travel_type_id = type_id, name = border_name)
                db.session.add(border)

    sea_type_id = q.filter_by(value = C.by_sea_type[0]).first().id
    for border_name in C.by_sea_border:
        if not BorderControl.query.filter_by(travel_type_id=sea_type_id, name=border_name).first():
            border = BorderControl(travel_type_id = sea_type_id, name = border_name)
            db.session.add(border)

    # Add hospitals
    for _, row in df.iterrows():
        hospital = Hospital()
        full_name = row["Name"]
        if not pd.isna(full_name):
            short_name = re.findall('"([^"]*)"', full_name.replace("«", "\"").replace("»", "\""))
            if not len(short_name):
                short_name = full_name
            elif not (len(short_name[0])):
                short_name = full_name
            else:
                short_name = short_name[0]
            if Hospital.query.filter_by(full_name=full_name).first() == None:
                hospital.name = short_name
                hospital.full_name = full_name
                
                region = Region.query.filter_by(name=row["region"]).first()
                hospital.region_id = region.id
                hospital.address = ", ".join(row["Adres"].split(":")[3:])

                hospital_type = Hospital_Type.query.filter_by(name=row["TIPMO"]).first()
                hospital.hospital_type_id = hospital_type.id

                hospital.beds_amount = 0
                hospital.meds_amount = 0
                hospital.tests_amount = 0
                hospital.tests_used = 0

                db.session.add(hospital)
    db.session.commit()
    
    # Add triggers
    triggerQueries = [
        'CREATE TRIGGER "triggerPatient" BEFORE INSERT OR UPDATE OR DELETE ON "Patient" FOR EACH ROW EXECUTE PROCEDURE change_trigger();',
        'CREATE TRIGGER "triggerContactedPersons" BEFORE INSERT OR UPDATE OR DELETE ON "ContactedPersons" FOR EACH ROW EXECUTE PROCEDURE change_trigger();',
        'CREATE TRIGGER "triggerRegion" BEFORE INSERT OR UPDATE OR DELETE ON "Region" FOR EACH ROW EXECUTE PROCEDURE change_trigger();',
        'CREATE TRIGGER "triggerTravelType" BEFORE INSERT OR UPDATE OR DELETE ON "TravelType" FOR EACH ROW EXECUTE PROCEDURE change_trigger();',
        'CREATE TRIGGER "triggerInfected_Country_Category" BEFORE INSERT OR UPDATE OR DELETE ON "Infected_Country_Category" FOR EACH ROW EXECUTE PROCEDURE change_trigger();',
        'CREATE TRIGGER "triggerPatientState" BEFORE INSERT OR UPDATE OR DELETE ON "PatientState" FOR EACH ROW EXECUTE PROCEDURE change_trigger();',
        'CREATE TRIGGER "triggerCountry" BEFORE INSERT OR UPDATE OR DELETE ON "Country" FOR EACH ROW EXECUTE PROCEDURE change_trigger();',
        'CREATE TRIGGER "triggerFlightCode" BEFORE INSERT OR UPDATE OR DELETE ON "FlightCode" FOR EACH ROW EXECUTE PROCEDURE change_trigger();',
        'CREATE TRIGGER "triggerBorderControl" BEFORE INSERT OR UPDATE OR DELETE ON "BorderControl" FOR EACH ROW EXECUTE PROCEDURE change_trigger();',
        'CREATE TRIGGER "triggerVisitedCountry" BEFORE INSERT OR UPDATE OR DELETE ON "VisitedCountry" FOR EACH ROW EXECUTE PROCEDURE change_trigger();',
        'CREATE TRIGGER "triggerAddress" BEFORE INSERT OR UPDATE OR DELETE ON "Address" FOR EACH ROW EXECUTE PROCEDURE change_trigger();',
        'CREATE TRIGGER "triggerUser" BEFORE INSERT OR UPDATE OR DELETE ON "User" FOR EACH ROW EXECUTE PROCEDURE change_trigger();',
        'CREATE TRIGGER "triggerHospital_Type" BEFORE INSERT OR UPDATE OR DELETE ON "Hospital_Type" FOR EACH ROW EXECUTE PROCEDURE change_trigger();',
        'CREATE TRIGGER "triggerHospital" BEFORE INSERT OR UPDATE OR DELETE ON "Hospital" FOR EACH ROW EXECUTE PROCEDURE change_trigger();',
        'CREATE TRIGGER "triggerFlightTravel" BEFORE INSERT OR UPDATE OR DELETE ON "FlightTravel" FOR EACH ROW EXECUTE PROCEDURE change_trigger();',
        'CREATE TRIGGER "triggerVariousTravel" BEFORE INSERT OR UPDATE OR DELETE ON "VariousTravel" FOR EACH ROW EXECUTE PROCEDURE change_trigger();'
    ]
    for triggerQuery in triggerQueries:
        try:
            db.engine.execute(triggerQuery)
        except Exception:
            pass

get_config_mode = os.environ.get('CONFIG_MODE', 'Debug')
config_mode = config_dict[get_config_mode.capitalize()]
app = create_app(config_mode)
db.init_app(app)
with app.app_context():
    db.create_all()
    initialize_db(db)
