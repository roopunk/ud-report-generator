#!/usr/bin/env python3

import psycopg2

db = psycopg2.connect(database='news')
c = db.cursor()

# First Query
c.execute("""
    select
        articles.title,
        l.count
    from
        (
            select
                path,
                count(*) as count
            from log
            where
                log.path != '/'
            group by path
            order by count(*) desc
            limit 3
        ) l join articles
    on l.path = '/article/' || articles.slug
    order by l.count desc
    """)
top_articles = c.fetchall()

# Top authors
c.execute("""
    select
        authors.name,
        l.count
    from (
        select
            count(*),
            articles.author
        from log, articles
        where
            log.path = '/article/' || articles.slug and
            log.path != '/'
        group by articles.author
        order by count(*) desc
    ) l join authors
    on authors.id = l.author
    order by l.count desc
""")
top_authors = c.fetchall()

# Days with more than 1% errors
c.execute("""
    select
        error_table.date,
        round(
            (cast(error_table.count*100 as decimal)/all_table.count), 2) ||
            '%'
        from
        (
            select
                date(time) as date,
                count(*)  as count
            from log
            where status != '200 OK'
            group by date(time)
        ) error_table join
        (
            select
                date(time) as date,
                count(*)  as count
            from log
            group by date(time)
        ) all_table
        on error_table.date = all_table.date
        where error_table.count * 100 > all_table.count
""")
error_days = c.fetchall()

# Writing data to a report file

file = open("report.txt", "w")
file.write("## Report\n\n")

file.write("### 1. Top Articles of all time \n\n")
for row in top_articles:
    file.write(str(row[0]) + ": " + str(row[1]) + " views" + "\n")

file.write("\n\n")
file.write("### 2. Authors with most views on their articles\n\n")
for row in top_authors:
    file.write(str(row[0]) + ": " + str(row[1]) + " views" + "\n")

file.write("\n\n")
file.write("### 3. Days when error rate was more than 1%\n\n")
for row in error_days:
    file.write(str(row[0]) + ": " + str(row[1]) + "\n")
file.close()

db.close()
