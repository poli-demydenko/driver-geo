from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import psycopg2
from psycopg2.extras import RealDictCursor
import logging
import os
import time
from fastapi.openapi.utils import get_openapi

app = FastAPI()

with open('settings.json') as f:
    settings = json.load(f)

logging.basicConfig(level=logging.INFO)

def connect_db(retries=5, delay=5):
    for i in range(retries):
        try:
            conn = psycopg2.connect(
                dbname=settings['db']['database'],
                user=settings['db']['user'],
                password=settings['db']['password'],
                host=settings['db']['host'],
                port=settings['db']['port']
            )
            return conn
        except psycopg2.OperationalError as e:
            logging.error(f"Error connecting to the database: {e}")
            time.sleep(delay)
    raise Exception("Failed to connect to the database after multiple retries")

conn = connect_db()

class DriverData(BaseModel):
    driver_id: int
    latitude: float
    longitude: float
    speed: float
    altitude: float

@app.post("/api/v1/driver-geo")
async def driver_geo(data: list[DriverData]):
    global conn
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            for entry in data:
                is_correct = (
                    entry.speed <= settings['thresholds']['max_speed'] and
                    settings['thresholds']['min_altitude'] <= entry.altitude <= settings['thresholds']['max_altitude']
                )
                
                cur.execute("""
                    INSERT INTO driver_geo (driver_id, latitude, longitude, speed, altitude, is_correct)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """, (entry.driver_id, entry.latitude, entry.longitude, entry.speed, entry.altitude, is_correct))
                
                if not is_correct:
                    logging.info(f"Anomalous data: {entry}")
                    
        conn.commit()
    except Exception as e:
        logging.error("Failed to process data: ", e)
        conn = connect_db()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    return {"status": "success"}

@app.on_event("startup")
async def startup():
    global conn
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS driver_geo (
                id SERIAL PRIMARY KEY,
                driver_id INT,
                latitude FLOAT,
                longitude FLOAT,
                speed FLOAT,
                altitude FLOAT,
                is_correct BOOLEAN
            )
        """)
        conn.commit()

@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint():
    return get_openapi(title="Driver Geo API", version="1.0.0", routes=app.routes)

@app.get("/docs", include_in_schema=False)
async def get_documentation():
    return get_openapi(title="Driver Geo API", version="1.0.0", routes=app.routes)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)