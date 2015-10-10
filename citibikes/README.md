# Testing whether more people ride citibike from Manhattan to Brooklyn, or from Brooklyn to Manhattan

# the citibike september 2015 file can be obtained here
# https://drive.google.com/file/d/0Bx8AmvwAoY0jUzV1dXltOXZHWTQ/view?usp=sharing

# the StationsBorough.csv file is uploaded to the repository.

Dataset: open data for citibike ridership for September 2015

Idea: We want to know if the ridership from Brooklyn to Manhattan during Weekdays is Greater than that from Manhattan to Brooklyn during Weekdays.

Terms: 

"Manhattan" Citibike stations in Manhattan and The Bronx
"Brooklyn" Citibike stations in Brooklyn and Queens

Control Group: People moving from Manhattan to Brooklyn

Test Group: People riding from Brooklyn to Manhattan

Hypotheses:

Null Hypothesis: The total number of rides from Manhattan to Brooklyn on weekdays is greater than the total number of rides from Brooklyn to Manhattan on weekdays.

Alternative Hypothesis: The total number of rides from Manhattan to Brooklyn on weekdays is less than or equal to the total number of rides from Brooklyn to Manhattan on weekdays.

Process:
First, we took the json file of citibike stations from the citibike database and extracted the station id, latitude and longitude. 
Then we used ArcGis to lasso around the stations in Manhattan+Bronx and add the value of 'Manhattan' against those stations in a new column entitled 'Boroughs', and we did the same for the stations in Brooklyn + Queens with the value 'Brooklyn'.
Next, we used Python to left-join our station-borough table to the citibike csv file using the start station id and repeated the join for stop station id, and deleted the columns we did not need.
Then we converted the starttime column into a datetime and calculated which days were weekends and which were weekdays.
We counted the weekdays against the boroughs and performed chi-squared testing of the hypothesis.
We got chi-squared value of 7 and rejected the null-hypothesis with a confidense of 95%. 

Participants:
Denis Khryashchev, Kiran Venkata Palla, Manushi Aashish Majumdar, Alan Polson, Svarmit Singh Pasricha.

1. Denis Khryashchev + Alan Polson came with the idea on what to test and how. Denis Khryashchev extracted the station-list from the citibike json file. Denis Khryashchev + Svarmit Singh Parsicha mapped the stations and divided them into the Brooklyn ones and Manhattan ones. Denis Khryashchev with assistance of Kiran Venkata Palla performed leftjoin of the station boroughs to the original table. Denis Khryashchev performed the calculation of the weekdays and weekends + summary.
2. Kiran Venkata Palla performed the chi-squared test and assisted in creating the left-joins.
3. Manushi Aashish Majumdar performed the z-score test + participated in the formulation of the hypothesis.
4. Alan Polson: formulated the hypothesis, prepared valuable comments.
5. Svarmit Singh Pasricha mapped the stations to find out which of them are in Brooklyn and Which are in Manhatta.