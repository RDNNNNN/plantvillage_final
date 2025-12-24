"""
生成所有38個類別的植物圖片展示
"""
import os
import random
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from PIL import Image
import numpy as np

# 設置中文字體
font_path = r'C:\Windows\Fonts\msyh.ttc'
chinese_font = fm.FontProperties(fname=font_path)
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# 資料集路徑
data_dir = '../plantvillage dataset/color'
if not os.path.exists(data_dir):
    data_dir = '../../plantvillage dataset/color'
if not os.path.exists(data_dir):
    data_dir = 'plantvillage dataset/color'

def get_all_category_samples(data_dir):
    """
    獲取所有類別的樣本圖像
    """
    samples = []
    
    if not os.path.exists(data_dir):
        print(f"警告：找不到資料集路徑 {data_dir}")
        return None
    
    # 獲取所有類別資料夾並排序
    class_folders = [f for f in os.listdir(data_dir) 
                     if os.path.isdir(os.path.join(data_dir, f))]
    class_folders.sort()
    
    print(f"找到 {len(class_folders)} 個類別")
    
    for class_name in class_folders:
        class_path = os.path.join(data_dir, class_name)
        image_files = [f for f in os.listdir(class_path) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        if image_files:
            # 每個類別選取1張圖片
            img_file = random.choice(image_files)
            img_path = os.path.join(class_path, img_file)
            try:
                img = Image.open(img_path)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                # 調整大小
                img = img.resize((200, 200), Image.Resampling.LANCZOS)
                samples.append((img, class_name))
                print(f"已載入: {class_name}")
            except Exception as e:
                print(f"無法載入圖片 {img_path}: {e}")
                continue
        else:
            print(f"警告：{class_name} 資料夾中沒有圖片文件")
    
    return samples

def create_all_categories_grid(samples, cols=6, save_path="all_categories_grid.png"):
    """
    創建所有類別的圖片網格（38個類別）
    """
    if samples is None or len(samples) == 0:
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.text(0.5, 0.5, '無法載入圖片\n請確認資料集路徑正確', 
                ha='center', va='center', fontsize=16, fontproperties=chinese_font,
                transform=ax.transAxes)
        ax.axis('off')
        plt.title('所有類別圖片展示', fontsize=18, fontweight='bold', pad=20, fontproperties=chinese_font)
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"已生成占位圖：{save_path}")
        return
    
    num_images = len(samples)
    rows = (num_images + cols - 1) // cols
    
    # 使用較大的圖形尺寸以容納所有圖片
    fig, axes = plt.subplots(rows, cols, figsize=(18, rows * 2.5))
    fig.suptitle(f'PlantVillage 資料集 - 所有38個類別圖片展示', 
                 fontsize=22, fontweight='bold', y=0.995, fontproperties=chinese_font)
    
    # 確保axes是2D數組
    if rows == 1:
        axes = axes.reshape(1, -1)
    
    for idx, (img, class_name) in enumerate(samples):
        row = idx // cols
        col = idx % cols
        ax = axes[row, col]
        
        # 顯示圖像
        ax.imshow(img)
        ax.axis('off')
        
        # 格式化類別名稱
        display_name = class_name.replace('___', '\n').replace('_', ' ')
        # 標記健康類別（綠色）和病害類別（紅色）
        if 'healthy' in class_name.lower():
            color = 'green'
            fontweight = 'bold'
        else:
            color = 'darkred'
            fontweight = 'normal'
        
        # 調整字體大小根據名稱長度
        fontsize = 8 if len(display_name) > 30 else 9
        
        ax.set_title(display_name, fontsize=fontsize, fontproperties=chinese_font, 
                    pad=3, color=color, fontweight=fontweight)
    
    # 隱藏多餘的子圖
    for idx in range(num_images, rows * cols):
        row = idx // cols
        col = idx % cols
        axes[row, col].axis('off')
    
    plt.tight_layout(rect=[0, 0, 1, 0.99])
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"已生成：{save_path} (共 {num_images} 個類別)")

def create_categories_by_plant(samples, save_path="categories_by_plant.png"):
    """
    按植物種類分組展示類別
    """
    if samples is None or len(samples) == 0:
        return
    
    # 按植物類型分組
    plant_groups = {}
    for img, class_name in samples:
        # 提取植物名稱（第一個下劃線前的部分）
        if '___' in class_name:
            plant_name = class_name.split('___')[0]
            # 簡化植物名稱
            plant_name = plant_name.replace('(including_sour)', '').replace('(maize)', '').replace(',_bell', '').strip()
        else:
            plant_name = class_name
        
        if plant_name not in plant_groups:
            plant_groups[plant_name] = []
        plant_groups[plant_name].append((img, class_name))
    
    # 按植物名稱排序
    sorted_plants = sorted(plant_groups.keys())
    
    # 計算需要多少行和列（每種植物一行，每行最多6張圖）
    max_classes_per_plant = max(len(classes) for classes in plant_groups.values())
    cols = min(max_classes_per_plant, 6)
    rows = len(sorted_plants)
    
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 2.5, rows * 3))
    fig.suptitle('按植物種類分組的所有類別展示', fontsize=20, fontweight='bold', 
                 y=0.995, fontproperties=chinese_font)
    
    # 確保axes是2D數組
    if rows == 1:
        axes = axes.reshape(1, -1)
    
    for row_idx, plant_name in enumerate(sorted_plants):
        classes = plant_groups[plant_name]
        for col_idx, (img, class_name) in enumerate(classes):
            if col_idx >= cols:
                break
            ax = axes[row_idx, col_idx]
            
            ax.imshow(img)
            ax.axis('off')
            
            # 格式化類別名稱（移除植物前綴，只顯示病害/健康類型）
            if '___' in class_name:
                disease_name = class_name.split('___', 1)[1]
                display_name = disease_name.replace('_', ' ')
            else:
                display_name = class_name.replace('_', ' ')
            
            # 標記健康類別
            if 'healthy' in class_name.lower():
                color = 'green'
                fontweight = 'bold'
            else:
                color = 'darkred'
                fontweight = 'normal'
            
            # 第一列顯示植物名稱
            if col_idx == 0:
                title = f"{plant_name}\n{display_name}"
                fontsize = 8
            else:
                title = display_name
                fontsize = 9
            
            ax.set_title(title, fontsize=fontsize, fontproperties=chinese_font, 
                        pad=3, color=color, fontweight=fontweight)
        
        # 隱藏該行多餘的子圖
        for col_idx in range(len(classes), cols):
            axes[row_idx, col_idx].axis('off')
    
    plt.tight_layout(rect=[0, 0, 1, 0.99])
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"已生成：{save_path}")

# 設置隨機種子
random.seed(42)
np.random.seed(42)

print("開始生成所有類別的植物圖片展示...")
print(f"資料集路徑: {data_dir}\n")

# 獲取所有類別的樣本
samples = get_all_category_samples(data_dir)

if samples:
    print(f"\n成功載入 {len(samples)} 個類別的圖片")
    
    # 1. 生成所有類別的網格圖（6列布局）
    create_all_categories_grid(samples, cols=6, save_path="all_categories_grid.png")
    
    # 2. 按植物種類分組展示（可選，如果圖片太多可能太大）
    # create_categories_by_plant(samples, save_path="categories_by_plant.png")
    
    print("\n所有類別圖片展示已生成完成！")
else:
    print("\n無法載入圖片，請檢查資料集路徑")


