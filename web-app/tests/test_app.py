import pytest
from app import app
class Tests:
    
    def test_client(self):
        res = app.test_client().get('/')
        response = res.data.decode('utf-8')
        print(response)
        assert res.status_code == 200
        assert res

    # def test_update_route(self):
    #     testreq = {'count':'5'}
    #     res = app.test_client().post('/update', json=testreq)
    #     print(res)
    #     assert res.count == 5
    #     assert res.status_code == 200