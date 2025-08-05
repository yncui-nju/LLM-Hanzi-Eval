import json
import re
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.utils import call_llm, extract_chinese_chars

def extract_title_character(title):
    match = re.search(r'([\u4e00-\u9fff])', title)
    return match.group(1) if match else None

def contains_irrelevant_chars(title_char, char_list):
    if len(char_list) < 3:
        print("× 项目太少")
        return True

    for char in char_list:
        if char == title_char:
            continue
        if len(char) != 1 or not (re.match(r'^[\u4e00-\u9fff]$', char) or char == '→'):
            print(f"× 异常字符: {char}")
            return True

    return False


def generate_question_answer_pairs(input_file, output_file, api_key):
    with open(input_file, "r", encoding='utf-8') as f:
        keywords = json.load(f)

    question_answer_pairs = {}
    skipped_entries = []

    for title_char in keywords:
        print(f"\n处理条目: {title_char}")

        if not title_char or not re.search(r'[\u4e00-\u9fff]', title_char):
            print("跳过: 无有效汉字")
            skipped_entries.append(title_char)
            continue

        print(f"目标字: {title_char}")

        prompt = f"""
        # 汉字结构解析任务

        ## 目标汉字: {title_char}

        你是一位汉字结构分析专家。请严格根据以下要求解析目标汉字“{title_char}”，列出它的组成部件或可独立成字的结构性子部件。输出结果必须完全符合以下规则。

        ## 输出规则：
        1. 所有输出必须是“{title_char}”的组成部分，可作为独立汉字存在。
        2. 输出中必须包含“{title_char}”本身。
        3. 不允许包含联想词、近义字或无关字（例如“勺”、“扑”、“芯”等）。
        4. 所有汉字必须是常用字。
        5. 输出用顿号（、）分隔。
        6. 请尽可能多地列出所有结构性、构形上合理、可独立成字的常用组成字，不要遗漏。
        7. 输出不要求固定数量，数量可以多，但必须准确，不能乱联想。

        ## 错误示例：
        错误: “一” → ['一','十','八','勺','芍','芯']（错误字: 勺、芍、芯）
        错误: “找” → ['找','扎','扑','打','扒']（错误字: 扎、扑、打、扒）

        ## 正确示例：
        葱 → 匆、心、芯、葱
        积 → 八、口、只、和、禾、积

        请严格分析并输出“{title_char}”的结构性汉字：
        """

        try:
            response = call_llm(prompt, api_key)
            print(f"模型响应: {response}")
            char_list = extract_chinese_chars(response)
            print("解析结果：", "、".join(char_list))

            if title_char in char_list and not contains_irrelevant_chars(title_char, char_list):
                question_answer_pairs[title_char] = char_list
                print("√ 验证通过")
            else:
                print("× 验证失败")
                skipped_entries.append(title_char)

        except Exception as e:
            print(f"调用失败: {str(e)}")
            skipped_entries.append(title_char)

    with open(output_file, "w", encoding='utf-8') as f:
        json.dump(question_answer_pairs, f, ensure_ascii=False, indent=4)

    print(f"\n完成: 成功解析 {len(question_answer_pairs)} 个条目，跳过 {len(skipped_entries)} 个。")


if __name__ == "__main__":
    input_file = "keywords_only.json"
    output_file = "qwen_answers_3.json"
    api_key = ""
    generate_question_answer_pairs(input_file, output_file, api_key)
