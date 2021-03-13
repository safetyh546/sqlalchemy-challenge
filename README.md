# sqlalchemy-challenge

# Key files included in this repository
Resources\hawaii.sqlite --> sqllite database used in analysis<br />
climate_analysis.ipynb --> juypter notebook with climate analysis<br />
app.py --> python file with flask app<br />


# Step 1 - Climate Analysis and Exploration
use Python and SQLAlchemy to do basic climate analysis and data exploration of the hawaiisqllite database<br />
All the analysis completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.<br />

## Precipiation Analysis
Using sqlalchemy retrive the last 12 months of the dataset, load into a pandas dataframe, and plot in a barchart<br />
Show summary statistics for precipitation data<br />

## Station Analysis
Find station with most observations<br />
For this most active station, get the min/max/avg temperature<br />
Pull the last 12 months of the dataset for the most active station and then plot in a histogram<br />

# Step 2 - Flask climate app
create a flask app that retrieves data from hawaiisqllite database<br />

## Flask app has 4 routes
/api/v1.0/precipitation<br/>
Return the maximum precipitation by date for the last 12 months of the dataset<br/><br/>

/api/v1.0/stations<br/>
Return a JSON list of stations from the dataset<br/><br/>

/api/v1.0/tobs<br/>
Return a JSON list of temperature observations (TOBS) for the previous year<br/><br/>

/api/v1.0/StartDate/2017-08-23<br/>
Return a JSON list of minimum, average, and maximum temperature for all dates greater than and equal to passed in StartDate<br/><br/>

/api/v1.0/StartDate/EndDate/2017-08-21/2017-08-22<br/>
Return a JSON list of the minimum temperature, the average temperature, and the max temperature for all dates between passed in StartDate and EndDate<br/><br/>

