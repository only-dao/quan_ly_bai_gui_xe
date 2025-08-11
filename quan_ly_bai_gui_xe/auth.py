from dbm import sqlite3

from database import tao_ket_noi

class XacThuc:
    @staticmethod
    def dang_ky(ten_dang_nhap, mat_khau):
        ket_noi = tao_ket_noi()
        con_tro = ket_noi.cursor()
        try:
            con_tro.execute('INSERT INTO nguoi_dung (ten_dang_nhap, mat_khau) VALUES (?, ?)', (ten_dang_nhap, mat_khau))
            ket_noi.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            ket_noi.close()

    @staticmethod
    def dang_nhap(ten_dang_nhap, mat_khau):
        ket_noi = tao_ket_noi()
        con_tro = ket_noi.cursor()
        con_tro.execute('SELECT * FROM nguoi_dung WHERE ten_dang_nhap = ? AND mat_khau = ?', (ten_dang_nhap, mat_khau))
        nguoi_dung = con_tro.fetchone()
        ket_noi.close()
        return nguoi_dung is not None