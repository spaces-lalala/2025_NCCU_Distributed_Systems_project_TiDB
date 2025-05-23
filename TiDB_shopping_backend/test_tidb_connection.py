from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# 載入 .env 的環境變數
load_dotenv()

# 取得 DATABASE_URL（來自 .env）
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL 環境變數不存在，請確認 .env 檔案是否設定正確。")

try:
    # 建立資料庫連線
    engine = create_engine(DATABASE_URL, echo=True)

    # 開始連線測試
    with engine.connect() as connection:
        result = connection.execute(text("SELECT NOW();"))
        print("✅ 成功連線到 TiDB！目前時間：", result.scalar())

except Exception as e:
    print("❌ 連線失敗：", e)
