from http import HTTPStatus

from tests.conftest import PatientFactory


def test_create_patient(client, token):
    response = client.post(
        '/patients',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'full_name': 'Maria Aparecida',
            'age': 58,
            'place_of_birth': 'Rio de Janeiro-RJ',
            'marital_status': 'Casada',
            'gender': 'Feminino',
            'profession': 'Professora',
            'residential_address': 'Rua X, 345, Centro - Rio de Janeiro - RJ',
            'commercial_address': 'Rua Y, 600, Barra da Tijuca - Rio de Janeiro - RJ',
        },
    )
    assert response.json() == {
        'patient_id': 1,
        'full_name': 'Maria Aparecida',
        'age': 58,
        'place_of_birth': 'Rio de Janeiro-RJ',
        'marital_status': 'Casada',
        'gender': 'Feminino',
        'profession': 'Professora',
        'residential_address': 'Rua X, 345, Centro - Rio de Janeiro - RJ',
        'commercial_address': 'Rua Y, 600, Barra da Tijuca - Rio de Janeiro - RJ',
        'clinical_history': [],
        'clinical_examination': [],
        'complementary_exams': [],
        'physiotherapy_diagnosis': [],
        'prognosis': [],
        'treatment_plan': [],
        'evolution_records': [],
    }


def test_list_patients_filter_full_name_should_return_5_patients(session, client, token):
    expected_patients = 5
    session.bulk_save_objects(PatientFactory.create_batch(5, full_name='Maria Aparecida'))
    session.commit()

    response = client.get(
        '/patients/?full_name=Maria Aparecida',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Captura o JSON da resposta
    response_data = response.json()

    # Verifica se a resposta é uma lista e o número de pacientes
    assert isinstance(response_data, list)
    assert len(response_data) == expected_patients


def test_list_patients_filter_age_should_return_5_patients(session, client, token):
    expected_patients = 5
    session.bulk_save_objects(PatientFactory.create_batch(5, age=58))
    session.commit()

    response = client.get(
        '/patients/?age=58',
        headers={'Authorization': f'Bearer {token}'},
    )

    response_data = response.json()

    assert isinstance(response_data, list)
    assert len(response_data) == expected_patients


def test_delete_patient(session, client, token):
    patient = PatientFactory()
    session.add(patient)
    session.commit()
    session.refresh(patient)

    response = client.delete(f'/patients/{patient.patient_id}', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Task has been deleted successfully.'}


def test_delete_patient_error(client, token):
    response = client.delete(f'/patients/{10}', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Patient not found.'}


def test_patch_patient(session, client, token):
    patient = PatientFactory()
    session.add(patient)
    session.commit()
    session.refresh(patient)

    response = client.patch(
        f'/patients/{patient.patient_id}',
        json={
            'full_name': 'Maria Aparecida',
            'age': patient.age,
            'place_of_birth': patient.place_of_birth,
            'marital_status': patient.marital_status,
            'gender': patient.gender,
            'profession': patient.profession,
            'residential_address': patient.residential_address,
            'commercial_address': patient.commercial_address,
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    updated_patient = response.json()
    assert updated_patient['full_name'] == 'Maria Aparecida'


def test_patch_patient_error(client, token):
    response = client.patch(
        '/patients/10',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Patient not found.'}
