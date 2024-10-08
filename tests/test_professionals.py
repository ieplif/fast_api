from http import HTTPStatus

from tests.conftest import ProfessionalFactory


def test_create_professional(client, token):
    response = client.post(
        '/professionals/',
        json={
            'full_name': 'fullname',
            'position': 'physiotherapist',
            'registration_number': 'registration_number',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.json() == {
        'professional_id': 1,
        'full_name': 'fullname',
        'position': 'physiotherapist',
        'registration_number': 'registration_number',
        'evolution_records': [],
    }


def test_list_professionals_filter_full_name_should_return_5_professionals(session, client, token):
    expected_professionals = 5

    session.bulk_save_objects(ProfessionalFactory.create_batch(5, full_name='fullname'))
    session.commit()

    response = client.get(
        '/professionals/?full_name=fullname',
        headers={'Authorization': f'Bearer {token}'},
    )

    response_data = response.json()

    assert isinstance(response_data, list)
    assert len(response_data) == expected_professionals


def test_list_professionals_filter_position_should_return_5_professionals(session, client, token):
    expected_professionals = 5

    session.bulk_save_objects(ProfessionalFactory.create_batch(5, position='physiotherapist'))
    session.commit()

    response = client.get(
        '/professionals/?position=physiotherapist',
        headers={'Authorization': f'Bearer {token}'},
    )

    response_data = response.json()

    assert isinstance(response_data, list)
    assert len(response_data) == expected_professionals


def test_list_professionals_filter_registration_number_should_return_5_professionals(session, client, token):
    expected_professionals = 5

    session.bulk_save_objects(ProfessionalFactory.create_batch(5, registration_number='registration_number'))
    session.commit()

    response = client.get(
        '/professionals/?registration_number=registration_number',
        headers={'Authorization': f'Bearer {token}'},
    )

    response_data = response.json()

    assert isinstance(response_data, list)
    assert len(response_data) == expected_professionals


def test_delete_professional(session, client, token):
    professional = ProfessionalFactory()
    session.add(professional)
    session.commit()
    session.refresh(professional)

    response = client.delete(
        f'/professionals/{professional.professional_id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Professional has been deleted successfully.'}


def test_delete_professional_error(client, token):
    response = client.delete(f'/professionals/{10}', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Professional not found.'}


def test_patch_professional(session, client, token):
    professional = ProfessionalFactory()
    session.add(professional)
    session.commit()
    session.refresh(professional)

    response = client.patch(
        f'/professionals/{professional.professional_id}',
        json={
            'full_name': 'fullname',
            'position': 'physiotherapist',
            'registration_number': professional.registration_number,
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK

    update_professional = response.json()
    assert update_professional['full_name'] == 'fullname'
    assert update_professional['position'] == 'physiotherapist'


def test_patch_professional_error(client, token):
    response = client.patch(
        '/professionals/10',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Professional not found.'}
