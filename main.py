from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import pandas as pd
from fastapi.staticfiles import StaticFiles


from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Connect to the SQLite database
conn = sqlite3.connect('cars.db')
cursor = conn.cursor()

# Read the CSV file using pandas
df = pd.read_csv('cars.csv')

# Infer data types for the table columns
column_types = {}
for column in df.columns:
    column_data = df[column]
    if column_data.dtype == 'object':
        column_types[column] = 'TEXT'
    elif column_data.dtype == 'int64':
        column_types[column] = 'INTEGER'
    elif column_data.dtype == 'float64':
        column_types[column] = 'REAL'
    else:
        column_types[column] = 'TEXT'

print(column_types)

# Connect to the SQLite database
conn = sqlite3.connect('cars.db')
cursor = conn.cursor()


# Create the cars table based on the inferred column types
create_table_sql = 'CREATE TABLE IF NOT EXISTS cars (\n'
for column, data_type in column_types.items():
    create_table_sql += f"{'_'.join(column.split(' '))} {data_type},\n"
create_table_sql = create_table_sql.rstrip(',\n') + '\n)'
cursor.execute(create_table_sql)

# Check if the table is empty
cursor.execute("SELECT count(*) FROM cars")
table_empty = cursor.fetchone()[0] == 0

# If the table is empty, create it and insert the data
if table_empty:
    make_index_sql = 'CREATE INDEX idx_make ON cars (Make)'
    cursor.execute(make_index_sql)
    model_index_sql = 'CREATE INDEX idx_model ON cars (Model)'
    cursor.execute(model_index_sql)
    conn.commit()
    # Insert the data into the cars table
    insert_sql = 'INSERT INTO cars VALUES ('
    for _ in range(len(column_types.items()) - 1):
        insert_sql += '?, '
    insert_sql += '?)'
    print(insert_sql)
    values = [tuple(row) for row in df.values]
    cursor.executemany(insert_sql, values)

    # Commit the changes and close the connection
    conn.commit()

limit = 6

@app.get("/search")
@cache(expire=300)
async def search_cars(q: str, page: int = 0):
    query = q.strip()

    # Split the query by spaces and create a list of search terms
    search_terms = query.split()
    # print(search_terms)s
    try:
        # Prepare the SQL statement with multiple search conditions
        conditions = " AND ".join(
            ["Make LIKE ? OR Model LIKE ?"] * len(search_terms))
        params = [(f"%{term}%") for term in search_terms]
        # print(conditions, params)
        cursor.execute(
            f"SELECT * FROM cars WHERE {conditions} LIMIT {limit} OFFSET {page*limit}", params*2)
        # print(conditions, params)
        results = cursor.fetchall()

        # Convert the results to a JSON dictionary
        columns = [column[0] for column in cursor.description]
        results_dict = [dict(zip(columns, row)) for row in results]

        return results_dict

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.mount("/", StaticFiles(directory="static", html=True), name="static")


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
