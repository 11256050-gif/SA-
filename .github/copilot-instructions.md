<!-- Django 小專案開發指南 -->

## 專案信息
- **專案名稱**: SA Shop Django
- **框架**: Django 4.x
- **資料庫**: SQLite（開發用）
- **Python版本**: 3.9+

## 快速開始

### 1. 創建虛擬環境
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 2. 安裝依賴
```bash
pip install -r requirements.txt
```

### 3. 遷移資料庫
```bash
python manage.py migrate
```

### 4. 創建超級用戶
```bash
python manage.py createsuperuser
```

### 5. 運行開發伺服器
```bash
python manage.py runserver
```

訪問 http://127.0.0.1:8000/

## 資料庫建議

### 開發階段（推薦）✅
- **SQLite** - Django預設，無需配置，完美適合小型專案和開發

### 未來擴展
- **PostgreSQL** - 多用戶應用、大數據量
- **MySQL** - 另一個生產級選項

## 項目結構
```
SA_shop-Django/
├── sa_shop/              # 項目配置
│   ├── settings.py
│   ├── urls.py
│   └── asgi.py
├── apps/                 # 應用程序
│   ├── products/         # 商品應用
│   └── users/            # 用戶應用
├── static/               # 靜態文件
├── templates/            # 模板文件
├── manage.py
├── requirements.txt
└── README.md
```

## 常用命令
- `python manage.py runserver` - 啟動開發伺服器
- `python manage.py makemigrations` - 創建遷移文件
- `python manage.py migrate` - 執行遷移
- `python manage.py createsuperuser` - 創建管理員
- `python manage.py shell` - Django互動殼
