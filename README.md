# 1. Project title
    LIBRARY MANAGEMENT

# 2. Brief description of the project
"Library Management" is an application for both users and librarians.
It can be used to provide insight into various information about the 
library and book rentals, as well as for jobs that are necessary for
functioning of the library.

The application was made in Python, with the help of the PostgreSQL 
database management system. The 'ttkbootstrap' library was used to create 
the user interface.


# 3. The README.md file contents
#### 1. Project title
#### 2. Brief description of the project
#### 3. The README.md file contents
#### 4. Database and table structure
#### 5. Application description and usage

# 4. Database and table structure
Database name: "library_management"

Tables:

    titles
        title               (varchar (50), primary key, not null)
                                                        # book title
        author              (varchar (40), not null)    # author's name
        genre               (varchar (20), not null)    # book genre
        publication_year    (varchar (4), not null)     # publication year

    books
        book_code       (varchar (10), primary key, not null)
                                                        # book code
        title           (varchar (50), not null)        # book title
        availability    (varchar (15), not null)        # copy availability

    members
        membership_id   (varchar (6), primary key, not null)
                                                        # membership ID
        first_name      (varchar (20), not null)        # member's first name
        last_name       (varchar (20), not null)        # member's last name
        address         (varchar (40), not null)        # member's address
        telephone       (varchar (10), not null)        # member's phone number
        membership_date (date, not null)                # date of membership
        password        (varchar (30), not null)        # member password

    librarians
        personal_id     (varchar (4), primary key, not null)
                                                    # librarian ID
        first_name      (varchar (20), not null)    # librarian's first name
        last_name       (varchar (20), not null)    # librarian's last name
        address         (varchar (40), not null)    # librarian's address
        telephone       (varchar (10), not null)    # librarian's phone number
        password        (varchar (30), not null)    # librarian password

    renting
        rent_id         (integer, serial primary key, not null)
        membership_id   (varchar (6), not null)     # membership ID
        book_code       (varchar (10), not null)    # book code
        rental_date     (date, not null)            # rental date
        return_date     (date)                      # return date

    reservations
        reservation_id      (integer, serial primary key, not null)
        membership_id       (varchar (6), not null)     # membership ID
        book_code           (varchar (10), not null)    # book code
        reservation_date    (date, not null)            # reservation date


# 5. Description and use of the application

## 5.1 Main screen

![main_screen_user](https://github.com/kdkrle/library_management/assets/59825527/2a27efac-074b-4b4c-a8db-15081d97a0e6)

_Picture 1: Main Screen - User_

### 5.1.1 Elements at the very top

The main screen consists of several elements. At the very top on the left 
side there is the choice of language (Serbian/English), and on the right 
side there is a member login button and an icon indicating whether a member 
of the library is logged in or not. Also, by placing the mouse over the icon, 
there appears the text with notification of whether a member has been 
logged in and who he/she is, if so.

### 5.1.2 Logo and title
Right below the previous elements, there is the logo and the main title of 
the library.

### 5.1.3 User/Librarian frame

The 'User/Librarian' frame contains a toggle button and a brief explanation 
of what it does. This button serves to change the user interface, depending 
on whether it is used by a regular user or a librarian.

### 5.1.4 User interface

Below the previous frame is the user interface depending on whether,
with the toggle button, we decide to choose either a user or a librarian.

If a user is selected, there are two frames, one for any user, and the 
other which is available only to library members.

In the first frame, we have buttons that allow us to search for the books and 
basic information about them, insight into the most read books, the most 
read authors, as well as readership by genre. Next to the buttons there are 
brief notifications about what is got by pressing a particular button.

The second frame is for library members only and that's why unavailable 
until the member logs in. This frame also has buttons and notificiations
next to them about their function. Once signed in, a member of the library
can view his/her account details, reserve a book and change the password.

If we choose the user interface for the librarian, instead of the previous two
frames there will appear only one, with options that only librarian can use. 
This frame, like the ones previously mentioned, has buttons on the left and 
brief explanations of their functions on the right. The function of all 
buttons will be explained below.

At the very bottom there is the 'Exit' button which is used to close the 
application, and it is always there, no matter which user interface is 
selected.

## 5.2 Section for all users

This section contains four buttons available to anyone who starts the 
application.

### 5.2.1 Book search

![book_search](https://github.com/kdkrle/library_management/assets/59825527/1cf79431-5aa5-4549-9611-f7546d4b7342)

_Picture 2: Book Search_

Pressing the 'Book Search' button on the main screen a new window opens, 
in which it is possible to see which books exist in the library and get 
basic information about them.

At the top of that window there is the logo and the title. Below that is 
the filter section. In that section, first there are brief explanations of 
the use, and after that we have filters to narrow down the selection to the 
target group of books. It is possible to choose a book by author, genre or 
publication year. Each filter is used separately.

Below that is a drop-down menu from which we select books. If none of the 
previous filters are selected, it is possible to select any title from the 
library from here.

Then there follows a frame in which we get basic information about the 
selected book. When no book is selected, there is no information, except 
that there is an image of the book in the upper left corner of this section.
By selecting one of the titles, information about the book will appear, and 
the image will change to the image of the genre to which the title belongs.

There are two buttons at the bottom. The first button resets all filters, 
deselects the book choice and removes information about the book. The 
second button closes this window.

### 5.2.2 The most read books

![most_read_books](https://github.com/kdkrle/library_management/assets/59825527/39ee33bc-8156-436a-b913-7f2cb3ee4b7d)

_Picture 3: Most Read Books_

Pressing this button a new window opens, with a list of the most read books.

At the bottom we have two buttons again. The first shows the chart of the ten 
most read books, and the second closes this form.

### 5.2.3 The most read authors

![most_read_authors](https://github.com/kdkrle/library_management/assets/59825527/77197fb0-96ec-48dd-90eb-8bbb59bc6a85)

_Picture 4: Most Read Authors_

Similar to the previous one, a new form opens with a list of ten most read 
authors from the library. At the bottom there is a button that opens a 
chart with this information, as well as a button that closes the window.

### 5.2.4 Read by genre

![read_by_genre](https://github.com/kdkrle/library_management/assets/59825527/13f57114-b80f-47e0-899f-2fb649c10cdc)

_Picture 5: Read by Genre_

Finally, in this section we have a button that opens a window with a list
of rented books by genre. This list is not sorted by number of reads, like 
the previous two, but by genre name. In front of each genre, there is a 
picture of the corresponding genre.

There is only one button at the bottom, the one that closes this window.

## 5.3 Members only section

When the application opens, there is only one button available in this 
section - the member login button. After the member has logged in, other 
options become available.

### 5.3.1 Member login

![member_log_in](https://github.com/kdkrle/library_management/assets/59825527/1f913b8f-890c-432a-b659-642a93dc26af)

_Picture 6: Member Login_

The member login button performs the same function as the one at the top of 
the main screen. By pressing either of those two buttons, the member login 
form opens. It has a field for entering the membership ID and a field for 
entering a password.

Below are two buttons, one for applying the entered data, and the other for 
canceling the login and closing this form.

A successful login causes several changes. Both this button and the one at 
the top change the original text 'Log in' to 'Log out'. The user's picture 
at the top of the screen changes, and its tooltip text now gives the name 
of the library member who is logged in. Finally, the other buttons in this 
section become available.

![member_log_out](https://github.com/kdkrle/library_management/assets/59825527/db6250c1-9cdd-4e49-8765-9ea16367eea4)

_Picture 7: Member Logout_

Pressing this button again the logout form opens. At the top is the 
member's name, below that is the title of the window followed by the 
logout button, and at the very bottom is the button to cancel logout and 
close this window.

NOTE: For ease of working with the application and trying it out, all 
member passwords have the same value ('member').

### 5.3.2 Account details

![account_details](https://github.com/kdkrle/library_management/assets/59825527/ac002a3f-24fd-4a2e-81f9-e6a3c813de94)

_Picture 8: Account Details_

Pressing this button opens a window where we can see the name and surname 
of the member, his membership ID, as well as information about renting 
books and their reservation.

The rental section shows the currently rented book (if any) and its code,
rental date, and return deadline date. In addition, the total number of 
previous rentals is also displayed, as well as the number of times the 
member did not return the book on time.

The reservation section displays the currently reserved book (if any), the 
reservation expiration date, and the total number of reservations for this 
library member.

At the bottom is the button to close this screen.

### 5.3.3 Reservation

![reservation](https://github.com/kdkrle/library_management/assets/59825527/de337596-ee46-4a92-8ea5-32124058279b)

_Picture 9: Reservation_

Reservations last seven days. After that period they are automatically 
cancelled.

The reservation window, in addition to having the logo and title at the top, 
also has the member's name written on it.

This window has two frames, one for the currently reserved book and the 
other for a new reservation. The first frame contains information about the 
title of the book and its code, as well as the date until which the current 
book reservation is valid.

The new reservation frame has a drop-down menu to select the title we want 
to reserve and how many copies of that title are available.If there is 
already a reserved book, the selection of a new title is disabled.

Below this are three buttons, one to confirm the reservation, the second to 
cancel the reservation and the third to close this form. The reservation 
button is disabled if there is no title selected. Also, the button to 
cancel the reservation is disabled, if no book is currently reserved.

### 5.3.4 Password change

![password_change](https://github.com/kdkrle/library_management/assets/59825527/4a1c5a96-c8ff-429c-ae80-5eda7e2384a0)

_Picture 10: Password Change_

Selecting this option opens a window with three input fields. The first one 
is for entering the current password, the entry of which is hidden, and the 
other two are for entering a new password and its confirmation. Entering 
the membership ID is not necessary, because this member is already logged in.

In addition to the standard button to close the window, we also have a 
button to apply the entered data.

## 5.4 User interface for librarians

![main_screen_librarian](https://github.com/kdkrle/library_management/assets/59825527/3d00a9cc-7074-4547-8801-c1e9ac76ac14)

_Picture 11: Main Screen - Librarian_

When the user interface for librarians is selected, it replaces the user 
interface for other users. Nine new buttons appear, of which only the login 
button is available, since other users should not have access to this part 
of the application.

### 5.4.1 Librarian login

![librarian_log_in](https://github.com/kdkrle/library_management/assets/59825527/325898d0-b363-4fd9-a14a-ae883283b8d2)

_Picture 12: Librarian Login_

The librarian login window is almost identical to the member login window. 
It contains a field for entering the librarian's personal number and a 
field for entering a password.

Below are two buttons, one for applying the entered data, and the other for 
canceling the login and closing this form.

Upon successful librarian login, this button changes the text from 'Log In' 
to 'Log Out'. In addition, all other buttons in the librarian section 
become available.

![librarian_log_out](https://github.com/kdkrle/library_management/assets/59825527/6d344957-7c39-486a-a657-bbff5dd7bc7f)

_Picture 13: Librarian Logout_

After logging in, pressing the same button again opens the logout form. At 
the top is the name of the librarian, below that is the title of the window,
followed by the logout button, and at the very bottom is the button to 
cancel the logout and close this window.

NOTE: For ease of working with the application and trying it out, all 
librarian passwords have the same value ('lib').

### 5.4.2 Inventory

![inventory](https://github.com/kdkrle/library_management/assets/59825527/fca00a00-f959-437d-ba3e-af17d21621b0)

_Picture 14: Inventory_

By pressing the 'Inventory' button, we get an insight into the library's 
book inventory.

In the newly opened window, apart from the logo and title at the top, there 
is also the librarian's name. This is common to all other options in this 
section.

Below is the filter frame. There are two filters. The first filter gives a 
list of books by availability. There are four options to choose from: 'All 
Titles' (default), 'Available Books', 'Rented Books' and 'Reserved Books'. 
Izbor jedne od opcija u tabeli ispod dobijamo spisak svih knjiga, 
samo dostupnih, samo iznajmljenih ili samo rezervisanih.

The second filter provides a list by book title. Since there are several 
copies of the same title in the library, a list of copies of the selected 
title appears in the table.

The table has three columns in which the code of the book, its title and 
its availability are printed.

Underneath everything are three buttons. 'Delay' shows the books that are 
delayed in return, 'Availability' shows the percentage of book availability,
and the third button is the one that exits this window.

### 5.4.3 Adding books

![adding_books](https://github.com/kdkrle/library_management/assets/59825527/220fa88e-a7b1-4540-80f5-c2e490212849)

_Picture 15: Adding Books_

Next is the option to add books to the library collection. Apart from the 
usual elements at the top, this window has two frames. The first box 
contains a choice between adding books with titles that already exist and 
adding books with a new title.

In the second frame, there is a drop-down menu for selecting or entering 
the title of the book, a newly generated book code (which does not exist in 
the database), a drop-down menu for selecting or entering the author, a 
drop-down menu for selecting the genre only, and a field for entering the 
book publication year.

If the existing title option is selected in the first frame, the fields for 
author, genre and publication year are unavailable, because that 
information already exists and is automatically printed on the screen when 
the book is selected.

The apply button accepts the entered data, and the close button exits this 
window.

### 5.4.4 Books update

![books_update_a](https://github.com/kdkrle/library_management/assets/59825527/024d3002-927f-4851-ae0b-9cf2eb35c6d3)

_Picture 16: Books Update (top)_

![books_update_b](https://github.com/kdkrle/library_management/assets/59825527/a55c6e0d-d8b8-49c2-8823-805ba59e4a99)

_Picture 17: Books Update (bottom)_

Below the header, which contains the logo, the librarian's name, and the 
title, there are two frames - title update frame and individual copy update 
frame.

The title update frame on the left has a drop-down menu to choose from
titles and information for author, genre and publication year. When 
selecting a title, other information is automatically printed. On the right 
are also the title, author, genre and publication year, but here we enter 
the values that need to be updated.

The second frame is somewhat different. There at the top we have a 
drop-down menu with a choice of code of the copy we want to update. The 
code _cannot_ be changed. By choosing a code, the title of the copy and its 
availability are printed on the left, and values for updating are entered 
on the right.

Both frames have their own buttons to reset data and accept values to be 
updated.

Updating titles updates the 'titles' table, and updating books updates the 
'books' table. It should also be said that if the title in the 'titles' 
table is updated, the values for the title in the 'books' table are checked 
and updated.

The 'Close' button closes the window.

### 5.4.5 Member information

![members_info](https://github.com/kdkrle/library_management/assets/59825527/3149e339-1ff7-475b-86e3-12db39e458d4)

_Picture 18: Members Info_

Besides the header at the top and the close button at the bottom of the 
form there are two frames. The first one contains information about the 
selected member. When the membership ID is selected from the drop-down menu,
the other information is printed. That information is the member's name, 
his address, his phone number, the time he has been a member and his password.

In the lower frame, which contains information about rentals and 
reservations, the values for the total number of rentals, how many times 
this member did not return the book on time, currently rented books and 
currently reserved books, if any, are printed.

### 5.4.6 New members

![new_members](https://github.com/kdkrle/library_management/assets/59825527/b63d9e85-7edf-4d8d-aa91-40f064f7aa8d)

_Picture 19: New Members_

Selecting this option opens a window with the usual header under which the 
data required to register a new member is entered. The name, surname, 
address and phone number of the new member are entered there. The value for 
the membership ID is automatically generated (so that it is different from 
those of other members), and the password can be changed or left at the 
default value 'member'.

If all values have been entered, the apply button can be used to enter a 
new member in the database, and the close button closes this window.

### 5.4.7 Members update

![members_update](https://github.com/kdkrle/library_management/assets/59825527/738b3aa6-7b93-437b-87c1-a55d295bd5b6)

_Picture 20: Members Update_

After the standard header, there is a drop-down menu with the selection of 
the code of the member whose data we want to update. When the code is 
selected on the left side, the current values for the name, surname, 
address, phone number and password of the member are printed. On the right 
there are fields to input these same values for updating.

There are three buttons at the bottom. The first is to accept the update 
with the new values that have been entered, the second is to reset all 
values and membership ID selections, and the third is to close the window.

### 5.4.8 Renting

![renting](https://github.com/kdkrle/library_management/assets/59825527/5a5fe8ac-8eca-4ec2-8d78-67ec1b54ba26)

_Picture 21: Renting_

The deadline for returning the rented book is fifteen days.

When the rent button is selected from the main screen, a window opens with 
a slightly different header than the others. Here, next to the name, there 
is today's date, so that there is an insight of the date when the rental 
is made.

Below the header are two frames. In the left frame are the data about the 
member: his membership ID, his name, the title of the currently rented 
book, the title of the currently reserved book, the code of the currently 
reserved book and the date when the reservation expires. These data change 
depending on the choice of membership ID.

In the right frame is the information about the title. There are the title 
of the book, the name of the author, the total number of copies of the book,
the number of copies available, the book code and the deadline for 
returning the rented book.

The book title and book code are selected from the drop-down menu. They are 
not immediately available. When the membership number is selected, the 
drop-down menu in the right frame becomes available, if there is not 
already a rented book. Only when the member with that ID returns the book 
he can rent a new one. After selecting a title from the drop-down menu, it 
becomes possible to select the code of the available copies of the book.

There are three buttons at the bottom. The first button inserts the new rental 
data into the appropriate tables and updates the data. The second button 
inserts data about the return of the currently rented book into the 
appropriate tables and resets all data.

Neither of these two buttons is available until a membership ID is selected. 
If the member with that number has a rented book, the return button becomes 
available and vice versa. Also, when a book is rented or returned, the 
pressed button becomes unavailable and the other button becomes available.

The third button closes this window.

### 5.4.9 Statistics

![statistics](https://github.com/kdkrle/library_management/assets/59825527/7e54eab9-6487-4e1c-9fef-a2cc8d06f512)

_Pictures 22: Statistics_

The last button in the section for librarians opens a window from which we 
can get various reports and charts.

At the top is the usual header, and at the bottom is the button to close 
the window. Between them there are eight buttons next to which there are 
brief explanations about their function.

The first button takes us to a list of members who have never been late in 
returning books. The second button gives us a list of members who are late 
in returning and how many times they have done so. The third button shows a 
chart of the ten members with the most delays. The fourth one shows a chart 
of ten most delayed titles. The fifth one gives us a graphical insight into 
the longest membership. The sixth button gives us a graphic representation 
of the members who rented books the most times. The seventh button takes us 
to the percentage display of the number of titles per genre, while the 
eighth button gives us an insight into the percentage display of the number 
of copies per genre.

Reports and charts from the 'Statistics' section:

![statistics_1_no_delay](https://github.com/kdkrle/library_management/assets/59825527/62029418-3163-44bf-aff8-d0e568160dcc)

_Picture 23: Statistics - No Delay_

![statistics_2_delay_list](https://github.com/kdkrle/library_management/assets/59825527/37ab8f3f-1e66-4410-aa62-30006f5c859f)

_Picture 24: Statistics - Members Delay List_

![statistics_3_delay_chart](https://github.com/kdkrle/library_management/assets/59825527/6f228c55-2ebd-4a42-81ea-c4c64087da7a)

_Picture 25: Statistics - Members Delay Chart_

![statistics_4_delay_titles](https://github.com/kdkrle/library_management/assets/59825527/fc317d23-0c11-471c-8e06-9a23594f73aa)

_Picture 26: Statistics - Titles Delay Chart_

![statistics_5_longest_membership](https://github.com/kdkrle/library_management/assets/59825527/97fca0ea-a23d-497e-a7da-8ee92bd4ee90)

_Picture 27: Statistic - Longest Membership_

![statistics_6_most_rentals](https://github.com/kdkrle/library_management/assets/59825527/c87ee99e-ecc7-478d-b01a-adafe159240a)

_Pictire 28: Most rentals_

![statistics_7_titles_by_genre](https://github.com/kdkrle/library_management/assets/59825527/7cfb3cc2-c4c1-4166-a0de-90afc5bfd467)

_Picture 29: Titles by Genre_

![statistics_8_copies_by_genre](https://github.com/kdkrle/library_management/assets/59825527/f5d2296a-276f-4d53-a874-a883666d6c1c)

_Picture 30: Copies by Genre_
