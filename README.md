API testing project for Vite App (http://34.141.58.52:8080)

Tests all main API endpoints: 

- POST/register
- POST/login
- GET/users
- DELETE/users/{id}
- POST/pet
- POST/pet/{id}/image
- GET/pet/{id}
- PUT/pet/{id}/like
- DELETE/pet/{id}

Test data is created before and deleted after every test execution automatically by fixtures. 

The project was created as a part of an educational course by QALearning School.

▶️ To run all tests at once use the command "pytest -v tests/tests_pets.py" in Terminal. 

