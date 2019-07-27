#import libraries
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#reflect an existing database, tables into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)
#Save table references
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create session
session = Session(engine)
#flask app
app = Flask(__name__)

#home page route
@app.route("/")
def welcome():
   """List all available api routes."""
   
   return (
       f"<h1>Welcome to my Climate App</h1><br/>"
       f"<h2>Available Routes:</h2>"
       f"/api/v1.0/precipitation<br/>"
       f"/api/v1.0/stations<br/>"
       f"/api/v1.0/tobs<br/>"
       f"/api/v1.0/<'start'>/<'end'>       :enter start and end dates<br/>"
       f"/api/v1.0/<'start'>             :enter start date<br/>"
   )

#precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    """Return a list of all the percp data"""
    prcp_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > '2016-08-23').all()
    prcp_list = list(np.ravel(prcp_data))
    return jsonify(prcp_list)

#stations route
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    """Return a list of all the Stations names"""
    station = session.query(Station.station).all()
    stations_list = list(np.ravel(station))
    return jsonify(stations_list)

#tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    """Return a list of all the Temperature data"""
    tobs_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > '2016-08-23').all()
    tobs_list = list(np.ravel(tobs_data))
    return jsonify(tobs_list)

#tmin, tmax, tavg
@app.route("/api/v1.0/<start>/<end>")
def temp_temp_data(start, end):
    session = Session(engine)
    trip_data = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    trip_list = list(np.ravel(trip_data))
    return jsonify(trip_list)

#tmin, tmax, tavg
@app.route("/api/v1.0/<start>")
def start_temp_data(start):
    session = Session(engine)
    date_data = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    date_list = list(np.ravel(date_data))
    return jsonify(date_list)

if __name__ == '__main__':
    app.run(debug=True)