from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os
load_dotenv()




CONNECTION_DB = os.environ["SQLALCHEMY_DATABASE_URI"]
Base = declarative_base()

class TribuPlatform(Base):
    __tablename__ = 'tribu_platform'
    platform_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

class TribuServices(Base):
    __tablename__ = 'tribu_services'
    service_id = Column(Integer, primary_key=True)
    name = Column(String(255))
    platform_id = Column(Integer, ForeignKey('tribu_platform.platform_id'))
    platform = relationship("TribuPlatform")


def get_all_services_with_platform():
    engine = create_engine(CONNECTION_DB)

    # Crea las tablas en la base de datos
    Base.metadata.create_all(engine)

    # Crea una sesión para interactuar con la base de datos
    Session = sessionmaker(bind=engine)
    session = Session()

    # Consulta para obtener todos los servicios con el nombre de la plataforma
    services_with_platform = session.query(TribuServices, TribuPlatform).join(TribuPlatform).all()

    return services_with_platform
    