import psycopg2 #imports the DB-API module

conn = psycopg2.connect("dbname=news") #connects to the database 'news' and creates a variable for this.
cursor = conn.cursor() #makes a cursor with the connection and creates a variable for this.
def execute(question):
#function for executing a query.
    cursor.execute(question)

query = "select title, count(title) as Views from articles, log where log.path like concat ('%', articles.slug) group by title order by views desc limit 3;"

execute(query)
rows = cursor.fetchall()
print ("\nTop 3 Articles:")
for row in rows:
    print ("Article: '" + str(row[0]) + "' - " + str(row[1]) + " Views")

query = "select authors.name, count(articles.author) as Views from articles, log, authors where log.path like concat ('%', articles.slug) and articles.author = authors.id group by authors.name order by Views desc;"

execute(query)
rows = cursor.fetchall()
print ("\nPopular Authors:")
for row in rows:
    print ("Author: " + str(row[0]) + " - " + str(row[1]) + " Views")

query = "select Date, (Error::float * 100) / Total::float as Percent from (select time::timestamp::date as Date, count(status) as Total, sum(case when status like '%404%' then 1 end) as Error from log group by Date) as Result where (Error::float * 100)/ Total::float > 1.0;"

execute(query)
rows = cursor.fetchall()
print ("\nDay where More than 1 Percent of Requests Lead to Errors:")
for row in rows:
    print ("Date: " + str(row[0]) + " - " + str(row[1]) + "% Errors")

conn.close() #closes the connection.