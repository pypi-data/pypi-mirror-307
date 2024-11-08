import json
import pandas as pd
import sys
from .xreader import *
from .xwriter import *

"""
合并文件工具
"""

def txt_merged_lst(output_file, input_files):
	res = []
	for i, arg in enumerate(input_files):
		lst = txt_reader_lst(arg)
		res.extend(lst)
	txt_writer_lst(output_file, res)
	

def jsonl_merged_lst(output_file, input_files):
	res = []
	for i, arg in enumerate(input_files):
		lst = jsonl_reader_lst(arg)
		res.extend(lst)
	jsonl_reader_lst(output_file, res)

def json_merged_lst(output_file, input_files):
	res = []
	for i, arg in enumerate(input_files):
		lst = json_reader_lst(arg)
		res.extend(lst)
	json_writer_lst(output_file, res)
	

def excel_merged_dic(output_file, input_files, sheet_name="Sheet1"):
	dic_lst = []
	for i, arg in enumerate(input_files):
		dic = excel_reader_dic(arg, sheet_name)
		dic_lst.append(dic)

	dic_res = dic_lst[0]
	for dic in dic_lst[1:]:
		for key,value in dic.items():
			dic_res[key] += value
	excel_writer_dic(output_file, dic_res)

def csv_merged_dic(output_file, input_files):
	dic_lst = []
	for i, arg in enumerate(input_files):
		dic = csv_reader_dic(arg)
		dic_lst.append(dic)

	dic_res = dic_lst[0]
	for dic in dic_lst[1:]:
		for key,value in dic.items():
			dic_res[key] += value
	csv_writer_dic(output_file, dic_res)

def parquet_merged_dic(output_file, input_files):
	dic_lst = []
	for i, arg in enumerate(input_files):
		dic = parquet_reader_dic(arg)
		dic_lst.append(dic)

	dic_res = dic_lst[0]
	for dic in dic_lst[1:]:
		for key,value in dic.items():
			dic_res[key] += value
	parquet_writer_dic(output_file, dic_res)