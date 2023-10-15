from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import configparser


config = configparser.ConfigParser()
config.read('/Users/p.matchenkov/Desktop/configurations/config.ini')
password, localhost, bd_type, bd_name, login = (config['DXCORE_prod']['password'], config['DXCORE_prod']['localhost'],
                                                config['DXCORE_prod']['bd_type'], config['DXCORE_prod']['bd_name'],
                                                config['DXCORE_prod']['login'])

DX_BASE_URL = f'{bd_type}://{login}:{password}@{localhost}/{bd_name}'
engine = create_engine(DX_BASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

