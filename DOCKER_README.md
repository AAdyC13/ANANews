# ANANews Docker 部署指南

## 開發環境

### 快速啟動

```bash
# 構建並啟動所有服務
docker-compose up --build

# 後台運行
docker-compose up -d --build
```

### 訪問應用

- 應用地址: http://localhost:8000
- Redis: localhost:6379

### 常用命令

```bash
# 查看日誌
docker-compose logs -f web

# 進入容器
docker-compose exec web bash

# 停止服務
docker-compose down

# 清理所有數據
docker-compose down -v
```

## 生產環境

### 部署

```bash
# 使用生產配置啟動
docker-compose -f docker-compose.prod.yml up -d --build
```

### 訪問應用

- 應用地址: http://localhost

### 維護命令

```bash
# 查看狀態
docker-compose -f docker-compose.prod.yml ps

# 更新應用
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d --build

# 備份數據
docker-compose -f docker-compose.prod.yml exec redis redis-cli BGSAVE
```

## 環境變量

可以創建 `.env` 文件來配置環境變量：

```env
DEBUG=True
SECRET_KEY=your-secret-key
REDIS_URL=redis://redis:6379/1
```

## 疑難排解

### 常見問題

1. 端口被佔用：修改 docker-compose.yml 中的端口映射
2. Redis 連接失敗：確保 Redis 服務正常啟動
3. 靜態文件 404：運行 `docker-compose exec web python manage.py collectstatic`

### 查看日誌

```bash
# 查看所有服務日誌
docker-compose logs

# 查看特定服務日誌
docker-compose logs web
docker-compose logs redis
docker-compose logs celery
```
