'''
Author: LiuSheng
Date: 2025-02-10 17:34:28
LastEditTime: 2025-02-10 17:55:26
Description: 
'''
import json
import pickle
import msgpack


# Open a file and use dump() 
with open('/home/liusheng/worksapce2024/Projects/RadiSmart/input.pkl', 'rb') as file: 
    # A new file will be created 
    input_dict = pickle.load(file) 
    
input_dict.keys(), type(input_dict)



# input_dict['Rest']['Image']['Data'] = None
# input_dict['Rest']['Image']['Data'] = None
# msgpack_data = msgpack.packb(input_dict)
# data_dict = msgpack.unpackb(msgpack_data, raw=False)

def print_type_recursive(data, indent=0):
    # 创建当前缩进的前缀
    indent_prefix = ' ' * indent

    if isinstance(data, dict):
        for key, value in data.items():
            # 打印键和类型，并递归处理值
            print(f"{indent_prefix}Key: {key}, Type: {type(value)}")
            print_type_recursive(value, indent + 4)  # 增加缩进
    elif isinstance(data, list):
        for item in data:
            # 打印列表项和类型，并递归处理
            print(f"{indent_prefix}Value: {item}, Type: {type(item)}")
            print_type_recursive(item, indent + 4)  # 增加缩进
    else:
        # 打印基本类型的值和类型
        # print(f"{indent_prefix}Value: {data}, Type: {type(data)}")
        print(f"{indent_prefix}Value: xxxxxx{0}, Type: {type(data)}")


input_dict['Rest']['Image']['Data'] = None
input_dict['Stress']['Image']['Data'] = None
# input_dict['Rest']['ROIInfo'] = None
# input_dict['Stress']['ROIInfo'] = None
# 调用递归函数
print_type_recursive(input_dict)



# print(input_dict)

print(json.dumps(input_dict, indent=4))