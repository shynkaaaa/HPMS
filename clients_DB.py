from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import asyncio

from fastapi import FastAPI

#создание асинхронного движка
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./sql_app.db"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

class Base(DeclarativeBase): pass


class Patients(Base):
    __tablename__ = 'Patients'

    id = Column(Integer, primary_key=True)
    IIN = Column(String)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    phone = Column(String)
    date_of_birth = Column(String)
    address = Column(String)
    role_id = Column(Integer, ForeignKey('Roles.id'))


class Doctors(Base):
    __tablename__ = 'Doctors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    phone = Column(String)
    experience = Column(String)
    date_of_birth = Column(String)
    office_id = Column(Integer, ForeignKey('Offices.id'))
    category_id = Column(Integer, ForeignKey('Categories.id'))
    lunch_starts = Column(String)
    lunch_ends = Column(String)


class Roles(Base):
    __tablename__ = 'Roles'

    id = Column(Integer, primary_key=True)
    title = Column(String)


class Categories(Base):
    __tablename__ = 'Categories'

    id = Column(Integer, primary_key=True)
    title = Column(String)


class Offices(Base):
    __tablename__ = 'Offices'

    id = Column(Integer, primary_key=True)
    address = Column(String)
    contact = Column(String)


class Slots(Base):
    __tablename__ = 'Slots'

    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey('Doctors.id'))
    office_id = Column(Integer, ForeignKey('Offices.id'))
    type = Column(String)
    date = Column(String)
    starts_at = Column(String)
    ends_at = Column(String)
    precalculated_cost = Column(String)
    final_cost = Column(String)


class Appointments(Base):
    __tablename__ = 'Appointments'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('Patients.id'))
    doctor_id = Column(Integer, ForeignKey('Doctors.id'))
    office_id = Column(Integer, ForeignKey('Offices.id'))
    slot_id = Column(Integer, ForeignKey('Slots.id'))
    status = Column(String)
    cost = Column(Integer)


class Tests(Base):
    __tablename__ = 'Tests'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('Patients.id'))
    title = Column(String)
    result = Column(String)


class Permissions(Base):
    __tablename__ = 'Permissions'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('Patients.id'))
    doctor_id = Column(Integer, ForeignKey('Doctors.id'))
    exp_date = Column(String)


class Medical_History(Base):
    __tablename__ = 'Medical_History'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('Patients.id'))
    test_id = Column(Integer, ForeignKey('Tests.id'))
    date = Column(String)
    anamnesis = Column(String)
    conclusion = Column(String)
    prescription = Column(String)
    recipe = Column(String)

#сессия тоже асинхронная
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession)

#асинхронная функция для инициализации базы данных
async def init_db():
    async with engine.begin() as conn:
        print("начал") #проверка
        # await conn.run_sync(Base.metadata.drop_all) #на всякий
        await conn.run_sync(Base.metadata.create_all)
    print("закончил")

#запуск
if __name__ == "__main__":
    asyncio.run(init_db())

app = FastAPI()