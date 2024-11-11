
import pandas as pd
import numpy as np
import json
import re
from icecream import ic
from pprint import  pprint
import os
from tqdm import tqdm

#读取xlsx所有sheetde
def load_all_sheet(path):
    path = path
    excel_file = pd.ExcelFile(path)
    sheet_names=excel_file.sheet_names
    print("所有工作表名称:", excel_file.sheet_names)
    dfs = {sheet_name: excel_file.parse(sheet_name) for sheet_name in excel_file.sheet_names}
    return sheet_names,dfs

import uuid
import os
import hashlib

def walk_dict(dirpath):
    '''
    [{  'id_': 'fa870abf-0c8b-55cd-9094-952bdc919c9e',
        'root': 'C:\\Users\\nlp\\代码',
        'file_name': 'chroma.log',
        'file_path': 'C:\\Users\\nlp\\代码\\chroma.log',
        'file_name_prefix': 'chroma',
        'file_name_suffix': '.log',
        'file_size': 3609,
        'file_modtime': 1721670101.1296072,
        'file_create_time': 1721871742.289491,
        'file_access_time': 1721985205.3720908,
        'file_permissions': 33206},
    '''
    # root=r'C:\Users\nlp\Desktop\工作文件\course_code_kp匹配\Econometrics-lecture note'
    # os.listdir(root)
    file_paths_jsonl=[]
    for root,dirs,visited_file_names in os.walk(dirpath):
        for file_name in visited_file_names:
            dict={"id_":'0-0-0-0-0',"root":'',"file_name":'',"file_path":'',"file_name_prefix":'','file_name_suffix':'',
                  "file_size":0,"file_modtime":0.0,"file_create_time":0.0,"file_access_time":0.0,"file_permissions":0}
            #if root is relative path, also get the absolute file path
            file_path=os.path.join(os.path.abspath(root),file_name)
            dict['root']=root
            dict['file_name']=file_name
            dict['file_path']=file_path
            
            try:
                stat = os.stat(file_path)
                file_size = stat.st_size
                last_modified_time = stat.st_mtime
                unique_string = f"{file_path}-{file_size}-{last_modified_time}"
                hash_object = hashlib.sha256(unique_string.encode())
                file_hash = hash_object.hexdigest()
                file_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, file_hash)
                dict['id_']=str(file_uuid)
            except Exception as e:
                ic(f'error while generate file uuid')
            
            try:
                file_stats = os.stat(file_path)
                file_size = file_stats.st_size
                dict['file_size']=file_size
                mod_time = file_stats.st_mtime
                # mod_time_human_readable = time.ctime(mod_time)
                dict['file_modtime']=mod_time
                creation_time = file_stats.st_ctime
                # creation_time_human_readable = time.ctime(creation_time)
                dict['file_create_time']=creation_time
                access_time = file_stats.st_atime
                # access_time_human_readable = time.ctime(access_time)
                dict['file_access_time']=access_time
                file_permissions = file_stats.st_mode
                # file_permissions = oct(file_stats.st_mode & 0o777)
                dict['file_permissions']=file_permissions
            except Exception as e:
                ic(f'when get file meta error:{e}')
                
            try:
                for i in range(len(file_name)-1,-1,-1):
                    # print(string1[i])
                    if file_name[i]=='.':
                        dict['file_name_prefix']=file_name[:i]
                        dict['file_name_suffix']=file_name[i:]
                        break
                # prefix=re.findall(r'(.*)\..*',file_name)[0]
                # suffix=re.findall(r'\..*',file_name)[0]
                # dict['file_name_prefix']=prefix
                # dict['file_name_suffix']=suffix
            except Exception as e:
                # dict['file_name_prefix']='error when parse prefix'
                # dict['file_name_suffix']='error when parse suffix'
                print(f'在解析{file_name}前后缀时报错了{e}')

            file_paths_jsonl.append(dict)
    
    return file_paths_jsonl

def dump_json(obj, fp, encoding='utf-8', indent=4, ensure_ascii=False):
    with open(fp, 'w', encoding=encoding) as fout:
        json.dump(obj, fout, indent=indent, ensure_ascii=ensure_ascii)

def load_json(fp, encoding='utf-8'):
    with open(fp, encoding=encoding) as fin:
        return json.load(fin)
    
def get_global_var_name(var):
    # Check global variables
    global_vars = globals()
    for name, value in global_vars.items():
        if value is var:
            return name
    return None
from datetime import datetime
def jsonl_dump(fp,obj,mode='a',ensure_ascii=False):
    while True:
        try:
            with open(fp, mode,encoding='utf8') as file:
                if isinstance(obj,list):
                    for item in obj:    
                        item['dump_time']=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        json_line = json.dumps(item,ensure_ascii=ensure_ascii)  # Convert the dictionary to a JSON string
                        file.write(json_line + '\n')  # Write the JSON string followed by a newline
                elif isinstance(obj,dict):
                    obj['dump_time']=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    json_line=json.dumps(obj,ensure_ascii=ensure_ascii)
                    file.write(json_line+'\n')
                elif hasattr(obj,'__str__'):
                    dump_dict={'dump_time':datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'obj_name':get_global_var_name(obj),'obj_type':str(type(obj)),"str":obj.__str__()}
                    json_line=json.dumps(dump_dict,ensure_ascii=ensure_ascii)
                    file.write(json_line+'\n')
        except OSError as e:
            print(f'error when open file:{e},sleep try to dump')
            time.sleep(1)
            continue
        except Exception as e:
            raise e
        break


def jsonl_load(fp, encoding='utf-8'):
    jsonl=[]
    with open(fp, encoding='utf-8') as f :
        for line in f:
            jsonl.append(json.loads(line))
    return jsonl

import tika
tika.initVM()
from tika import parser
os.environ['TIKA_SERVER_JAR']='./tika-server.jar'
def tikaread_filepaths_content(filepath):
    ic(filepath)
    try:
        parsed = parser.from_file(filepath)
        return parsed['content']
    except Exception as e:
        print('error when tika read file content')
        return ''

def read_text_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print('error when read text file content')
        return ''

def read_filepaths_content(filepaths):
    """"
    [{  "filepath":filepath,
        'filecontent':content}]
    """
    from pathlib import Path
    from openai import OpenAI
    client = OpenAI(
        api_key = "sk-BShsfsRpa3tzOI1P8xbU35FnHc1Hk5al2sQHMskd3QSc7o9R",
        base_url = "https://api.moonshot.cn/v1",
    )

    def readfile(filepath):
        file_content=''
        try:
            file_object = client.files.create(file=Path(filepath), purpose="file-extract")
            file_content = client.files.content(file_id=file_object.id).text
        except Exception as e:
            print(e)
        return file_content

    file_content_jsonl=[]
    for filepath in tqdm(filepaths):
        content='error when reader file content'
        try:
            content=readfile(filepath)
            content=json.loads(content)
            content=content['content']
        except Exception as e:
            print('error when reader file content')
            print(e)
            
        file_content_jsonl.append({'filepath':filepath,'filecontent':content})
    return file_content_jsonl
    


import tempfile
import zipfile
def unzip(zip_path):
    '''
    解压缩到临时文件夹, 不带压缩包名
    '''
    temp_dir = tempfile.mkdtemp()  # 创建临时文件夹
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    return temp_dir