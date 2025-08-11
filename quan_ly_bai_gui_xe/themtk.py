import sqlite3
with sqlite3.connect("quan_ly_bai_gui_xe.db") as db:
    cur = db.cursor()
    cur.execute("""INSERT INTO nguoi_dung(
    id, ten_dang_nhap,mat_khau)
    VALUES("1","dao","123");""")
    db.commit()