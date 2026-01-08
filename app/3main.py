from flask import Flask, render_template, request
import sqlite3, os

# =====================
# 設定
# =====================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "DB", "date.db")

app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "static"),
    template_folder=os.path.join(BASE_DIR, "templates")
)

print("📁 BASE_DIR =", BASE_DIR)
print("📁 DB_PATH =", DB_PATH)


# =====================
# DB検索（超単純）
# =====================
def query_db(keyword, categories):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    sql = """
        SELECT "group", number, name, enerc_kcal, prot_, fat_, choavlm,
               na, k, ca, mg, p, fe
        FROM items
        WHERE 1=1
    """
    params = []

    # 名前検索
    if keyword:
        sql += " AND name LIKE ?"
        params.append(f"%{keyword}%")

    # グループ完全一致（←ここが肝）
    if categories:
        placeholders = ",".join("?" for _ in categories)
        sql += f' AND "group" IN ({placeholders})'
        params.extend([int(c) for c in categories])  # ★ 数値に変換

    print("🧠 SQL:", sql)
    print("🧠 params:", params)

    cur.execute(sql, params)
    rows = cur.fetchall()
    conn.close()
    return rows


# =====================
# ルーティング
# =====================
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    keyword = request.form.get("keyword", "").strip()
    categories = request.form.getlist("category[]")

    print("🔍 keyword:", keyword)
    print("📂 categories:", categories)

    rows = query_db(keyword, categories)

    return render_template(
        "page/search_result.html",
        rows=rows,
        keyword=keyword,
        categories=categories
    )
    
@app.route("/what")
def what():
    return render_template("what.html")



# =====================
# 起動
# =====================
if __name__ == "__main__":
    app.run(debug=True)
