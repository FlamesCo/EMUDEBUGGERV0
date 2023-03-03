import tkinter as tk
from tkinter import filedialog
import os
import shutil

class DevkitProCompilerDebugger:
    def __init__(self, root, platform):
        self.root = root
        self.platform = platform
        self.root.title(f"DevkitPro {self.platform} Compiler and Debugger")
        self.root.geometry("800x600")

        self.file_path = ""

        self.build_button = tk.Button(text="Build", command=self.build)
        self.build_button.pack()

        self.debug_button = tk.Button(text="Debug", command=self.debug)
        self.debug_button.pack()

    def build(self):
        self.file_path = filedialog.askopenfilename(initialdir = ".", title = "Select file", filetypes = (("C files", ".c"), ("all files", ".*")))
        if self.platform == "nes":
            self.executable_path = self.file_path.split('.')[0] + ".nes"
            assembler = "ca65"
            linker = "ld65"
            ld_config = "nes.cfg"
            ld_opts = "-C"
        elif self.platform == "switch":
            self.executable_path = self.file_path.split('.')[0] + ".nro"
            assembler = "aarch64-none-elf-gcc"
            linker = "nxlink"
            ld_config = "switch.ld"
            ld_opts = "-o"

        dkp_path = os.environ.get("DEVKITPRO")
        if dkp_path is None:
            tk.messagebox.showerror("Error", "DevkitPro not found. Please install devkitPro.")
            return

        devkitpro_bin_path = os.path.join(dkp_path, "tools", "bin")
        if not os.path.isdir(devkitpro_bin_path):
            tk.messagebox.showerror("Error", "DevkitPro tools not found. Please check that DEVKITPRO environment variable is set correctly.")
            return

        toolchain_bin_path = os.path.join(dkp_path, f"devkit{self.platform.capitalize()}", "bin")
        if not os.path.isdir(toolchain_bin_path):
            tk.messagebox.showerror("Error", f"DevkitPro {self.platform} toolchain not found. Please check that DEVKITPRO environment variable is set correctly.")
            return

        os.makedirs("out", exist_ok=True)
        os.system(f"{toolchain_bin_path}/{assembler} -o {self.executable_path}.o {self.file_path}")
        os.system(f"{toolchain_bin_path}/{linker} {ld_opts} {ld_config} -o {self.executable_path} {self.executable_path}.o")

    def debug(self):
        if self.platform == "nes":
            debugger = "fceux"
        elif self.platform == "switch":
            debugger = "gdb"

        debugger_path = shutil.which(debugger)
        if debugger_path is None:
            tk.messagebox.showerror("Error", f"{debugger} not found. Please install the appropriate debugger.")
            return

        os.system(f"{debugger_path} {self.executable_path}")

root = tk.Tk()

nes_app = DevkitProCompilerDebugger(root, "nes")
nes_app.build_button.config(text="Assemble")
nes_app.root.title("DevkitPro NES Assembler and Debugger")

switch_app = DevkitProCompilerDebugger(root, "switch")
switch_app.root.title("DevkitPro Switch Compiler and Debugger")

root.mainloop()
