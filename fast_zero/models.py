from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


class Position(Enum):
    physiotherapist = 'physiotherapist'
    intern = 'intern'


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())


@table_registry.mapped_as_dataclass
class Patient:
    __tablename__ = 'patients'

    patient_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    full_name: Mapped[str]
    age: Mapped[int]
    place_of_birth: Mapped[str]
    marital_status: Mapped[str]
    gender: Mapped[str]
    profession: Mapped[str]
    residential_address: Mapped[str]
    commercial_address: Mapped[str]

    clinical_history = relationship('ClinicalHistory', back_populates='patient')
    clinical_examination = relationship('ClinicalExamination', back_populates='patient')
    complementary_exams = relationship('ComplementaryExams', back_populates='patient')
    physiotherapy_diagnosis = relationship('PhysiotherapyDiagnosis', back_populates='patient')
    prognosis = relationship('Prognosis', back_populates='patient')
    treatment_plan = relationship('TreatmentPlan', back_populates='patient')
    evolution_records = relationship('EvolutionRecords', back_populates='patient')


@table_registry.mapped_as_dataclass
class ClinicalHistory:
    __tablename__ = 'clinical_histories'

    history_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey('patients.patient_id'))
    main_complaint: Mapped[str]
    disease_history: Mapped[str]
    lifestyle_habits: Mapped[str]
    previous_treatments: Mapped[str]
    personal_family_history: Mapped[str]
    other_information: Mapped[str] = None

    patient = relationship('Patient', back_populates='clinical_history')


@table_registry.mapped_as_dataclass
class ClinicalExamination:
    __tablename__ = 'clinical_examinations'

    exam_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey('patients.patient_id'))
    exam_details: Mapped[str]

    patient = relationship('Patient', back_populates='clinical_examination')


@table_registry.mapped_as_dataclass
class ComplementaryExams:
    __tablename__ = 'complementary_exams'

    comp_exam_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey('patients.patient_id'))
    exam_details: Mapped[str]

    patient = relationship('Patient', back_populates='complementary_exams')


@table_registry.mapped_as_dataclass
class PhysiotherapyDiagnosis:
    __tablename__ = 'physiotherapy_diagnosis'

    diagnosis_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey('patients.patient_id'))
    diagnosis_details: Mapped[str]

    patient = relationship('Patient', back_populates='physiotherapy_diagnosis')


@table_registry.mapped_as_dataclass
class Prognosis:
    __tablename__ = 'prognosis'

    prognosis_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey('patients.patient_id'))
    prognosis_details: Mapped[str]

    patient = relationship('Patient', back_populates='prognosis')


@table_registry.mapped_as_dataclass
class TreatmentPlan:
    __tablename__ = 'treatments_plan'

    plan_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey('patients.patient_id'))
    objectives: Mapped[str]
    probable_sessions: Mapped[int]
    procedures: Mapped[str]

    patient = relationship('Patient', back_populates='treatment_plan')


@table_registry.mapped_as_dataclass
class Professional:
    __tablename__ = 'professionals'

    professional_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    full_name: Mapped[str]
    position: Mapped[Position]
    registration_number: Mapped[str]

    evolution_records = relationship('EvolutionRecords', back_populates='professional')


@table_registry.mapped_as_dataclass
class EvolutionRecords:
    __tablename__ = 'evolution_records'

    record_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey('patients.patient_id'))
    professional_id: Mapped[int] = mapped_column(ForeignKey('professionals.professional_id'))
    date = Mapped[datetime.date]
    procedures: Mapped[str]
    complications: Mapped[str]
    health_status_evolution: Mapped[str]

    patient = relationship('Patient', back_populates='evolution_records')
    professional = relationship('Professional', back_populates='evolution_records')
