import pytest
import flask
from flask_socketio import SocketIO
from app import app
class Tests:
    
    def test_client(self):
        res = app.test_client().post('/capture')
        assert res.status_code == 200
        assert res.json["message"] == "Image captured and saved"

    # def test_update_route(self):
    #     testreq = {'count':'5'}
    #     res = app.test_client().post('/update', json=testreq)
    #     print(res)
    #     assert res.count == 5
    #     assert res.status_code == 200