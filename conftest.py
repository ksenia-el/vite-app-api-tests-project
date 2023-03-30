#  file to collect all fixtures

import pytest
from settings import TestData
from api import Pets


#  fixture that creates a Pets-object (with the library of all API-methods to run available)
@pytest.fixture()
def create_pet_object():
    pets = Pets()
    yield pets


# fixture that creates a Pet-object (with the library of all API-methods to run available),
# then register a new user, log in
# AFTER YIELD it deletes the user created
@pytest.fixture()
def register_login_delete_user(create_pet_object):
    pets = create_pet_object
    reg_response = pets.register_user(TestData.REGISTRATION_DATA[0])
    user_id_created = reg_response[1]
    #  just to keep track of created and then deleted user IDs
    print(f"Fixture: The user was created with ID: {user_id_created}")
    login_response = pets.login_user(TestData.LOGIN_DATA[0])
    token = login_response[1]
    yield token, user_id_created
    delete_result = pets.delete_user(user_id_created, token)
    delete_status = delete_result[0]
    if delete_status == 200:
        print(f"Fixture: The user with ID {user_id_created} was deleted")
    else:
        print(f"Fixture: The user with ID {user_id_created} was NOT deleted!!!")


# fixture that creates a Pet-object (with the library of all API-methods to run available),
# then register a new user, log in
# creates a new pet
# AFTER YIELD it deletes the pet created
# and then deletes the user created
@pytest.fixture()
def create_delete_pet(create_pet_object, register_login_delete_user):
    pets = create_pet_object
    token = register_login_delete_user[0]
    create_request = pets.create_pet(TestData.PET_DATA[0], token)
    pet_id_created = create_request[1]
    print(f"Fixture: The Pet was created with ID: {pet_id_created}")
    yield pet_id_created
    delete_result = pets.delete_pet(pet_id_created, token)
    delete_status = delete_result[0]
    if delete_status == 200:
        print(f"Fixture: The Pet with ID {pet_id_created} was deleted")
    else:
        print(f"Fixture: The Pet with ID {pet_id_created} was NOT deleted!!!")
