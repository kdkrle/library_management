from library import *
from data import *
import random
from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap.scrolled import ScrolledFrame
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

root = ttk.Window(themename="darkly")
root.title("Upravljanje bibliotekom")
root.geometry("920x1030")
root.resizable(False, False)
root.iconbitmap("pics/library.ico")
root.iconbitmap(default="pics/library.ico")

# Global variables
member_status = "inactive"
librarian_status = "inactive"
language = "srpski"
logged_in_member_code = ""
logged_in_librarian_code = ""

# Big buttons style
big_buttons_style = ttk.Style("litera")
big_buttons_style.configure("big.dark.TButton", font=("Calibri", 18, "bold"))

# Huge buttons style
huge_buttons_style = ttk.Style("litera")
huge_buttons_style.configure("huge.primary.TButton",
                            font=("Calibri", 24, "bold"))

# Treeview style
tree_style = ttk.Style("litera")
tree_style.configure("tree.warning.Treeview", font=("Calibri", 14),
                     rowheight=25)

# Radiobutton style
radio_style = ttk.Style("litera")
radio_style.configure("warning.TRadiobutton", font=("Calibri", 16))

# Dropdown Combobox font size.
root.option_add('*TCombobox*Listbox.font', ("Calibri", 12))


def exit_app():
    """Closing the application."""
    msg_title = language_text("Zatvaranje aplikacije",
                              "Closing the application")
    msg_message = language_text("Da li želite da izađete iz applikacije?",
                                "Do you want to exit the application?")
    question = Messagebox.yesno(
        title=msg_title,
        message=msg_message,
        parent=root,
        alert=True
    )
    if question == "Yes":
        root.destroy()


def language_text(srb_text, eng_text):
    """Function which returns Serbian or English text."""
    if language == "srpski":
        text = srb_text
    else:
        text = eng_text
    return text


def len_digit_limit(inp, length):
    """Limiting the number and type of characters (numbers only,
    four characters long)."""
    
    if inp.isdigit() and len(inp) <= length:
        return True
    elif inp == "":
        return True
    else:
        return False


def creating_values_list(data):
    """Creating a list of values depending on the language."""
    global language

    values_lst = []
    values_lst_srb = []
    if language == "srpski":
        sorted_values = sorted(data)
        for i in range(len(sorted_values)):
            values_lst_srb.append(sorted_values[i][0])
            values_lst.append(sorted_values[i][1])
        return values_lst_srb, values_lst
    else:
        for i in range(len(data)):
            values_lst.append(data[i][1])
        values_lst.sort()
    
        for value in values_lst:
            for j in range(len(data)):
                if value in data[j]:
                    values_lst_srb.append(data[j][0])
        return values_lst_srb, values_lst


def unique_code_generating(old_list, code_length):
    """Generating of unique code with a specified length."""
    
    unique = ""
    for _ in range(code_length):
        unique += str(random.randint(0, 9))

    if unique in old_list:
        unique_code_generating(old_list, code_length)
    else:
        return unique


def language_change(event):
    """Changes that happen with the choice of language."""
    global language
    global member_status
    
    member_logged_in = logged_in_member()
    
    if language_cmb.get() == "Srpski":
        language = "srpski"
        
        if member_status == "inactive":
            log_button = "Prijavite se"
            tooltip_log_txt = "Korisnik nije prijavljen"
        else:
            log_button = "Odjavite se"
            tooltip_log_txt = f"Član: {member_logged_in}"

        choose_language = "Izaberite jezik:"
        title = "Biblioteka \"Vuk Karadžić\""
        subtitle = "Sa vama od 2000. godine"
        ui = " Radno okruženje "
        switch_widget = "  Korisnik/Bibliotekar"
        switch_txt = "Radno okruženje: običan korisnik (isključeno) / " \
                     "bibliotekar (uključno)."
        exit_txt = "Izađi"
        
        ui_create()
    else:
        language = "english"
        
        if member_status == "inactive":
            log_button = "Log In"
            tooltip_log_txt = "User is not logged in"
        else:
            log_button = "Log Out"
            tooltip_log_txt = f"Member: {member_logged_in}"

        choose_language = "Choose Language:"
        title = "Library \"Vuk Karadžić\""
        subtitle = "With you since 2000."
        ui = " User Interface "
        switch_widget = "  User/Librarian"
        switch_txt = "User interface: common user (Off) / librarian (On)."
        exit_txt = "Exit"
        
        ui_create()

    language_lbl.configure(text=choose_language)
    login_btn.configure(text=log_button)
    ToolTip(login_lbl, text=tooltip_log_txt, bootstyle="warning")
    main_title.configure(text=title)
    main_subtitle.configure(text=subtitle)
    switch_lf.configure(text=ui)
    switch_chb.configure(text=switch_widget)
    switch_lbl.configure(text=switch_txt)
    exit_btn.configure(text=exit_txt)


def login_image():
    """Prepare a login image."""
    
    if member_status == "inactive":
        img = Image.open("pics/reader_inactive.png")
    else:
        img = Image.open("pics/reader_active.png")
    
    resize_img = img.resize((30, 30))
    login_img = ImageTk.PhotoImage(resize_img)
    
    return login_img


def getting_image(genre=None, img_size=(150, 150)):
    """Getting the requested image."""
    
    if not genre:
        path = "pics/book.png"
    else:
        genre_name = genre.replace(" ", "_").lower()
        path = f"pics/genre_{genre_name}.png"

    # Preparing an image for placement
    img = Image.open(path)
    img_resize = img.resize(img_size)
    picture = ImageTk.PhotoImage(img_resize)
    
    return picture


def ui_create():
    """Creating a UI for visitors/members or librarians."""
    global librarian_status
    global member_status

    # Clear frame
    for widget in ui_frame.winfo_children():
        widget.destroy()

    # Creating new widgets
    if switch_var.get() == 0:
        visitor_lf_text = language_text(" Posetioci i članovi ",
                                        " Visitors and Members ")
        visitors_lf = ttk.LabelFrame(
            ui_frame,
            text=visitor_lf_text,
            bootstyle="warning"
        )
        visitors_lf.pack(expand=True, fill="x", padx=20, pady=10)
        
        members_lf_text = language_text(" Samo za članove ", " Members Only ")
        members_lf = ttk.LabelFrame(
            ui_frame,
            text=members_lf_text,
            bootstyle="warning"
        )
        members_lf.pack(expand=True, fill="x", padx=20, pady=10)
        
        # Buttons in 'Visitors and Members' frame
        books_btn = language_text("PRETRAGA KNJIGA", "BOOK SEARCH")
        ttk.Button(
            visitors_lf,
            width=20,
            text=books_btn,
            style="big.dark.TButton",
            command=book_search
        ).grid(column=0, row=0, padx=50, pady=(20, 10))
        
        most_read_books_btn = language_text("NAJČITANIJE KNJIGE",
                                            "MOST READ BOOKS")
        ttk.Button(
            visitors_lf,
            width=20,
            text=most_read_books_btn,
            style="big.dark.TButton",
            command=most_read_books_list
        ).grid(column=0, row=1, padx=50, pady=10)
        
        most_read_authors_btn = language_text("NAJČITANIJI AUTORI",
                                              "MOST READ AUTHORS")
        ttk.Button(
            visitors_lf,
            width=20,
            text=most_read_authors_btn,
            style="big.dark.TButton",
            command=most_read_authors_list
        ).grid(column=0, row=2, padx=50, pady=10)
        
        most_read_by_genre_btn = language_text("PROČITANO PO ŽANRU",
                                                "READ BY GENRE")
        ttk.Button(
            visitors_lf,
            width=20,
            text=most_read_by_genre_btn,
            style="big.dark.TButton",
            command=read_by_genre
        ).grid(column=0, row=3, padx=50, pady=(10, 20))

        # Labels in 'Visitors and Members' frame
        books_lbl = language_text(
            "Pretraživanje knjiga po naslovu, autoru ili žanru.",
            "Search books by title, author or genre."
        )
        ttk.Label(
            visitors_lf,
            text=books_lbl,
            font=("Calibri", 16),
            bootstyle="light"
        ).grid(column=1, row=0, padx=50, pady=(20, 10), sticky="w")

        most_read_books_lbl = language_text(
            "Spisak i grafik deset najčitanijih naslova.",
            "List and graphic of the ten most read titles."
        )
        ttk.Label(
            visitors_lf,
            text=most_read_books_lbl,
            font=("Calibri", 16),
            bootstyle="light"
        ).grid(column=1, row=1, padx=50, pady=10, sticky="w")
        
        most_read_authors_lbl = language_text(
            "Spisak i grafik deset najčitanijih autora.",
            "List and graphic of the ten most read authors."
        )
        ttk.Label(
            visitors_lf,
            text=most_read_authors_lbl,
            font=("Calibri", 16),
            bootstyle="light"
        ).grid(column=1, row=2, padx=50, pady=10, sticky="w")
        
        most_read_by_genre_lbl = language_text(
            "Pročitano knjiga iz svakog žanra.",
            "Read books from each genre."
        )
        ttk.Label(
            visitors_lf,
            text=most_read_by_genre_lbl,
            font=("Calibri", 16),
            bootstyle="light"
        ).grid(column=1, row=3, padx=50, pady=(10, 20), sticky="w")

        # Buttons in 'Members Only' frame
        if member_status == "inactive":
            member_login_btn = language_text("PRIJAVITE SE", "LOG IN")
            member_login_lbl = language_text(
                "Prijavljivanje člana biblioteke.",
                "Library member login."
            )
            state = "disabled"
        else:
            member_login_btn = language_text("ODJAVITE SE", "LOG OUT")
            member_login_lbl = language_text(
                "Odjavljivanje člana biblioteke.",
                "Library member logout."
            )
            state = "normal"

        ttk.Button(
            members_lf,
            width=20,
            text=member_login_btn,
            style="big.dark.TButton",
            command=member_login
        ).grid(column=0, row=0, padx=50, pady=(20, 10))

        renting_btn = language_text("DETALJI NALOGA", "ACCOUNT DETAILS")
        ttk.Button(
            members_lf,
            width=20,
            text=renting_btn,
            style="big.dark.TButton",
            state=state,
            command=member_details
        ).grid(column=0, row=1, padx=50, pady=10)

        reservation_btn = language_text("REZERVACIJA", "RESERVATION")
        ttk.Button(
            members_lf,
            width=20,
            text=reservation_btn,
            style="big.dark.TButton",
            state=state,
            command=book_reservation
        ).grid(column=0, row=2, padx=50, pady=10)

        pass_change_btn = language_text("PROMENA LOZINKE", "PASSWORD CHANGE")
        ttk.Button(
            members_lf,
            width=20,
            text=pass_change_btn,
            style="big.dark.TButton",
            state=state,
            command=password_change
        ).grid(column=0, row=3, padx=50, pady=(10, 20))

        # Labels in 'Members Only' frame
        ttk.Label(
            members_lf,
            text=member_login_lbl,
            font=("Calibri", 16),
            bootstyle="light"
        ).grid(column=1, row=0, padx=50, pady=(20, 10), sticky="w")

        renting_lbl = language_text(
            "Podaci o iznajmljenim knjigama i rezervacijama.",
            "Data on rented books and reservations."
        )
        ttk.Label(
            members_lf,
            text=renting_lbl,
            font=("Calibri", 16),
            bootstyle="light"
        ).grid(column=1, row=1, padx=50, pady=10, sticky="w")

        reservation_lbl = language_text(
            "Rezervacija knjiga (važi nedelju dana).",
            "Book reservation (valid for one week).")
        ttk.Label(
            members_lf,
            text=reservation_lbl,
            font=("Calibri", 16),
            bootstyle="light"
        ).grid(column=1, row=2, padx=50, pady=10, sticky="w")

        pass_change_lbl = language_text(
            "Menjanje postojeće lozinke.",
            "Changing an existing password.")
        ttk.Label(
            members_lf,
            text=pass_change_lbl,
            font=("Calibri", 16),
            bootstyle="light"
        ).grid(column=1, row=3, padx=50, pady=(10, 20), sticky="w")
    else:
        librarian_lf_text = language_text(" Bibliotekari ", " Librarians ")
        librarians_lf = ttk.LabelFrame(
            ui_frame,
            text=librarian_lf_text,
            bootstyle="warning"
        )
        librarians_lf.pack(expand=True, fill="both", padx=20, pady=10)

        # Buttons in 'Librarians' frame
        if librarian_status == "inactive":
            lib_login_btn_text = language_text("PRIJAVITE SE", "LOG IN")
        else:
            lib_login_btn_text = language_text("ODJAVITE SE", "LOG OUT")
            
        lib_login_btn = ttk.Button(
            librarians_lf,
            width=20,
            text=lib_login_btn_text,
            style="big.dark.TButton",
            command=librarian_login
        )
        lib_login_btn.grid(column=0, row=0, padx=50, pady=(20, 10))

        inventory_btn_text = language_text("INVENTAR", "INVENTORY")
        lib_inventory_btn = ttk.Button(
            librarians_lf,
            width=20,
            text=inventory_btn_text,
            style="big.dark.TButton",
            command=inventory
        )
        lib_inventory_btn.grid(column=0, row=1, padx=50, pady=10)

        adding_btn_text = language_text("DODAVANJE KNJIGA", "ADDING BOOKS")
        lib_adding_btn = ttk.Button(
            librarians_lf,
            width=20,
            text=adding_btn_text,
            style="big.dark.TButton",
            command=adding_books
        )
        lib_adding_btn.grid(column=0, row=2, padx=50, pady=10)
        
        books_update_btn_text = language_text("AŽURIRANJE KNJIGA",
                                              "BOOKS UPDATE")
        lib_books_update_btn = ttk.Button(
            librarians_lf,
            width=20,
            text=books_update_btn_text,
            style="big.dark.TButton",
            command=books_updating
        )
        lib_books_update_btn.grid(column=0, row=3, padx=50, pady=10)
        
        members_info_btn_text = language_text("ČLANOVI INFO", "MEMBERS INFO")
        lib_membres_info_btn = ttk.Button(
            librarians_lf,
            width=20,
            text=members_info_btn_text,
            style="big.dark.TButton",
            command=members_info
        )
        lib_membres_info_btn.grid(column=0, row=4, padx=50, pady=10)
        
        new_members_btn_text = language_text("NOVI ČLANOVI", "NEW MEMBERS")
        lib_new_members_btn = ttk.Button(
            librarians_lf,
            width=20,
            text=new_members_btn_text,
            style="big.dark.TButton",
            command=new_members
        )
        lib_new_members_btn.grid(column=0, row=5, padx=50, pady=10)
        
        members_update_btn_text = language_text("AŽURIRANJE ČLANOVA",
                                                "MEMBERS UPDATE")
        lib_members_update_btn = ttk.Button(
            librarians_lf,
            width=20,
            text=members_update_btn_text,
            style="big.dark.TButton",
            command=members_updating
        )
        lib_members_update_btn.grid(column=0, row=6, padx=50, pady=10)
        
        renting_lib_btn_text = language_text("IZNAJMLJIVANJE", "RENTING")
        lib_renting_lib_btn = ttk.Button(
            librarians_lf,
            width=20,
            text=renting_lib_btn_text,
            style="big.dark.TButton",
            command=book_rental
        )
        lib_renting_lib_btn.grid(column=0, row=7, padx=50, pady=10)
        
        statistics_btn_text = language_text("STATISTIKA", "STATISTICS")
        lib_statistics_btn = ttk.Button(
            librarians_lf,
            width=20,
            text=statistics_btn_text,
            style="big.dark.TButton",
            command=statistics
        )
        lib_statistics_btn.grid(column=0, row=8, padx=50, pady=(10, 20))

        librarian_buttons = [lib_inventory_btn, lib_adding_btn,
                             lib_books_update_btn, lib_membres_info_btn,
                             lib_new_members_btn, lib_members_update_btn,
                             lib_renting_lib_btn, lib_statistics_btn]
        
        if librarian_status == "inactive":
            for button in librarian_buttons:
                button.configure(state="disabled")
        else:
            for button in librarian_buttons:
                button.configure(state="normal")
        
        # Labels in 'Librarians' frame
        librarian_login_lbl = language_text(
            "Prijavljivanje bibliotekara.",
            "Librarian login."
        )
        ttk.Label(
            librarians_lf,
            text=librarian_login_lbl,
            font=("Calibri", 16),
            bootstyle="light"
        ).grid(column=1, row=0, padx=50, pady=(20, 10), sticky="w")

        inventory_lbl = language_text("Pregled naslova i status primeraka.",
                                      "Title overview and copy status.")
        ttk.Label(
            librarians_lf,
            text=inventory_lbl,
            font=("Calibri", 16),
            bootstyle="light"
        ).grid(column=1, row=1, padx=50, pady=10, sticky="w")

        adding_lbl = language_text(
            "Dodavanje knjiga u fond biblioteke.",
            "Adding books to the library collection."
        )
        ttk.Label(
            librarians_lf,
            text=adding_lbl,
            font=("Calibri", 16),
            bootstyle="light"
        ).grid(column=1, row=2, padx=50, pady=10, sticky="w")
        
        books_update_lbl = language_text(
            "Ažuriranje podataka za naslove i knjige.",
            "Updating data for titles and books."
        )
        ttk.Label(
            librarians_lf,
            text=books_update_lbl,
            font=("Calibri", 16),
            bootstyle="light"
        ).grid(column=1, row=3, padx=50, pady=10, sticky="w")
        
        members_info_lbl = language_text(
            "Podaci o članovima biblioteke.",
            "Information about library members."
        )
        ttk.Label(
            librarians_lf,
            text=members_info_lbl,
            font=("Calibri", 16),
            bootstyle="light"
        ).grid(column=1, row=4, padx=50, pady=10, sticky="w")
        
        new_members_lbl = language_text(
            "Unos podataka za novog člana biblioteke.",
            "Data entry for a new library member."
        )
        ttk.Label(
            librarians_lf,
            text=new_members_lbl,
            font=("Calibri", 16),
            bootstyle="light"
        ).grid(column=1, row=5, padx=50, pady=10, sticky="w")
        
        members_update_lbl = language_text(
            "Ažuriranje podataka članova biblioteke.",
            "Updating library members information."
        )
        ttk.Label(
            librarians_lf,
            text=members_update_lbl,
            font=("Calibri", 16),
            bootstyle="light"
        ).grid(column=1, row=6, padx=50, pady=10, sticky="w")
        
        renting_lib_lbl = language_text(
            "Uvid u trenutno iznajmljene knjige.",
            "Insight into currently rented books."
        )
        ttk.Label(
            librarians_lf,
            text=renting_lib_lbl,
            font=("Calibri", 16),
            bootstyle="light"
        ).grid(column=1, row=7, padx=50, pady=10, sticky="w")
        
        statistics_lbl = language_text(
            "Podaci i grafici vezani za rad bibilioteke.",
            "Data and graphics related to library work."
        )
        ttk.Label(
            librarians_lf,
            text=statistics_lbl,
            font=("Calibri", 16),
            bootstyle="light"
        ).grid(column=1, row=8, padx=50, pady=(10, 20), sticky="w")


def logged_in_member():
    """Name of logged in member."""
    
    mem_name = members.members_df.first_name[
        members.members_df.membership_id == logged_in_member_code
            ].to_string(index=False)
    mem_surname = members.members_df.last_name[
        members.members_df.membership_id == logged_in_member_code
            ].to_string(index=False)
    name = f"{mem_name} {mem_surname}"
    
    return name


def logged_in_librarian():
    """Name of logged in librarian."""
    
    lib_name = librarians.librarians_df.first_name[
        librarians.librarians_df.personal_id == logged_in_librarian_code
    ].to_string(index=False)
    lib_surname = librarians.librarians_df.last_name[
        librarians.librarians_df.personal_id == logged_in_librarian_code
    ].to_string(index=False)
    name = f"{lib_name} {lib_surname}"
    
    return name


def not_on_time(membership_id):
    """How many times a book was not returned on time."""
    
    # Dateframe with returned books only
    returned_books_df = renting.renting_df.dropna()
    
    # Dataframe for the specified member
    member_returned_df = returned_books_df[
        returned_books_df.membership_id == membership_id]
    
    rented_returned_lists = []
    for index, rows in member_returned_df.iterrows():
        row_values = [rows.rental_date, rows.return_date]
        rented_returned_lists.append(row_values)
    
    not_on_time_counter = 0
    for i in range(len(rented_returned_lists)):
        if rented_returned_lists[i][0] + timedelta(days=15) < \
                rented_returned_lists[i][1]:
            not_on_time_counter += 1
    
    return not_on_time_counter


def most_read_books_data():
    """Data for the ten most read books."""
    
    # List of all copies
    book_codes_list = books.books_df.book_code.to_list()
    
    # How many times a copy has been read (rented)
    copies_read = []
    for code in book_codes_list:
        times_read = renting.renting_df[renting.renting_df.book_code == code][
            "book_code"].count()
        single_copy_read = [times_read, code]
        
        copies_read.append(single_copy_read)
    
    # List of all titles
    titles_list = titles.titles_df.title.to_list()
    authors_list = titles.titles_df.author.to_list()
    
    total_read_title_author_lists = []
    for i in range(len(titles_list)):
        codes_list_of_title = books.books_df.book_code[
            books.books_df.title == titles_list[i]].to_list()
        total_read = 0
        for lst in copies_read:
            if lst[1] in codes_list_of_title:
                total_read += lst[0]
        total_read_title_author_lists.append([total_read, titles_list[i],
                                              authors_list[i]])
    sorted_lists = sorted(total_read_title_author_lists, reverse=True)
    
    return sorted_lists


def most_read_authors_data():
    """Data for the ten most read authors."""
    
    # Most read titles
    most_read_titles = most_read_books_data()
    
    # List of all authors
    authors_list = set(titles.titles_df.author.to_list())
    
    authors_read_list = []
    for author in authors_list:
        single_author_read = 0
        for i in range(len(most_read_titles)):
            if author == most_read_titles[i][2]:
                single_author_read += most_read_titles[i][0]
        authors_read_list.append([single_author_read, author])
    authors_read_sorted = sorted(authors_read_list, reverse=True)
    
    return authors_read_sorted


def book_search():
    """New window for searching books by certain criteria."""
    
    def data_reset():
        """Resetting all data to initial values."""
        
        # Labels resetting
        labels = [search_info_title_val, search_info_author_val,
                  search_info_genre_val, search_info_year_val]
        for label in labels:
            label.configure(text="-")

        # Image resetting
        default_image = getting_image()
        search_image_lbl.configure(image=default_image)
        search_image_lbl.image = default_image
        
        # Titles dropdown values resetting
        search_selection_combo.set("")
        search_selection_combo.configure(values=titles.df_list_sort_by_title(
            titles.titles_df))
    
    def reset_all():
        """Resetting all labels and combos."""
        combos = [search_author_combo, search_genre_combo, search_year_combo]
        for combo in combos:
            combo.set("")
        
        data_reset()
    
    def filter_author(event):
        """Changes that occur when a value is selected from the 'Author'
        dropdown menu."""
        search_genre_combo.set("")
        search_year_combo.set("")
        search_selection_combo.set("")
        data_reset()
        
        df = titles.titles_df[titles.titles_df.author ==
                              search_author_combo.get()]
        search_selection_combo.configure(
            values=titles.df_list_sort_by_title(df))

    def filter_genre(event):
        """Changes that occur when a value is selected from the 'Genre'
        dropdown menu."""
        search_author_combo.set("")
        search_year_combo.set("")
        search_selection_combo.set("")
        data_reset()
        
        # Getting English names for genres when the interface language is in
        # Serbian.
        if language == "srpski":
            for genre in GENRES:
                if genre[0] == search_genre_combo.get():
                    genre_name = genre[1]
        else:
            genre_name = search_genre_combo.get()
    
        df = titles.titles_df[
            titles.titles_df.genre == genre_name]
        search_selection_combo.configure(
            values=titles.df_list_sort_by_title(df))

    def filter_year(event):
        """Changes that occur when a value is selected from the 'Genre'
        dropdown menu."""
        search_author_combo.set("")
        search_genre_combo.set("")
        search_selection_combo.set("")
        data_reset()
    
        df = titles.titles_df[
            titles.titles_df.publication_year == search_year_combo.get()]
        search_selection_combo.configure(
            values=titles.df_list_sort_by_title(df))
    
    def search_title_selected(event):
        """Changes that occur when selecting a title."""
        
        current_data = titles.titles_df[
            titles.titles_df.title == search_selection_combo.get()
        ].values.flatten().tolist()
        
        # Get genre
        for i in range(len(GENRES)):
            if current_data[2] == GENRES[i][1]:
                genre_srb = GENRES[i][0]
        
        genre = language_text(genre_srb, current_data[2])
        
        search_info_title_val.configure(text=current_data[0])
        search_info_author_val.configure(text=current_data[1])
        search_info_genre_val.configure(text=genre)
        search_info_year_val.configure(text=f"{current_data[3]}.")
        
        # Set the genre image
        genre_image = getting_image(genre=current_data[2])
        search_image_lbl.configure(image=genre_image)
        search_image_lbl.image = genre_image
    
    book_search_title = language_text("Pretraga knjiga", "Book Search")
    
    book_search_tl = ttk.Toplevel(title=book_search_title)
    book_search_tl.attributes("-topmost", "true")
    book_search_tl.resizable(False, False)
    book_search_tl.geometry("1000x900")
    book_search_tl.grab_set()
    
    # Scrollable frame for other frames
    search_sf = ScrolledFrame(book_search_tl, autohide=True)
    search_sf.pack(expand=True, fill="both")
    
    # Other frames
    search_filters_lf_text = language_text(" Filteri ", " Filters ")
    search_selection_lf_text = language_text(" Izbor naslova ",
                                             " Title selection ")
    search_info_lf_text = language_text(" Informacije o naslovu ",
                                        " Title information ")
    
    search_top_frm = ttk.Frame(search_sf)
    search_top_frm.pack(expand=True, fill="x", padx=20, pady=20)
    
    search_filters_lf = ttk.LabelFrame(
        search_sf,
        text=search_filters_lf_text,
        bootstyle="warning"
    )
    search_filters_lf.pack(expand=True, fill="x", padx=20, pady=10)

    search_selection_lf = ttk.LabelFrame(
        search_sf,
        text=search_selection_lf_text,
        bootstyle="warning")
    search_selection_lf.pack(expand=True, fill="x", padx=20, pady=10)
    
    search_info_lf = ttk.LabelFrame(
        search_sf,
        text=search_info_lf_text,
        bootstyle="warning"
    )
    search_info_lf.pack(expand=True, fill="x", padx=20, pady=10)

    search_buttons_frm = ttk.Frame(search_sf)
    search_buttons_frm.pack(expand=True, fill="x", padx=20, pady=10)
    
    # Widget in top (title) frame
    title_text = language_text(" Biblioteka \"Vuk Karadžić\"",
                               " Library \"Vuk Karadžić\"")
    
    search_title_lbl = ttk.Label(
        search_top_frm,
        text=title_text,
        font=("Calibri", 36, "bold"),
        image=logo_smaller,
        compound="left",
        anchor="center",
        bootstyle="warning"
    )
    search_title_lbl.pack(expand=True, fill="x")
    
    # Widgets in filters frame
    search_filters_lf.grid_columnconfigure((0, 1, 2), weight=1)
    
    search_info_srb = "Izaberite filter za selekciju naslova.\nUkoliko ne " \
                      "izaberete nijedan filter, imaćete izbor svih " \
                      "naslova.\nPritiskom na dugme \"Resetuj\" poništava " \
                      "se izbor filtera i brišu prethodni podaci."
    search_info_eng = "Choose a title selection filter.\nIf you do not " \
                      "select any filter, you will have a selection of all " \
                      "titles.\nPressing the \"Reset\" button cancels the " \
                      "filter selection and deletes the previous data."
    search_info_text = language_text(search_info_srb, search_info_eng)
    search_author_text = language_text("Autor", "Author")
    search_genre_text = language_text("Žanr", "Genre")
    search_year_text = language_text("Godina izdanja", "Publication year")
    search_selection_text = language_text("Izbor naslova", "Title selection")
    
    # Valus for filter Comboboxes
    author_values = list(set(titles.titles_df.author.to_list()))
    author_values.sort()
    
    genre_values_eng = list(set(titles.titles_df.genre.to_list()))
    genre_values_srb = []
    for genre_lst in GENRES:
        for genre in genre_values_eng:
            if genre == genre_lst[1]:
                genre_values_srb.append(genre_lst[0])
    
    if language == "srpski":
        genre_values = genre_values_srb
    else:
        genre_values = genre_values_eng
    
    genre_values.sort()
    
    year_values = list(set(titles.titles_df.publication_year.to_list()))
    year_values.sort()
    
    search_info_lbl = ttk.Label(
        search_filters_lf,
        text=search_info_text,
        font=("Calibri", 16),
        anchor="nw",
        justify="left",
        bootstyle="light"
    )
    search_info_lbl.grid(column=0, row=0, columnspan=3, padx=50, pady=10,
                         sticky="ew")
    
    search_author_lbl = ttk.Label(
        search_filters_lf,
        text=search_author_text,
        font=("Calibri", 14),
        bootstyle="light"
    )
    search_author_lbl.grid(column=0, row=1, padx=(50, 20), pady=(10, 0),
                           sticky="ew")
    
    search_author_combo = ttk.Combobox(
        search_filters_lf,
        width=25,
        font=("Calibri", 12),
        values=author_values,
        state="readonly",
        bootstyle="light"
    )
    search_author_combo.grid(column=0, row=2, padx=(50, 20), pady=(0, 20),
                             sticky="w")

    # Bind author filter combobox
    search_author_combo.bind("<<ComboboxSelected>>", filter_author)
    
    search_genre_lbl = ttk.Label(
        search_filters_lf,
        text=search_genre_text,
        font=("Calibri", 14),
        bootstyle="light"
    )
    search_genre_lbl.grid(column=1, row=1, padx=20, pady=(10, 0), sticky="ew")
    
    search_genre_combo = ttk.Combobox(
        search_filters_lf,
        width=25,
        font=("Calibri", 12),
        values=genre_values,
        state="readonly",
        bootstyle="light"
    )
    search_genre_combo.grid(column=1, row=2, padx=20, pady=(0, 20),
                             sticky="w")

    # Bind genre filter combobox
    search_genre_combo.bind("<<ComboboxSelected>>", filter_genre)
    
    search_year_lbl = ttk.Label(
        search_filters_lf,
        text=search_year_text,
        font=("Calibri", 14),
        bootstyle="light"
    )
    search_year_lbl.grid(column=2, row=1, padx=(20, 50), pady=(10, 0),
                         sticky="ew")
    
    search_year_combo = ttk.Combobox(
        search_filters_lf,
        width=25,
        font=("Calibri", 12),
        values=year_values,
        state="readonly",
        bootstyle="light"
    )
    search_year_combo.grid(column=2, row=2, padx=(20, 50), pady=(0, 30),
                             sticky="w")

    # Bind publication year filter combobox
    search_year_combo.bind("<<ComboboxSelected>>", filter_year)

    # Widgets in selection frame
    search_selection_lbl = ttk.Label(
        search_selection_lf,
        text=search_selection_text,
        font=("Calibri", 14),
        bootstyle="light"
    )
    search_selection_lbl.grid(column=0, row=0, padx=(50, 20), pady=(10, 0),
                              sticky="ew")

    selection_combo_values = titles.df_list_sort_by_title(titles.titles_df)
    search_selection_combo = ttk.Combobox(
        search_selection_lf,
        width=42,
        font=("Calibri", 12),
        values=selection_combo_values,
        state="readonly",
        bootstyle="light"
    )
    search_selection_combo.grid(column=0, row=1, padx=(50, 20), pady=(0, 30),
                                sticky="w")
    
    # Bind title selection combobox
    search_selection_combo.bind("<<ComboboxSelected>>", search_title_selected)

    # Widgets in info frame
    info_title_lbl_text = language_text("Naslov:", "Title:")
    info_author_lbl_text = language_text("Autor:", "Author:")
    info_genre_lbl_text = language_text("Žanr:", "Genre:")
    info_year_lbl_text = language_text("Godina izdanja:", "Publication year:")
    pic = getting_image()
    
    image_frm = ttk.Frame(search_info_lf)
    image_frm.pack(fill="y", side="left")
    
    data_frm = ttk.Frame(search_info_lf)
    data_frm.pack(expand=True, fill="both", side="left")
    
    search_image_lbl = ttk.Label(image_frm, image=pic)
    search_image_lbl.image = pic
    search_image_lbl.grid(column=0, row=0, padx=50, pady=50, sticky="nw")
    
    search_info_title_lbl = ttk.Label(
        data_frm,
        text=info_title_lbl_text,
        width=20,
        font=("Calibri", 20),
        bootstyle="light"
    )
    search_info_title_lbl.grid(column=0, row=0, padx=20, pady=(50, 0),
                               sticky="w")

    search_info_title_val = ttk.Label(
        data_frm,
        text="-",
        width=45,
        font=("Calibri", 24),
        bootstyle="warning"
    )
    search_info_title_val.grid(column=0, row=1, padx=20, pady=(0, 20),
                               sticky="w")
    
    search_info_author_lbl = ttk.Label(
        data_frm,
        text=info_author_lbl_text,
        width=20,
        font=("Calibri", 20),
        bootstyle="light"
    )
    search_info_author_lbl.grid(column=0, row=2, padx=20, sticky="w")
    
    search_info_author_val = ttk.Label(
        data_frm,
        text="-",
        width=45,
        font=("Calibri", 20),
        bootstyle="warning"
    )
    search_info_author_val.grid(column=0, row=3, padx=20, pady=(0, 20),
                                sticky="w")
    
    search_info_genre_lbl = ttk.Label(
        data_frm,
        text=info_genre_lbl_text,
        width=20,
        font=("Calibri", 20),
        bootstyle="light"
    )
    search_info_genre_lbl.grid(column=0, row=4, padx=20, sticky="w")

    search_info_genre_val = ttk.Label(
        data_frm,
        text="-",
        width=45,
        font=("Calibri", 20),
        bootstyle="warning"
    )
    search_info_genre_val.grid(column=0, row=5, padx=20, pady=(0, 20),
                                sticky="w")
    
    search_info_year_lbl = ttk.Label(
        data_frm,
        text=info_year_lbl_text,
        width=20,
        font=("Calibri", 20),
        bootstyle="light"
    )
    search_info_year_lbl.grid(column=0, row=6, padx=20, sticky="w")

    search_info_year_val = ttk.Label(
        data_frm,
        text="-",
        width=45,
        font=("Calibri", 20),
        bootstyle="warning"
    )
    search_info_year_val.grid(column=0, row=7, padx=20, pady=(0, 40),
                                sticky="w")

    # Button widgets in buttons frame
    search_close_btn_text = language_text("Zatvori", "Close")
    search_close_btn = ttk.Button(
        search_buttons_frm,
        text=search_close_btn_text,
        width=10,
        style="big.dark.TButton",
        command=book_search_tl.destroy
    )
    search_close_btn.pack(padx=(20, 50), pady=(10, 20), side="right")
    
    search_reset_btn_text = language_text("Resetuj", "Reset")
    search_reset_btn = ttk.Button(
        search_buttons_frm,
        text=search_reset_btn_text,
        width=10,
        style="big.dark.TButton",
        command=reset_all
    )
    search_reset_btn.pack(padx=20, pady=(10, 20), side="right")


def most_read_books_list():
    """New window with a list of the ten most read books."""
    
    most_list_title_text = language_text("Lista najčitnijih knjiga",
                                         "List of the most read books")
    
    most_list_tl = ttk.Toplevel(title=most_list_title_text)
    most_list_tl.resizable(False, False)
    most_list_tl.geometry("700x800")
    most_list_tl.grab_set()

    # Scrollable frame for other elements
    most_list_sf = ScrolledFrame(most_list_tl, autohide=True)
    most_list_sf.pack(expand=True, fill="both")
    
    # Frames
    most_list_top_frm = ttk.Frame(most_list_sf)
    most_list_top_frm.pack(fill="x", padx=20, pady=20)
    
    most_list_books_frm = ttk.Frame(most_list_sf)
    most_list_books_frm.pack(fill="x", padx=20, pady=20)
    
    # Top frame
    most_list_main_text = language_text(" Biblioteka \"Vuk Karadžić\"",
                                        " Library \"Vuk Karadžić\"")
    most_list_main_lbl = ttk.Label(
        most_list_top_frm,
        text=most_list_main_text,
        font=("Calibri", 36, "bold"),
        image=logo_smaller,
        compound="left",
        anchor="center",
        bootstyle="warning"
    )
    most_list_main_lbl.pack(expand=True, fill="x")
    
    most_list_title_lbl = ttk.Label(
        most_list_top_frm,
        text=most_list_title_text.upper(),
        font=("Calibri", 28, "bold"),
        anchor="center",
        bootstyle="warning"
    )
    most_list_title_lbl.pack(expand=True, fill="x", pady=10)
    
    # Book list frame
    most_list_books_frm.grid_columnconfigure((0, 1), weight=1)
    
    most_list_readings_text = language_text("Čitanja", "Readings")
    most_list_readings_lbl = ttk.Label(
        most_list_books_frm,
        text=most_list_readings_text,
        font=("Calibri", 16),
        anchor="center",
        bootstyle="light"
    )
    most_list_readings_lbl.grid(column= 0, row=0, padx=20)

    most_list_book_text = language_text("Knjiga", "Book")
    most_list_book_lbl = ttk.Label(
        most_list_books_frm,
        text=most_list_book_text,
        font=("Calibri", 16),
        anchor="center",
        bootstyle="light"
    )
    most_list_book_lbl.grid(column=1, row=0, padx=20, sticky="w")
    
    # Data
    first_ten_read_titles = most_read_books_data()[:10]
    
    # Making a list of the most read titles
    for i in range(len(first_ten_read_titles)):
        ttk.Label(
            most_list_books_frm,
            text=first_ten_read_titles[i][0],
            font=("Calibri", 16)
        ).grid(column=0, row=(2*(i+1)-1), padx=20, pady=(10, 0))
        
        ttk.Label(
            most_list_books_frm,
            text=first_ten_read_titles[i][1],
            font=("Calibri", 16),
            bootstyle="warning"
        ).grid(column=1, row=(2*(i+1)-1), padx=20, pady=(10, 0), sticky="w")
        
        ttk.Label(
            most_list_books_frm,
            text=first_ten_read_titles[i][2],
            font=("Calibri", 16)
        ).grid(column=1, row=2*(i+1), padx=20, pady=(0, 10), sticky="w")
    
    # Close and chart button
    most_list_close_btn_text = language_text("Zatvori", "Close")
    most_list_close_btn = ttk.Button(
        most_list_sf,
        text=most_list_close_btn_text,
        width=10,
        style="big.dark.TButton",
        command=most_list_tl.destroy
    )
    most_list_close_btn.pack(padx=50, pady=30, side="right")
    
    most_list_chart_btn_text = language_text("Grafik", "Chart")
    most_list_chart_btn = ttk.Button(
        most_list_sf,
        text=most_list_chart_btn_text,
        width=10,
        style="big.dark.TButton",
        command=most_read_books_chart
    )
    most_list_chart_btn.pack(pady=30, side="right")


def most_read_books_chart():
    """Chart of the ten most read books."""
    
    first_ten_read_titles = most_read_books_data()[:10]
    
    # Axes and title text
    title_txt = language_text("DESET NAJČITANIJIH NASLOVA",
                              "TEN MOST READ TITLES")
    x_axis_txt = language_text("Broj čitanja", "Readings Number")
    y_axis_txt = language_text("Naslov knjige", "Book Title")
    
    # Axes values
    title_names = []
    readings_number = []
    for i in range(len(first_ten_read_titles)):
        title_names.append(first_ten_read_titles[i][1])
        readings_number.append(first_ten_read_titles[i][0])
    
    # The most read title at the top
    title_names.reverse()
    readings_number.reverse()

    # Bar chart
    fig, ax = plt.subplots(figsize=(16, 8), facecolor="#242124")

    ax.set_facecolor("#242124")
    ax.spines["bottom"].set_color("lightgrey")
    ax.spines["top"].set_color("lightgrey")
    ax.spines["left"].set_color("lightgrey")
    ax.spines["right"].set_color("lightgrey")
    plt.xticks(color="lightgrey")
    plt.yticks(color="lightgrey", rotation=30)
    ax.tick_params(axis="x", colors="lightgrey")
    ax.tick_params(axis="y", colors="lightgrey")
    ax.barh(title_names, readings_number, 0.5, color="#006400")
    plt.title(
        title_txt,
        fontdict={"family": "Calibri", "color": "#0093af", "size": 22,
                  "weight": "bold"},
        pad=30
    )
    plt.xlabel(
        x_axis_txt,
        fontdict={"family": "Calibri", "color": "#0093af", "size": 16,
                  "weight": "bold"},
        labelpad=20
    )
    plt.ylabel(
        y_axis_txt,
        fontdict={"family": "Calibri", "color": "#0093af", "size": 16,
                  "weight": "bold"},
        labelpad=20
    )
    plt.grid()
    plt.subplots_adjust(left=0.23, right=0.96)
    
    plt.show()


def most_read_authors_list():
    """New window with a list of the ten most read authors."""
    
    most_authors_title_text = language_text("Lista najčitanijih autora",
                                            "List of the most read authors")

    most_authors_tl = ttk.Toplevel(title=most_authors_title_text)
    most_authors_tl.resizable(False, False)
    most_authors_tl.geometry("700x800")
    most_authors_tl.grab_set()

    # Scrollable frame for other elements
    most_authors_sf = ScrolledFrame(most_authors_tl, autohide=True)
    most_authors_sf.pack(expand=True, fill="both")

    # Frames
    most_authors_top_frm = ttk.Frame(most_authors_sf)
    most_authors_top_frm.pack(fill="x", padx=20, pady=20)

    most_list_authors_frm = ttk.Frame(most_authors_sf)
    most_list_authors_frm.pack(fill="x", padx=20, pady=20)

    # Top frame
    most_authors_main_text = language_text(" Biblioteka \"Vuk Karadžić\"",
                                           " Library \"Vuk Karadžić\"")

    most_authors_main_lbl = ttk.Label(
        most_authors_top_frm,
        text=most_authors_main_text,
        font=("Calibri", 36, "bold"),
        image=logo_smaller,
        compound="left",
        anchor="center",
        bootstyle="warning"
    )
    most_authors_main_lbl.pack(expand=True, fill="x")

    most_authors_title_lbl = ttk.Label(
        most_authors_top_frm,
        text=most_authors_title_text.upper(),
        font=("Calibri", 28, "bold"),
        anchor="center",
        bootstyle="warning"
    )
    most_authors_title_lbl.pack(expand=True, fill="x", pady=10)

    # Book list frame
    most_list_authors_frm.grid_columnconfigure((0, 1), weight=1)

    most_authors_readings_text = language_text("Čitanja", "Readings")
    most_authors_readings_lbl = ttk.Label(
        most_list_authors_frm,
        text=most_authors_readings_text,
        font=("Calibri", 16),
        anchor="center",
        bootstyle="light"
    )
    most_authors_readings_lbl.grid(column=0, row=0, padx=20)

    most_authors_name_text = language_text("Autor", "Author")
    most_authors_name_lbl = ttk.Label(
        most_list_authors_frm,
        text=most_authors_name_text,
        font=("Calibri", 16),
        anchor="center",
        bootstyle="light"
    )
    most_authors_name_lbl.grid(column=1, row=0, padx=20, sticky="w")

    # Data
    first_ten_read_authors = most_read_authors_data()[:10]

    # Making a list of the most read authors
    for i in range(len(first_ten_read_authors)):
        ttk.Label(
            most_list_authors_frm,
            text=first_ten_read_authors[i][0],
            font=("Calibri", 16)
        ).grid(column=0, row=(i+1), padx=20, pady=(10, 0))
    
        ttk.Label(
            most_list_authors_frm,
            text=first_ten_read_authors[i][1],
            font=("Calibri", 16),
            bootstyle="warning"
        ).grid(column=1, row=(i+1), padx=20, pady=(10, 0), sticky="w")

    # Close and chart button
    most_authors_close_btn_text = language_text("Zatvori", "Close")
    most_authors_close_btn = ttk.Button(
        most_authors_sf,
        text=most_authors_close_btn_text,
        width=10,
        style="big.dark.TButton",
        command=most_authors_tl.destroy
    )
    most_authors_close_btn.pack(padx=50, pady=(40, 30), side="right")

    most_authors_chart_btn_text = language_text("Grafik", "Chart")
    most_authors_chart_btn = ttk.Button(
        most_authors_sf,
        text=most_authors_chart_btn_text,
        width=10,
        style="big.dark.TButton",
        command=most_read_authors_chart
    )
    most_authors_chart_btn.pack(pady=(40, 30), side="right")


def most_read_authors_chart():
    """Chart of the ten most read authors."""

    first_ten_read_authors = most_read_authors_data()[:10]

    # Axes and title text
    title_txt = language_text("DESET NAJČITANIJIH AUTORA",
                              "TEN MOST READ AUTHORS")
    x_axis_txt = language_text("Broj čitanja", "Readings Number")
    y_axis_txt = language_text("Ime autora", "Author's Name")

    # Axes values
    title_names = []
    readings_number = []
    for i in range(len(first_ten_read_authors)):
        title_names.append(first_ten_read_authors[i][1])
        readings_number.append(first_ten_read_authors[i][0])

    # The most read authors at the top
    title_names.reverse()
    readings_number.reverse()

    # Bar chart
    fig, ax = plt.subplots(figsize=(16, 8), facecolor="#242124")

    ax.set_facecolor("#242124")
    ax.spines["bottom"].set_color("lightgrey")
    ax.spines["top"].set_color("lightgrey")
    ax.spines["left"].set_color("lightgrey")
    ax.spines["right"].set_color("lightgrey")
    plt.xticks(color="lightgrey")
    plt.yticks(color="lightgrey")
    ax.tick_params(axis="x", colors="lightgrey")
    ax.tick_params(axis="y", colors="lightgrey")
    ax.barh(title_names, readings_number, 0.5, color="#9b111e")
    plt.title(title_txt,
        fontdict={"family": "Calibri", "color": "#ffbf00", "size": 22,
                  "weight": "bold"}, pad=30)
    plt.xlabel(x_axis_txt,
        fontdict={"family": "Calibri", "color": "#ffbf00", "size": 16,
                  "weight": "bold"}, labelpad=20)
    plt.ylabel(y_axis_txt,
        fontdict={"family": "Calibri", "color": "#ffbf00", "size": 16,
                  "weight": "bold"}, labelpad=20)
    plt.grid()
    plt.subplots_adjust(left=0.16, right=0.96)

    plt.show()


def read_by_genre():
    """How many books have been read from each genre."""
    
    genre_title_text = language_text("Pročitano po žanru",
                                     "Read by genre")
    
    genre_tl = ttk.Toplevel(title=genre_title_text)
    genre_tl.resizable(False, False)
    genre_tl.geometry("650x800")
    genre_tl.attributes("-topmost", "true")
    genre_tl.grab_set()

    # Scrollable frame for other elements
    genre_sf = ScrolledFrame(genre_tl, autohide=True)
    genre_sf.pack(expand=True, fill="both")

    # Frames
    genre_top_frm = ttk.Frame(genre_sf)
    genre_top_frm.pack(fill="x", padx=20, pady=20)

    genre_read_books_frm = ttk.Frame(genre_sf)
    genre_read_books_frm.pack(fill="x", padx=20, pady=20)

    # Top frame
    genre_main_text = language_text(" Biblioteka \"Vuk Karadžić\"",
                                    " Library \"Vuk Karadžić\"")

    genre_main_lbl = ttk.Label(
        genre_top_frm,
        text=genre_main_text,
        font=("Calibri", 36, "bold"),
        image=logo_smaller,
        compound="left",
        anchor="center",
        bootstyle="warning"
    )
    genre_main_lbl.pack(expand=True, fill="x")

    genre_title_lbl = ttk.Label(
        genre_top_frm,
        text=genre_title_text.upper(),
        font=("Calibri", 28, "bold"),
        anchor="center",
        bootstyle="warning"
    )
    genre_title_lbl.pack(expand=True, fill="x", pady=10)
    
    # Read books by genre frame
    genre_read_books_frm.grid_columnconfigure((0, 1), weight=1)
    
    genre_genre_text = language_text("Žanr"," Genre")
    genre_genre_lbl = ttk.Label(
        genre_read_books_frm,
        text=genre_genre_text,
        font=("Calibri", 16),
        anchor="center",
        bootstyle="light"
    )
    genre_genre_lbl.grid(column= 0, row=0, padx=(50, 25))
    
    genre_read_books_text = language_text("Čitanja", "Readings")
    genre_read_books_lbl = ttk.Label(
        genre_read_books_frm,
        text=genre_read_books_text,
        font=("Calibri", 16),
        anchor="center",
        bootstyle="light"
    )
    genre_read_books_lbl.grid(column=1, row=0, padx=(25, 50))
    
    # Creating a list of genres
    genres_list = creating_values_list(GENRES)[1]
    genres_list_srb = creating_values_list(GENRES)[0]

    # List of books for each genre from 'genres_list'
    books_of_genre = []
    for genre in genres_list:
        books_list = titles.titles_df.title[
            titles.titles_df.genre == genre].to_list()
        books_of_genre.append(books_list)

    # Calculating of reading numbers by genre
    titles_read = most_read_books_data()
    
    total_genre_read = []
    for i in range(len(books_of_genre)):
        total_read_from_one_genre = 0
        for j in range(len(books_of_genre[i])):
            for k in range(len(titles_read)):
                if books_of_genre[i][j] == titles_read[k][1]:
                    total_read_from_one_genre += titles_read[k][0]
        total_genre_read.append(total_read_from_one_genre)
    
    # Creating a label widgets with appropriate values
    for i in range(len(genres_list)):
        pic = getting_image(genre=genres_list[i], img_size=(30, 30))
        image_genre_lbl = ttk.Label(
            genre_read_books_frm,
            text=language_text(f"   {genres_list_srb[i]}",
                               f"   {genres_list[i]}"),
            image=pic,
            compound="left",
            font=("Calibri", 16),
            bootstyle="warning"
        )
        image_genre_lbl.grid(column=0, row=(i+1), padx=(50, 25), pady=(10, 0),
                             sticky="w")
        image_genre_lbl.image = pic
        
        ttk.Label(
            genre_read_books_frm,
            text=total_genre_read[i],
            font=("Calibri", 16)
        ).grid(column=1, row=(i+1), padx=(25, 50), pady=(10, 0))

    # Close button
    genre_close_btn_text = language_text("Zatvori", "Close")
    genre_close_btn = ttk.Button(
        genre_sf,
        text=genre_close_btn_text,
        width=10,
        style="big.dark.TButton",
        command=genre_tl.destroy
    )
    genre_close_btn.pack(padx=50, pady=(40, 30), side="right")


def member_login():
    """Access to the personal member section."""
    
    def mem_apply_login():
        """Actions when the 'Apply' ('Primeni') button is pressed."""
        global member_status
        global logged_in_member_code

        # Texts for messageboxes
        mem_title_text = language_text("Nedostaje unos", "Missing entry")
        mem_message_id_text = language_text("Niste uneli svoj ID!",
                                            "You have not entered your ID!")
        mem_message_password_text = language_text(
            "Niste uneli svoju lozinku!",
            "You have not entered your password!"
        )
        mem_invalid_id_title_text = language_text("Pogrešan ID", "Invalid ID")
        mem_invalid_id_msg_text = language_text(
            "ID koji ste uneli ne postoji u bazi podataka.",
            "The ID you entered does not exist in the database."
        )
        mem_invalid_pass_title_text = language_text("Pogrešna lozinka",
                                                    "Invalid password")
        mem_invalid_pass_msg_text = language_text(
            "Niste uneli ispravnu lozinku.",
            "You have not entered the correct password."
        )
        
        # All member IDs
        member_ids = members.members_df.membership_id.to_list()

        # Checking if the entry fields are filled and the data is valid
        if not mem_id_entry.get():
            Messagebox.show_info(
                title=mem_title_text,
                message=mem_message_id_text,
                parent=member_login_tl,
                alert=True
            )
        elif not mem_password_entry.get():
            Messagebox.show_info(
                title=mem_title_text,
                message=mem_message_password_text,
                parent=member_login_tl,
                alert=True
            )
        elif mem_id_entry.get() not in member_ids:
            Messagebox.show_info(
                title=mem_invalid_id_title_text,
                message=mem_invalid_id_msg_text,
                parent=member_login_tl,
                alert=True
            )
        elif mem_password_entry.get() != members.members_df.password[
            members.members_df.membership_id ==
            mem_id_entry.get()].to_string(index=False):
            Messagebox.show_info(
                title=mem_invalid_pass_title_text,
                message=mem_invalid_pass_msg_text,
                parent=member_login_tl,
                alert=True
            )
        else:
            logged_in_member_code = mem_id_entry.get()
            mem_logged_in = logged_in_member()
    
            member_status = "active"
            ui_create()
            login_picture = login_image()
            login_lbl.configure(image=login_picture)
            login_lbl.image = login_picture
            tooltip_txt = language_text(f"Član: {mem_logged_in}",
                                               f"Member: {mem_logged_in}")
            ToolTip(login_lbl, text=tooltip_txt, bootstyle="warning")
            login_btn.configure(text=language_text("Odjavite se", "Log out"))
            member_login_tl.destroy()
    
    def mem_logout():
        """Librarian logout."""
        global member_status
        global logged_in_member_code

        member_status = "inactive"
        ui_create()
        login_picture = login_image()
        login_lbl.configure(image=login_picture)
        login_lbl.image = login_picture
        tooltip_txt = language_text("Korisnik nije prijavljen",
                                    "User is not logged in")
        ToolTip(login_lbl, text=tooltip_txt, bootstyle="warning")
        login_btn.configure(text=language_text("Prijavite se", "Log In"))
        member_logout_tl.destroy()

    if member_status == "inactive":
        member_login_title = language_text("Prijavljivanje člana",
                                           "Member login")
        
        member_login_tl = ttk.Toplevel(title=member_login_title)
        member_login_tl.attributes("-topmost", "true")
        member_login_tl.resizable(False, False)
        member_login_tl.geometry("500x350")
        member_login_tl.grab_set()
        
        # Title
        mem_title_lbl = ttk.Label(
            member_login_tl,
            text=member_login_title.upper(),
            font=("Calibri", 24, "bold"),
            bootstyle="warning"
        )
        mem_title_lbl.pack(padx=30, pady=15)
        
        # Login labels and entries.
        mem_id_text = language_text("Unesite vaš ID:", "Enter your ID:")
        mem_id_lbl = ttk.Label(
            member_login_tl,
            text=mem_id_text,
            font=("Calibri", 14),
            bootstyle="light"
        )
        mem_id_lbl.pack(fill="x", padx=40, pady=(15, 0))
        
        mem_id_reg = member_login_tl.register(
            lambda inp: len_digit_limit(inp, length=6))
        mem_id_entry = ttk.Entry(
            member_login_tl,
            font=("Calibri", 14),
            validate="key",
            validatecommand=(mem_id_reg, "%P")
        )
        mem_id_entry.pack(fill="x", padx=40, pady=(0, 20))
        mem_id_entry.focus()
        
        mem_password_text = language_text("Unesite vašu lozinku:",
                                          "Enter your password:")
        mem_password_lbl = ttk.Label(
            member_login_tl,
            text=mem_password_text,
            font=("Calibri", 14),
            bootstyle="light"
        )
        mem_password_lbl.pack(fill="x", padx=40)

        mem_password_entry = ttk.Entry(
            member_login_tl,
            font=("Calibri", 14),
            show="*"
        )
        mem_password_entry.pack(fill="x", padx=40, pady=(0, 20))

        # Buttons and frame for them
        mem_buttons_frm = ttk.Frame(member_login_tl)
        mem_buttons_frm.pack(expand=True, fill="x", padx=40, pady=(10, 30))

        mem_cancel_text = language_text("Otkaži", "Cancel")
        mem_cancel_btn = ttk.Button(
            mem_buttons_frm,
            width=10,
            text=mem_cancel_text,
            style="big.dark.TButton",
            command=member_login_tl.destroy
        )
        mem_cancel_btn.pack(side="right")

        mem_apply_text = language_text("Primeni", "Apply")
        mem_apply_btn = ttk.Button(
            mem_buttons_frm,
            width=10,
            text=mem_apply_text,
            style="big.dark.TButton",
            command=mem_apply_login
        )
        mem_apply_btn.pack(padx=30, side="right")

        # Binding 'Return' and 'Esc' keystrokes to buttons
        member_login_tl.bind("<Return>",
                             (lambda event: mem_apply_btn.invoke()))
        member_login_tl.bind("<Key-Escape>",
                             (lambda event: mem_cancel_btn.invoke()))
    else:
        member_logout_title = language_text("Odjavljivanje člana",
                                            "Member logout")
        member_logout_tl = ttk.Toplevel(title=member_logout_title)
        member_logout_tl.attributes("-topmost", "true")
        member_logout_tl.resizable(False, False)
        member_logout_tl.geometry("500x300")
        member_logout_tl.grab_set()

        # Logged in member
        member_logged_in = logged_in_member()
        mem_logged_in_text = language_text(f"Član: {member_logged_in}",
                                           f"Member: {member_logged_in}")
        mem_logged_in_lbl = ttk.Label(
            member_logout_tl,
            text=mem_logged_in_text,
            font=("Calibri", 16),
            bootstyle="danger"
        )
        mem_logged_in_lbl.pack(padx=20, pady=10)

        # Title
        mem_logout_title_lbl = ttk.Label(
            member_logout_tl,
            text=member_logout_title.upper(),
            font=("Calibri", 24, "bold"),
            bootstyle="warning"
        )
        mem_logout_title_lbl.pack(padx=30, pady=15)

        # Buttons
        mem_logout_apply_text = language_text("Odjavite se", "Log out")
        mem_logout_apply_btn = ttk.Button(
            member_logout_tl, width=20,
            text=mem_logout_apply_text.upper(),
            style="huge.primary.TButton",
            command=mem_logout
        )
        mem_logout_apply_btn.pack(pady=10)

        mem_logout_cancel_text = language_text("Otkaži", "Cancel")
        mem_logout_cancel_btn = ttk.Button(
            member_logout_tl, width=10,
            text=mem_logout_cancel_text,
            style="big.dark.TButton",
            command=member_logout_tl.destroy
        )
        mem_logout_cancel_btn.pack(side="right", padx=30, pady=10)


def reservation_info(membership_id):
    """Information about the current reservation."""

    reserved_book_df = reservations.reservations_df[
        reservations.reservations_df.membership_id == membership_id]
    reserved_book_codes = reserved_book_df.book_code.to_list()
    reserved_dates = reserved_book_df.reservation_date.to_list()

    total_reserved = len(reserved_book_codes)
    if reserved_dates:
        last_date = max(reserved_dates)

    reserved_book = "-"
    expire_date_str = "-"
    for code in reserved_book_codes:
        if books.books_df.availability[
            books.books_df.book_code == code].to_string(
            index=False) == "Reserved":
            reserved_code = code
            reserved_title = books.books_df.title[
                books.books_df.book_code == code].to_string(index=False)
            reserved_book = f"{reserved_title} - {reserved_code}"
            expire_date = last_date + timedelta(days=7)
            expire_date_str = expire_date.strftime("%d. %m. %Y.")
    
    return reserved_book, expire_date_str, total_reserved


def member_details():
    """Details of the member's account."""
    
    details_title_text = language_text("Detalji naloga", "Account details")
    
    details_tl = ttk.Toplevel(title=details_title_text)
    details_tl.resizable(False, False)
    details_tl.geometry("700x900")
    details_tl.grab_set()
    
    # Lists of book codes, membership IDs and rental dates of rented books
    rented_df = renting.renting_df[renting.renting_df.return_date.isnull()]
    code_id_date = []
    for index, rows in rented_df.iterrows():
        row_list = [rows.book_code, rows.membership_id, rows.rental_date]
        code_id_date.append(row_list)
    
    # Scrollable frame for other elements
    details_sf = ScrolledFrame(details_tl, autohide=True)
    details_sf.pack(expand=True, fill="both")
    
    # Frames
    details_top_frm = ttk.Frame(details_sf)
    details_top_frm.pack(fill="x", padx=20, pady=20)
    
    details_member_text = language_text(" Član ", " Member ")
    details_member_frm = ttk.LabelFrame(
        details_sf,
        text=details_member_text,
        bootstyle="warning"
    )
    details_member_frm.pack(fill="x", padx=20, pady=20)
    
    details_rent_text = language_text(" Iznajmljivanje ", " Renting ")
    details_rent_frm = ttk.LabelFrame(
        details_sf,
        text=details_rent_text,
        bootstyle="warning"
    )
    details_rent_frm.pack(fill="x", padx=20, pady=20)
    
    details_reserve_text = language_text(" Rezervacija ", " Reserevation ")
    details_reserve_frm = ttk.LabelFrame(
        details_sf,
        text=details_reserve_text,
        bootstyle="warning"
    )
    details_reserve_frm.pack(fill="x", padx=20, pady=20)
    
    # Top frame
    details_main_text = language_text(" Biblioteka \"Vuk Karadžić\"",
                                      " Library \"Vuk Karadžić\"")
    details_main_lbl = ttk.Label(
        details_top_frm,
        text=details_main_text,
        font=("Calibri", 36, "bold"),
        image=logo_smaller,
        compound="left",
        anchor="center",
        bootstyle="warning"
    )
    details_main_lbl.pack(fill="x")
    
    details_title_lbl = ttk.Label(
        details_top_frm,
        text=details_title_text.upper(),
        font=("Calibri", 28, "bold"),
        anchor="center",
        bootstyle="warning"
    )
    details_title_lbl.pack(fill="x", pady=10)
    
    # Member frame
    details_member_frm.grid_columnconfigure((0, 1), weight=1, uniform="a")
    
    details_member_name_text = language_text("Ime člana:", "Member's name:")
    details_member_name_lbl = ttk.Label(
        details_member_frm,
        text=details_member_name_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    details_member_name_lbl.grid(column=0, row=0, padx=50, pady=(10, 0),
                                 sticky="w")
    
    member_logged_in = logged_in_member()
    details_member_name_val = ttk.Label(
        details_member_frm,
        text=member_logged_in,
        font=("Calibri", 16),
        bootstyle="warning"
    )
    details_member_name_val.grid(column=0, row=1, padx=50, pady=(0, 10),
                                 sticky="w")
    
    details_member_id_text = language_text("Broj članske karte:",
                                           "Membership ID:")
    details_member_id_lbl = ttk.Label(
        details_member_frm,
        text=details_member_id_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    details_member_id_lbl.grid(column=1, row=0, padx=50, pady=(10, 0),
                               sticky="w")
    
    details_member_id_val = ttk.Label(
        details_member_frm,
        text=logged_in_member_code,
        font=("Calibri", 16),
        bootstyle="warning"
    )
    details_member_id_val.grid(column=1, row=1, padx=50, pady=(0, 10),
                               sticky="w")
    
    # Renting frame
    details_rent_frm.grid_columnconfigure((0, 1), weight=1, uniform="a")
    
    # Data needed
    for i in range(len(code_id_date)):
        if logged_in_member_code == code_id_date[i][1]:
            rented_title = books.books_df.title[
                books.books_df.book_code == code_id_date[i][0]].to_string(
                index=False)
            rented_code = code_id_date[i][0]
            rented_book = f"{rented_title} - {rented_code}"
            rented_date = code_id_date[i][2]
            rented_date_str = rented_date.strftime("%d. %m. %Y.")
            return_date = rented_date + timedelta(days=15)
            return_date_str = return_date.strftime("%d. %m. %Y.")
            break
        else:
            rented_book = "-"
            rented_date_str = "-"
            return_date_str = "-"
    
    details_rent_title_text = language_text(
        "Trenutno iznajmljena knjiga i njena šifra:",
        "Currently rented book and its code:"
    )
    details_rent_title_lbl = ttk.Label(
        details_rent_frm,
        text=details_rent_title_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    details_rent_title_lbl.grid(column=0, row=0, columnspan=2, padx=50,
                                pady=(10, 0), sticky="w")
    
    details_rent_title_val = ttk.Label(
        details_rent_frm,
        text=rented_book,
        font=("Calibri", 16),
        bootstyle="warning"
    )
    details_rent_title_val.grid(column=0, row=1, columnspan=2, padx=50,
                                pady=(0, 10), sticky="w")
    
    details_rent_date_text = language_text("Datum iznajmljivanja:",
                                           "Rental date:")
    details_rent_date_lbl = ttk.Label(
        details_rent_frm,
        text=details_rent_date_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    details_rent_date_lbl.grid(column=0, row=2, padx=50, pady=(10, 0),
                               sticky="w")
    
    details_rent_date_val = ttk.Label(
        details_rent_frm,
        text=rented_date_str,
        font=("Calibri", 16),
        bootstyle="warning"
    )
    details_rent_date_val.grid(column=0, row=3, padx=50, pady=(0, 10),
                               sticky="w")
    
    details_return_date_text = language_text("Istek roka:", "Expiration date:")
    details_return_date_lbl = ttk.Label(
        details_rent_frm,
        text=details_return_date_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    details_return_date_lbl.grid(column=1, row=2, padx=50, pady=(10, 0),
                                 sticky="w")
    
    details_return_date_val = ttk.Label(
        details_rent_frm,
        text=return_date_str,
        font=("Calibri", 16),
        bootstyle="warning"
    )
    details_return_date_val.grid(column=1, row=3, padx=50, pady=(0, 10),
                                 sticky="w")
    
    details_rent_previously_text = language_text("Ranije iznajmljivano:",
                                                 "Previously rented:")
    details_rent_previously_lbl = ttk.Label(
        details_rent_frm,
        text=details_rent_previously_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    details_rent_previously_lbl.grid(column=0, row=4, padx=50, pady=(10, 0),
                                     sticky="w")
    
    previously_rented = renting.renting_df[
        renting.renting_df.membership_id == logged_in_member_code
    ]["return_date"].count()
    details_rent_previously_val = ttk.Label(
        details_rent_frm,
        text=previously_rented,
        font=("Calibri", 16),
        bootstyle="warning"
    )
    details_rent_previously_val.grid(column=0, row=5, padx=50, pady=(0, 10),
                                     sticky="w")
    
    details_rent_not_on_time_text = language_text("Nije vraćeno na vreme:",
                                                  "Not returned on time:")
    details_rent_not_on_time_lbl = ttk.Label(
        details_rent_frm,
        text=details_rent_not_on_time_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    details_rent_not_on_time_lbl.grid(column=1, row=4, padx=50, pady=(10, 0),
                                      sticky="w")
    
    missed_deadline = not_on_time(logged_in_member_code)
    details_rent_not_on_time_val = ttk.Label(
        details_rent_frm,
        text=missed_deadline,
        font=("Calibri", 16),
        bootstyle="warning")
    details_rent_not_on_time_val.grid(column=1, row=5, padx=50, pady=(0, 10),
                                      sticky="w")
    
    # Reservation frame
    details_reserve_frm.grid_columnconfigure((0, 1), weight=1, uniform="a")
    
    # Data needed
    reservation_data = reservation_info(logged_in_member_code)
    
    details_reserve_title_text = language_text(
        "Trenutno rezervisana knjiga i njena šifra:",
        "Currently reserved book and its code:"
    )
    details_reserve_title_lbl = ttk.Label(
        details_reserve_frm,
        text=details_reserve_title_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    details_reserve_title_lbl.grid(column=0, row=0, columnspan=2, padx=50,
                                   pady=(10, 0), sticky="w")
    
    details_reserve_title_val = ttk.Label(
        details_reserve_frm,
        text=reservation_data[0],
        font=("Calibri", 16),
        bootstyle="warning"
    )
    details_reserve_title_val.grid(column=0, row=1, columnspan=2, padx=50,
                                   pady=(0, 10), sticky="w")
    
    details_reserve_expire_text = language_text("Rezervacija važi do:",
                                                "Reservation is valid until:")
    details_reserve_expire_lbl = ttk.Label(
        details_reserve_frm,
        text=details_reserve_expire_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    details_reserve_expire_lbl.grid(column=0, row=2, padx=50, pady=(10, 0),
                                    sticky="w")
    
    details_reserve_expire_val = ttk.Label(
        details_reserve_frm,
        text=reservation_data[1],
        font=("Calibri", 16),
        bootstyle="warning"
    )
    details_reserve_expire_val.grid(column=0, row=3, padx=50, pady=(0, 10),
                                    sticky="w")
    
    details_reserve_previously_text = language_text("Ukupno rezervacija:",
                                                    "Total reservation:")
    details_reserve_previously_lbl = ttk.Label(
        details_reserve_frm,
        text=details_reserve_previously_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    details_reserve_previously_lbl.grid(column=1, row=2, padx=50, pady=(10, 0),
                                        sticky="w")
    
    details_reserve_previously_val = ttk.Label(
        details_reserve_frm,
        text=reservation_data[2],
        font=("Calibri", 16),
        bootstyle="warning"
    )
    details_reserve_previously_val.grid(column=1, row=3, padx=50, pady=(0, 10),
                                        sticky="w")
    
    # Close button
    details_close_btn_text = language_text("Zatvori", "Close")
    details_close_btn = ttk.Button(
        details_sf,
        text=details_close_btn_text,
        width=10,
        style="big.dark.TButton",
        command=details_tl.destroy
    )
    details_close_btn.pack(padx=50, pady=(20, 40), side="right")


def book_reservation():
    """Book reservation form."""
    
    def new_title_selected(event):
        """Changes when a title is selected."""
        reserve_reserve_btn.configure(state="normal")
        
        # Number of available copies for the selected title.
        copies_available = books.books_df[
            (books.books_df.title == reserve_new_combo.get()) &
            (books.books_df.availability == "Available")
            ]["availability"].count()
        
        reserve_available_val.configure(text=copies_available)
    
    def reservation_apply():
        """Entering data into tables and applying other changes."""
        
        available_codes = books.books_df.book_code[
            (books.books_df.title == reserve_new_combo.get()) &
            (books.books_df.availability == "Available")
            ].to_list()
        
        code_picked = random.choice(available_codes)
        
        # Texts for messageboxes
        error_title = language_text("Greška", "Error")
        error_message = language_text(
            "Došlo je do greške prilikom rezervacije.",
            "An error occurred during the reservation."
        )
        success_title = language_text("Proces završen", "Proccess complete")
        success_message = language_text(
            "Proces rezervacije uspešno je završen.",
            "The reservation process has been successfully completed."
        )
        
        try:
            reservations.reservation_entering(code_picked,
                                              logged_in_member_code)
            books.set_book_status(code=code_picked, status="Reserved")
            
            res_info = reservation_info(logged_in_member_code)
            
            reserve_current_title_code_val.configure(text=res_info[0])
            reserve_current_expire_val.configure(text=res_info[1])
            reserve_reserve_btn.configure(state="disabled")
            reserve_cancel_btn.configure(state="normal")
            reserve_new_combo.set("")
            reserve_new_combo.configure(state="disabled")
            reserve_available_val.configure(text="-")
        except:
            Messagebox.show_error(
                title=error_title,
                message=error_message,
                parent=reservation_tl,
                alert=True
            )
        else:
            Messagebox.show_info(
                title=success_title,
                message=success_message,
                parent=reservation_tl,
                alert=True
            )
    
    def cancel_reservation():
        """Cancellation of reservation (book availability = 'Available') and
        changes on other widgets."""
        
        res_info = reservation_info(logged_in_member_code)
        reserved_book_code = res_info[0][-10:]

        # Texts for messageboxes
        error_title = language_text("Greška", "Error")
        error_message = language_text(
            "Došlo je do greške prilikom otkazivanja rezervacije.",
            "An error occurred while canceling the reservation."
        )
        success_title = language_text("Proces završen", "Proccess complete")
        success_message = language_text(
            "Otkazivanje rezervacije uspešno je završeno.",
            "The reservation cancelling has been successfully completed."
        )
        
        try:
            books.set_book_status(code=reserved_book_code, status="Available")
            
            update_info = reservation_info(logged_in_member_code)
    
            reserve_current_title_code_val.configure(text=update_info[0])
            reserve_current_expire_val.configure(text=update_info[1])
            reserve_new_combo.configure(state="readonly")
            reserve_cancel_btn.configure(state="disabled")
        except:
            Messagebox.show_error(
                title=error_title,
                message=error_message,
                parent=reservation_tl,
                alert=True
            )
        else:
            Messagebox.show_info(
                title=success_title,
                message=success_message,
                parent=reservation_tl,
                alert=True
            )
    
    book_reservation_title = language_text("Rezervacija knjige",
                                           "Book reservation")
    
    reservation_tl = ttk.Toplevel(title=book_reservation_title)
    reservation_tl.attributes("-topmost", "true")
    reservation_tl.resizable(False, False)
    reservation_tl.geometry("700x800")
    reservation_tl.grab_set()
    
    # Frames
    reserve_top_frm = ttk.Frame(reservation_tl)
    reserve_top_frm.pack(fill="x", padx=20, pady=20)
    
    reserve_current_text = language_text(" Trenutno rezervisano ",
                                         " Currently reserved ")
    reserve_current_frm = ttk.LabelFrame(
        reservation_tl,
        text=reserve_current_text,
        bootstyle="warning"
    )
    reserve_current_frm.pack(fill="x", padx=20, pady=20)
    
    reserve_new_text = language_text(" Nova rezervacija ", " New reservation ")
    reserve_new_frm = ttk.LabelFrame(
        reservation_tl,
        text=reserve_new_text,
        bootstyle="warning"
    )
    reserve_new_frm.pack(fill="x", padx=20, pady=20)
    
    # Top frame
    reserve_main_text = language_text(" Biblioteka \"Vuk Karadžić\"",
                                      " Library \"Vuk Karadžić\"")
    reserve_main_lbl = ttk.Label(
        reserve_top_frm,
        text=reserve_main_text,
        font=("Calibri", 36, "bold"),
        image=logo_smaller,
        compound="left",
        anchor="center",
        bootstyle="warning"
    )
    reserve_main_lbl.pack(expand=True, fill="x")
    
    member_logged_in = logged_in_member()
    reserve_member_text = language_text(f"Član: {member_logged_in}",
                                        f"Member: {member_logged_in}")
    reserve_member_lbl = ttk.Label(
        reserve_top_frm,
        text=reserve_member_text,
        font=("Calibri", 16),
        bootstyle="danger"
    )
    reserve_member_lbl.pack(pady=10)
    
    reserve_title_lbl = ttk.Label(
        reserve_top_frm,
        text=book_reservation_title.upper(),
        font=("Calibri", 28, "bold"),
        anchor="center",
        bootstyle="warning"
    )
    reserve_title_lbl.pack(expand=True, fill="x", pady=(0, 10))
    
    # Currently reserved frame
    reserve_data = reservation_info(logged_in_member_code)
    
    reserve_current_title_code_text = language_text(
        "Trenutno rezervisana knjiga i njena šifra:",
        "Currently reserved book and its code:"
    )
    reserve_current_title_code_lbl = ttk.Label(
        reserve_current_frm,
        text=reserve_current_title_code_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    reserve_current_title_code_lbl.grid(column=0, row=0, padx=50, pady=(10, 0),
                                        sticky="w")
    
    reserve_current_title_code_val = ttk.Label(
        reserve_current_frm,
        text=reserve_data[0],
        font=("Calibri", 16),
        bootstyle="warning"
    )
    reserve_current_title_code_val.grid(column=0, row=1, padx=50, pady=(0, 10),
                                        sticky="w")
    
    reserve_current_expire_text = language_text("Rezervacija ističe:",
                                                "Reservation expires:")
    reserve_current_expire_lbl = ttk.Label(
        reserve_current_frm,
        text=reserve_current_expire_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    reserve_current_expire_lbl.grid(column=0, row=2, padx=50, pady=(10, 0),
                                    sticky="w")
    
    reserve_current_expire_val = ttk.Label(
        reserve_current_frm,
        text=reserve_data[1],
        font=("Calibri", 16),
        bootstyle="warning"
    )
    reserve_current_expire_val.grid(column=0, row=3, padx=50, pady=(0, 10),
                                    sticky="w")
    
    # New reservation frame
    reserve_new_lbl_text = language_text("Izbor naslova:", "Title selection:")
    reserve_new_lbl = ttk.Label(
        reserve_new_frm,
        text=reserve_new_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    reserve_new_lbl.grid(column=0, row=0, padx=50, pady=(10, 0), sticky="w")
    
    titles_sorted_list = titles.df_list_sort_by_title(titles.titles_df)
    reserve_new_combo = ttk.Combobox(
        reserve_new_frm,
        width=42,
        font=("Calibri", 14),
        values=titles_sorted_list,
        state="readonly",
        bootstyle="warning"
    )
    reserve_new_combo.grid(column=0, row=1, padx=50, pady=(0, 10), sticky="w")
    
    # Bind combobox
    reserve_new_combo.bind("<<ComboboxSelected>>", new_title_selected)
    
    reserve_available_text = language_text("Dostupno primeraka:",
                                           "Copies available:")
    reserve_available_lbl = ttk.Label(
        reserve_new_frm,
        text=reserve_available_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    reserve_available_lbl.grid(column=0, row=2, padx=50, pady=(10, 0),
                               sticky="w")
    
    reserve_available_val = ttk.Label(
        reserve_new_frm,
        text="-",
        font=("Calibri", 16),
        bootstyle="warning"
    )
    reserve_available_val.grid(column=0, row=3, padx=50, pady=(0, 10),
                               sticky="w")
    
    # Buttons
    reserve_close_btn_text = language_text("Zatvori", "Close")
    reserve_close_btn = ttk.Button(
        reservation_tl,
        text=reserve_close_btn_text,
        width=10,
        style="big.dark.TButton",
        command=reservation_tl.destroy
    )
    reserve_close_btn.pack(padx=(15, 30), pady=(10, 20), side="right")
    
    reserve_cancel_btn_text = language_text("Otkaži", "Cancel")
    reserve_cancel_btn = ttk.Button(
        reservation_tl,
        text=reserve_cancel_btn_text,
        width=10,
        style="big.dark.TButton",
        command=cancel_reservation
    )
    reserve_cancel_btn.pack(padx=15, pady=(10, 20), side="right")
    
    reserve_reserve_btn_text = language_text("Rezerviši", "Reserve")
    reserve_reserve_btn = ttk.Button(
        reservation_tl,
        text=reserve_reserve_btn_text,
        width=10,
        style="big.dark.TButton",
        command=reservation_apply
    )
    reserve_reserve_btn.pack(padx=15, pady=(10, 20), side="right")
    
    # Set buttons and combobox states
    reserve_reserve_btn.configure(state="disabled")
    
    if reserve_data[0] == "-":
        reserve_cancel_btn.configure(state="disabled")
    else:
        reserve_new_combo.configure(state="disabled")


def password_change():
    """Logged in member can change his/her password."""
    
    def change_password_apply():
        """Completing the password change."""
        
        old_password = members.members_df.password[
            members.members_df.membership_id == logged_in_member_code
        ].to_string(index=False)
        
        title_text = language_text("Nedostaje unos", "Missing entry")
        
        if not old_password_entry.get():
            missing_old_pass_message = language_text(
                "Niste uneli vrednost za trenutnu lozinku.",
                "You have not entered a value for the current password."
            )
            Messagebox.show_info(
                title=title_text,
                message=missing_old_pass_message,
                parent=member_pass_tl,
                alert=True
            )
        elif old_password_entry.get() != old_password:
            incorrect_password_title = language_text("Pogrešna lozinka",
                                                     "Incorrect password")
            incorrect_password_message = language_text(
                "Niste uneli ispravnu lozinku.",
                "You have not entered the correct password."
            )
            Messagebox.show_info(
                title=incorrect_password_title,
                message=incorrect_password_message,
                parent=member_pass_tl,
                alert=True
            )
        elif not new_password_1st_entry.get():
            missing_1st_new_pass_message = language_text(
                "Niste uneli prvu vrednost za novu lozinku.",
                "You did not enter a first value for the new password."
            )
            Messagebox.show_info(
                title=title_text,
                message=missing_1st_new_pass_message,
                parent=member_pass_tl,
                alert=True
            )
        elif not new_password_2nd_entry.get():
            missing_2nd_new_pass_message = language_text(
                "Niste uneli drugu vrednost za novu lozinku.",
                "You did not enter a second value for the new password.")
            Messagebox.show_info(
                title=title_text,
                message=missing_2nd_new_pass_message,
                parent=member_pass_tl,
                alert=True
            )
        elif new_password_1st_entry.get() != new_password_2nd_entry.get():
            differnt_values_title = language_text("Različite vrednosi",
                                                  "Different values")
            differnt_values_message = language_text(
                "Unosi za novu lozinku se razlikuju.",
                "The entries for the new password are different."
            )
            Messagebox.show_info(
                title=differnt_values_title,
                message=differnt_values_message,
                parent=member_pass_tl,
                alert=True
            )
        else:
            new_password = new_password_1st_entry.get()
            
            try:
                members.new_password(new_password, logged_in_member_code)
            except:
                error_title = language_text("Greška", "Error")
                error_message = language_text(
                    "Došlo je do greške prilikom menjanja lozinke.",
                    "An error occurred while changing the password.")
                Messagebox.show_error(
                    title=error_title,
                    message=error_message,
                    parent=member_pass_tl,
                    alert=True
                )
            else:
                success_title = language_text("Uspešna izmena lozinke",
                                             "Password change successful")
                success_message = language_text(
                    "Uspešno ste izmenili lozinku.",
                    "You have successfully changed your password."
                )
                
                Messagebox.show_info(
                    title=success_title,
                    message=success_message,
                    parent=member_pass_tl,
                    alert=True
                )
    
    member_pass_change_text = language_text("Promena lozinke",
                                            "Password Change")
    member_pass_tl = ttk.Toplevel(title=member_pass_change_text)
    member_pass_tl.attributes("-topmost", "true")
    member_pass_tl.resizable(False, False)
    member_pass_tl.geometry("500x450")
    member_pass_tl.grab_set()
    
    # Title
    pass_change_title_lbl = ttk.Label(
        member_pass_tl,
        text=member_pass_change_text.upper(),
        font=("Calibri", 24, "bold"),
        bootstyle="warning"
    )
    pass_change_title_lbl.pack(padx=30, pady=15)
    
    # Entries and their labels
    old_password_text = language_text("Unesite trenutnu lozinku:",
                                      "Enter your current password:")
    old_password_lbl = ttk.Label(
        member_pass_tl,
        text=old_password_text,
        font=("Calibri", 14),
        bootstyle="light"
    )
    old_password_lbl.pack(fill="x", padx=40, pady=(15, 0))
    
    old_password_entry = ttk.Entry(
        member_pass_tl,
        font=("Calibri", 14),
        show="*",
        bootstyle="warning"
    )
    old_password_entry.pack(fill="x", padx=40, pady=(0, 10))
    old_password_entry.focus()
    
    new_password_1st_text = language_text("Unesite novu lozinku:",
                                          "Enter a new password:")
    new_password_1st_lbl = ttk.Label(
        member_pass_tl,
        text=new_password_1st_text,
        font=("Calibri", 14),
        bootstyle="light"
    )
    new_password_1st_lbl.pack(fill="x", padx=40, pady=(10, 0))
    
    new_password_1st_entry = ttk.Entry(
        member_pass_tl,
        font=("Calibri", 14),
        bootstyle="warning"
    )
    new_password_1st_entry.pack(fill="x", padx=40, pady=(0, 10))

    new_password_2nd_text = language_text("Ponovite novu lozinku:",
                                          "Repeat the new password:")
    new_password_2nd_lbl = ttk.Label(
        member_pass_tl,
        text=new_password_2nd_text,
        font=("Calibri", 14),
        bootstyle="light"
    )
    new_password_2nd_lbl.pack(fill="x", padx=40, pady=(10, 0))

    new_password_2nd_entry = ttk.Entry(
        member_pass_tl,
        font=("Calibri", 14),
        bootstyle="warning"
    )
    new_password_2nd_entry.pack(fill="x", padx=40, pady=(0, 10))
    
    # Buttons
    pass_close_btn_text = language_text("Zatvori", "Close")
    pass_close_btn = ttk.Button(
        member_pass_tl,
        text=pass_close_btn_text,
        width=10,
        style="big.dark.TButton",
        command=member_pass_tl.destroy
    )
    pass_close_btn.pack(padx=(15, 40), pady=30, side="right")

    pass_apply_btn_text = language_text("Primeni", "Apply")
    pass_apply_btn = ttk.Button(
        member_pass_tl,
        text=pass_apply_btn_text,
        width=10,
        style="big.dark.TButton",
        command=change_password_apply
    )
    pass_apply_btn.pack(padx=15, pady=30, side="right")


def librarian_login():
    """Access to the librarian section."""

    def lib_apply_login():
        """Actions when the 'Apply' ('Primeni') button is pressed."""
        global librarian_status
        global logged_in_librarian_code

        # Texts for messageboxes
        lib_title_text = language_text("Nedostaje unos", "Missing entry")
        lib_message_id_text = language_text("Niste uneli svoj ID!",
                                            "You have not entered your ID!")
        lib_message_password_text = language_text(
            "Niste uneli svoju lozinku!",
            "You have not entered your password!"
        )
        lib_invalid_id_title_text = language_text("Pogrešan ID", "Invalid ID")
        lib_invalid_id_msg_text = language_text(
            "ID koji ste uneli ne postoji u bazi podataka.",
            "The ID you entered does not exist in the database."
        )
        lib_invalid_pass_title_text = language_text("Pogrešna lozinka",
                                                    "Invalid password")
        lib_invalid_pass_msg_text = language_text(
            "Niste uneli ispravnu lozinku.",
            "You have not entered the correct password."
        )
        
        # All librarian IDs
        librarian_ids = librarians.librarians_df.personal_id.to_list()
        
        # Checking if the entry fields are filled and the data is valid
        if not lib_id_entry.get():
            Messagebox.show_info(
                title=lib_title_text,
                message=lib_message_id_text,
                parent=librarian_login_tl,
                alert=True
            )
        elif not lib_password_entry.get():
            Messagebox.show_info(
                title=lib_title_text,
                message=lib_message_password_text,
                parent=librarian_login_tl,
                alert=True
            )
        elif lib_id_entry.get() not in librarian_ids:
            Messagebox.show_info(
                title=lib_invalid_id_title_text,
                message=lib_invalid_id_msg_text,
                parent=librarian_login_tl,
                alert=True
            )
        elif lib_password_entry.get() != librarians.librarians_df.password[
            librarians.librarians_df.personal_id ==
            lib_id_entry.get()].to_string(index=False):
            Messagebox.show_info(
                title=lib_invalid_pass_title_text,
                message=lib_invalid_pass_msg_text,
                parent=librarian_login_tl,
                alert=True
            )
        else:
            logged_in_librarian_code = lib_id_entry.get()
            
            librarian_status = "active"
            ui_create()
            librarian_login_tl.destroy()
    
    def lib_logout():
        """Librarian logout."""
        global librarian_status
        global logged_in_librarian_code

        librarian_status = "inactive"
        ui_create()
        librarian_logout_tl.destroy()
    
    
    if librarian_status == "inactive":
        librarian_login_title = language_text("Prijavljivanje bibliotekara",
                                              "Librarian login")
        
        librarian_login_tl = ttk.Toplevel(title=librarian_login_title)
        librarian_login_tl.attributes("-topmost", "true")
        librarian_login_tl.resizable(False, False)
        librarian_login_tl.geometry("500x350")
        librarian_login_tl.grab_set()
        
        # Title
        lib_title_lbl = ttk.Label(
            librarian_login_tl,
            text=librarian_login_title.upper(),
            font=("Calibri", 24, "bold"),
            bootstyle="warning"
        )
        lib_title_lbl.pack(padx=30, pady=15)
    
        # Login labels and entries.
        lib_id_text = language_text("Unesite vaš ID:", "Enter your ID:")
        lib_id_lbl = ttk.Label(
            librarian_login_tl,
            text=lib_id_text,
            font=("Calibri", 14),
            bootstyle="light"
        )
        lib_id_lbl.pack(fill="x", padx=40, pady=(15, 0))
    
        lib_id_reg = librarian_login_tl.register(
            lambda inp: len_digit_limit(inp, length=4))
        lib_id_entry = ttk.Entry(
            librarian_login_tl,
            font=("Calibri", 14),
            validate="key",
            validatecommand=(lib_id_reg, "%P")
        )
        lib_id_entry.pack(fill="x", padx=40, pady=(0, 20))
        lib_id_entry.focus()
    
        lib_password_text = language_text("Unesite vašu lozinku:",
                                          "Enter your password:")
        lib_password_lbl = ttk.Label(
            librarian_login_tl,
            text=lib_password_text,
            font=("Calibri", 14),
            bootstyle="light"
        )
        lib_password_lbl.pack(fill="x", padx=40)
    
        lib_password_entry = ttk.Entry(
            librarian_login_tl,
            font=("Calibri", 14),
            show="*"
        )
        lib_password_entry.pack(fill="x", padx=40, pady=(0, 20))
    
        # Buttons and frame for them
        lib_buttons_frm = ttk.Frame(librarian_login_tl)
        lib_buttons_frm.pack(expand=True, fill="x", padx=40, pady=(10, 30))
    
        lib_cancel_text = language_text("Otkaži", "Cancel")
        lib_cancel_btn = ttk.Button(
            lib_buttons_frm,
            width=10,
            text=lib_cancel_text,
            style="big.dark.TButton",
            command=librarian_login_tl.destroy
        )
        lib_cancel_btn.pack(side="right")
    
        lib_apply_text = language_text("Primeni", "Apply")
        lib_apply_btn = ttk.Button(
            lib_buttons_frm,
            width=10,
            text=lib_apply_text,
            style="big.dark.TButton",
            command=lib_apply_login
        )
        lib_apply_btn.pack(padx=30, side="right")
        
        # Binding 'Return' and 'Esc' keystrokes to buttons
        librarian_login_tl.bind("<Return>",
                                (lambda event: lib_apply_btn.invoke()))
        librarian_login_tl.bind("<Key-Escape>",
                                (lambda event: lib_cancel_btn.invoke()))
    else:
        librarian_logout_title = language_text("Odjavljivanje bibliotekara",
                                               "Librarian logout")
        librarian_logout_tl = ttk.Toplevel(title=librarian_logout_title)
        librarian_logout_tl.attributes("-topmost", "true")
        librarian_logout_tl.resizable(False, False)
        librarian_logout_tl.geometry("500x300")
        librarian_logout_tl.grab_set()

        # Logged in librarian
        librarian_logged_in = logged_in_librarian()
        lib_logged_in_text = language_text(
            f"Bibliotekar: {librarian_logged_in}",
            f"Librarian: {librarian_logged_in}"
        )
        lib_logged_in_lbl = ttk.Label(
            librarian_logout_tl,
            text=lib_logged_in_text,
            font=("Calibri", 16),
            bootstyle="danger"
        )
        lib_logged_in_lbl.pack(padx=20, pady=10)

        # Title
        lib_logout_title_lbl = ttk.Label(
            librarian_logout_tl,
            text=librarian_logout_title.upper(),
            font=("Calibri", 24, "bold"),
            bootstyle="warning")
        lib_logout_title_lbl.pack(padx=30, pady=15)

        # Buttons
        lib_logout_apply_text = language_text("Odjavite se", "Log out")
        lib_logout_apply_btn = ttk.Button(
            librarian_logout_tl,
            width=20,
            text=lib_logout_apply_text.upper(),
            style="huge.primary.TButton",
            command=lib_logout
        )
        lib_logout_apply_btn.pack(pady=10)
        
        lib_logout_cancel_text = language_text("Otkaži", "Cancel")
        lib_logout_cancel_btn = ttk.Button(
            librarian_logout_tl,
            width=10,
            text=lib_logout_cancel_text,
            style="big.dark.TButton",
            command=librarian_logout_tl.destroy
        )
        lib_logout_cancel_btn.pack(side="right", padx=30, pady=10)


def inventory():
    """Inventory review of all books or by availability status."""
    
    def availability_selected(event):
        """Changes occur when the availability combobox is selected."""

        inventory_titles_combo.set("")
        
        all_books = language_text("Sve knjige", "All books")
        available_books = language_text("Dostupne knjige", "Available books")
        rented_books = language_text("Iznajmljene knjige", "Rented books")
        
        for item in inventory_treeview.get_children():
            inventory_treeview.delete(item)
        
        if inventory_availability_combo.get() == all_books:
            code_sort_all_df = books.books_df.sort_values(by=["book_code"])
            
            codes_lst = code_sort_all_df.book_code.to_list()
            books_lst = code_sort_all_df.title.to_list()
            availability_lst = code_sort_all_df.availability.to_list()
            
        elif inventory_availability_combo.get() == available_books:
            code_sort_available_df = books.books_df[
                books.books_df.availability == "Available"
            ].sort_values(by=["book_code"])

            codes_lst = code_sort_available_df.book_code.to_list()
            books_lst = code_sort_available_df.title.to_list()
            availability_lst = code_sort_available_df.availability.to_list()
        
        elif inventory_availability_combo.get() == rented_books:
            code_sort_rented_df = books.books_df[
                books.books_df.availability == "Rented"
            ].sort_values(by=["book_code"])
    
            codes_lst = code_sort_rented_df.book_code.to_list()
            books_lst = code_sort_rented_df.title.to_list()
            availability_lst = code_sort_rented_df.availability.to_list()
        
        else:
            code_sort_reserved_df = books.books_df[
                books.books_df.availability == "Reserved"].sort_values(
                by=["book_code"])
    
            codes_lst = code_sort_reserved_df.book_code.to_list()
            books_lst = code_sort_reserved_df.title.to_list()
            availability_lst = code_sort_reserved_df.availability.to_list()
        
        for i in range(len(codes_lst)):
            inventory_treeview.insert(
                parent="",
                index=i,
                values=(codes_lst[i], books_lst[i], availability_lst[i])
            )
        inventory_treeview.update()

    def title_selected(event):
        """Changes occur when the title combobox is selected."""
        
        inventory_availability_combo.set("")

        for item in inventory_treeview.get_children():
            inventory_treeview.delete(item)

        for title in title_values:
            if inventory_titles_combo.get() == title:
                selected_title_df = books.books_df[
                    books.books_df.title == title
                ].sort_values(by=["book_code"])

                codes_lst = selected_title_df.book_code.to_list()
                books_lst = selected_title_df.title.to_list()
                availability_lst = selected_title_df.availability.to_list()
        
        for i in range(len(codes_lst)):
            inventory_treeview.insert(
                parent="",
                index=i,
                values=(codes_lst[i], books_lst[i], availability_lst[i])
            )
        inventory_treeview.update()
    
    def delay_list():
        """List of book return delays."""
        
        # Data needed
        rented_books_df = renting.renting_df[
            renting.renting_df.return_date.isnull()]
        book_codes_list = rented_books_df.book_code.to_list()
        mem_ids_list = rented_books_df.membership_id.to_list()
        rental_dates_list = rented_books_df.rental_date.to_list()
        
        book_titles_list = []
        for code in book_codes_list:
            book_title = books.books_df.title[
                books.books_df.book_code == code].to_string(index=False)
            book_titles_list.append(book_title)
        
        deadline_exceeding_list = []
        for i in range(len(rental_dates_list)):
            days_exceeded = (date.today() - rental_dates_list[i]) - timedelta(
                days=15)
            days_exceeded_int = int(days_exceeded / timedelta(days=1))
            if days_exceeded_int > 0:
                deadline_exceeding_list.append(
                    [book_codes_list[i], book_titles_list[i],
                     mem_ids_list[i], days_exceeded_int])
        
        delay_tl_title = language_text("Kašnjenje s vraćanjem",
                                       "Delay in return")
        delay_tl = ttk.Toplevel(title=delay_tl_title)
        delay_tl.attributes("-topmost", "true")
        delay_tl.resizable(False, False)
        delay_tl.geometry("1000x500")
        delay_tl.grab_set()
        
        # Title
        delay_main_title_text = language_text("KAŠNJENJE S VRAĆANJEM KNJIGA",
                                              "DELAY IN RETURNING BOOKS")
        delay_main_title_lbl = ttk.Label(
            delay_tl,
            text=delay_main_title_text,
            font=("Calibri", 24, "bold"),
            anchor="center",
            bootstyle="warning"
        )
        delay_main_title_lbl.pack(fill="x", padx=30, pady=20)
        
        # Data frame
        delay_scrolled_frm = ScrolledFrame(delay_tl, autohide=True)
        delay_scrolled_frm.pack(expand=True, fill="both")
        
        # In ttk bootstrap it is necessary to create a frame inside a
        # scrolledframe, because the command 'grid_columnconfigure' for
        # scrolledframe does not work.
        delay_data_frm = ttk.Frame(delay_scrolled_frm)
        delay_data_frm.pack(expand=True, fill="both")
        
        if len(deadline_exceeding_list) > 0:
            delay_data_frm.grid_columnconfigure((0, 1, 2, 3), weight=1)
            
            delay_code_lbl_text = language_text("Šifra knjige:", "Book code:")
            delay_code_lbl = ttk.Label(
                delay_data_frm,
                text=delay_code_lbl_text,
                font=("Calibri", 16),
                bootstyle="light"
            )
            delay_code_lbl.grid(column=0, row=0, padx=(50, 20), pady=(20, 5))
            
            delay_title_lbl_text = language_text("Naslov knjige:",
                                                 "Book title:")
            delay_title_lbl = ttk.Label(
                delay_data_frm,
                text=delay_title_lbl_text,
                font=("Calibri", 16),
                bootstyle="light"
            )
            delay_title_lbl.grid(column=1, row=0, padx=20, pady=(20, 5))
    
            delay_id_lbl_text = language_text("Broj članske karte:",
                                              "Membership ID:")
            delay_id_lbl = ttk.Label(
                delay_data_frm,
                text=delay_id_lbl_text,
                font=("Calibri", 16),
                bootstyle="light"
            )
            delay_id_lbl.grid(column=2, row=0, padx=20, pady=(20, 5))
    
            delay_days_lbl_text = language_text("Prekoračeno dana:",
                                                "Days exceeded:")
            delay_days_lbl = ttk.Label(
                delay_data_frm,
                text=delay_days_lbl_text,
                font=("Calibri", 16),
                bootstyle="light"
            )
            delay_days_lbl.grid(column=3, row=0, padx=(20, 50), pady=(20, 5))
            
            for i in range(len(book_codes_list)):
                ttk.Label(
                    delay_data_frm,
                    text=deadline_exceeding_list[i][0],
                    font=("Calibri", 14)
                ).grid(column=0, row=(i+1), padx=(50, 20), pady=(0, 5))
                
                ttk.Label(
                    delay_data_frm,
                    text=deadline_exceeding_list[i][1],
                    font=("Calibri", 14)
                ).grid(column=1, row=(i+1), padx=20, pady=(0, 5), sticky="w")
                
                ttk.Label(
                    delay_data_frm,
                    text=deadline_exceeding_list[i][2],
                    font=("Calibri", 14)
                ).grid(column=2, row=(i+1), padx=20, pady=(0, 5))
                
                ttk.Label(
                    delay_data_frm,
                    text=deadline_exceeding_list[i][3],
                    font=("Calibri", 14)
                ).grid(column=3, row=(i+1), padx=(20, 50), pady=(0, 5))
        else:
            not_exceeded_text = language_text(
                "Nema prekoračenja roka za vraćanje iznajmljenih knjiga.",
                "There is no exceeded deadline for returning rented books."
            )
            ttk.Label(
                delay_data_frm,
                text=not_exceeded_text,
                font=("Calibri", 20, "bold"),
                anchor="center",
                bootstyle="info"
            ).pack(fill="x", padx=50, pady=50)
        
        # Close button
        delay_close_btn = ttk.Button(
            delay_tl,
            text=inventory_close_btn_text,
            width=10,
            style="big.dark.TButton",
            command=delay_tl.destroy
        )
        delay_close_btn.pack(side="right", padx=50, pady=20)
    
    def availability_chart():
        """Chart of books availability."""
        
        # Data needed
        books_available = books.books_df[
            books.books_df.availability == "Available"]["title"].count()
        books_rented = books.books_df[
            books.books_df.availability == "Rented"]["title"].count()
        books_reserved = books.books_df[
            books.books_df.availability == "Reserved"]["title"].count()
        
        available_text = language_text("Dostupno", "Available")
        rented_text = language_text("Iznajmljeno", "Rented")
        reserved_text = language_text("Rezervisano", "Reserved")
        
        title_text = language_text("Procentualni prikaz dostupnosti knjiga",
                                   "Percentage review of book availability")
        
        plt.figure(figsize=(8, 8))

        plt.pie(
            [books_available, books_rented, books_reserved],
            labels=[available_text, rented_text, reserved_text],
            autopct="%.1f%%",
            colors=["tomato", "cornflowerblue", "yellowgreen"]
        )
        plt.title(
            label=title_text.upper(),
            fontdict={"family": "Calibri", "color": "darkgoldenrod",
                      "size": 22, "weight": "bold"},
            pad=20
        )
        
        plt.show()
    
    
    inventory_tl_title = language_text("Inventar", "Inventory")
    inventory_tl = ttk.Toplevel(title=inventory_tl_title)
    inventory_tl.resizable(False, False)
    inventory_tl.geometry("1100x950")
    inventory_tl.grab_set()
    
    # Frames
    inventory_top_frm = ttk.Frame(inventory_tl)
    inventory_top_frm.pack(fill="x", padx=20, pady=20)
    
    inventory_filters_text = language_text(" Filteri ", " Filters ")
    inventory_filters_lf = ttk.LabelFrame(
        inventory_tl,
        text=inventory_filters_text,
        bootstyle="warning"
    )
    inventory_filters_lf.pack(fill="x", padx=20, pady=20)
    
    inventory_tree_frm = ttk.Frame(inventory_tl)
    inventory_tree_frm.pack(fill="x", padx=20)
    
    # Widgets in top (title) frame
    inventory_main_text = language_text(" Biblioteka \"Vuk Karadžić\"",
                                        " Library \"Vuk Karadžić\"")
    inventory_main_lbl = ttk.Label(
        inventory_top_frm,
        text=inventory_main_text,
        font=("Calibri", 36, "bold"),
        image=logo_smaller,
        compound="left",
        anchor="center",
        bootstyle="warning"
    )
    inventory_main_lbl.pack(expand=True, fill="x")
    
    librarian = logged_in_librarian()
    inventory_librarian_text = language_text(f"Bibliotekar: {librarian}",
                                             f"Librarian: {librarian}")
    inventory_librarian_lbl = ttk.Label(
        inventory_top_frm,
        text=inventory_librarian_text,
        font=("Calibri", 16),
        bootstyle="danger"
    )
    inventory_librarian_lbl.pack(pady=10)
    
    inventory_title_lbl = ttk.Label(
        inventory_top_frm,
        text=inventory_tl_title.upper(),
        font=("Calibri", 28, "bold"),
        anchor="center",
        bootstyle="warning"
    )
    inventory_title_lbl.pack(expand=True, fill="x", pady=(0, 10))
    
    # Widgets in 'Filters' frame
    inventory_availability_text = language_text("Knjige po dostupnosti",
                                                "Books by availability")
    inventory_availability_lbl = ttk.Label(
        inventory_filters_lf,
        text=inventory_availability_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    inventory_availability_lbl.grid(column=0, row=0, padx=50, pady=(10, 0),
                                    sticky="w")
    
    if language == "srpski":
        availability_values = ["Sve knjige", "Dostupne knjige",
                               "Iznajmljene knjige", "Rezervisane knjige"]
    else:
        availability_values = ["All books", "Available books", "Rented books",
                               "Reserved books"]
    availability_combo_default = language_text("Sve knjige", "All books")

    inventory_availability_combo = ttk.Combobox(
        inventory_filters_lf,
        width=40,
        font=("Calibri", 14),
        values=availability_values,
        state="readonly",
        bootstyle="light"
    )
    inventory_availability_combo.grid(column=0, row=1, padx=50, pady=(0, 30),
                                      sticky="w")
    inventory_availability_combo.set(availability_combo_default)

    # Bind combobox
    inventory_availability_combo.bind("<<ComboboxSelected>>",
                                      availability_selected)
    
    inventory_titles_text = language_text("Knjige po naslovu",
                                          "Books by title")
    inventory_titles_lbl = ttk.Label(
        inventory_filters_lf,
        text=inventory_titles_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    inventory_titles_lbl.grid(column=1, row=0, padx=50, pady=(10, 0),
                              sticky="w")

    title_list = titles.titles_df.title.to_list()
    title_values = sorted(title_list)
    inventory_titles_combo = ttk.Combobox(
        inventory_filters_lf,
        width=40,
        font=("Calibri", 14),
        values=title_values,
        state="readonly",
        bootstyle="light"
    )
    inventory_titles_combo.grid(column=1, row=1, padx=50, pady=(0, 30),
                                sticky="w")

    # Bind combobox
    inventory_titles_combo.bind("<<ComboboxSelected>>", title_selected)
    
    # Treeview
    code_text = language_text("Šifra", "Code")
    book_text = language_text("Knjiga", "Book")
    availability_text = language_text("Dostupnost", "Availability")
    columns = ["code", "book", "availability"]
    
    tree_style.configure("Treeview.Heading", font=("Calibri", 16))
    
    inventory_treeview = ttk.Treeview(
        inventory_tree_frm,
        columns=columns,
        show="headings",
        height=15,
        style="tree.warning.Treeview"
    )
    inventory_treeview.heading("code", text=code_text)
    inventory_treeview.heading("book", text=book_text)
    inventory_treeview.heading("availability", text=availability_text)
    
    inventory_treeview.column("code", width=14, anchor="center")
    inventory_treeview.column("book", width=45, anchor="w")
    inventory_treeview.column("availability", width=13, anchor="center")
    
    inventory_treeview.pack(expand=True, fill="both", side="left")
    
    # Treeview scroll
    tree_scroll = ttk.Scrollbar(
        inventory_tree_frm,
        orient="vertical",
        command=inventory_treeview.yview
    )
    tree_scroll.bind("<MouseWheel>",
        lambda event: inventory_treeview.yview_scroll(-int(event.delta / 60),
                                                      "units"))
    inventory_treeview.configure(yscrollcommand=tree_scroll.set,
                                 selectmode="browse")
    tree_scroll.pack(side="right", fill="y")
    
    # Default treeview data
    code_sort_books_df = books.books_df.sort_values(by=["book_code"])
    codes_list = code_sort_books_df.book_code.to_list()
    books_list = code_sort_books_df.title.to_list()
    availability_list = code_sort_books_df.availability.to_list()
    
    for i in range(len(codes_list)):
        inventory_treeview.insert(
            parent="",
            index=i,
            values = (codes_list[i], books_list[i], availability_list[i])
        )
    
    # Buttons
    inventory_close_btn_text = language_text("Zatvori", "Close")
    inventory_close_btn = ttk.Button(
        inventory_tl,
        width=10,
        text=inventory_close_btn_text,
        style="big.dark.TButton",
        command=inventory_tl.destroy
    )
    inventory_close_btn.pack(side="right", padx=(20, 50), pady=20)

    inventory_availability_btn_text = language_text("Dostupnost",
                                                    "Availability")
    inventory_availability_btn = ttk.Button(
        inventory_tl,
        width=10,
        text=inventory_availability_btn_text,
        style="big.dark.TButton",
        command=availability_chart
    )
    inventory_availability_btn.pack(side="right", padx=20, pady=20)

    inventory_delay_btn_text = language_text("Kašnjenje", "Delay")
    inventory_delay_btn = ttk.Button(
        inventory_tl,
        width=10,
        text=inventory_delay_btn_text,
        style="big.dark.TButton",
        command=delay_list
    )
    inventory_delay_btn.pack(side="right", padx=20, pady=20)


def adding_books():
    """Adding books to the library."""

    def choose_old_new():
        """Adding widgets to the frame with the required data."""
    
        if add_choice_var.get() == "1":
            # Generating a new book code
            book_code = unique_code_generating(
                books.books_df.book_code.to_list(), 10)

            add_book_title_combo.set("")
            add_book_title_combo.configure(state="readonly")
            
            add_book_code_val.configure(text=book_code)
            
            add_author_combo.set("")
            add_author_combo.configure(state="disabled")
            
            add_genre_combo.set("")
            add_genre_combo.configure(state="disabled")
            
            add_year_entry.delete(0, END)
            add_year_entry.configure(state="readonly")
        else:
            # Generating a new book code
            book_code = unique_code_generating(
                books.books_df.book_code.to_list(), 10)

            add_book_title_combo.set("")
            add_book_title_combo.configure(state="normal")

            add_book_code_val.configure(text=book_code)

            add_author_combo.set("")
            add_author_combo.configure(state="normal")

            add_genre_combo.set("")
            add_genre_combo.configure(state="readonly")

            add_year_entry.configure(state="normal")
            add_year_entry.delete(0, END)
    
    def title_selected(event):
        """Changes that occur when a title is selected."""
        selected_title = add_book_title_combo.get()
        author = titles.titles_df.author[
            titles.titles_df.title == selected_title].to_string(index=False)
        publication_year = titles.titles_df.publication_year[
            titles.titles_df.title == selected_title].to_string(index=False)
        genre_eng = titles.titles_df.genre[
            titles.titles_df.title == selected_title].to_string(index=False)
        
        if language == "srpski":
            for i in range(len(GENRES)):
                if GENRES[i][1] == genre_eng:
                    genre = GENRES[i][0]
        else:
            genre = genre_eng
    
    
        add_author_combo.set(author)
        add_genre_combo.set(genre)
        if add_choice_var.get() == "1":
            add_year_entry.configure(state="normal")
            add_year_entry.delete(0, END)
            add_year_entry.insert(0, publication_year)
            add_year_entry.configure(state="readonly")
        else:
            add_year_entry.delete(0, END)
            add_year_entry.insert(0, publication_year)
    
    def adding_apply():
        """Events that take place when the 'Apply' ('Primeni') button is
        pressed."""
        existing_titles = titles.titles_df.title.to_list()

        # Texts for messageboxes
        missing_entry = language_text("Nedostaje unos", "Missing entry")
        missing_title_text = language_text(
            "Niste uneli naslov knjige!",
            "You have not entered a book title!"
        )
        missing_author_text = language_text(
            "Niste uneli ime autora!",
            "You have not entered the author's name!"
        )
        missing_genre_text = language_text("Niste uneli žanr!",
                                           "You have not entered the genre!")
        missing_year_text = language_text(
            "Niste uneli godinju izdanja!",
            "You have not entered the year of publication!"
        )
        
        if not add_book_title_combo.get():
            Messagebox.show_info(
                title=missing_entry,
                message=missing_title_text,
                parent=add_tl,
                alert=True
            )
        elif not add_author_combo.get():
            Messagebox.show_info(
                title=missing_entry,
                message=missing_author_text,
                parent=add_tl,
                alert=True
            )
        elif not add_genre_combo.get():
            Messagebox.show_info(
                title=missing_entry,
                message=missing_genre_text,
                parent=add_tl,
                alert=True
            )
        elif not add_year_entry.get():
            Messagebox.show_info(
                title=missing_entry,
                message=missing_year_text,
                parent=add_tl,
                alert=True
            )
        else:
            # Inserting data into the 'books' table
            books.adding_new_copy(add_book_code_val, add_book_title_combo)
            
            if add_book_title_combo.get() not in existing_titles:
                # Inserting data into the 'titles' table
                title_to_add = add_book_title_combo.get()
                author_to_add = add_author_combo.get()
                year_to_add = add_year_entry.get()
                genre_get = add_genre_combo.get()
                
                if language == "srpski":
                    for i in range(len(GENRES)):
                        if GENRES[i][0] == genre_get:
                            genre_to_add = GENRES[i][1]
                else:
                    genre_to_add = genre_get
                
                titles.adding_new_title(title_to_add, author_to_add,
                                        genre_to_add, year_to_add)
                
                # New lists for combobox values
                values_of_title = sorted(titles.titles_df.title.to_list())
                values_of_author = sorted(list(set(
                    titles.titles_df.author.to_list())))
                if language == "srpski":
                    values_of_genre = creating_values_list(GENRES)[0]
                else:
                    values_of_genre = creating_values_list(GENRES)[1]
                
                # Add new lists to combobox values
                add_book_title_combo.configure(values=values_of_title)
                add_author_combo.configure(values=values_of_author)
                add_genre_combo.configure(values=values_of_genre)
                
            # Resetting old data
            add_book_title_combo.set("")
            add_author_combo.set("")
            add_genre_combo.set("")
            if add_choice_var.get() == "1":
                add_year_entry.configure(state="normal")
                add_year_entry.delete(0, END)
                add_year_entry.configure(state="readonly")
            else:
                add_year_entry.delete(0, END)

            # Getting a new book code with an updated list of codes
            new_codes_list = books.books_df.book_code.to_list()
            new_book_code_value = unique_code_generating(new_codes_list, 10)
            add_book_code_val.configure(text=new_book_code_value)
            
            add_success_title_text = language_text("Uspešno dodavanje knjige",
                                                   "Book added successfully")
            add_success_message_text = language_text(
                "Podaci o novoj knjizi uspešno dodati u bazu podataka.",
                "New book data successfully added to the database."
            )
            Messagebox.show_info(
                title=add_success_title_text,
                message=add_success_message_text,
                parent=add_tl,
                alert=True
            )

    
    add_tl_title = language_text("Dodavanje knjiga", "Adding books")
    add_tl = ttk.Toplevel(title=add_tl_title)
    add_tl.attributes("-topmost", "true")
    add_tl.resizable(False, False)
    add_tl.geometry("800x850")
    add_tl.grab_set()
    
    # Frames
    add_top_frm = ttk.Frame(add_tl)
    add_top_frm.pack(fill="x", padx=20, pady=20)
    
    add_choice_lf_text = language_text(" Postojeći ili novi naslov ",
                                        " Existing or new title ")
    add_choice_lf = ttk.LabelFrame(
        add_tl,
        text=add_choice_lf_text,
        style="warning"
    )
    add_choice_lf.pack(fill="x", padx=20, pady=20)

    add_data_lf_text = language_text(" Podaci ", " Data ")
    add_data_lf = ttk.LabelFrame(
        add_tl,
        text=add_data_lf_text,
        style="warning"
    )
    add_data_lf.pack(fill="x", padx=20, pady=20)
    
    # Top frame widgets
    add_main_text = language_text(" Biblioteka \"Vuk Karadžić\"",
                                  " Library \"Vuk Karadžić\"")
    add_main_lbl = ttk.Label(
        add_top_frm,
        text=add_main_text,
        font=("Calibri", 36, "bold"),
        image=logo_smaller,
        compound="left",
        anchor="center",
        bootstyle="warning"
    )
    add_main_lbl.pack(expand=True, fill="x")

    librarian = logged_in_librarian()
    add_librarian_text = language_text(f"Bibliotekar: {librarian}",
                                       f"Librarian: {librarian}")
    add_librarian_lbl = ttk.Label(
        add_top_frm,
        text=add_librarian_text,
        font=("Calibri", 16),
        bootstyle="danger"
    )
    add_librarian_lbl.pack(pady=10)

    add_title_lbl = ttk.Label(
        add_top_frm,
        text=add_tl_title.upper(),
        font=("Calibri", 28, "bold"),
        anchor="center",
        bootstyle="warning"
    )
    add_title_lbl.pack(expand=True, fill="x", pady=(0, 10))
    
    # Choice frame widget
    radiobutton_text_1 = language_text("Postojeći naslov", "Existing title")
    radiobutton_text_2 = language_text("Novi naslov", "New title")
    
    choice_radiobuttons = {radiobutton_text_1: "1", radiobutton_text_2: "2"}
    add_choice_var = ttk.StringVar(add_choice_lf)
    
    for (radio_text, radio_value) in choice_radiobuttons.items():
        ttk.Radiobutton(
            add_choice_lf,
            text=radio_text,
            variable=add_choice_var,
            value=radio_value,
            style="warning.TRadiobutton",
            command=choose_old_new
        ).pack(anchor="nw", padx=50, pady=5)
    add_choice_var.set("1")
    
    # Data frame widgets
    add_data_lf.grid_columnconfigure((0, 1), weight=1)
    
    add_book_title_lbl_text = language_text("Naslov knjige:", "Book title:")
    add_book_title_lbl = ttk.Label(
        add_data_lf,
        text=add_book_title_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    add_book_title_lbl.grid(column=0, row=0, padx=(50, 20), pady=(20, 0),
                            sticky="w")
    
    title_values = sorted(titles.titles_df.title.to_list())
    add_book_title_combo = ttk.Combobox(
        add_data_lf,
        width=42,
        values=title_values,
        font=("Calibri", 14),
        state="readonly",
        bootstyle="light"
    )
    add_book_title_combo.grid(column=0, row=1, padx=(50, 20), pady=(0, 10),
                              sticky="w")
    # Bind this Combobox
    add_book_title_combo.bind("<<ComboboxSelected>>", title_selected)

    add_book_code_lbl_text = language_text("Šifra knjige:", "Book code:")
    add_book_code_lbl = ttk.Label(
        add_data_lf,
        text=add_book_code_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    add_book_code_lbl.grid(column=1, row=0, padx=(20, 50), pady=(20, 0),
                           sticky="w")

    book_codes = books.books_df.book_code.to_list()
    book_code_value = unique_code_generating(book_codes, 10)
    add_book_code_val = ttk.Label(
        add_data_lf,
        text=book_code_value,
        width=16,
        font=("Calibri", 16),
        state="disabled"
    )
    add_book_code_val.grid(column=1, row=1, padx=(20, 50), pady=(0, 10),
                           sticky="w")

    add_author_lbl_text = language_text("Autor:", "Author:")
    add_author_lbl = ttk.Label(
        add_data_lf,
        text=add_author_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    add_author_lbl.grid(column=0, row=2, padx=(50, 20), pady=(10, 0),
                        sticky="w")
    
    author_values = sorted(list(set(titles.titles_df.author.to_list())))
    add_author_combo = ttk.Combobox(
        add_data_lf,
        width=42,
        values=author_values,
        font=("Calibri", 14),
        state="disabled",
        bootstyle="light"
    )
    add_author_combo.grid(column=0, row=3, padx=(50, 20), pady=(0, 10),
                          sticky="w")
    
    add_genre_lbl_text = language_text("Žanr:", "Genre:")
    add_genre_lbl = ttk.Label(
        add_data_lf,
        text=add_genre_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    add_genre_lbl.grid(column=1, row=2, padx=(20, 50), pady=(10, 0),
                       sticky="w")
    
    if language == "srpski":
        genre_values = creating_values_list(GENRES)[0]
    else:
        genre_values = creating_values_list(GENRES)[1]
    add_genre_combo = ttk.Combobox(
        add_data_lf,
        width=16,
        values=genre_values,
        font=("Calibri", 14),
        state="disabled",
        bootstyle="light"
    )
    add_genre_combo.grid(column=1, row=3, padx=(20, 50), pady=(0, 10),
                         sticky="w")
    
    add_year_lbl_text = language_text("Godina izdanja:", "Publication year:")
    add_year_lbl = ttk.Label(
        add_data_lf,
        text=add_year_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    add_year_lbl.grid(column=0, row=4, padx=(50, 20), pady=(10, 0), sticky="w")
    
    publication_year_reg = add_data_lf.register(
        lambda inp: len_digit_limit(inp, length=4))
    add_year_entry = ttk.Entry(
        add_data_lf,
        width=16,
        font=("Calibri", 16),
        validate="key",
        validatecommand=(publication_year_reg, "%P"),
        bootstyle="light"
    )
    add_year_entry.grid(column=0, row=5, padx=(50, 20), pady=(0, 20),
                        sticky="w")
    add_year_entry.state(["readonly"])
    
    # Buttons
    add_close_btn_text = language_text("Zatvori", "Close")
    add_close_btn = ttk.Button(
        add_tl,
        width=10,
        text=add_close_btn_text,
        style="big.dark.TButton",
        command=add_tl.destroy
    )
    add_close_btn.pack(side="right", padx=(20, 50), pady=20)
    
    add_apply_btn_text = language_text("Primeni", "Apply")
    add_apply_btn = ttk.Button(
        add_tl,
        width=10,
        text=add_apply_btn_text,
        style="big.dark.TButton",
        command=adding_apply
    )
    add_apply_btn.pack(side="right", padx=20, pady=20)


def books_updating():
    """Updating data for titles and books."""
    
    def title_picked(event):
        """Changes that occur when a title is selected."""
        
        # Current data
        current_author = titles.titles_df.author[
            titles.titles_df.title == books_upd_title_old_title_combo.get()
        ].to_string(index=False)
        
        current_year = titles.titles_df.publication_year[
            titles.titles_df.title == books_upd_title_old_title_combo.get()
        ].to_string(index=False)
        
        current_genre_eng = titles.titles_df.genre[
            titles.titles_df.title == books_upd_title_old_title_combo.get()
        ].to_string(index=False)
        if language == "srpski":
            for i in range(len(GENRES)):
                if current_genre_eng == GENRES[i][1]:
                    current_genre = GENRES[i][0]
        else:
            current_genre = current_genre_eng
        
        # Setting data to labels
        books_upd_title_old_author_val.configure(text=current_author)
        books_upd_title_old_genre_val.configure(text=current_genre)
        books_upd_title_old_year_val.configure(text=current_year)

        # Change state of genre Combobox
        books_upd_title_new_genre_combo.configure(state="readonly")

    def reset_title_updating_frame():
        """Resetting widgets in 'Title updating' frame."""

        books_upd_title_old_title_combo.set("")
        books_upd_title_new_title_entry.delete(0, END)
        books_upd_title_old_author_val.configure(text="-")
        books_upd_title_new_author_entry.delete(0, END)
        books_upd_title_old_genre_val.configure(text="-")
        books_upd_title_new_genre_combo.set("")
        books_upd_title_new_genre_combo.configure(state="disabled")
        books_upd_title_old_year_val.configure(text="-")
        books_upd_title_new_year_entry.delete(0, END)

    def code_picked(event):
        """Changes that occur when a book code is selected."""
        
        # Current data
        current_title = books.books_df.title[
            books.books_df.book_code == books_upd_book_code_combo.get()
        ].to_string(index=False)
        
        current_availability_eng = books.books_df.availability[
            books.books_df.book_code == books_upd_book_code_combo.get()
        ].to_string(index=False)
        if language == "srpski":
            for i in range(len(AVAILABILITY)):
                if current_availability_eng == AVAILABILITY[i][1]:
                    current_availability = AVAILABILITY[i][0]
        else:
            current_availability = current_availability_eng

        # Setting data to labels
        books_upd_book_old_title_val.configure(text=current_title)
        books_upd_book_old_availability_val.configure(
            text=current_availability)
        
        # Change state of availability Combobox
        books_upd_book_new_availability_combo.configure(state="readonly")

    def reset_book_updating_frame():
        """Resetting widgets in 'Book updating' frame."""

        books_upd_book_code_combo.set("")
        books_upd_book_old_title_val.configure(text="-")
        books_upd_book_old_availability_val.configure(text="-")
        books_upd_book_new_title_entry.delete(0, END)
        books_upd_book_new_availability_combo.set("")
        books_upd_book_new_availability_combo.configure(state="disabled")

    def title_update_apply():
        """Entering data into tables and accompanying messages."""
        
        # The title must be changed separately, because if it is changed
        # first, the other values will not change
        title_dict ={
            "author": books_upd_title_new_author_entry.get(),
            "genre": books_upd_title_new_genre_combo.get(),
            "publication_year": books_upd_title_new_year_entry.get()
        }
        
        if not books_upd_title_old_title_combo.get():
            no_title_text = language_text("Nema naslova", "No title")
            no_title_message = language_text(
                "Niste izabrali nijedan naslov.",
                "You have not selected any title."
            )
            Messagebox.show_info(
                title=no_title_text,
                message=no_title_message,
                parent=books_upd_tl,
                alert=True
            )
        elif not books_upd_title_new_title_entry.get() and not \
                books_upd_title_new_author_entry.get() and not \
                books_upd_title_new_genre_combo.get() and not \
                books_upd_title_new_year_entry.get():
            no_value_title_text = language_text("Nema vrednosti", "No value")
            no_value_message_text = language_text(
                "Niste uneli nijednu vrednost za ažariranje.",
                "You have not entered any values to update."
            )
            Messagebox.show_info(
                title=no_value_title_text,
                message=no_value_message_text,
                parent=books_upd_tl,
                alert=True
            )
        else:
            for key, value in title_dict.items():
                if value:
                    if key == "genre" and language == "srpski":
                        for i in range(len(GENRES)):
                            if GENRES[i][0] == value:
                                value_eng = GENRES[i][1]
                        
                        title_sql = f"""
                        UPDATE titles
                        SET {key} = '{value_eng}'
                        WHERE title = '{books_upd_title_old_title_combo.get()}';
                        """
                    else:
                        title_sql = f"""
                        UPDATE titles
                        SET {key} = '{value}'
                        WHERE title = '{books_upd_title_old_title_combo.get()}';
                        """
                    titles.titles_updating(title_sql)
                    
            if books_upd_title_new_title_entry.get():
                only_title_sql = f"""
                UPDATE titles
                SET title = '{books_upd_title_new_title_entry.get()}'
                WHERE title = '{books_upd_title_old_title_combo.get()}';
                """
                titles.titles_updating(only_title_sql)
            
            reset_title_updating_frame()
            
            # Title list is subject to change
            new_title_list = sorted(titles.titles_df.title.to_list())
            books_upd_title_old_title_combo.configure(values=new_title_list)

            successful_update_title = language_text("Uspešno ažuriranje",
                                                    "Successful update")
            successful_update_message = language_text(
                "Ažuriranje uspešno izvršeno", "Update completed successfully")
            Messagebox.show_info(
                title=successful_update_title,
                message=successful_update_message,
                parent=books_upd_tl,
                alert=True)
    
    def book_update_apply():
        """Entering data into table and accompanying messages."""
        book_dict = {
            "title": books_upd_book_new_title_entry.get(),
            "availability": books_upd_book_new_availability_combo.get()
        }
        
        if not books_upd_book_code_combo.get():
            no_book_code_title = language_text("Nema šifre knjige",
                                               "No book code")
            no_book_code_message = language_text(
                "Niste izabrali nijednu šifru knjige.",
                "You have not selected any book code."
            )
            Messagebox.show_info(
                title=no_book_code_title,
                message=no_book_code_message,
                parent=books_upd_tl,
                alert=True
            )
        elif not books_upd_book_new_title_entry.get() and not \
                books_upd_book_new_availability_combo.get():
            no_value_title_text = language_text("Nema vrednosti", "No value")
            no_value_message_text = language_text(
                "Niste uneli nijednu vrednost za ažariranje.",
                "You have not entered any values to update."
            )
            Messagebox.show_info(
                title=no_value_title_text,
                message=no_value_message_text,
                parent=books_upd_tl,
                alert=True
            )
        else:
            for key, value in book_dict.items():
                if value:
                    if key == "availability" and language == "srpski":
                        for i in range(len(AVAILABILITY)):
                            if AVAILABILITY[i][0] == value:
                                value_eng = AVAILABILITY[i][1]

                        books_sql = f"""
                        UPDATE books
                        SET {key} = '{value_eng}'
                        WHERE book_code = '{books_upd_book_code_combo.get()}';
                        """
                    else:
                        books_sql = f"""
                        UPDATE books
                        SET {key} = '{value}'
                        WHERE book_code = '{books_upd_book_code_combo.get()}';
                        """
                    books.updating_books(books_sql)
            
            reset_book_updating_frame()
            
            successful_update_title = language_text("Uspešno ažuriranje",
                                                    "Successful update")
            successful_update_message = language_text(
                "Ažuriranje uspešno izvršeno", "Update completed successfully"
            )
            Messagebox.show_info(
                title=successful_update_title,
                message=successful_update_message,
                parent=books_upd_tl,
                alert=True
            )
    
    
    books_upd_main_title_text = language_text("Ažuriranje knjiga",
                                              "Books update")
    books_upd_tl = ttk.Toplevel(title=books_upd_main_title_text)
    books_upd_tl.attributes("-topmost", "true")
    books_upd_tl.resizable(False, False)
    books_upd_tl.geometry("1000x900")
    books_upd_tl.grab_set()
    
    # Frame for other frames
    books_upd_sf = ScrolledFrame(books_upd_tl, autohide=True)
    books_upd_sf.pack(expand=True, fill="both")
    
    # Frames
    books_upd_top_frm = ttk.Frame(books_upd_sf)
    books_upd_top_frm.pack(fill="x", padx=20, pady=20)
    
    books_upd_title_lf_text = language_text(" Ažuriranje naslova ",
                                             " Title updating ")
    books_upd_title_lf = ttk.LabelFrame(
        books_upd_sf,
        text=books_upd_title_lf_text,
        bootstyle="warning"
    )
    books_upd_title_lf.pack(fill="x", padx=20, pady=20)

    books_upd_book_lf_text = language_text(" Ažuriranje knjige ",
                                             " Book updating ")
    books_upd_book_lf = ttk.LabelFrame(
        books_upd_sf,
        text=books_upd_book_lf_text,
        bootstyle="warning"
    )
    books_upd_book_lf.pack(fill="x", padx=20, pady=20)
    
    # Top frame widgets
    books_upd_main_text = language_text(" Biblioteka \"Vuk Karadžić\"",
                                        " Library \"Vuk Karadžić\"")
    books_upd_main_lbl = ttk.Label(
        books_upd_top_frm,
        text=books_upd_main_text,
        font=("Calibri", 36, "bold"),
        image=logo_smaller,
        compound="left",
        anchor="center",
        bootstyle="warning"
    )
    books_upd_main_lbl.pack(expand=True, fill="x")

    librarian = logged_in_librarian()
    books_upd_librarian_text = language_text(f"Bibliotekar: {librarian}",
                                             f"Librarian: {librarian}")
    books_upd_librarian_lbl = ttk.Label(
        books_upd_top_frm,
        text=books_upd_librarian_text,
        font=("Calibri", 16),
        bootstyle="danger"
    )
    books_upd_librarian_lbl.pack(pady=10)

    books_upd_title_lbl = ttk.Label(
        books_upd_top_frm,
        text=books_upd_main_title_text.upper(),
        font=("Calibri", 28, "bold"),
        anchor="center",
        bootstyle="warning"
    )
    books_upd_title_lbl.pack(expand=True, fill="x", pady=(0, 10))
    
    # Title update frame
    books_upd_title_lf.grid_columnconfigure((0, 1), weight=1)
    
    books_upd_title_old_title_lbl_text = language_text(
        "Naslov - trenutna vrednost:", "Title - current value:")
    books_upd_title_old_title_lbl = ttk.Label(
        books_upd_title_lf,
        text=books_upd_title_old_title_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    books_upd_title_old_title_lbl.grid(column=0, row=0, padx=(40, 20),
                                       pady=(20, 0), sticky="w")
    
    titles_list = sorted(titles.titles_df.title.to_list())
    books_upd_title_old_title_combo = ttk.Combobox(
        books_upd_title_lf,
        width=40,
        values=titles_list,
        font=("Calibri", 14),
        state="readonly",
        bootstyle="light"
    )
    books_upd_title_old_title_combo.grid(column=0, row=1, padx=(40, 20),
                                         pady=(0, 10), sticky="w")

    # Bind this Combobox
    books_upd_title_old_title_combo.bind("<<ComboboxSelected>>", title_picked)
    
    books_upd_title_new_title_lbl_text = language_text(
        "Naslov - nova vrednost:", "Title - new value:")
    books_upd_title_new_title_lbl = ttk.Label(
        books_upd_title_lf,
        text=books_upd_title_new_title_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    books_upd_title_new_title_lbl.grid(column=1, row=0, padx=(20, 40),
                                       pady=(20, 0), sticky="w")

    books_upd_title_new_title_entry = ttk.Entry(
        books_upd_title_lf,
        width=40,
        font=("Calibri", 16),
        bootstyle="light"
    )
    books_upd_title_new_title_entry.grid(column=1, row=1, padx=(20, 40),
                                         pady=(0, 10), sticky="w")
    
    books_upd_title_old_author_lbl_text = language_text(
        "Autor - trenutna vrednost:", "Author - current value:")
    books_upd_title_old_author_lbl = ttk.Label(
        books_upd_title_lf,
        text=books_upd_title_old_author_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    books_upd_title_old_author_lbl.grid(column=0, row=2, padx=(40, 20),
                                        pady=(10, 0), sticky="w")
    
    books_upd_title_old_author_val = ttk.Label(
        books_upd_title_lf,
        text="-",
        width=40,
        font=("Calibri", 16),
        bootstyle="warning"
    )
    books_upd_title_old_author_val.grid(column=0, row=3, padx=(40, 20),
                                        pady=(0, 10), sticky="w")
    
    books_upd_title_new_author_lbl_text = language_text(
        "Autor - nova vrednost:", "Author - new value:")
    books_upd_title_new_author_lbl = ttk.Label(
        books_upd_title_lf,
        text=books_upd_title_new_author_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    books_upd_title_new_author_lbl.grid(column=1, row=2, padx=(20, 40),
                                        pady=(10, 0), sticky="w")
    
    books_upd_title_new_author_entry = ttk.Entry(
        books_upd_title_lf,
        width=40,
        font=("Calibri", 16),
        bootstyle="light"
    )
    books_upd_title_new_author_entry.grid(column=1, row=3, padx=(20, 40),
                                          pady=(0, 10), sticky="w")
    
    books_upd_title_old_genre_lbl_text = language_text(
        "Žanr - trenutna vrednost:", "Genre - current value:")
    books_upd_title_old_genre_lbl = ttk.Label(
        books_upd_title_lf,
        text=books_upd_title_old_genre_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    books_upd_title_old_genre_lbl.grid(column=0, row=4, padx=(40, 20),
                                       pady=(10, 0), sticky="w")
    
    books_upd_title_old_genre_val = ttk.Label(
        books_upd_title_lf,
        text="-",
        width=40,
        font=("Calibri", 16),
        bootstyle="warning"
    )
    books_upd_title_old_genre_val.grid(column=0, row=5, padx=(40, 20),
                                       pady=(0, 10), sticky="w")
    
    books_upd_title_new_genre_lbl_text = language_text(
        "Žanr - nova vrednost:", "Genre - new value:")
    books_upd_title_new_genre_lbl = ttk.Label(
        books_upd_title_lf,
        text=books_upd_title_new_genre_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    books_upd_title_new_genre_lbl.grid(column=1, row=4, padx=(20, 40),
                                       pady=(10, 0), sticky="w")
    
    if language == "srpski":
        genres_list = creating_values_list(GENRES)[0]
    else:
        genres_list = creating_values_list(GENRES)[1]
    books_upd_title_new_genre_combo = ttk.Combobox(
        books_upd_title_lf,
        width=40,
        values=genres_list,
        font=("Calibri", 14),
        state="disabled",
        bootstyle="light"
    )
    books_upd_title_new_genre_combo.grid(column=1, row=5, padx=(20, 40),
                                         pady=(0, 10), sticky="w")
    
    books_upd_title_old_year_lbl_text = language_text(
        "Godina izdanja - trenutna vrednost:",
        "Publication year - current value:"
    )
    books_upd_title_old_year_lbl = ttk.Label(
        books_upd_title_lf,
        text=books_upd_title_old_year_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    books_upd_title_old_year_lbl.grid(column=0, row=6, padx=(40, 20),
                                      pady=(10, 0), sticky="w")
    
    books_upd_title_old_year_val = ttk.Label(
        books_upd_title_lf,
        text="-",
        width=20,
        font=("Calibri", 16),
        bootstyle="warning"
    )
    books_upd_title_old_year_val.grid(column=0, row=7, padx=(40, 20),
                                      pady=(0, 10), sticky="w")
    
    books_upd_title_new_year_lbl_text = language_text(
        "Godina izdanja - nova vrednost:", "Publication year - new value:")
    books_upd_title_new_year_lbl = ttk.Label(
        books_upd_title_lf,
        text=books_upd_title_new_year_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    books_upd_title_new_year_lbl.grid(column=1, row=6, padx=(20, 40),
                                      pady=(10, 0), sticky="w")
    
    pub_year_reg = books_upd_book_lf.register(
        lambda inp: len_digit_limit(inp, length=4))
    books_upd_title_new_year_entry = ttk.Entry(
        books_upd_title_lf,
        width=20,
        font=("Calibri", 16),
        validate="key",
        validatecommand=(pub_year_reg, "%P"),
        bootstyle="light"
    )
    books_upd_title_new_year_entry.grid(column=1, row=7, padx=(20, 40),
                                        pady=(0, 10), sticky="w")

    # 'Reset' and 'Update' buttons
    books_upd_title_buttons_frm = ttk.Frame(books_upd_title_lf)
    books_upd_title_buttons_frm.grid(column=1, row=8, pady=(10, 20),
                                     sticky="e")

    books_upd_update_btn_text = language_text("Ažuriraj", "Update")
    books_upd_title_update_btn = ttk.Button(
        books_upd_title_buttons_frm,
        text=books_upd_update_btn_text,
        width=10,
        style="big.dark.TButton",
        command=title_update_apply
    )
    books_upd_title_update_btn.pack(side="right", padx=40)

    books_upd_reset_btn_text = language_text("Resetuj", "Reset")
    books_upd_title_reset_btn = ttk.Button(
        books_upd_title_buttons_frm,
        text=books_upd_reset_btn_text,
        width=10,
        style="big.dark.TButton",
        command=reset_title_updating_frame
    )
    books_upd_title_reset_btn.pack(side="right")

    # Book update frame
    books_upd_book_lf.grid_columnconfigure((0, 1), weight=1)
    
    books_upd_book_code_lbl_text = language_text("Šifra knjige:", "Book code:")
    books_upd_book_code_lbl = ttk.Label(
        books_upd_book_lf,
        text=books_upd_book_code_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    books_upd_book_code_lbl.grid(column=0, row=0, padx=40, pady=(20, 0),
                                 sticky="w")
    
    codes_list = sorted(books.books_df.book_code.to_list())
    books_upd_book_code_combo = ttk.Combobox(
        books_upd_book_lf,
        width=20,
        values=codes_list,
        font=("Calibri", 14),
        state="readonly",
        bootstyle="light"
    )
    books_upd_book_code_combo.grid(column=0, row=1, padx=40, pady=(0, 10),
                                   sticky="w")

    # Bind this Combobox
    books_upd_book_code_combo.bind("<<ComboboxSelected>>", code_picked)

    books_upd_book_old_title_lbl = ttk.Label(
        books_upd_book_lf,
        text=books_upd_title_old_title_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    books_upd_book_old_title_lbl.grid(column=0, row=2, padx=(40, 20),
                                      pady=(10, 0), sticky="w")
    
    books_upd_book_old_title_val = ttk.Label(
        books_upd_book_lf,
        text="-",
        width=40,
        font=("Calibri", 16),
        bootstyle="warning"
    )
    books_upd_book_old_title_val.grid(column=0, row=3, padx=(40, 20),
                                      pady=(0, 10), sticky="w")

    books_upd_book_new_title_lbl = ttk.Label(
        books_upd_book_lf,
        text=books_upd_title_new_title_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    books_upd_book_new_title_lbl.grid(column=1, row=2, padx=(20, 40),
                                      pady=(10, 0), sticky="w")

    books_upd_book_new_title_entry = ttk.Entry(
        books_upd_book_lf,
        width=40,
        font=("Calibri", 16),
        bootstyle="light"
    )
    books_upd_book_new_title_entry.grid(column=1, row=3, padx=(20, 40),
                                        pady=(0, 10), sticky="w")
    
    books_upd_book_old_availability_lbl_text = language_text(
        "Dostupnost - trenutna vrednost:", "Availability - current value:")
    books_upd_book_old_availability_lbl = ttk.Label(
        books_upd_book_lf,
        text=books_upd_book_old_availability_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    books_upd_book_old_availability_lbl.grid(column=0, row=4, padx=(40, 20),
                                             pady=(10, 0), sticky="w")

    books_upd_book_old_availability_val = ttk.Label(
        books_upd_book_lf,
        text="-",
        width=20,
        font=("Calibri", 16),
        bootstyle="warning"
    )
    books_upd_book_old_availability_val.grid(column=0, row=5, padx=(40, 20),
                                             pady=(0, 10), sticky="w")

    books_upd_book_new_availability_lbl_text = language_text(
        "Dostupnost - nova vrednost:", "Availability - new value:")
    books_upd_book_new_availability_lbl = ttk.Label(
        books_upd_book_lf,
        text=books_upd_book_new_availability_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    books_upd_book_new_availability_lbl.grid(column=1, row=4, padx=(20, 40),
                                             pady=(10, 0), sticky="w")

    if language == "srpski":
        availability_list = creating_values_list(AVAILABILITY)[0]
    else:
        availability_list = creating_values_list(AVAILABILITY)[1]
    books_upd_book_new_availability_combo = ttk.Combobox(
        books_upd_book_lf,
        width=20,
        values=availability_list,
        font=("Calibri", 14),
        state="disabled",
        bootstyle="light"
    )
    books_upd_book_new_availability_combo.grid(column=1, row=5, padx=(20, 40),
                                               pady=(0, 10), sticky="w")
    
    # 'Reset' and 'Update' buttons
    books_upd_book_buttons_frm = ttk.Frame(books_upd_book_lf)
    books_upd_book_buttons_frm.grid(column=1, row=6, pady=(10, 20), sticky="e")
    
    books_upd_book_update_btn = ttk.Button(
        books_upd_book_buttons_frm,
        text=books_upd_update_btn_text,
        width=10,
        style="big.dark.TButton",
        command=book_update_apply
    )
    books_upd_book_update_btn.pack(side="right", padx=40)
    
    books_upd_book_reset_btn = ttk.Button(
        books_upd_book_buttons_frm,
        text=books_upd_reset_btn_text,
        width=10,
        style="big.dark.TButton",
        command=reset_book_updating_frame
    )
    books_upd_book_reset_btn.pack(side="right")
    
    # Close button
    books_upd_close_btn_text = language_text("Zatvori", "Close")
    books_upd_close_btn = ttk.Button(
        books_upd_sf,
        text=books_upd_close_btn_text,
        width=10,
        style="big.dark.TButton",
        command=books_upd_tl.destroy
    )
    books_upd_close_btn.pack(side="right", padx=60, pady=20)


def members_info():
    """Information about library members."""
    
    def mem_id_selected(event):
        """Changes that occur when a membership ID is selected."""
        
        # Data needed
        selected_mem_id = info_mem_id_combo.get()
        
        mem_first_name = members.members_df.first_name[
            members.members_df.membership_id == selected_mem_id
        ].to_string(index=False)
        mem_last_name = members.members_df.last_name[
            members.members_df.membership_id == selected_mem_id
        ].to_string(index=False)
        full_name = f"{mem_first_name} {mem_last_name}"
        
        mem_address = members.members_df.address[
            members.members_df.membership_id == selected_mem_id
        ].to_string(index=False)
        
        mem_phone = members.members_df.telephone[
            members.members_df.membership_id == selected_mem_id
        ].to_string(index=False)
        
        mem_since_str = members.members_df.membership_date[
            members.members_df.membership_id == selected_mem_id
        ].to_string(index=False)
        mem_since_lst = mem_since_str.split("-")
        mem_since = f"{mem_since_lst[2]}. {mem_since_lst[1]}. " \
                    f"{mem_since_lst[0]}."
        
        mem_password = members.members_df.password[
            members.members_df.membership_id == selected_mem_id
        ].to_string(index=False)
        
        total_rented = renting.renting_df[
            renting.renting_df.membership_id == selected_mem_id
        ]["membership_id"].count()
        
        delays = not_on_time(selected_mem_id)
        
        # Membership IDs of unreturned books
        rented_mem_ids_list = renting.renting_df.membership_id[
            renting.renting_df.return_date.isnull()].to_list()
        
        # Dataframe of unreturned books
        currently_rented_df = renting.renting_df[
            renting.renting_df.return_date.isnull()]
        
        if selected_mem_id in rented_mem_ids_list:
            rented_row_list = currently_rented_df[
                currently_rented_df.membership_id == selected_mem_id
            ].values.flatten()
            
            rented_title = books.books_df.title[
                books.books_df.book_code == rented_row_list[2]
            ].to_string(index=False)
            
            rented_date_str = rented_row_list[3].strftime("%d. %m. %Y.")
            
            info_current_val.configure(bootstyle="info")
            currently_rented = f"{rented_row_list[1]} - {rented_title}" \
                               f" - {rented_date_str}"
        else:
            info_current_val.configure(bootstyle="danger")
            currently_rented = language_text("Nema iznajmljene knjige",
                                             "There is no rented book")

        # Dataframe for the specified member
        mem_reservation_df = reservations.reservations_df[
            reservations.reservations_df.membership_id == selected_mem_id]
        
        book_codes_reserved_list = mem_reservation_df.book_code[
            mem_reservation_df.membership_id == selected_mem_id].to_list()
        dates_reserved_list = mem_reservation_df.reservation_date[
            mem_reservation_df.membership_id == selected_mem_id].to_list()
        
        if reservation_info(selected_mem_id)[0] != "-":
            last_date = max(dates_reserved_list)
            last_date_str = last_date.strftime("%d. %m. %Y.")
            for i in range(len(dates_reserved_list)):
                if dates_reserved_list[i] == last_date:
                    reserved_book_code = book_codes_reserved_list[i]

            reserved_title = books.books_df.title[
                books.books_df.book_code == reserved_book_code
            ].to_string(index=False)
            
            info_reserve_val.configure(bootstyle="info")
            currently_reserved = f"{reserved_book_code} - {reserved_title}" \
                                 f" - {last_date_str}"
        else:
            info_reserve_val.configure(bootstyle="danger")
            currently_reserved = language_text("Nema rezervisane knjige",
                                               "There is no reserved book")
        
        # Set labels texts
        info_name_val.configure(text=full_name)
        info_address_val.configure(text=mem_address)
        info_phone_val.configure(text=mem_phone)
        info_membership_val.configure(text=mem_since)
        info_password_val.configure(text=mem_password)
        
        info_total_val.configure(text=total_rented)
        info_retern_val.configure(text=delays)
        info_current_val.configure(text=currently_rented)
        info_reserve_val.configure(text=currently_reserved)
        
    
    info_tl_title = language_text("Informacije o članovima",
                                  "Member information")
    info_tl = ttk.Toplevel(title=info_tl_title)
    info_tl.attributes("-topmost", "true")
    info_tl.resizable(False, False)
    info_tl.geometry("900x960")
    info_tl.grab_set()
    
    # Frames
    info_top_frm = ttk.Frame(info_tl)
    info_top_frm.pack(fill="x", padx=20, pady=20)
    
    info_member_lf_text = language_text(" Član ", " Member ")
    info_member_lf = ttk.LabelFrame(
        info_tl,
        text=info_member_lf_text,
        bootstyle="warning"
    )
    info_member_lf.pack(fill="x", padx=20, pady=20)

    info_rent_lf_text = language_text(" Iznajmljivanja i rezervacije ",
                                       " Rentals and reservations ")
    info_rent_lf = ttk.LabelFrame(
        info_tl,
        text=info_rent_lf_text,
        bootstyle="warning"
    )
    info_rent_lf.pack(fill="x", padx=20, pady=20)
    
    # Top frame widgets
    info_main_text = language_text(" Biblioteka \"Vuk Karadžić\"",
                                   " Library \"Vuk Karadžić\"")
    info_main_lbl = ttk.Label(
        info_top_frm,
        text=info_main_text,
        font=("Calibri", 36, "bold"),
        image=logo_smaller,
        compound="left",
        anchor="center",
        bootstyle="warning"
    )
    info_main_lbl.pack(expand=True, fill="x")
    
    librarian = logged_in_librarian()
    info_librarian_lbl_text = language_text(f"Bibliotekar: {librarian}",
                                            f"Librarian: {librarian}")
    info_librarian_lbl = ttk.Label(
        info_top_frm,
        text=info_librarian_lbl_text,
        font=("Calibri", 16),
        bootstyle="danger"
    )
    info_librarian_lbl.pack(pady=10)
    
    info_title_lbl = ttk.Label(
        info_top_frm,
        text=info_tl_title.upper(),
        font=("Calibri", 28, "bold"),
        anchor="center",
        bootstyle="warning"
    )
    info_title_lbl.pack(expand=True, fill="x", pady=(0, 10))
    
    # Member frame widgets
    info_member_lf.grid_columnconfigure((0, 1), weight=1)
    
    info_mem_id_lbl_text = language_text("Broj članske karte:",
                                         "Membership ID:")
    info_mem_id_lbl = ttk.Label(
        info_member_lf,
        text=info_mem_id_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    info_mem_id_lbl.grid(column=0, row=0, padx=(40, 20), pady=(20, 0),
                         sticky="w")
    
    mem_id_list = sorted(members.members_df.membership_id.to_list())
    info_mem_id_combo = ttk.Combobox(
        info_member_lf,
        width=20,
        values=mem_id_list,
        font=("Calibri", 14),
        state="readonly",
        bootstyle="light"
    )
    info_mem_id_combo.grid(column=0, row=1, padx=(40, 20), pady=(0, 10),
                           sticky="w")

    # Bind this Combobox
    info_mem_id_combo.bind("<<ComboboxSelected>>", mem_id_selected)
    
    info_name_lbl_text = language_text("Ime člana:", "Member name:")
    info_name_lbl = ttk.Label(
        info_member_lf,
        text=info_name_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    info_name_lbl.grid(column=1, row=0, padx=(20, 40), pady=(20, 0),
                       sticky="w")
    
    info_name_val = ttk.Label(
        info_member_lf,
        text="-",
        width=40,
        font=("Calibri", 16),
        bootstyle="warning"
    )
    info_name_val.grid(column=1, row=1, padx=(20, 40), pady=(0, 10),
                       sticky="w")
    
    info_address_lbl_text = language_text("Adresa člana:", "Member's address:")
    info_address_lbl = ttk.Label(
        info_member_lf,
        text=info_address_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    info_address_lbl.grid(column=0, row=2, padx=(40, 20), pady=(10, 0),
                          sticky="w")
    
    info_address_val = ttk.Label(
        info_member_lf,
        text="-",
        width=40,
        font=("Calibri", 16),
        bootstyle="warning"
    )
    info_address_val.grid(column=0, row=3, padx=(40, 20), pady=(0, 10),
                          sticky="w")
    
    info_phone_lbl_text = language_text("Telefon člana:", "Member's phone:")
    info_phone_lbl = ttk.Label(
        info_member_lf,
        text=info_phone_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    info_phone_lbl.grid(column=1, row=2, padx=(20, 40), pady=(10, 0),
                        sticky="w")
    
    info_phone_val = ttk.Label(
        info_member_lf,
        text="-",
        width=40,
        font=("Calibri", 16),
        bootstyle="warning"
    )
    info_phone_val.grid(column=1, row=3, padx=(20, 40), pady=(0, 10),
                        sticky="w")
    
    info_membership_lbl_text = language_text("Člana od:", "Member since:")
    info_membership_lbl = ttk.Label(
        info_member_lf,
        text=info_membership_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    info_membership_lbl.grid(column=0, row=4, padx=(40, 20), pady=(10, 0),
                             sticky="w")
    
    info_membership_val = ttk.Label(
        info_member_lf,
        text="-",
        width=40,
        font=("Calibri", 16),
        bootstyle="warning"
    )
    info_membership_val.grid(column=0, row=5, padx=(40, 20), pady=(0, 20),
                             sticky="w")
    
    info_password_lbl_text = language_text("Lozinka člana:",
                                           "Member password:")
    info_password_lbl = ttk.Label(
        info_member_lf,
        text=info_password_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    info_password_lbl.grid(column=1, row=4, padx=(20, 40), pady=(10, 0),
                           sticky="w")
    
    info_password_val = ttk.Label(
        info_member_lf,
        text="-",
        width=40,
        font=("Calibri", 16),
        bootstyle="warning"
    )
    info_password_val.grid(column=1, row=5, padx=(20, 40), pady=(0, 20),
                           sticky="w")

    # Rental frame widget
    info_rent_lf.grid_columnconfigure((0, 1), weight=1)

    info_total_lbl_text = language_text("Ukupno iznajmljivano:",
                                         "Total rented:")
    info_total_lbl = ttk.Label(
        info_rent_lf,
        text=info_total_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    info_total_lbl.grid(column=0, row=0, padx=(40, 20), pady=(20, 0),
                        sticky="w")

    info_total_val = ttk.Label(
        info_rent_lf,
        text="-",
        width=40,
        font=("Calibri", 16),
        bootstyle="warning"
    )
    info_total_val.grid(column=0, row=1, padx=(40, 20), pady=(0, 10),
                        sticky="w")

    info_retern_lbl_text = language_text("Nije vraćeno na vreme:",
                                         "Not returned on time:")
    info_retern_lbl = ttk.Label(
        info_rent_lf,
        text=info_retern_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    info_retern_lbl.grid(column=1, row=0, padx=(20, 40), pady=(20, 0),
                         sticky="w")

    info_retern_val = ttk.Label(
        info_rent_lf,
        text="-",
        width=40,
        font=("Calibri", 16),
        bootstyle="warning"
    )
    info_retern_val.grid(column=1, row=1, padx=(20, 40), pady=(0, 10),
                         sticky="w")

    info_current_lbl_text = language_text(
        "Trenutno iznajmljeno (šifra - naslov - datum):",
        "Currently rented (code - title - date):"
    )
    info_current_lbl = ttk.Label(
        info_rent_lf,
        text=info_current_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    info_current_lbl.grid(column=0, row=2, columnspan=2, padx=40, pady=(10, 0),
                          sticky="w")

    info_current_val = ttk.Label(
        info_rent_lf,
        text="-",
        width=100,
        font=("Calibri", 16),
        bootstyle="warning"
    )
    info_current_val.grid(column=0, row=3, columnspan=2, padx=40, pady=(0, 10),
                          sticky="w")

    info_reserve_lbl_text = language_text(
        "Trenutno rezervisano (šifra - naslov - datum):",
        "Currently reserved (code - title - date):"
    )
    info_reserve_lbl = ttk.Label(
        info_rent_lf,
        text=info_reserve_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    info_reserve_lbl.grid(column=0, row=4, columnspan=2, padx=40, pady=(10, 0),
                          sticky="w")

    info_reserve_val = ttk.Label(
        info_rent_lf, text="-",
        width=100,
        font=("Calibri", 16),
        bootstyle="warning"
    )
    info_reserve_val.grid(column=0, row=5, columnspan=2, padx=40, pady=(0, 20),
                          sticky="w")

    # Close button
    info_close_btn_text = language_text("Zatvori", "Close")
    info_close_btn = ttk.Button(
        info_tl,
        text=info_close_btn_text,
        width=10,
        style="big.dark.TButton",
        command=info_tl.destroy
    )
    info_close_btn.pack(side="right", padx=50, pady=(0, 20))


def new_members():
    """Adding new members to the library."""
    
    def new_member_data_apply():
        """Adding new date to the 'members' table."""
        
        # Messagebox titles
        msg_title = language_text("Nedostaje unos", "Missing entry")
        title_success = language_text("Uspešan unos", "Successful entry")
        
        # Messages
        missing_first_name = language_text(
            "Niste uneli ime novog člana!",
            "You have not entered a new member's name!"
        )
        
        missing_last_name = language_text(
            "Niste uneli prezime novog člana!",
            "You have not entered a new member's surname!"
        )
        
        missing_address = language_text(
            "Niste uneli adresu novog člana!",
            "You have not entered a new member's address!"
        )
        
        missing_phone = language_text(
            "Niste uneli broj telefona novog člana!",
            "You have not entered a new member's phone number!"
        )
        
        msg_success = language_text(
            "Podaci o novom članu biblioteke uspešno su uneti.",
            "The data about the new library member has been successfully "
            "entered."
        )
        
        # Data needed
        mem_id = new_id_val.cget("text")
        f_name = new_first_name_entry.get()
        l_name = new_last_name_entry.get()
        address = new_address_entry.get()
        phone = new_phone_entry.get()
        mem_date = date.today()
        password = new_password_entry.get()
        
        if not new_first_name_entry.get():
            Messagebox.show_info(
                title=msg_title,
                message=missing_first_name,
                parent=new_tl,
                alert=True
            )
        elif not new_last_name_entry.get():
            Messagebox.show_info(
                title=msg_title,
                message=missing_last_name,
                parent=new_tl,
                alert=True
            )
        elif not new_address_entry.get():
            Messagebox.show_info(
                title=msg_title,
                message=missing_address,
                parent=new_tl,
                alert=True
            )
        elif not new_phone_entry.get():
            Messagebox.show_info(
                title=msg_title,
                message=missing_phone,
                parent=new_tl,
                alert=True
            )
        else:
            new_member_sql = f"""
            INSERT INTO members (membership_id, first_name, last_name,
            address, telephone, membership_date, password)
            VALUES ('{mem_id}', '{f_name}', '{l_name}', '{address}', '{phone}',
            '{mem_date}', '{password}');
            """
            members.members_updating(new_member_sql)

            new_mem_ids_list = members.members_df.membership_id.to_list()
            new_mem_id_value = unique_code_generating(new_mem_ids_list, 6)
            
            new_id_val.configure(text=new_mem_id_value)
            new_first_name_entry.delete(0, END)
            new_last_name_entry.delete(0, END)
            new_address_entry.delete(0, END)
            new_phone_entry.delete(0, END)
            new_password_entry.delete(0, END)
            new_password_entry.insert(0, "member")
            
            Messagebox.show_info(
                title=title_success,
                message=msg_success,
                parent=new_tl,
                alert=True
            )
    
    
    new_tl_title = language_text("Novi članovi", "New members")
    new_tl = ttk.Toplevel(title=new_tl_title)
    new_tl.attributes("-topmost", "true")
    new_tl.resizable(False, False)
    new_tl.geometry("800x680")
    new_tl.grab_set()
    
    # Frames
    new_top_frm = ttk.Frame(new_tl)
    new_top_frm.pack(fill="x", padx=20, pady=20)
    
    new_data_frm = ttk.Frame(new_tl)
    new_data_frm.pack(fill="x", padx=20, pady=20)
    
    # Top frame wigdets
    new_main_text = language_text(" Biblioteka \"Vuk Karadžić\"",
                                  " Library \"Vuk Karadžić\"")
    new_main_lbl = ttk.Label(
        new_top_frm,
        text=new_main_text,
        font=("Calibri", 36, "bold"),
        image=logo_smaller,
        compound="left",
        anchor="center",
        bootstyle="warning"
    )
    new_main_lbl.pack(expand=True, fill="x")

    librarian = logged_in_librarian()
    new_librarian_lbl_text = language_text(f"Bibliotekar: {librarian}",
                                           f"Librarian: {librarian}")
    new_librarian_lbl = ttk.Label(
        new_top_frm,
        text=new_librarian_lbl_text,
        font=("Calibri", 16),
        bootstyle="danger"
    )
    new_librarian_lbl.pack(pady=10)

    new_title_lbl_text = language_text("DODAVANJE NOVOG ČLANA",
                                       "NEW MEMBER ADDING")
    new_title_lbl = ttk.Label(
        new_top_frm,
        text=new_title_lbl_text,
        font=("Calibri", 28, "bold"),
        anchor="center",
        bootstyle="warning"
    )
    new_title_lbl.pack(expand=True, fill="x", pady=(0, 10))
    
    # Data frame widgets
    new_data_frm.grid_columnconfigure((0, 1), weight=1)
    
    new_first_name_lbl_text = language_text("Ime novog člana:",
                                            "New member name:")
    new_first_name_lbl = ttk.Label(
        new_data_frm,
        text=new_first_name_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    new_first_name_lbl.grid(column=0, row=0, padx=(40, 20), pady=(20, 0),
                            sticky="w")
    
    new_first_name_entry = ttk.Entry(
        new_data_frm,
        width=35,
        font=("Calibri", 16),
        bootstyle="light"
    )
    new_first_name_entry.grid(column=0, row=1, padx=(40, 20), pady=(0, 10),
                              sticky="w")
    new_first_name_entry.focus()
    
    new_last_name_lbl_text = language_text("Prezime novog člana:",
                                           "New member surname:")
    new_last_name_lbl = ttk.Label(
        new_data_frm,
        text=new_last_name_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    new_last_name_lbl.grid(column=1, row=0, padx=(20, 40), pady=(20, 0),
                           sticky="w")
    
    new_last_name_entry = ttk.Entry(
        new_data_frm,
        width=35,
        font=("Calibri", 16),
        bootstyle="light"
    )
    new_last_name_entry.grid(column=1, row=1, padx=(20, 40), pady=(0, 10),
                             sticky="w")
    
    new_address_lbl_text = language_text("Adresa novog člana:",
                                         "New member address:")
    new_address_lbl = ttk.Label(
        new_data_frm,
        text=new_address_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    new_address_lbl.grid(column=0, row=2, padx=(40, 20), pady=(10, 0),
                         sticky="w")
    
    new_address_entry = ttk.Entry(
        new_data_frm,
        width=35,
        font=("Calibri", 16),
        bootstyle="light"
    )
    new_address_entry.grid(column=0, row=3, padx=(40, 20), pady=(0, 10),
                           sticky="w")
    
    new_phone_lbl_text = language_text("Telefon novog člana:",
                                         "New member phone:")
    new_phone_lbl = ttk.Label(
        new_data_frm,
        text=new_phone_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    new_phone_lbl.grid(column=1, row=2, padx=(20, 40), pady=(10, 0),
                       sticky="w")
    
    new_phone_reg = new_data_frm.register(
        lambda inp: len_digit_limit(inp, length=10))
    new_phone_entry = ttk.Entry(
        new_data_frm,
        width=35,
        font=("Calibri", 16),
        validate="key",
        validatecommand=(new_phone_reg, "%P"),
        bootstyle="light"
    )
    new_phone_entry.grid(column=1, row=3, padx=(20, 40), pady=(0, 10),
                         sticky="w")
    
    new_id_lbl_text = language_text("Broj članske karte:", "Membership ID:")
    new_id_lbl = ttk.Label(
        new_data_frm,
        text=new_id_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    new_id_lbl.grid(column=0, row=4, padx=(40, 20), pady=(10, 0), sticky="w")
    
    mem_ids_list = members.members_df.membership_id.to_list()
    new_id_value = unique_code_generating(mem_ids_list, 6)
    new_id_val = ttk.Label(
        new_data_frm,
        text=new_id_value,
        width=35,
        font=("Calibri", 16)
    )
    new_id_val.grid(column=0, row=5, padx=(40, 20), pady=(0, 20), sticky="w")
    
    new_password_lbl_text = language_text("Lozinka novog člana:",
                                          "New Member Password:")
    new_password_lbl = ttk.Label(
        new_data_frm,
        text=new_password_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    new_password_lbl.grid(column=1, row=4, padx=(20, 40), pady=(10, 0),
                          sticky="w")
    
    new_password_entry = ttk.Entry(
        new_data_frm,
        width=35,
        font=("Calibri", 16),
        bootstyle="light"
    )
    new_password_entry.grid(column=1, row=5, padx=(20, 40), pady=(0, 20),
                         sticky="w")
    new_password_entry.insert(0, "member")
    
    # Buttons
    new_close_btn_text = language_text("Zatvori", "Close")
    new_close_btn = ttk.Button(
        new_tl,
        text=new_close_btn_text,
        width=10,
        style="big.dark.TButton",
        command=new_tl.destroy
    )
    new_close_btn.pack(side="right", padx=(40, 60), pady=(0, 20))
    
    new_apply_btn_text = language_text("Primeni", "Apply")
    new_apply_btn = ttk.Button(
        new_tl,
        text=new_apply_btn_text,
        width=10,
        style="big.dark.TButton",
        command=new_member_data_apply
    )
    new_apply_btn.pack(side="right", pady=(0, 20))


def members_updating():
    """Updating library member data."""
    
    def member_id_selected(event):
        """Changes that occur when a membership ID is selected."""
        
        # Current data
        current_list = members.members_df[
            members.members_df.membership_id == mem_upd_id_combo.get()
        ].values.flatten().tolist()
        
        # Set the current values in the corresponding labels
        mem_upd_old_name_val.configure(text=current_list[1])
        mem_upd_old_surname_val.configure(text=current_list[2])
        mem_upd_old_address_val.configure(text=current_list[3])
        mem_upd_old_phone_val.configure(text=current_list[4])
        mem_upd_old_password_val.configure(text=current_list[6])
    
    def update_member_reset():
        """Reset all values."""
        
        mem_upd_id_combo.set("")
        mem_upd_old_name_val.configure(text="-")
        mem_upd_old_surname_val.configure(text="-")
        mem_upd_old_address_val.configure(text="-")
        mem_upd_old_phone_val.configure(text="-")
        mem_upd_old_password_val.configure(text="-")
        mem_upd_new_name_entry.delete(0, END)
        mem_upd_new_surname_entry.delete(0, END)
        mem_upd_new_address_entry.delete(0, END)
        mem_upd_new_phone_entry.delete(0, END)
        mem_upd_new_password_entry.delete(0, END)
    
    def execute_members_sql():
        """Entering new data into the 'members' table."""
        
        members_update_dict = {
            "first_name": mem_upd_new_name_entry.get(),
            "last_name": mem_upd_new_surname_entry.get(),
            "address": mem_upd_new_address_entry.get(),
            "telephone": mem_upd_new_phone_entry.get(),
            "password": mem_upd_new_password_entry.get()
        }
        
        if not mem_upd_new_name_entry.get() and not \
                mem_upd_new_surname_entry.get() and not \
                mem_upd_new_address_entry.get() and not \
                mem_upd_new_phone_entry.get() and not \
                mem_upd_new_password_entry.get():
            no_data_title = language_text("Nema podatak", "No data")
            no_data_message = language_text(
                "Niste uneli nijedan podatak za ažuriranje.",
                "You have not entered any information to update."
            )
            Messagebox.show_info(
                title=no_data_title,
                message=no_data_message,
                parent=mem_upd_tl,
                alert=True
            )
        else:
            for key, value in members_update_dict.items():
                if value:
                    mem_upd_sql = f"""
                    UPDATE members
                    SET {key} = '{value}'
                    WHERE membership_id = '{mem_upd_id_combo.get()}';
                    """
                    
                    members.members_updating(mem_upd_sql)
    
            member_id = mem_upd_id_combo.get()
            title_success = language_text("Uspešan unos", "Successful entry")
            message_success = language_text(
                f"Podaci člana pod brojem {member_id} uspešno su ažurirani.",
                f"Member data under number {member_id} has been successfully "
                f"updated."
            )
            
            update_member_reset()
            
            Messagebox.show_info(
                title=title_success,
                message=message_success,
                parent=mem_upd_tl,
                alert=True
            )
    
    
    mem_upd_main_title_text = language_text("Ažuriranje članova",
                                            "Members update")
    mem_upd_tl = ttk.Toplevel(title=mem_upd_main_title_text)
    mem_upd_tl.attributes("-topmost", "true")
    mem_upd_tl.resizable(False, False)
    mem_upd_tl.geometry("800x930")
    mem_upd_tl.grab_set()
    
    # Frames
    mem_upd_top_frm = ttk.Frame(mem_upd_tl)
    mem_upd_top_frm.pack(fill="x", padx=20, pady=20)
    
    mem_upd_data_frm = ttk.Frame(mem_upd_tl)
    mem_upd_data_frm.pack(fill="x", padx=20, pady=20)
    
    # Top frame widgets
    mem_upd_main_text = language_text(" Biblioteka \"Vuk Karadžić\"",
                                      " Library \"Vuk Karadžić\"")
    mem_upd_main_lbl = ttk.Label(
        mem_upd_top_frm,
        text=mem_upd_main_text,
        font=("Calibri", 36, "bold"),
        image=logo_smaller,
        compound="left",
        anchor="center",
        bootstyle="warning"
    )
    mem_upd_main_lbl.pack(expand=True, fill="x")
    
    librarian = logged_in_librarian()
    mem_upd_librarian_text = language_text(f"Bibliotekar: {librarian}",
                                           f"Librarian: {librarian}")
    mem_upd_librarian_lbl = ttk.Label(
        mem_upd_top_frm,
        text=mem_upd_librarian_text,
        font=("Calibri", 16),
        bootstyle="danger"
    )
    mem_upd_librarian_lbl.pack(pady=10)
    
    mem_upd_title_lbl = ttk.Label(
        mem_upd_top_frm,
        text=mem_upd_main_text.upper(),
        font=("Calibri", 28, "bold"),
        anchor="center",
        bootstyle="warning"
    )
    mem_upd_title_lbl.pack(expand=True, fill="x", pady=(0, 10))
    
    # Data frame widgets
    mem_upd_data_frm.grid_columnconfigure((0, 1), weight=1)
    
    mem_upd_id_lbl_text = language_text("Broj članske karte:",
                                        "Membership ID:")
    mem_upd_id_lbl = ttk.Label(
        mem_upd_data_frm,
        text=mem_upd_id_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    mem_upd_id_lbl.grid(column=0, row=0, padx=(40, 20), pady=(20, 0),
                        sticky="w")
    
    membership_ids_list = sorted(members.members_df.membership_id.to_list())
    mem_upd_id_combo = ttk.Combobox(
        mem_upd_data_frm,
        width=10,
        values=membership_ids_list,
        font=("Calibri", 14),
        state="readonly",
        bootstyle="light"
    )
    mem_upd_id_combo.grid(column=0, row=1, padx=(40, 20), pady=(0, 10),
                          sticky="w")
    
    # Bind this Combobox
    mem_upd_id_combo.bind("<<ComboboxSelected>>", member_id_selected)
    
    mem_upd_old_name_lbl_text = language_text("Ime u bazi podataka:",
                                              "Name in the database:")
    mem_upd_old_name_lbl = ttk.Label(
        mem_upd_data_frm,
        text=mem_upd_old_name_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    mem_upd_old_name_lbl.grid(column=0, row=2, padx=(40, 20), pady=(10, 0),
                              sticky="w")
    
    mem_upd_old_name_val = ttk.Label(
        mem_upd_data_frm,
        text="-",
        width=35,
        font=("Calibri", 16),
        bootstyle="warning"
    )
    mem_upd_old_name_val.grid(column=0, row=3, padx=(40, 20), pady=(0, 10),
                              sticky="w")
    
    mem_upd_new_name_lbl_text = language_text("Novo ime:", "New name:")
    mem_upd_new_name_lbl = ttk.Label(
        mem_upd_data_frm,
        text=mem_upd_new_name_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    mem_upd_new_name_lbl.grid(column=1, row=2, padx=(20, 40), pady=(10, 0),
                              sticky="w")
    
    mem_upd_new_name_entry = ttk.Entry(
        mem_upd_data_frm,
        width=35,
        font=("Calibri", 16),
        bootstyle="light"
    )
    mem_upd_new_name_entry.grid(column=1, row=3, padx=(20, 40), pady=(0, 10),
                                sticky="w")
    
    mem_upd_old_surname_lbl_text = language_text("Prezime u bazi podataka:",
                                                 "Surname in the database:")
    mem_upd_old_surname_lbl = ttk.Label(
        mem_upd_data_frm,
        text=mem_upd_old_surname_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    mem_upd_old_surname_lbl.grid(column=0, row=4, padx=(40, 20), pady=(10, 0),
                                 sticky="w")
    
    mem_upd_old_surname_val = ttk.Label(
        mem_upd_data_frm,
        text="-",
        width=35,
        font=("Calibri", 16),
        bootstyle="warning"
    )
    mem_upd_old_surname_val.grid(column=0, row=5, padx=(40, 20), pady=(0, 10),
                                 sticky="w")
    
    mem_upd_new_surname_lbl_text = language_text("Novo prezime:",
                                                 "New surname:")
    mem_upd_new_surname_lbl = ttk.Label(
        mem_upd_data_frm,
        text=mem_upd_new_surname_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    mem_upd_new_surname_lbl.grid(column=1, row=4, padx=(20, 40), pady=(10, 0),
                                 sticky="w")
    
    mem_upd_new_surname_entry = ttk.Entry(
        mem_upd_data_frm,
        width=35,
        font=("Calibri", 16),
        bootstyle="light"
    )
    mem_upd_new_surname_entry.grid(column=1, row=5, padx=(20, 40),
                                   pady=(0, 10), sticky="w")
    
    mem_upd_old_address_lbl_text = language_text("Adresa u bazi podataka:",
                                                 "Address in the database:")
    mem_upd_old_address_lbl = ttk.Label(
        mem_upd_data_frm,
        text=mem_upd_old_address_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    mem_upd_old_address_lbl.grid(column=0, row=6, padx=(40, 20), pady=(10, 0),
                                 sticky="w")
    
    mem_upd_old_address_val = ttk.Label(
        mem_upd_data_frm,
        text="-",
        width=35,
        font=("Calibri", 16),
        bootstyle="warning"
    )
    mem_upd_old_address_val.grid(column=0, row=7, padx=(40, 20), pady=(0, 10),
                                 sticky="w")
    
    mem_upd_new_address_lbl_text = language_text("Nova adresa:",
                                                 "New address:")
    mem_upd_new_address_lbl = ttk.Label(
        mem_upd_data_frm,
        text=mem_upd_new_address_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    mem_upd_new_address_lbl.grid(column=1, row=6, padx=(20, 40), pady=(10, 0),
                                 sticky="w")
    
    mem_upd_new_address_entry = ttk.Entry(
        mem_upd_data_frm,
        width=35,
        font=("Calibri", 16),
        bootstyle="light"
    )
    mem_upd_new_address_entry.grid(column=1, row=7, padx=(20, 40),
                                   pady=(0, 10), sticky="w")
    
    mem_upd_old_phone_lbl_text = language_text("Telefon u bazi podataka:",
                                               "Phone in the database:")
    mem_upd_old_phone_lbl = ttk.Label(
        mem_upd_data_frm,
        text=mem_upd_old_phone_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    mem_upd_old_phone_lbl.grid(column=0, row=8, padx=(40, 20), pady=(10, 0),
                               sticky="w")
    
    mem_upd_old_phone_val = ttk.Label(
        mem_upd_data_frm,
        text="-",
        width=35,
        font=("Calibri", 16),
        bootstyle="warning"
    )
    mem_upd_old_phone_val.grid(column=0, row=9, padx=(40, 20), pady=(0, 10),
                               sticky="w")
    
    mem_upd_new_phone_lbl_text = language_text("Novi telefon:", "New phone:")
    mem_upd_new_phone_lbl = ttk.Label(
        mem_upd_data_frm,
        text=mem_upd_new_phone_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    mem_upd_new_phone_lbl.grid(column=1, row=8, padx=(20, 40), pady=(10, 0),
                               sticky="w")
    mem_upd_new_phone_reg = mem_upd_data_frm.register(
        lambda inp: len_digit_limit(inp, length=10))
    mem_upd_new_phone_entry = ttk.Entry(
        mem_upd_data_frm,
        width=35,
        font=("Calibri", 16),
        validate="key",
        validatecommand=(mem_upd_new_phone_reg, "%P"),
        bootstyle="light"
    )
    mem_upd_new_phone_entry.grid(column=1, row=9, padx=(20, 40), pady=(0, 10),
                                 sticky="w")
    
    mem_upd_old_password_lbl_text = language_text("Lozinka u bazi podataka:",
                                                  "Password in the database:")
    mem_upd_old_password_lbl = ttk.Label(
        mem_upd_data_frm,
        text=mem_upd_old_password_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    mem_upd_old_password_lbl.grid(column=0, row=10, padx=(40, 20), pady=(10, 0),
                      sticky="w")
    
    mem_upd_old_password_val = ttk.Label(
        mem_upd_data_frm,
        text="-",
        width=35,
        font=("Calibri", 16),
        bootstyle="warning"
    )
    mem_upd_old_password_val.grid(column=0, row=11, padx=(40, 20), pady=(0, 10),
                          sticky="w")
    
    mem_upd_new_password_lbl_text = language_text("Nova lozinka:",
                                                  "New password:")
    mem_upd_new_password_lbl = ttk.Label(
        mem_upd_data_frm,
        text=mem_upd_new_password_lbl_text,
        font=("Calibri", 16),
        bootstyle="light"
    )
    mem_upd_new_password_lbl.grid(column=1, row=10, padx=(20, 40), pady=(10, 0),
                          sticky="w")
    
    mem_upd_new_password_entry = ttk.Entry(
        mem_upd_data_frm,
        width=35,
        font=("Calibri", 16),
        bootstyle="light"
    )
    mem_upd_new_password_entry.grid(column=1, row=11, padx=(20, 40), pady=(0, 10),
                            sticky="w")
    
    # Buttons
    mem_upd_close_btn_text = language_text("Zatvori", "Close")
    mem_upd_close_btn = ttk.Button(
        mem_upd_tl,
        text=mem_upd_close_btn_text,
        width=10,
        style="big.dark.TButton",
        command=mem_upd_tl.destroy
    )
    mem_upd_close_btn.pack(side="right", padx=(40, 60), pady=20)
    
    mem_upd_reset_btn_text = language_text("Resetuj", "Reset")
    mem_upd_reset_btn = ttk.Button(
        mem_upd_tl,
        text=mem_upd_reset_btn_text,
        width=10,
        style="big.dark.TButton",
        command=update_member_reset
    )
    mem_upd_reset_btn.pack(side="right", pady=20)
    
    mem_upd_apply_btn_text = language_text("Primeni", "Apply")
    mem_upd_apply_btn = ttk.Button(
        mem_upd_tl,
        text=mem_upd_apply_btn_text,
        width=10,
        style="big.dark.TButton",
        command=execute_members_sql
    )
    mem_upd_apply_btn.pack(side="right", padx=40, pady=20)


def book_rental():
    """Recording of rental and return dates of books."""
    
    def membership_id_selected(event):
        """Changes that occur when selecting a membership ID."""

        # Selected ID
        mem_id = rent_member_id_combo.get()
        
        # Member's first and last name
        mem_first_name = members.members_df.first_name[
            members.members_df.membership_id == mem_id].to_string(index=False)
        mem_last_name = members.members_df.last_name[
            members.members_df.membership_id == mem_id].to_string(index=False)
        
        rent_member_name_val.configure(text=f"{mem_first_name} "
                                            f"{mem_last_name}")

        # Lists of book codes and membership IDs of rented books
        code_book_rented_list = renting.renting_df.book_code[
            renting.renting_df.return_date.isnull()].to_list()
        membership_id_rented_list = renting.renting_df.membership_id[
            renting.renting_df.return_date.isnull()].to_list()
        
        if mem_id in membership_id_rented_list:
            # Index of the book code and the membership ID in their lists
            idx = membership_id_rented_list.index(mem_id)
            
            # Required values
            currently_rented = books.books_df.title[
                books.books_df.book_code == code_book_rented_list[idx]
            ].to_string(index=False)
            rented_book_author = titles.titles_df.author[
                titles.titles_df.title == currently_rented
            ].to_string(index=False)
            copies_total = books.books_df[
                books.books_df.title == currently_rented]["title"].count()
            copies_available = books.books_df[
                (books.books_df.title == currently_rented) & (
                        books.books_df.availability == "Available")][
                "title"].count()
            rented_date = renting.renting_df.rental_date[
                (renting.renting_df.membership_id ==
                 membership_id_rented_list[idx]) &
                (renting.renting_df.book_code == code_book_rented_list[idx]) &
                (renting.renting_df.return_date.isnull())
            ]
            deadline_date = (rented_date + timedelta(days=15)).item().strftime(
                "%d. %m. %Y.")
            
            # Widgets change
            rent_currently_val.configure(text=currently_rented)
            rent_book_title_combo.set(currently_rented)
            rent_book_title_combo.configure(state="disabled")
            rent_author_val.configure(text=rented_book_author)
            rent_book_copies_val.configure(text=copies_total)
            rent_available_val.configure(text=copies_available)
            rent_book_code_combo.set(code_book_rented_list[idx])
            rent_book_code_combo.configure(state="disabled")
            rent_deadline_val.configure(text=deadline_date)
            rent_rent_btn.configure(state="disabled")
            rent_return_btn.configure(state="normal")
        
        else:
            # Widgets change
            rent_currently_val.configure(text="-")
            rent_book_title_combo.set("")
            rent_book_title_combo.configure(state="readonly")
            rent_author_val.configure(text="-")
            rent_book_copies_val.configure(text="-")
            rent_available_val.configure(text="-")
            rent_book_code_combo.set("")
            rent_book_code_combo.configure(state="disabled")
            rent_deadline_val.configure(text="-")
            rent_rent_btn.configure(state="disabled")
            rent_return_btn.configure(state="disabled")

        # Reserved books Dataframe
        currently_reserved_df = reservations.reservations_df[
            reservations.reservations_df.reservation_date >
            (date.today() - timedelta(days=7))]
        
        # List of membership IDs, book codes and reservation dates
        currently_reserved_values_list = []
        for index, row in currently_reserved_df.iterrows():
            row_list = [row.membership_id, row.book_code, row.reservation_date]
            currently_reserved_values_list.append(row_list)

        rent_reserved_val.configure(text="-")
        rent_reserved_code_val.configure(text="-")
        rent_reservation_expires_val.configure(text="-")

        for lst in currently_reserved_values_list:
            if mem_id == lst[0]:
                reserved_code = lst[1]
                reserved_title = books.books_df.title[
                    books.books_df.book_code == reserved_code
                ].to_string(index=False)
                reservation_valid = (lst[2] + timedelta(days=7)
                                 ).strftime("%d. %m. %Y.")
                
                rent_reserved_val.configure(text=reserved_title)
                rent_reserved_code_val.configure(text=reserved_code)
                rent_reservation_expires_val.configure(text=reservation_valid)
        
    def rent_title_selected(event):
        """Changes that occur when selecting a book title."""
        
        title_name = rent_book_title_combo.get()
        author_name = titles.titles_df.author[
            titles.titles_df.title == title_name].to_string(index=False)
        rent_author_val.configure(text=author_name)
        
        # Total number of copies
        copies_total = books.books_df[books.books_df.title == title_name][
            "title"].count()
        rent_book_copies_val.configure(text=copies_total)
        
        # Number of available copies
        copies_available = books.books_df[
            (books.books_df.title == title_name) &
            (books.books_df.availability == "Available")
        ]["title"].count()
        
        rent_available_val.configure(text=copies_available)
        
        # Values for 'Book code' Combobox
        book_code_values = books.books_df.book_code[
            (books.books_df.title == title_name) &
            (books.books_df.availability == "Available")
        ].to_list()
        book_code_values.sort()
        rent_book_code_combo.configure(values=book_code_values)
        
        rent_book_code_combo.set("")
        rent_book_code_combo.configure(state="readonly")
        
        rent_rent_btn.configure(state="disabled")
    
    def rent_book_code_selected(event):
        """Changes that occur when selecting an available book code."""
        
        rent_rent_btn.configure(state="normal")
    
    def renting_apply():
        """Renting the selected book."""
        
        # Selected membership ID, book title and book code
        selected_id = rent_member_id_combo.get()
        selected_title = rent_book_title_combo.get()
        selected_code = rent_book_code_combo.get()
        
        # Enter data in the 'renting' table
        rental_sql = f"""
        INSERT INTO renting (membership_id, book_code, rental_date)
        VALUES ('{selected_id}', '{selected_code}', '{date.today()}');
        """
        renting.rent_execute(rental_sql)
        
        # Set book availability to 'Rented'
        book_availability_sql = f"""
        UPDATE books
        SET availability = 'Rented'
        WHERE book_code = '{selected_code}';
        """
        books.updating_books(book_availability_sql)
        
        # Updating widgets and necessery values for them
        available_books = books.books_df[
            (books.books_df.title == selected_title) &
            (books.books_df.availability == "Available")]["book_code"].count()
        
        deadline_value = (date.today() + timedelta(days=15)
                          ).strftime("%d. %m. %Y.")
        
        rent_currently_val.configure(text=selected_title)
        rent_reserved_val.configure(text="-")
        rent_reserved_code_val.configure(text="-")
        rent_reservation_expires_val.configure(text="-")
        rent_book_title_combo.configure(state="disabled")
        rent_available_val.configure(text=available_books)
        rent_book_code_combo.configure(state="disabled")
        rent_deadline_val.configure(text=deadline_value)
        rent_return_btn.configure(state="normal")
        rent_rent_btn.configure(state="disabled")

        # Successfully done
        success_title_text = language_text("Uspešno iznajmljivanje knjige",
                                           "Book rental successful")
        success_title_message = language_text(
            "Podaci o iznajmljenoj knjizi uspešno su uneseni u bazu podataka.",
            "The data about the rented book has been successfully entered "
            "into the database.")
        Messagebox.show_info(
            title=success_title_text,
            message=success_title_message,
            parent=book_rental_tl,
            alert=True
        )
    
    def returning_apply():
        """Returning the rented book."""
        
        # Selected membership ID
        member_id = rent_member_id_combo.get()
        
        # Rented ID of rented book for the selected member
        rented_id = int(renting.renting_df.rent_id[
            (renting.renting_df.membership_id == member_id) &
            (renting.renting_df.return_date.isnull())
        ].to_string(index=False))
        
        # Enter the return date
        rental_sql = f"""
        UPDATE renting
        SET return_date = '{date.today()}'
        WHERE rent_id = {rented_id};
        """
        renting.rent_execute(rental_sql)
        
        # Set book availability to 'Available'
        rented_book_code = renting.renting_df.book_code[
            renting.renting_df.rent_id == rented_id].to_string(index=False)
        
        book_availability_sql = f"""
        UPDATE books
        SET availability = 'Available'
        WHERE book_code = '{rented_book_code}';
        """
        books.updating_books(book_availability_sql)
        
        # Resetting all values
        rent_currently_val.configure(text="-")
        rent_book_title_combo.configure(state="readonly")
        rent_book_title_combo.set("")
        rent_author_val.configure(text="-")
        rent_book_copies_val.configure(text="-")
        rent_available_val.configure(text="-")
        rent_book_code_combo.set("")
        rent_deadline_val.configure(text="-")
        rent_return_btn.configure(state="disabled")
        
        # Successfully done
        success_title_text = language_text("Uspešno vraćenje knjige",
                                           "Book return successful")
        success_title_message = language_text(
            "Podaci o vraćanju knjige uspešno su ažurirani.",
            "The book return data has been successfully updated."
        )
        Messagebox.show_info(
            title=success_title_text,
            message=success_title_message,
            parent=book_rental_tl,
            alert=True
        )
    
    
    book_rental_title_text = language_text("Iznajmljivanje knjiga",
                                           "Book rental")
    book_rental_tl = ttk.Toplevel(title=book_rental_title_text)
    book_rental_tl.attributes("-topmost", "true")
    book_rental_tl.resizable(False, False)
    book_rental_tl.geometry("800x850")
    book_rental_tl.grab_set()
    
    # Labelframes texts
    rent_member_lf_text = language_text(" Podaci o članu ",
                                        " Member information ")
    rent_title_lf_text = language_text(" Podaci o naslovu ",
                                       " Title information ")
    
    # Frames
    book_rental_tl.grid_columnconfigure((0, 1), weight=1)
    
    rent_top_frm = ttk.Frame(book_rental_tl)
    rent_top_frm.grid(column=0, row=0, columnspan=2, padx=20, pady=20)
    
    rent_member_lf = ttk.LabelFrame(
        book_rental_tl,
        text=rent_member_lf_text,
        bootstyle="warning"
    )
    rent_member_lf.grid(column=0, row=1, padx=(20, 10), pady=10)
    
    rent_title_lf = ttk.LabelFrame(
        book_rental_tl,
        text=rent_title_lf_text,
        bootstyle="warning"
    )
    rent_title_lf.grid(column=1, row=1, padx=(10, 20), pady=10)
    
    rent_buttons_frm = ttk.Frame(book_rental_tl)
    rent_buttons_frm.grid(column=0, row=2, columnspan=2, padx=20, pady=20,
                          sticky="e")

    # Widgets in top (title) frame
    rent_main_text = language_text(" Biblioteka \"Vuk Karadžić\"",
                                    " Library \"Vuk Karadžić\"")
    rent_main_lbl = ttk.Label(
        rent_top_frm,
        text=rent_main_text,
        font=("Calibri", 36, "bold"),
        image=logo_smaller,
        compound="left",
        anchor="center",
        bootstyle="warning"
    )
    rent_main_lbl.pack(expand=True, fill="x")

    current_date = date.today().strftime("%d. %m. %Y.")
    librarian_logged_in = logged_in_librarian()
    rent_librarian_text = language_text(
        f"Bibliotekar: {librarian_logged_in}, datum: {current_date}",
        f"Librarian: {librarian_logged_in}, date: {current_date}"
    )
    rent_librarian_lbl = ttk.Label(
        rent_top_frm,
        text=rent_librarian_text,
        font=("Calibri", 16),
        bootstyle="danger"
    )
    rent_librarian_lbl.pack(pady=10)

    rent_title_lbl = ttk.Label(
        rent_top_frm,
        text=book_rental_title_text.upper(),
        font=("Calibri", 28, "bold"),
        anchor="center",
        bootstyle="warning"
    )
    rent_title_lbl.pack(expand=True, fill="x", pady=(0, 10))

    # Widgets in member labelframe
    rent_member_id_lbl_text = language_text("Broj članske karte:",
                                            "Membership ID:")
    rent_member_id_lbl = ttk.Label(
        rent_member_lf,
        text=rent_member_id_lbl_text,
        font=("Calibri", 14),
        bootstyle="light"
    )
    rent_member_id_lbl.grid(column=0, row=0, padx=30, pady=(10, 0),
                            sticky="w")
    
    rent_member_id_values = members.membership_ids_sorted()
    rent_member_id_combo = ttk.Combobox(
        rent_member_lf,
        width=42,
        values=rent_member_id_values,
        state="readonly",
        bootstyle="light"
    )
    rent_member_id_combo.grid(column=0, row=1, padx=30, pady=(0, 10),
                              sticky="w")
    
    # Bind this Combobox
    rent_member_id_combo.bind("<<ComboboxSelected>>", membership_id_selected)

    rent_member_name_lbl_text = language_text("Ime člana:", "Member name:")
    rent_member_name_lbl = ttk.Label(
        rent_member_lf,
        text=rent_member_name_lbl_text,
        font=("Calibri", 14),
        bootstyle="light"
    )
    rent_member_name_lbl.grid(column=0, row=2, padx=30, pady=(10, 0),
                              sticky="w")
    
    rent_member_name_val = ttk.Label(
        rent_member_lf,
        text="-",
        font=("Calibri", 14),
        bootstyle="warning"
        
    )
    rent_member_name_val.grid(column=0, row=3, padx=30, pady=(0, 10),
                              sticky="w")

    rent_currently_lbl_text = language_text("Trenutno iznajmljeno:",
                                            "Currently rented:")
    rent_currently_lbl = ttk.Label(
        rent_member_lf,
        text=rent_currently_lbl_text,
        font=("Calibri", 14),
        bootstyle="light"
    )
    rent_currently_lbl.grid(column=0, row=4, padx=30, pady=(10, 0), sticky="w")

    rent_currently_val = ttk.Label(
        rent_member_lf,
        text="-",
        font=("Calibri", 14),
        bootstyle="warning"
    )
    rent_currently_val.grid(column=0, row=5, padx=30, pady=(0, 10), sticky="w")

    rent_reserved_lbl_text = language_text("Rezervisano:", "Reserved:")
    rent_reserved_lbl = ttk.Label(
        rent_member_lf,
        text=rent_reserved_lbl_text,
        font=("Calibri", 14),
        bootstyle="light"
    )
    rent_reserved_lbl.grid(column=0, row=6, padx=30, pady=(10, 0),
                              sticky="w")
    
    rent_reserved_val = ttk.Label(
        rent_member_lf,
        text="-",
        font=("Calibri", 14),
        bootstyle="warning"
        
    )
    rent_reserved_val.grid(column=0, row=7, padx=30, pady=(0, 10), sticky="w")

    rent_reserved_code_lbl_text = language_text("Šifra rezervisane knjige:",
                                                "Reserved book code:")
    rent_reserved_code_lbl = ttk.Label(
        rent_member_lf,
        text=rent_reserved_code_lbl_text,
        font=("Calibri", 14),
        bootstyle="light"
    )
    rent_reserved_code_lbl.grid(column=0, row=8, padx=30, pady=(10, 0),
                                sticky="w")

    rent_reserved_code_val = ttk.Label(
        rent_member_lf,
        text="-",
        font=("Calibri", 14),
        bootstyle="warning"
    )
    rent_reserved_code_val.grid(column=0, row=9, padx=30, pady=(0, 10),
                                sticky="w")

    rent_reservation_expires_lbl_text = language_text("Rezervacija ističe:",
                                                      "Reservation expires:")
    rent_reservation_expires_lbl = ttk.Label(
        rent_member_lf,
        text=rent_reservation_expires_lbl_text,
        font=("Calibri", 14),
        bootstyle="light"
    )
    rent_reservation_expires_lbl.grid(column=0, row=10, padx=30, pady=(10, 0),
                                      sticky="w")

    rent_reservation_expires_val = ttk.Label(
        rent_member_lf,
        text="-",
        font=("Calibri", 14),
        bootstyle="warning"
    )
    rent_reservation_expires_val.grid(column=0, row=11, padx=30, pady=(0, 20),
                                      sticky="w")

    # Widgets in title labelframe
    rent_book_title_lbl_text = language_text("Naslov knjige:", "Book title:")
    rent_book_title_lbl = ttk.Label(
        rent_title_lf,
        text=rent_book_title_lbl_text,
        font=("Calibri", 14),
        bootstyle="light"
    )
    rent_book_title_lbl.grid(column=0, row=0, padx=30, pady=(10, 0),
                            sticky="w")
    
    book_title_values = titles.df_list_sort_by_title(titles.titles_df)
    rent_book_title_combo = ttk.Combobox(
        rent_title_lf,
        width=42,
        values=book_title_values,
        state="disabled",
        bootstyle="light"
    )
    rent_book_title_combo.grid(column=0, row=1, padx=30, pady=(0, 10),
                              sticky="w")
    
    # Bind this Combobox
    rent_book_title_combo.bind("<<ComboboxSelected>>", rent_title_selected)
    
    rent_author_lbl_text = language_text("Ime autora:", "Author Name:")
    rent_author_lbl = ttk.Label(
        rent_title_lf,
        text=rent_author_lbl_text,
        font=("Calibri", 14),
        bootstyle="light"
    )
    rent_author_lbl.grid(column=0, row=2, padx=30, pady=(10, 0), sticky="w")
    
    rent_author_val = ttk.Label(
        rent_title_lf, text="-",
        font=("Calibri", 14),
        bootstyle="warning"
    )
    rent_author_val.grid(column=0, row=3, padx=30, pady=(0, 10), sticky="w")
    
    rent_book_copies_lbl_text = language_text("Ukupno primeraka:",
                                              "Total copies:")
    rent_book_copies_lbl = ttk.Label(
        rent_title_lf,
        text=rent_book_copies_lbl_text,
        font=("Calibri", 14),
        bootstyle="light"
    )
    rent_book_copies_lbl.grid(column=0, row=4, padx=30, pady=(10, 0),
                              sticky="w")
    
    rent_book_copies_val = ttk.Label(
        rent_title_lf,
        text="-",
        font=("Calibri", 14),
        bootstyle="warning"
    )
    rent_book_copies_val.grid(column=0, row=5, padx=30, pady=(0, 10),
                              sticky="w")
    
    rent_available_lbl_text = language_text("Dostupno primeraka:",
                                            "Copies available:")
    rent_available_lbl = ttk.Label(
        rent_title_lf,
        text=rent_available_lbl_text,
        font=("Calibri", 14),
        bootstyle="light"
    )
    rent_available_lbl.grid(column=0, row=6, padx=30, pady=(10, 0), sticky="w")
    
    rent_available_val = ttk.Label(
        rent_title_lf,
        text="-",
        font=("Calibri", 14),
        bootstyle="warning"
    )
    rent_available_val.grid(column=0, row=7, padx=30, pady=(0, 10), sticky="w")
    
    rent_book_code_lbl_text = language_text("Šifra knjige:", "Book code:")
    rent_book_code_lbl = ttk.Label(
        rent_title_lf,
        text=rent_book_code_lbl_text,
        font=("Calibri", 14),
        bootstyle="light"
    )
    rent_book_code_lbl.grid(column=0, row=8, padx=30, pady=(10, 0), sticky="w")
    
    rent_book_code_combo = ttk.Combobox(
        rent_title_lf,
        width=42,
        state="disabled",
        bootstyle="light"
    )
    rent_book_code_combo.grid(column=0, row=9, padx=30, pady=(0, 10),
                              sticky="w")
    
    # Bind this Combobox
    rent_book_code_combo.bind("<<ComboboxSelected>>", rent_book_code_selected)

    rent_deadline_lbl_text = language_text("Rok za vraćanje:",
                                           "Return deadline:")
    rent_deadline_lbl = ttk.Label(
        rent_title_lf,
        text=rent_deadline_lbl_text,
        font=("Calibri", 14),
        bootstyle="light"
    )
    rent_deadline_lbl.grid(column=0, row=10, padx=30, pady=(10, 0), sticky="w")

    rent_deadline_val = ttk.Label(
        rent_title_lf,
        text="-",
        font=("Calibri", 14),
        bootstyle="warning"
    )
    rent_deadline_val.grid(column=0, row=11, padx=30, pady=(0, 20), sticky="w")

    # Widgets in buttons frame
    rent_close_btn_text = language_text("Zatvori", "Close")
    rent_close_btn = ttk.Button(
        rent_buttons_frm,
        width=10,
        text=rent_close_btn_text,
        style="big.dark.TButton",
        command=book_rental_tl.destroy
    )
    rent_close_btn.pack(side="right", expand=True, fill="x", padx=10, pady=10)
    
    rent_return_btn_text = language_text("Vrati", "Return")
    rent_return_btn = ttk.Button(
        rent_buttons_frm,
        width=10,
        text=rent_return_btn_text,
        style="big.dark.TButton",
        state="disabled",
        command=returning_apply
    )
    rent_return_btn.pack(side="right", expand=True, fill="x", padx=10, pady=10)
    
    rent_rent_btn_text = language_text("Iznajmi", "Rent")
    rent_rent_btn = ttk.Button(
        rent_buttons_frm,
        width=10,
        text=rent_rent_btn_text,
        style="big.dark.TButton",
        state="disabled",
        command=renting_apply
    )
    rent_rent_btn.pack(side="right", expand=True, fill="x", padx=10, pady=10)


def statistics():
    """Various reports and charts."""
    
    # Dataframe of 'renting' table without currently rented copies
    no_rented_df = renting.renting_df.dropna()
    delay_member_ids = set(no_rented_df.membership_id[
            no_rented_df.rental_date + timedelta(days=15) <
            no_rented_df.return_date].to_list())
    
    def delays_data():
        """List of lists of delays, member ids and member names."""

        delay_members_data = []
        for mem_id in delay_member_ids:
            f_name = members.members_df.first_name[
                members.members_df.membership_id == mem_id].to_string(
                index=False)
            l_name = members.members_df.last_name[
                members.members_df.membership_id == mem_id].to_string(
                index=False)
    
            full_name = f"{f_name} {l_name}"
    
            delay_times = not_on_time(mem_id)
    
            delays_id_name = [delay_times, mem_id, full_name]
            delay_members_data.append(delays_id_name)

        delay_members_data_sorted = sorted(delay_members_data, reverse=True)
        
        return delay_members_data_sorted
    
    def no_delay():
        """List of members who have never been late in returning books."""
        
        all_member_ids = set(members.members_df.membership_id.to_list())
        no_delay_ids = list(all_member_ids - delay_member_ids)

        no_delay_members = []
        for mem_id in no_delay_ids:
            f_name = members.members_df.first_name[
                members.members_df.membership_id == mem_id
            ].to_string(index=False)
            l_name = members.members_df.last_name[
                members.members_df.membership_id == mem_id
            ].to_string(index=False)
            
            full_name = f"{f_name} {l_name}"
            name_and_id_list = [mem_id, full_name]
            no_delay_members.append(name_and_id_list)
            
        no_delay_members_sorted = sorted(no_delay_members)
        
        # Widgets
        no_delay_tl_text = language_text(button_texts[0][0],
                                         button_texts[0][1])
        no_delay_tl = ttk.Toplevel(title=no_delay_tl_text)
        no_delay_tl.attributes("-topmost", "true")
        no_delay_tl.resizable(False, False)
        no_delay_tl.geometry("600x700")
        no_delay_tl.grab_set()
        
        no_delay_sf = ScrolledFrame(no_delay_tl, autohide=True)
        no_delay_sf.pack(expand=True, fill="both")
        
        no_delay_title_lbl_text = no_delay_tl_text.upper()
        no_delay_title_lbl = ttk.Label(
            no_delay_sf,
            text=no_delay_title_lbl_text,
            font=("Calibri", 28, "bold"),
            anchor="center",
            bootstyle="warning"
        )
        no_delay_title_lbl.pack(expand=True, fill="x", pady=(30,0))
        
        no_delay_info_lbl_text = language_text(info_texts[0][0],
                                               info_texts[0][1])
        no_delay_info_lbl = ttk.Label(
            no_delay_sf,
            text=no_delay_info_lbl_text,
            font=("Calibri", 16),
            anchor="center",
            bootstyle="light"
        )
        no_delay_info_lbl.pack(expand=True, fill="x", pady=(10, 30))
        
        no_delay_data_frm = ttk.Frame(no_delay_sf)
        no_delay_data_frm.pack(fill="both", padx=30, pady=10)
        no_delay_data_frm.grid_columnconfigure((0, 1), weight=1)
        
        no_delay_mem_id_lbl_text = language_text("Članski broj",
                                                 "Membership ID")
        no_delay_membership_id_lbl = ttk.Label(
            no_delay_data_frm,
            text=no_delay_mem_id_lbl_text,
            font=("Calibri", 16),
            bootstyle="light"
        )
        no_delay_membership_id_lbl.grid(column=0, row=0, padx=(50, 20),
                                        pady=(0, 10))
        
        no_delay_name_lbl_text = language_text("Ime člana", "Member name")
        no_delay_name_lbl = ttk.Label(
            no_delay_data_frm,
            text=no_delay_name_lbl_text,
            font=("Calibri", 16),
            bootstyle="light"
        )
        no_delay_name_lbl.grid(column=1, row=0, padx=(20, 50), pady=(0, 10))
        
        for i in range(len(no_delay_members_sorted)):
            ttk.Label(
                no_delay_data_frm,
                text=no_delay_members_sorted[i][0],
                font=("Calibri", 16)
            ).grid(column=0, row=i+1, padx=(50, 20), pady=(0, 10))
            
            ttk.Label(
                no_delay_data_frm,
                text=no_delay_members_sorted[i][1],
                font=("Calibri", 16),
                bootstyle="warning"
            ).grid(column=1, row=i+1, padx=(20, 50), pady=(0, 10))
        
        no_delay_btn_text = language_text("Zatvori", "Close")
        no_delay_close_btn = ttk.Button(
            no_delay_sf,
            text=no_delay_btn_text,
            width=10,
            style="big.dark.TButton",
            command=no_delay_tl.destroy
        )
        no_delay_close_btn.pack(side="right", padx=60, pady=30)
    
    def delay_list():
        """List of members who did not return books on time."""
        
        delays_ids_names = delays_data()
        
        # Widgets
        delay_list_tl_text = language_text(button_texts[1][0],
                                           button_texts[1][1])
        delay_list_tl = ttk.Toplevel(title=delay_list_tl_text)
        delay_list_tl.attributes("-topmost", "true")
        delay_list_tl.resizable(False, False)
        delay_list_tl.geometry("800x700")
        delay_list_tl.grab_set()
        
        delay_list_sf = ScrolledFrame(delay_list_tl, autohide=True)
        delay_list_sf.pack(expand=True, fill="both")
        
        delay_list_title_lbl_text = language_text(
            "KAŠNJENJE U VRAĆANJU KNJIGA - SPISAK",
            "DELAY IN RETURNING BOOKS - LIST"
        )
        delay_list_title_lbl = ttk.Label(
            delay_list_sf,
            text=delay_list_title_lbl_text,
            font=("Calibri", 28, "bold"),
            anchor="center",
            bootstyle="warning"
        )
        delay_list_title_lbl.pack(expand=True, fill="x", pady=(30, 0))
        
        delay_list_info_lbl_text = language_text(
            "Članovi koji nisu vraćali knjige na vreme i broj kašnjenja.",
            "Members who did not return books on time and number of delays."
        )
        delay_list_info_lbl = ttk.Label(
            delay_list_sf,
            text=delay_list_info_lbl_text,
            font=("Calibri", 16),
            anchor="center",
            bootstyle="light"
        )
        delay_list_info_lbl.pack(expand=True, fill="x", pady=(10, 30))

        delay_list_data_frm = ttk.Frame(delay_list_sf)
        delay_list_data_frm.pack(fill="both", padx=30, pady=10)
        delay_list_data_frm.grid_columnconfigure((0, 1, 2), weight=1)

        delay_list_mem_id_lbl_text = language_text("Članski broj",
                                                   "Membership ID")
        delay_list_membership_id_lbl = ttk.Label(
            delay_list_data_frm,
            text=delay_list_mem_id_lbl_text,
            font=("Calibri", 16),
            bootstyle="light"
        )
        delay_list_membership_id_lbl.grid(column=0, row=0, padx=(50, 20),
                                          pady=(0, 10))

        delay_list_name_lbl_text = language_text("Ime člana", "Member name")
        delay_list_name_lbl = ttk.Label(
            delay_list_data_frm,
            text=delay_list_name_lbl_text,
            font=("Calibri", 16),
            bootstyle="light"
        )
        delay_list_name_lbl.grid(column=1, row=0, padx=20, pady=(0, 10))

        delay_list_delays_lbl_text = language_text("Kašnjenja", "Delays")
        delay_list_delays_lbl = ttk.Label(
            delay_list_data_frm,
            text=delay_list_delays_lbl_text,
            font=("Calibri", 16),
            bootstyle="light"
        )
        delay_list_delays_lbl.grid(column=2, row=0, padx=(20, 50),
                                   pady=(0, 10))

        for i in range(len(delays_ids_names)):
            ttk.Label(
                delay_list_data_frm,
                text=delays_ids_names[i][1],
                font=("Calibri", 16)
            ).grid(column=0, row=i+1, padx=(50, 20), pady=(0, 10))
    
            ttk.Label(
                delay_list_data_frm,
                text=delays_ids_names[i][2],
                font=("Calibri", 16),
                bootstyle="warning"
            ).grid(column=1, row=i+1, padx=20, pady=(0, 10))

            ttk.Label(
                delay_list_data_frm,
                text=delays_ids_names[i][0],
                font=("Calibri", 16)
            ).grid(column=2, row=i+1, padx=(20, 50), pady=(0, 10))

        delay_list_btn_text = language_text("Zatvori", "Close")
        delay_list_close_btn = ttk.Button(
            delay_list_sf,
            text=delay_list_btn_text,
            width=10,
            style="big.dark.TButton",
            command=delay_list_tl.destroy
        )
        delay_list_close_btn.pack(side="right", padx=60, pady=30)
    
    def delay_chart():
        """Chart of members who did not return books on time (first 10)."""
        
        first_ten_delay_members = delays_data()[:10]
        
        # Title and axes texts
        delay_members_title_text = language_text(
            "DESET ČLANOVA KOJI SU NAJVIŠE KASNILI S VRAĆANJEM KNJIGA",
            "TEN MEMBERS WHO WERE MOST LATE IN RETURNING THEIR BOOKS"
        )
        
        x_axis_text = language_text("Broj kašnjenja", "Number of delays")
        y_axis_text = language_text("Ime člana", "Member name")
        
        # Axes values
        member_names = []
        delays = []
        for lst in first_ten_delay_members:
            member_names.append(lst[2])
            delays.append(lst[0])
        
        # The most delays at the top
        member_names.reverse()
        delays.reverse()
        
        # Horizontal bar chart
        fig, ax = plt.subplots(figsize=(16, 8), facecolor="#1b1b1b")
        
        ax.set_facecolor("#1b1b1b")
        ax.spines["bottom"].set_color("lightgrey")
        ax.spines["top"].set_color("lightgrey")
        ax.spines["left"].set_color("lightgrey")
        ax.spines["right"].set_color("lightgrey")
        
        plt.xticks(color="lightgrey")
        plt.yticks(color="lightgrey", rotation=30)
        ax.tick_params(axis="x", colors="lightgrey")
        ax.tick_params(axis="y", colors="lightgrey")
        
        ax.barh(member_names, delays, 0.5, color="#507d2a")
        plt.title(
            delay_members_title_text,
            fontdict={"family": "Calibri", "color": "#665d1e", "size": 22,
                      "weight": "bold"},
            pad=30
        )
        plt.xlabel(
            x_axis_text,
            fontdict={"family": "Calibri", "color": "#665d1e", "size": 16,
                      "weight": "bold"},
            labelpad=20
        )
        plt.ylabel(
            y_axis_text,
            fontdict={"family": "Calibri", "color": "#665d1e", "size": 16,
                      "weight": "bold"},
            labelpad=20
        )
        plt.grid()
        plt.subplots_adjust(left=0.16, right=0.95)
        
        plt.show()
    
    def delay_titles():
        """Chart of titles that were not returned on time (first 10)."""
        
        # Delays dataframe
        delays_df = no_rented_df[no_rented_df.rental_date + timedelta(days=15)
                                 < no_rented_df.return_date]
        
        # Books that were returned late
        delay_book_codes = list(set(delays_df.book_code.to_list()))
        
        # Sorted list of how many times some book was returned late
        codes_delay_list = []
        for code in delay_book_codes:
            number_of_delays = delays_df[delays_df.book_code == code][
                "book_code"].count()
            codes_delay_list.append([number_of_delays, code])
        codes_delay_list.sort(reverse=True)
        
        # All titles
        all_titles_list = titles.titles_df.title.to_list()
        
        # Sorted list of how many times some title was returned late
        titles_delay_list = []
        for ttl in all_titles_list:
            title_delays = 0
            for lst in codes_delay_list:
                if books.books_df.title[
                    books.books_df.book_code == lst[1]
                ].to_string(index=False) == ttl:
                    title_delays += lst[0]
            titles_delay_list.append([title_delays, ttl])
        titles_delay_list.sort(reverse=True)
        
        first_ten_delay_titles = titles_delay_list[:10]
        
        # Chart title and axes texts
        delay_titles_title_text = language_text(
            "DESET NASLOVA S KOJIMA SE NAJVIŠE KASNILO",
            "THE TEN MOST DELAYED TITLES"
        )
        
        x_axis_text = language_text("Broj kašnjenja", "Number of delays")
        y_axis_text = language_text("Naslov knjige", "Book title")
        
        # Axes values
        title_names = []
        delays = []
        for lst in first_ten_delay_titles:
            title_names.append(lst[1])
            delays.append(lst[0])
        
        # The most delays at the top
        title_names.reverse()
        delays.reverse()
        
        # Horizontal bar chart
        fig, ax = plt.subplots(figsize=(16, 8), facecolor="#1b1b1b")

        ax.set_facecolor("#1b1b1b")
        ax.spines["bottom"].set_color("lightgrey")
        ax.spines["top"].set_color("lightgrey")
        ax.spines["left"].set_color("lightgrey")
        ax.spines["right"].set_color("lightgrey")

        plt.xticks(color="lightgrey")
        plt.yticks(color="lightgrey", rotation=30)
        ax.tick_params(axis="x", colors="lightgrey")
        ax.tick_params(axis="y", colors="lightgrey")

        ax.barh(title_names, delays, 0.5, color="#960018")
        plt.title(delay_titles_title_text,
            fontdict={"family": "Calibri", "color": "#8b0000", "size": 22,
                      "weight": "bold"}, pad=30)
        plt.xlabel(x_axis_text,
            fontdict={"family": "Calibri", "color": "#8b0000", "size": 16,
                      "weight": "bold"}, labelpad=20)
        plt.ylabel(y_axis_text,
            fontdict={"family": "Calibri", "color": "#8b0000", "size": 16,
                      "weight": "bold"}, labelpad=20)
        plt.grid()
        plt.subplots_adjust(left=0.17, right=0.96)

        plt.show()
    
    def longest_member():
        """Members with the longest membership in months (first 10)."""
        
        data_lists = []
        for index, row in members.members_df.iterrows():
            row_list = [row.first_name, row.last_name, row.membership_date]
            data_lists.append(row_list)
        
        months_name_lists = []
        for i in range(len(data_lists)):
            f_name = data_lists[i][0]
            l_name = data_lists[i][1]
            mem_date = data_lists[i][2]
            
            # Duration of membership
            duration = 12 * (date.today().year - mem_date.year) + (
                date.today().month - mem_date.month)
            months_name_lists.append([duration, f"{f_name} {l_name}"])
        
        months_name_lists.sort(reverse=True)
        
        first_ten_longest = months_name_lists[:10]
        
        # Chart title and axes texts
        longest_title_text = language_text(
            "DESET ČLANOVA S NAJDUŽIM ČLANSTVOM (u mesecima)",
            "TEN MEMBERS WITH THE LONGEST MEMBERSHIP (in months)"
        )
        
        x_axis_text = language_text("Ime člana", "Member name")
        y_axis_text = language_text("Dužina članstva",
                                    "Duration of membership")
        
        # Axes values
        member_names = []
        duration_in_months = []
        for lst in first_ten_longest:
            member_names.append(lst[1])
            duration_in_months.append(lst[0])
        
        # Plot
        fig, ax = plt.subplots(figsize=(16, 9), facecolor="#1b1b1b")

        ax.set_facecolor("#1b1b1b")
        ax.spines["bottom"].set_color("lightgrey")
        ax.spines["top"].set_color("lightgrey")
        ax.spines["left"].set_color("lightgrey")
        ax.spines["right"].set_color("lightgrey")

        plt.xticks(color="lightgrey", rotation=75)
        plt.yticks(color="lightgrey")
        ax.tick_params(axis="x", colors="lightgrey")
        ax.tick_params(axis="y", colors="lightgrey")
        
        ax.plot(
            member_names,
            duration_in_months,
            marker="o",
            color="#ee82ee",
            markerfacecolor="#8b008b",
            linestyle="-."
        )
        plt.title(
            longest_title_text,
            fontdict={"family": "Calibri", "color": "#a50b5e",
                      "size": 22, "weight": "bold"},
            pad=30
        )
        plt.xlabel(
            x_axis_text,
            fontdict={"family": "Calibri", "color": "#a50b5e",
                      "size": 16, "weight": "bold"},
            labelpad=30
        )
        plt.ylabel(
            y_axis_text,
            fontdict={"family": "Calibri", "color": "#a50b5e",
                      "size": 16, "weight": "bold"},
            labelpad=30
        )
        
        for x, y in zip(member_names, duration_in_months):
            label = y
            plt.annotate(label, (x, y), textcoords="offset points",
                         xytext=(0, 10), ha="center", color="#ee82ee")
        
        plt.subplots_adjust(left=0.12, right=0.93, bottom=0.26)
        
        plt.show()
    
    def most_rentals():
        """Members with the most rentals (first 10)."""
        
        id_name_surname_list = []
        for index, row in members.members_df.iterrows():
            row_list = [row.first_name, row.last_name, row.membership_id]
            id_name_surname_list.append(row_list)
        
        renting_name_list = []
        for lst in id_name_surname_list:
            rental_num = renting.renting_df[
                renting.renting_df.membership_id == lst[2]
            ]["rental_date"].count()
            f_name = lst[0]
            l_name = lst[1]
            
            renting_name_list.append([rental_num, f"{f_name} {l_name}"])
        
        renting_name_list.sort(reverse=True)
        
        first_ten_most_rented = renting_name_list[:10]

        # Chart title and axes texts
        most_rented_title_text = language_text(
            "DESET ČLANOVA KOJI SU NAJVIŠE IZNAJMLJIVALI",
            "TEN MEMBERS WHO RENT THE MOST"
        )
        
        x_axis_text = language_text("Ime člana", "Member name")
        y_axis_text = language_text("Broj iznajmljivanja", "Rental number")
        
        # Axes values
        member_names = []
        rental_numbers = []
        for lst in first_ten_most_rented:
            member_names.append(lst[1])
            rental_numbers.append(lst[0])
        
        # Plot
        fig, ax = plt.subplots(figsize=(16, 9), facecolor="#1b1b1b")

        ax.set_facecolor("#1b1b1b")
        ax.spines["bottom"].set_color("lightgrey")
        ax.spines["top"].set_color("lightgrey")
        ax.spines["left"].set_color("lightgrey")
        ax.spines["right"].set_color("lightgrey")

        plt.xticks(color="lightgrey", rotation=75)
        plt.yticks(color="lightgrey")
        ax.tick_params(axis="x", colors="lightgrey")
        ax.tick_params(axis="y", colors="lightgrey")

        ax.plot(
            member_names, rental_numbers,
            marker="o",
            color="#9bddff",
            markerfacecolor="#008b8b",
            linestyle=":"
        )
        plt.title(
            most_rented_title_text,
            fontdict={"family": "Calibri", "color": "#004f98", "size": 22,
                      "weight": "bold"},
            pad=30
        )
        plt.xlabel(
            x_axis_text,
            fontdict={"family": "Calibri", "color": "#004f98", "size": 16,
                      "weight": "bold"},
            labelpad=30
        )
        plt.ylabel(
            y_axis_text,
            fontdict={"family": "Calibri", "color": "#004f98", "size": 16,
                      "weight": "bold"},
            labelpad=30
        )

        for x, y in zip(member_names, rental_numbers):
            label = y
            plt.annotate(label, (x, y), textcoords="offset points",
                         xytext=(0, 10), ha="center", color="#9bddff")

        plt.subplots_adjust(left=0.1, right=0.95, bottom=0.28)

        plt.show()
    
    def titles_by_genre():
        """Percentage of titles by genre."""
        
        genre_number_list = []
        for i in range(len(GENRES)):
            genre_name = GENRES[i][1]
            titles_num = titles.titles_df[
                titles.titles_df.genre == genre_name]["genre"].count()
            genre_number_list.append([titles_num, genre_name])
        
        genre_number_list.sort(reverse=True)
        
        # Chart title text
        genre_number_title_text = language_text(
            "Procentulano naslova po žanru",
            "Percentage of titles by genre"
        ).upper()
        
        # Values
        title_numbers = []
        genres = []
        for lst in genre_number_list:
            num = lst[0]
            if language == "srpski":
                for i in range(len(GENRES)):
                    if lst[1] == GENRES[i][1]:
                        gen = GENRES[i][0]
            else:
                gen = lst[1]
            title_numbers.append(num)
            genres.append(gen)
        
        # Chart
        fig, ax = plt.subplots(figsize=(8, 8), facecolor="#c19a6b")
        
        ax.set_facecolor("#c19a6b")
        matplotlib.rcParams["text.color"] = "#062a78"
        
        ax.pie(
            title_numbers,
            labels=genres,
            colors=sns.color_palette("YlOrBr"),
            autopct="%.2f%%",
            explode=[0.12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        )
        plt.title(
            label=genre_number_title_text,
            fontdict={"family": "Calibri", "color": "#062a78", "size": 22,
                      "weight": "bold"},
            pad=30
        )
        
        plt.show()
    
    def copies_by_genre():
        """Percentage of copies by genre."""
        
        # List of all title names
        all_titles_list = titles.titles_df.title.to_list()
        
        # List of pairs: copies number and title name
        copies_title_list = []
        for ttl in all_titles_list:
            copies_per_title = books.books_df[books.books_df.title == ttl][
                "title"].count()
            copies_title_list.append([copies_per_title, ttl])
        
        # List of genres and their titles
        genre_titles_list = []
        for i in range(len(GENRES)):
            genre_titles = titles.titles_df.title[
                titles.titles_df.genre == GENRES[i][1]].to_list()
            genre_titles_list.append([GENRES[i][1], genre_titles])
        
        # List of book copies by genre
        copies_genre_list = []
        for lst in genre_titles_list:
            counter = 0
            for pair in copies_title_list:
                if pair[1] in lst[1]:
                    counter += pair[0]
            copies_genre_list.append([counter, lst[0]])
        
        copies_genre_list.sort(reverse=True)
        
        # Chart title text
        copy_number_genre_text = language_text(
            "Procentualno primeraka po žanru",
            "Percentage of copies by genre"
        ).upper()
        
        # Values
        copy_numbers = []
        genres = []
        for lst in copies_genre_list:
            num = lst[0]
            if language == "srpski":
                for i in range(len(GENRES)):
                    if lst[1] == GENRES[i][1]:
                        gen = GENRES[i][0]
            else:
                gen = lst[1]
            copy_numbers.append(num)
            genres.append(gen)
            
        # Chart
        fig, ax = plt.subplots(figsize=(8, 8), facecolor="#8fbc8f")

        ax.set_facecolor("#8fbc8f")
        matplotlib.rcParams["text.color"] = "#4e1609"

        ax.pie(
            copy_numbers,
            labels=genres,
            colors=sns.color_palette("Blues"),
            autopct="%.2f%%",
            explode=[0.12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        )
        plt.title(
            label=copy_number_genre_text,
            fontdict={"family": "Calibri", "color": "#4e1609", "size": 22,
                      "weight": "bold"},
            pad=30
        )

        plt.show()
    
    
    stat_main_title_text = language_text("Statistika", "Statistics")
    statistics_tl = ttk.Toplevel(title=stat_main_title_text)
    statistics_tl.resizable(False, False)
    statistics_tl.grab_set()
    
    # Frames
    stat_top_frm = ttk.Frame(statistics_tl)
    stat_top_frm.pack(fill="x", padx=20, pady=20)
    
    stat_options_frm = ttk.Frame(statistics_tl)
    stat_options_frm.pack(fill="x", padx=40, pady=20)
    
    # Top frame widgets
    stat_main_text = language_text(" Biblioteka \"Vuk Karadžić\"",
                                   " Library \"Vuk Karadžić\"")
    stat_main_lbl = ttk.Label(
        stat_top_frm,
        text=stat_main_text,
        font=("Calibri", 36, "bold"),
        image=logo_smaller,
        compound="left",
        anchor="center",
        bootstyle="warning"
    )
    stat_main_lbl.pack(expand=True, fill="x")
    
    librarian = logged_in_librarian()
    stat_librarian_text = language_text(f"Bibliotekar: {librarian}",
                                        f"Librarian: {librarian}")
    stat_librarian_lbl = ttk.Label(
        stat_top_frm,
        text=stat_librarian_text,
        font=("Calibri", 16),
        bootstyle="danger"
    )
    stat_librarian_lbl.pack(pady=10)
    
    stat_title_lbl = ttk.Label(
        stat_top_frm,
        text=stat_main_title_text.upper(),
        font=("Calibri", 28, "bold"),
        anchor="center",
        bootstyle="warning"
    )
    stat_title_lbl.pack(expand=True, fill="x", pady=(0, 20))
    
    # Function list
    function_list = [no_delay, delay_list, delay_chart, delay_titles,
                     longest_member, most_rentals, titles_by_genre,
                     copies_by_genre]
    
    # Text for widgets in option frame
    button_texts = [
        ["Bez kašnjenja", "No delay"],
        ["Kašnjenje - spisak", "Delay - list"],
        ["Kašnjenje - grafik", "Delay - chart"],
        ["Kašnjenje - naslovi", "Delay - titles"],
        ["Najduže članstvo", "Longest membership"],
        ["Najviše iznajmljivanja", "Most rentals"],
        ["Naslova po žanru", "Titles by genre"],
        ["Primeraka po žanru", "Copies by genre"]
    ]
    
    info_texts = [
        ["Članovi koji nikada nisu kasnili s vraćanjem knjiga.",
         "Members who have never been late in returning books."],
        ["Članovi koji nisu vraćali knjige na vreme.",
         "Members who did not return books on time."],
        ["Grafik članova koji nisu vraćali knjige na vreme.",
         "Chart of members who did not return books on time."],
        ["Grafik naslova koji nisu vraćani na vreme.",
         "Chart of titles that were not returned on time."],
        ["Članovi koji imaju najduže članstvo.",
         "Members with the longest membership."],
        ["Članovi s najviše iznajmljivanja.",
         "Members with the most rentals."],
        ["Procentulano naslova po žanru.",
         "Percentage of titles by genre."],
        ["Procentualno primeraka po žanru.",
         "Percentage of copies by genre."]
    ]
    
    # Options frame widgets
    for i in range(len(button_texts)):
        ttk.Button(
            stat_options_frm,
            text=language_text(button_texts[i][0], button_texts[i][1]),
            width=20,
            style="big.dark.TButton",
            command=function_list[i]
        ).grid(column=0, row=i, padx=20, pady=10)
        
        ttk.Label(
            stat_options_frm,
            text=language_text(info_texts[i][0], info_texts[i][1]),
            font=("Calibri", 16),
            bootstyle="light"
        ).grid(column=1, row=i, padx=20, pady=10, sticky="w")
    
    # Close button
    stat_close_btn_text = language_text("Zatvori", "Close")
    stat_close_btn = ttk.Button(
        statistics_tl,
        text=stat_close_btn_text,
        width=10,
        style="big.dark.TButton",
        command=statistics_tl.destroy
    )
    stat_close_btn.pack(side="right", padx=60, pady=(20, 30))


# Top frame - choose language and login
top_frm = ttk.Frame(root)
top_frm.pack(expand=True, fill="x", pady=10)
top_frm.grid_columnconfigure((1, 2), weight=1)

# Choose language
lang_txt = language_text("Izaberite jezik:", "Choose Language:")
language_lbl = ttk.Label(
    top_frm,
    text=lang_txt,
    font=("Calibri", 16),
    width=14,
    bootstyle="light"
)
language_lbl.grid(column=0, row=0, padx=(30, 10), sticky="w")

# Language Combobox
languages_list = ["Srpski", "English"]
language_cmb = ttk.Combobox(
    top_frm,
    font=("Calibri", 12, "bold"),
    width=15,
    state="readonly",
    values=languages_list,
    bootstyle="light"
)
language_cmb.grid(column=1, row=0, padx=10, sticky="w")
language_cmb.set("Srpski")

language_cmb.bind("<<ComboboxSelected>>", language_change)

# Login button
login_btn_text = language_text("Prijavite se", "Log In")
login_btn = ttk.Button(
    top_frm,
    text=login_btn_text,
    width=10,
    bootstyle="dark",
    command=member_login
)
login_btn.grid(column=2, row=0, sticky="e")

login_pic = login_image()
login_lbl = ttk.Label(top_frm, image=login_pic)
login_lbl.grid(column=3, row=0, padx=(10, 30), sticky="e")

tooltip_login_text = language_text("Korisnik nije prijavljen",
                                   "User is not logged in")
tooltip_login = ToolTip(login_lbl, text=tooltip_login_text,
                        bootstyle="warning")

# Frame for logo and title
logo_frm = ttk.Frame(root)
logo_frm.pack(pady=10, anchor="center")

# Logo
image = Image.open("pics/vuk_karadzic.png")
image_resize = image.resize((120, 150))
image_smaller = image.resize((80, 100))
logo = ImageTk.PhotoImage(image_resize)
logo_smaller = ImageTk.PhotoImage(image_smaller)

# Place the image
logo_lbl = ttk.Label(logo_frm, image=logo)
logo_lbl.grid(column=0, row=0, rowspan=2, padx=20)

# Title and subtitle
main_title_text = language_text("Biblioteka \"Vuk Karadžić\"",
                                "Library \"Vuk Karadžić\"")
main_title = ttk.Label(
    logo_frm,
    text=main_title_text,
    width=20,
    font=("Calibri", 40, "bold"),
    bootstyle="warning"
)
main_title.grid(column=1, row=0, padx=20, pady=10)

main_subtitle_text = language_text("Sa vama od 2000. godine",
                                   "With you since 2000.")
main_subtitle = ttk.Label(
    logo_frm,
    text=main_subtitle_text,
    font=("Calibri", 20),
    bootstyle="light",
    anchor="n"
)
main_subtitle.grid(column=1, row=1, padx=20, sticky="n")

# Switch frame
switch_lf_text = language_text(" Radno okruženje ", " User Interface ")
switch_lf = ttk.LabelFrame(
    root,
    text=switch_lf_text,
    bootstyle="warning"
)
switch_lf.pack(expand=True, fill="x", pady=10, padx=20)

switch_var = ttk.IntVar()
switch_chb_text = language_text("  Korisnik/Bibliotekar", "  User/Librarian")
switch_chb = ttk.Checkbutton(
    switch_lf,
    variable=switch_var,
    text=switch_chb_text,
    width=20,
    bootstyle="warning-round-toggle",
    command=ui_create
)
switch_chb.grid(column=0, row=0, padx=20, pady=20, sticky="w")

switch_lbl_text = language_text(
    "Radno okruženje: običan korisnik (isključeno) / "
    "bibliotekar (uključno).",
    "User interface: common user (Off) / librarian (On)."
)
switch_lbl = ttk.Label(
    switch_lf,
    text=switch_lbl_text,
    font=("Calibri", 16),
    bootstyle="light"
)
switch_lbl.grid(column=1, row=0, padx=30, pady=20, sticky="w")

# User Interface frame
ui_frame = ttk.Frame(root)
ui_frame.pack(expand=True, fill="both")

ui_create()

# Exit the application - 'Exit' button.
exit_btn_text = language_text("Izađi", "Exit")
exit_btn = ttk.Button(
    root,
    width=10,
    text=exit_btn_text,
    style="big.dark.TButton",
    command=lambda: [titles.con.close(), books.con.close(),
                     members.con.close(), reservations.con.close(),
                     renting.con.close(), exit_app()]
)
exit_btn.pack(pady=(10, 20), padx=50, anchor="e")

root.mainloop()
