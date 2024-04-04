from tkinter import simpledialog
from typing import Optional, Tuple
import tkinter as tk
import re


class SizeChangeDialog(simpledialog.Dialog):

    # 相方となるEntryと入力後になる予定の文字列が両方存在しているときにのみOKボタンを有効化する
    def verticalEntrySwitchOKButtonValidate(self, editedstr):
        if self.horizon_entry.get() and editedstr:
            self.button1["state"] = tk.NORMAL
        else:
            self.button1["state"] = tk.DISABLED
        return self.entryValidate(editedstr)

    def horizonEntrySwitchOKButtonValidate(self, editedstr):
        if self.vertical_entry.get() and editedstr:
            self.button1["state"] = tk.NORMAL
        else:
            self.button1["state"] = tk.DISABLED
        return self.entryValidate(editedstr)

    # 数字の入力と文字の削除しか受け付けないようにする
    def entryValidate(self, editedstr):
        if re.fullmatch(re.compile("[0-9]+"), editedstr) or not editedstr:
            return True
        else:
            # 入力をキャンセルする際、入力前の状態でOKボタンの状態を再度決定する
            if self.vertical_entry.get() and self.horizon_entry.get():
                self.button1["state"] = tk.NORMAL
            else:
                self.button1["state"] = tk.DISABLED
            return False

    def __init__(self, master):
        self.size = None
        super().__init__(parent=master, title="サイズ変更")

    def body(self, master):
        vertical_val_cmd = self.register(self.verticalEntrySwitchOKButtonValidate)
        horizon_val_cmd = self.register(self.horizonEntrySwitchOKButtonValidate)
        self.vertical_entry: tk.Entry = tk.Entry(master, width=10, validate="key",
                                                 validatecommand=(vertical_val_cmd, "%P"))
        self.horizon_entry: tk.Entry = tk.Entry(master, width=10, validate="key",
                                                validatecommand=(horizon_val_cmd, "%P"))
        self.vertical_entry.pack(side=tk.LEFT, padx=5, pady=5)
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

    def get_size(self) -> Optional[Tuple[int, int]]:

        return self.size
