# this API library contains methods for all main API-requests of Vite App: http://34.141.58.52:8080/

import json
import requests


class Pets:

    def __init__(self):
        self.base_url = "http://34.141.58.52:8000/"

    def register_user(self, registration_data) -> json:
        """runs POST/register API request that
        - creates a new user
        - and returns dictionary with 3 fields: "token", "email" and "id" of the user created
        this method runs such method with the username and password provided
        :return: status code of response + ID of the user created"""
        response = requests.post(self.base_url + 'register',
                                 data=json.dumps(registration_data))  # by the last expression we
        # specify body of response and convert registration data into json file
        status = response.status_code
        response_body = response.json()  # by that we parse json file of response into Python object to use later
        user_id = response_body.get('id')  # by that we choose the value of the field "id"
        print(
            f"After running registration request the user ID received is: {user_id}, and the status code of the response is: {status}")
        return status, user_id

    def login_user(self, login_data) -> json:
        """runs POST/login API request that
        - login the user
        - and returns dictionary with 3 fields: "token", "email" and "id" of the user logged in
        :return: status code + token
        """
        response = requests.post(self.base_url + "login", data=json.dumps(login_data))
        status = response.status_code
        response_body = response.json()
        token_received = response_body.get("token")
        user_id = response_body.get("id")
        print(
            f"After running login request the user ID received is: {user_id}, the status code of the response is: {status}, and the token received is: {token_received}")
        return status, token_received, user_id

    def get_user_id(self, token) -> json:
        """runs GET/users API request that
        - returns user ID from which the request was made (OR returns dictionary with details in case of error)
        - ! requires authorization (login) to be run successfully
        :return: status code of response + int of user ID
        """
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(self.base_url + "users", headers=headers)
        user_id_received = response.json()
        status = response.status_code
        print(
            f"After running request to get user ID the response is: {user_id_received}, and the status code is: {status}")
        return status, user_id_received

    def delete_user(self, user_id, token) -> json:
        """runs DELETE/users/{id} API request that
        - delete the user with the ID provided
        - and returns empty array (OR dictionary with "detail" field in case of error)
        - ! requires authorization (login) to be run successfully
        this method runs such response
        :return: status code of response + empty array (from response)"""
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(self.base_url + f"users/{user_id}", headers=headers)
        status = response.status_code
        response_body = response.json()
        print(f"After running delete request for the user with ID: {user_id} the status code of response is: {status}")
        return status, response_body

    def create_pet(self, pet_data, token) -> json:
        """runs POST/pet API request that
        - creates a new pet
        - have 2 required fields in the body: "name" of the Pet and "type" of the pet (should be "cat", "dog", "hamster", "reptile" or "parrot")"
        - and could also have 8 other (optional) fields like ???"id", "age", "gender", ???"owner_id", "pic", ???"owner_name", ???"likes_count", ???"liked_by_user")
        - ! requires authorization (login) to be run successfully
        - returns dictionary with "id" field that contains int of pet ID created (if request run successfully)
        :return: status code of response + ID of the pet created
        """
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(self.base_url + "pet", data=json.dumps(pet_data), headers=headers)
        status = response.status_code
        response_body = response.json()
        pet_id_received = response_body.get("id")
        print(
            f"After running Pet creation process the ID of it received is: {pet_id_received}, and the status code is: {status}")
        return status, pet_id_received

    def add_pet_photo(self, pet_id, pet_image_filename, token) -> json:
        """runs POST/pet/{id}/image request that
        - adds photo to some Pet specified by ID
        - returns status code 200 and link to the photo uploaded (in case of success)
        - ! requires authorization (login) to be run successfully
        - ! requires ID of the Pet in the path of request
        - ! requires the filename of pet image to upload (the image should be stored in the "tests\\photo" directory in the project)
        :return: status code of response + link to the image uploaded
        """
        image = {'pic': ('any_file_name.jpg', open(f'tests/photo/{pet_image_filename}', 'rb'), 'image/jpeg')}
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(self.base_url + f"pet/{pet_id}/image", files=image, headers=headers)
        status = response.status_code
        link_received = response.json()['link']
        print(f"After uploading pet image with ID {pet_id} the link received is: {link_received}, and status code is: {status}")
        return status, link_received

    def delete_pet(self, pet_id, token) -> json:
        """runs DELETE/pet/{id} API request that
        - delete a PET specified by ID provided
        - returns an empty dictionary with response code 200 if run successfully
        - ! requires authorization (login) to be run successfully
        - ! requires ID of the Pet in the path
        :return: status code of response + body of response with empty dictionary (in case of success)
        """
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(self.base_url + f"pet/{pet_id}", headers=headers)
        status = response.status_code
        response_body = response.json()
        print(f"After deleting the Pet specified by ID: {pet_id}, the body of response is: {response_body}, and the status code is: {status}")
        return status, response_body

    def get_pet_info(self, pet_id, token) -> json:
        """runs GET/pet/{id} API request that
        - returns dictionary with info of specific pet
        - ??? requires authorization (login) to be run successfully
        - requires pet ID in path of request
        - returns dictionary with 2 key-value pairs ("pet" key has a value in form of dictionary, that includes fields "id", "name", "type", "age", "gender", "owner_id", "pic", "owner_name", "likes_count" and "liked_by_user";
        and "comments" key with a value in form of array (array will be empty in case of no comments)
        :return: status code of response + Pet ID + Pet name + Pet type + owner ID + (Pet age + Pet gender + Pet picture - THESE VALUES COULD BE NULL, because optional) + array of comments to Pet (empty, if no comments exist)
        """
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(self.base_url + f"pet/{pet_id}", headers=headers)
        status = response.status_code
        pet_info = response.json()["pet"]
        pet_id = pet_info["id"]
        pet_name = pet_info["name"]
        pet_type = pet_info["type"]
        pet_age = pet_info["age"]
        pet_gender = pet_info["gender"]
        pet_owner_id = pet_info["owner_id"]
        pet_picture = pet_info["pic"]
        pet_owner_name = pet_info["owner_name"]  # should be an email
        pet_likes_count = pet_info["likes_count"]
        pet_liked_by_user = pet_info["liked_by_user"]
        pet_comments = response.json()["comments"]
        print(
            f"After requesting info about the Pet with ID: {pet_id}, the general info received is: {pet_info}, the comments to the Pet are: {pet_comments} and the status code of response is: {status}")
        return status, pet_id, pet_name, pet_type, pet_age, pet_gender, pet_owner_id, pet_picture, pet_owner_name, pet_likes_count, pet_liked_by_user, pet_comments

    def add_pet_like(self, pet_id, token) -> json:
        """runs PUT/pet/{id}/like API request that
        - adds one like to some PET
        - ! requires authorization (login) to be run successfully
        - ! requires ID of the Pet in the path
        - returns null as body of response (if request run successfully) - OR returns dictionary with error details
        :return: status code of response + None (as an indicator if run successfully) ///
        """
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.put(self.base_url + f"pet/{pet_id}/like", headers=headers)
        status = response.status_code
        indicator = response.json()
        print(f"After running the request to add like to the pet with ID: {pet_id} the status code of response is: {status}, and the indicator from the response is: {indicator}")
        return status, indicator
