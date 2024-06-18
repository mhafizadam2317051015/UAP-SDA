import csv
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog

class Book:
    def __init__(self, id, title, author, year):
        self.id = id
        self.title = title
        self.author = author
        self.year = year

    def __str__(self):
        return f"ID: {self.id}, Title: {self.title}, Author: {self.author}, Year: {self.year}"

class Library:
    def __init__(self, filename="library.csv"):
        self.books = []
        self.filename = filename
        self.load_books_from_csv()

    def add_book(self, id, title, author, year):
        if any(book.id == id for book in self.books):
            return f"Book ID {id} already exists!"
        book = Book(id, title, author, year)
        self.books.append(book)
        self.save_books_to_csv()
        return f"Book '{title}' added successfully!"

    def view_books(self):
        if not self.books:
            return "No books in the library."
        return "\n".join(str(book) for book in self.books)

    def update_book(self, id, title=None, author=None, year=None):
        for book in self.books:
            if book.id == id:
                if title:
                    book.title = title
                if author:
                    book.author = author
                if year:
                    book.year = year
                self.save_books_to_csv()
                return f"Book ID {id} updated successfully!"
        return f"No book found with ID {id}"

    def delete_book(self, id):
        for book in self.books:
            if book.id == id:
                self.books.remove(book)
                self.save_books_to_csv()
                return f"Book ID {id} deleted successfully!"
        return f"No book found with ID {id}"

    def search_books(self, keyword):
        results = [book for book in self.books if keyword.lower() in book.title.lower() or keyword.lower() in book.author.lower()]
        if not results:
            return "No books found matching the keyword."
        return "\n".join(str(book) for book in results)

    def sort_books_by_title(self):
        self.books.sort(key=lambda book: book.title)
        self.save_books_to_csv()
        return "Books sorted by title!"

    def sort_books_by_year(self):
        self.books.sort(key=lambda book: book.year)
        self.save_books_to_csv()
        return "Books sorted by year!"

    def import_books_from_csv(self, filename):
        try:
            with open(filename, mode='r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    self.add_book(row['id'], row['title'], row['author'], row['year'])
            return "Books imported successfully from CSV file!"
        except FileNotFoundError:
            return f"File {filename} not found."
        except Exception as e:
            return str(e)


    def save_books_to_csv(self):
        with open(self.filename, mode='w', newline='') as file:
            fieldnames = ['id', 'title', 'author', 'year']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for book in self.books:
                writer.writerow({'id': book.id, 'title': book.title, 'author': book.author, 'year': book.year})

    def load_books_from_csv(self):
        try:
            with open(self.filename, mode='r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    self.add_book(row['id'], row['title'], row['author'], row['year'])
        except FileNotFoundError:
            pass

def add_book_gui(library):
    id = simpledialog.askstring("Input", "Enter book ID:")
    if not id:
        messagebox.showerror("Error", "Book ID cannot be empty!")
        return
    title = simpledialog.askstring("Input", "Enter book title:")
    author = simpledialog.askstring("Input", "Enter book author:")
    year = simpledialog.askstring("Input", "Enter publication year:")
    if year and not year.isdigit():
        messagebox.showerror("Error", "Publication year must be a number!")
        return
    messagebox.showinfo("Result", library.add_book(id, title, author, year))

def view_books_gui(library, text_widget):
    books = library.view_books()
    text_widget.config(state=tk.NORMAL)
    text_widget.delete(1.0, tk.END)
    text_widget.insert(tk.END, books)
    text_widget.config(state=tk.DISABLED)

def update_book_gui(library):
    id = simpledialog.askstring("Input", "Enter book ID to update:")
    if not id:
        messagebox.showerror("Error", "Book ID cannot be empty!")
        return
    title = simpledialog.askstring("Input", "Enter new title (leave blank to keep unchanged):")
    author = simpledialog.askstring("Input", "Enter new author (leave blank to keep unchanged):")
    year = simpledialog.askstring("Input", "Enter new year (leave blank to keep unchanged):")
    if year and not year.isdigit():
        messagebox.showerror("Error", "Publication year must be a number!")
        return
    messagebox.showinfo("Result", library.update_book(id, title, author, year))

def delete_book_gui(library):
    id = simpledialog.askstring("Input", "Enter book ID to delete:")
    if not id:
        messagebox.showerror("Error", "Book ID cannot be empty!")
        return
    messagebox.showinfo("Result", library.delete_book(id))

def search_books_gui(library):
    keyword = simpledialog.askstring("Input", "Enter keyword to search:")
    if not keyword:
        messagebox.showerror("Error", "Keyword cannot be empty!")
        return
    results = library.search_books(keyword)
    messagebox.showinfo("Search Results", results)

def import_books_gui(library):
    filename = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV files", "*.csv")])
    if filename:
        messagebox.showinfo("Result", library.import_books_from_csv(filename))

def sort_books_title_gui(library):
    messagebox.showinfo("Result", library.sort_books_by_title())

def sort_books_year_gui(library):
    messagebox.showinfo("Result", library.sort_books_by_year())

def main():
    library = Library()
    
    root = tk.Tk()
    root.title("Library Management System")
    
    root.configure(bg='lightcyan')

    title_label = tk.Label(root, text="Library Management System", bg='lightcyan', fg='blue', font=('Algerian', 24, 'bold'))
    title_label.pack(pady=10)

    button_frame = tk.Frame(root, bg='#D2B48C')
    button_frame.pack(pady=10)

    text_widget = tk.Text(root, height=15, width=100, wrap='word', bg='white', fg='black', font=('Times New Roman', 12), borderwidth=5, relief='groove')
    text_widget.pack(pady=10)
    text_widget.config(state=tk.DISABLED)

    def create_button(frame, text, command, bg_color):
        return tk.Button(frame, text=text, command=command, bg=bg_color, fg='black', font=('Times New Roman', 10, 'bold'), padx=10, pady=5, borderwidth=3, relief='raised')

    create_button(button_frame, "Add Book", lambda: add_book_gui(library), 'lightblue').pack(side='left', padx=5, pady=5)
    create_button(button_frame, "View Books", lambda: view_books_gui(library, text_widget), 'lightgreen').pack(side='left', padx=5, pady=5)
    create_button(button_frame, "Update Book", lambda: update_book_gui(library), 'lightyellow').pack(side='left', padx=5, pady=5)
    create_button(button_frame, "Delete Book", lambda: delete_book_gui(library), 'lightcoral').pack(side='left', padx=5, pady=5)
    create_button(button_frame, "Search Books", lambda: search_books_gui(library), 'lightpink').pack(side='left', padx=5, pady=5)
    create_button(button_frame, "Import Books from CSV", lambda: import_books_gui(library), 'lightgray').pack(side='left', padx=5, pady=5)
    create_button(button_frame, "Sort Books by Title", lambda: sort_books_title_gui(library), 'lavender').pack(side='left', padx=5, pady=5)
    create_button(button_frame, "Sort Books by Year", lambda: sort_books_year_gui(library), 'lightgoldenrodyellow').pack(side='left', padx=5, pady=5)
    create_button(button_frame, "Exit", root.quit, 'lightsteelblue').pack(side='left', padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()