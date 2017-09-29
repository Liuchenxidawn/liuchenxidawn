"""
Name: Liuchenxi
Date: 30/09/2017
Brief Project Description: This program is basically on assesment 1 then implemented on the app.kv file
When it work will display " required book" button. In addition, if the people click this button will show
the book is completed. The " add button" can input some valuable text. Finally, the "clear button" can clear
all text.
GitHub URL: https://github.com/Liuchenxidawn/liuchenxidawn
"""

from kivy.app import App
from kivy.lang import Builder
from book import book
from booklist import bookList
from kivy.uix.button import Button

class ReadingListApp(App):
    def __init__(self, **kwargs):
        """This is main class"""
        super(ReadingListApp, self).__init__(**kwargs)
        book_lists = BookList()
        book_object = Book()
        self.book_lists = book_lists
        self.book_object = book_object
        self.book_lists.load_books("books.csv")# loading book to get book list object

    def build(self):
        self.title = "Reading List 2.0"  # kivy name
        self.root = Builder.load_file('app.kv')  # Kivy target
        self.start_run()
        return self.root

    def create_books(self, mode):
        """This function is to make book list botton """
        self.root.ids.item_list.clear_widgets()
        # clear all current button

        if mode == "required":
            for book in range(len(self.book_lists.booklists)):
                if self.book_lists[book].status == 'r':
                    temp_button = Button(text=self.book_lists[book].title)
                    temp_button.bind(on_release=self.click_required_books)
                    page_check = self.book_object.long_pages(self.book_lists[book].pages)
                    if page_check == True:
                        temp_button.background_color = "blue"# if the book page number more than 500 that will diaplay blue

                    else:
                        temp_button.background_color = "red"# if less than 500 will diaplay red
                    self.root.ids.entriesBox.add_widget(temp_button)
            total_required_pages = self.book_lists.counting_required_pages()
            self.root.ids.bookPages.text = total_required_pages
            self.root.ids.bookMsg.text = "Click book to mark them as completed"


    def press_item_to_complete(self, instance):
        # complete mode when use this button
        name = instance.text
        item = self.book_list_list.find(name)
        if self.listing_option == 'c' and item.is_completed():  # For item already completed
            self.status_text = "complete"  # Display message
        elif self.listing_option == 'r' and not item.is_completed():  # For item available
            item.complete()
        self.start_run()

    def add_book (self):
            #this function is to add new book
            title = self.root.ids.input_name.text  # enter the book name
            author = self.root.ids.input_author.text  # enter the book pages
            pages = self.root.ids.input_pages.text  # enter the priority of book

            if title == "" or pages == "" or author == "":
                self.root.ids.status_label.text = "All fields must be completed"
            else:
                try:  # Using exception let user enter valid number
                    author = self.root.ids.input_author.text
                    pages = int(self.root.ids.input_pages.text)
                except ValueError:
                    self.root.ids.status_label.text = "Please enter a valid number"
                else:
                    if pages <= 0:
                        self.root.ids.status_label.text = "pages must be >= 0"
                    else:
                        book = Book(title, author, pages, flag='r')
                        self.booklist.add_book(book)
                        self.root.ids.status_label.text = "book \'{}\' wrote by {} in {} pages has been add to book list".format(
                            title, author, pages)
                        # show the added item at the status label
                        self.root.ids.input_name.text = ""
                        self.root.ids.input_author.text = ""
                        self.root.ids.input_pages.text = ""
                        # Clear whole input box after the new item add to the list
                        # Error check

        def handle_clear(self):  # This is clear function
            self.root.ids.input_name.text = ""
            self.root.ids.input_author.text = ""
            self.root.ids.input_pages.text = ""

        def save_book(self):  # Create save button
            file_writer = open("books.csv", "w")  # Open the file with the correct format
            count = 0
            writer = csv.writer(file_writer)
            for book in self.booklist.requirelist:
                writer.writerow([book.title, book.author, book.pages, book.flag])
                count += 1
            for book in self.booklist.completelist:
                writer.writerow([book.title, book.author, book.pages, book.flag])
                count += 1
            self.root.ids.status_label.text = "{} items saved to items.csv".format(count)
            # show the whole numble of books
            file_writer.close()


    if __name__ == "__main__":
        BookReadList().run()


