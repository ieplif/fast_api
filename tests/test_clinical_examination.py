from http import HTTPStatus

from fast_zero import models
from tests.conftest import ClinicalExaminationFactory, PatientFactory


def test_create_clinical_examination(client, token, session):
    patient = PatientFactory()
    session.add(patient)
    session.commit()
    session.refresh(patient)

    response = client.post(
        f'/patients/{patient.patient_id}/clinical_examination/',
        json={'exam_details': 'clinical_examination exam_details'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()
    assert data['patient_id'] == patient.patient_id
    assert data['exam_details'] == 'clinical_examination exam_details'


def test_list_clinical_examinations_should_return_5_clinical_examinations(session, client, token):
    expected_clinical_examinations = 5
    patient = PatientFactory()
    session.add(patient)
    session.commit()
    session.refresh(patient)

    session.bulk_save_objects(ClinicalExaminationFactory.create_batch(5, patient_id=patient.patient_id))
    session.commit()

    response = client.get(
        f'/patients/{patient.patient_id}/clinical_examination/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK

    response_data = response.json()
    assert len(response_data) == expected_clinical_examinations


def test_delete_clinical_examination(session, client, token):
    clinical_examination = ClinicalExaminationFactory()
    session.add(clinical_examination)
    session.commit()
    session.refresh(clinical_examination)

    response = client.delete(
        f'/clinical_examination/{clinical_examination.exam_id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK

    deleted_clinical_examination = session.query(models.ClinicalExamination).filter(models.ClinicalExamination.exam_id == clinical_examination.exam_id).first()
    assert deleted_clinical_examination is None


def test_delete_clinical_examination_error(client, token):
    response = client.delete(
        f'/clinical_examination/{10}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Clinical Examination not found.'}


def test_patch_clinical_examination(session, client, token):
    clinical_examination = ClinicalExaminationFactory()
    session.add(clinical_examination)
    session.commit()
    session.refresh(clinical_examination)

    response = client.patch(
        f'/clinical_examination/{clinical_examination.exam_id}',
        json={'exam_details': 'exam_details'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['exam_details'] == 'exam_details'


def test_patch_clinical_examination_error(client, token):
    response = client.patch(
        '/clinical_examination/10',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Clinical Examination not found'}
