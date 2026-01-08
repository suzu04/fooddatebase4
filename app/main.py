from flask import Flask, render_template, request
import sqlite3
import os

# =========================
# パス設定
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "DB", "date.db")

print("📁 BASE_DIR =", BASE_DIR)
print("📁 DB_PATH =", DB_PATH)

app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "static"),
    template_folder=os.path.join(BASE_DIR, "templates")
)

app.config["TEMPLATES_AUTO_RELOAD"] = True


# =========================
# DB検索関数（カテゴリ対応）
# =========================
def query_db(keyword="", categories=None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

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

    # キーワード検索
    if keyword:
        sql += " AND name LIKE ?"
        params.append(f"%{keyword}%")

    # カテゴリ検索
    if categories:
        placeholders = ",".join("?" for _ in categories)
        sql += f' AND "group" IN ({placeholders})'
        params.extend(categories)

    cur.execute(sql, params)
    rows = cur.fetchall()
    conn.close()
    return rows


# =========================
# トップページ
# =========================
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# =========================
# 検索結果ページ
# =========================
@app.route("/search", methods=["POST"])
def search():
    keyword = request.form.get("keyword", "")
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


# =========================
# 静的ページ
# =========================
@app.route("/what")
def what():
    return render_template("page/what.html")


@app.route("/help")
def help():
    return render_template("page/help.html")


@app.route("/answer")
def answer():
    return render_template("page/answer.html")


# =========================
# ダイエットページ（仮）
# =========================
@app.route("/diet")
def diet():
    rows = query_db()
    return render_template("page/diet.html", rows=rows)


# =========================
# お気に入り
# =========================
@app.route("/favorites")
def favorites():
    rows = query_db()
    return render_template("page/favorites.html", rows=rows)


# =========================
# PFC比較
# =========================
@app.route("/pfc-compare")
def pfc_compare():
    return render_template("page/pfc-compare.html")


# =========================
# グループ管理
# =========================
@app.route("/group-manage")
def group_manage():
    return render_template("page/group-manage.html")


@app.route("/group-create")
def group_create():
    return render_template("page/group-create.html")


@app.route("/group-view")
def group_view():
    return render_template("page/group-view.html")


# =========================
# 起動
# =========================
if __name__ == "__main__":
    app.run(debug=True, port=5000)
