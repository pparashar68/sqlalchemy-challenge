
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


#Flask Routes for application
@app.route("/")
def homepage():
    return (
        f"Welcome to trip information page!!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
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
    return "Stations Information"
@app.route("/api/v1.0/tobs")
def tobs():
    return "tobs information"
@app.route("/api/v1.0/start")
def startendrange():
    return "start-end-range tmin,tavg,tmax for the dates"
    

#Define runtime environment in debug mode

if __name__ == "__main__":
    app.run(debug=True)