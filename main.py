import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, simpledialog, font
import platform
import keyword
import re

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
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Find and Replace", command=self.find_and_replace)
        self.edit_menu.add_command(label="Word Count", command=self.word_count)
        self.edit_menu.add_command(label="Change Font Size", command=self.change_font_size)

        # Run Menu
        self.run_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="Run", menu=self.run_menu)
        self.run_menu.add_command(label="Run", command=self.run_code)

        # Format Menu
        self.format_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="Format", menu=self.format_menu)
        self.format_menu.add_command(label="Indent Code", command=self.indent_code)

        # Syntax Highlighting
        self.text_area.tag_configure("keyword", foreground="blue")
        self.highlight_syntax()

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

    def highlight_syntax(self):
        # Highlight Python keywords
        for key in keyword.kwlist:
            self.text_area.tag_configure(key, foreground="blue")
            self.highlight_pattern(key, "keyword")

    def highlight_pattern(self, pattern, tag, start="1.0", end="end", regexp=False):
        start = self.text_area.index(start)
        end = self.text_area.index(end)
        self.text_area.mark_set("matchStart", start)
        self.text_area.mark_set("matchEnd", start)
        self.text_area.mark_set("searchLimit", end)

        count = tk.IntVar()
        while True:
            index = self.text_area.search(pattern, "matchEnd","searchLimit",
                                        count=count, regexp=regexp)
            if index == "": break
            self.text_area.mark_set("matchStart", index)
            self.text_area.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.text_area.tag_add(tag, "matchStart", "matchEnd")

    def indent_code(self):
        selected_text = self.text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
        if selected_text:
            formatted_text = self.format_code(selected_text)
            self.text_area.replace(tk.SEL_FIRST, tk.SEL_LAST, formatted_text)

    def format_code(self, code):
        # Example: Indent code by adding four spaces
        lines = code.split("\n")
        formatted_lines = ["    " + line if line.strip() else "" for line in lines]
        formatted_code = "\n".join(formatted_lines)
        return formatted_code

    def find_and_replace(self):
        find_text = simpledialog.askstring("Find", "Find:")
        if find_text:
            replace_text = simpledialog.askstring("Replace", "Replace:")
            if replace_text:
                content = self.text_area.get(1.0, tk.END)
                new_content = content.replace(find_text, replace_text)
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, new_content)

    def word_count(self):
        content = self.text_area.get(1.0, tk.END)
        word_count = len(re.findall(r'\w+', content))
        messagebox.showinfo("Word Count", f"Total Words: {word_count}")

    def change_font_size(self):
        font_size = simpledialog.askinteger("Font Size", "Enter font size:")
        if font_size:
            current_font = font.Font(font=self.text_area['font'])
            self.text_area.configure(font=(current_font.actual("family"), font_size))

def main():
    root = tk.Tk()
    app = SimpleIDE(root)
    root.mainloop()

if __name__ == "__main__":
    main()
