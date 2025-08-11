from datetime import datetime, timedelta
from database import tao_ket_noi
import sqlite3


class Xe:
    @staticmethod
    def kiem_tra_bien_so(bien_so):
        ket_noi = tao_ket_noi()
        con_tro = ket_noi.cursor()
        con_tro.execute('SELECT id FROM xe WHERE bien_so = ? AND thoi_gian_ra IS NULL', (bien_so,))
        xe = con_tro.fetchone()
        ket_noi.close()
        return xe is not None

    @staticmethod
    def them_xe(bien_so, loai_xe, loai_thanh_toan):
        if Xe.kiem_tra_bien_so(bien_so):
            return "Biển số đã tồn tại trong bãi."

        ket_noi = tao_ket_noi()
        con_tro = ket_noi.cursor()
        thoi_gian_vao = datetime.now()
        han_ve_thang = None
        if loai_thanh_toan == 'thang':
            han_ve_thang = datetime.now().replace(day=1, month=thoi_gian_vao.month + 1)
        con_tro.execute('''
        INSERT INTO xe (bien_so, loai_xe, thoi_gian_vao, loai_thanh_toan, han_ve_thang)
        VALUES (?, ?, ?, ?, ?)
        ''', (bien_so, loai_xe, thoi_gian_vao, loai_thanh_toan, han_ve_thang))
        ket_noi.commit()
        ket_noi.close()
        return "Thêm xe thành công."

    @staticmethod
    def tinh_phi(id_hoac_bien_so):
        ket_noi = tao_ket_noi()
        con_tro = ket_noi.cursor()
        try:
            id_xe = int(id_hoac_bien_so)
            con_tro.execute(
                'SELECT id, thoi_gian_vao, loai_thanh_toan, han_ve_thang, loai_xe FROM xe WHERE id = ? AND thoi_gian_ra IS NULL',
                (id_xe,))
        except ValueError:
            con_tro.execute(
                'SELECT id, thoi_gian_vao, loai_thanh_toan, han_ve_thang, loai_xe FROM xe WHERE bien_so = ? AND thoi_gian_ra IS NULL',
                (id_hoac_bien_so,))

        xe = con_tro.fetchone()
        if not xe:
            ket_noi.close()
            return "Xe không có trong bãi hoặc đã ra khỏi bãi."

        id_xe = xe[0]
        thoi_gian_vao = datetime.strptime(xe[1], '%Y-%m-%d %H:%M:%S.%f')
        loai_thanh_toan = xe[2]
        han_ve_thang = xe[3]
        loai_xe = xe[4]

        if loai_thanh_toan == 'thang':
            if han_ve_thang and datetime.now() < datetime.strptime(han_ve_thang, '%Y-%m-%d %H:%M:%S.%f'):
                ket_noi.close()
                return "Xe có vé tháng, không cần thanh toán."
            else:
                ket_noi.close()
                return "Vé tháng đã hết hạn, vui lòng gia hạn."
        else:
            thoi_gian_ra = datetime.now()
            thoi_gian_gui = (thoi_gian_ra - thoi_gian_vao).total_seconds() / 3600
            so_buoi = int(thoi_gian_gui // 4) + 1

            if loai_xe == "Xe máy":
                phi = so_buoi * 5000
            elif loai_xe == "Ô tô":
                phi = so_buoi * 40000
            else:
                phi = 0
            con_tro.execute('UPDATE xe SET thoi_gian_ra = ? WHERE id = ?', (thoi_gian_ra, id_xe))
            ket_noi.commit()
            ket_noi.close()
            return f"Phí gửi xe là: {phi:.2f} VND (số buổi: {so_buoi}). Xe đã được xóa khỏi bãi gửi."

    @staticmethod
    def danh_sach_xe():
        ket_noi = tao_ket_noi()
        con_tro = ket_noi.cursor()
        con_tro.execute(
            'SELECT id, bien_so, loai_xe, thoi_gian_vao, loai_thanh_toan FROM xe WHERE thoi_gian_ra IS NULL')
        danh_sach = con_tro.fetchall()
        ket_noi.close()
        return danh_sach

    @staticmethod
    def xoa_xe(id_xe):
        ket_noi = tao_ket_noi()
        con_tro = ket_noi.cursor()
        thoi_gian_ra = datetime.now()
        con_tro.execute('UPDATE xe SET thoi_gian_ra = ? WHERE id = ?', (thoi_gian_ra, id_xe))
        ket_noi.commit()
        ket_noi.close()
        return f"Xe có ID {id_xe} đã được xóa khỏi bãi gửi."

    @staticmethod
    def tim_kiem_xe(bien_so_hoac_id):
        ket_noi = tao_ket_noi()
        con_tro = ket_noi.cursor()
        try:
            id_xe = int(bien_so_hoac_id)
            con_tro.execute('SELECT * FROM xe WHERE id = ?', (id_xe,))
        except ValueError:
            con_tro.execute('SELECT * FROM xe WHERE bien_so = ?', (bien_so_hoac_id,))
        xe = con_tro.fetchone()
        ket_noi.close()
        return xe

    @staticmethod
    def lay_lich_su_vao():
        ket_noi = tao_ket_noi()
        con_tro = ket_noi.cursor()
        con_tro.execute('SELECT id, bien_so, loai_xe, thoi_gian_vao FROM xe ORDER BY thoi_gian_vao DESC')
        lich_su = con_tro.fetchall()
        ket_noi.close()
        return lich_su

    @staticmethod
    def lay_lich_su_ra():
        ket_noi = tao_ket_noi()
        con_tro = ket_noi.cursor()
        con_tro.execute(
            'SELECT id, bien_so, loai_xe, thoi_gian_ra FROM xe WHERE thoi_gian_ra IS NOT NULL ORDER BY thoi_gian_ra DESC')
        lich_su = con_tro.fetchall()
        ket_noi.close()
        return lich_su


class VeThang:
    @staticmethod
    def tao_ve_thang(bien_so, loai_xe, thoi_han):
        ket_noi = tao_ket_noi()
        con_tro = ket_noi.cursor()
        ngay_bat_dau = datetime.now()
        ngay_ket_thuc = ngay_bat_dau + timedelta(days=30 * thoi_han)
        try:
            con_tro.execute('''
            INSERT INTO ve_thang (bien_so, loai_xe, ngay_bat_dau, ngay_ket_thuc)
            VALUES (?, ?, ?, ?)
            ''', (bien_so, loai_xe, ngay_bat_dau, ngay_ket_thuc))
            ket_noi.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            ket_noi.close()

    @staticmethod
    def sua_ve_thang(id_ve_thang, bien_so_moi=None, loai_xe_moi=None, thoi_han_moi=None):
        ket_noi = tao_ket_noi()
        con_tro = ket_noi.cursor()
        try:
            if bien_so_moi:
                con_tro.execute('UPDATE ve_thang SET bien_so = ? WHERE id = ?', (bien_so_moi, id_ve_thang))
            if loai_xe_moi:
                con_tro.execute('UPDATE ve_thang SET loai_xe = ? WHERE id = ?', (loai_xe_moi, id_ve_thang))
            if thoi_han_moi:
                ngay_ket_thuc = datetime.now() + timedelta(days=30 * thoi_han_moi)
                con_tro.execute('UPDATE ve_thang SET ngay_ket_thuc = ? WHERE id = ?', (ngay_ket_thuc, id_ve_thang))
            ket_noi.commit()
            return True
        except Exception as e:
            print(f"Lỗi khi sửa vé tháng: {e}")
            return False
        finally:
            ket_noi.close()

    @staticmethod
    def xoa_ve_thang(id_ve_thang):
        ket_noi = tao_ket_noi()
        con_tro = ket_noi.cursor()
        con_tro.execute('DELETE FROM ve_thang WHERE id = ?', (id_ve_thang,))
        ket_noi.commit()
        ket_noi.close()

    @staticmethod
    def lay_danh_sach_ve_thang():
        ket_noi = tao_ket_noi()
        con_tro = ket_noi.cursor()
        con_tro.execute('SELECT * FROM ve_thang')
        danh_sach = con_tro.fetchall()
        ket_noi.close()
        return danh_sach