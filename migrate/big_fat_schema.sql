CREATE EXTENSION IF NOT EXISTS vector;


-- agency.csv
-- columns: agency_id,agency_name,agency_url,agency_timezone,agency_lang,agency_phone,agency_fare_url
-- example: 100,"V-S ELY-keskus, palveluntuottaja FinFerries",https://www.finferries.fi/,Europe/Helsinki,fi,0207 118 750,

CREATE TABLE IF NOT EXISTS agency(
    agency_id TEXT NOT NULL,
    agency_name TEXT,
    agency_url TEXT,
    agency_timezone TEXT,
    agency_lang VARCHAR(5),
    agency_phone VARCHAR(24),
    agency_fare_url TEXT,

    PRIMARY KEY (agency_id)

);

-- routes.csv
-- columns: route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,route_url,route_color,route_text_color
CREATE TABLE IF NOT EXISTS routes (
    route_id TEXT NOT NULL,
    agency_id TEXT NOT NULL,
    route_short_name VARCHAR(20),
    route_long_name TEXT,
    route_desc TEXT,
    route_type INTEGER,
    route_url TEXT,
    route_color VARCHAR(6),
    route_text_color VARCHAR(6),

    PRIMARY KEY (route_id),
    FOREIGN KEY (agency_id) REFERENCES agency(agency_id)

);

-- trips.csv
-- columns: route_id,service_id,trip_id,trip_headsign,direction_id,block_id,shape_id,wheelchair_accessible,bikes_allowed

CREATE TABLE IF NOT EXISTS trips (
    trip_id text NOT NULL,
    route_id TEXT,
    service_id TEXT,
    trip_headsign text,
    direction_id SMALLINT,
    block_id INTEGER,
    shape_id TEXT,
    wheelchair_accessible SMALLINT,
    bikes_allowed SMALLINT,
    
    PRIMARY KEY (trip_id),
    FOREIGN KEY (route_id) REFERENCES routes(route_id));




-- trip_notes.csv
-- columns: trip_id,abbreviation,description,lang
CREATE TABLE IF NOT EXISTS trip_notes (
    trip_id text NOT NULL, 
    abbreviation text, 
    description text, 
    language text NOT NULL,

    PRIMARY KEY (trip_id, language),
    FOREIGN KEY (trip_id) REFERENCES trips(trip_id)
);


-- stops.csv
-- columns:stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,zone_id,stop_url,location_type,parent_station,stop_timezone,wheelchair_boarding,platform_code

CREATE TABLE IF NOT EXISTS stops(
    stop_id TEXT NOT NULL, 
    stop_code TEXT,
    stop_name VARCHAR(100),
    stop_desc text,
    stop_lat DOUBLE PRECISION,
    stop_lon DOUBLE PRECISION,
    zone_id VARCHAR(10),
    stop_url text,
    location_type SMALLINT,
    parent_station text,
    stop_timezone text,
    wheelchair_boarding SMALLINT,
    platform_code VARCHAR(50),

    PRIMARY KEY (stop_id)
);

--stop_times.csv
-- columns: trip_id,arrival_time,departure_time,stop_id,stop_sequence,stop_headsign,pickup_type,drop_off_type,shape_dist_traveled,timepoint
--ex: "00014922__1006060106",06:21:00,06:25:00,1901,32,,0,0,15072,1
-- 1901 is from stops.csv 1901,1901,Kauppatori A1,,60.45168218,22.26545694,FÖLI,,0,,Europe/Helsinki,0,A1


CREATE TABLE IF NOT EXISTS stop_times(
    trip_id text NOT NULL,
    arrival_time VARCHAR(8), -- this and departure_time goes past midnight, will need to parsed post pull from db
    departure_time VARCHAR(8),
    stop_id text,
    stop_sequence INTEGER NOT NULL,
    stop_headsign VARCHAR(150),
    pickup_type INTEGER,
    drop_off_type INTEGER,
    shape_dist_traveled INTEGER,
    timepoint INTEGER,

    PRIMARY KEY (trip_id, stop_sequence),
    FOREIGN KEY (trip_id) REFERENCES trips(trip_id),
    FOREIGN KEY (stop_id) REFERENCES stops(stop_id)

);


-- stops_translations and trip_headsign_translations was one csv, called translations.csv
-- translations.csv not that easy, contains two types of rows
-- columns: table_name,field_name,language,translation,record_id,field_value
-- rowtype1: stops,stop_name,sv,Satava,386,
-- rowtype2: trips,trip_headsign,sv,Lundo-Tarvasjoki-Koskis,,Lieto-Tarvasjoki-Koski Tl

CREATE TABLE IF NOT EXISTS stops_translations(
    stop_id TEXT, --corresponds directly to the original finnish name in stops.csv so foreign key to stop_id 
    language text,
    translation text, -- the translation of stop_id in stops.csv

    PRIMARY KEY (stop_id, language),
    FOREIGN KEY (stop_id) REFERENCES stops(stop_id)
    
);

CREATE TABLE IF NOT EXISTS trip_headsign_translations(
    original TEXT, -- maps to field_value, uncertain atm how to get to this, iguess just a costly search
    language VARCHAR(10),
    translation TEXT,
    
    PRIMARY KEY (original, language)
    
);


-- calendar_dates.csv
-- service_id,date,exception_type
-- 1001010100,20260810,1
-- 1001010100,20260811,1

CREATE TABLE IF NOT EXISTS calendar_dates(
    service_id TEXT NOT NULL,
    date VARCHAR(8), --transform into date in service layer ig
    exception_type INTEGER, 

    PRIMARY KEY (service_id));


--skipped - calendar.csv
--service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date
--1001010100,0,0,0,0,0,0,0,20260810,20270606

CREATE TABLE IF NOT EXISTS calendar(
    service_id TEXT NOT NULL,
    monday SMALLINT,
    tuesday SMALLINT,
    wednesday SMALLINT,
    thursday SMALLINT,
    friday SMALLINT,
    saturday SMALLINT,
    sunday SMALLINT,
    start_date VARCHAR(8),
    end_date VARCHAR(8),

    PRIMARY KEY (service_id, start_date)
    );

CREATE INDEX IF NOT EXISTS idx_stop_times_stop_dep ON stop_times (stop_id, departure_time);
CREATE INDEX IF NOT EXISTS idx_trips_service ON trips (service_id);