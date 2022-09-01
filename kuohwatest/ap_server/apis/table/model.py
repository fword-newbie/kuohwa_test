import uuid
from flask_restplus import Namespace, Resource, fields, model
from werkzeug.datastructures import FileStorage

api = Namespace("table", description=u"表格偵測結構", ordered=False)


base_input_payload = api.model(u'基礎輸入參數定義', {
    'result': fields.Integer(required=True, default=0),
    'message': fields.String(required=True, default=""),
})


# 表格偵測 API
getDetectTable_input_payload = api.model(u'表格偵測input',  {
    "uuid": fields.String(required=True, example="s5weqw183cwqe75dd")
})


getDetectTable_output_payload = api.model(u'表格偵測output',  {
    "name": fields.String(required=True, example="cell_id1"),
    "upper_left": fields.String(required=True, example="99,82"),
    "upper_right": fields.String(required=True, example="99,857"),
    "lower_right": fields.String(required=True, example="2356,857"),
    "lower_left": fields.String(required=True, example="2356,82"),
    "start_row": fields.Integer(required=True, example=0),
    "end_row": fields.Integer(required=True, example=2),
    "start_col": fields.Integer(required=True, example=0),
    "end_col": fields.Integer(required=True, example=3),
    "content": fields.String(required=True, example="example"),
})


autosaveDetectTable_input_2_data_payload = api.model(u'自動儲存第二層',  {
    "upper_left": fields.String(required=True, example="99,82"),
    "upper_right": fields.String(required=True, example="99,857"),
    "lower_right": fields.String(required=True, example="2356,857"),
    "lower_left": fields.String(required=True, example="2356,82"),
    "cells": fields.List(fields.Nested(getDetectTable_output_payload))
})


autosaveDetectTable_input_3_data_payload = api.model(u'自動儲存第三層',  {
    "table_id": fields.Nested(autosaveDetectTable_input_2_data_payload)
})


autosaveDetectTable_input_4_data_payload = api.model(u'自動儲存第四層',  {
    "page_number": fields.Nested(autosaveDetectTable_input_3_data_payload)
})


autosave_detect_table_input_payload = api.model(u'自動儲存第五層',{
    "uuid": fields.String(required=True, example="s5weqw183cwqe75dd"),
    "data": fields.Nested(autosaveDetectTable_input_4_data_payload)
})


get_detect_cell_input_payload = api.model(u'單元格偵測入',{
    "uuid": fields.String(required=True, example="s5weqw183cwqe75dd")
})


get_key_value_mapping_input_payload = api.model(u'ERP Key-Value 對照表 API',{
    "vendor": fields.String(required=True, example=""),
    "file_type": fields.String(required=True, example="")
})


get_image_path_input_payload = api.model(u'圖片路徑 API輸入',{
    "uuid": fields.String(required=True, example="")
})


get_image_path_outdata_payload= api.model(u'圖片路徑 API輸出',{
    "uuid":fields.String(required=True, example=""), 
    "front_path":fields.String(required=True, example=""), 
    "back_path":fields.String(required=True, example="")
})


get_image_path_output_payload= api.clone(u'圖片路徑 API輸出',base_input_payload,{
    "data":fields.Nested(get_image_path_outdata_payload)
})


autosave_image_path_input_payload = api.model(u'自動儲存圖片路徑 API',{
    "uuid": fields.String(required=True, example=""),
    "front_path": fields.String(required=True, example=""),
    "back_path": fields.String(required=True, example="")
})

upload_file = api.parser()
upload_file.add_argument(
    'file', type=FileStorage, location='files')

upload_file_out = api.clone(u'自動儲存圖片路徑output', base_input_payload,{
    "task_id": fields.String(required=True, example=""),
    "uuid": fields.String(required=True, example="")
})

# get_detect_cell_outdata_payload = api.model(u'單元格偵測檔案輸出前',  {
#     "cell_type": fields.String(required=True, example="Table"),
#     "range": fields.String(required=True, example="$B$3:$O$25")
# })


# get_detect_cell_output_payload = api.clone(u'單元格偵測檔案處理後輸出',  base_input_payload,{
#     "table_id": fields.List(fields.Nested(get_detect_cell_outdata_payload))
# })

upload_file_option_output = api.model(u'upload_file 下拉式選單 outout',{
    "model_name": fields.String(required=True, example=""),
    "file_type": fields.String(required=True, example=""),
    "vendor": fields.String(required=True, example=""),
    "update_time": fields.String(required=True, example="")
})


get_upload_progress_output_data = api.model(u'辨識進度列表輸出前',{
    "user_id": fields.String(required=True, example=""),
    "vendor": fields.String(required=True, example=""),
    "file_type": fields.String(required=True, example=""),
    "file_name": fields.String(required=True, example=""),
    "upload_time": fields.String(required=True, example=""),
    "status": fields.String(required=True, example=""),
    "task_id": fields.String(required=True, example="")
})


get_upload_progress_output = api.clone(u'辨識進度列表輸出', base_input_payload ,{
    "data":fields.Nested(get_upload_progress_output_data)
})


delete_upload_progress_input = api.model(u'刪除進度列表輸入',{
    "task_id": fields.String(required=True, example="")
})


get_compare_version_input = api.model(u'比對版本輸入' ,{
    "hist_version":fields.String(required=True, example="")
})
#---------------------------比對版本---------------------------
get_compare_version_output_histroy_data= api.model(u'比對版本歷史資料' ,{
    "key_start_row":fields.String(required=True, example=""),
    "key_end_row":fields.String(required=True, example=""),
    "key_start_col":fields.String(required=True, example=""),
    "key_end_col":fields.String(required=True, example=""),
    "value_start_row":fields.String(required=True, example=""),
    "value_end_row":fields.String(required=True, example=""),
    "value_start_col":fields.String(required=True, example=""),
    "value_end_col":fields.String(required=True, example=""),
    "mark":fields.String(required=True, example=""),
    "key":fields.String(required=True, example=""),
    "key_type":fields.String(required=True, example=""),
    "value_type":fields.String(required=True, example=""),
    "value":fields.String(required=True, example="")
})

get_compare_version_output_current_data= api.model(u'比對版本正確資料' ,{
    "key_start_row":fields.String(required=True, example=""),
    "key_end_row":fields.String(required=True, example=""),
    "key_start_col":fields.String(required=True, example=""),
    "key_end_col":fields.String(required=True, example=""),
    "value_start_row":fields.String(required=True, example=""),
    "value_end_row":fields.String(required=True, example=""),
    "value_start_col":fields.String(required=True, example=""),
    "value_end_col":fields.String(required=True, example=""),
    "mark":fields.String(required=True, example=""),
    "key":fields.String(required=True, example=""),
    "key_type":fields.String(required=True, example=""),
    "value_type":fields.String(required=True, example=""),
    "value":fields.String(required=True, example="")
})


get_compare_version_output_current_table= api.model(u'比對版本正確table' ,{
    "table1":fields.Nested(get_compare_version_output_current_data, required=True)
})

get_compare_version_output_histroy_table= api.model(u'比對版本歷史table' ,{
    "table1":fields.Nested(get_compare_version_output_histroy_data, required=True)
})

get_compare_version_output_current_page= api.model(u'比對版本正確page' ,{
    "page1":fields.Nested(get_compare_version_output_current_table)
})

get_compare_version_output_histroy_page= api.model(u'比對版本歷史page' ,{
    "page1":fields.Nested(get_compare_version_output_histroy_table)
})

get_compare_version_output_fin = api.clone(u'比對版本最後輸出', base_input_payload,{
    'current':fields.Nested(get_compare_version_output_current_page),
    'history':fields.Nested(get_compare_version_output_histroy_page)
})
#---------------------------比對版本---------------------------
autosave_compare_version_input= api.model(u'儲存版本輸入' ,{
    "key_start_row":fields.String(required=True, example=""),
    "key_end_row":fields.String(required=True, example=""),
    "key_start_col":fields.String(required=True, example=""),
    "key_end_col":fields.String(required=True, example=""),
    "value_start_row":fields.String(required=True, example=""),
    "value_end_row":fields.String(required=True, example=""),
    "value_start_col":fields.String(required=True, example=""),
    "value_end_col":fields.String(required=True, example=""),
    "key_type":fields.String(required=True, example=""),
    "value_type":fields.String(required=True, example=""),
    "key":fields.String(required=True, example=""),
    "value":fields.String(required=True, example="")
})


get_detect_cell_file_input= api.model(u'獲取單元格偵測 輸入',{
    'uuid':fields.String(required=True, example=""),
    'page_number':fields.String(required=True, example="")
})