import sqlite3, csv, os, glob

os.makedirs('../DB', exist_ok=True)
conn = sqlite3.connect('../DB/date.db')
cur = conn.cursor()

csv_files = glob.glob('../CSVfile/*.csv')
for file in csv_files:
    print(f"📂 読み込み中: {os.path.abspath(file)}")
    with open(file, encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)

        # 🔧 空白・重複列名を自動修正
        seen = {}
        clean_headers = []
        for i, h in enumerate(headers):
            if not h.strip():  # 空文字列だった場合
                h = f"col_{i+1}"
            elif h in seen:
                seen[h] += 1
                h = f"{h}_{seen[h]}"
            else:
                seen[h] = 1
            clean_headers.append(h)

        # テーブル作成
        cur.execute('DROP TABLE IF EXISTS items')
        columns = ', '.join([f'"{h}" TEXT' for h in clean_headers])
        cur.execute(f'CREATE TABLE items ({columns})')

        # データ挿入
        for row in reader:
            values = [v.strip() for v in row]
            cur.execute(f'INSERT INTO items VALUES ({",".join(["?"] * len(values))})', values)

conn.commit()
conn.close()

print("✅ DB作成完了：../DB/date.db にデータを登録しました。")
