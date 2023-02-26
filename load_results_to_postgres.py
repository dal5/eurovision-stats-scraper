import psycopg2

def create_connection():
    connection = psycopg2.connect(
        database="XXX",
        user="XXX",
        password="XXX",
        host="XXX",
        port="XXX"
    )
    connection.autocommit = True
    return connection


def create_tables():
    connection = create_connection()
    cursor = connection.cursor()

    # Remove table if already exists
    sql = "DROP TABLE IF EXISTS eurovision_stats.finals"
    cursor.execute(sql)

    # Remove schema if already exists
    sql = "DROP SCHEMA IF EXISTS eurovision_stats"
    cursor.execute(sql)

    # Create schema
    sql = "CREATE SCHEMA eurovision_stats"
    cursor.execute(sql)

    # Set up table for eurovision finals
    sql = "CREATE TABLE eurovision_stats.finals" \
          "(" \
          "contest_year smallint, " \
          "running_order smallint," \
          "country varchar(50), " \
          "artist varchar(200), " \
          "song varchar(250), " \
          "language varchar(250), " \
          "points smallint, " \
          "place smallint" \
          ")"
    cursor.execute(sql)
    connection.close()


def load(rows):
    connection = create_connection()
    cursor = connection.cursor()

    for row in rows:
        for item in row:
            item.replace("'", "''")

        sql = "INSERT INTO eurovision_stats.finals VALUES " + str(row).replace('[', '(').replace(']', ')')
        print(sql)
        cursor.execute(sql)

    connection.close()
