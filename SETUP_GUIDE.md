# SA Shop Django - EasyBuy 電商平台

完整的Django電商應用程序，集成了前端和後端，支持購物、訂單管理和賣家後台管理。

## ✨ 核心功能

### 買家功能
- 🛍️ 瀏覽商品與商城分類
- 🔍 搜尋商品功能
- 🛒 購物結帳流程
- 📦 訂單追蹤與物流狀態
- 👤 用戶登入/註冊與資料管理

### 賣家功能
- 📦 商品上架與管理
- 📊 賣場商品清單
- ⚙️ 商品編輯與下架
- 🏪 店鋪管理

### 核心功能
- ✅ SQLite 資料庫（開發環境）
- 🔐 用戶認證與授權
- 📱 響應式設計
- 🎨 溫暖大地色系UI

## 🗄️ 資料庫選擇

### 開發階段（推薦）✅

**SQLite** - 最適合小型專案
- ✅ 無需配置，開箱即用
- ✅ 文件型輕量級資料庫
- ✅ Django 預設支持
- ✅ 完美適合開發與測試
- ✅ 輕鬆備份與遷移

### 未來擴展建議

**PostgreSQL** - 生產級解決方案
- 多用戶高併發場景
- 大數據量存儲
- 複雜查詢需求
- 企業級應用

**MySQL** - 另一生產級選項
- 廣泛使用和支持
- 穩定的性能
- 易於部署

## 🚀 快速開始

### 1. 環境設置

```bash
# 複製項目或進入目錄
cd SA_shop-Django

# 創建虛擬環境
python -m venv venv

# 啟用虛擬環境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 2. 安裝依賴

```bash
pip install -r requirements.txt
```

### 3. 數據庫配置（已完成）

資料庫遷移已完成，SQLite 資料庫已建立：
```bash
# 查看現有遷移（可選）
python manage.py showmigrations

# 如有新模型，創建遷移
python manage.py makemigrations

# 執行遷移
python manage.py migrate
```

### 4. 管理員帳戶（已創建）

```
用戶名: admin
密碼: admin123
訪問: http://127.0.0.1:8000/admin/
```

### 5. 運行開發伺服器

```bash
python manage.py runserver
```

訪問應用：
- 主頁: http://127.0.0.1:8000/
- 管理員面板: http://127.0.0.1:8000/admin/

## 📁 項目結構

```
SA_shop-Django/
├── sa_shop/                    # 項目配置
│   ├── settings.py             # Django設置（含數據庫配置）
│   ├── urls.py                 # 主URL路由
│   ├── wsgi.py / asgi.py       # 應用伺服器配置
│   └── __init__.py
│
├── apps/                        # 應用程序
│   ├── products/                # 商品應用
│   │   ├── models.py            # 商品、分類、訂單模型
│   │   ├── views.py             # 視圖和API端點
│   │   ├── urls.py              # URL路由
│   │   ├── admin.py             # 管理員配置
│   │   ├── apps.py              # 應用配置
│   │   └── migrations/          # 數據庫遷移文件
│   │
│   └── users/                   # 用戶應用
│       ├── models.py            # CustomUser 用戶模型
│       ├── views.py             # 認證視圖和API
│       ├── urls.py              # URL路由
│       ├── admin.py             # 管理員配置
│       ├── apps.py              # 應用配置
│       └── migrations/          # 數據庫遷移文件
│
├── templates/                   # HTML模板
│   └── index.html              # 主前端頁面（EasyBuy）
│
├── static/                      # 靜態文件（CSS、JS、圖片）
├── media/                       # 用戶上傳的媒體文件
├── db.sqlite3                   # SQLite 資料庫（已初始化）
├── manage.py                    # Django 管理命令入口
├── requirements.txt             # Python 依賴列表
└── README.md                    # 本文件
```

## 🗂️ 資料庫模型

### 用戶模型 (CustomUser)
- 用戶名、郵箱、密碼
- 手機、地址、頭像、個人簡介
- 用戶類型（買家/賣家/兼職）
- 店鋪名稱（賣家用）
- 驗證狀態

### 商品模型 (Product)
- 商品名稱、描述、價格
- 分類、圖片、庫存
- 賣家關聯
- 商品狀態（販售中/已下架）

### 訂單模型 (Order)
- 訂單號、買家、商品
- 數量、價格、運費
- 收件人信息
- 訂單狀態、付款方式
- 時間戳

### 訂單追蹤 (OrderTracking)
- 物流進度時間軸
- 追蹤標題與描述
- 活動狀態標記

### 商品分類 (Category)
- 分類名稱、圖標、描述

## 🔧 常用命令

```bash
# 啟動開發伺服器
python manage.py runserver

# 進入 Django Shell（互動環境）
python manage.py shell

# 創建新的超級用戶
python manage.py createsuperuser

# 查看所有遷移
python manage.py showmigrations

# 創建新遷移（有新模型時）
python manage.py makemigrations

# 執行待遷移
python manage.py migrate

# 收集靜態文件（生產用）
python manage.py collectstatic

# 運行測試（如有）
python manage.py test
```

## 🔐 生產環境配置清單

⚠️ 部署前必須做以下調整：

1. **安全設置**
   ```python
   # settings.py
   DEBUG = False
   SECRET_KEY = 'your-very-secret-key-change-this'
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   ```

2. **數據庫配置**
   - 切換至 PostgreSQL 或 MySQL
   - 更新資料庫連接字符串
   - 配置用戶認證

3. **環境變量**
   - 使用 `.env` 文件存儲敏感信息
   - 配置郵件服務
   - 設定支付網關

4. **HTTPS & 安全**
   - 配置 SSL 證書
   - 設置 SECURE_SSL_REDIRECT
   - 啟用 HSTS

5. **靜態 & 媒體文件**
   - 配置 CDN 或 S3
   - 設置檔案伺服器

## 📝 API 端點

### 商品 API
```
GET /api/products/list/              # 獲取商品列表（支持搜尋與分類過濾）
GET /api/products/categories/        # 獲取分類列表
```

### 用戶 API
```
POST /api/users/register/            # 用戶註冊
POST /api/users/login/               # 用戶登錄
```

## 🎨 前端功能

- **單頁應用 (SPA)** - 使用 JavaScript 進行頁面切換
- **響應式設計** - 支持桌面與行動設備
- **實時搜尋** - 即時過濾商品
- **購物流程** - 完整的購物到結帳流程

## 🐛 故障排除

### 數據庫相關
```bash
# 重置數據庫（開發環境）
rm db.sqlite3
python manage.py migrate

# 檢查遷移狀態
python manage.py showmigrations
```

### 模塊缺失
```bash
# 重新安裝依賴
pip install -r requirements.txt --force-reinstall
```

### 靜態文件問題
```bash
# 收集靜態文件
python manage.py collectstatic --noinput
```

## 📚 技術棧

- **後端**: Django 4.2+
- **資料庫**: SQLite（開發）/ PostgreSQL（生產）
- **前端**: HTML5 + CSS3 + Vanilla JavaScript
- **API**: Django REST Framework
- **認證**: Django 內置認證系統
- **CORS**: django-cors-headers

## 📄 許可證

MIT License

## 👨‍💻 聯繫方式

如有問題或建議，歡迎提出！

---

**最後更新**: 2026年6月1日
**版本**: 1.0.0
**狀態**: ✅ 開發就緒
