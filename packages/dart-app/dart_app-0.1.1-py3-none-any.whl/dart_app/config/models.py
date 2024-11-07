from sqlalchemy import Column, Integer, String, Date, Time, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MainLog(Base):
    __tablename__ = "main_log"
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    time = Column(Time)
    level = Column(String)
    message = Column(String)


class LoginLog(Base):
    __tablename__ = "login_log"
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    time = Column(Time)
    level = Column(String)
    message = Column(String)


class SetupLog(Base):
    __tablename__ = "setup_log"
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    time = Column(Time)
    level = Column(String)
    message = Column(String)


# Add any other tables you need for logging in other modules

# Setup database engine and session
engine = create_engine("sqlite:///dart_logs.db")
Base.metadata.create_all(engine)
