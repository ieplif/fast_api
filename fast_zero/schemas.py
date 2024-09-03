from datetime import date
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from fast_zero.models import Position


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: List[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


# Schemas para Patient (Paciente)
class PatientBase(BaseModel):
    full_name: Optional[str]
    age: Optional[int]
    place_of_birth: Optional[str]
    marital_status: Optional[str]
    gender: Optional[str]
    profession: Optional[str]
    residential_address: Optional[str]
    commercial_address: Optional[str]


class PatientCreate(PatientBase):
    full_name: str


class Patient(PatientBase):
    patient_id: int
    clinical_history: List['ClinicalHistory'] = []
    clinical_examination: List['ClinicalExamination'] = []
    complementary_exams: List['ComplementaryExams'] = []
    physiotherapy_diagnosis: List['PhysiotherapyDiagnosis'] = []
    prognosis: List['Prognosis'] = []
    treatment_plan: List['TreatmentPlan'] = []
    evolution_records: List['EvolutionRecords'] = []

    class Config:
        from_attributes = True


class PatientUpdate(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    place_of_birth: Optional[str] = None
    marital_status: Optional[str] = None
    gender: Optional[str] = None
    profession: Optional[str] = None
    residential_address: Optional[str] = None
    commercial_address: Optional[str] = None


# Schemas para ClinicalHistory (Histórico Clínico)
class ClinicalHistoryBase(BaseModel):
    main_complaint: Optional[str]
    disease_history: Optional[str]
    lifestyle_habits: Optional[str]
    previous_treatments: Optional[str]
    personal_family_history: Optional[str]
    other_information: Optional[str]


class ClinicalHistoryCreate(ClinicalHistoryBase):
    pass


class ClinicalHistory(ClinicalHistoryBase):
    history_id: int
    patient_id: int

    class Config:
        from_attributes = True


class ClinicalHistoryUpdate(BaseModel):
    main_complaint: Optional[str] = None
    disease_history: Optional[str] = None
    lifestyle_habits: Optional[str] = None
    previous_treatments: Optional[str] = None
    personal_family_history: Optional[str] = None
    other_information: Optional[str] = None


# Schemas para ClinicalExamination (Exame Clínico)
class ClinicalExaminationBase(BaseModel):
    exam_details: Optional[str]


class ClinicalExaminationCreate(ClinicalExaminationBase):
    pass


class ClinicalExamination(ClinicalExaminationBase):
    exam_id: int
    patient_id: int

    class Config:
        from_attributes = True


class ClinicalExaminationUpdate(BaseModel):
    exam_details: Optional[str] = None


# Schemas para ComplementaryExams (Exames Complementares)
class ComplementaryExamsBase(BaseModel):
    exam_details: Optional[str]


class ComplementaryExamsCreate(ComplementaryExamsBase):
    pass


class ComplementaryExams(ComplementaryExamsBase):
    comp_exam_id: int
    patient_id: int

    class Config:
        from_attributes = True


class ComplementaryExamsUpdate(BaseModel):
    exam_details: Optional[str] = None


# Schemas para PhysiotherapyDiagnosis (Diagnóstico Fisioterapêutico)
class PhysiotherapyDiagnosisBase(BaseModel):
    diagnosis_details: Optional[str]


class PhysiotherapyDiagnosisCreate(PhysiotherapyDiagnosisBase):
    pass


class PhysiotherapyDiagnosis(PhysiotherapyDiagnosisBase):
    diagnosis_id: int
    patient_id: int

    class Config:
        from_attributes = True


# Schemas para Prognosis (Prognóstico)
class PrognosisBase(BaseModel):
    prognosis_details: Optional[str]


class PrognosisCreate(PrognosisBase):
    pass


class Prognosis(PrognosisBase):
    prognosis_id: int
    patient_id: int

    class Config:
        from_attributes = True


# Schemas para TreatmentPlan (Plano de Tratamento)
class TreatmentPlanBase(BaseModel):
    objectives: Optional[str]
    probable_sessions: Optional[int]
    procedures: Optional[str]


class TreatmentPlanCreate(TreatmentPlanBase):
    pass


class TreatmentPlan(TreatmentPlanBase):
    plan_id: int
    patient_id: int

    class Config:
        from_attributes = True


# Schemas para Professional (Profissionais)
class ProfessionalBase(BaseModel):
    full_name: Optional[str]
    position: Optional[Position]
    registration_number: Optional[str]


class ProfessionalCreate(ProfessionalBase):
    full_name: str
    position: Position


class Professional(ProfessionalBase):
    professional_id: int
    evolution_records: List['EvolutionRecords'] = []

    class Config:
        from_attributes = True


# Schemas para EvolutionRecords (Registros de Evolução)
class EvolutionRecordsBase(BaseModel):
    date: Optional[date]
    procedures: Optional[str]
    complications: Optional[str]
    health_status_evolution: Optional[str]
    professional_id: Optional[int]


class EvolutionRecordsCreate(EvolutionRecordsBase):
    pass


class EvolutionRecords(EvolutionRecordsBase):
    record_id: int
    patient_id: int

    class Config:
        from_attributes = True
