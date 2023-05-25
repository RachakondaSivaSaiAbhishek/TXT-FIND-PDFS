import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PyPDF2 import PdfReader


def search_pdf_files(folder_path, keyword):
    pdf_files = []
    for file in os.listdir(folder_path):
        if file.endswith('.pdf'):
            pdf_files.append(file)
    sorted_files = sorted(pdf_files)

    found_files = []
    for file in sorted_files:
        pdf_path = os.path.join(folder_path, file)
        with open(pdf_path, 'rb') as f:
            pdf = PdfReader(f)
            for page in pdf.pages:
                text = page.extract_text()
                if re.search(r'\b{}\b'.format(keyword), text, re.IGNORECASE):
                    found_files.append(file)
                    break

    return found_files


def search_files_callback():
    folder_path = folder_path_entry.get()
    keyword = keyword_entry.get()

    if not folder_path or not keyword:
        messagebox.showerror("Error", "Please provide a folder path and a keyword.")
        return

    if not os.path.isdir(folder_path):
        messagebox.showerror("Error", "Invalid folder path.")
        return

    found_files = search_pdf_files(folder_path, keyword)
    if found_files:
        file_listbox.delete(0, tk.END)
        for file in found_files:
            file_listbox.insert(tk.END, file)
    else:
        messagebox.showinfo("Result", "No files found containing the keyword.")


def browse_folder_callback():
    folder_path = filedialog.askdirectory()
    folder_path_entry.delete(0, tk.END)
    folder_path_entry.insert(tk.END, folder_path)


# Create the main window
window = tk.Tk()
window.title("PDF File Search")
window.geometry("600x600")

# Create styles
style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#ffffff", foreground="#1111ff")
style.configure("TEntry", padding=6, relief="flat")
style.configure("TLabel", padding=6, relief="flat", font=("Helvetica", 10), foreground="#333333")
style.configure("TListbox", padding=6, relief="flat")

# Folder path label and entry
folder_path_label = ttk.Label(window, text="Folder Path:")
folder_path_label.pack()

folder_path_entry = ttk.Entry(window, width=40)
folder_path_entry.pack()

# Browse button
browse_button = ttk.Button(window, text="Browse", command=browse_folder_callback)
browse_button.pack()

# Keyword label and entry
keyword_label = ttk.Label(window, text="Keyword:")
keyword_label.pack()

keyword_entry = ttk.Entry(window, width=40)
keyword_entry.pack()

# Search button
search_button = ttk.Button(window, text="Search", command=search_files_callback)
search_button.pack()

# File listbox
file_listbox = tk.Listbox(window, width=60, height=15)
file_listbox.pack()

window.mainloop()
