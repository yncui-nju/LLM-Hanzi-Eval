import numpy as np
import matplotlib.pyplot as plt

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 数据 - 请替换为您的实际数据
data = {
    '纯问题提示词': [0.7836,0.5558,0.6503],
    '问题+CoT提示词': [0.5876,0.6351,0.6104],
    '问题+举例提示词': [0.5628,0.6212,0.5906]
}

# 创建图形
fig, ax = plt.subplots(figsize=(10, 6))

# 设置柱状图参数
bar_width = 0.25
index = np.arange(len(data))
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # 蓝、橙、绿
metrics = ['Precision', 'Recall', 'F1-Score']

# 绘制柱状图
for i, metric in enumerate(metrics):
    position = index + i * bar_width
    values = [data[model][i] for model in data]
    ax.bar(position, values, bar_width,
           label=metric,
           color=colors[i],
           edgecolor='grey')

# 添加图表元素
ax.set_xlabel('Doubao', fontsize=12)
ax.set_ylabel('得分', fontsize=12)
ax.set_title('Prompt性能对比 (Precision/Recall/F1-Score)', fontsize=14, pad=20)
ax.set_xticks(index + bar_width)
ax.set_xticklabels(list(data.keys()))
ax.legend(loc='upper right', framealpha=0.9)
ax.grid(axis='y', linestyle='--', alpha=0.7)

# 设置y轴范围
ax.set_ylim(0, 1.0)

# 在柱子上方显示数值
for i, model in enumerate(data):
    for j, value in enumerate(data[model]):
        ax.text(i + j*bar_width, value + 0.01, f'{value:.3f}',
                ha='center', va='bottom', fontsize=9)

# 调整布局并保存为图片
plt.tight_layout()
output_path = "Prompt性能对比_3.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"图表已保存至: {output_path}")

# 清理内存
plt.close(fig)