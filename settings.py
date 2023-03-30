#  values used in tests
# written in UpperCase as constants

class TestData:

    VALID_EMAIL = ""
    VALID_PASSWORD = ""

    REGISTRATION_DATA = [{"email": "test.email@gmail.com",
                          "password": "testpassword",
                          "confirm_password": "testpassword"}]

    LOGIN_DATA = [{"email": "test.email@gmail.com",
                   "password": "testpassword"}]

    PET_DATA = [{"name": "Baster", "type": "dog",
                 "age": 7, "gender": "male"}]

    PET_IMAGE_PATH = ['dog_photo.jpeg']

    # ADDITIONAL THOUGHTS
    # maybe it is worth to add some "storage" to automatically collect all user/pet ID
    # that were not deleted, as it was supposed by code, after running tests?
    # - but not sure about a specific solution

    # what about replacing BASE_URL here from the Pets-class?
    # in case the URL can be changed for some reason as other Test data
