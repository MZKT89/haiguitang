from scipy.stats import spearmanr
import numpy as np

# 假设result1和result2是两个评测结果列表（可以是布尔型或转换为数值型）
# result1 = [1, 0, 0]
# result2 = [1, 0, 1]

# correlation, p_value = spearmanr(result1, result2)
# print(correlation)

ai_access_result = ['True', 'False', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'False', 'True', 'False', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'False', 'True', 'False', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'False', 'True', 'True', 'True', 'True', 'True', 'False', 'True', 'False', 'False', 'True', 'True', 'False', 'True', 'True', 'True', 'True', 'False', 'True', 'True', 'True', 'True', 'True', 'True', 'False', 'True', 'True', 'True', 'True', 'True', 'False', 'True', 'True', 'True', 'False', 'False', 'True', 'True', 'False', 'False', 'False', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'False', 'False', 'True', 'True', 'True', 'True', 'True', 'False', 'False', 'True', 'True', 'True', 'True', 'True']
ai_access_result = ['True', 'False', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'False', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'False', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'False', 'True', 'True', 'False', 'True', 'True', 'True', 'True', 'True', 'False', 'False', 'True', 'True', 'False', 'False', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'False', 'False', 'True', 'True', 'True', 'True', 'True', 'False', 'False', 'True', 'True', 'True', 'True', 'True']
print(sum([1 if i=='True' else 0 for i in ai_access_result]))

ai_access_result = [1 if i=='True' else 0 for i in ai_access_result]

human_wrong = [4, 6, 8, 30, 34, 43, 67, 73, 85, 86, 90, 91, 94, 95, 96, 99]
# 找到最大索引值
max_index = 100
# 初始化一个全为 1 的列表
result = [1] * max_index
# 将 human_wrong 中数字减 1 对应的索引位置置为 0
for num in human_wrong:
    result[num - 1] = 0

correlation, p_value = spearmanr(ai_access_result, result)
print(correlation, p_value)

correlation_matrix = np.corrcoef(ai_access_result, result)
correlation = correlation_matrix[0, 1]
print(correlation)

same_count = sum(1 for x, y in zip(ai_access_result, result) if x == y)
print(same_count/100)