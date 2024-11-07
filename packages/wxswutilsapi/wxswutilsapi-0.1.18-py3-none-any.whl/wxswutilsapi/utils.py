import ast
import re

import numpy as np

def predict_to_chartdata(data):
    try:
        labels = []
        xs = []
        ys = {}

        # 解析数据
        for entry in data:
            if entry['used'] == '1':
                predict_data = entry['predict']
                if isinstance(predict_data, str):
                    predict_list =  ast.literal_eval(predict_data)
                else:
                    predict_list = predict_data 
                xs.append(entry['time'])  # 记录时间戳
                for predict in predict_list:
                    component = predict['component']
                    value = predict['value']

                    # 添加到labels
                    if component not in labels:
                        labels.append(component)
                        ys[component] = []

                    # 按组件存储数值
                    ys[component].append(value)

        # 构建ys为嵌套数组
        ys_list = [ys[label] for label in labels]

        # 生成最终的结构
        result = {
            'labels': labels,
            'xs': xs,
            'ys': ys_list
        }

        return result
    except Exception as e:
        raise ValueError(f"Unexpected error in predict_to_chartdata:{str(e)}") from e
        
def predict_average(data,resultIsObject = False):
    try:
        # 初始化用于存储每个物质的值
        values = {}

        # 解析数据
        for entry in data:
            if entry['used'] == '1':
                predict_data = entry['predict']
                # 检查 predict_data 是否为字符串，如果是则转换
                if isinstance(predict_data, str):
                    predict_list = ast.literal_eval(predict_data)
                else:
                    predict_list = predict_data 
                for predict in predict_list:
                    component = predict['component']
                    value = predict['value']

                    # 如果物质还没有出现在values中，初始化为空列表
                    if component not in values:
                        values[component] = []

                    # 将该物质的值添加到列表中
                    values[component].append(value)

        average_result = None
        # 计算去掉两个最大和两个最小值后的平均值
        if resultIsObject is False:
            average_result = []
        else:
            average_result = {}

        for component, component_values in values.items():
            # 对该物质的值进行排序
            sorted_values = sorted(component_values)

            # 确保有足够的值去掉两个最大和两个最小
            if len(sorted_values) > 4:
                trimmed_values = sorted_values[2:-2]  # 去掉两个最大和两个最小
            else:
                trimmed_values = sorted_values  # 如果值不足 4 个，不做裁剪

            # 计算平均值
            avg_value = np.mean(trimmed_values)
            if resultIsObject is False:
                average_result.append({'component': component, 'value': avg_value})
            else:
                average_result[component] = avg_value

        return average_result
    except Exception as e:
        raise ValueError(f"Unexpected error in predict_average:{str(e)}") from e
    
def is_number(value):
    try:
        if isinstance(value, (int, float)):
            return True
        if isinstance(value, str):
            # 使用正则表达式检查是否为数字
            return bool(re.match(r'^-?\d+(\.\d+)?$', value))
        return False
    except Exception as e:
        raise ValueError(f"Unexpected error in is_number:{str(e)}") from e