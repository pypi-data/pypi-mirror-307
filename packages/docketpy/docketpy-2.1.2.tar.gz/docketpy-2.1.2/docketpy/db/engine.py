USERNAME="docket"
PASSWORD="docket"
HOST="localhost"
PORT=5432
DATABASE="docket_db"
DATABASE_URL = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(USERNAME, PASSWORD, HOST, PORT, DATABASE)

if __name__ == "__main__":
    print(DATABASE_URL)
