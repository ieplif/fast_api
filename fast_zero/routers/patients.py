from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from fast_zero import crud, schemas
from fast_zero.database import get_session

router = APIRouter()

T_Session = Annotated[Session, Depends(get_session)]


# Routes for Patients
@router.post('/patients/', response_model=schemas.Patient, tags=['patients'])
def create_patient(patient: schemas.PatientCreate, db: T_Session):
    return crud.create_patient(db=db, patient=patient)


@router.get('/patients/{patient_id}', response_model=schemas.Patient, tags=['patients'])
def read_patient(patient_id: int, db: T_Session):
    db_patient = crud.get_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Patient not found')
    return db_patient


@router.get('/patients/', response_model=list[schemas.Patient], tags=['patients'])
def read_patients(db: T_Session, skip: int = 0, limit: int = 10):
    patients = crud.get_patients(db, skip=skip, limit=limit)
    return patients


@router.patch('/patients/{patient_id}', response_model=schemas.Patient, tags=['patients'])
def update_patient(patient_id: int, patient: schemas.PatientUpdate, db: T_Session):
    db_patient = crud.update_patient(db=db, patient_id=patient_id, patient=patient)
    if db_patient is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Patient not found.')
    update_data = patient.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_patient, key, value)

    db.commit()
    return db_patient


@router.delete('/patients/{patient_id}', response_model=schemas.Message, tags=['patients'])
def delete_patient(patient_id: int, db: T_Session):
    db_patient = crud.delete_patient(db=db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Patient not found.')
    return {'message': 'Task has been deleted successfully.'}


# Routes for Clinical History
@router.post('/patients/{patient_id}/clinical_history/', response_model=schemas.ClinicalHistory, status_code=201, tags=['clinical_history'])
def create_clinical_history_for_patient(patient_id: int, clinical_history: schemas.ClinicalHistoryCreate, db: T_Session):
    return crud.create_clinical_history(db=db, clinical_history=clinical_history, patient_id=patient_id)


@router.get('/patients/{patient_id}/clinical_history/', response_model=list[schemas.ClinicalHistory], tags=['clinical_history'])
def read_clinical_history_for_patient(db: T_Session, patient_id: int, skip: int = 0, limit: int = 10):
    return crud.get_clinical_histories(db=db, patient_id=patient_id, skip=skip, limit=limit)


@router.patch('/clinical_history/{history_id}', response_model=schemas.ClinicalHistory, tags=['clinical_history'])
def update_clinical_history(history_id: int, clinical_history: schemas.ClinicalHistoryUpdate, db: T_Session):
    db_clinical_history = crud.update_clinical_history(db=db, history_id=history_id, updated_data=clinical_history)
    if db_clinical_history is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Clinical History not found.')
    return db_clinical_history


@router.delete('/clinical_history/{history_id}', response_model=schemas.Message, tags=['clinical_history'])
def delete_clinical_history(history_id: int, db: T_Session):
    db_clinical_history = crud.delete_clinical_history(db=db, history_id=history_id)
    if db_clinical_history is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Clinical History not found.')
    return {'message': 'Clinical history has been deleted successfully.'}


# Routes for Clinical Examination
@router.post('/patients/{patient_id}/clinical_examination/', response_model=schemas.ClinicalExamination, status_code=201, tags=['clinical_examination'])
def create_clinical_examination_for_patient(patient_id: int, clinical_examination: schemas.ClinicalExaminationCreate, db: T_Session):
    return crud.create_clinical_examination(db=db, clinical_examination=clinical_examination, patient_id=patient_id)


@router.get('/patients/{patient_id}/clinical_examination/', response_model=list[schemas.ClinicalExamination], tags=['clinical_examination'])
def read_clinical_examination_for_patient(db: T_Session, patient_id: int, skip: int = 0, limit: int = 10):
    return crud.get_clinical_examinations(db=db, patient_id=patient_id, skip=skip, limit=limit)


@router.patch('/clinical_examination/{exam_id}', response_model=schemas.ClinicalExamination, tags=['clinical_examination'])
def update_clinical_examination(exam_id: int, clinical_examination: schemas.ClinicalExaminationUpdate, db: T_Session):
    db_clinical_examination = crud.update_clinical_examination(db=db, exam_id=exam_id, update_data=clinical_examination)
    if db_clinical_examination is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Clinical Examination not found')
    return db_clinical_examination


@router.delete('/clinical_examination/{exam_id}', response_model=schemas.Message, tags=['clinical_examination'])
def delete_clinical_examination(exam_id: int, db: T_Session):
    db_clinical_examination = crud.delete_clinical_examination(db=db, exam_id=exam_id)
    if db_clinical_examination is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Clinical Examination not found.')
    return {'message': 'Clinical examination has been deleted successfully.'}


# Routes for Complementary Exams
@router.post('/patients/{patient_id}/complementary_exams/', response_model=schemas.ComplementaryExams, status_code=201, tags=['complementary_exams'])
def create_complementary_exams_for_patient(patient_id: int, complementary_exam: schemas.ComplementaryExamsCreate, db: T_Session):
    return crud.create_complementary_exams(db=db, complementary_exam=complementary_exam, patient_id=patient_id)


@router.get('/patients/{patient_id}/complementary_exams/', response_model=list[schemas.ComplementaryExams], tags=['complementary_exams'])
def read_complementary_exams_for_patient(db: T_Session, patient_id: int, skip: int = 0, limit: int = 10):
    return crud.get_complementary_exams(db=db, patient_id=patient_id, skip=skip, limit=limit)


@router.patch('/complementary_exams/{comp_exam_id}', response_model=schemas.ComplementaryExams, tags=['complementary_exams'])
def update_complementary_exam(comp_exam_id: int, complementary_exams: schemas.ComplementaryExamsUpdate, db: T_Session):
    db_complementary_exams = crud.update_complementary_exam(db=db, comp_exam_id=comp_exam_id, update_data=complementary_exams)
    if db_complementary_exams is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Complementary Exams not found.')
    return db_complementary_exams


@router.delete('/complementary_exams/{comp_exam_id}', response_model=schemas.Message, tags=['complementary_exams'])
def delete_complementary_exam(comp_exam_id: int, db: T_Session):
    db_complementary_exams = crud.delete_complementary_exam(db=db, comp_exam_id=comp_exam_id)
    if db_complementary_exams is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Complementary Exams not found.')
    return {'message': 'Complementary exams has been deleted successfully.'}


# Routes for Physiotherapy Diagnosis
@router.post('/patients/{patient_id}/physiotherapy_diagnosis/', response_model=schemas.PhysiotherapyDiagnosis, status_code=201, tags=['physiotherapy_diagnosis'])
def create_physiotherapy_diagnosis_for_patient(patient_id: int, physiotherapy_diagnosis: schemas.PhysiotherapyDiagnosisCreate, db: T_Session):
    return crud.create_physiotherapy_diagnosis(db=db, physiotherapy_diagnosis=physiotherapy_diagnosis, patient_id=patient_id)


@router.get('/patients/{patient_id}/physiotherapy_diagnosis/', response_model=list[schemas.PhysiotherapyDiagnosis], tags=['physiotherapy_diagnosis'])
def read_physiotherapy_diagnosis_for_patient(db: T_Session, patient_id: int, skip: int = 0, limit: int = 10):
    return crud.get_physiotherapy_diagnoses(db=db, patient_id=patient_id, skip=skip, limit=limit)


@router.patch('/physiotherapy_diagnosis/{diagnosis_id}', response_model=schemas.PhysiotherapyDiagnosis, tags=['physiotherapy_diagnosis'])
def update_physiotherapy_diagnosis(diagnosis_id: int, physiotherapy_diagnosis: schemas.PhysiotherapyDiagnosisUpdate, db: T_Session):
    db_physiotherapy_diagnosis = crud.update_physiotherapy_diagnosis(db=db, diagnosis_id=diagnosis_id, update_data=physiotherapy_diagnosis)
    if db_physiotherapy_diagnosis is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Physiotherapy Diagnosis not found.')
    return db_physiotherapy_diagnosis


@router.delete('/physiotherapy_diagnosis/{diagnosis_id}', response_model=schemas.Message, tags=['physiotherapy_diagnosis'])
def delete_physiotherapy_diagnosis(diagnosis_id: int, db: T_Session):
    db_physiotherapy_diagnosis = crud.delete_physiotherapy_diagnosis(db=db, diagnosis_id=diagnosis_id)
    if db_physiotherapy_diagnosis is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Physiotherapy Diagnosis not found')
    return {'message': 'Physiotherapy diagnosis has been deleted successfully.'}


# Routes for Prognosis
@router.post('/patients/{patient_id}/prognosis/', response_model=schemas.Prognosis, status_code=201, tags=['prognosis'])
def create_prognosis_for_patient(patient_id: int, prognosis: schemas.PrognosisCreate, db: T_Session):
    return crud.create_prognosis(db=db, prognosis=prognosis, patient_id=patient_id)


@router.get('/patients/{patient_id}/prognosis/', response_model=list[schemas.Prognosis], tags=['prognosis'])
def read_prognosis_for_patient(db: T_Session, patient_id: int, skip: int = 0, limit: int = 10):
    return crud.get_prognoses(db=db, patient_id=patient_id, skip=skip, limit=limit)


@router.patch('/prognosis/{prognosis_id}', response_model=schemas.Prognosis, tags=['prognosis'])
def update_prognosis(prognosis_id: int, prognosis: schemas.PrognosisUpdate, db: T_Session):
    db_prognosis = crud.update_prognosis(db=db, prognosis_id=prognosis_id, update_data=prognosis)
    if db_prognosis is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Prognosis not found.')
    return db_prognosis


@router.delete('/prognosis/{prognosis_id}', response_model=schemas.Message, tags=['prognosis'])
def delete_prognosis(prognosis_id: int, db: T_Session):
    db_prognosis = crud.delete_prognosis(db=db, prognosis_id=prognosis_id)
    if db_prognosis is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Prognosis not found.')
    return {'message': 'Prognosis has been deleted successfully.'}


# Routes for Treatment Plan
@router.post('/patients/{patient_id}/treatment_plan/', response_model=schemas.TreatmentPlan, status_code=201, tags=['treatment_plan'])
def create_treatment_plan_for_patient(patient_id: int, treatment_plan: schemas.TreatmentPlanCreate, db: T_Session):
    return crud.create_treatment_plan(db=db, treatment_plan=treatment_plan, patient_id=patient_id)


@router.get('/patients/{patient_id}/treatment_plan/', response_model=list[schemas.TreatmentPlan], tags=['treatment_plan'])
def read_treatment_plan_for_patient(db: T_Session, patient_id: int, skip: int = 0, limit: int = 10):
    return crud.get_treatment_plans(db=db, patient_id=patient_id, skip=skip, limit=limit)


@router.patch('/treatment_plan/{plan_id}', response_model=schemas.TreatmentPlan, tags=['treatment_plan'])
def update_treatment_plan(plan_id: int, treatment_plan: schemas.TreatmentPlanUpdate, db: T_Session):
    db_treatment_plan = crud.update_treatment_plan(db=db, plan_id=plan_id, update_data=treatment_plan)
    if db_treatment_plan is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Treatment Plan not found.')
    return db_treatment_plan


@router.delete('/treatment_plan/{plan_id}', response_model=schemas.Message, tags=['treatment_plan'])
def delete_treatment_plan(plan_id: int, db: T_Session):
    db_treatment_plan = crud.delete_treatment_plan(db=db, plan_id=plan_id)
    if db_treatment_plan is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Treatment Plan not found.')
    return {'message': 'Treatment plan has been deleted successfully.'}


# Routes for Professional
@router.post('/professionals/', response_model=schemas.Professional, tags=['professionals'])
def create_professional(professional: schemas.ProfessionalCreate, db: T_Session):
    return crud.create_professional(db=db, professional=professional)


@router.get('/professionals/{professional_id}', response_model=schemas.Professional, tags=['professionals'])
def read_professional(professional_id: int, db: T_Session):
    db_professional = crud.get_professional(db, professional_id=professional_id)
    if db_professional is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Professional not found')
    return db_professional


@router.get('/professionals/', response_model=list[schemas.Professional], tags=['professionals'])
def read_professionals(db: T_Session, skip: int = 0, limit: int = 10):
    professionals = crud.get_professionals(db, skip=skip, limit=limit)
    return professionals


@router.patch('/professionals/{professional_id}', response_model=schemas.Professional, tags=['professionals'])
def update_professional(professional_id: int, professional: schemas.ProfessionalUpdate, db: T_Session):
    db_professional = crud.update_professional(db=db, professional_id=professional_id, professional=professional)
    if db_professional is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Professional not found.')
    update_data = professional.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_professional, key, value)

    db.commit()
    return db_professional


@router.delete('/professionals/{professional_id}', response_model=schemas.Message, tags=['professionals'])
def delete_professional(professional_id: int, db: T_Session):
    db_professional = crud.delete_professional(db=db, professional_id=professional_id)
    if db_professional is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Professional not found.')
    return {'message': 'Professional has been deleted successfully.'}


# Routes for Evolution Record
@router.post('/patients/{patient_id}/evolution_records/', response_model=schemas.EvolutionRecords, tags=['evolution_records'])
def create_evolution_records_for_patient(patient_id: int, evolution_records: schemas.EvolutionRecordsCreate, db: T_Session):
    return crud.create_evolution_record(db=db, evolution_record=evolution_records, patient_id=patient_id)


@router.get('/patients/{patient_id}/evolution_records/', response_model=list[schemas.EvolutionRecords], tags=['evolution_records'])
def read_evolution_records_for_patient(db: T_Session, patient_id: int, skip: int = 0, limit: int = 10):
    return crud.get_evolution_record(db=db, patient_id=patient_id, skip=skip, limit=limit)


@router.put('/evolution_records/{record_id}', response_model=schemas.EvolutionRecords, tags=['evolution_records'])
def update_evolution_records(record_id: int, evolution_records: schemas.EvolutionRecordsCreate, db: T_Session):
    db_evolution_records = crud.update_evolution_record(db=db, record_id=record_id, evolution_records=evolution_records)
    if db_evolution_records is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Evolution Record not found')
    return db_evolution_records


@router.delete('/evolution_records/{record_id}', response_model=schemas.EvolutionRecords, tags=['evolution_records'])
def delete_evolution_records(record_id: int, db: T_Session):
    db_evolution_records = crud.delete_evolution_record(db=db, record_id=record_id)
    if db_evolution_records is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Evolution Record not found')
    return db_evolution_records
