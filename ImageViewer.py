import re
import tkinter as tk
import tkinter.filedialog as fd
from tkinter import simpledialog
from PIL import Image, ImageTk
from typing import Optional, Tuple

from Stack import Stack


class ImageData:
    now_image: Image = None
    first_image: Image = None
    monochrome: bool = False
    rotate: int = 0

    def reset(self):
        self.rotate = 0
        self.monochrome = False


class SizeChangeDialog(simpledialog.Dialog):
    def verticalSwitchButtonValidate(self, s):
        if self.horizon_entry.get() and s:
            self.button1["state"] = tk.NORMAL
        else:
            self.button1["state"] = tk.DISABLED
        return self.validater(s)

    def horizonSwitchButtonValidate(self, s):
        if self.vertical_entry.get() and s:
            self.button1["state"] = tk.NORMAL
        else:
            self.button1["state"] = tk.DISABLED
        return self.validater(s)

    @staticmethod
    def validater(s):
        if re.fullmatch(re.compile("[0-9]+"), s) or not s:
            return True
        else:
            return False

    def __init__(self, master):
        self.size = None
        super().__init__(parent=master, title="サイズ変更")

    def body(self, master):
        vcmd = self.register(self.verticalSwitchButtonValidate)
        hcmd = self.register(self.horizonSwitchButtonValidate)
        self.vertical_entry: tk.Entry = tk.Entry(master, width=10, validate="key",
                                                 validatecommand=(vcmd, "%P"))
        self.vertical_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.horizon_entry: tk.Entry = tk.Entry(master, width=10, validate="key",
                                                validatecommand=(hcmd, "%P"))
        self.horizon_entry.pack(side=tk.LEFT, padx=5, pady=5)

    def buttonbox(self):
        box = tk.Frame(self)

        self.button1 = tk.Button(box, text="OK", width=10, command=self.ok, state=tk.DISABLED)
        self.button1.pack(side=tk.LEFT, padx=5, pady=5)
        self.button2 = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        self.button2.pack(side=tk.LEFT, padx=5, pady=5)

        box.pack()

    # 戻り値の設定
    def apply(self):
        self.size = int(self.vertical_entry.get()), int(self.horizon_entry.get())

    def get_size(self) -> Optional[Tuple]:

        return self.size


# ウィンドウの作成
root = tk.Tk()
root.minsize(width=300, height=400)
root.maxsize(width=root.winfo_screenwidth(), height=root.winfo_screenheight())
root.geometry("500x450")
menubar = tk.Menu(root)
root.config(menu=menubar)
root.title("画像表示アプリ")

# 画像の状態を扱うインスタンスの作成
now = ImageData()
img_stack = Stack()


# ラベルへ画像を張り付ける
def dispLabel(new_image):
    img = ImageTk.PhotoImage(new_image)
    # ガベージコレクションで画像情報を失わないようにLabelの内部パラメータに画像の参照を持たせている
    image_lbl.configure(image=img)
    image_lbl.image = img
    # 関数終了時に描画


# フォルダを開く
def openFile():
    fpath = fd.askopenfilename()
    # 指定のアドレスが存在するなら画面に表示する
    if fpath:
        new_image = Image.open(fpath)
        now.reset()
        now.now_image = new_image
        now.first_image = new_image
        # 元になる画像が変わるためスタックも初期化を行う
        img_stack.__init__()
        img_stack.push(now.now_image)
        dispLabel(new_image)
        address_box.configure(state="normal")
        address_box.delete(0, tk.END)
        address_box.insert(tk.END, fpath)
        address_box.configure(state="readonly")


def resize():
    address_box.configure(state="normal")
    if not now.now_image:
        address_box.configure(state="readonly")
        return

    if not now.now_image.size == now.first_image.size:
        new_image = now.now_image.resize(size=now.first_image.size)
    else:
        input_size = SizeChangeDialog(root).get_size()
        print(input_size, type(input_size))
        new_image = now.now_image.resize(size=input_size)

    now.now_image = new_image
    img_stack.push(now.now_image)
    dispLabel(new_image)
    address_box.configure(state="readonly")


def monochromatize():
    address_box.configure(state="normal")
    if not now.now_image:
        address_box.configure(state="readonly")
        return

    if now.monochrome:
        new_image = now.first_image.rotate(now.rotate % 360, expand=True)
        if now.now_image.size != now.first_image.size:
            new_image = new_image.resize(size=now.now_image.size)
        now.monochrome = False
    else:
        new_image = now.now_image.convert("L")
        now.monochrome = True
    now.now_image = new_image
    img_stack.push(now.now_image)
    dispLabel(new_image)
    address_box.configure(state="readonly")


# 90度ずつ回転処理
def turnLeft():
    address_box.configure(state="normal")
    if not now.now_image:
        address_box.configure(state="readonly")
        return
    new_image = now.now_image.rotate(90, expand=True)
    now.rotate += 90
    now.now_image = new_image
    img_stack.push(now.now_image)
    dispLabel(new_image)
    address_box.configure(state="readonly")


def turnRight():
    address_box.configure(state="normal")
    if not now.now_image:
        address_box.configure(state="readonly")
        return
    new_image = now.now_image.rotate(-90, expand=True)
    now.rotate -= 90
    now.now_image = new_image
    img_stack.push(now.now_image)
    dispLabel(new_image)
    address_box.configure(state="readonly")


"""
ショートカットキーで呼び出す関数は引数を受け取る必要があるが、ツールバーから呼び出した際は
引数が発生しないためデフォルト引数でNoneにしておく
"""


# 元に戻す・やり直す処理
def undo(event=None):
    address_box.configure(state="normal")
    new_image = img_stack.undoPop()
    if not now.now_image or not new_image:
        address_box.configure(state="readonly")
        return
    now.now_image = new_image
    dispLabel(new_image)
    address_box.configure(state="readonly")


def redo(event=None):
    address_box.configure(state="normal")
    new_image = img_stack.redoPop()
    if not now.now_image or not new_image:
        address_box.configure(state="readonly")
        return
    now.now_image = new_image
    dispLabel(new_image)
    address_box.configure(state="readonly")


# ボタン等の作成
address_box = tk.Entry(state="readonly")
open_btn = tk.Button(text="画像を開く", command=openFile)
change_btn = tk.Button(text="画像を変える", command=openFile)
resize_btn = tk.Button(text="リサイズ", command=resize)
monochrome_btn = tk.Button(text="モノクロ", command=monochromatize)
turn_l_btn = tk.Button(text="↺", command=turnLeft)
turn_r_btn = tk.Button(text="↻", command=turnRight)
image_lbl = tk.Label(relief="sunken")

# メニューバーの設置
edit_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="編集", menu=edit_menu)
edit_menu.add_command(label="Undo", command=undo, accelerator="Ctrl+Z")
edit_menu.add_command(label="Redo", command=redo, accelerator="Ctrl+Y")

# ショートカットキーの設定
root.bind("<Control-z>", undo)
root.bind("<Control-y>", redo)

# ボタン等の設置
image_lbl.pack()
address_box.pack()
open_btn.pack()
change_btn.pack(side="left", anchor=tk.SW)
resize_btn.pack(side="left", anchor=tk.SW)
monochrome_btn.pack(side="left", anchor=tk.SW)
turn_l_btn.pack(side="left", anchor=tk.SW)
turn_r_btn.pack(side="left", anchor=tk.SW)

tk.mainloop()
