#################################################
# import dependencies
#################################################

from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
from pandas import DataFrame
import pandas as pd
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/Hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Welcome to Hawaii Weather Stations API!<br/>"
        f"Available Routes:<br/><br/>"
        f"/api/v1.0/precipitation<br/>Return the maximum precipitation by date for the last 12 months of the dataset<br/><br/>"
        f"/api/v1.0/stations<br/>Return a JSON list of stations from the dataset<br/><br/>"
        f"/api/v1.0/tobs<br/>Return a JSON list of temperature observations (TOBS) for the previous year<br/><br/>"
        f"/api/v1.0/StartDate/2017-08-23<br/>Return a JSON list of minimum, average, and maximum temperature for all dates greater than and equal to passed in StartDate<br/><br/>"
        f"/api/v1.0/StartDate/EndDate/2017-08-21/2017-08-22<br/>Return a JSON list of the minimum temperature, the average temperature, and the max temperature for all dates between passed in StartDate and EndDate<br/><br/>"

    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Return max precipitation by day for the last 12 months of the dataset
    LastDate = session.query(measurement.date).order_by(measurement.date.desc()).first().date
    OneYearBeforeLastDate = dt.datetime.strptime(LastDate, '%Y-%m-%d') - dt.timedelta(days=365)
    DateList = session.query(measurement.date,func.max(measurement.prcp)).filter(measurement.date >= OneYearBeforeLastDate).group_by(measurement.date).all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of all_dates
    all_dates = []
    for date, prcp in DateList:
        date_dict = {}
        date_dict["date"] = date
        date_dict["prcp"] = prcp
        all_dates.append(date_dict)

    return jsonify(all_dates)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Return list of all stations 
    StationList = session.query(station.station,station.name).all()

    session.close()
    return jsonify(StationList)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    # Return a JSON list of temperature observations (TOBS) latest 12 months for most active station 
    StationCount = session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).order_by((func.count(measurement.station)).desc()).all()
    MostActiveStation = StationCount[0][0]
    LastDate = session.query(measurement.date).order_by(measurement.date.desc()).first().date
    OneYearBeforeLastDate = dt.datetime.strptime(LastDate, '%Y-%m-%d') - dt.timedelta(days=365)
    tobs = session.query(measurement.station,measurement.date,measurement.tobs).filter(measurement.station == MostActiveStation).filter((measurement.date >= OneYearBeforeLastDate)).all()
    
    session.close()  

    return jsonify(tobs)



@app.route("/api/v1.0/StartDate/<StartDate>")
def Temp(StartDate):
    session = Session(engine)

    Temp = session.query(func.min(measurement.tobs),func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= StartDate).all()

    session.close()  


    Agg = []
    for TMIN, TAVG,TMAX in Temp:
        Agg_dict = {}
        Agg_dict["TMIN"] = TMIN
        Agg_dict["TAVG"] = TAVG
        Agg_dict["TMAX"] = TMAX
        Agg.append(Agg_dict)

    return jsonify(Agg)

@app.route("/api/v1.0/StartDate/EndDate/<StartDate>/<EndDate>")
def TempSE(StartDate,EndDate):
    session = Session(engine)

    TempSE = session.query(func.min(measurement.tobs),func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= StartDate).filter(measurement.date <= EndDate).all()

    session.close()  


    Agg = []
    for TMIN, TAVG,TMAX in TempSE:
        Agg_dict = {}
        Agg_dict["TMIN"] = TMIN
        Agg_dict["TAVG"] = TAVG
        Agg_dict["TMAX"] = TMAX
        Agg.append(Agg_dict)

    return jsonify(Agg)


if __name__ == "__main__":
    app.run(debug=True)    