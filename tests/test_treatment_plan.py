from http import HTTPStatus

from fast_zero import models
from tests.conftest import PatientFactory, TreatmentPlanFactory

PROBABLE_SESSIONS = 10


def test_create_treatment_plan(client, token, session):
    patient = PatientFactory()
    session.add(patient)
    session.commit()
    session.refresh(patient)

    response = client.post(
        f'/patients/{patient.patient_id}/treatment_plan/',
        json={
            'objectives': 'treatment_plan.objectives',
            'probable_sessions': 10,
            'procedures': 'treatment_plan.procedures',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()
    assert data['patient_id'] == patient.patient_id
    assert data['objectives'] == 'treatment_plan.objectives'
    assert data['probable_sessions'] == PROBABLE_SESSIONS
    assert data['procedures'] == 'treatment_plan.procedures'


def test_list_treatment_plans_should_return_5_treatment_plans(session, client, token):
    expected_treatment_plans = 5
    patient = PatientFactory()
    session.add(patient)
    session.commit()
    session.refresh(patient)

    session.bulk_save_objects(TreatmentPlanFactory.create_batch(5, patient_id=patient.patient_id))
    session.commit()

    response = client.get(
        f'/patients/{patient.patient_id}/treatment_plan/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK

    response_data = response.json()
    assert len(response_data) == expected_treatment_plans


def test_delete_treatment_plan(session, client, token):
    treatment_plan = TreatmentPlanFactory()
    session.add(treatment_plan)
    session.commit()
    session.refresh(treatment_plan)

    response = client.delete(
        f'/treatment_plan/{treatment_plan.plan_id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    deleted_treatment_plan = session.query(models.TreatmentPlan).get(treatment_plan.plan_id)
    assert deleted_treatment_plan is None


def test_delete_treatment_plan_error(client, token):
    response = client.delete(f'/treatment-plan/{10}', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Not Found'}


def test_patch_treatment_plan(session, client, token):
    treatment_plan = TreatmentPlanFactory()
    session.add(treatment_plan)
    session.commit()
    session.refresh(treatment_plan)

    response = client.patch(
        f'/treatment_plan/{treatment_plan.plan_id}',
        json={
            'objectives': 'treatment_plan.objectives',
            'probable_sessions': 10,
            'procedures': 'treatment_plan.procedures',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['objectives'] == 'treatment_plan.objectives'
    assert data['probable_sessions'] == PROBABLE_SESSIONS
    assert data['procedures'] == 'treatment_plan.procedures'


def test_patch_treatment_plan_error(client, token):
    response = client.patch(
        '/treatment_plan/10',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Treatment Plan not found.'}
