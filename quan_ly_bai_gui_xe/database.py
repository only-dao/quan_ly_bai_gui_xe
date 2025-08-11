import sqlite3

def tao_ket_noi():
    """Tạo kết nối đến cơ sở dữ liệu."""
    ket_noi = sqlite3.connect('quan_ly_bai_gui_xe.db')
    return ket_noi

def khoi_tao_csdl():
    """Khởi tạo cơ sở dữ liệu và tạo bảng nếu chưa tồn tại."""
    ket_noi = tao_ket_noi()
    con_tro = ket_noi.cursor()
    con_tro.execute('''
    CREATE TABLE IF NOT EXISTS nguoi_dung (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ten_dang_nhap TEXT NOT NULL UNIQUE,
        mat_khau TEXT NOT NULL
    )
    ''')
    con_tro.execute('''
    CREATE TABLE IF NOT EXISTS xe (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bien_so TEXT NOT NULL,
        loai_xe TEXT NOT NULL,
        thoi_gian_vao DATETIME,
        thoi_gian_ra DATETIME,
        loai_thanh_toan TEXT NOT NULL,
        han_ve_thang DATETIME
    )
    ''')
    con_tro.execute('''
    CREATE TABLE IF NOT EXISTS ve_thang (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bien_so TEXT NOT NULL UNIQUE,
        loai_xe TEXT NOT NULL,
        ngay_bat_dau DATETIME NOT NULL,
        ngay_ket_thuc DATETIME NOT NULL
    )
    ''')
    ket_noi.commit()
    ket_noi.close()