from .xmerged import *
from .xconvert import *

"""
操作文件工具 
"""

class FileMerger:
    def __init__(self, input_file="", output_file=""):
        """
            初始化文件合并器
            :param input_file: 输入文件路径 
            :param output_file: 输出文件路径
        """
        self.input_file = input_file
        self.output_file = output_file
    
    def reader(self):
        """
            读取文件
        """
        if self.input_file.endswith(".txt"):
            res = txt_reader_lst(self.input_file)
        elif self.input_file.endswith(".jsonl"):
            res = jsonl_reader_lst(self.input_file)
        elif self.input_file.endswith(".json"):
            res = json_reader_lst(self.input_file)
        elif self.input_file.endswith(".xlsx"):
            res = excel_reader_dic(self.input_file)
        elif self.input_file.endswith(".csv"):
            res = csv_reader_dic(self.input_file)
        elif self.input_file.endswith(".parquet"):
            res = parquet_reader_dic(self.input_file)
        else:
            print("不支持的文件类型")
            sys.exit(1)
        return res
    

    def writer(self, res):
        """
            写入文件
        """
        if self.output_file.endswith(".txt"):
            txt_writer_lst(self.output_file, res)
        elif self.output_file.endswith(".jsonl"):
            jsonl_writer_lst(self.output_file, res)
        elif self.output_file.endswith(".json"):
            json_writer_lst(self.output_file, res)
        elif self.output_file.endswith(".xlsx"):
            excel_writer_dic(self.output_file, res)
        elif self.output_file.endswith(".csv"):
            csv_writer_dic(self.output_file, res)
        elif self.output_file.endswith(".parquet"):
            parquet_writer_dic(self.output_file, res)
        else:
            print("不支持的文件类型")
            sys.exit(1)
    
    def merger(self, input_lsts):
        """
            合并文件
        """
        if not input_lsts or self.output_file == "":
            print("输入文件或输出文件为空")
            sys.exit(1)

        if self.output_file.endswith(".txt"):
           txt_merged_lst(self.output_file, input_lsts)
        elif self.output_file.endswith(".jsonl"):
           jsonl_merged_lst(self.output_file, input_lsts)
        elif self.output_file.endswith(".json"):
           json_merged_lst(self.output_file, input_lsts)
        elif self.output_file.endswith(".xlsx"):
           excel_merged_dic(self.output_file, input_lsts)
        elif self.output_file.endswith(".csv"):
           csv_merged_dic(self.output_file, input_lsts)
        elif self.output_file.endswith(".parquet"):
           parquet_merged_dic(self.output_file, input_lsts)
        else:
            print("不支持的文件类型")
            sys.exit(1)

    def convert(self, method):
        """
            转换文件
        """
        if method == "jsonl2excel":
            jsonl_to_excel(self.input_file, self.output_file)
        elif method == "json2excel":
            json_to_excel(self.input_file, self.output_file)
        elif method == "excel2jsonl":
            excel_to_jsonl(self.input_file, self.output_file)
        elif method == "json2jsonl":
            json_to_jsonl(self.input_file, self.output_file)
        elif method == "jsonl2json":
            jsonl_to_json(self.input_file, self.output_file)
        elif method == "sharegpt2message":
            sharegpt_to_message(self.input_file, self.output_file)
        elif method == "message2sharegpt":
            message_to_sharegpt(self.input_file, self.output_file)   
        elif method == "parquet2sharegpt":
            parquet_to_sharegpt(self.input_file, self.output_file)
        elif method == "parquet2dpo":
            parquet_to_dpo(self.input_file, self.output_file)
        else:
            print("不支持的转换方法")
            sys.exit(1)
        

if __name__ == "__main__":
    input_file = "/cloudide/workspace/pyxcoder/pyxcoder/xfile/test_data/1.jsonl"
    output_file = "/cloudide/workspace/pyxcoder/pyxcoder/xfile/test_data/2.json"

    file_merger = FileMerger(input_file=input_file, output_file=output_file)
    res = file_merger.reader()
    # import pdb;pdb.set_trace()

    # file_merger.writer(res)
    file_merger.convert("jsonl2json")
    print(res, type(res))
