import json
import re
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils import call_llm

def get_first_chinese_char(s):
    """获取字符串中的第一个汉字"""
    for c in s:
        if '\u4e00' <= c <= '\u9fff':
            return c
    raise ValueError(f"字符串中没有汉字：{s}")


def parse_response(response):
    """解析模型返回的文本，提取汉字列表"""
    response = response.strip()

    # 去除可能的前缀（如"答案："）
    if "答案：" in response:
        response = response.split("答案：", 1)[-1]

    # 使用正则表达式提取汉字
    words = re.findall(r'[\u4e00-\u9fa5]+', response)
    # 去除重复项并排序
    return sorted(list(set(words)), key=lambda x: (len(x), x))


def process_questions(input_path, output_path, api_key):
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("输入文件不存在")

    processed = {}

    for question_key, answer in raw_data.items():
        try:
            # 直接取键中的第一个汉字作为题目字
            title_char = get_first_chinese_char(question_key)

            # 构造提示模板（简化版）
            prompt = (
            f"你是一个经验丰富的汉语言专家，"
            f"现在需要根据用户提供的问题，从原始答案中提取所有找到的汉字，"
            f"如果发现问题中的汉字不由原始答案组成，试图从原始答案分析出问题的汉字并替换，"
            f"如果发现问题和答案的冗余部分，将冗余部分全部去除，"
            f"如果发现问题字不由原始答案的字组成，则分析出问题字由哪些汉字组成，并作为原始答案输出例如：甲找出16个字为：一，二，三，四，五，六，七...，此时你发现甲不由这些字组成，你将甲,田,日,口,山,王,干,工,土,上,下,一,二,三,十作为原始答案输出"
            f"仅返回问题和单个汉字，顿号分割的汉字列表，例如问题：甲，答案：甲,田,日,口,山,王,干,工,土,上,下,一,二,三,十"
            f"问题：{question_key}\n"
            f"原始答案：{answer}"
            )

            # 调用模型获取响应
            response = call_llm("deepseek", prompt, api_key)

            # 解析结果并存储
            word_list = parse_response(response)
            processed[title_char] = word_list

        except Exception as e:
            print(f"处理键'{question_key}'时出错：{str(e)}")

    # 保存结果
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(processed, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # 配置参数
    API_KEY = ""  # 需替换为有效API密钥
    INPUT_FILE = "processed_questions.json"  # 输入文件路径
    OUTPUT_FILE = "llm_answers.json"  # 输出文件路径

    process_questions(INPUT_FILE, OUTPUT_FILE, API_KEY)
