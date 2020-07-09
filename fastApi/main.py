from fastapi import FastAPI,Form,UploadFile,File
from pydantic import BaseModel
from typing import List
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from video2audio_noiseReduction import video2audio_removeNoise

app = FastAPI()

# class People(BaseModel):
#     name: str
#     age: int
#     address: str
#     salary: float

# @app.get('/')
# def index():
#     return {'message': '你已经正确创建 FastApi 服务！'}
# # 字符都可以
# @app.get('/query/{uid}')
# def query(uid):
#     msg = f'你查询的 uid 为：{uid}'
#     return {'success': True, 'msg': msg}
# # 限定数字
# @app.get('/query_num/{uid}')
# def query(uid: int):
#     msg = f'你查询的 uid 为：{uid}'
#     return {'success': True, 'msg': msg}

# # psot方法
# @app.post('/insert')
# # def index_post():
# #     return {'message': '你已经正确创建 FastApi 服务！'}
# def insert(people: People):
#     # print(people.age)
#     # mesg="ok"
#     age_after_10_years = people.age + 10
#     msg = f'此人名字叫做：{people.name}，十年后此人年龄：{age_after_10_years}'
#     return {'success': True, 'msg': msg}
# """
# 表单数据使用的“media type”是application/x-www-form-urlencode.但是当表单中包含文件的时候，可以使用multipart/form-data.
# """
# # 使用Form
# @app.post("/login/")
# async def login(*, username: str = Form(...), password: str = Form(...)):
#     return {"username": username,"password": password}

# # 传输文件
# @app.post("/file/")
# async def create_file(file: bytes = File(...)):
#     return {"file_size": len(file)}

# # 使用UpliadFile定义File参数
# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile = File(...)):
#     return {"filename": file.filename}

# # 多文件上传
# @app.post("/files/")
# # async def create_files(files: List[bytes] = File(...)):
# async def create_files(files: List[bytes] = File(...)):
#     return {"file_sizes": [len(file) for file in files]}


# 使用UpliadFile定义File参数
@app.post("/video2audio/")
async def video2audio(video_path: UploadFile = File(...)):

    outpath = video2audio_removeNoise(video_path.filename)
    print(outpath)
    return {"audio_filename": outpath}

# @app.post("/uploadfiles/")
# async def create_upload_files(files: List[UploadFile] = File(...)):
#     return {"filenames": [file.filename for file in files]}


# @app.get("/multifile")
# async def main():
#     content = """
# <body>
# <form action="/files/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
# <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
# </body>
#     """
#     return HTMLResponse(content=content)
