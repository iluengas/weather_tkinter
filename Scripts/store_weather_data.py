import sqlite3 as sql

database = "weather_patterns.db"


def create_database():
    connection = sql.connect(database)
    cursor = connection.cursor()

    create_cities_table = """
        CREATE TABLE IF NOT EXISTS cities (
            city_id INTEGER PRIMARY KEY,
            city_name VARCHAR(50) NOT NULL
        )
    """

    create_daily_weather_table = """
        CREATE TABLE IF NOT EXISTS daily_weather (
            weather_id INTEGER PRIMARY KEY,
            city_id INTEGER,
            date DATE,
            temperature REAL,
            wind_speed REAL,
            humidity REAL,
            pressure REAL,
            FOREIGN KEY (city_id) REFERENCES cities (city_id)
        )
    """

    try:
        cursor.execute(create_cities_table)
        cursor.execute(create_daily_weather_table)
        connection.commit()
    except Exception as e:
        print(e)
        connection.rollback()
    finally:
        cursor.close()
        connection.close()


def store_city(city_name):
    connection = sql.connect(database)
    cursor = connection.cursor()
    add_city = """
                INSERT INTO cities (city_name) VALUES (?)
                """

    try:
        cursor.execute(add_city, (city_name,))
        connection.commit()
    except Exception as e:
        print(e)
        connection.rollback()
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    # This block will be executed if the script is run directly
    create_database()
    store_city("santa barbara")
