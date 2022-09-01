from doctest import Example
from pkg_resources import require
from requests import request
from flask_restplus import Namespace, Resource, fields, model

api = Namespace("account", description=u"帳號及權限管理")


base_input_payload = api.model(u'基礎輸入參數定義', {
    'result': fields.Integer(required=True, default=0),
    'message': fields.String(required=True, default=""),
})


# 登入 API
account_input_payload = api.model(u'帳號input', {
    'username': fields.String(required=True, example="tami"),
    'passwd': fields.String(required=True, example="tami")
})

account_output_payload = api.clone(u'帳號output', base_input_payload, {
    'data': fields.String(required=True),
    "test": fields.String(required=True)
})


#忘記密碼的預輸出入api
account_forget_input_payload=api.model('忘記密碼的預輸入', {
    'username': fields.String(require=True,example='itri@kuohwa.com')
})
account_forget_output_payload=api.clone('忘記密碼的預輸出',base_input_payload)

#新增帳號的api
account_add_input_payload=api.model('新增帳號輸入',{
    'user_id': fields.String(require=True,example=''),
    'role': fields.List(fields.String, required=True, example=["admin", "super_user","Gerneral_User"]),
    'email': fields.String(require=True,example='')
})
account_add_output_payload=api.clone('新增帳號輸出',base_input_payload)

#獲得帳號清單的api
account_get_output_payload=api.model('獲得帳號清單輸出',{
    'user_id': fields.String(require=True,example='ta'),
    'role': fields.List(fields.String, required=True, example=["admin", "super_user","Gerneral_User"]),
    'email': fields.String(require=True,example='itri@kuohwa.com'),
    'update_time':fields.String(require=True,example='2021/03/14')
})
account_get_output_and_status_payload=api.clone('加上reasult的帳號清單輸出',base_input_payload,{
    'data':fields.List(fields.Nested(account_get_output_payload), required=True,)
})

#刪除帳號清單的api  
account_delete_input_payload=api.model('刪除帳號輸入',{
    'user_id': fields.String(require=True,example='')
})
account_delete_output_payload=api.clone('刪除帳號輸出',base_input_payload)

#更新帳號清單的api
account_updatedata_input_payload=api.model('更新帳號的新data',{
    'new_user_id': fields.String(require=True,example=''),
    'new_role': fields.List(fields.String, required=True, example=["admin", "super_user","Gerneral_User"]),
    'new_email': fields.String(require=True,example='')
})
account_update_input_payload=api.model('加上新data的更新帳號輸入',{
    'old_user_id': fields.String(require=True,example=''),
    'data':fields.List(fields.Nested(account_updatedata_input_payload), required=True,)
})
account_update_output_payload=api.clone('更新帳號輸出',base_input_payload)

#更新帳號狀態的api
account_update_status_input_payload=api.model('更新帳號狀態輸入',{
    'old_user_id': fields.String(require=True,example=''),
    'is_activated': fields.String(require=True,example='true')    
})
account_update_status_output_payload=api.clone('更新帳號狀態輸出',base_input_payload)


#批次
pichi_output=api.model('新增帳號輸入',{
    'user_id': fields.String(require=True,example=''),
    'password': fields.String(require=True,example=''),
    'email': fields.String(require=True,example='')
})