from http import HTTPStatus

from tests.conftest import PatientFactory, ProfessionalFactory


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
