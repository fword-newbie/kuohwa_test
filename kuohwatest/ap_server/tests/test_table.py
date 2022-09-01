from werkzeug.datastructures import FileStorage
import unittest
import pytest
import os

import json
from tests.base import BaseTestCase
from utils.orcl_utils import OracleAccess
from configs.tbl_consts import TBL_USER_DETECT_TABLE, TBL_USER_IMAGE_PATH_TABLE, TBL_USER_MAPPING_TABLE


@pytest.fixture
def client():
    app = BaseTestCase.create_app({'TESTING': True})

    with app.test_client() as client:
        yield client


def test_get_detect_table(client, mocker):
    is_exist = False

    def _query(sql):
        nonlocal is_exist
        if not is_exist:
            is_exist = True
            return []
        else:
            return [["s5weqw183cwqe75dd", "99,82", "99,857", "2356,82", "2356,857", "cell_id1", "99,82", "99,857", "2356,82", "2356,857", "0", "2", "0", "3", "example"]]

    mocker.patch.object(OracleAccess, "query", _query)

    response = client.post(
        '/api/table/get_detect_table',
        data=json.dumps({
            "uuid": "s5weqw183cwqe75dd"
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert data['result'] == 1
    assert data['message'] == 'No data'
    assert response.status_code == 200
    assert is_exist == True
    

    response = client.post(
        '/api/table/get_detect_table',
        data=json.dumps({
            "uuid": "s5weqw183cwqe75dd"
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert data['result'] == 0
    assert data['message'] == ''
    assert response.status_code == 200
    assert is_exist == True
    assert data['data'] == {
        "page_number": {
            "table_id": {
                "upper_left": "99,82",
                "upper_right": "99,857",
                "lower_right": "2356,857",
                "lower_left": "2356,82",
                "cells": [{
                    "name": "cell_id1",
                    "upper_left": "99,82",
                    "upper_right": "99,857",
                    "lower_right": "2356,857",
                    "lower_left": "2356,82",
                    "start_row": 0,
                    "end_row": 2,
                    "start_col": 0,
                    "end_col": 3,
                    "content": "example"
                }]
            }
        }
    }


def test_autosave_detect_table(client, mocker):
    is_exist = False

    def _execute(sql, *args, **kwargs):
        nonlocal is_exist
        if TBL_USER_DETECT_TABLE in sql:
            is_exist = True
            return []

    mocker.patch.object(OracleAccess, "execute", _execute)

    response = client.post(
        '/api/table/autosave_detect_table',
        data=json.dumps({
            "uuid": "sa5e122hy215cb3degrt",
            "data": {
                "page_number": {
                    "table_id": {
                        "upper_left": "99,82",
                        "upper_right": "99,857",
                        "lower_right": "2356,857",
                        "lower_left": "2356,82",
                        "cells": [
                            {
                                "name": "cell_id1",
                                "upper_left": "99,82",
                                "upper_right": "99,857",
                                "lower_right": "2356,857",
                                "lower_left": "2356,82",
                                "start_row": 0,
                                "end_row": 2,
                                "start_col": 0,
                                "end_col": 3,
                                "content": "example"
                            }
                        ]
                    }
                }
            }
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert data['result'] == 0
    assert data['message'] == ''
    assert response.status_code == 200
    assert is_exist == True


def test_get_detect_cell(client, mocker):
    is_exist = False

    def _query(sql):
        nonlocal is_exist
        if not is_exist:
            is_exist = True
            return []
        else:
            return [[["Table", "$B$3:$O$25"], ["Header", "$C$3:$O$3"]]]

    mocker.patch.object(OracleAccess, "query", _query)

    response = client.post(
        '/api/table/get_detect_cell',
        data=json.dumps({
            "uuid": "s5weqw183cwqe75dd"
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert data['result'] == 1
    assert data['message'] == 'No data'
    assert response.status_code == 200
    assert is_exist == True
    

    response = client.post(
        '/api/table/get_detect_cell',
        data=json.dumps({
            "uuid": "s5weqw183cwqe75dd"
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert data['result'] == 0
    assert data['message'] == ''
    assert response.status_code == 200
    assert is_exist == True
    assert data['data'] == {
        "page_number": {
            "table_id": [{
                "cell_type":"Table",
                "range":"$B$3:$O$25" },
                {
                "cell_type":"Header", 
                "range":"$C$3:$O$3"}]
        }
    }


def test_autosave_detect_cell(client, mocker):
    is_exist = False

    def _execute(sql, *args, **kwargs):
        nonlocal is_exist
        if TBL_USER_DETECT_TABLE in sql:
            is_exist = True
            return []

    mocker.patch.object(OracleAccess, "execute", _execute)

    response = client.post(
        '/api/table/autosave_detect_cell',
        data=json.dumps({
            "uuid": "sa5e122hy215cb3degrt",
            "data": {
                    "page_number":{ "table_id":[{
                        "cell_type":"Table",
                        "range":"$B$3:$O$25" },
                        {
                        "cell_type":"Header",
                        "range":"$C$3:$O$3" }
                        ]}
                    }
                }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert data['result'] == 0
    assert data['message'] == ''
    assert response.status_code == 200
    assert is_exist == True


def test_get_key_value_mapping(client, mocker):
    is_exist = False

    def _query(sql):
        nonlocal is_exist
        if not is_exist:
            is_exist = True
            return []
        else:
            return [["epr_key1", "Bo,Borad,Boardnum"], ["epr_key4", "sta,status,status1"]]

    mocker.patch.object(OracleAccess, "query", _query)

    response = client.post(
        '/api/table/get_key_value_mapping',
        data=json.dumps({
            "vendor": "aa",
            "file_type": "bb"
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert data['result'] == 1
    assert data['message'] == 'No match data'
    assert response.status_code == 200
    assert is_exist == True
    assert data['data'] == {}

    response = client.post(
        '/api/table/get_key_value_mapping',
        data=json.dumps({
            "vendor": "aa",
            "file_type": "bb"
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert data['result'] == 0
    assert data['message'] == ''
    assert response.status_code == 200
    assert is_exist == True
    assert data['data'] == {
        "epr_key1": [
            "Bo",
            "Borad",
            "Boardnum"
        ],
        "epr_key4": [
            "sta",
            "status",
            "status1"
        ]
    }


def test_autosave_key_value_mapping(client, mocker):
    is_exist = False

    def _execute(sql, *args, **kwargs):
        nonlocal is_exist
        if TBL_USER_MAPPING_TABLE in sql:
            is_exist = True
            return []

    mocker.patch.object(OracleAccess, "execute", _execute)

    response = client.post(
        '/api/table/autosave_key_value_mapping',
        data=json.dumps({"data": [{
            "field": "epr_key1",
            "fieldvalue": [
                "Bo",
                "Borad"
            ],
            "vendor": "",
            "file_type": ""
        }]}),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert data['result'] == 0
    assert data['message'] == ''
    assert response.status_code == 200
    assert is_exist == True


def test_get_image_path(client, mocker):
    is_exist = False

    def _query(sql):
        nonlocal is_exist
        if not is_exist:
            is_exist = True
            return []
        else:
            return [["s5weqw183cwqe75dd", "../storage/photo/s5weqw183cwqe75dd/front.jpg", "../storage/photo/s5weqw183cwqe75dd/end.jpg"]]

    mocker.patch.object(OracleAccess, "query", _query)

    response = client.post(
        '/api/table/get_image_path',
        data=json.dumps({"uuid": ""}),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert data['result'] == 1
    assert data['message'] == 'uuid_not_exist'
    assert response.status_code == 200
    assert is_exist == True
    assert data['data'] == {
        'uuid': None,
        'front_path': None,
        'back_path': None
    }

    response = client.post(
        '/api/table/get_image_path',
        data=json.dumps({"uuid": ""}),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert data['result'] == 0
    assert data['message'] == ''
    assert response.status_code == 200
    assert is_exist == True
    assert data['data'] == {
        "uuid": "s5weqw183cwqe75dd",
        "front_path": "../storage/photo/s5weqw183cwqe75dd/front.jpg",
        "back_path": "../storage/photo/s5weqw183cwqe75dd/end.jpg"
    }


def test_autosave_image_path(client, mocker):
    is_exist = False

    def _query(sql):
        nonlocal is_exist
        if not is_exist:
            is_exist = True
            return []
        else:
            return [["s5weqw183cwqe75dd", "../storage/photo/s5weqw183cwqe75dd/front.jpg", "../storage/photo/s5weqw183cwqe75dd/end.jpg"]]

    def _execute(sql, *args, **kwargs):
        if TBL_USER_IMAGE_PATH_TABLE in sql:
            return []

    mocker.patch.object(OracleAccess, "query", _query)
    mocker.patch.object(OracleAccess, "execute", _execute)

    response = client.post(
        '/api/table/autosave_image_path',
        data=json.dumps({
            "uuid": "s1",
            "front_path": "../storage/photo/s5weqw183cwqe75dd/front.jpg",
            "back_path": "../storage/photo/s5weqw183cwqe75dd/end.jpg"
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert data['result'] == 0
    assert data['message'] == ''
    assert response.status_code == 200
    assert is_exist == True


def test_get_history_operate_list(client, mocker):
    is_exist = False

    def _query(sql):
        nonlocal is_exist
        if not is_exist:
            is_exist = True
            return [["7788", "a50558", "PRL",'Tenpack','jojo','TODO','','2020-11-24T14:58:45',"0"]]
        else:
            return []

    mocker.patch.object(OracleAccess, "query", _query)

    response = client.post(
        '/api/table/get_history_operate_list',
        data={},
        content_type='application/json'
    )

    data = json.loads(response.data)
    assert data['result'] == 0
    assert data['message'] == ''
    assert response.status_code == 200
    assert is_exist == True
    assert data['data'] == [{
                        "uuid" : "7788", 
                        "user_id" : "a50558",
                        "vendor" : "PRL",
                        "file_type" : "Tenpack",
                        "file_name" : "jojo",
                        "status" : "TODO",
                        "note" : "",
                        "update_time" : "2020-11-24T14:58:45",
                        "page_number" : "0"
                        }]


def test_upload_file(client, mocker):
    is_exist = False

    def _execute(sql, *args, **kwargs):
        nonlocal is_exist
        if TBL_USER_DETECT_TABLE in sql:
            is_exist = True
            return []

    mocker.patch.object(OracleAccess, "execute", _execute)

    file = open('./ap_server/tests/ToscaBrochure.pdf', 'rb')
    response = client.post(
        '/api/table/upload_file',
        content_type='multipart/form-data',
        data={
            'file': (file, './ap_server/tests/ToscaBrochure.pdf'),
        },
    )
    data = json.loads(response.data)
    assert data['result'] == 0
    assert data['message'] == ''
    assert response.status_code == 200
    assert is_exist == True


def test_upload_file_option(client, mocker):
    is_exist = False

    def _query(sql):
        nonlocal is_exist
        if not is_exist:
            is_exist = True
            return [["ocr_1_a","pdf","itri","null"]]
        else:
            return [["ocr_1_a","pdf","itri",'null']]


    mocker.patch.object(OracleAccess, "query", _query)


    response = client.post(
        '/api/table/upload_file_option',
        data={},
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert data['result'] == 0
    assert data['message'] == ''
    assert response.status_code == 200
    assert data['data'] ==[{
        "model_name": "ocr_1_a", 
        "file_type": "pdf", 
        "vendor": "itri", 
        "update_time": 'null'
    }]


def test_get_upload_progress(client, mocker):
    is_exist = False

    def _query(sql):
        nonlocal is_exist
        if not is_exist:
            is_exist = True
            return [["account2","PRL","Tenpack","123","2020-10-05 22:45:13","預測中","fd955004-a37d-44b5-8c71-5209ae90959c"]]
        else:
            return []


    mocker.patch.object(OracleAccess, "query", _query)


    response = client.post(
        '/api/table/get_upload_progress',
        data={},
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert data['result'] == 0
    assert data['message'] == ''
    assert response.status_code == 200
    assert data['data'] ==[{
        "user_id":"account2",
        "vendor":"PRL",
        "file_type":"Tenpack",
        "file_name":"123",
        "upload_time":"2020-10-05 22:45:13", 
        "status":"預測中",
        "task_id": "fd955004-a37d-44b5-8c71-5209ae90959c"
    }]


def test_delete_upload_progress(client, mocker):
    is_exist = False
    def _query(sql):
        nonlocal is_exist
        if not is_exist:
            is_exist = True
            return [["fd955004-a37d-44b5-8c71-5209ae90959c"]]
        else:
            return []

    def _execute(sql, *args, **kwargs):
        nonlocal is_exist
        if TBL_USER_DETECT_TABLE in sql:
            is_exist = True
            return []

    mocker.patch.object(OracleAccess, "query", _query)
    mocker.patch.object(OracleAccess, "execute", _execute)

    response = client.post(
        '/api/table/delete_upload_progress',
        data=json.dumps({
            "task_id": "fd955004-a37d-44b5-8c71-5209ae90959c"
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert data['result'] == 0
    assert data['message'] == ''
    assert response.status_code == 200
    assert is_exist == True


def test_get_compare_version(client, mocker):
    is_exist = False


    def _query(sql):
        nonlocal is_exist
        if not is_exist:
            is_exist = True
            return [[0,2,0,0,3,5,0,0,1,'factory','data','data','123456'],[0,2,0,0,3,5,0,0,0,'board_num','data','data','123456']]
        else:
            return []

    mocker.patch.object(OracleAccess, "query", _query)

    response = client.post(
        '/api/table/get_compare_version',
        data=json.dumps({'hist_version':'1'}),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert data['result'] == 0
    assert data['message'] == ''
    assert response.status_code == 200
    assert data['history'] == {'page1':{'table1':{'key_start_row':'0', 'key_end_row':'2', 'key_start_col':'0', 'key_end_col':'0','value_start_row':'3', 'value_end_row':'5', 'value_start_col':'0', 'value_end_col':'0', 'mark':'0', 'key':'board_num', 'key_type':'data', 'value_type':'data', 'value':'123456'}}}
    assert data['current'] == {'page1':{'table1':{'key_start_row':'0', 'key_end_row':'2', 'key_start_col':'0', 'key_end_col':'0', 'value_start_row':'3', 'value_end_row':'5', 'value_start_col':'0', 'value_end_col':'0', 'mark':'1',  'key':'factory','key_type':'data', 'value_type':'data', 'value':'123456'}}}


def test_autosave_compare_version(client, mocker):

    def _execute(sql, *args, **kwargs):
        if TBL_USER_DETECT_TABLE in sql:
            return []

    mocker.patch.object(OracleAccess, "execute", _execute)

    response = client.post(
        '/api/table/autosave_compare_version',
        data=json.dumps({
            "page1":{ 
                "table1":[
                {
                    "key_start_row":0, 
                    "key_end_row":2, 
                    "key_start_col":0, 
                    "key_end_col":0, 
                    "value_start_row":3, 
                    "value_end_row":5, 
                    "value_start_col":0, 
                    "value_end_col":0, 
                    "key_type":"data", 
                    "value_type":"data", 
                    "key":"factory", 
                    "value":"123456"
                }]
            }
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert data['result'] == 0
    assert data['message'] == ''
    assert response.status_code == 200


def test_autosave_compare_version(client, mocker):

    def _execute(sql, *args, **kwargs):
        if TBL_USER_DETECT_TABLE in sql:
            return []

    mocker.patch.object(OracleAccess, "execute", _execute)

    response = client.post(
        '/api/table/autosave_compare_version',
        data=json.dumps({
            "page1":{ 
                "table1":[
                {
                    "key_start_row":0, 
                    "key_end_row":2, 
                    "key_start_col":0, 
                    "key_end_col":0, 
                    "value_start_row":3, 
                    "value_end_row":5, 
                    "value_start_col":0, 
                    "value_end_col":0, 
                    "key_type":"data", 
                    "value_type":"data", 
                    "key":"factory", 
                    "value":"123456"
                }]
            }
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert data['result'] == 0
    assert data['message'] == ''
    assert response.status_code == 200


def test_get_detect_cell_file(client, mocker):
    
    response = client.post(
        '/api/table/get_detect_cell_file',
        data=json.dumps({"uuid": "12",
        "page_number": "12",}),
        content_type='application/json'
    )