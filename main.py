import tkinter as tk
from tkinter import filedialog, scrolledtext
import platform

class SimpleIDE:
    def __init__(self, master):
        self.master = master
        self.master.title("SimpleIDE")

        self.text_area = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, undo=True)
        self.text_area.pack(expand=True, fill='both')

        self.output_area = scrolledtext.ScrolledText(self.master, wrap=tk.WORD)
        self.output_area.pack(expand=True, fill='both')

        self.menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.menu_bar)

        # File Menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.create_file_menu()

        # Edit Menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.text_area.edit_undo)
        self.edit_menu.add_command(label="Redo", command=self.text_area.edit_redo)

        # Run Menu
        self.run_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="Run", menu=self.run_menu)
        self.run_menu.add_command(label="Run", command=self.run_code)

    def create_file_menu(self):
        self.file_menu.add_command(label="New", accelerator="Cmd+N" if platform.system() == 'Darwin' else "Ctrl+N", command=self.new_file)
        self.file_menu.add_command(label="Open", accelerator="Cmd+O" if platform.system() == 'Darwin' else "Ctrl+O", command=self.open_file)
        self.file_menu.add_command(label="Save", accelerator="Cmd+S" if platform.system() == 'Darwin' else "Ctrl+S", command=self.save_file)
        self.file_menu.add_command(label="Save As", accelerator="Cmd+Shift+S" if platform.system() == 'Darwin' else "Ctrl+Shift+S", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", accelerator="Cmd+Q" if platform.system() == 'Darwin' else "Alt+F4", command=self.exit_editor)

        self.master.bind_all("<Command-n>" if platform.system() == 'Darwin' else "<Control-n>", self.new_file)
        self.master.bind_all("<Command-o>" if platform.system() == 'Darwin' else "<Control-o>", self.open_file)
        self.master.bind_all("<Command-s>" if platform.system() == 'Darwin' else "<Control-s>", self.save_file)
        self.master.bind_all("<Command-Shift-s>" if platform.system() == 'Darwin' else "<Control-Shift-s>", self.save_as_file)
        self.master.bind_all("<Command-q>" if platform.system() == 'Darwin' else "<Alt-F4>", self.exit_editor)

    def new_file(self, event=None):
        self.text_area.delete(1.0, tk.END)

    def open_file(self, event=None):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)

    def save_file(self, event=None):
        if not self.file_path:
            self.save_as_file()
        else:
            with open(self.file_path, "w") as file:
                content = self.text_area.get(1.0, tk.END)
                file.write(content)

    def save_as_file(self, event=None):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                content = self.text_area.get(1.0, tk.END)
                file.write(content)
            self.file_path = file_path

    def exit_editor(self, event=None):
        self.master.destroy()

    def run_code(self):
        code = self.text_area.get(1.0, tk.END)
        output = self.execute_code(code)
        self.output_area.delete(1.0, tk.END)
        self.output_area.insert(tk.END, output)

    def execute_code(self, code):
        try:
            # Execute the code using eval() and capture the output
            output = eval(code)
            return str(output)
        except Exception as e:
            return str(e)

def main():
    root = tk.Tk()
    app = SimpleIDE(root)
    root.mainloop()

if __name__ == "__main__":
    main()
