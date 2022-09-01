import unittest
from urllib import response
import pytest

import json
from simplejson import loads

# from yaml import load
from tests.base import BaseTestCase
from utils.orcl_utils import OracleAccess
from configs.tbl_consts import TBL_USER_ACCOUNT


def login_user(self):
    return self.client.post(
        '/api/account/login',
        data=json.dumps(dict(
            username='tami',
            passwd='tami'
        )),
        content_type='application/json'
    )


class TestAuthBlueprint(BaseTestCase):
    def test_registration(self):
        ''' Test for user registration '''
        with self.client:
            response = login_user(self)
            data = json.loads(response.data)
            self.assertTrue(data['result'] == 0)
            self.assertTrue(data['data'] == '登入成功')
            self.assertTrue(data['test'] == '123')
            self.assertEqual(response.status_code, 200)


@pytest.fixture
def client():
    app = BaseTestCase.create_app({'TESTING': True})
    with app.test_client() as client:
        yield client


def test_forget(client, mocker):#忘記密碼
    account_exist = True

    def _query(sql):
        nonlocal account_exist
        if not account_exist:
            return [[]]
        else:
            return [['itri@kuohwa.com']]

    def _excute(sql, *args, **kwargs):
        nonlocal account_exist
        if TBL_USER_ACCOUNT in sql:
            account_exist == False
            return [['itri@kuohwa.com']]

    mocker.patch.object(OracleAccess, 'query', _query)
    mocker.patch.object(OracleAccess, 'execute', _excute)

    response = client.post(
        '/api/account/forget',
        data=json.dumps({
            'username': 'itri@kuohwa.com'
        }),
        content_type='application/json'
    )
    a=json.loads(response.data)
    assert a['result'] == 0

 
def test_get_account_list(client, mocker):#獲取帳戶列表
    is_exist = False

    def _query(sql):
        nonlocal is_exist
        if is_exist:
            return [['ta', 'admin', 'itri@kuohwa.com', '', '2021/03/14']]
        else:
            is_exist = True
            return []
            
    mocker.patch.object(OracleAccess, 'query', _query)

    response = client.post(
        '/api/account/get_account_list'
    )
    data = json.loads(response.data)
    assert data['result'] == 1
    assert data['message'] == 'No Account'
    assert response.status_code == 200
    assert data['data'] == []
    assert is_exist == True

    response = client.post(
        '/api/account/get_account_list'
    )
    data = json.loads(response.data)
    assert data['result'] == 0
    assert data['message'] == ''
    assert response.status_code == 200
    assert data['data'] == [{
        'user_id': 'ta',
        'role': ['admin'],
        'email': 'itri@kuohwa.com',
        'update_time': '2021/03/14'
    }]
    assert is_exist == True


def test_add_account_list(client, mocker):#新增帳號
    is_exist = False

    def _query(sql):
        nonlocal is_exist
        if not is_exist:
            return []
        else:
            return [['tami', 'super_user', 'test@gmail.com']]

    def _execute(sql, *args, **kwargs):
        nonlocal is_exist
        if TBL_USER_ACCOUNT in sql:
            is_exist = True
            return []

    mocker.patch.object(OracleAccess, 'query', _query)
    mocker.patch.object(OracleAccess, 'execute', _execute)

    response = client.post(
        '/api/account/add_account_list',
        data=json.dumps({
            'user_id': 'tami',
            'role': 'super_user',
            'email': 'test@gmail.com'
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert data['result'] == 0
    assert data['message'] == ''
    assert response.status_code == 200
    assert is_exist == True

    response = client.post(
        '/api/account/add_account_list',
        data=json.dumps({
            'user_id': 'tami',
            'role': 'super_user',
            'email': 'test@gmail.com'
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert data['result'] == 1
    assert data['message'] == 'add fail. Account is already exist'
    assert response.status_code == 200
    assert is_exist == True



def test_delete_account_list(client, mocker):#刪除帳號
    is_exist = True

    def _query(sql):
        nonlocal is_exist
        if not is_exist:
            return []
        else:
            return [['tami', 'aa,bb', 'test@gmail.com', '', '2021/12/1 08:00:00']]

    def _execute(sql, *args, **kwargs):
        nonlocal is_exist
        if TBL_USER_ACCOUNT in sql:
            is_exist = False
            return None

    mocker.patch.object(OracleAccess, 'query', _query)
    mocker.patch.object(OracleAccess, 'execute', _execute)

    response = client.post(
        '/api/account/delete_account_list',
        data=json.dumps({
            'user_id': 'tami'
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert data['result'] == 0
    assert data['message'] == ''
    assert response.status_code == 200
    assert is_exist == False

    response = client.post(
        '/api/account/delete_account_list',
        data=json.dumps({
            'user_id': '1'
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert data['result'] == 1
    assert data['message'] == 'account not exist'
    assert response.status_code == 200
    assert is_exist == False


def test_update_account_list(client, mocker):#更新帳號
    is_exist = True

    def _query(sql):
        nonlocal is_exist
        if not is_exist:
            return []
        else:
            return [['tami', 'aa,bb', 'test@gmail.com', '', '2021/12/1 08:00:00']]

    def _execute(sql, *args, **kwargs):
        nonlocal is_exist
        if TBL_USER_ACCOUNT in sql:
            is_exist = False
            return None

    mocker.patch.object(OracleAccess, 'query', _query)
    mocker.patch.object(OracleAccess, 'execute', _execute)

    response = client.post(
        '/api/account/update_account_list',
        data=json.dumps({
            'old_user_id': '1',
            'data': {
                'new_user_id': '2',
                'new_role': ['admin', 'super_user'],
                'new_email': 'test@gmail.com'
            }
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert data['result'] == 0
    assert data['message'] == ''
    assert response.status_code == 200
    assert is_exist == False

    response = client.post(
        '/api/account/update_account_list',
        data=json.dumps({
            'old_user_id': '1',
            'data': {
                'new_user_id': '2',
                'new_role': ['admin', 'super_user'],
                'new_email': 'test@gmail.com'
            }
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert data['result'] == 1
    assert data['message'] == 'account not exist'
    assert response.status_code == 200
    assert is_exist == False


def test_update_account_status(client, mocker):#更新帳號狀態
    is_exist = True

    def _query(sql):
        nonlocal is_exist
        if not is_exist:
            return []
        else:
            return [['1', 'aa,bb', 'test@gmail.com', '', '2021/12/1 08:00:00']]

    def _execute(sql, *args, **kwargs):
        nonlocal is_exist
        if TBL_USER_ACCOUNT in sql:
            is_exist = False
            return None

    mocker.patch.object(OracleAccess, 'query', _query)
    mocker.patch.object(OracleAccess, 'execute', _execute)

    response = client.post(
        '/api/account/update_account_status',
        data=json.dumps({
            'old_user_id': '1',
            'is_activated': "true"
            }
        ),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert data['result'] == 0
    assert data['message'] == ''
    assert response.status_code == 200
    assert is_exist == False

    response = client.post(
        '/api/account/update_account_status',
        data=json.dumps({
            'old_user_id': '12',
            'is_activated':"true"
            }
        ),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert data['result'] == 1
    assert data['message'] == 'account not exist'
    assert response.status_code == 200
    assert is_exist == False


