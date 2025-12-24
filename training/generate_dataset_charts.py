"""
生成資料集相關的視覺化圖表，用於報告展示
"""
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import seaborn as sns

# 設置中文字體
font_path = r'C:\Windows\Fonts\msyh.ttc'
chinese_font = fm.FontProperties(fname=font_path)
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False
sns.set_style('darkgrid')

# 資料集基本資訊
dataset_info = {
    '訓練集': 43444,
    '驗證集': 5430,
    '測試集': 5431,
    '總計': 54305
}

# 類別數統計
class_stats = {
    '植物種類數': 14,
    '總類別數': 38,
    '健康類別': 14,
    '病害類別': 24
}

# 按植物種類的類別數統計（所有14種植物）
plant_class_counts = {
    '番茄': 10,
    '蘋果': 4,
    '玉米': 4,
    '葡萄': 4,
    '馬鈴薯': 3,
    '櫻桃': 2,
    '桃子': 2,
    '甜椒': 2,
    '草莓': 2,
    '柑橘': 1,
    '藍莓': 1,
    '覆盆子': 1,
    '大豆': 1,
    '南瓜': 1
}

# 測試集樣本數最多的前15個類別
top_classes_samples = {
    'Orange_Haunglongbing': 551,
    'Tomato_Yellow_Leaf_Curl_Virus': 536,
    'Soybean_healthy': 509,
    'Apple_healthy': 165,
    'Squash_Powdery_mildew': 184,
    'Peach_Bacterial_spot': 230,
    'Tomato_Bacterial_spot': 213,
    'Tomato_Late_blight': 191,
    'Squash_Powdery_mildew_alt': 184,  # 避免重複，使用不同名稱
    'Strawberry_Leaf_scorch': 111,
    'Grape_Esca': 139,
    'Tomato_healthy': 159,
    'Corn_Common_rust': 119,
    'Corn_healthy': 116,
    'Cherry_Powdery_mildew': 105
}

# 1. 資料集分割比例圖（圓餅圖）
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# 圓餅圖
colors_pie = ['#ff6b6b', '#4ecdc4', '#95e1d3']
labels = ['訓練集', '驗證集', '測試集']
sizes = [43444, 5430, 5431]
explode = (0.05, 0, 0)  # 突出顯示訓練集

ax1.pie(sizes, explode=explode, labels=labels, colors=colors_pie, autopct='%1.1f%%',
        shadow=True, startangle=90, textprops={'fontproperties': chinese_font})
ax1.set_title('資料集分割比例', fontsize=14, fontweight='bold', pad=20, fontproperties=chinese_font)

# 柱狀圖
bars = ax2.bar(labels, sizes, color=colors_pie, alpha=0.8)
ax2.set_ylabel('樣本數', fontsize=12, fontproperties=chinese_font)
ax2.set_title('資料集樣本數分布', fontsize=14, fontweight='bold', fontproperties=chinese_font)
ax2.set_xticks(range(len(labels)))
ax2.set_xticklabels(labels, fontproperties=chinese_font)
for bar, size in zip(bars, sizes):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             f'{size:,}', ha='center', va='bottom', fontsize=11, fontproperties=chinese_font)
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('dataset_split.png', dpi=300, bbox_inches='tight')
plt.close()
print("已生成：dataset_split.png")

# 2. 類別統計圖
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 9))

# 類別類型統計
category_types = ['健康類別', '病害類別']
category_counts = [14, 24]
colors_bar = ['#4ecdc4', '#ff6b6b']

bars1 = ax1.bar(category_types, category_counts, color=colors_bar, alpha=0.8)
ax1.set_ylabel('類別數量', fontsize=12, fontproperties=chinese_font)
ax1.set_title('健康與病害類別統計', fontsize=14, fontweight='bold', fontproperties=chinese_font)
ax1.set_xticks(range(len(category_types)))
ax1.set_xticklabels(category_types, fontproperties=chinese_font)
for bar, count in zip(bars1, category_counts):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{count}', ha='center', va='bottom', fontsize=12, fontweight='bold', 
             fontproperties=chinese_font)
ax1.grid(True, alpha=0.3, axis='y')

# 植物種類類別數統計（所有14種植物）
plants = list(plant_class_counts.keys())
counts = list(plant_class_counts.values())

bars2 = ax2.barh(plants, counts, color='#95e1d3', alpha=0.8)
ax2.set_xlabel('類別數', fontsize=12, fontproperties=chinese_font)
ax2.set_title('各植物種類類別數統計（所有14種植物）', fontsize=14, fontweight='bold', fontproperties=chinese_font)
ax2.set_yticks(range(len(plants)))
ax2.set_yticklabels(plants, fontproperties=chinese_font, fontsize=10)
for i, (bar, count) in enumerate(zip(bars2, counts)):
    width = bar.get_width()
    ax2.text(width, bar.get_y() + bar.get_height()/2.,
             f' {count}', ha='left', va='center', fontsize=9, fontproperties=chinese_font)
ax2.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('class_statistics.png', dpi=300, bbox_inches='tight')
plt.close()
print("已生成：class_statistics.png")

# 3. 測試集類別樣本數分布（前15個類別）
fig, ax = plt.subplots(figsize=(12, 8))

# 簡化類別名稱用於顯示
class_names_display = [
    'Orange_Haunglongbing', 'Tomato_Yellow_Leaf', 'Soybean_healthy',
    'Peach_Bacterial', 'Tomato_Bacterial', 'Tomato_Late_blight',
    'Squash_Powdery', 'Tomato_healthy', 'Grape_Esca', 'Strawberry_Leaf',
    'Corn_Common_rust', 'Corn_healthy', 'Cherry_Powdery', 'Apple_healthy',
    'Grape_Leaf_blight'
]

# 實際樣本數（基於報告中的數據）
sample_counts = [551, 536, 509, 230, 213, 191, 184, 159, 139, 111, 119, 116, 105, 165, 108]

bars = ax.barh(class_names_display, sample_counts, color='#4ecdc4', alpha=0.8)
ax.set_xlabel('測試集樣本數', fontsize=12, fontproperties=chinese_font)
ax.set_title('測試集類別樣本數分布（前15個類別）', fontsize=14, fontweight='bold', pad=20, fontproperties=chinese_font)
ax.set_yticks(range(len(class_names_display)))
ax.set_yticklabels(class_names_display, fontproperties=chinese_font, fontsize=9)

for i, (bar, count) in enumerate(zip(bars, sample_counts)):
    width = bar.get_width()
    ax.text(width, bar.get_y() + bar.get_height()/2.,
            f' {count}', ha='left', va='center', fontsize=9, fontproperties=chinese_font)

ax.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.savefig('test_samples_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("已生成：test_samples_distribution.png")

# 4. 資料集整體資訊總結圖
fig = plt.figure(figsize=(14, 8))
ax = fig.add_subplot(111)
ax.axis('off')

# 創建資訊框
info_text = f"""
資料集整體資訊摘要

總樣本數：54,305 張圖像
總類別數：38 種植物病害類型
植物種類：14 種主要植物

資料分割：
  • 訓練集：43,444 張 (80%)
  • 驗證集：5,430 張 (10%)
  • 測試集：5,431 張 (10%)

類別分布：
  • 健康類別：14 個
  • 病害類別：24 個

主要植物：
  • 番茄：10 個類別（最多）
  • 蘋果、玉米、葡萄：各 4 個類別
  • 馬鈴薯：3 個類別

資料來源：PlantVillage 資料集（color 資料夾）
圖像格式：彩色 RGB 圖像
標準尺寸：224 × 224 像素
"""

ax.text(0.1, 0.5, info_text, fontsize=14, fontproperties=chinese_font,
        verticalalignment='center', family='monospace',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
ax.set_title('PlantVillage 植物病害檢測資料集資訊', 
             fontsize=16, fontweight='bold', pad=20, fontproperties=chinese_font)

plt.tight_layout()
plt.savefig('dataset_summary.png', dpi=300, bbox_inches='tight')
plt.close()
print("已生成：dataset_summary.png")

print("\n所有資料集圖表已生成完成！")

