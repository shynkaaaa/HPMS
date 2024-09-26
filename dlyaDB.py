from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import Column, Integer, String
from faker import Faker
from sqlalchemy.orm import Session
from datetime import datetime

from fastapi import FastAPI

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

class Base(DeclarativeBase): pass

class Patients(Base):
    __tablename__ = 'Patients'

    patient_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)
    IIN = Column(String)
    date_of_birth = Column(String)
    password = Column(String)
    registration_date = Column(String)

class Doctors(Base):
    __tablename__ = 'Doctors'

    doctor_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    category = Column(String)
    email = Column(String)
    phone = Column(String)
    office_number = Column(String)
    password = Column(String)
    registration_date = Column(String)

class Manager(Base):
    __tablename__ = 'Managers'

    manager_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)
    password = Column(String)

class Notifications(Base):
    __tablename__ = 'Notifications'

    notification_id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('Patients.patient_id'))
    doctor_id = Column(Integer, ForeignKey('Doctors.doctor_id'))
    notification_type = Column(String)
    notification_date = Column(String)

class Appointments(Base):
    __tablename__ = 'Appointments'

    appointment_id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('Patients.patient_id'))
    doctor_id = Column(Integer, ForeignKey('Doctors.doctor_id'))
    manager_id = Column(Integer, ForeignKey('Managers.manager_id'))
    appointment_date = Column(String)
    appointment_type = Column(String)
    status = Column(String)
    treatment_details = Column(String)

class Receipts(Base):
    __tablename__ = 'Receipts'

    receipt_id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('Patients.patient_id'))
    doctor_id = Column(Integer, ForeignKey('Doctors.doctor_id'))
    appointment_id = Column(Integer, ForeignKey('Appointments.appointment_id'))
    total_cost = Column(Integer)
    appointment_type = Column(String)
    payment_status = Column(String)
    payment_date = Column(String)

class Medical_History(Base):
    __tablename__ = 'Medical_History'

    history_id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('Patients.patient_id'))
    doctor_id = Column(Integer, ForeignKey('Doctors.doctor_id'))
    manager_id = Column(Integer, ForeignKey('Managers.manager_id'))
    visit_date = Column(String)
    tests = Column(String)
    anemnesis = Column(String)
    conclusion = Column(String)
    prescription = Column(String)
    treatment_cost = Column(Integer)

class Prices(Base):
    __tablename__ = 'Prices'

    price_id = Column(Integer, primary_key=True)
    category = Column(String, ForeignKey('Doctors.category'))
    visit_cost = Column(Integer)
    treatment_cost = Column(Integer)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()
#
# fake = Faker()
#
# def create_test_data(ses: Session):
#     for _ in range(10):
#         patient = Patients(
#             first_name=fake.first_name(),
#             last_name=fake.last_name(),
#             email=fake.email(),
#             phone=fake.bothify(text='87#########'),
#             IIN=fake.bothify(text='############'),
#             date_of_birth=fake.date_of_birth().isoformat(),
#             password=fake.password(),
#             registration_date=str(datetime.now()),
#         )
#         ses.add(patient)
#
#     categories = [
#         "Cardiologist", "Dermatologist", "Endocrinologist", "Gastroenterologist",
#         "Neurologist", "Oncologist", "Ophthalmologist", "Orthopedic Surgeon",
#         "Pediatrician", "Psychiatrist", "Pulmonologist", "Radiologist",
#         "Rheumatologist", "Urologist", "General Practitioner"
#     ]
#
#     for i in range(15):
#         doctor = Doctors(
#             first_name=fake.first_name(),
#             last_name=fake.last_name(),
#             category=categories[i],
#             email=fake.email(),
#             phone=fake.bothify(text='87#########'),
#             office_number=fake.bothify(text='##'),
#             password=fake.password(),
#             registration_date=str(datetime.now()),
#         )
#         ses.add(doctor)
#
#     for _ in range(2):
#         manager = Manager(
#             first_name=fake.first_name(),
#             last_name=fake.last_name(),
#             email=fake.email(),
#             phone=fake.bothify(text='877########'),
#             password=fake.password(),
#         )
#         ses.add(manager)
#     for i in range(10):
#         doctor = Doctors(
#             doctor_id=i + 1,
#         )
#
#         appointment = Appointments(
#             patient_id=fake.random_int(min=1, max=10),
#             doctor_id=doctor.doctor_id,
#             manager_id=fake.random_int(min=1, max=2),
#             appointment_date=str(fake.date_time_this_year()),
#             appointment_type=fake.random_element(elements=("Visit", "Treatment")),
#             status="Booked",
#             treatment_details=fake.text(max_nb_chars=50)
#         )
#         ses.add(appointment)
#     for i in range(10):
#         doctor = Doctors(
#             doctor_id=i + 1,
#         )
#
#         receipt=Receipts(
#             patient_id=fake.random_int(min=1, max=10),
#             doctor_id=doctor.doctor_id,
#             appointment_id=fake.random_int(min=1, max=10),
#             total_cost=fake.random_int(min=50, max=500),
#             appointment_type=fake.random_element(elements=("Visit", "Treatment")),
#             payment_status=fake.random_element(elements=("Paid", "Unpaid")),
#             payment_date=str(fake.date_time_this_year())
#         )
#         ses.add(receipt)
#     ses.commit()
#
# create_test_data(db)
app = FastAPI()