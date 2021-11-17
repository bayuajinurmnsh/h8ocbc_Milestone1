import unittest
import app
import json

from directors import read_all as directors_read
from movies import read_all as movies_read


class TestDirectorsCreate(unittest.TestCase):
    """
    this class is used to test all case in create function in directors.py
    """

    # set up the connection to the apps
    def setUp(self):
        app.connex_app.app.testing = True
        self.app = app.connex_app.app.test_client()

    # test create data (if post success)
    def test_create_director(self):

        directors = {
            'name': 'unit test',
            'gender': 2,
            'department': 'Unit Test',
            'uid': 100
        }

        result = self.app.post(
            '/api/directors', data=json.dumps(directors), content_type='application/json')
        self.assertEqual(result.status_code, 201,
                         "it should give response 201")

    # test create data (if user dont send invalid json data)
    def test_create_invalid_json(self):
        """
        function create in directors.py has been set to only accept variable department, gender, name, and uid
        if one or all of them are missing, function create should send a response with code 406
        """

        directors = {
            'name': 'unit test',        # valid
            'gender': 2,                # valid
            'department': 'Unit Test',  # valid
            # 'uid': 2                  this is the valid data
            'uuid': 2                   # this is invalid data, user should send uid, not uuid
        }

        result = self.app.post(
            '/api/directors', data=json.dumps(directors), content_type='application/json')
        self.assertEqual(result.status_code, 406,
                         'it should give response 406')

    # test create data (if user dont send invalid json data)
    def test_create_less_json_data(self):
        """
        function create in directors.py has been set to only accept variable with total is 4 variable  [department, gender, name, and uid]
        if user send data less than 4, function create should send a response with code 406
        """
        directors = {
            'name': 'unit test',        # valid
            'gender': 2,                # valid
            'department': 'Unit Test',  # valid
        }

        result = self.app.post(
            '/api/directors', data=json.dumps(directors), content_type='application/json')
        self.assertEqual(result.status_code, 406,
                         'it should give response 406')

    # test create data (if user dont send invalid json data)
    def test_create_more_json_data(self):
        """
        function create in directors.py has been set to only accept variable with total is 4 variable  [department, gender, name, and uid]
        if user send data more than 4, function create should send a response with code 406
        """
        directors = {
            'name': 'unit test',        # valid
            'gender': 2,                # valid
            'department': 'Unit Test',  # valid
            'uid': 2,                   # valid

            'extra_variable': "this should give response 406"  # invalid
        }

        result = self.app.post(
            '/api/directors', data=json.dumps(directors), content_type='application/json')
        self.assertEqual(result.status_code, 406,
                         'it should give response 406')


class TestDirectorsRead(unittest.TestCase):

    """
    this class is used to test all case in read function in directors.py
    the function to test is :
        -read_all()
        -read_one()
        -get_director_by_name()
        -get_each_revenue_from_movie()
    """

    def setUp(self):
        app.connex_app.app.testing = True
        self.app = app.connex_app.app.test_client()

    # check if funcion read all return responses 200
    def test_response_read_all(self):
        result = self.app.get('/api/directors')
        self.assertEqual(result.status_code, 200,
                         "it should return http code : 200")

    # function read_all must return a list data type
    def test_read_all(self):
        self.assertIs(type(directors_read()), list, "it should list")

    # check if funcion read one return responses 200
    def test_response_read_one(self):
        result = self.app.get('api/directors/1')
        self.assertEqual(result.status_code, 200,
                         "it should return http code : 200")

    # function read_one must return a list data type
    def test_read_one(self):
        self.assertIs(type(directors_read()), list, "it should list")

    # check if funcion get_director_by_name return responses 200
    def test_response_get_director_by_name(self):
        result = self.app.get('api/directors/get_by_name/nolan')
        self.assertEqual(result.status_code, 200,
                         "it should return http code : 200")

    # function get_director_by_name must return a list data type
    def test_get_director_by_name(self):
        self.assertIs(type(directors_read()), list, "it should list")

    # check if funcion get_director_by_name return responses 200
    def test_response_get_each_revenue_from_movie(self):
        result = self.app.get('api/directors/get_total_networth/1')
        self.assertEqual(result.status_code, 200,
                         "it should return http code : 200")

    # function get_director_by_name must return a list data type
    def test_get_each_revenue_from_movie(self):
        self.assertIs(type(directors_read()), list, "it should list")


class TestMovies(unittest.TestCase):

    def setUp(self):
        app.connex_app.app.testing = True
        self.app = app.connex_app.app.test_client()

    # check if funcion read all return responses 200
    def test_response_read_all(self):
        result = self.app.get('/api/movies')
        self.assertEqual(result.status_code, 200,
                         "it should return http code : 200")

    # function read_all must return a list data type
    def test_read_all(self):
        self.assertIs(type(movies_read()), list, "it should list")


if __name__ == '__main__':
    unittest.main()
