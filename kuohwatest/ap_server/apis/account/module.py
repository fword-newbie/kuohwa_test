from flask_mail import Message
import string
import random

import base_api
from configs.tbl_consts import TBL_USER_ACCOUNT
from utils.orcl_utils import OracleAccess
import hashlib



class Account(object):
    @staticmethod
    def login(username, passwd):  # 登入 API
        # TODO
        # raw = OracleAccess.query("select * from test")
        return {
            'result': 0,
            'message': "",
            "data": "登入成功",
            "test": "123"
        }


    @staticmethod
    def forget(username):  # 忘記密碼 API
        user_exist=OracleAccess.query(
            f"select * from {TBL_USER_ACCOUNT} where USER_ID = '{username}'")
        if user_exist[0]:
            password=hashlib.sha1("password".encode('utf-8'))
            password=password.hexdigest().upper()
            OracleAccess.execute(
            f"update {TBL_USER_ACCOUNT} set PASSWORD = '{password}' where USER_ID = '{username}' ", args=[])
            msg = Message("title", recipients=[user_exist[0][0]])
            msg.body = "content"
            base_api.mail.send(msg)
            return {
                'result': 0,
                'message': ""
            }
        else:
            return {
                'result': 1,
                'message': "Account not found"
            }


    @staticmethod
    def get_account_list():  # 獲取清單 API
        all_account=OracleAccess.query(f"SELECT * FROM {TBL_USER_ACCOUNT}")
        if all_account!= []:
            for user in all_account:
                user_data=[]
                user_data.append({
                    'user_id':user[0],
                    'role':[role for role in user[1].split(',')],
                    'email':user[2],
                    'update_time':"2021/03/14"
                    }
                )
            return {
                'result': 0,
                'message': "",
                'data':user_data
            }
        return {
            'result': 1,
            'message': "No Account",
            'data': []
        }

    @staticmethod
    def add_account_list(user_id,role,email):  # 新增帳號 API
        user_data=OracleAccess.query(
            f"select * from {TBL_USER_ACCOUNT} where USER_ID = {user_id}")
        if user_data:
            return {
                'result': 1,
                'message': "add fail. Account is already exist"
            }
        OracleAccess.execute(
            f"insert into {TBL_USER_ACCOUNT} (USER_ID, ROLE, EMAIL) values (:1, :2, :3)", [(user_id, role, email)])
        return{
            'result': 0,
            'message': "",
        }


    @staticmethod
    def delete_account_list(user_id):  # 刪除帳號 API
        user_exist= OracleAccess.query("select * from {TBL_USER_ACCOUNT} where USER_ID = {user_id}")
        if user_exist != []:
            OracleAccess.execute(
                f"delete from {TBL_USER_ACCOUNT} where where USER_ID = '{user_id}'",args=[])
            return{
                'result': 0,
                'message': "",
            }
        else:
            return{
                'result': 1,
                'message': "account not exist",
            }


    @staticmethod
    def update_account_list(old_user_id,data):  # 更新帳號 API
        user_exist= OracleAccess.query("select * from {TBL_USER_ACCOUNT} where USER_ID = '{old_user_id}'")
        if user_exist != []:
            new_user_id=data['new_user_id']
            new_role=data['new_role']
            new_email=data['new_email']
            OracleAccess.execute(
                f"update from {TBL_USER_ACCOUNT} set USER_ID = '{new_user_id}' ROLE = '{new_role}' EMAIL = '{new_email}' where where USER_ID = '{old_user_id}'", arg=[])
            return{
                'result': 0,
                'message': "",
            } 
        else:
            return{
                'result': 1,
                'message': "account not exist",
            }

    
    @staticmethod
    def update_account_status(old_user_id,is_activated):  # 更新帳號狀態 API
        user_exist= OracleAccess.query("select * from {TBL_USER_ACCOUNT} where USER_ID = '{old_user_id}'")
        if user_exist!= []:
            OracleAccess.execute(
                f"update from {TBL_USER_ACCOUNT} set is_activated = '{is_activated}' where where USER_ID = '{old_user_id}'", arg=[])
            return{
                'result': 0,
                'message': "",
            } 
        else:
            return{
                'result': 1,
                'message': "account not exist",
            }


    @staticmethod
    def import_account(data):  # 獲取清單 API
        user_id=data['account']
        password=data['password']
        email=data['email']
        password=hashlib.sha1(password.encode('utf-8'))
        password=password.hexdigest().upper()
        OracleAccess.execute(
            f"insert into {TBL_USER_ACCOUNT} (USER_ID, PASSWORD, EMAIL) values (:1, :2, :3)", [(user_id, password, email)])
        return {
                'result': 0,
                'message': ""
        }