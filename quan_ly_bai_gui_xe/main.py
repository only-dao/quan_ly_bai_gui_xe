from database import khoi_tao_csdl
from gui import UngDungQuanLyXe
import tkinter as tk

if __name__ == "__main__":
    khoi_tao_csdl()
    root = tk.Tk()
    app = UngDungQuanLyXe(root)
    root.mainloop()