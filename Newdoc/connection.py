from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.sql import BASE
#from fastapi 

db_user: str = 'postgres'
db_port: int = 5432
db_host: str ='localhost'
db_password: str ='pgadmin'

uri: str = F'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/to_do_app'

engine = create_engine(uri)

BASE.metadata.create_all(bind = engine)

#session
session = sessionmaker(
    bind=engine,
    autoflush=True
)

db_session = session()

try:
    connection = engine.connect()
    connection.close()
    print('ping, Connected Successfully')

except Exception as e:
    print(f'Error: {str(e)}') 