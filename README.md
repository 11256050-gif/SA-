# SA Shop Django

一個使用Django框架開發的小型購物應用程序。

## 功能特性

- 用戶認證與管理
- 商品管理與展示
- 訂單管理
- 管理員面板

## 技術棧

- **框架**: Django 4.2.13
- **資料庫**: SQLite（開發用）
- **API**: Django REST Framework
- **認證**: Django內置認證系統

## 快速開始

### 環境需求

- Python 3.9+
- pip

### 安裝步驟

1. **克隆或下載項目**

2. **創建虛擬環境**
   ```bash
   python -m venv venv
   ```

3. **啟用虛擬環境**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **安裝依賴**
   ```bash
   pip install -r requirements.txt
   ```

5. **執行遷移**
   ```bash
   python manage.py migrate
   ```

6. **創建超級用戶（管理員）**
   ```bash
   python manage.py createsuperuser
   ```

7. **運行開發伺服器**
   ```bash
   python manage.py runserver
   ```

8. **訪問應用**
   - 主頁: http://127.0.0.1:8000/
   - 管理員面板: http://127.0.0.1:8000/admin/

## 項目結構

```
SA_shop-Django/
├── sa_shop/              # 項目主配置目錄
│   ├── settings.py       # Django設置
│   ├── urls.py           # URL路由配置
│   ├── wsgi.py           # WSGI配置
│   └── asgi.py           # ASGI配置
├── apps/                 # 應用程序目錄
│   ├── products/         # 商品應用
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── admin.py
│   └── users/            # 用戶應用
│       ├── models.py
│       ├── views.py
│       ├── urls.py
│       └── admin.py
├── static/               # 靜態文件（CSS、JS、圖片）
├── templates/            # HTML模板文件
├── media/                # 用戶上傳的媒體文件
├── manage.py             # Django管理命令
├── requirements.txt      # Python依賴列表
└── README.md             # 本文件
```

## 常用命令

```bash
# 啟動開發伺服器
python manage.py runserver

# 創建數據庫遷移
python manage.py makemigrations

# 執行遷移
python manage.py migrate

# 創建超級用戶
python manage.py createsuperuser

# 進入Django互動殼
python manage.py shell

# 收集靜態文件
python manage.py collectstatic
```

## 資料庫選擇

### 開發階段（推薦）✅

**SQLite** 是最佳選擇，原因：
- ✅ 無需單獨安裝或配置
- ✅ 文件型資料庫，輕量級
- ✅ Django預設支持
- ✅ 完美適合小型項目
- ✅ 開發測試完全夠用
- ✅ 易於備份和遷移

### 未來生產環境建議

當應用需要擴展時，可考慮：

- **PostgreSQL** - 推薦用於
  - 多用戶高併發場景
  - 大數據量存儲
  - 複雜查詢需求
  - 生產環境

- **MySQL** - 另一個生產級選項
  - 廣泛使用的關係型資料庫
  - 性能穩定
  - 易於部署

### 資料庫遷移指南

若要從SQLite遷移到PostgreSQL：

1. 安裝PostgreSQL驅動：
   ```bash
   pip install psycopg2-binary
   ```

2. 更新 `settings.py`：
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'sa_shop_db',
           'USER': 'postgres',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

3. 執行遷移命令：
   ```bash
   python manage.py migrate
   ```

## 配置說明

### 允許訪問的主機

在 `sa_shop/settings.py` 中配置 `ALLOWED_HOSTS`：

```python
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'yourdomain.com']
```

### 静態文件配置

- `STATIC_URL = '/static/'` - 静態文件URL
- `STATIC_ROOT` - 生產環境收集的靜態文件存放位置
- `MEDIA_URL = '/media/'` - 用戶上傳文件URL
- `MEDIA_ROOT` - 用戶上傳文件存放位置

### 安全設置

⚠️ **生產環境注意事項：**

1. 更改 `SECRET_KEY`
2. 設置 `DEBUG = False`
3. 更新 `ALLOWED_HOSTS`
4. 配置安全的資料庫密碼
5. 使用環境變量管理敏感信息

## 貢獻

歡迎提出問題和提交改進建議。

## 許可

MIT License

## 聯繫方式

如有問題，請聯繫開發者。
