from datetime import date
from http import HTTPStatus

from fast_zero.models import EvolutionRecords
from tests.conftest import EvolutionRecordsFactory, PatientFactory, ProfessionalFactory


def test_create_evolution_records(client, token, session):
    patient = PatientFactory()
    session.add(patient)
    session.commit()
    session.refresh(patient)

    professional = ProfessionalFactory()
    session.add(professional)
    session.commit()
    session.refresh(professional)

    response = client.post(
        f'/patients/{patient.patient_id}/evolution_records/?professional_id={professional.professional_id}',
        json={
            'date': '2021-01-01',
            'procedures': 'procedures',
            'complications': 'complications',
            'health_status_evolution': 'health_status_evolution',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()
    assert data['patient_id'] == patient.patient_id
    assert data['professional_id'] == professional.professional_id
    assert data['date'] == '2021-01-01'
    assert data['procedures'] == 'procedures'
    assert data['complications'] == 'complications'
    assert data['health_status_evolution'] == 'health_status_evolution'


def test_list_evolution_records_should_return_5_evolution_records(session, client, token):
    expected_evolution_records = 5
    patient = PatientFactory()
    session.add(patient)
    session.commit()
    session.refresh(patient)

    professional = ProfessionalFactory()
    session.add(professional)
    session.commit()
    session.refresh(professional)

    session.bulk_save_objects(EvolutionRecordsFactory.create_batch(5, patient_id=patient.patient_id, professional_id=professional.professional_id))
    session.commit()

    response = client.get(
        f'/patients/{patient.patient_id}/evolution_records/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK

    response_data = response.json()
    assert len(response_data) == expected_evolution_records


def test_delete_evolution_records(session, client, token):
    evolution_records = EvolutionRecordsFactory()
    session.add(evolution_records)
    session.commit()
    session.refresh(evolution_records)

    response = client.delete(
        f'/evolution_records/{evolution_records.record_id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK

    deleted_evolution_records = session.query(EvolutionRecords).get(evolution_records.record_id)
    assert deleted_evolution_records is None


def test_delete_evolution_records_error(client, token):
    response = client.delete(f'/evolution_records/{10}', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Evolution Record not found'}


def test_update_evolution_records(client, token, session):
    evolution_records = EvolutionRecordsFactory()
    session.add(evolution_records)
    session.commit()
    session.refresh(evolution_records)

    response = client.patch(
        f'/evolution_records/{evolution_records.record_id}',
        json={
            'date': '2021-01-01',
            'procedures': 'procedures',
            'complications': 'complications',
            'health_status_evolution': 'health_status_evolution',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert data['record_id'] == evolution_records.record_id
    assert data['date'] == '2021-01-01'
    assert data['procedures'] == 'procedures'
    assert data['complications'] == 'complications'
    assert data['health_status_evolution'] == 'health_status_evolution'


def test_update_evolution_records_error(client, token):
    response = client.patch(
        '/evolution_records/9999',
        json={'date': date.today().isoformat(), 'procedures': 'Example procedures', 'complications': 'Example complications', 'health_status_evolution': 'Example evolution'},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Evolution Record not found'}
