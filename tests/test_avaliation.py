from http import HTTPStatus

from tests import conftest


def test_create_avaliation(client, token, session):
    patient = conftest.PatientFactory()
    session.add(patient)
    session.commit()
    session.refresh(patient)

    professional = conftest.ProfessionalFactory()
    session.add(professional)
    session.commit()
    session.refresh(professional)

    clinical_history = conftest.ClinicalHistoryFactory(patient_id=patient.patient_id)
    session.add(clinical_history)
    session.commit()
    session.refresh(clinical_history)

    clinical_examination = conftest.ClinicalExaminationFactory(patient_id=patient.patient_id)
    session.add(clinical_examination)
    session.commit()
    session.refresh(clinical_examination)

    physiotherapy_diagnosis = conftest.PhysiotherapyDiagnosisFactory(patient_id=patient.patient_id)
    session.add(physiotherapy_diagnosis)
    session.commit()
    session.refresh(physiotherapy_diagnosis)

    prognosis = conftest.PrognosisFactory(patient_id=patient.patient_id)
    session.add(prognosis)
    session.commit()
    session.refresh(prognosis)

    treatment_plan = conftest.TreatmentPlanFactory(patient_id=patient.patient_id)
    session.add(treatment_plan)
    session.commit()
    session.refresh(treatment_plan)

    response = client.post(
        f'/patients/{patient.patient_id}/avaliation/',
        json={
            'professional_id': professional.professional_id,
            'clinical_history_id': clinical_history.history_id,
            'clinical_examination_id': clinical_examination.exam_id,
            'physiotherapy_diagnosis_id': physiotherapy_diagnosis.diagnosis_id,
            'prognosis_id': prognosis.prognosis_id,
            'treatment_plan_id': treatment_plan.plan_id,
        },
        headers={'Authorization': f'Bearer {token}'},
    )
    print(response.json())
    assert response.status_code == HTTPStatus.CREATED

    data = response.json()
    assert data['professional_id'] == professional.professional_id
    assert data['patient_id'] == patient.patient_id
    assert data['clinical_history_id'] == clinical_history.history_id
    assert data['clinical_examination_id'] == clinical_examination.exam_id
    assert data['physiotherapy_diagnosis_id'] == physiotherapy_diagnosis.diagnosis_id
    assert data['prognosis_id'] == prognosis.prognosis_id
    assert data['treatment_plan_id'] == treatment_plan.plan_id
