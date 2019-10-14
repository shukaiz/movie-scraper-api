import os
import flask
import unittest
import tempfile
from graph import *


class APITestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flask.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.config['TESTING'] = True
        self.app = flask.app.test_client()
        flask.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flask.app.config['DATABASE'])


if __name__ == '__main__':
    unittest.main()
