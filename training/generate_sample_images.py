"""
生成實際植物圖片的展示圖，用於報告
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

# 資料集路徑（相對於training目錄）
data_dir = '../plantvillage dataset/color'
# 如果不存在，嘗試其他可能的路徑
if not os.path.exists(data_dir):
    data_dir = '../../plantvillage dataset/color'
if not os.path.exists(data_dir):
    data_dir = 'plantvillage dataset/color'

def get_sample_images(data_dir, num_classes=12, images_per_class=1):
    """
    從資料集中獲取樣本圖像
    """
    samples = []
    
    if not os.path.exists(data_dir):
        print(f"警告：找不到資料集路徑 {data_dir}")
        print("將創建占位圖像")
        return None
    
    # 獲取所有類別資料夾
    class_folders = [f for f in os.listdir(data_dir) 
                     if os.path.isdir(os.path.join(data_dir, f))]
    class_folders.sort()
    
    # 選擇前num_classes個類別，並確保包含健康和多種病害類型
    selected_classes = class_folders[:num_classes]
    
    for class_name in selected_classes:
        class_path = os.path.join(data_dir, class_name)
        image_files = [f for f in os.listdir(class_path) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        if image_files:
            # 隨機選擇images_per_class張圖片
            selected_images = random.sample(image_files, min(images_per_class, len(image_files)))
            
            for img_file in selected_images:
                img_path = os.path.join(class_path, img_file)
                try:
                    img = Image.open(img_path)
                    # 轉換為RGB（處理RGBA等格式）
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    # 調整大小以便展示（統一尺寸）
                    img = img.resize((224, 224), Image.Resampling.LANCZOS)
                    samples.append((img, class_name))
                except Exception as e:
                    print(f"無法載入圖片 {img_path}: {e}")
                    continue
    
    return samples

def create_sample_grid(samples, title="植物病害樣本展示", save_path="sample_images_grid.png"):
    """
    創建樣本圖像網格
    """
    if samples is None or len(samples) == 0:
        # 創建占位圖
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.text(0.5, 0.5, '無法載入圖片\n請確認資料集路徑正確', 
                ha='center', va='center', fontsize=16, fontproperties=chinese_font,
                transform=ax.transAxes)
        ax.axis('off')
        plt.title(title, fontsize=18, fontweight='bold', pad=20, fontproperties=chinese_font)
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"已生成占位圖：{save_path}")
        return
    
    # 計算網格大小（每行4張圖）
    num_images = len(samples)
    cols = 4
    rows = (num_images + cols - 1) // cols
    
    fig, axes = plt.subplots(rows, cols, figsize=(16, rows * 4))
    fig.suptitle(title, fontsize=20, fontweight='bold', y=0.995, fontproperties=chinese_font)
    
    # 如果是單行，確保axes是2D數組
    if rows == 1:
        axes = axes.reshape(1, -1)
    
    for idx, (img, class_name) in enumerate(samples):
        row = idx // cols
        col = idx % cols
        ax = axes[row, col]
        
        # 顯示圖像
        ax.imshow(img)
        ax.axis('off')
        
        # 簡化類別名稱用於顯示（移除前綴，只保留關鍵信息）
        display_name = class_name.replace('___', ' - ').replace('_', ' ')
        # 如果名稱太長，進行截斷
        if len(display_name) > 30:
            display_name = display_name[:27] + '...'
        
        ax.set_title(display_name, fontsize=10, fontproperties=chinese_font, 
                    pad=5, color='darkblue', fontweight='bold')
    
    # 隱藏多餘的子圖
    for idx in range(num_images, rows * cols):
        row = idx // cols
        col = idx % cols
        axes[row, col].axis('off')
    
    plt.tight_layout(rect=[0, 0, 1, 0.98])
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"已生成：{save_path} (共 {num_images} 張圖片)")

def create_category_comparison(data_dir, categories=None, save_path="category_comparison.png"):
    """
    創建特定類別的對比展示（健康 vs 病害）
    """
    if categories is None:
        # 選擇幾個代表性植物進行對比
        categories = [
            'Apple___healthy',
            'Apple___Apple_scab',
            'Tomato___healthy',
            'Tomato___Bacterial_spot',
            'Corn_(maize)___healthy',
            'Corn_(maize)___Common_rust_'
        ]
    
    samples = []
    for class_name in categories:
        class_path = os.path.join(data_dir, class_name)
        if not os.path.exists(class_path):
            continue
        
        image_files = [f for f in os.listdir(class_path) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        if image_files:
            img_file = random.choice(image_files)
            img_path = os.path.join(class_path, img_file)
            try:
                img = Image.open(img_path)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img = img.resize((300, 300), Image.Resampling.LANCZOS)
                samples.append((img, class_name))
            except Exception as e:
                print(f"無法載入圖片 {img_path}: {e}")
                continue
    
    if len(samples) == 0:
        return
    
    # 創建對比圖（2行3列）
    rows = 2
    cols = 3
    fig, axes = plt.subplots(rows, cols, figsize=(15, 10))
    fig.suptitle('健康植物與病害植物對比展示', fontsize=20, fontweight='bold', 
                 y=0.98, fontproperties=chinese_font)
    
    for idx, (img, class_name) in enumerate(samples[:rows*cols]):
        row = idx // cols
        col = idx % cols
        ax = axes[row, col]
        
        ax.imshow(img)
        ax.axis('off')
        
        # 格式化類別名稱
        display_name = class_name.replace('___', ' - ').replace('_', ' ')
        # 標記健康類別
        if 'healthy' in class_name.lower():
            color = 'green'
        else:
            color = 'red'
        
        ax.set_title(display_name, fontsize=12, fontproperties=chinese_font, 
                    pad=10, color=color, fontweight='bold')
    
    # 隱藏多餘的子圖
    for idx in range(len(samples), rows * cols):
        row = idx // cols
        col = idx % cols
        axes[row, col].axis('off')
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"已生成：{save_path}")

# 設置隨機種子以確保可重現
random.seed(42)
np.random.seed(42)

print("開始生成植物圖片展示...")
print(f"資料集路徑: {data_dir}")

# 1. 生成樣本圖片網格（12個不同類別）
samples = get_sample_images(data_dir, num_classes=12, images_per_class=1)
create_sample_grid(samples, 
                  title="植物病害檢測資料集 - 樣本圖片展示（部分類別）",
                  save_path="sample_images_grid.png")

# 2. 生成健康vs病害對比圖
create_category_comparison(data_dir, save_path="category_comparison.png")

print("\n所有植物圖片展示已生成完成！")


