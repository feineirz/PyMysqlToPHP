#! /usr/bin/env python3
import math, os, shutil
from tokenize import String
from pathlib import Path
from mysql_database import *


def prepare_directory_structure(mysql_connector: MySQLConnector):
    Path(str(Path.home())+'/Output/PHP/'+mysql_connector.connection_info.database+'/classes/').mkdir(parents=True, exist_ok=True)
    Path(str(Path.home())+'/Output/JAVA/'+mysql_connector.connection_info.database+'/classes/').mkdir(parents=True, exist_ok=True)
    Path(str(Path.home())+'/Output/PYTHON/'+mysql_connector.connection_info.database+'/classes/').mkdir(parents=True, exist_ok=True)
    Path(str(Path.home())+'/Output/C#/'+mysql_connector.connection_info.database+'/classes/').mkdir(parents=True, exist_ok=True)
    Path(str(Path.home())+'/Output/VB.NET/'+mysql_connector.connection_info.database+'/classes/').mkdir(parents=True, exist_ok=True)
    

def ribbonize(length=70, char='-', content='', tab_count=0, tab_size=4):
    if content == '':
        return char*(length - (tab_size*tab_count))

    elif length > len(content) + 2:
        l_side = int(math.ceil((length - len(content) - (tab_size*tab_count) - 2) / 2))
        r_side = int(math.floor((length - len(content) - (tab_size*tab_count) - 2) / 2))
        return f'{(char*l_side)} {content} {(char * r_side)}'
    else:
        return content


def camel_cap(content):
    parts = content.split('_')
    parts = [x.capitalize() for x in parts]
    return ''.join(parts)


def tab(length=1, tabsize=4):
    return '\t'*(length)


def replace_content(content: str, replace_dict: dict):
    for k, v in replace_dict.items():
        content = content.replace(k, v)
    return content


def readfile(path):
    buff = ''
    with open(path, 'r') as f:
        buff = f.read()

    return buff


def writefile(path, content: str):
    with open(path, 'w') as f:
        f.write(content)


def replace_file_content(path, replace_dict: dict, outpath=None):
    if outpath is None:
        outpath = path
    buff = readfile(path)
    for k,v in replace_dict.items():
        buff = buff.replace(k, v)
    writefile(outpath, buff)


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def db_datatype2php_datatype(db_datatype: str):
    dt_dict = {
        'string': 'char varchar nvarchar tinytext mediumtext text longtext date datetime',
        'integer': 'tinyint int bigint',
        'float': 'decimal'    
    }
    for k,v in dt_dict.items():
        if db_datatype.lower() in v :
            return k
    return 'mixed'
