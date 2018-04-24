# ud-report-builder

This repo contains a python script to extract three kinds of data from a 
postgresql news database.

1. What are the most popular three articles of all time.
2. What are the most popular arcticle authors of all time.
3. On which days did more than 1% of requests lead to errors.

## How to Run

* Make sure that `python3` and `psycopg2` module are installed.
* Make sure that postgresql server is up and running with the news database imported
* Run the script by `python3 generate_report.py`

This will create a report.txt file which contains human readable data for the above three queries.
