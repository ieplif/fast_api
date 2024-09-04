from http import HTTPStatus

from fast_zero import models
from tests.conftest import PatientFactory, PhysiotherapyDiagnosisFactory


def test_create_physiotherapy_diagnosis(client, token, session):
    patient = PatientFactory()
    session.add(patient)
    session.commit()
    session.refresh(patient)

    response = client.post(
        f'/patients/{patient.patient_id}/physiotherapy_diagnosis/',
        json={'diagnosis_details': 'physiotherapy_diagnosis diagnosis_details'},
        headers={'Authorization': f'Bearer {token}'},   
    )

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()
    assert data['patient_id'] == patient.patient_id
    assert data['diagnosis_details'] == 'physiotherapy_diagnosis diagnosis_details'


def test_list_physiotherapy_diagnosis_should_return_5_physiotherapy_diagnosis(session, client, token):
    expected_physiotherapy_diagnosis = 5
    patient = PatientFactory()
    session.add(patient)
    session.commit()
    session.refresh(patient)

    session.bulk_save_objects(PhysiotherapyDiagnosisFactory.create_batch(5, patient_id=patient.patient_id))
    session.commit()

    response = client.get(
          f'/patients/{patient.patient_id}/physiotherapy_diagnosis/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK

    response_data = response.json()
    assert len(response_data) == expected_physiotherapy_diagnosis



def test_delete_physiotherapy_diagnosis(session, client, token):
    physiotherapy_diagnosis = PhysiotherapyDiagnosisFactory()
    session.add(physiotherapy_diagnosis)
    session.commit()
    session.refresh(physiotherapy_diagnosis)

    response = client.delete(
        f'/physiotherapy_diagnosis/{physiotherapy_diagnosis.diagnosis_id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK

    deleted_physiotherapy_diagnosis = session.query(models.PhysiotherapyDiagnosis).get(physiotherapy_diagnosis.diagnosis_id)
    assert deleted_physiotherapy_diagnosis is None


def test_delete_physiotherapy_diagnosis_error(client, token):
    response = client.delete(
        f'/physiotherapy-diagnosis/{10}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Not Found'}


def test_patch_physiotherapy_diagnosis(session, client, token):
    physiotherapy_diagnosis = PhysiotherapyDiagnosisFactory()
    session.add(physiotherapy_diagnosis)
    session.commit()
    session.refresh(physiotherapy_diagnosis)

    response = client.patch(
        f'/physiotherapy_diagnosis/{physiotherapy_diagnosis.diagnosis_id}',
        json={'diagnosis_details': 'physiotherapy_diagnosis diagnosis_details'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['diagnosis_details'] == 'physiotherapy_diagnosis diagnosis_details'


def test_patch_physiotherapy_diagnosis_error(client, token):
    response = client.patch(
        '/physiotherapy_diagnosis/10',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Physiotherapy Diagnosis not found.'}
