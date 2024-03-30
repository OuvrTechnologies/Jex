import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, simpledialog, font, colorchooser
import platform
import keyword
import re
import tkinter.messagebox as messagebox

class SimpleIDE:
    def __init__(self, master):

        author_name = "Your Name"
        version_number = "1.0"

        self.master = master
        self.master.title("Jex")
        self.master.geometry("800x600")

        # Create a frame for the editor
        self.editor_frame = tk.Frame(self.master, bd=2, relief=tk.GROOVE)
        self.editor_frame.pack(expand=True, fill='both', padx=5, pady=5)

        # Title for the editor
        self.editor_title_label = tk.Label(self.editor_frame, text="Code Editor", font=("Helvetica", 16, "bold"))
        self.editor_title_label.pack(pady=(10, 5))

        # Text area for code editing
        self.text_area = scrolledtext.ScrolledText(self.editor_frame, wrap=tk.WORD, undo=True, bd=2, relief=tk.SOLID)
        self.text_area.pack(expand=True, fill='both', padx=5, pady=5)

        # Create a frame for the output
        self.output_frame = tk.Frame(self.master, bd=2, relief=tk.GROOVE)
        self.output_frame.pack(expand=True, fill='both', padx=5, pady=5)

        # Title for the output
        self.output_title_label = tk.Label(self.output_frame, text="Output", font=("Helvetica", 16, "bold"))
        self.output_title_label.pack(pady=(10, 5))

        # Text area for output display
        self.output_area = scrolledtext.ScrolledText(self.output_frame, wrap=tk.WORD, bd=2, relief=tk.SOLID)
        self.output_area.pack(expand=True, fill='both', padx=5, pady=5)

        # Menu bar
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
        self.format_menu.add_command(label="Syntax Highlighting", command=self.change_syntax_colors)
        self.format_menu.add_command(label="Toggle Line Numbers", command=self.toggle_line_numbers)
        self.line_numbers = False

        # Settings Menu
        self.settings_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)
        self.settings_menu.add_command(label="Select Theme", command=self.select_theme)
        self.settings_menu.add_command(label="File Encoding", command=self.select_encoding)

        # Syntax Highlighting
        self.keywords = keyword.kwlist
        self.string_pattern = re.compile(r'\'[^\']*\'|\"[^\"]*\"')
        self.comment_pattern = re.compile(r'#.*?$')
        self.number_pattern = re.compile(r'\b\d+\b')

        self.load_settings()

        self.text_area.bind('<KeyRelease>', self.on_key_release)

    def load_settings(self):
        self.syntax_highlighting_colors = {
            "keyword": "blue",
            "string": "green",
            "comment": "red",
            "number": "purple"
        }

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

    def on_key_release(self, event):
        if event.keysym == "BackSpace":
            self.text_area.tag_remove("highlight", 1.0, tk.END)
        else:
            self.highlight_syntax()

    def highlight_syntax(self):
        self.text_area.tag_remove("keyword", 1.0, tk.END)
        self.text_area.tag_remove("string", 1.0, tk.END)
        self.text_area.tag_remove("comment", 1.0, tk.END)
        self.text_area.tag_remove("number", 1.0, tk.END)

        self.highlight_pattern(self.keywords, "keyword")
        self.highlight_pattern(self.string_pattern, "string")
        self.highlight_pattern(self.comment_pattern, "comment")
        self.highlight_pattern(self.number_pattern, "number")

    def highlight_pattern(self, pattern, tag):
        start = "1.0"
        end = tk.END
        text = self.text_area.get(start, end)
        for match in pattern.finditer(text):
            start_index = self.text_area.index(f"{match.start() + 1}c")
            end_index = self.text_area.index(f"{match.end()}c")
            self.text_area.tag_add(tag, start_index, end_index)

    def indent_code(self):
        current_line = self.text_area.index(tk.INSERT).split('.')[0]
        current_line_text = self.text_area.get(f"{current_line}.0", f"{current_line}.end")
        indentation = len(current_line_text) - len(current_line_text.lstrip())
        self.text_area.insert(tk.INSERT, '\n' + ' ' * indentation)

    def toggle_line_numbers(self):
        if self.line_numbers:
            self.text_area.event_delete("<<LineNumbers>>")
        else:
            self.text_area.event_add("<<LineNumbers>>", "<KeyPress>")
            self.text_area.bind("<<LineNumbers>>", self.show_line_numbers)
        self.line_numbers = not self.line_numbers

    def show_line_numbers(self, event):
        current_line, _ = self.text_area.index(tk.INSERT).split('.')
        if not event.char.isdigit():
            self.text_area.insert(tk.END, f'{current_line}\n')

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

    def change_syntax_colors(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.syntax_highlighting_colors["keyword"] = color
            self.syntax_highlighting_colors["string"] = color
            self.syntax_highlighting_colors["comment"] = color
            self.syntax_highlighting_colors["number"] = color
            self.highlight_syntax()

    def select_theme(self):
        pass  # Implement theme selection functionality

    def select_encoding(self):
        pass  # Implement file encoding selection functionality

def main():
    root = tk.Tk()
    app = SimpleIDE(root)
    root.mainloop()

if __name__ == "__main__":
    main()
