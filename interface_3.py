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


def open_pdf(filename):
    pdf_path = os.path.join(folder_path_entry.get(), filename)
    os.startfile(pdf_path)


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

    # Bind double-click event to open PDF on double-click
    file_listbox.bind("<Double-Button-1>", lambda event: open_pdf(file_listbox.get(file_listbox.curselection())))


def browse_folder_callback():
    folder_path = filedialog.askdirectory()
    folder_path_entry.delete(0, tk.END)
    folder_path_entry.insert(tk.END, folder_path)


# Create the main window
window = tk.Tk()
window.title("PDF File Search and Viewer")
window.geometry("500x500")

# Set the background color
window.configure(bg="#f2f2f2")

# Create styles
style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#d3d3d3", foreground="#333333")
style.configure("TEntry", padding=6, relief="flat", background="#ffffff")
style.configure("TLabel", padding=6, relief="flat", font=("Helvetica", 10), foreground="#333333", background="#f2f2f2")
style.configure("TListbox", padding=6, relief="flat", background="#ffffff", foreground="#333333")

# Folder path label and entry
folder_path_label = ttk.Label(window, text="Folder Path:")
folder_path_label.pack(pady=(20, 5))

folder_path_entry = ttk.Entry(window, width=40)
folder_path_entry.pack()

# Browse button
browse_button = ttk.Button(window, text="Browse", command=browse_folder_callback)
browse_button.pack(pady=(10, 5))

# Keyword label and entry
keyword_label = ttk.Label(window, text="Keyword:")
keyword_label.pack(pady=(10, 5))

keyword_entry = ttk.Entry(window, width=40)
keyword_entry.pack()

# Search button
search_button = ttk.Button(window, text="Search", command=search_files_callback)
search_button.pack(pady=(10, 20))

# File listbox with vertical scrollbar
file_listbox = tk.Listbox(window, width=60, height=15)
file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, padx=(20, 10), pady=(0, 20))

scrollbar = tk.Scrollbar(window, orient=tk.VERTICAL, command=file_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

file_listbox.configure(yscrollcommand=scrollbar.set)

window.mainloop()
