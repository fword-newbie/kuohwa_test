import uuid
from apis.table.model import *
from apis.table.module import *
from flask import session
from base_api import CustomResource

ROLE_ADMIN = "Admin" 


@api.route("/upload_file")  #  上傳檔案 API OK
class uploadfile(CustomResource):
    @api.expect(upload_file)
    @api.marshal_with(upload_file_out)
    def post(self):
        files=request.files["file"]
        return Table.upload_file(file=files)


@api.route("/get_detect_table")
class get_detect_table(CustomResource): #表格偵測 API OK
    @api.expect(getDetectTable_input_payload)
    # @api.marshal_with(getDetectTable_output_payload)
    def post(self):
        data=api.payload
        uuid=data['uuid']
        return Table.get_detect_table(uuid=uuid)


@api.route("/autosave_detect_table")  # 表格偵測自動儲存 API OK
class autosave_detect_table(CustomResource):
    @api.expect(autosave_detect_table_input_payload)
    def post(self):
        data = api.payload
        return Table.autosave_detect_table(uuid=data['uuid'], data=data['data'])


@api.route("/get_detect_cell")  # 單元格偵測檔案 API OK
class get_detect_cell(CustomResource):
    @api.expect(get_detect_cell_input_payload)
    # @api.marshal_with(get_detect_cell_output_payload)
    def post(self):
        data = api.payload
        return Table.get_detect_cell(uuid=data['uuid'])


@api.route("/autosave_detect_cell")  # 單元格偵測自動儲存 API OK
class autosave_detect_cell(CustomResource):
    def post(self):
        data = api.payload
        return Table.autosave_detect_cell(uuid=data['uuid'],data=data['data'])


@api.route("/get_key_value_mapping")  # ERP Key-Value 對照表 API OK
class get_key_value_mapping(CustomResource):
    @api.expect(get_key_value_mapping_input_payload)
    def post(self):
        data = api.payload
        return Table.get_key_value_mapping(vendor=data['vendor'],file_type=data['file_type'])


@api.route("/autosave_key_value_mapping")  # 自動儲存ERP Key-Value API OK
class autosave_key_value_mapping(CustomResource):
    def post(self):
        data = api.payload
        return Table.autosave_key_value_mapping(data=data)


@api.route("/get_image_path")  # 圖片路徑 API OK
class get_image_path(CustomResource):
    @api.expect(get_image_path_input_payload)
    @api.marshal_with(get_image_path_output_payload)
    def post(self):
        data = api.payload
        return Table.get_image_path(uuid=data['uuid'])


@api.route("/autosave_image_path")  # 自動儲存圖片路徑 API OK
class autosave_image_path(CustomResource):
    @api.expect(autosave_image_path_input_payload)
    def post(self):
        data = api.payload
        return Table.autosave_image_path(uuid=data['uuid'],front_path=data['front_path'],back_path=data['back_path'])


@api.route("/upload_file_option")  #  上傳檔案 API upload_file 下拉式選單 API OK
class upload_file_option(CustomResource):
    # @api.marshal_with(upload_file_option_output)
    def post(self):
        return Table.upload_file_option()


@api.route("/get_history_operate_list")  # 歷史清單 API OK
class get_history_operate_list(CustomResource):
    def post(self):
        return Table.get_history_operate_list()


@api.route("/get_upload_progress")  # 辨識進度列表 API OK
class get_upload_progress(CustomResource):
    @api.marshal_with(get_upload_progress_output)
    def post(self):
        return Table.get_upload_progress()


@api.route("/delete_upload_progress")  # 刪除進度列表 API OK
class delete_upload_progress(CustomResource):
    @api.expect(delete_upload_progress_input)
    def post(self):
        data=api.payload
        return Table.delete_upload_progress(task_id=data['task_id'])


@api.route("/get_compare_version_option")  # 選擇對比版本 API OK
class get_compare_version_option(CustomResource):
    def post(self):
        return Table.get_compare_version_option()


@api.route("/get_compare_version")  # 對比版本 API OK
class get_compare_version(CustomResource):
    @api.expect(get_compare_version_input)
    @api.marshal_with(get_compare_version_output_fin)
    def post(self):
        data=api.payload
        return Table.get_compare_version(hist_version=data['hist_version'])


@api.route("/autosave_compare_version")  # 儲存對比版本 API  OK
class autosave_compare_version(CustomResource):
    @api.expect(autosave_compare_version_input)
    @api.marshal_with(base_input_payload)
    def post(self):
        data=api.payload
        return Table.autosave_compare_version(data=data)


@api.route("/get_detect_cell_file")  # 單元格偵測檔案 API
class get_detect_cell_file(CustomResource):
    @api.expect(get_detect_cell_file_input)
    def post(self):
        data = api.payload
        return Table.get_detect_cell_file(uuid=data['uuid'], page_number=data['page_number'])