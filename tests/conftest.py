import factory
import factory.fuzzy
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import (
    ClinicalExamination,
    ClinicalHistory,
    ComplementaryExams,
    Patient,
    PhysiotherapyDiagnosis,
    Position,
    Professional,
    Prognosis,
    TreatmentPlan,
    User,
    table_registry,
)
from fast_zero.security import get_password_hash


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')


class PatientFactory(factory.Factory):
    class Meta:
        model = Patient

    full_name = factory.Faker('text')
    age = factory.Faker('random_int', min=10, max=99)
    place_of_birth = factory.Faker('text')
    marital_status = factory.Faker('text')
    gender = factory.Faker('text')
    profession = factory.Faker('text')
    residential_address = factory.Faker('text')
    commercial_address = factory.Faker('text')


class ClinicalHistoryFactory(factory.Factory):
    class Meta:
        model = ClinicalHistory

    main_complaint = factory.Faker('text')
    disease_history = factory.Faker('text')
    lifestyle_habits = factory.Faker('text')
    previous_treatments = factory.Faker('text')
    personal_family_history = factory.Faker('text')
    other_information = factory.Faker('text')
    patient_id = 1


class ClinicalExaminationFactory(factory.Factory):
    class Meta:
        model = ClinicalExamination

    exam_details = factory.Faker('text')
    patient_id = 1


class ComplementaryExamFactory(factory.Factory):
    class Meta:
        model = ComplementaryExams

    exam_details = factory.Faker('text')
    patient_id = 1


class PhysiotherapyDiagnosisFactory(factory.Factory):
    class Meta:
        model = PhysiotherapyDiagnosis

    diagnosis_details = factory.Faker('text')
    patient_id = 1


class PrognosisFactory(factory.Factory):
    class Meta:
        model = Prognosis

    prognosis_details = factory.Faker('text')
    patient_id = 1


class TreatmentPlanFactory(factory.Factory):
    class Meta:
        model = TreatmentPlan

    patient_id = 1
    objectives = factory.Faker('text')
    probable_sessions = factory.Faker('random_int', min=1, max=10)
    procedures = factory.Faker('text')


class ProfessionalFactory(factory.Factory):
    class Meta:
        model = Professional

    full_name = factory.Faker('name')
    position = factory.Iterator([Position.physiotherapist, Position.intern])
    registration_number = factory.Faker('bothify', text='######')


@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture()
def user(session):
    pwd = 'testtest'
    user = UserFactory(password=get_password_hash(pwd))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'testtest'

    return user


@pytest.fixture()
def other_user(session):
    user = UserFactory()

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture()
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']


@pytest.fixture()
def patient(session):
    patient = PatientFactory.create()
    session.add(patient)
    session.commit()
    return patient
