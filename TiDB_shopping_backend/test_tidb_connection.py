from sqlalchemy import create_engine, text

# 資料庫連線字串
db_url = "mysql+pymysql://root@127.0.0.1:4000/shopping_db"

# 建立資料庫引擎
engine = create_engine(db_url)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SHOW TABLES"))
        print("✅ 成功連接資料庫，以下是目前的資料表：")
        for row in result:
            print("-", row[0])
except Exception as e:
    print("❌ 連接失敗：", e)
