# SA Shop Django - API 集成指南

## 開發服務器
```bash
python manage.py runserver
```
- 主頁: http://127.0.0.1:8000/
- 管理後台: http://127.0.0.1:8000/admin/ (admin/admin123)

## 測試帳戶

### 賣家帳戶
- 用戶名: `seller_demo`
- 密碼: `seller123`
- Email: `seller@easybuy.com`
- Token: `6db636c007b6fe1b41d3a8e7bd0bbe5f1793468c`

### 管理員帳戶
- 用戶名: `admin`
- 密碼: `admin123`
- Email: `admin@easybuy.com`

## API 端點詳解

### 1. 商品列表 (GET)
```
GET /api/products/products/
GET /api/products/products/?search=燈
GET /api/products/products/?category=生活美學
```

**Response:**
```json
{
  "count": 6,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "極簡原木微光檯燈",
      "price": "1480.00",
      "category": 1,
      "category_name": "生活美學",
      "stock": 12,
      "status": "onsale",
      "seller": 2,
      "seller_name": "seller_demo",
      "description": "嚴選北美胡桃木製成...",
      "image": null,
      "created_at": "2026-06-02T00:02:57.178557+08:00",
      "updated_at": "2026-06-02T00:02:57.178574+08:00"
    }
  ]
}
```

### 2. 商品分類 (GET)
```
GET /api/products/categories/
```

**Response:**
```json
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "name": "生活美學",
      "icon": "💡",
      "description": "極簡居家裝飾",
      "count": 3
    }
  ]
}
```

### 3. 訂單建立 (POST)
```
POST /api/products/orders/create_order/
Content-Type: application/json
Authorization: Token 6db636c007b6fe1b41d3a8e7bd0bbe5f1793468c

{
  "product_id": 1,
  "quantity": 1,
  "recipient_name": "王小明",
  "recipient_phone": "0912345678",
  "recipient_address": "台北市信義區",
  "payment_method": "cod"
}
```

**Response:**
```json
{
  "success": true,
  "message": "訂單建立成功",
  "order_id": 1,
  "order_number": "EB-20260602-1234"
}
```

### 4. 用戶登錄 (POST)
```
POST /api/users/api/login/
Content-Type: application/json

{
  "username": "seller_demo",
  "password": "seller123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "登錄成功",
  "user": {
    "id": 2,
    "username": "seller_demo",
    "email": "seller@easybuy.com",
    "user_type": "seller",
    "store_name": "阿明的生活選物店"
  },
  "token": "6db636c007b6fe1b41d3a8e7bd0bbe5f1793468c"
}
```

### 5. 用戶註冊 (POST)
```
POST /api/users/api/register/
Content-Type: application/json

{
  "username": "newuser",
  "email": "user@example.com",
  "phone": "0912345678",
  "password": "password123",
  "password2": "password123",
  "user_type": "buyer"
}
```

**Response:**
```json
{
  "success": true,
  "message": "註冊成功",
  "user": {
    "id": 3,
    "username": "newuser",
    "email": "user@example.com"
  }
}
```

### 6. 獲取當前用戶信息 (GET)
```
GET /api/users/api/me/
Authorization: Token 6db636c007b6fe1b41d3a8e7bd0bbe5f1793468c
```

### 7. 獲取用戶訂單 (GET)
```
GET /api/products/orders/
Authorization: Token <用戶Token>
```

### 8. 創建商品 (POST)
```
POST /api/products/products/
Authorization: Token 6db636c007b6fe1b41d3a8e7bd0bbe5f1793468c
Content-Type: application/json

{
  "name": "新商品",
  "description": "商品描述",
  "category": 1,
  "price": "1999.00",
  "stock": 10,
  "status": "onsale"
}
```

## 前端集成範例

### 獲取商品列表
```javascript
// 將硬編碼數據替換為API調用
fetch('http://127.0.0.1:8000/api/products/products/')
  .then(res => res.json())
  .then(data => {
    const products = data.results;
    // 更新前端UI
  });
```

### 提交訂單
```javascript
fetch('http://127.0.0.1:8000/api/products/orders/create_order/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Token ' + userToken
  },
  body: JSON.stringify({
    product_id: productId,
    quantity: quantity,
    recipient_name: name,
    recipient_phone: phone,
    recipient_address: address,
    payment_method: paymentMethod
  })
})
.then(res => res.json())
.then(data => {
  if (data.success) {
    console.log('訂單號:', data.order_number);
  }
});
```

## CORS 配置
已在 `settings.py` 配置允許的來源：
- `http://localhost:3000`
- `http://127.0.0.1:3000`

如需其他來源，請更新 `CORS_ALLOWED_ORIGINS`

## 認證方式

### Token 認證
```
Authorization: Token 6db636c007b6fe1b41d3a8e7bd0bbe5f1793468c
```

### Session 認證
登錄後自動設置 Django Session，同一瀏覽器可直接訪問受保護的資源

## 常見問題

**Q: 如何添加商品圖片？**
A: 商品圖片支持通過 `multipart/form-data` 上傳，映射到 `media/products/` 目錄

**Q: 如何支持多語言？**
A: 當前支持繁體中文，可通過 Django 的翻譯框架擴展

**Q: 前端應該用什麼方式存儲 Token？**
A: 推薦存在 `localStorage` 中，但生產環境應考慮安全性（HttpOnly Cookie 更安全）

## 下一步開發計劃
- [ ] JWT 令牌認證（更安全的替代方案）
- [ ] 文件上傳功能實現
- [ ] 支付網關集成（信用卡、LINE Pay）
- [ ] 圖片處理和縮略圖
- [ ] 訂單搜尋和篩選
- [ ] 評分和評論系統
- [ ] 購物車功能
- [ ] 收藏夾功能
