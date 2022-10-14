import openpyxl
import psycopg2

# Define variable to load the wookbook
wookbook = openpyxl.load_workbook("Справочник ТС.xlsx")

# Define variable to read the active sheet:
worksheet = wookbook.active

# Iterate the loop to read the cell values
dc = dict()
c = 0
for i in range(1, 139):
    for col in worksheet.iter_cols(2, 2):
        dc[col[i].value] = dc.get(col[i].value, 0) + 1

print(list(dc.items()))

pg_database = 'polus'
pg_username = 'postgres'
pg_password = 'postgres'
pg_host = '127.0.0.1'

with psycopg2.connect(dbname=pg_database,
                      user=pg_username,
                      password=pg_password,
                      host=pg_host) as conn:
    with conn.cursor() as cursor:
        for type_, amount in list(dc.items()):
            cursor.execute(f"""INSERT INTO transports VALUES ('{type_}', {amount})""")
