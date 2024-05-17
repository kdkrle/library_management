import psycopg2 as pg
import pandas as pd
from datetime import date, timedelta


class Titles:
    """Managing data from the 'titles' table."""
    
    def __init__(self):
        self.con = pg.connect(
            database="library_management",
            user="postgres",
            password="pg11kdk",
            host="localhost",
            port="5433"
        )
        self.titles_df = None
    
    def titles_loading(self):
        """Refreshing the 'titles' table data."""
        
        self.titles_df = pd.read_sql_query("SELECT * FROM titles", self.con)
    
    def df_list_sort_by_title(self, df):
        """Sorting Dataframe by title and return title sorted list."""
        
        title_sort_df = df.sort_values(by=["title"])
        title_list = title_sort_df.title.to_list()
        
        return title_list
    
    def adding_new_title(self, new_title, new_author, new_genre, new_pub_year):
        """Entering data for a new title."""

        new_title_sql = f"""
                INSERT INTO titles (title, author, genre, publication_year)
                VALUES ('{new_title}', '{new_author}', '{new_genre}',
                '{new_pub_year}')
                """

        curs = self.con.cursor()
        curs.execute(new_title_sql)
        self.con.commit()

        # The connection will be closed with the application.
        curs.close()

        self.titles_loading()
    
    def titles_updating(self, sql):
        """Updating values in the 'titles' table."""

        curs = self.con.cursor()
        curs.execute(sql)
        self.con.commit()

        # The connection will be closed with the application.
        curs.close()

        self.titles_loading()


class Books:
    """Managing data from the 'books' table."""
    
    def __init__(self):
        self.con = pg.connect(
            database="library_management",
            user="postgres",
            password="pg11kdk",
            host="localhost",
            port="5433"
        )
        self.books_df = None
    
    def books_loading(self):
        """Refreshing the 'books' table data."""
        
        self.books_df = pd.read_sql_query("SELECT * FROM books", self.con)
    
    def update_reservations(self):
        """Automatic cancel any reservation, if the deadline (7 days) has
        passed."""
        
        reserved_book_codes_list = self.books_df.book_code[
            self.books_df.availability == "Reserved"].to_list()
        
        for code in reserved_book_codes_list:
            res_dates_list = reservations.reservations_df.reservation_date[
                reservations.reservations_df.book_code == code].to_list()
            
            # If the difference between today and the latest date listed is
            # more than 7 days (deadline), the copy is available.
            if date.today() - max(res_dates_list) > timedelta(days=7):
                
                reserved_sql = f"""UPDATE books
                SET availability = 'Available'
                WHERE book_code = '{code}';
                """
                
                curs = self.con.cursor()
                curs.execute(reserved_sql)
                self.con.commit()
    
                curs.close()
                
            self.books_loading()

    def set_book_status(self, code, status):
        """Setting the status of the copy."""
        
        set_status_sql = f"""
        UPDATE books
        SET availability = '{status}'
        WHERE book_code = '{code}'
        """
        
        curs = self.con.cursor()
        curs.execute(set_status_sql)
        self.con.commit()
        
        # The connection will be closed with the application.
        curs.close()
        
        self.books_loading()
    
    def adding_new_copy(self, code_lbl, title_cb):
        """Adding a copy of a book to an existing title."""
        
        new_copy_sql = f"""
        INSERT INTO books (book_code, title, availability)
        VALUES ('{code_lbl.cget("text")}', '{title_cb.get()}', 'Available')
        """

        curs = self.con.cursor()
        curs.execute(new_copy_sql)
        self.con.commit()

        # The connection will be closed with the application.
        curs.close()

        self.books_loading()
    
    def updating_books(self, sql):
        """Updating values in the 'books' table."""

        curs = self.con.cursor()
        curs.execute(sql)
        self.con.commit()

        # The connection will be closed with the application.
        curs.close()

        self.books_loading()


class Members:
    """Managing data from the 'members' table."""
    
    def __init__(self):
        self.con = pg.connect(
            database="library_management",
            user="postgres",
            password="pg11kdk",
            host="localhost",
            port="5433"
        )
        self.members_df = None
    
    def members_loading(self):
        """Refreshing the 'members' table data."""
        
        self.members_df = pd.read_sql_query("SELECT * FROM members",
                                             self.con)

    def membership_ids_sorted(self):
        """Sorting values of table 'members' by membership_id."""
    
        ids_sorted = self.members_df.sort_values(by=["membership_id"])
        id_list = ids_sorted.membership_id.to_list()
    
        return id_list
    
    def new_password(self, new_pass, mem_id):
        """Entering a new password value."""

        new_pass_sql = f"""
                UPDATE members
                SET password = '{new_pass}'
                WHERE membership_id = '{mem_id}'
                """

        curs = self.con.cursor()
        curs.execute(new_pass_sql)
        self.con.commit()

        # The connection will be closed with the closing of the application.
        curs.close()

        self.members_loading()

    def members_updating(self, sql):
        """Updating values in the 'members' table."""

        curs = self.con.cursor()
        curs.execute(sql)
        self.con.commit()

        # The connection will be closed with the application.
        curs.close()

        self.members_loading()


class Librarians:
    """Managing data from the 'librarians' table."""
    
    def __init__(self):
        self.con = pg.connect(
            database="library_management",
            user="postgres",
            password="pg11kdk",
            host="localhost",
            port="5433"
        )
        self.librarians_df = None
    
    def librarians_loading(self):
        """Refreshing the 'librarians' table data."""
        
        self.librarians_df = pd.read_sql_query("SELECT * FROM librarians",
                                                 self.con)


class Renting:
    """Managing data from the 'renting' table."""
    
    def __init__(self):
        self.con = pg.connect(
            database="library_management",
            user="postgres",
            password="pg11kdk",
            host="localhost",
            port="5433"
        )
        self.renting_df = None
    
    def renting_loading(self):
        """Refreshing the 'renting' table data."""
        
        self.renting_df = pd.read_sql_query(
            "SELECT * FROM renting", self.con)
    
    def rent_execute(self, sql):
        """Executing the sql for the 'renting' table."""
        
        curs = self.con.cursor()
        curs.execute(sql)
        self.con.commit()
        
        # The connection will be closed with the application.
        curs.close()

        self.renting_loading()
        


class Reservations:
    """Managing data from the 'reservations' table."""
    
    def __init__(self):
        self.con = pg.connect(
            database="library_management",
            user="postgres",
            password="pg11kdk",
            host="localhost",
            port="5433"
        )
        self.reservations_df = None
    
    def reservations_loading(self):
        """Refreshing the 'reservations' table data."""
        
        self.reservations_df = pd.read_sql_query("SELECT * FROM "
                                                 "reservations", self.con)
    
    def reservation_entering(self, code, mem_id):
        """Entering a reservation in the 'reservations' table."""
        
        today = date.today()
        
        entering_sql = f"""
        INSERT INTO reservations (membership_id, book_code, reservation_date)
        VALUES ('{mem_id}', '{code}', '{today}');
        """

        # Execute the sql
        curs = self.con.cursor()
        curs.execute(entering_sql)
        self.con.commit()

        # The connection will be closed with the application.
        curs.close()

        self.reservations_loading()


titles = Titles()
titles.titles_loading()
books = Books()
books.books_loading()
members = Members()
members.members_loading()
librarians = Librarians()
librarians.librarians_loading()
renting = Renting()
renting.renting_loading()
reservations = Reservations()
reservations.reservations_loading()

books.update_reservations()