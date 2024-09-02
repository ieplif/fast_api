from http import HTTPStatus

from tests.conftest import ClinicalHistoryFactory, PatientFactory
from fast_zero import models

def test_create_clinical_history(client, token, session):
    # Cria um paciente usando a factory
    patient = PatientFactory()
    session.add(patient)
    session.commit()
    session.refresh(patient)

    # Faz a requisição para criar o histórico clínico
    response = client.post(
        f'/patients/{patient.patient_id}/clinical_history/',
        json={
            'main_complaint': 'clinical_history.main_complaint,',
            'disease_history': 'clinical_history disease_history,',
            'lifestyle_habits': 'clinical_history lifestyle_habits',
            'previous_treatments': 'clinical_history previous_treatments',
            'personal_family_history': 'clinical_history personal_family_history',
            'other_information': 'clinical_history other_information',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    
    assert response.status_code == HTTPStatus.CREATED 

    
    response_data = response.json()
    assert response_data['patient_id'] == patient.patient_id
    assert response_data['main_complaint'] == 'clinical_history.main_complaint,'
    assert response_data['disease_history'] == 'clinical_history disease_history,'
    assert response_data['lifestyle_habits'] == 'clinical_history lifestyle_habits'
    assert response_data['previous_treatments'] == 'clinical_history previous_treatments'
    assert response_data['personal_family_history'] == 'clinical_history personal_family_history'
    assert response_data['other_information'] == 'clinical_history other_information'


def test_list_clinical_history_should_return_5_clinical_history(session, client, token):
    expected_clinical_histories = 5
    patient = PatientFactory()
    session.add(patient)
    session.commit()
    session.refresh(patient)
    
    session.bulk_save_objects(
        ClinicalHistoryFactory.create_batch(5, patient_id=patient.patient_id)
    )
    session.commit()

    response = client.get(
        f'/patients/{patient.patient_id}/clinical_history/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK 

    response_data = response.json()
    assert len(response_data) == expected_clinical_histories


def test_list_clinical_history_for_patient_should_return_5_clinical_history(session, client, token):
    patient = PatientFactory()
    session.add(patient)
    session.commit()
    session.refresh(patient)

    session.bulk_save_objects(
        ClinicalHistoryFactory.create_batch(5, patient_id=patient.patient_id)
    )
    session.commit()

    response = client.get(
        f'/patients/{patient.patient_id}/clinical_history/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK 

    response_data = response.json()
    assert len(response_data) == 5


def test_delete_clinical_history(session, client, token):
    # Cria um histórico clínico usando a factory
    clinical_history = ClinicalHistoryFactory()
    session.add(clinical_history)
    session.commit()
    session.refresh(clinical_history)

    # Faz a requisição para deletar o histórico clínico
    response = client.delete(
        f'/clinical_history/{clinical_history.history_id}',  # Corrigido para corresponder à rota
        headers={'Authorization': f'Bearer {token}'}
    )

    # Verifica o status da resposta
    assert response.status_code == HTTPStatus.OK  # Verifica se o status é 200 OK

    # Verifica se o histórico clínico foi realmente deletado
    deleted_history = session.query(models.ClinicalHistory).filter(models.ClinicalHistory.history_id == clinical_history.history_id).first()
    assert deleted_history is None


def test_delete_clinical_history_error(client, token):
    response = client.delete(
        f'/clinical_history/{10}', 
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Clinical History not found.'}


def test_patch_clinical_history(session, client, token):
    clinical_history = ClinicalHistoryFactory()
    session.add(clinical_history)
    session.commit()
    session.refresh(clinical_history)

    response = client.patch(
        f'/clinical_history/{clinical_history.history_id}',
        json={'main_complaint': 'Dor pélvica'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['main_complaint'] == 'Dor pélvica'

"""
def test_patch_clinic_history_error(client, token):
    response = client.patch(
        '/clinical-history/10',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Clinical History not found.'}
"""