"""
生成完整的14種植物類別數統計圖表
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

# 所有14種植物的類別數統計（按類別數從高到低排序）
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

# 創建圖表
fig, ax = plt.subplots(figsize=(12, 10))

plants = list(plant_class_counts.keys())
counts = list(plant_class_counts.values())

# 使用漸變色
colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(plants)))

bars = ax.barh(plants, counts, color=colors, alpha=0.8, edgecolor='black', linewidth=0.5)
ax.set_xlabel('類別數', fontsize=14, fontweight='bold', fontproperties=chinese_font)
ax.set_title('PlantVillage 資料集 - 所有14種植物類別數統計\n（總計38個類別）', 
             fontsize=16, fontweight='bold', pad=20, fontproperties=chinese_font)
ax.set_yticks(range(len(plants)))
ax.set_yticklabels(plants, fontproperties=chinese_font, fontsize=11)

# 在每個柱狀圖上顯示數值
for i, (bar, count) in enumerate(zip(bars, counts)):
    width = bar.get_width()
    ax.text(width, bar.get_y() + bar.get_height()/2.,
             f' {count} 個類別', ha='left', va='center', 
             fontsize=10, fontweight='bold', fontproperties=chinese_font)

# 添加總計標註
total = sum(counts)
ax.text(0.98, 0.02, f'總計：{total} 個類別', 
        transform=ax.transAxes, fontsize=12, fontweight='bold',
        ha='right', va='bottom', fontproperties=chinese_font,
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

ax.grid(True, alpha=0.3, axis='x')
ax.set_xlim(0, max(counts) * 1.15)

plt.tight_layout()
plt.savefig('complete_plant_statistics.png', dpi=300, bbox_inches='tight')
plt.close()
print("已生成完整圖表：complete_plant_statistics.png")


