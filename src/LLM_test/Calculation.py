import json

# 读取文件一和文件二，指定编码为UTF-8
with open('qwen_answers_3.json', 'r', encoding='utf-8') as file1:
    answers = json.load(file1)

with open('processed_questions.json', 'r', encoding='utf-8') as file2:
    processed_answers = json.load(file2)

# 初始化计数器
true_positives = 0
false_positives = 0
false_negatives = 0

# 验证文件二的答案是否存在于文件一中
for key in answers.keys():
    correct_values = set(answers[key])
    predicted_values = set(processed_answers.get(key, []))

    true_positives += len(correct_values & predicted_values)
    false_negatives += len(predicted_values - correct_values)
    false_positives += len(correct_values - predicted_values)

# 计算Precision, Recall, F1-score
precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

# 准备结果字典
results = {
    "Precision": precision,
    "Recall": recall,
    "F1-score": f1_score
}

# 将结果输出到Result_1文件中，指定编码为UTF-8
with open('qwen_Result_3', 'w', encoding='utf-8') as result_file:
    json.dump(results, result_file, indent=4)

print("验证完成，结果已保存到Result_3文件中")