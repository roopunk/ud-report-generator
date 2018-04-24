# ud-report-builder

This repo contains a python script to extract three kinds of data from a 
postgresql news database.

1. What are the most popular three articles of all time.
2. What are the most popular article authors of all time.
3. On which days did more than 1% of requests lead to errors.

## How to Run

* Make sure that `python3` and `psycopg2` module are installed.
* Make sure that postgresql server is up and running with the news database imported
* Run the script by `python3 generate_report.py`

This will create a report.txt file which contains human readable data for the above three queries in the same diretory.

## Design

The script use `psycopg2` module to connect to the database and run queries.
All the three data sets have been done using a single query using joins, the result of which
are stored in three seprate variables which is later used to write into a file to create the report.

All three queries use subqueries to create a data set, on which join is performed. 
We also using string operations `||` to concatenate strings to match article slugs with path in 
log table, since it contains the full URI including `/article/`

We are also using `cast()` in the third query to find out percentage upto 2 decimal places.  
