# sqlalchemy-challenge

There are two parts of this challenge: 
1) Querying an SQL database using SQLAlchemy and Pandas
2) Creating an API route to those queries using Flask

The data being analyzed is from weather stations in Hawaii collecting temperature and precipitation data for various dates over multiple years ending in August 2017

The first part of the project analyzes the database based on precipitation and temperature data separately. The precipitation data is filtered down to the last 12 months of the collective data and plotted as a bar graph. The temperature data is plotted as a histogram for the last 12 months of observations collected by the most active weather station (USC00519281). 

This analysis can be found under the SurfsUp folder in the file titled 'climate_starter.ipynb'.

In the second part of the project, the queries run in the first part are copied into a python script along with the set up for a flask server. The API routes to these queries are then defined in flask and the respective end points are listed on the main web page. 

The script for this can be found in the SurfsUp folder in a file titled app.py.