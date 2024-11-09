import os 
LOGS_BUCKET = "st-temp-docket-logs-bucket"
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
# print(f"REDIS_HOST: {REDIS_HOST}")
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
# print(f"REDIS_PORT: {REDIS_PORT}")
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
# print(f"POSTGRES_HOST: {POSTGRES_HOST 
POSTGRES_USER = os.getenv('POSTGRES_USER', 'docket')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'docket')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'docket_db')
# print(f"POSTGRES_DB: {POSTGRES_DB}")
POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', 5432))
# print(f"POSTGRES_PORT: {POSTGRES_PORT}")