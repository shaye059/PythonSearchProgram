def menu():
    '''()->None
    Prints a menu displaying the acceptable inputs then asks the user for input.
    If the input is not one of the accepted forms it displays an error message
    and then asks again. If the input is one of the accepted inputs, it either
    quits it makes a function call to the function that executes that function.
    '''
    run=True
    while run==True:
        print("====================================================="
              "\n1: Look up range"
              "\n2: Look up month/year"
              "\n3: Look up author"
              "\n4: Search for title"
              "\n5: Number of authors with at least x bestsellers"
              "\n6: List y authors with the most bestsellers"
              "\nQ: Quit"
              "\n=====================================================")
        menu_option=0
        while menu_option!='q' and menu_option not in range(1,7):
            menu_option=input("Enter 1-6 or Q: ").strip()
            try:
                menu_option=int(menu_option)
            except ValueError:
                menu_option=menu_option.lower()
                if menu_option=='q':
                    return
                else:
                    print("Sorry, invalid input. Please try again.")

        lines=open('NYT-bestsellers.txt',encoding="utf-8").read().splitlines()
        book_info=[]
        for book in lines:
            book_info.append(book.split('\t'))

        
        if menu_option==1:
            year_range(book_info)
        if menu_option==2:
            month_year(book_info)
        if menu_option==3:
            author(book_info)
        if menu_option==4:
            title(book_info)
        if menu_option==5:
            number_author(book_info)
        if menu_option==6:
            y_authors(book_info)
        try:
             input("\nPress enter to continue. ")
             print()
        except SyntaxError:
             pass
    

#Common functions
def date_finder(book):
    '''(list)->lst
    Takes as input the list containg information about the book and then
    turns the object that is the date into a sublist with three objects:
    the first being the month, the second the day, and the third the year.

    >>> date_finder(['Lean Mean Thirteen', 'Janet Evanovich', "St. Martin's", '7/8/2007', 'Fiction'])
    >>> ['7', '8', '2007']
    '''
    date=book[3].strip()
    date=date.split("/")
    return date

def date_formatter(date):
    '''(lst)->str
    Takes as input a list containing three objects of a date (the first is the
    month, second the day and third the year). If the date or the month aren't
    two digits long it adds a zero to the front of either. It the returns the
    date as a string in the form yyyy-mm-dd.

    
    >>> date_formatter(['2', '19', '1950'])
    >>> 1950-02-19
    '''
    if len(date[0])==1:
        date[0]='0'+date[0]
    if len(date[1])==1:
        date[1]='0'+date[1]
    date=date[2]+"-"+date[0]+"-"+date[1]
    return date


def result_printer(result):
    '''(2D list)->None
    Takes as input a 2D list, of which each sublist is a book and the objects in that
    sublist are the information abou the book. If the 2D list is empty it prints a
    message stating that there are no books in the time period, else it sorts the
    books by date and then prints each one with the information being diplayed
    as the title first, then the author and then the date.

    '''
    if result==[]:
        print("Unfortunatley there's no record of best sellers for the time period entered.")
        exit
    from operator import itemgetter
    result = sorted(result, key=itemgetter(2))
    for book in result:
        print(book[0].strip()+", by "+book[1].strip()+" ("+book[2]+")")


def frequency(book_info):
    '''(2D_list)->(2D_list)
    Takes as input a 2D list of books, with each sublist containing information about the
    book. It then removes any white pace around the authors name and then creates a new
    2D list with each sublist containing the author and how many books they have in the
    input list.
    '''
    for book in book_info:
        book[1]=book[1].strip()
    f=[]
    from operator import itemgetter
    book_info = sorted(book_info, key=itemgetter(1))
    book=0
    while book <= len(book_info)-2:
        counter=1
        author=[]
        while book_info[book][1]==book_info[book+1][1]:
            counter=counter+1
            book=book+1
        author.extend((book_info[book][1], counter))
        f.append(author)
        book=book+1
    return f

#Look up range
    
def year_range(book_info):
    '''(2D List)->None
    Takes as input a 2D list of books and then prompts the user to enter
    a starting and ending year. It then prints all books in the list that
    were published between and including the two years given.
    Note: years must be entered as four digit integers. If a valid input
    is not detected then the user is prompted again to input a year until
    a valid year is entered.
    '''
    year1=1
    year2=1
    while year1<1000 or year1>9999:
        try:
            year1=int(input("Enter a starting year: ").strip())
            if year1<1000 or year1>9999:
                   print("Sorry, please enter a four digit integer for the year.")
            else:
                year1=int(year1)
        except ValueError:
            print("Sorry, please enter a four digit integer for the year.")
            year1=1
            
    while year2<1000 or year2>9999:
        try:
            year2=int(input("Enter an ending year: ").strip())
            if year2<1000 or year2>9999:
                   print("Sorry, please enter a four digit integer for the year.")
            else:
                year2=int(year2)
        except ValueError:
            print("Sorry, please enter a four digit integer for the year.")
            year2=1

    result=[]
    for book in book_info:
        date=date_finder(book)
        year=int(date[2])
        if year1<=year<=year2:
            date=date_formatter(date)
            book1=[]
            book1.extend((book[0],book[1],date))
            result.append((book1))
            
    result_printer(result)



#Look up month/year
    
def month_year(book_info):
    '''(2D list)-> None
    Takes as input a 2D list of books and then prompts the user to enter
    a year and a month. It then prints all books in the 2D list that
    were published during the month and year inputed. If no books are found
    at the date, a message is printed informing the user that no books
    were found.
    Note: years must be entered as four digit integers and month must be
    entered as a a single or double digit integer between 1-12. If a valid
    input is not detected then the user is prompted again to input a year until
    a valid year is entered.
    '''
    year_s=1
    month_s=0
    while month_s<1 or month_s>12:
        try:
            month_s=int(input("Enter a month: ").strip())
            if month_s<1 or month_s>12:
                   print("Sorry, please enter an integer between 1-12 for the month.")
            else:
                month_s=int(month_s)
        except ValueError:
            print("Sorry, please enter an integer between 1-12 for the month.")
            month_s=0
            
    while year_s<1000 or year_s>9999:
        try:
            year_s=int(input("Enter a year: ").strip())
            if year_s<1000 or year_s>9999:
                   print("Sorry, please enter a four digit integer for the year.")
            else:
                year_s=int(year_s)
        except ValueError:
            print("Sorry, please enter a four digit integer for the year.")
            year_s=1

    result=[]
    for book in book_info:
        date=date_finder(book)
        year=int(date[2])
        month=int(date[0])
        if year==year_s and month==month_s:
            date=date_formatter(date)
            book1=[]
            book1.extend((book[0],book[1],date))
            result.append((book1))
    print("All titles in month "+str(month_s)+" of year "+str(year_s)+":")        
    result_printer(result)

#Search for author

def author(book_info):
    '''(2D list)->None
    Takes as input a 2D list and prompts the user for a name (or part of
    a name) of aan author). It then prints all books written by authors
    whose name's contain the user's input. If no books are found the
    function prints a message that no books were found written by authors
    whose name's contain the input.
    '''
    name=(input("Enter an author's name or part of a name: ").strip()).lower()
    result=[]
    for book in book_info:
        author=book[1].strip().lower()
        date=date_finder(book)
        if name in author:
            date=date_formatter(date)
            book1=[]
            book1.extend((book[0],book[1],date))
            result.append((book1))
    if result==[]:
        print("Unfortunatley there's no books found by an author whose name contains: "+name)
        exit
    from operator import itemgetter
    result = sorted(result, key=itemgetter(2))
    for book in result:
        print(book[0].strip()+", by "+book[1].strip()+" ("+book[2]+")")

#Search for title
def title(book_info):
    '''(2D list)->None
    Takes as input a 2D list and prompts the user for a name (or part of
    a name) of a title). It then prints all books with titles which contain
    the user's input. If no books are found the function prints a message
    that no books were found containing the input.
    '''
    name=(input("Enter a title or part of a title: ").strip()).lower()
    result=[]
    for book in book_info:
        title=book[0].strip().lower()
        date=date_finder(book)
        if name in title:
            date=date_formatter(date)
            book1=[]
            book1.extend((book[0],book[1],date))
            result.append((book1))
    if result==[]:
        print("Unfortunatley there's no books found with a title that contains: "+name)
        exit
    from operator import itemgetter
    result = sorted(result, key=itemgetter(2))
    for book in result:
        print(book[0].strip()+", by "+book[1].strip()+" ("+book[2]+")")

#Number of authors with x bestsellers
def number_author(book_info):
    '''(2D list)-> None
    Takes as input a 2D list of numbers then prompts the user to input a number
    of bestsellers. The function then prints the authors who have as many or
    more than the entered number of books in the list. If there are no authors
    with as many or more books than the number entered, the function prints a
    message informing the user.
    
    Conditions: the number entered by the user must be an integer larger than 0.
    Else to function will continue to prompt the user until a valid input is
    enterd.
    '''
    number_bestsellers=-1
    result=[]
    while number_bestsellers <1:
        try:
            number_bestsellers=int(input("Enter the number of bestsellers (integer larger than 0): ").strip())
            if number_bestsellers<1:
                print("Sorry, integer must be larger than 0.")
        except ValueError:
            print("Sorry, input invalid.")
    lst=frequency(book_info)
    for author in lst:
        if author[1]>=number_bestsellers:
            result.append(author)
    if result==[]:
        print("Unfortunatley there's are no authors with "+str(number_bestsellers)+".")
        exit

    from operator import itemgetter
    result = sorted(result, key=itemgetter(1), reverse=True)
    print("The list of authors with at least "+str(number_bestsellers)+" NYT bestsellers is:")
    rank=1
    for author in result:
        print(str(rank)+". "+str(author[0])+" with "+str(author[1])+" bestsellers")
        rank=rank+1
        
#List y auhors with the most bestsellers
def y_authors(book_info):
    '''(2D list)-> None
    Takes as input a 2D list of numbers then prompts the user to input the number
    of authors. It prints the authors by rank of how many times they appear in the
    inputed list, up to the rank equal to the number the user entered.
    
    Note: If the number is 0 or smaller the function continues to prompt the user
    until they input an integer larger than 0. If the input is larger than the
    number of authors that appear in the list, the function prints a message
    stating that the number has exceeded the number of authors.
    '''
    number_authors=-1
    result=[]
    while number_authors<1:
        try:
            number_authors=int(input("Enter the number of authors (integer larger than 0): ").strip())
            if number_authors<1:
                print("Sorry, integer must be larger than 0.")
        except ValueError:
            print("Sorry, input invalid.")
    lst=frequency(book_info)
    if number_authors>len(lst):
        print("Sorry, there are only "+str(len(lst))+" authors in the NYT bestseller list.")
    else:
        from operator import itemgetter
        lst = sorted(lst, key=itemgetter(1), reverse=True)
        for times in range(number_authors):
            print(str(times+1)+". "+str(lst[times][0]))


#main
menu()

