from flask import Flask, render_template, request
import sqlite3
import os

# =========================
# パス設定
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "DB", "date.db")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

print("📁 BASE_DIR =", BASE_DIR)
print("📁 DB_PATH =", DB_PATH)

app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR
)

# =========================
# DB接続用関数
# =========================
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# =========================
# ルート
# =========================
# @app.route("/")
# def index():
#     conn = get_db_connection()
#     foods = conn.execute("SELECT * FROM items").fetchall()
#     conn.close()

#     foods_list = [dict(row) for row in foods]  # dict に変換
#     return render_template("index.html", all_foods=foods_list)

@app.route("/")
def index():
    conn = get_db_connection()
    foods = conn.execute("SELECT * FROM items").fetchall()
    conn.close()
    foods_list = [dict(f) for f in foods]
    return render_template("index.html", all_foods=foods_list)


@app.route("/what")
def what():
    return render_template("page/what.html")

@app.route("/help")
def help():
    return render_template("page/help.html")

@app.route("/answer")
def answer():
    return render_template("page/answer.html")

@app.route("/favorites")
def favorites():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM items").fetchall()
    conn.close()
    return render_template("page/favorites.html", rows=rows)

@app.route("/group-create")
def group_create():
    return render_template("page/group-create.html")

@app.route("/group-list")
def group_list():
    return render_template("page/group-list.html")

# @app.route("/group-view")
# def group_view():
#     return render_template("page/group-view.html")

@app.route("/group-view")
def group_view():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM items")
    rows = c.fetchall()
    conn.close()
    return render_template("page/group-view.html", rows=rows)



@app.route("/diet")
def diet():
    return render_template("page/diet.html")

@app.route("/pfc-compare")
def pfc_compare():
    return render_template("page/pfc-compare.html")

# =========================
# 検索
# =========================
@app.route("/search", methods=["GET", "POST"])
def search():
    keyword = request.form.get("keyword", "").strip()
    categories = request.form.getlist("category[]")

    print("🔍 keyword:", keyword)
    print("📂 categories:", categories)

    sql = """
        SELECT
            "group",
            number,
            name,
            enerc_kcal,
            prot_,
            fat_,
            choavlm,
            na,
            k,
            ca,
            mg,
            p,
            fe
        FROM items
        WHERE 1=1
    """
    params = []

    if keyword:
        sql += " AND name LIKE ?"
        params.append(f"%{keyword}%")

    if categories:
        placeholders = ",".join(["?"] * len(categories))
        sql += f' AND "group" IN ({placeholders})'
        params.extend(categories)

    print("🧠 SQL:", sql)
    print("📦 params:", params)

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sql, params)
    rows = cur.fetchall()
    conn.close()

    return render_template(
        "page/search_result.html",
        rows=rows,
        keyword=keyword,
        categories=categories
    )

# =========================
# 起動
# =========================
if __name__ == "__main__":
    app.run(debug=True)
