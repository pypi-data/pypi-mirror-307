import sys
import re

from .xwriter import *
from .xreader import *
from datasets import load_dataset

"""
    训练文件格式转化工具，所有的jsonl、json、excel都是微调的格式

    1. jsonl 转化为 excel
    2. json 转化为 excel
    3. excel 转化为 jsonl
    4. json 转化为 jsonl
    5. jsonl 转化为 json
    6. sharegpt 转化为 message
    7. message 转化为 sharegpt
    8. parquet 转化为 sharegpt
    9. parquet 转化为 dpo
"""

# method1: jsonl 转化为 excel
def jsonl_to_excel(input_file, output_file):
    all_lst = jsonl_reader_lst(input_file)
    system_lst = []
    prompt_lst = []
    output_lst = []

    for line in all_lst:
        system  = line.get('instruction', '')
        human = line['input']
        output = line['output']

        system_lst.append(system)
        prompt_lst.append(human)
        output_lst.append(output)
    
    dic = {
        "system": system_lst,
        "prompt": prompt_lst,
        "answer": output_lst,
    }

    excel_writer_dic(output_file, dic)

# method2: json 转化为 excel
def json_to_excel(input_file, output_file):
    all_lst = json_reader_lst(input_file)
    prompt_lst = []
    output_lst = []

    for line in all_lst:
        human = line['conversations'][0]['value']
        output = line['conversations'][1]['value']

        prompt_lst.append(human)
        output_lst.append(output)
    
    dic = {
        "prompt": prompt_lst,
        "answer": output_lst,
    }

    excel_writer_dic(output_file, dic)

# method3: excel 转化为 jsonl
def excel_to_jsonl(input_file, output_file):
    all_lst = excel_reader_dic(input_file)
    try:
        instruct_lst = all_lst['instruction']
        input_lst = all_lst['input']
        output_lst = all_lst['output']
    except:
        instruct_lst = [""] * len(input_lst)
        input_lst = all_lst['prompt']
        output_lst = all_lst['answer']

    res = []
    for i in range(len(input_lst)):
        res.append({"instruction":instruct_lst[i], "input":input_lst[i], "output":output_lst[i]})

    jsonl_writer_lst(output_file, res)

# method4: json 转化为 jsonl
def json_to_jsonl(input_file, output_file):
    all_lst = json_reader_lst(input_file)
    ##将vicuna格式转化为gpt4格式
    res = []
    for line in all_lst:
        human = line['conversations'][0]['value']
        gpt = line['conversations'][1]['value']
        res.append({"instruction":human, "input":"", "output":gpt})
    jsonl_writer_lst(output_file, res)

# method5: jsonl 转化为 json
def jsonl_to_json(input_file, output_file):
    input_lsts = jsonl_reader_lst(input_file)
    res = []
    idx = 1
    for line in  input_lsts:
        prompt = line['input']
        output = line['output']

        res.append({
            "id": idx,
            "conversations":[
                {"from":"human","value":prompt},
                {"from":"gpt","value":output}
            ]
        })
        idx +=1
    jsonl_writer_lst(output_file, res)

# method6: sharegpt 转化为 message
def sharegpt_to_message(input_file, output_file):
    """
        sharegpt 转化为 message格式
    """

    input_lst = json_reader_lst(input_file)
    res = []
    for line in input_lst:
        messages = [
            {"role": "user", "content": line['conversations'][0]['value']},
            {"role": "assistant", "content": line['conversations'][1]['value']},
        ]

        res.append({
            "messages": messages,
            "source": ""
        })

    json_writer_lst(output_file, res)

# method7: message 转化为 sharegpt
def message_to_sharegpt(input_file, output_file):
    """
        message 转化为sharegpt的格式
    """
    input_lst = json_reader_lst(input_file)
    res = []
    for i, conv in enumerate(input_lst):
        cur_data = []
        for role in conv['messages']:
            if role['role'] == "system":
                cur_data.append({
                    "from":"system",
                    "value": role['content']
                })
            elif role['role'] == "user":
                cur_data.append({
                    "from": "human",
                    "value": role['content']
                })
            elif role['role'] == "assistant":
                cur_data.append({
                    "from": "gpt",
                    "value": role['content']
                })
        res.append({
            "id": i,
            "conversations":cur_data
        })

    json_writer_lst(output_file, res)

# method8: sharegpt 转化为 parquet
def parquet_to_sharegpt(input_file, output_file):
    """
        parquet 转化为 sharegpt
    """
    datas = load_dataset(input_file)['messages']

    res = []
    for i, conv in enumerate(datas):
        cur_data = []
        for role in conv:
            if role['role'] == "system":
                cur_data.append({
                    "from":"system",
                    "value": role['content']
                })
            elif role['role'] == "user":
                cur_data.append({
                    "from": "human",
                    "value": role['content']
                })
            elif role['role'] == "assistant":
                cur_data.append({
                    "from": "gpt",
                    "value": role['content']
                })
        res.append({
            "id": i,
            "conversations":cur_data
        })

    json_writer_lst(output_file, res)

# method9: parquet 转化为 dpo
def parquet_to_dpo(input_file, output_file):
    """
        parquet 转化为dpo格式
    """
    datas = load_dataset(input_file)['train']
    res = []
    for line in datas:
        t_res = {}
        t_res['conversations'] = [{
            "from": "human",
            "value": line['chosen'][0]['content']
        }]

        t_res['chosen'] = {
            "from": "gpt",
            "value": line['chosen'][1]['content']
        }

        t_res['rejected'] = {
            "from": "gpt",
            "value": line['rejected'][1]['content']
        }

        res.append(t_res)

    json_writer_lst(output_file, res)





    
