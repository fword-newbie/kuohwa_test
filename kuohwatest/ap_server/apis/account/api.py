from apis.account.model import *
from apis.account.module import *
from flask import session
from base_api import CustomResource
import csv
ROLE_ADMIN = "Admin"


@api.route("/test")
class Login2(CustomResource):
    allow_roles = [ROLE_ADMIN]

    def post(self):
        return "OK"


@api.route("/login")  # 登入 API
class Login(CustomResource):
    @api.expect(account_input_payload)
    @api.marshal_with(account_output_payload)
    def post(self):
        session["roles"] = [ROLE_ADMIN]
        data = api.payload
        return Account.login(username=data["username"], passwd=data["passwd"])


@api.route("/forget") #忘記密碼 O
class forget(CustomResource):
    @api.expect(account_forget_input_payload)
    @api.marshal_with(account_forget_output_payload)
    def post(self):
        data=api.payload
        return Account.forget(username=data['username'])


@api.route("/get_account_list") #獲取帳號清單 O
class get_account_list(CustomResource):
    @api.marshal_with(account_get_output_and_status_payload)
    def post(self):
        return Account.get_account_list()


@api.route("/add_account_list") #新增帳號 O
class add_account_list(CustomResource):
    @api.expect(account_add_input_payload)
    @api.marshal_with(account_add_output_payload)
    def post(self):
        data=api.payload
        return Account.add_account_list(user_id=data['user_id'],role=data['role'],email=data['email'])


@api.route("/delete_account_list") #刪除帳號 O
class delete_account_list(CustomResource):
    @api.expect(account_delete_input_payload)
    @api.marshal_with(account_delete_output_payload)
    def post(self):
        data=api.payload
        return Account.delete_account_list(user_id=data['user_id'])


@api.route("/update_account_list") #更新帳號 O
class update_account_list(CustomResource):
    @api.expect(account_update_input_payload)
    @api.marshal_with(account_update_output_payload)
    def post(self):
        data=api.payload
        return Account.update_account_list(old_user_id=data['old_user_id'],data=data["data"])


@api.route("/update_account_status") #更新帳號狀態 O
class update_account_status(CustomResource):
    @api.expect(account_update_status_input_payload)
    @api.marshal_with(account_update_status_output_payload)
    def post(self):
        data=api.payload
        return Account.update_account_status(old_user_id=data['old_user_id'],is_activated=data['is_activated'])


@api.route("/import_account") #批次傳入
class import_account(CustomResource):
    @api.marshal_with(pichi_output)
    def post(self):
        data=request.files["file"]
        data = csv.DictReader(data.read().decode(
            'utf-8').splitlines()[1:], fieldnames=("account", "email", "passwd"))
        return Account.update_account_status(data)