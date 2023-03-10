import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite", echo=False)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# # Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

# #################################################
# Flask Setup
# #################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>startdate/<end>enddate"

    f"<br/> <br/> Note: All dates should be entered in the following format YYYY-MM-DD"
    )

#############################################################################
# Query to return precipitation observations from 2016-08-23 to 2017-08-23
#############################################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    #Create session link from Python to the database
    session = Session(engine)

    """Return precipitation observations from 2016-08-23 to 2017-08-23"""
    #Query of precipitation measurements
    results = session.query(Measurement.prcp, Measurement.date).\
    filter(Measurement.date >= '2016-08-23')

    session.close()

    precipitation_rows = [{"date": result[1], "prcp": result[0]} for result in results]

    return jsonify(precipitation_rows)

#######################################################
# Query to return JSON list of stations from DataSet
######################################################

@app.route("/api/v1.0/stations")
def stations():
    #Create session link from Python to the database
    session = Session(engine)

    """Return list of observation stations in dataset"""
    #Query of list of stations with all properties
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation)

    session.close()

    station_dict = [{"Station ID": result[0], "Name": result[1], "Latitude": result[2], "Longitude": result[3], "Elevation": result[4]} for result in results]

    return jsonify(station_dict)

##################################################################
# Query temp observation for last 12 mos of most active station
#################################################################

@app.route("/api/v1.0/tobs")
def tobs():
    #Create session link from Python to the database
    session = Session(engine)

    """Return temperature observations in F for most active observation station"""
    #Query of temperature observations for the last 12 months for most active station
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= '2016-08-23')

    session.close()

    tobs_dict = [{"Date": result[0], "Temp (F)": result[1]} for result in results]

    return jsonify(tobs_dict)

#########################################################
# Query min, max and avg temp for a specfied start date
#########################################################

@app.route("/api/v1.0/<start>")
def tobs_calc(start):
    #Create session link from Python to the database
    session = Session(engine)

    """Return min, max and avg temp for a specfied start date"""
    #Query of min, max and avg temp for the specified start date
    sel = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    
    results = session.query(*sel).filter(Measurement.date >= start)

    session.close()

    start_dict = [{"TMIN": result[0], "TMAX": result[1], "TAVG": result[2]} for result in results]

    return jsonify(start_dict)

##################################################################
# Query min, max and avg temp for a specfied start and end date
##################################################################

@app.route("/api/v1.0/<start>/<end>")
def tobs_end_calc(start, end):
    #Create session link from Python to the database
    session = Session(engine)

    """Return min, max and avg temp for a specfied start and end date"""
    #Query of min, max and avg temp for the specified start and end date
    sel2 = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    
    results = session.query(*sel2).filter(Measurement.date >= start).filter(Measurement.date <= end)

    session.close()

    start_end_dict = [{"TMIN": result[0], "TMAX": result[1], "TAVG": result[2]} for result in results]

    return jsonify(start_end_dict)

if __name__ == '__main__':
    app.run(debug=True)