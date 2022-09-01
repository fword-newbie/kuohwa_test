from pydoc import pager
from sre_constants import RANGE
from typing import KeysView
import uuid
from flask import request ,send_file,send_from_directory
from flask_mail import Message
from werkzeug.utils import secure_filename
import os
import xlwt

import base_api
from configs.tbl_consts import TBL_USER_DETECT_TABLE, TBL_USER_IMAGE_PATH_TABLE, TBL_USER_MAPPING_TABLE
from utils.orcl_utils import OracleAccess

 
class Table(object):
    @staticmethod
    def upload_file(file):#上傳檔案
        task_id=""
        uuid=""
        OracleAccess.execute(
            f"insert into {TBL_USER_DETECT_TABLE} (UUID, FILE) values (:1, :2)", [uuid, file])
        return{
            "result":0, 
            "message":"", 
            "task_id": task_id, 
            "uuid": uuid
            }


    @staticmethod
    def get_detect_table(uuid):#表格偵測 API
        user_data = OracleAccess.query(
        f"select * from {TBL_USER_DETECT_TABLE} where UUID = '{uuid}'")
        uuid=uuid
        if user_data != []:
            data = {
                "page_number": {
                    "table_id": {
                        "upper_left": user_data[0][1],
                        "upper_right": user_data[0][2],
                        "lower_right": user_data[0][4],
                        "lower_left": user_data[0][3],
                        "cells": [{
                            "name": user_data[0][5],
                            "upper_left": user_data[0][6],
                            "upper_right": user_data[0][7],
                            "lower_right": user_data[0][9],
                            "lower_left": user_data[0][8],
                            "start_row": int(user_data[0][10]),
                            "end_row": int(user_data[0][11]),
                            "start_col": int(user_data[0][12]),
                            "end_col": int(user_data[0][13]),
                            "content": user_data[0][14]
                        }]
                    }
                }
            }
            return{
                "result":0, 
                "message":"", 
                "data":data
                }
        return{
                "result":1, 
                "message":"No data"
                }


    @staticmethod
    def autosave_detect_table(uuid,data):
        OracleAccess.execute(
            f"""insert into {TBL_USER_DETECT_TABLE} (
                UUID, 
                UPPER_LEFT, 
                UPPER_RIGHT, 
                LOWER_LEFT, 
                LOWER_RIGHT, 
                CELL_NAME, 
                CELL_UPPER_LEFT, 
                CELL_UPPER_RIGHT, 
                CELL_LOWER_LEFT, 
                CELL_LOWER_RIGHT, 
                START_ROW, 
                END_ROW, 
                START_COL, 
                END_COL, 
                CONTENT) values (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15)""", [(
                uuid,
                data['page_number']['table_id']['upper_left'],
                data['page_number']['table_id']['upper_right'],
                data['page_number']['table_id']['lower_left'],
                data['page_number']['table_id']['lower_right'],
                data['page_number']['table_id']['cells'][0]['name'],
                data['page_number']['table_id']['cells'][0]['upper_left'],
                data['page_number']['table_id']['cells'][0]['upper_right'],
                data['page_number']['table_id']['cells'][0]['lower_left'],
                data['page_number']['table_id']['cells'][0]['lower_right'],
                data['page_number']['table_id']['cells'][0]['start_row'],
                data['page_number']['table_id']['cells'][0]['end_row'],
                data['page_number']['table_id']['cells'][0]['start_col'],
                data['page_number']['table_id']['cells'][0]['end_col'],
                data['page_number']['table_id']['cells'][0]['content'])])
        return{
            "result":0,
            "message":"" 
            }


    # @staticmethod
    # def get_detect_cell_file(uuid,page_number):
    #     # user_data = OracleAccess.query(f"select * from {TBL_USER_DETECT_TABLE} where UUID = '{uuid}',where PAGE_NUMBER = '{page_number}'")
    #     user_data = OracleAccess.query(
    #     f"select * from {TBL_USER_DETECT_TABLE} where UUID = '{uuid}'")

  
    @staticmethod
    def get_detect_cell(uuid):#單元格偵測 API OK
        user_data = OracleAccess.query(
        f"select * from {TBL_USER_DETECT_TABLE} where UUID = '{uuid}'")
        if user_data!= []:
            table_id=[]
            for count in (0,(len(user_data[0])-1)):
                cell_type=user_data[0][count][0]
                range=user_data[0][count][1]
                dic={'cell_type':cell_type,'range':range}
                table_id.append(dic)
            return{
            "result":0,
            "message":"" ,
            "data":{
                "page_number":{
                    "table_id":table_id
                }
            }
            }
        return{
        "result":1,
        "message":"No data" 
        }


    @staticmethod
    def autosave_detect_cell(uuid,data): #單元格偵測自動儲存 API
        for count in (0,(len(data['page_number']['table_id'])-1)):
            OracleAccess.execute(
                f"""insert into {TBL_USER_DETECT_TABLE} (
                    UUID,
                    CELL_TYPE,
                    RANGE,
                    CONTENT) values (:1, :2, :3)""", [(
                    uuid,
                    data['page_number']['table_id'][count]['cell_type'],
                    data['page_number']['table_id'][count]['range'])])
        return{
            "result":0,
            "message":""
        }
                    

    @staticmethod
    def get_key_value_mapping(vendor, file_type):  # ERP Key-Value 對照表 API
        user_data = OracleAccess.query(
            f"select * from {TBL_USER_MAPPING_TABLE} where VENDOR = '{vendor}' and FILE_TYPE = '{file_type}'")
        data = {}
        if user_data:
            
            for user_data_data in user_data:
                data[user_data_data[0]] = [
                    field_value for field_value in user_data_data[1].split(",")]
            return {
                'result': 0,
                'message': "",
                'data': data
            }
        return {
            'result': 1,
            'message': "No match data",
            'data':data
        }

    
    @staticmethod
    def autosave_key_value_mapping(data):  # ERP Key-Value 自動儲存 API
        file=data['data'][0]['field']
        vendor=data['data'][0]['vendor']
        file_type=data['data'][0]['file_type']
        fieldvalue=",".join(data['data'][0]['fieldvalue'])
        OracleAccess.execute(
            f"""insert into {TBL_USER_MAPPING_TABLE} (
                file,
                vendor,
                file_type,
                fieldvalue) values (:1, :2, :3, :4)""", [(
                file,
                vendor,
                file_type,
                fieldvalue)])
        return {
            'result': 0,
            'message': "",
        }


    @staticmethod
    def get_image_path(uuid):  # 圖片路徑 API
        user_data = OracleAccess.query(
            f"select * from {TBL_USER_IMAGE_PATH_TABLE} where UUID = '{uuid}' '")
        if user_data != []:
            return {
                'result': 0,
                'message': "",
                'data':{
                    'uuid':user_data[0][0],
                    'front_path':user_data[0][1],
                    'back_path':user_data[0][2]
                }
            }
        return {
                'result': 1,
                'message': "uuid_not_exist",
            }


    @staticmethod
    def autosave_image_path(uuid,front_path,back_path):  # 自動儲存圖片路徑 API
        user_data = OracleAccess.query(
            f"select * from {TBL_USER_IMAGE_PATH_TABLE} where UUID = '{uuid}' '")
        if user_data !=[]:
            OracleAccess.execute(
            f"delete * from {TBL_USER_IMAGE_PATH_TABLE} where UUID = '{uuid}' '")
        OracleAccess.execute(
        f"""insert into  {TBL_USER_IMAGE_PATH_TABLE} (
            UUID,
            front_path,
            back_path) values(:1, :2, :3)""",[(
                uuid,
                front_path,
                back_path
            )]
        )
        return {
            'result': 0,
            'message': "",
        }


    @staticmethod
    def get_history_operate_list():  # 歷史資料 API
        history_data = OracleAccess.query(
            f"select * from {TBL_USER_IMAGE_PATH_TABLE} where UUID = '{uuid}' '")
        data=[]
        for count in range(1,(len(history_data)+1)):
            data_dic={}
            data_dic['uuid']=history_data[0][0]
            data_dic['user_id']=history_data[0][1]
            data_dic['vendor']=history_data[0][2]
            data_dic['file_type']=history_data[0][3]
            data_dic['file_name']=history_data[0][4]
            data_dic['status']=history_data[0][5]
            data_dic['note']=history_data[0][6]
            data_dic['update_time']=history_data[0][7]
            data_dic['page_number']=history_data[0][8]
            data.append(data_dic)
        return {
            'result': 0,
            'message': "",
            'data':data
        }


    @staticmethod
    def upload_file_option():  # upload_file下拉式選單 API
        user_data = OracleAccess.query(
            f"select * from {TBL_USER_DETECT_TABLE}'")
        data=[]
        for count in range(len(user_data)):    
            dic={}        
            dic['model_name']=user_data[0][0]
            dic['file_type']=user_data[0][1]
            dic['vendor']=user_data[0][2]
            dic['update_time']=user_data[0][3]
            data.append(dic)
        return {
            'result': 0,
            'message': "",
            'data':data
        }


    @staticmethod
    def get_upload_progress():  # 辨識進度 API
        user_data = OracleAccess.query(
            f"select * from {TBL_USER_DETECT_TABLE}'")
        data=[]
        for count in range(len(user_data)):    
            dic={}        
            dic['user_id']=user_data[0][0]
            dic['vendor']=user_data[0][1]
            dic['file_type']=user_data[0][2]
            dic['file_name']=user_data[0][3]
            dic['upload_time']=user_data[0][4]
            dic['status']=user_data[0][5]
            dic['task_id']=user_data[0][6]
            data.append(dic)
        return {
            'result': 0,
            'message': "",
            'data':data
        }


    @staticmethod
    def delete_upload_progress(task_id):  # 自動儲存圖片路徑 API
        uuid="1112233"
        user_data = OracleAccess.query(
            f"select * from {TBL_USER_DETECT_TABLE} where UUID = '{uuid}' '")
        if user_data !=[]:
            OracleAccess.execute(
            f"delete * from {TBL_USER_DETECT_TABLE} where UUID = '{uuid}' and TASK_ID = '{task_id}'", arg=[] )
        return {
            'result': 0,
            'message': "",
        }


    @staticmethod
    def get_compare_version_option():  # 選擇對比版本 API
        Version=[]
        Version.append("version1")
        Version.append("version2")
        return {
            'result': 0,
            'message': "",
            'data':Version
        }


    @staticmethod
    def get_compare_version(hist_version):  # 對比版本 API
        user_data = OracleAccess.query(
            f"select * from {TBL_USER_DETECT_TABLE} where HIST_VERSION = '{hist_version}' '")
        data=[]
        for count in range(len(user_data)):    
            dic={}
            tab_dic={}
            pag_dic={}
            dic['key_start_row']=user_data[count][0]
            dic['key_end_row']=user_data[count][1]
            dic['key_start_col']=user_data[count][2]
            dic['key_end_col']=user_data[count][3]
            dic['value_start_row']=user_data[count][4]
            dic['value_end_row']=user_data[count][5]
            dic['value_start_col']=user_data[count][6]
            dic['value_end_col']=user_data[count][7]
            dic['mark']=user_data[count][8]
            dic['key']=user_data[count][9]
            dic['key_type']=user_data[count][10]
            dic['value_type']=user_data[count][11]
            dic['value']=user_data[count][12]
            tab_dic['table1']=dic
            pag_dic['page1']=tab_dic
            data.append(pag_dic)
        return {
            'result': 0,
            'message': "",
            'current':data[0],
            'history':data[1]
        }


    @staticmethod
    def autosave_compare_version(data):  # 儲存對比版本 API
        page=list(data.keys())[0]
        table=list(data[page].keys())[0]
        data_to_use=data[page][table][0]
        OracleAccess.execute(
        f"""insert into {TBL_USER_DETECT_TABLE} (
            page,
            table,
            key_start_row,
            key_end_row, 
            key_start_col,
            key_end_col,
            value_start_row,
            value_end_row,
            value_start_col,
            value_end_col,
            key_type,
            value_type,
            key,
            value) values (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13 ,:14)""", 
            [(
            page,
            table,
            data_to_use['key_start_row'],
            data_to_use['key_end_row'],
            data_to_use['key_start_col'],
            data_to_use['key_end_col'],
            data_to_use['value_start_row'],
            data_to_use['value_end_row'],
            data_to_use['value_start_col'],
            data_to_use['value_end_col'],
            data_to_use['key_type'],
            data_to_use['value_type'],
            data_to_use['key'],
            data_to_use['value']
            )] 
        )
        return {
            'result': 0,
            'message': ""
        }


    @staticmethod
    def get_detect_cell_file(uuid,page_number):  # 單元格偵測 API
        workbook = xlwt.Workbook(encoding='utf-8')       #新建工作簿
        sheet1 = workbook.add_sheet("測試表格")          #新建sheet
        sheet1.write(0,0,"uuid")      #第1行第1列資料
        sheet1.write(0,1,"page_number")      #第1行第2列資料
        sheet1.write(1,0,uuid)      #第2行第1列資料
        sheet1.write(1,1,page_number)      #第2行第2列資料
        workbook.save(r'/home/ubuntu/kuohwatest/ap_server/tests/test.xlsx')   #儲存
        try:
            return send_file('/home/ubuntu/kuohwatest/ap_server/tests/test.xlsx', attachment_filename='test.xlsx')
        except Exception as e:
            return print(e)