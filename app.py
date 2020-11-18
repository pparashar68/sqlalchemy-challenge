
#Boiler Plate code 
from sqlalchemy import create_engine, inspect, func ,distinct,inspect
import numpy as np
import pandas as pd
import datetime as dt
import datetime
from flask import Flask, jsonify
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


#Reflect Tables into SQLAlchemy ORM
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

# Flask application setup
from flask import Flask
app = Flask(__name__)

# Initialize trip start and end dates(random)
start_date = '2016-02-01'
end_date = '2016-02-10'
#Flask Routes for application
@app.route("/")
def homepage():
    return (
        f"Welcome to trip information page!!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    from datetime import datetime
    max_date_in_db = session.query(func.max(measurement.date)).one()
    max_date_in_db = datetime.strptime(max_date_in_db[0], '%Y-%m-%d')
    one_year_before_maxdate = datetime(max_date_in_db.year -1, max_date_in_db.month, max_date_in_db.day)
    prcp_query_result = session.query(measurement.date,
                        measurement.prcp).filter(measurement.date 
                        >one_year_before_maxdate).filter(measurement.date 
                        <= max_date_in_db).all()
    prcp_query_result_dict = {prcp_query_result[i][0]: prcp_query_result[i][1] for i in range(0, len(prcp_query_result))}
    
    return jsonify(prcp_query_result_dict)  ## It's returning 12 month precipitation data as per readme

@app.route("/api/v1.0/stations")
def stations():
    #Return a JSON list of Active stations from the dataset
    sel = [measurement.station,func.count(measurement.station)]
    active_stations = session.query(*sel).group_by(measurement.station).\
                      order_by(func.count(measurement.station).desc()).all()
    active_stations_dict = {active_stations[i][0]: active_stations[i][1] for i in range(0, len(active_stations))}

    return jsonify(active_stations_dict)

@app.route("/api/v1.0/tobs")
def tobs():
    #Query the dates and temperature observations of the most active station for the last year of data
    sel1 = [measurement.station,func.count(measurement.station)]
    active_stations = session.query(*sel1).group_by(measurement.station).\
                  order_by(func.count(measurement.station).desc()).first()
    most_active_station_id = active_stations.station
    sel = [measurement.station,func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)]
    most_active_station_temp = session.query(*sel).filter(measurement.station==most_active_station_id)
    for row in most_active_station_temp:
        most_active_station_temp_dict ={"Active Station":row[0] ,"MinTemp": row[1], "MaxTemp": row[2], "AvgTemp" : row[3]}
    return jsonify(most_active_station_temp_dict)

@app.route("/api/v1.0/start_date")
def temps_start():
    
    tobs_results=session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).all()

    # Convert the query results to a Dictionary using date as the key and tobs as the value.
    tobs=[]
    for row in tobs_results:
        tobs_dict = {}
        tobs_dict["tmin"] = row[0]
        tobs_dict["tavg"] = row[1]
        tobs_dict["tmax"] = row[2]
        tobs.append(tobs_dict)

    return jsonify(tobs)


@app.route("/api/v1.0/start_date/end_date")
def temps_start_end():
    
    tobs_results=session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()

    # Convert the query results to a Dictionary using date as the key and tobs as the value.
    tobs=[]
    for row in tobs_results:
        tobs_dict = {}
        tobs_dict["tmin"] = row[0]
        tobs_dict["tavg"] = row[1]
        tobs_dict["tmax"] = row[2]
        tobs.append(tobs_dict)

    return jsonify(tobs)

#Define runtime environment in debug mode

if __name__ == "__main__":
    app.run(debug=True)