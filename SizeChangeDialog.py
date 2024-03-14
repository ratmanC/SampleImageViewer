from tkinter import simpledialog
from typing import Optional, Tuple
import tkinter as tk
import re


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
