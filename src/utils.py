import re
import time
import json
import os
from openai import OpenAI

def call_llm(llm_name, input_text, api_key):
    if llm_name == "deepseek":
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        completion = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": input_text}],
            max_tokens=100
        )
        return completion.choices[0].message.content.strip()

    elif llm_name == "qwen":
        client = OpenAI(api_key=api_key, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
        completion = client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": input_text}
            ],
            max_tokens=100
        )
        return completion.choices[0].message.content.strip()

    elif llm_name == "doubao":
        client = OpenAI(api_key=api_key, base_url="https://ark.cn-beijing.volces.com/api/v3")
        completion = client.chat.completions.create(
            model="doubao-seed-1-6-thinking-250715",
            messages=[{"role": "user", "content": input_text}],
            max_tokens=100
        )
        return completion.choices[0].message.content.strip()

    else:
        raise ValueError(f"Unsupported model: {llm_name}")

import re

def extract_chinese_chars(response):
    """
    提取字符串中的所有中文字符（去重、保序）。
    特殊处理了包含箭头 →、顿号 、 等符号的情形。

    参数：
        response (str): 原始文本（如 LLM 输出）

    返回：
        List[str]: 提取出的汉字字符列表，已去重且保持顺序
    """
    # 尝试匹配一段包含中文字符、顿号、箭头、空格的文本
    match = re.search(r'[:：]?\s*([\u4e00-\u9fff、→\s]+)', response)
    if match:
        candidates = match.group(1)

        allowed_chars = set(chr(i) for i in range(0x4E00, 0x9FFF + 1))  # 中文区间
        allowed_chars.add('→')  # 箭头先保留用于辅助处理

        temp_chars = [char for char in candidates if char in allowed_chars]
        char_list = [char for char in temp_chars if char != '→']  # 去掉箭头
    else:
        # fallback 只提纯汉字
        char_list = [char for char in response if '\u4e00' <= char <= '\u9fff']

    # 去重同时保持顺序
    seen = set()
    return [char for char in char_list if char not in seen and not seen.add(char)]
