from flask import Flask, render_template, request
import sqlite3, os

# --- 設定 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))        # app/
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "DB", "date.db"))
TEMPLATE_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "templates"))  # templates をルートに設定
print("📁 DB_PATH =", DB_PATH)
print("📁 TEMPLATE_DIR =", TEMPLATE_DIR)

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, 'static'),
    template_folder=os.path.join(BASE_DIR, 'templates')
)


# --- DB検索関数 ---
def query_db(keyword):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT "group", number, name, enerc_kcal, prot_, fat_, choavlm, na, k, ca, mg, p, fe
        FROM items
        WHERE name LIKE ?
    """, (f'%{keyword}%',))
    rows = cur.fetchall()
    conn.close()
    return rows

# --- トップページ（検索フォーム） ---
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')  # templates/index.html を参照

# --- 検索結果ページ ---
@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    rows = query_db(keyword)
    return render_template('page/search_result.html', rows=rows, keyword=keyword)

# --- その他の静的ページ ---
@app.route('/what')
def what():
    return render_template('page/what.html')

# --- その他の静的ページ ---
@app.route('/help')
def help():
    return render_template('page/help.html')

# --- その他の静的ページ ---
@app.route('/answer')
def answer():
    return render_template('page/answer.html')

# @app.route('/diet')
# def diet():
#     type_filter = request.args.get('type', '')
#     rows = query_db("")  # DB から全件取得

#     if type_filter == 'muscle':
#         # 筋トレ向けフィルター例: タンパク質>15, 脂質<5
#         rows = [r for r in rows if r[4] > 15 and r[5] < 5]

#     return render_template('page/diet.html', rows=rows)

# --- ダイエットページ ---
@app.route('/diet')
def diet():
    return render_template('page/diet.html', rows=rows)

# --- お気に入りページ ---
@app.route('/favorites')
def favorites():
    # 全件取得して後で JS で ★だけ表示
    rows = query_db("")
    return render_template('page/favorites.html', rows=rows)

# --- PFC比較ページ ---
@app.route("/pfc-compare")
def pfc_compare():
    return render_template("page/pfc-compare.html")

# --- ページグループ化ページ ---
@app.route("/group-manage")
def group_manage():
    return render_template("page/group-manage.html")

# --- グループ化ページ ---
@app.route("/group-create")
def group_create():
    return render_template("page/group-create.html")

# --- グループ化ページ ---
@app.route("/group-view")
def group_view():
    return render_template("page/group-view.html")


if __name__ == '__main__':
    app.run(debug=True, port=5001)

app.config['TEMPLATES_AUTO_RELOAD'] = True

