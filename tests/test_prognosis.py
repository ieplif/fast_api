from http import HTTPStatus

from fast_zero import models
from tests.conftest import PatientFactory, PrognosisFactory


def test_create_prognosis(client, token, session):
    patient = PatientFactory()
    session.add(patient)
    session.commit()
    session.refresh(patient)

    response = client.post(
        f'/patients/{patient.patient_id}/prognosis/',
        json={'prognosis_details': 'prognosis prognosis_details'},
        headers={'Authorization': f'Bearer {token}'},     
    )

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()
    assert data['patient_id'] == patient.patient_id
    assert data['prognosis_details'] == 'prognosis prognosis_details'


def test_list_prognosis_should_return_5_prognosis(session, client, token):
    expected_prognosis = 5
    patient = PatientFactory()
    session.add(patient)
    session.commit()
    session.refresh(patient)

    session.bulk_save_objects(PrognosisFactory.create_batch(5, patient_id=patient.patient_id))
    session.commit()

    response = client.get(
        f'/patients/{patient.patient_id}/prognosis/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK

    response_data = response.json()
    assert len(response_data) == expected_prognosis


def test_delete_prognosis(session, client, token):
    prognosis = PrognosisFactory()
    session.add(prognosis)
    session.commit()
    session.refresh(prognosis)

    response = client.delete(
        f'/prognosis/{prognosis.prognosis_id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    deleted_prognosis = session.query(models.Prognosis).get(prognosis.prognosis_id)
    assert deleted_prognosis is None


def test_delete_prognosis_error(client, token):
    response = client.delete(
        f'/prognosis/{10}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Prognosis not found.'}


def test_patch_prognosis(session, client, token):
    prognosis = PrognosisFactory()
    session.add(prognosis)
    session.commit()
    session.refresh(prognosis)

    response = client.patch(
        f'/prognosis/{prognosis.prognosis_id}',
        json={'prognosis_details': 'prognosis prognosis_details'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['prognosis_details'] == 'prognosis prognosis_details'


def test_patch_prognosis_error(client, token):
    response = client.patch(
        '/prognosis/10',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Prognosis not found.'}
