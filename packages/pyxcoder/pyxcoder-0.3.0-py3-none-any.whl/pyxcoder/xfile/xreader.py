import json
import pandas as pd
import sys

"""
读文件工具
"""

def txt_reader_lst(input_file):
    res = []
    with open(input_file,"r",encoding= "utf-8") as fp:
        for line in fp:
            res.append(line.strip())
    return res

def jsonl_reader_lst(input_file):
    res = []
    with open(input_file,"r") as fp:
        for line in fp:
            res.append(json.loads(line)) 
    return res

def json_reader_lst(input_file):
    res = []
    with open(input_file,"r") as fp:
        res = json.load(fp)
    return res


def excel_reader_dic(input_file,sheet_name="Sheet1"):
    res = {}
    df = pd.read_excel(input_file,sheet_name=sheet_name,keep_default_na=False)
    title_lst = df.columns
    for i in title_lst:
        res[i] = df[i].tolist()
    return res

def csv_reader_dic(input_file):
    res = {}
    df = pd.read_csv(input_file,sep=",",keep_default_na=False)
    title_lst = df.columns
    for i in title_lst:
        res[i] = df[i].tolist()
    return res

def parquet_reader_dic(input_file):
    res = {}
    df = pd.read_parquet(input_file)
    title_lst = df.columns
    for i in title_lst:
        res[i] = df[i].tolist()
    return res
