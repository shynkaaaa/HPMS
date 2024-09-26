from datetime import timedelta, datetime, timezone

from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from auth import create_access_token, verify_password, get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES, verify_token
from dlyaDB import Patients
from dlyaDB import SessionLocal
from schemas import PatientCreate, PatientLogin

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#пост для реги пациентов
@app.post("/patient/auth/sign-up")
def register_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    #чекает на наличие эмейла в базе
    existing_patient = db.query(Patients).filter(Patients.email == patient.email).first()
    if existing_patient:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(patient.password)

    #создаем клиента
    new_patient = Patients(
        first_name=patient.first_name,
        last_name=patient.last_name,
        email=patient.email,
        phone=patient.phone,
        IIN=patient.IIN,
        date_of_birth=patient.date_of_birth,
        password=hashed_password,
        registration_date=datetime.now(
            timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return {"message": "Patient registered successfully", "patient_id": new_patient.patient_id}


#пост для логина пациентов
@app.post("/patient/auth/sign-in")
def login_patient(patient: PatientLogin, db: Session = Depends(get_db)):
    #чекаем почту
    db_patient = db.query(Patients).filter(Patients.email == patient.email).first()

    if not db_patient:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    #чекаем пароль
    if not verify_password(patient.password, db_patient.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    #jwt токены для пациентов
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": db_patient.patient_id}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


# получаем детали клиента
@app.get("/patient/auth/me")
def get_current_user(Authorization: str = Header(...), db: Session = Depends(get_db)):
    token = Authorization.replace("Bearer ", "")
    user_id = verify_token(token)

    db_patient = db.query(Patients).filter(Patients.patient_id == user_id).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "first_name": db_patient.first_name,
        "last_name": db_patient.last_name,
        "email": db_patient.email,
        "phone": db_patient.phone,
        "IIN": db_patient.IIN,
        "date_of_birth": db_patient.date_of_birth
    }


#отправляет в почту верификацию(пример)
@app.post("/patient/auth/email")
def send_verification_email(email: str, db: Session = Depends(get_db)):

    db_patient = db.query(Patients).filter(Patients.email == email).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Email not found")

    #функция блаблабла
    #считайте что отправили

    return {"message": "Verification email sent"}