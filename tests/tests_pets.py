from settings import TestData
import pytest

# all test data (like new user accounts, new Pet-cards created) is deleted automatically after executing each test
# (otherwise the message about the problem with deletion will be shown)


class TestPet:

    @pytest.mark.parametrize("registration_data", TestData.REGISTRATION_DATA)
    @pytest.mark.parametrize("login_data", TestData.LOGIN_DATA)
    def test_register_user(self, create_pet_object, registration_data,
                           login_data):  # by the fixtures in parameters we create a pet-object
        # to do requests using it later
        pets = create_pet_object
        register_request = pets.register_user(registration_data)  # request result
        expected_status = 200
        actual_status = register_request[0]
        user_id_created = register_request[1]
        assert actual_status == expected_status, f"Wrong result (expected status code: {expected_status}', actual: {actual_status})"
        assert user_id_created > 0, "Wrong result (the ID of the user should not be zero)"
        #  then, after executing the test itself, we delete the user created -
        #  to get rid of data created during test execution
        login_request = pets.login_user(login_data)
        token_received = login_request[1]
        delete_request = pets.delete_user(user_id_created, token_received)
        delete_status = delete_request[0]
        assert delete_status == 200, f"Wrong result of the teardown after executing test (the user with ID {user_id_created} was not deleted)"

    #
    @pytest.mark.parametrize("login_data", TestData.LOGIN_DATA)
    def test_login_user(self, create_pet_object, register_login_delete_user, login_data):
        print(f"PRINT: {login_data}")
        pets = create_pet_object
        login_request = pets.login_user(login_data)
        expected_status = 200
        actual_status = login_request[0]
        assert actual_status == expected_status, f"Wrong result (expected status code: {expected_status}', actual: {actual_status})"
        token_received = login_request[1]
        assert token_received is not None, "Wrong result (the token received should not be null)"

    #
    def test_get_user_id(self, create_pet_object, register_login_delete_user):
        #  token = self.pets.login_user(TestData.LOGIN_DATA)[1]  # gets token required to run do the request
        pets = create_pet_object
        token, user_id_created = register_login_delete_user
        response = pets.get_user_id(token)
        expected_status = 200
        actual_status = response[0]
        id_received = response[1]
        assert actual_status == expected_status, f"Wrong result (expected status code: {expected_status}', actual: {actual_status})"
        assert id_received == user_id_created, f"Wrong result (expected user ID: {expected_status}, actual: {id_received})"

    #
    @pytest.mark.parametrize("registration_data", TestData.REGISTRATION_DATA)
    @pytest.mark.parametrize("login_data", TestData.LOGIN_DATA)
    def test_delete_user(self, create_pet_object, registration_data, login_data):
        pets = create_pet_object
        register_request = pets.register_user(registration_data)
        user_id_created = register_request[1]
        login_request = pets.login_user(login_data)
        token_received = login_request[1]
        delete_request = pets.delete_user(user_id_created, token_received)
        expected_status = 200
        actual_status = delete_request[0]
        response_body = delete_request[1]
        assert actual_status == expected_status, f"Wrong result (expected status code: {expected_status}', actual: {actual_status})"
        assert len(
            response_body) == 0, f"Wrong result (expected: to return an empty dictionary, actual result: {response_body})"

    #
    @pytest.mark.parametrize("pet_data", TestData.PET_DATA)
    def test_create_pet(self, create_pet_object, register_login_delete_user, pet_data):
        pets = create_pet_object
        token = register_login_delete_user[0]
        create_request = pets.create_pet(pet_data, token)
        actual_status = create_request[0]
        pet_id_created = create_request[1]
        status_expected = 200
        assert actual_status == status_expected, f"Wrong result (expected status code: {status_expected}', actual: {actual_status})"
        assert pet_id_created is not None, "Wrong result (the ID of the pet created should not be zero)"
        #  there is no code to delete the pet after executing test,
        #  because it's done automatically after deleting the user who created it

    def test_add_pet_like(self, create_pet_object, register_login_delete_user, create_delete_pet):
        pets = create_pet_object
        token = register_login_delete_user[0]
        pet_id = create_delete_pet
        like_request = pets.add_pet_like(pet_id, token)
        expected_status = 200
        actual_status = like_request[0]
        indicator = like_request[1]  # should be None if the request was run successfully
        assert actual_status == expected_status, f"Wrong result (expected status code: {expected_status}', actual: {actual_status})"
        assert indicator is None, f"Wrong result (expected to receive: \"None\" value in response body as the " \
                                  f"indicator of success, actual: {indicator}"
        # maybe it's also worth to run get_pet_info-request to check the number of likes recorded?

    @pytest.mark.parametrize("image_filename", TestData.PET_IMAGE_PATH)
    def test_add_pet_photo(self, create_pet_object, register_login_delete_user, create_delete_pet, image_filename):
        pets = create_pet_object
        token = register_login_delete_user[0]
        pet_id = create_delete_pet
        add_response = pets.add_pet_photo(pet_id, image_filename, token)
        expected_status = 200
        actual_status = add_response[0]
        photo_link_received = add_response[1]
        assert actual_status == expected_status, f"Wrong result (expected status code: {expected_status}', actual: {actual_status})"
        link_should_starts_with = "https://www.googleapis.com/download/storage"
        assert photo_link_received.startswith(link_should_starts_with), f"Wrong result (expected to receive a link " \
                                                                        f"that starts with: {link_should_starts_with}, actual: {photo_link_received}"
        #  or instead of the last statement it's better just to check that photo_link_received is not None or len()!=0 ?

    # in this test the Pet is created, 1 like and 1 photo added to it -
    # and then we compare if the get_pet_info-request returns all this info correctly
    @pytest.mark.parametrize("pet_data", TestData.PET_DATA)  # this data will be used to compare with the response
    @pytest.mark.parametrize("image_filename", TestData.PET_IMAGE_PATH)
    def test_get_pet_info(self, create_pet_object, register_login_delete_user, create_delete_pet, pet_data,
                          image_filename):
        pets = create_pet_object
        token = register_login_delete_user[0]
        pet_id = create_delete_pet
        owner_id = register_login_delete_user[1]
        pets.add_pet_like(pet_id, token)
        pets.add_pet_photo(pet_id, image_filename, token)
        info_response = pets.get_pet_info(pet_id, token)
        expected_status = 200
        actual_status = info_response[0]
        assert actual_status == expected_status, f"Wrong result (expected status code: {expected_status}', actual: {actual_status})"
        pet_id_received = info_response[1]
        assert pet_id_received == pet_id, f"Wrong result (expected pet ID: {pet_id}, received: {pet_id_received})"
        pet_name_received = info_response[2]
        assert pet_name_received == pet_data["name"]
        pet_type_received = info_response[3]
        assert pet_type_received == pet_data["type"]
        pet_age_received = info_response[4]
        assert pet_age_received == pet_data["age"]
        pet_gender_received = info_response[5]
        assert pet_gender_received == pet_data["gender"]
        pet_owner_id_received = info_response[6]
        assert pet_owner_id_received == owner_id
        pet_picture_received = info_response[7]
        assert pet_picture_received is not None
        #  assertion of the owner_name is skipped - because its ID was already checked
        expected_likes_count = 1
        pet_likes_count_rec = info_response[9]
        assert pet_likes_count_rec == expected_likes_count
        # assertion of the pet_liked_by_user, pet_comments are skipped for now

    @pytest.mark.parametrize("pet_data", TestData.PET_DATA)
    def test_delete_pet(self, create_pet_object, register_login_delete_user, pet_data):
        pets = create_pet_object
        token = register_login_delete_user[0]
        create_request = pets.create_pet(pet_data, token)
        pet_id = create_request[1]
        delete_response = pets.delete_pet(pet_id, token)
        expected_status = 200
        actual_status = delete_response[0]
        assert actual_status == expected_status, f"Wrong result (expected status code: {expected_status}', actual: {actual_status})"
        response_body = delete_response[1]
        assert len(
            response_body) == 0, f"Wrong result (expected: to return an empty dictionary, actual result: {response_body})"
