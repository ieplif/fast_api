from sqlalchemy.orm import Session

from fast_zero import models, schemas


# Funções CRUD para Pacientes
def get_patient(db: Session, patient_id: int):
    return db.query(models.Patient).filter(models.Patient.patient_id == patient_id).first()


def get_patients(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Patient).offset(skip).limit(limit).all()


def create_patient(db: Session, patient: schemas.PatientCreate):
    db_patient = models.Patient(**patient.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def update_patient(db: Session, patient_id: int, patient: schemas.PatientCreate):
    db_patient = get_patient(db, patient_id)
    if not db_patient:
        return None
    for key, value in patient.model_dump().items():
        setattr(db_patient, key, value)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def delete_patient(db: Session, patient_id: int):
    db_patient = get_patient(db, patient_id)
    if db_patient:
        db.delete(db_patient)
        db.commit()
    return db_patient


# Funções CRUD para ClinicalHistory
def get_clinical_history(db: Session, history_id: int):
    return db.query(models.ClinicalHistory).filter(models.ClinicalHistory.history_id == history_id).first()


def get_clinical_histories(db: Session, patient_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.ClinicalHistory).filter(models.ClinicalHistory.patient_id == patient_id).offset(skip).limit(limit).all()


def create_clinical_history(db: Session, clinical_history: schemas.ClinicalHistoryCreate, patient_id: int):
    db_clinical_history = models.ClinicalHistory(**clinical_history.model_dump(), patient_id=patient_id)
    db.add(db_clinical_history)
    db.commit()
    db.refresh(db_clinical_history)
    return db_clinical_history


def update_clinical_history(db: Session, history_id: int, updated_data: schemas.ClinicalHistoryUpdate):
    db_clinical_history = db.query(models.ClinicalHistory).filter(models.ClinicalHistory.history_id == history_id).first()
    if db_clinical_history is None:
        return None

    update_data = updated_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_clinical_history, key, value)
    
    db.commit()
    db.refresh(db_clinical_history)
    return db_clinical_history


def delete_clinical_history(db: Session, history_id: int):
    db_clinical_history = get_clinical_history(db, history_id)
    if db_clinical_history:
        db.delete(db_clinical_history)
        db.commit()
    return db_clinical_history


# Funções CRUD para ClinicalExamination
def get_clinical_examination(db: Session, exam_id: int):
    return db.query(models.ClinicalExamination).filter(models.ClinicalExamination.exam_id == exam_id).first()


def get_clinical_examinations(db: Session, patient_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.ClinicalExamination).filter(models.ClinicalExamination.patient_id == patient_id).offset(skip).limit(limit).all()


def create_clinical_examination(db: Session, clinical_examination: schemas.ClinicalExaminationCreate, patient_id: int):
    db_clinical_examination = models.ClinicalExamination(**clinical_examination.model_dump(), patient_id=patient_id)
    db.add(db_clinical_examination)
    db.commit()
    db.refresh(db_clinical_examination)
    return db_clinical_examination


def update_clinical_examination(db: Session, exam_id: int, clinical_examination: schemas.ClinicalExaminationCreate):
    db_clinical_examination = get_clinical_examination(db, exam_id)
    if not db_clinical_examination:
        return None
    for key, value in clinical_examination.model_dump().items():
        setattr(db_clinical_examination, key, value)
    db.commit()
    db.refresh(db_clinical_examination)
    return db_clinical_examination


def delete_clinical_examination(db: Session, exam_id: int):
    db_clinical_examination = get_clinical_examination(db, exam_id)
    if db_clinical_examination:
        db.delete(db_clinical_examination)
        db.commit()
    return db_clinical_examination


# Funções CRUD para ComplementaryExams
def get_complementary_exam(db: Session, comp_exam_id: int):
    return db.query(models.ComplementaryExams).filter(models.ComplementaryExams.comp_exam_id == comp_exam_id).first()


def get_complementary_exams(db: Session, patient_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.ComplementaryExams).filter(models.ComplementaryExams.patient_id == patient_id).offset(skip).limit(limit).all()


def create_complementary_exam(db: Session, complementary_exam: schemas.ComplementaryExamsCreate, patient_id: int):
    db_complementary_exam = models.ComplementaryExams(**complementary_exam.model_dump(), patient_id=patient_id)
    db.add(db_complementary_exam)
    db.commit()
    db.refresh(db_complementary_exam)
    return db_complementary_exam


def update_complementary_exam(db: Session, comp_exam_id: int, complementary_exam: schemas.ComplementaryExamsCreate):
    db_complementary_exam = get_complementary_exam(db, comp_exam_id)
    if not db_complementary_exam:
        return None
    for key, value in complementary_exam.model_dump().items():
        setattr(db_complementary_exam, key, value)
    db.commit()
    db.refresh(db_complementary_exam)
    return db_complementary_exam


def delete_complementary_exam(db: Session, comp_exam_id: int):
    db_complementary_exam = get_complementary_exam(db, comp_exam_id)
    if db_complementary_exam:
        db.delete(db_complementary_exam)
        db.commit()
    return db_complementary_exam


# Funções CRUD para PhysiotherapyDiagnosis
def get_physiotherapy_diagnosis(db: Session, diagnosis_id: int):
    return db.query(models.PhysiotherapyDiagnosis).filter(models.PhysiotherapyDiagnosis.diagnosis_id == diagnosis_id).first()


def get_physiotherapy_diagnoses(db: Session, patient_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.PhysiotherapyDiagnosis).filter(models.PhysiotherapyDiagnosis.patient_id == patient_id).offset(skip).limit(limit).all()


def create_physiotherapy_diagnosis(db: Session, physiotherapy_diagnosis: schemas.PhysiotherapyDiagnosisCreate, patient_id: int):
    db_physiotherapy_diagnosis = models.PhysiotherapyDiagnosis(**physiotherapy_diagnosis.model_dump(), patient_id=patient_id)
    db.add(db_physiotherapy_diagnosis)
    db.commit()
    db.refresh(db_physiotherapy_diagnosis)
    return db_physiotherapy_diagnosis


def update_physiotherapy_diagnosis(db: Session, diagnosis_id: int, physiotherapy_diagnosis: schemas.PhysiotherapyDiagnosisCreate):
    db_physiotherapy_diagnosis = get_physiotherapy_diagnosis(db, diagnosis_id)
    if not db_physiotherapy_diagnosis:
        return None
    for key, value in physiotherapy_diagnosis.model_dump().items():
        setattr(db_physiotherapy_diagnosis, key, value)
    db.commit()
    db.refresh(db_physiotherapy_diagnosis)
    return db_physiotherapy_diagnosis


def delete_physiotherapy_diagnosis(db: Session, diagnosis_id: int):
    db_physiotherapy_diagnosis = get_physiotherapy_diagnosis(db, diagnosis_id)
    if db_physiotherapy_diagnosis:
        db.delete(db_physiotherapy_diagnosis)
        db.commit()
    return db_physiotherapy_diagnosis


# Funções CRUD para Prognosis
def get_prognosis(db: Session, prognosis_id: int):
    return db.query(models.Prognosis).filter(models.Prognosis.prognosis_id == prognosis_id).first()


def get_prognoses(db: Session, patient_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Prognosis).filter(models.Prognosis.patient_id == patient_id).offset(skip).limit(limit).all()


def create_prognosis(db: Session, prognosis: schemas.PrognosisCreate, patient_id: int):
    db_prognosis = models.Prognosis(**prognosis.model_dump(), patient_id=patient_id)
    db.add(db_prognosis)
    db.commit()
    db.refresh(db_prognosis)
    return db_prognosis


def update_prognosis(db: Session, prognosis_id: int, prognosis: schemas.PrognosisCreate):
    db_prognosis = get_prognosis(db, prognosis_id)
    if not db_prognosis:
        return None
    for key, value in prognosis.model_dump().items():
        setattr(db_prognosis, key, value)
    db.commit()
    db.refresh(db_prognosis)
    return db_prognosis


def delete_prognosis(db: Session, prognosis_id: int):
    db_prognosis = get_prognosis(db, prognosis_id)
    if db_prognosis:
        db.delete(db_prognosis)
        db.commit()
    return db_prognosis


# Funções CRUD para TreatmentPlan
def get_treatment_plan(db: Session, plan_id: int):
    return db.query(models.TreatmentPlan).filter(models.TreatmentPlan.plan_id == plan_id).first()


def get_treatment_plans(db: Session, patient_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.TreatmentPlan).filter(models.TreatmentPlan.patient_id == patient_id).offset(skip).limit(limit).all()


def create_treatment_plan(db: Session, treatment_plan: schemas.TreatmentPlanCreate, patient_id: int):
    db_treatment_plan = models.TreatmentPlan(**treatment_plan.model_dump(), patient_id=patient_id)
    db.add(db_treatment_plan)
    db.commit()
    db.refresh(db_treatment_plan)
    return db_treatment_plan


def update_treatment_plan(db: Session, plan_id: int, treatment_plan: schemas.TreatmentPlanCreate):
    db_treatment_plan = get_treatment_plan(db, plan_id)
    if not db_treatment_plan:
        return None
    for key, value in treatment_plan.model_dump().items():
        setattr(db_treatment_plan, key, value)
    db.commit()
    db.refresh(db_treatment_plan)
    return db_treatment_plan


def delete_treatment_plan(db: Session, plan_id: int):
    db_treatment_plan = get_treatment_plan(db, plan_id)
    if db_treatment_plan:
        db.delete(db_treatment_plan)
        db.commit()
    return db_treatment_plan


# Funções CRUD para Professional
def get_professional(db: Session, professional_id: int):
    return db.query(models.Professional).filter(models.Professional.professional_id == professional_id).first()


def get_professionals(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Professional).offset(skip).limit(limit).all()


def create_professional(db: Session, professional: schemas.ProfessionalCreate):
    db_professional = models.Professional(**professional.model_dump())
    db.add(db_professional)
    db.commit()
    db.refresh(db_professional)
    return db_professional


def update_professional(db: Session, professional_id: int, professional: schemas.ProfessionalCreate):
    db_professional = get_professional(db, professional_id)
    if not db_professional:
        return None
    for key, value in professional.model_dump().items():
        setattr(db_professional, key, value)
    db.commit()
    db.refresh(db_professional)
    return db_professional


def delete_professional(db: Session, professional_id: int):
    db_professional = get_professional(db, professional_id)
    if db_professional:
        db.delete(db_professional)
        db.commit()
    return db_professional


# Funções CRUD para EvolutionRecords
def get_evolution_record(db: Session, record_id: int):
    return db.query(models.EvolutionRecords).filter(models.EvolutionRecords.record_id == record_id).first()


def get_evolution_records(db: Session, patient_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.EvolutionRecords).filter(models.EvolutionRecords.patient_id == patient_id).offset(skip).limit(limit).all()


def create_evolution_record(db: Session, evolution_record: schemas.EvolutionRecordsCreate, patient_id: int, professional_id: int):
    db_evolution_record = models.EvolutionRecords(**evolution_record.model_dump(), patient_id=patient_id, professional_id=professional_id)
    db.add(db_evolution_record)
    db.commit()
    db.refresh(db_evolution_record)
    return db_evolution_record


def update_evolution_record(db: Session, record_id: int, evolution_record: schemas.EvolutionRecordsCreate):
    db_evolution_record = get_evolution_record(db, record_id)
    if not db_evolution_record:
        return None
    for key, value in evolution_record.model_dump().items():
        setattr(db_evolution_record, key, value)
    db.commit()
    db.refresh(db_evolution_record)
    return db_evolution_record


def delete_evolution_record(db: Session, record_id: int):
    db_evolution_record = get_evolution_record(db, record_id)
    if db_evolution_record:
        db.delete(db_evolution_record)
        db.commit()
    return db_evolution_record
