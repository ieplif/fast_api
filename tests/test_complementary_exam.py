from http import HTTPStatus

from fast_zero import models
from tests.conftest import ComplementaryExamFactory, PatientFactory


def test_create_complementary_exams(client, token, session):
    patient = PatientFactory()
    session.add(patient)
    session.commit()
    session.refresh(patient)

    response = client.post(
        f'/patients/{patient.patient_id}/complementary_exams/',
        json={'exam_details': 'complementary_exam exam_details'},
        headers={'Authorization': f'Bearer {token}'},
       
    )

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()
    assert data['patient_id'] == patient.patient_id
    assert data['exam_details'] == 'complementary_exam exam_details'


def test_list_complementary_exams_should_return_5_complementary_exams(session, client, token):
    expected_complementary_exams = 5
    patient = PatientFactory()
    session.add(patient)
    session.commit()
    session.refresh(patient)

    session.bulk_save_objects(ComplementaryExamFactory.create_batch(5, patient_id=patient.patient_id))
    session.commit()

    response = client.get(
        f'/patients/{patient.patient_id}/complementary_exams/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK

    response_data = response.json()
    assert len(response_data) == expected_complementary_exams


def test_delete_complementary_exam(session, client, token):
    complementary_exam = ComplementaryExamFactory()
    session.add(complementary_exam)
    session.commit()
    session.refresh(complementary_exam)

    response = client.delete(
        f'/complementary_exams/{complementary_exam.comp_exam_id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK

    deteted_complementary_exam = session.query(models.ComplementaryExams).filter(models.ComplementaryExams.comp_exam_id == complementary_exam.comp_exam_id).first()
    assert deteted_complementary_exam is None


def test_delete_complementary_exam_error(client, token):
    response = client.delete(
        f'/complementary_exama/{10}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Not Found'}


def test_patch_complementary_exam(session, client, token):
    complementary_exam = ComplementaryExamFactory()
    session.add(complementary_exam)
    session.commit()
    session.refresh(complementary_exam)

    response = client.patch(
        f'/complementary_exams/{complementary_exam.comp_exam_id}',
        json={'exam_details': 'complementary_exam exam_details'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['exam_details'] == 'complementary_exam exam_details'


def test_patch_complementary_exam_error(client, token):
    response = client.patch(
        '/complementary_exams/10',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Complementary Exams not found.'}
