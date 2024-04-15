from tkinter import simpledialog
from typing import Optional, Tuple
import tkinter as tk
import re


class SizeChangeDialog(simpledialog.Dialog):

    # 相方となるEntryと入力後になる予定の文字列が両方存在しているときにのみOKボタンを有効化する
    def judgeSwitchOKButtonByVerticalEntry(self, edited_str):
        if self.horizon_entry.get() and edited_str:
            self.ok_button["state"] = tk.NORMAL
        else:
            self.ok_button["state"] = tk.DISABLED
        return self.validateEntry(edited_str)

    def judgeSwitchOKButtonByHorizonEntry(self, edited_str):
        if self.vertical_entry.get() and edited_str:
            self.ok_button["state"] = tk.NORMAL
        else:
            self.ok_button["state"] = tk.DISABLED
        return self.validateEntry(edited_str)

    # 数字の入力と文字の削除しか受け付けないようにする
    def validateEntry(self, edited_str):
        if re.fullmatch(re.compile("[0-9]+"), edited_str) or not edited_str:
            return True
        else:
            # 入力をキャンセルする際、入力前の状態でOKボタンの状態を再度決定する
            if self.vertical_entry.get() and self.horizon_entry.get():
                self.ok_button["state"] = tk.NORMAL
            else:
                self.ok_button["state"] = tk.DISABLED
            return False

    def __init__(self, master):
        self.size = None
        super().__init__(parent=master, title="サイズ変更")

    def body(self, master):
        vertical_val_cmd = self.register(self.judgeSwitchOKButtonByVerticalEntry)
        horizon_val_cmd = self.register(self.judgeSwitchOKButtonByHorizonEntry)
        self.vertical_entry: tk.Entry = tk.Entry(master, width=10, validate="key",
                                                 validatecommand=(vertical_val_cmd, "%P"))
        self.horizon_entry: tk.Entry = tk.Entry(master, width=10, validate="key",
                                                validatecommand=(horizon_val_cmd, "%P"))
        self.vertical_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.horizon_entry.pack(side=tk.LEFT, padx=5, pady=5)

    def buttonbox(self):
        box = tk.Frame(self)

        self.ok_button = tk.Button(box, text="OK", width=10, command=self.ok, state=tk.DISABLED)
        self.ok_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.cancel_button = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        self.cancel_button.pack(side=tk.LEFT, padx=5, pady=5)

        box.pack()

    # get_sizeで呼び出されたときのみ戻り値を返し、OKボタンで閉じた場合のみ戻り値の中身が設定されている
    def apply(self):
        self.size = int(self.vertical_entry.get()), int(self.horizon_entry.get())

    def get_size(self) -> Optional[Tuple[int, int]]:

        return self.size
