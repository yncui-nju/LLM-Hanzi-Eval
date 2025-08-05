import requests
from bs4 import BeautifulSoup
import json
import os
import time
import random


def scrape_hanzi_data(base_url, output_file, pages_to_scrape, keyword, count):
    """爬取百度知道数据并保存为JSON"""
    # 创建输出目录
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://zhidao.baidu.com/'
    }

    all_questions = {}

    for page in range(pages_to_scrape):
        url = f"{base_url}&pn={page * 10}"
        try:
            time.sleep(random.uniform(2, 4))

            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()

            # 自动检测编码
            response.encoding = response.apparent_encoding
            soup = BeautifulSoup(response.text, 'html.parser')

            # 使用精确的CSS选择器
            questions = soup.select('dt.dt.mb-3.line')
            answers = soup.select('dd.dd.answer')

            # 调试信息
            if not questions or not answers:
                print(f"第{page + 1}页未找到问题/答案元素，保存调试文件")
                with open(f"debug_page_{page}.html", "w", encoding="utf-8") as f:
                    f.write(response.text)
                continue

            # 验证问题和答案数量匹配
            if len(questions) != len(answers):
                print(f"警告：第{page + 1}页问题和答案数量不匹配，问题数:{len(questions)}，答案数:{len(answers)}")

            # 配对处理问题和答案
            for dt, dd in zip(questions, answers):
                question_text = dt.get_text(strip=True)
                answer_text = dd.get_text(strip=True)

                # 关键词过滤
                if keyword in question_text:
                    # 优化文本清洗（移除多余空白和换行）
                    clean_question = ' '.join(question_text.split())
                    clean_answer = ' '.join(answer_text.split())
                    all_questions[clean_question] = clean_answer

            print(f"成功爬取第{page + 1}页，新增 {len(all_questions)} 个问题")

        except Exception as e:
            print(f"爬取第{page + 1}页失败: {str(e)}")
            if 'response' in locals():
                print(f"状态码: {response.status_code}")
                print(f"响应片段: {response.text[:500]}")

    # 保存结果
    with open(output_file, "w", encoding='utf-8') as f:
        json.dump(all_questions, f, ensure_ascii=False, indent=2)

    print(f"总共成功爬取 {len(all_questions)} 个问题，已保存至 {output_file}")


if __name__ == "__main__":
    base_url = "https://zhidao.baidu.com/search?&fr=search&dyTabStr=null&word=%E5%AD%97%E6%8B%86%E5%B8%B8%E7%94%A8%E5%AD%97%3F"
    output_file = "../raw_questions_1.json"
    keywords = ["拆"]

    for count, keyword in enumerate(keywords):
        scrape_hanzi_data(base_url, output_file, 50, keyword, count)