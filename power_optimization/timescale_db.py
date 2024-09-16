import psycopg2
from psycopg2.extras import RealDictCursor
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def get_timescale_connection():
    try:
        connection = psycopg2.connect(
            dbname=settings.DATABASES["timescale"]["NAME"],
            user=settings.DATABASES["timescale"]["USER"],
            password=settings.DATABASES["timescale"]["PASSWORD"],
            host=settings.DATABASES["timescale"]["HOST"],
            port=settings.DATABASES["timescale"]["PORT"],
        )
        return connection
    except psycopg2.Error as e:
        logger.error(f"Error connecting to TimescaleDB: {e}")
        return None


def create_power_readings_table():
    conn = get_timescale_connection()
    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS power_readings (
                    time TIMESTAMPTZ NOT NULL,
                    sensor_id INTEGER,
                    current FLOAT
                );
                """
            )
            cur.execute(
                "SELECT create_hypertable('power_readings', 'time', if_not_exists => TRUE);"
            )
        conn.commit()
        logger.info("Power readings table created successfully")
    except psycopg2.Error as e:
        logger.error(f"Error creating power readings table: {e}")
        conn.rollback()
    finally:
        conn.close()


def insert_power_reading(sensor_id, timestamp, current):
    conn = get_timescale_connection()
    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO power_readings (time, sensor_id, current)
                VALUES (%s, %s, %s)
                """,
                (timestamp, sensor_id, current),
            )
        conn.commit()
        logger.info(f"Power reading inserted for sensor {sensor_id}")
    except psycopg2.Error as e:
        logger.error(f"Error inserting power reading: {e}")
        conn.rollback()
    finally:
        conn.close()


def get_latest_power_readings(sensor_id, limit=100):
    conn = get_timescale_connection()
    if conn is None:
        return []

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT time, sensor_id, current
                FROM power_readings
                WHERE sensor_id = %s
                ORDER BY time DESC
                LIMIT %s
                """,
                (sensor_id, limit),
            )
            return cur.fetchall()
    except psycopg2.Error as e:
        logger.error(f"Error retrieving power readings: {e}")
        return []
    finally:
        conn.close()
