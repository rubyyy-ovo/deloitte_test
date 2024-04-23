import json

def extract_and_format_table(json_file, target_text):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    extracted_data = []
    # 遍历JSON数据中的所有表格
    for entry in data:
        if "018.png" in entry:
            tables = data[entry][0]['result']['tables']
            target_table_index = None
            for index, table in enumerate(tables):
                # 检查表格的标题或行中是否含有目标文本
                if any(target_text in line['text'] for line in table['lines']):
                    target_table_index = index
                    # 提取单位信息
                    unit = next((line['text'] for line in table['lines'] if "单位:" in line['text']), "单位信息未提供")
                    break

            if target_table_index is not None and target_table_index + 1 < len(tables):
                # 获取目标文本表格的下一个表格
                header_table = tables[target_table_index + 1]
                # 提取表头信息
                headers = [cell['text'] for cell in header_table['table_cells'] if cell['start_row'] == 0]
                # # 提取关键索引
                key_indices = [
                    cell['text'] for cell in header_table['table_cells']
                    if cell['start_row'] == cell['end_row'] and cell['start_col'] == 0 and cell['start_row'] != 0
                ]

                # 按行收集数据
                values = []
                for row in range(1, header_table['table_rows']):
                    row_values = [cell['text'] for cell in header_table['table_cells'] 
                                  if cell['start_row'] == row and cell['start_col'] != 0
                    ]
                    values.append(row_values)
                extracted_data.append({
                    'title': target_text,
                    'unit': unit,
                    'header': headers,
                    'key_index': key_indices,
                    'values': values
                })
        if "019.png" in entry and extracted_data:
            # 使用019.png中的数据来更新018.png中的结果
            tables = data[entry][0]['result']['tables']
            header_table = tables[1]
            key_indices_019 = [
                cell['text'] for cell in header_table['table_cells']
                if cell['start_row'] == cell['end_row'] and cell['start_col'] == 0 and cell['start_row'] != 0
            ]
            values_019 = []
            for row in range(1, header_table['table_rows']):
                row_values = [cell['text'] for cell in header_table['table_cells'] 
                              if cell['start_row'] == row and cell['start_col'] != 0]
                values_019.append(row_values)

            # 更新最后添加的字典元素
            last_entry = extracted_data[-1]
            last_entry['key_index'].extend(key_indices_019)
            last_entry['values'].extend(values_019)
    return extracted_data

# 调用函数并指定文件路径和目标文本
file_path = 'annual_report.json'
target_text = '1.利润表及现金流量表相关科目变动分析表'
tables = extract_and_format_table(file_path, target_text)

# 打印提取的表格数据
for table in tables:
    print(table)