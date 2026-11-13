from Bioskopske_projekcije import multicriteria_search_projections1, cinema_screening_term_list, show_results
from Bioskopske_projekcije import get_projection_date, write_to_reserved_tickets, cinema_screening_term_append
from Bioskopske_projekcije import cinema_projection_list, cinema_projection_read, data_loaded, reserved_tickets_read
#from Bioskopske_projekcije import user_data_append, user_data
from datetime import datetime, timedelta
#import Bioskopske_projekcije
from prettytable import PrettyTable
from Bioskopske_projekcije import get_password_projection1, cinema_projection_append, reserved_tickets_list
from Reports_second import all_tickets_list, fill_all_projections_list_append, all_projections_list, fill_list_append
#from Bioskopske_projekcije import reserved_tickets_loaded, reserved_tickets_read


def ticket_reservation(username, condition, seller_username):
    print("Odaberite zeljeni termin projekcije. ")
    print("[A] Pretraga projekcije")
    print("[B] Unos sifre projekcije")
    
    while True:
        input1 = input("Izaberite opciju: ")
        if input1.upper() == "A":
            #cinema_projection_search(cinema_projection_list, criterions)
            multicriteria_search_projections1(username, condition, seller_username)
            #overview_of_available_seats(get_password_projection1)

            #input_term = input("Unesite broj termina: ")
            #if input
            break
        elif input1.upper() == "B":
            global reserved_tickets_list
            #reserved_tickets_list = load_reserved_cards()

            reserved_tickets_read()
            #while True:
            #    input_password = input("Unesite sifru projekcije: ").upper().strip()
            #    found, password = get_password_projection(input_password)
            #    if found:
            #        break
            cinema_screening_term_append()
            while True:
                overview_of_available_terms()
                input_password = input("Unesite šifru termina: ").upper().strip()
                seat_available, card_password, card_date = search_projection_by_password(input_password)

                if seat_available == True:
                    #rows, columns = overview_of_available_seats(input_password)

                    seat_info = overview_of_available_seats(input_password)
                    if seat_info is not None:
                        rows, columns = seat_info
                        seat_matrix = generate_seat_matrix(rows, columns, card_password)
                        
                        matrix(seat_matrix, rows, columns, card_password, card_date, username, condition, seller_username)

                        update_matrix_with_reservations(seat_matrix, reserved_tickets_list, card_password)

                    else:
                        print("Nisu pronađeni podaci o sedištima za unetu šifru projekcije.")


                    break
                else:
                    print("Pogresan unos! Molimo vas pokusajte ponovo. ")
            #search_projection_by_password(input_password, projections)
            #enter_projection_by_password()
            break
        else:
            print("Vas unos nije ispravan! Molimo vas pokusajte ponovo.")

    #rows, columns = overview_of_available_seats(input_password)
    #for row in rows:
    #    print(f"Red {row}")
        


                    

def get_password_projection(input_password):
    global cinema_screening_term_list
    #matching_dates = []
    for term in cinema_screening_term_list:
        if term["Term_password"] == input_password:
            #matching_dates.append(datetime.strptime(["Date"], "%d.%m.%Y.").strftime("%d.%m.%Y."))
            
            return True, input_password
            
    print("Uneta sifra termina ne postoji! Molimo vas pokusajte ponovo.")
    return False, None

#def get_password_projection1(selected_date):
#    global cinema_screening_term_list
#
#    for term in cinema_screening_term_list:
#        if term["Date"] == selected_date:
#            return term["Term_password"]



def search_projection_by_password(password):
    global cinema_screening_term_list
    with open("reserved_tickets.txt", "a") as file:
        #file.write()

        for projection in cinema_screening_term_list:
            if projection["Term_password"] == password:
                #file.write(projection["Date"] + "\n")
                return True, projection["Term_password"], projection["Date"]
    return False, None, None

###############################################################################################################reserved_tickets_list = []
def add_reserved_cards(seat, card_password, card_date, username, condition, seller_username):
    global cinema_screening_term_list
    global reserved_tickets_list
    global all_tickets_list
    fill_list_append()

    global all_projections_list
    fill_all_projections_list_append()

    with open("reserved_tickets.txt", "a") as file:
        #file.write()
        real_date = datetime.now().strftime("%d.%m.%Y.")
        #for projection in cinema_screening_term_list:

        current_time = datetime.now()
        last_365_days = current_time - timedelta(days=365)
        total_price = 0
        for all_ticket in all_tickets_list:
            #print("Datummmmmmmmmmmmmmmmm" +  str(datetime.strptime(all_ticket["ticket_all_real_date"], "%d.%m.%Y.")))
            if all_ticket["ticket_all_username"].strip() == username.strip() and datetime.strptime(all_ticket["ticket_all_real_date"].strip(), "%d.%m.%Y.") >= last_365_days:
                for all_projection in all_projections_list:
                    if all_projection["Password"].strip() == all_ticket["ticket_all_password"][:4].strip():
                        total_price += float(all_projection["Price"])
        
        projection = next((proj for proj in all_projections_list if proj["Password"].strip() == card_password[:4].strip()), None)
        #price = next((proj for proj in all_projections_list if proj["Password"].strip() == card_password[:4].strip()), None)

        #card_price = projection["Price"]
        weekday = datetime.strptime(card_date, "%d.%m.%Y.").weekday()
        #print("WEEEEkk dayy" + weekday)
        if weekday == 1:
            card_price = float(projection["Price"]) - 50
        elif weekday in [5, 6]:
            card_price = float(projection["Price"]) + 50
        else:
            card_price = projection["Price"]


        if total_price >= 5000:
            
            card_price = 0.9 * float(projection["Price"])
            print("Dobili ste popust zbog kartice lojalnosti.\n")

        if condition.strip() == "R":
            seller_username = ""
        file.write("{}|{}|{}|{}|{}|{}|{}|{}|\n".format(card_password, card_date, seat, username, condition, real_date, seller_username, card_price))

        reserved_ticket = {
            "card_password": card_password,
            "card_date": card_date,
            "seat": seat,
            "username": username,
            "condition": condition,
            "real_date": real_date,
            "seller_username": seller_username,
            "card_price": card_price

        }

        reserved_tickets_list.append(reserved_ticket)

        ticket_all = {
                "ticket_all_password": card_password,
                "ticket_all_date": card_date,
                "ticket_all_seat": seat,
                "ticket_all_username": username,
                "ticket_all_condition": condition,
                "ticket_all_real_date": real_date,
                "ticket_all_seller_username": seller_username,
                "ticket_all_card_price": card_price 
            }
        all_tickets_list.append(ticket_all)



def overview_of_available_seats(password):
    global data_loaded
    if not data_loaded:
        cinema_projection_read()
        data_loaded = True

    with open("halls.txt", "r") as file:
        lines = file.readlines()
        #for projection in cinema_projection_list:
        #        if projection["Password"] == password[:4]:
        #            if projection["Hall"] 
        for line in lines:
            apart_line = line.strip().split("|")
            hall = apart_line[0]
            #rows_number = apart_line[2]
            #colums_number = apart_line[3]

            for projection in cinema_projection_list:
                if projection["Password"] == password[:4] and projection["Hall"] == hall:
                    rows_number = int(apart_line[2])
                    #colums_number = apart_line[3]
                    columns_letter = apart_line[3]
                    #columns_number = ord(columns_number) - ord('A') + 1
                    columns_number = ord(columns_letter) - ord('A') + 1
                    return rows_number, columns_number
    return None, None

def update_matrix_with_reservations(seat_matrix, reserved_cards, card_password):
    for reserved_card in reserved_cards:
        if reserved_card["card_password"] == card_password:
            seat = reserved_card["seat"]
            row_number = int(seat[:-1]) - 1
            column_letter = seat[-1]
            if 0 <= row_number < len(seat_matrix) and 'A' <= column_letter <= chr(ord('A') + len(seat_matrix[0]) - 1):
                seat_matrix[row_number][ord(column_letter) - ord('A')] = "X"


#def update_matrix_with_reservations(seat_matrices, reserved_cards):
#    global cinema_screening_term_list
#    cinema_screening_term_append()
#    for reserved_card in reserved_cards:
#        for term in cinema_screening_term_list:
#            if term["Term_password"] == reserved_card["card_password"]:
#                seat_matrix = seat_matrices.get(reserved_card["card_password"], None)
#                if seat_matrix is not None:
#                    seat = reserved_card["seat"]
#                    row_number = int(seat[:-1]) - 1
#                    column_letter = seat[-1]
#                    if 0 <= row_number < len(seat_matrix) and 'A' <= column_letter <= chr(ord('A') + len(seat_matrix[0]) - 1):
#                        seat_matrix[row_number][ord(column_letter) - ord('A')] = "X"

#def seat_valid():

# Dodajte poziv funkcije za učitavanje rezervacija na početak programa
#reserved_cards_list = load_reserved_cards()

def generate_seat_matrix(rows, columns, card_password):
    # Generišite matricu slobodnih sedišta koristeći broj redova i kolona
    matrix = []
    for _ in range(rows):
        #row_seats = ['X' for _ in range(columns)]
        row_seats = [chr(ord('A') + i) for i in range(columns)]

        #for term in cinema_screening_term_list:
        #            for reserved_ticket in reserved_tickets_list:
        #                if term["Term_password"] == card_password:
        #                    reserved_ticket["seat"] = "X"

        matrix.append(row_seats)

    #update_matrix_with_reservations(matrix, reserved_cards_list) 
    return matrix

def print_seat_matrix(matrix):
    for i, row in enumerate(matrix, start=1):
        print(f'Red {i}: {" ".join(row)}')
    print("\n")

#seat_matrices = {}
def matrix(seat_matrix, rows, columns, card_password, card_date, username, condition, seller_username):
    global reserved_tickets_list
    #reserved_tickets_list = load_reserved_cards()
    reserved_tickets_read()
    update_matrix_with_reservations(seat_matrix, reserved_tickets_list, card_password)
    print("Matrica slobodnih sedišta:")
    print_seat_matrix(seat_matrix)

    #seat_matrices[card_password] = [row[:] for row in seat_matrix]
    #seat_matrices[card_password] = seat_matrix

    while True:
        #try:
        seat = input("Unesite oznaku sedista (na primer 3F): ").strip().upper()
        if not seat:
            print("Pogresan unos! Molimo vas unesite validno sediste.")
        elif seat[:-1].isdigit() and seat[-1].isalpha():
            #print("Pogresan unos! Molimo vas pokusajte ponovo.")
        
            row_number = int(seat[:-1]) - 1
            column_letter = seat[-1]
            try:
                if seat_matrix[row_number][ord(column_letter) - ord('A')] == "X":
                    print("Sediste je vec rezervisano! Molimo vas pokusajte neko drugo sediste.")
                elif 0 <= row_number < rows and 'A' <= column_letter <= chr(ord('A') + columns - 1):
                    seat_matrix[row_number][ord(column_letter) - ord('A')] = "X"
                    if condition == "R":
                        print("Uspesno ste rezervisali kartu.")
                    elif condition == "K":
                        print("Uspesno ste kupili kartu.")
                    add_reserved_cards(seat, card_password, card_date, username, condition, seller_username)
                    update_matrix_with_reservations(seat_matrix, reserved_tickets_list, card_password)
                    break
            except IndexError:
                print("Sediste nije dostupno!")
                #else:
                #    print("Sediste nije dostupno!")
        else:
            print("Pogresan unos! Molimo vas unesite validno sediste.")
        #except ValueError:
        #    print("Pogresan unos! Molimo vas unesite validno sediste.")
    #if 0 <= row_number < rows and 'A' <= column_letter <= chr(ord('A') + columns - 1):
    #    seat_matrix[row_number][ord(column_letter) - ord('A')] = "X"
    #    print("Uspesno ste rezervisali sediste")
    #    add_reserved_cards(seat, card_password, card_date)
#           
    while True:     
        print("Da li zelite da rezervisete jos karata?")  
        print("[1] DA")      
        print("[2] NE") 
        more_cards = input("Izaberite opciju: ")
        if more_cards == "1":
            print("Matrica slobodnih sedišta:")
            print_seat_matrix(seat_matrix)
            while True:
                seat = input("Unesite oznaku sedista (na primer 3F): ").strip().upper()
                if not seat:
                    print("Pogresan unos! Molimo vas unesite validno sediste.")
                elif seat[:-1].isdigit() and seat[-1].isalpha():
                #print("Pogresan unos! Molimo vas pokusajte ponovo.")
                    row_number = int(seat[:-1]) - 1
                    column_letter = seat[-1]

                    try:
                        if seat_matrix[row_number][ord(column_letter) - ord('A')] == "X":
                            print("Sediste je vec rezervisano! Molimo vas pokusajte neko drugo sediste.")
                        elif 0 <= row_number < rows and 'A' <= column_letter <= chr(ord('A') + columns - 1):
                            seat_matrix[row_number][ord(column_letter) - ord('A')] = "X"
                            print("Uspesno ste rezervisali sediste")
                            add_reserved_cards(seat, card_password, card_date, username, condition, seller_username)
                            update_matrix_with_reservations(seat_matrix, reserved_tickets_list, card_password)
                            break
                    except IndexError:
                        print("Sediste nije dostupno!")
                        #else:
                        #    print("Sediste nije dostupno!")
                else:
                    print("Pogresan unos! Molimo vas unesite validno sediste.")
                #break
            #row_number = int(seat[:-1]) - 1
            #column_letter = seat[-1]
            #if 0 <= row_number < rows and 'A' <= column_letter <= chr(ord('A') + columns - 1):
            #    seat_matrix[row_number][ord(column_letter) - ord('A')] = "X"
            #    print("Uspesno ste rezervisali sediste")
            #    add_reserved_cards(seat, card_password, card_date)
        elif more_cards == "2":
            break
        else:
            print("Pogresan unos! Molimo vas pokusajte ponovo.")
    update_matrix_with_reservations(seat_matrix, reserved_tickets_list, card_password)
    print("Matrica slobodnih sedišta:")
    print_seat_matrix(seat_matrix)
    #else:
    #    print("Sediste nije dostupno!")


def load_reserved_cards():
    reserved_cards = []
    try:
        #counter = 1
        with open("reserved_tickets.txt", "r") as file:
            for line in file:
                apart_line = line.strip().split("|")
                #term_password, _, seat = line.strip().split("|")
                term_password = apart_line[0]
                card_date = apart_line[1]
                seat = apart_line[2]
                username = apart_line[3]
                condition = apart_line[4]
                real_date = apart_line[5]
                seller_username = apart_line[6]
                card_price = apart_line[7]
                ########################
                
                #if {"card_password": term_password, "card_date": card_date, "seat": seat, "username": username, "condition": condition, "real_date": real_date, "seller_username": seller_username, "card_price": card_price} not in reserved_cards:
                #    reserved_cards.append({"card_password": term_password, "card_date": card_date, "seat": seat, "username": username, "condition": condition, "real_date": real_date, "seller_username": seller_username, "card_price": card_price})
                #    counter += 1
                #    print(counter)
                
                if not any(
                    card["card_password"] == term_password and
                    card["card_date"] == card_date and
                    card["seat"] == seat and
                    card["username"] == username and
                    card["condition"] == condition and
                    (card["real_date"] == real_date or datetime.strptime(card["real_date"], "%d.%m.%Y.") == datetime.strptime(real_date, "%d.%m.%Y.")) and
                    card["seller_username"] == seller_username and
                    card["card_price"] == card_price
                    for card in reserved_cards
                ):
                    reserved_cards.append({
                        "card_password": term_password,
                        "card_date": card_date,
                        "seat": seat,
                        "username": username,
                        "condition": condition,
                        "real_date": real_date,
                        "seller_username": seller_username,
                        "card_price": card_price
                    })
                    #counter += 1
                    #print(counter)

    except FileNotFoundError:
        print("Fajl nije pronadjen!")
        #pass  
    return reserved_cards

reserved_tickets_loaded = False
def reserved_tickets_read():
    global reserved_tickets_loaded
    global reserved_tickets_list
    if not reserved_tickets_loaded:
        reserved_tickets_list = load_reserved_cards()
        reserved_tickets_loaded = True
        return reserved_tickets_list

#def overview_of_reserved_tickets(username):
#    global reserved_tickets_list
#    global cinema_projection_list
#    global cinema_screening_term_list
#
#    reserved_tickets_read()
#    cinema_projection_append()
#    cinema_screening_term_append()
#
#    table = PrettyTable()
#    table.field_names = ["Oznaka", "Naziv filma", "Datum", "Vreme pocetka", "Vreme kraja", "Sediste"]
#
#    for ticket in reserved_tickets_list:
#        if ticket["username"] == username:
#            for projection in cinema_projection_list:
#                if ticket["card_password"][:4] == projection["Password"]:
#                    for term in cinema_screening_term_list:
#                        if term["Term_password"] == ticket["card_password"]:
#                            # Provera da li podaci već postoje u tabeli
#                            exists_in_table = any(
#                                row[0] == ticket["card_password"] and
#                                row[5] == ticket["seat"]
#                                for row in table._rows  # _rows sadrži trenutne redove tabele
#                            )
#                            if not exists_in_table:
#                                table.add_row([ticket["card_password"], projection["Film"], term["Date"], projection["Time_start"], projection["Time_end"], ticket["seat"]])
#    
#    print(table)
#
#    while True:
#        inputN = input("[N] Nazad: ").upper()
#        if inputN == "N":
#            break
#        else:
#            print("Pogresan unos! Molimo vas unesite 'N' za nazad.")
#    print("\n")


def overview_of_reserved_tickets(username):
    global reserved_tickets_list
    global cinema_projection_list
    global cinema_screening_term_list

    
    reserved_tickets_read()
    cinema_projection_append()
    cinema_screening_term_append()

    table = PrettyTable()
    table.field_names = ["Br", "Oznaka", "Naziv filma", "Datum", "Vreme pocetka", "Vreme kraja", "Sediste"]
    counter = 1
    for ticket in reserved_tickets_list:
        #print("UnUtraaaaaaa")
        if ticket["username"] == username:

            #projection = next((proj for proj in cinema_projection_list if proj["Password"] == ticket["card_password"][:4]), None)
            #term = next((term for term in cinema_screening_term_list if term["Term_password"] == ticket["card_password"]), None)

            #projection = [proj for proj in cinema_projection_list if proj["Password"] == ticket["card_password"][:4]].split()
            #term = [term for term in cinema_screening_term_list if term["Term_password"] == ticket["card_password"]]
            for projection in cinema_projection_list:
                if projection["Password"] == ticket["card_password"][:4]:
                    for term in cinema_screening_term_list:
                        if term["Term_password"] == ticket["card_password"]:
                            #if term and projection not in table:
                            #    table.add_row([counter, ticket["card_password"], projection["Film"], term["Date"], projection["Time_start"], projection["Time_end"], ticket["seat"]])
                            #    counter += 1
                            
                            exists_in_table = any(
                            row[1] == ticket["card_password"] and row[2] == projection["Film"] and row[3] == term["Date"] and row[4] == projection["Time_start"] and row[5] == projection["Time_end"] and row[6] == ticket["seat"]
                            for row in table._rows
                            )

                            if not exists_in_table:
                                table.add_row([counter, ticket["card_password"], projection["Film"], term["Date"], projection["Time_start"], projection["Time_end"], ticket["seat"]])
                                counter += 1
                                
            #if projection and term:
            #    table.add_row([counter, ticket["card_password"], projection["Film"], term["Date"], projection["Time_start"], projection["Time_end"], ticket["seat"]])
            #    counter += 1
    #:
    #    print("Nemate rezervisanih karti.")

    print(table)
    if not table:
        print("Nemate rezervisanih karti.")

    #while True:
    #    inputN = input("[N] Nazad: ").upper()
    #    if inputN == "N":
    #        break
    #    else:
    #        print("Pogresan unos! Molimo vas unesite 'N' za nazad.")

    #print("\n")

#def cancellation_ticket_reservation(username):
#    global reserved_tickets_list
#    reserved_tickets_read()
#    
#    overview_tickets = []
#    overview_of_reserved_tickets(username)
#    while True:
#        try:
#            del_reservation = int(input("Unesite redni broj rezervacije koju zelite da ponistite: "))
#
#            #if not del_reservation:
#            #    print("Pogresan unos! Molimo vas pokusajte ponovo.")
#            if del_reservation:   #isdigit()
#                del_index = int(del_reservation) - 1
#
#                for ticket in reserved_tickets_list:
#                    if ticket["username"] == username:
#                        overview_tickets.append(ticket)
#
#                if 0 <= del_index <= len(overview_tickets):
#                    for ticket in reserved_tickets_list:
#                        if overview_tickets[del_index] == ticket:
#                            del ticket
#                            with open("reserved_tickets.txt", "w") as file:
#                                for ticket in reserved_tickets_list:
#                                    #file.write("{}|{}|{}|{}|{}\n".format(ticket[0], ticket[1], ticket[2], ticket[3], ticket[4]))
#                                    file.write("{}|{}|{}|{}|{}\n".format(ticket["card_password"], ticket["card_date"], ticket["seat"], ticket["username"], ticket["condition"])) #, ticket["condition"]
#
#
#                            print("Rezervacija uspesno obrisana! \n")
#                            break
#                        
#                    break
#                    
#                else:
#                    print("Nepostojeci redni broj rezervacije! ")
#
#
#            else:
#                print("Pogresan unos! Molimo vas pokusajte ponovo.")
#        except ValueError:
#            print("Pogresan unos! Molimo vas unesite redni broj.")


def cancellation_ticket_reservation(username):
    global reserved_tickets_list
    reserved_tickets_read()
    
    overview_tickets = []
    #overview_of_reserved_tickets(username)
    while True:
        try:
            overview_of_reserved_tickets(username)
            del_reservation = int(input("Unesite redni broj rezervacije koju zelite da ponistite: "))
            overview_tickets = []

            del_reservation_index = del_reservation - 1
            new_reserved_tickets_list = []
            currently_time = datetime.now()
            # Promenljiva za pracenje rezervacija koje su relevantne za korisnika
            overview_tickets = [ticket for ticket in reserved_tickets_list if ticket["username"] == username and datetime.strptime(ticket["card_date"], "%d.%m.%Y.") > currently_time]
            
            if 0 <= del_reservation_index < len(overview_tickets):
                #del_index = del_reservation - 1
                for ticket in reserved_tickets_list:
                    #if overview_tickets[del_reservation] == ticket:
                    if overview_tickets[del_reservation_index] != ticket:
                        new_reserved_tickets_list.append(ticket)
                        
                        #removed_ticket = ticket
                        #reserved_tickets_list.remove(removed_ticket)
                reserved_tickets_list = []     
                with open("reserved_tickets.txt", "w") as file:
                    for ticket in new_reserved_tickets_list:
                        #if ticket != removed_ticket:
                        reserved_tickets_list.append(ticket)
                        #with open("reserved_tickets", "a") as file1:
                        file.write("{}|{}|{}|{}|{}|{}|{}|{}|\n".format(ticket["card_password"], ticket["card_date"], ticket["seat"], ticket["username"], ticket["condition"], ticket["real_date"], ticket["seller_username"], ticket["card_price"]))
                print("Rezervacija uspesno obrisana! \n")
                break


            else:
                print("Nepostojeci redni broj rezervacije! ")


            #else:
            #    print("Pogresan unos! Molimo vas pokusajte ponovo.")
        except ValueError:
            print("Pogresan unos! Molimo vas unesite redni broj.")


user_data_loaded = False
def user_data_append():
    global user_data
    global user_data_loaded

    if user_data_loaded == False:
        user_data = read_user_data()
        user_data_loaded = True
    return user_data

user_data = []
def read_user_data():
    global user_data
    with open("users.txt", "r") as file1:
        lines = file1.readlines()
        for line in lines:
            user_data.append(line.strip().split("|"))
        return user_data

reserved_sold_tickets_list_loaded = False
reserved_sold_tickets_list = []
def overview_of_reserved_tickets_seller():
    global reserved_sold_tickets_list_loaded
    global reserved_sold_tickets_list
    reserved_sold_tickets_list = [] # restartujemo listu
    global reserved_tickets_list
    global cinema_projection_list
    global cinema_screening_term_list

    global user_data
    user_data_append()

    reserved_tickets_read()
    cinema_projection_append()
    cinema_screening_term_append()

    table = PrettyTable()
    table.field_names = ["Br", "Oznaka", "Ime i Prezime", "Naziv filma", "Datum", "Vreme pocetka", "Vreme kraja", "Sediste", "Stanje"]
    counter = 1
    #print("SPOLJAAA")
    for ticket in reserved_tickets_list:
        #print("UNUTRAA")
        user1 = next((user for user in user_data if ticket["username"] == user[0]), None)
        if user1:
        #for user in user_data:
            #if ticket["username"] == user[0]:
                name = user1[2]
                surname = user1[3]
                #projection_key = ticket["card_password"][:4]
                projection = next((proj for proj in cinema_projection_list if proj["Password"] == ticket["card_password"][:4]), None)
                term = next((term for term in cinema_screening_term_list if term["Term_password"] == ticket["card_password"]), None)

                if projection and term:
                    table.add_row([counter, ticket["card_password"], name + " " + surname,  projection["Film"], term["Date"], projection["Time_start"], projection["Time_end"], ticket["seat"], ticket["condition"]])
                    reserved_sold_tickets_list.append(ticket)
                    counter += 1
        else:
            name_and_username = ticket["username"]
            projection = next((proj for proj in cinema_projection_list if proj["Password"] == ticket["card_password"][:4]), None)
            term = next((term for term in cinema_screening_term_list if term["Term_password"] == ticket["card_password"]), None)
            if projection and term:
                table.add_row([counter, ticket["card_password"], name_and_username,  projection["Film"], term["Date"], projection["Time_start"], projection["Time_end"], ticket["seat"], ticket["condition"]])
                reserved_sold_tickets_list.append(ticket)
                counter += 1

    #:
    #    print("Nemate rezervisanih karti.")
    reserved_sold_tickets_list_loaded = True
    print(table)
    if not table:
        print("Nemate rezervisanih karti.")

def cancellation_reserved_sold_tickets():
    global reserved_sold_tickets_list
    global reserved_tickets_list
    global cinema_screening_term_list

    reserved_tickets_read()
    cinema_screening_term_append()

    overview_of_reserved_tickets_seller()
    #for term1 in cinema_screening_term_list:
    #    term = next()
    while True:
        try:
            ticket1_index = int(input("Unesite redni broj karte koju zelite da ponistite: "))
            ticket_index = ticket1_index - 1
            #if 1 <= ticket_index <= len(reserved_tickets_list):
            if 1 <= ticket_index <= len(reserved_sold_tickets_list):
                #reserved_sold_tickets_list.pop(ticket_index)
                for ticket in reserved_tickets_list:
                    if reserved_sold_tickets_list[ticket_index] == ticket:
                        reserved_tickets_list.remove(ticket)
                        reserved_sold_tickets_list.pop(ticket_index)
                with open("reserved_tickets.txt", "w") as file:
                    for ticket in reserved_tickets_list:
                        file.write("{}|{}|{}|{}|{}|{}|{}|{}|\n".format(ticket["card_password"], ticket["card_date"], ticket["seat"], ticket["username"], ticket["condition"], ticket["real_date"], ticket["seller_username"], ticket["card_price"]))
                if ticket["condition"] == "R":
                    print("Uspesno ste obrisali rezervisanu kartu.")
                elif ticket["condition"] == "K":    # Ovde da stavim P za prodate !!!!!!!!
                    print("Uspesno ste obrisali prodatu kartu.")
                break
            else:
                print("Uneli ste nepostojeci redni broj karte! Molimo vas pokusajte ponovo.")


        except ValueError:
            print("Pogresan unos! Molimo vas unesite validan redni broj karte.")


def reserved_sold_tickets_list_read():
    global reserved_sold_tickets_list_loaded
    global reserved_sold_tickets_list
    reserved_sold_tickets_list = [] # resetujemo listu
    global reserved_tickets_list
    global cinema_projection_list
    global cinema_screening_term_list

    global user_data
    user_data_append()

    reserved_tickets_read()
    cinema_projection_append()
    cinema_screening_term_append()

    #table = PrettyTable()
    #table.field_names = ["Br", "Oznaka", "Ime i Prezime", "Naziv filma", "Datum", "Vreme pocetka", "Vreme kraja", "Sediste", "Stanje"]
    #counter = 1
    for ticket in reserved_tickets_list:
        user1 = next((user for user in user_data if ticket["username"] == user[0]), None)
        if user1:
                #name = user1[2]
                #surname = user1[3]
                
                projection = next((proj for proj in cinema_projection_list if proj["Password"] == ticket["card_password"][:4]), None)
                term = next((term for term in cinema_screening_term_list if term["Term_password"] == ticket["card_password"]), None)

                if projection and term:
                    #table.add_row([counter, ticket["card_password"], name + " " + surname,  projection["Film"], term["Date"], projection["Time_start"], projection["Time_end"], ticket["seat"], ticket["condition"]])
                    reserved_sold_tickets_list.append(ticket)
                    #counter += 1
        else:
            #name_and_username = ticket["username"]
            projection = next((proj for proj in cinema_projection_list if proj["Password"] == ticket["card_password"][:4]), None)
            term = next((term for term in cinema_screening_term_list if term["Term_password"] == ticket["card_password"]), None)
            if projection and term:
                #table.add_row([counter, ticket["card_password"], name_and_username,  projection["Film"], term["Date"], projection["Time_start"], projection["Time_end"], ticket["seat"], ticket["condition"]])
                reserved_sold_tickets_list.append(ticket)
                #counter += 1

    #:
    #    print("Nemate rezervisanih karti.")

    #print(table)
    #reserved_sold_tickets_list_loaded = True
    if not reserved_sold_tickets_list:
        #pass
        print("Nema rezervisanih/prodatih karti.")

def reserved_sold_tickets_list_append():
    global reserved_sold_tickets_list
    global reserved_sold_tickets_list_loaded

    if not reserved_sold_tickets_list_loaded:
        reserved_sold_tickets_list_read()
        reserved_sold_tickets_list_loaded = True
        return reserved_sold_tickets_list_read() 
    
###def multicriteria_search_tickets():
###    global reserved_sold_tickets_list
###    reserved_sold_tickets_list_append()
###
###    global cinema_screening_term_list
###    cinema_screening_term_append()
###
###    global user_data_append
###    user_data_append()
###
###    search_tickets_list = []
###    print("Visekriterijumska pretraga karata. ")
###    print("Unesite kriterijume pretrage (ili pritisnite Enter da preskocite): ")
###    criterions = {
###        "ticket_password": input("Unesite sifru projekcije: ").strip().upper(),
###        "ticket_name": input("Unesite ime kupca: ").strip(),
###        "ticket_surname": input("Unesite prezime kupca: ").strip(),
###        "ticket_date": input("Unesite datum karte: ").strip(),
###        "ticket_start_time": input("Unesite vreme pocetka karte: ").strip(),
###        "ticket_end_time": input("Unesite vreme kraja karte: ").strip(),
###        "ticket_condition": input("Unesite stanje karte (R ili K): ").strip()
###    }
###    table = PrettyTable()
###    table.field_names = ["Br", "Sifra projekcije", "Ime", "Prezime", "Naziv filma", "Datum", "Vreme pocetka", "Vreme kraja", "Sediste", "Stanje"]
###    counter = 1
###    for ticket in reserved_sold_tickets_list:
###        #name = next((name1 for name1 in ), None)
###        #user1 = next((user for user in user_data if ticket["username"] == user[0]), None)
###        term = next((term for term in cinema_screening_term_list if term["Term_password"] == ticket["card_password"]), None)
###        #name = next((user1[2] for user1 in user_data if ticket["username"] == user1[0]), None)
###        #surname = next((user1[3] for user1 in user_data if ticket["username"] == user1[0]), None)
###
###        apart_line = ticket["username"].split("")
###        name = apart_line[0]
###        surname = apart_line[1]
###
###        #if user1:
###
###        for user in user_data:
###        #    name = user1[2]
###        #    surname = user1[3]
###        #name = user1[2] for user1 in user_data else None
###            if user[2] == name and user[3] == surname:
###        
###                if (
###                    (not criterions["ticket_password"] or criterions["ticket_password"] == ticket["card_password"].upper()) or
###                    (not criterions["ticket_name"] or criterions["ticket_name"] == user[2]) or  
###                    (not criterions["ticket_surname"] or criterions["ticket_surname"] == user[3]) or 
###                    (not criterions["ticket_date"] or criterions["ticket_date"] == ticket["card_date"]) or
###                    #(not criterions["ticket_start_time"] or criterions["ticket_start_time"] == ) or 
###                    #(not criterions["ticket_end_time"] or criterions["ticket_end_time"] == ) or
###                    (not criterions["ticket_condition"] or criterions["ticket_condition"] == ticket["condition"]) 
###                ):
###                    search_tickets_list.append(ticket)
###                    table.add_row([counter, ticket["card_password"], user[2], user[3], "Naziv filma", ticket["card_date"], "vreme_pocetka", "vreme_kraja", ticket["seat"], ticket["condition"]])
###                    counter += 1
###    #table = PrettyTable()
###    #table.field_names = ["Br", "Sifra projekcije", "Ime", "Prezime", "Naziv filma", "Datum", "Vreme pocetka", "Vreme kraja", "Sediste", "Stanje"]#
###
###    #counter = 1
###    #for search_ticket in search_tickets_list:
###    #    table.add_row([counter, search_ticket["card_password"], user[2], user[3], "Naziv filma", search_ticket["card_date"], "vreme_pocetka", "vreme_kraja", search_ticket["seat"], search_ticket["condition"]])
###    #    counter += 1
###    
###    print(table)

search_tickets_list = []
def multicriteria_search_tickets(sale_reserved_ticket):     # drugi nacin za funkciju
    global reserved_sold_tickets_list_loaded
    global reserved_sold_tickets_list
    global search_tickets_list
    reserved_sold_tickets_list_append()
    #reserved_sold_tickets_list = [] # restartujemo listu
    global reserved_tickets_list
    global cinema_projection_list
    global cinema_screening_term_list

    global user_data
    user_data_append()

    reserved_tickets_read()
    cinema_projection_append()
    cinema_screening_term_append()



    search_tickets_list = []
    print("\n Visekriterijumska pretraga karata. ")
    print("Unesite kriterijume pretrage (ili pritisnite Enter da preskocite): ")
    criterions = {
        "ticket_password": input("Unesite sifru projekcije: ").strip().upper(),
        "ticket_name": input("Unesite ime kupca: ").strip().upper(),
        "ticket_surname": input("Unesite prezime kupca: ").strip().upper(),
        "ticket_date": ticket_date_valid(),          #input("Unesite datum karte (dd.mm.yyyy.): ").strip().upper(),
        "ticket_start_time": ticket_start_time_valid(),    #input("Unesite vreme pocetka karte: ").strip().upper(),
        "ticket_end_time": ticket_end_time_valid(),      #input("Unesite vreme kraja karte: ").strip().upper(),
        "ticket_condition": ""
    }
    if sale_reserved_ticket == True:
        criterions["ticket_condition"] = "R"
        sale_reserved_ticket = False
    else:
        criterions["ticket_condition"] = input("Unesite stanje karte (R ili K): ").strip().upper()


    #date_valid(criterions)
    #start_time_valid(criterions)
    #
    # end_time_valid(criterions)

    table = PrettyTable()
    table.field_names = ["Br", "Sifra projekcije", "Ime", "Prezime", "Naziv filma", "Datum", "Vreme pocetka", "Vreme kraja", "Sediste", "Stanje"]
    counter = 1



    #table = PrettyTable()
    #table.field_names = ["Br", "Oznaka", "Ime i Prezime", "Naziv filma", "Datum", "Vreme pocetka", "Vreme kraja", "Sediste", "Stanje"]
    #counter = 1
    for ticket in reserved_tickets_list:
        user1 = next((user for user in user_data if ticket["username"] == user[0]), None)
        if user1:
        #for user in user_data:
            #if ticket["username"] == user[0]:
                name = user1[2]
                surname = user1[3]
                #projection_key = ticket["card_password"][:4]
                projection = next((proj for proj in cinema_projection_list if proj["Password"] == ticket["card_password"][:4]), None)
                term = next((term for term in cinema_screening_term_list if term["Term_password"] == ticket["card_password"]), None)

                if projection and term:
                    if (
                    (not criterions["ticket_password"] or criterions["ticket_password"] == ticket["card_password"].upper()) and
                    (not criterions["ticket_name"] or criterions["ticket_name"] == name.upper()) and
                    (not criterions["ticket_surname"] or criterions["ticket_surname"] == surname.upper()) and
                    (not criterions["ticket_date"] or datetime.strptime(criterions["ticket_date"], "%d.%m.%Y.") == datetime.strptime(ticket["card_date"], "%d.%m.%Y.")) and
                    (not criterions["ticket_start_time"] or datetime.strptime(criterions["ticket_start_time"], "%H:%M") <= datetime.strptime(projection["Time_start"], "%H:%M")) and 
                    (not criterions["ticket_end_time"] or datetime.strptime(criterions["ticket_end_time"], "%H:%M") >= datetime.strptime(projection["Time_end"], "%H:%M")) and
                    (not criterions["ticket_condition"] or criterions["ticket_condition"] == ticket["condition"].upper()) 
                ):
                    #search_tickets_list.append(ticket)
                        table.add_row([counter, ticket["card_password"], name, surname, projection["Film"], ticket["card_date"], projection["Time_start"], projection["Time_end"], ticket["seat"], ticket["condition"]])
                        counter += 1
                        search_ticket = {
                            "search_counter": counter,
                            "search_password": ticket["card_password"],
                            "search_name": name,
                            "search_surname": surname,
                            "search_film": projection["Film"],
                            "search_date": ticket["card_date"],
                            "search_time_start": projection["Time_start"],
                            "search_time_end": projection["Time_end"],
                            "search_seat": ticket["seat"],
                            "search_condition": ticket["condition"]

                        }
                        search_tickets_list.append(search_ticket)

                    #table.add_row([counter, ticket["card_password"], name + " " + surname,  projection["Film"], term["Date"], projection["Time_start"], projection["Time_end"], ticket["seat"], ticket["condition"]])
                    #reserved_sold_tickets_list.append(ticket)
                    #counter += 1
        else:
            name_and_surname = ticket["username"]
            apart_line = name_and_surname.split(" ")
            #print("Duzina od apart_line prvi je: ", len(apart_line))
            if len(apart_line) >= 2:
                name = apart_line[0]
                surname = apart_line[1]
                projection = next((proj for proj in cinema_projection_list if proj["Password"] == ticket["card_password"][:4]), None)
                term = next((term for term in cinema_screening_term_list if term["Term_password"] == ticket["card_password"]), None)
                if projection and term:
                    if (
                        (not criterions["ticket_password"] or criterions["ticket_password"] == ticket["card_password"].upper()) and
                        (not criterions["ticket_name"] or criterions["ticket_name"] == name.upper()) and  
                        (not criterions["ticket_surname"] or criterions["ticket_surname"] == surname.upper()) and
                        (not criterions["ticket_date"] or datetime.strptime(criterions["ticket_date"], "%d.%m.%Y.") == datetime.strptime(ticket["card_date"], "%d.%m.%Y.")) and
                        (not criterions["ticket_start_time"] or datetime.strptime(criterions["ticket_start_time"], "%H:%M") <= datetime.strptime(projection["Time_start"], "%H:%M")) and 
                        (not criterions["ticket_end_time"] or datetime.strptime(criterions["ticket_end_time"], "%H:%M") >= datetime.strptime(projection["Time_end"], "%H:%M")) and
                        (not criterions["ticket_condition"] or criterions["ticket_condition"] == ticket["condition"].upper()) 
                    ):
                        #search_tickets_list.append(ticket)
                            table.add_row([counter, ticket["card_password"], name, surname, projection["Film"], ticket["card_date"], projection["Time_start"], projection["Time_end"], ticket["seat"], ticket["condition"]])
                            counter += 1
                            search_ticket = {
                            "search_counter": counter,
                            "search_password": ticket["card_password"],
                            "search_name": name,
                            "search_surname": surname,
                            "search_film": projection["Film"],
                            "search_date": ticket["card_date"],
                            "search_time_start": projection["Time_start"],
                            "search_time_end": projection["Time_end"],
                            "search_seat": ticket["seat"],
                            "search_condition": ticket["condition"]
                            }
                            search_tickets_list.append(search_ticket)
                    #table.add_row([counter, ticket["card_password"], name_and_surname,  projection["Film"], term["Date"], projection["Time_start"], projection["Time_end"], ticket["seat"], ticket["condition"]])
                    #reserved_sold_tickets_list.append(ticket)
                    #counter += 1
            else:
                #print("Duzina od apart_line drugi je:", len(apart_line))
                name = apart_line[0]
                #surname = apart_line[1]
                projection = next((proj for proj in cinema_projection_list if proj["Password"] == ticket["card_password"][:4]), None)
                term = next((term for term in cinema_screening_term_list if term["Term_password"] == ticket["card_password"]), None)
                if projection and term:
                    if (
                        (not criterions["ticket_password"] or criterions["ticket_password"] == ticket["card_password"].upper()) and
                        (not criterions["ticket_name"] or criterions["ticket_name"] == name) and  
                        (not criterions["ticket_surname"] or criterions["ticket_surname"] == name) and 
                        (not criterions["ticket_date"] or datetime.strptime(criterions["ticket_date"], "%d.%m.%Y.") == datetime.strptime(ticket["card_date"], "%d.%m.%Y.")) and
                        (not criterions["ticket_start_time"] or datetime.strptime(criterions["ticket_start_time"], "%H:%M") <= datetime.strptime(projection["Time_start"], "%H:%M")) and 
                        (not criterions["ticket_end_time"] or datetime.strptime(criterions["ticket_end_time"], "%H:%M") >= datetime.strptime(projection["Time_end"], "%H:%M")) and
                        (not criterions["ticket_condition"] or criterions["ticket_condition"] == ticket["condition"]) 
                    ):
                        #search_tickets_list.append(ticket)
                            table.add_row([counter, ticket["card_password"], name, name, "Naziv filma", ticket["card_date"], "vreme_pocetka", "vreme_kraja", ticket["seat"], ticket["condition"]])
                            counter += 1
                            search_ticket = {
                            "search_counter": counter,
                            "search_password": ticket["card_password"],
                            "search_name": name,
                            "search_surname": surname,
                            "search_film": projection["Film"],
                            "search_date": ticket["card_date"],
                            "search_time_start": projection["Time_start"],
                            "search_time_end": projection["Time_end"],
                            "search_seat": ticket["seat"],
                            "search_condition": ticket["condition"]
                            }
                            search_tickets_list.append(search_ticket)
                    #table.add_row([counter, ticket["card_password"], name_and_surname,  projection["Film"], term["Date"], projection["Time_start"], projection["Time_end"], ticket["seat"], ticket["condition"]])
                    #reserved_sold_tickets_list.append(ticket)
                    #counter += 1

    #:
    #    print("Nemate rezervisanih karti.")
    #reserved_sold_tickets_list_loaded = True
    print(table)
    if not table:
        print("Nemate rezervisanih karti.")

def ticket_date_valid():
    while True:
        ticket_date = input("Unesite datum karte (dd.mm.yyyy.): ").strip()
        if not ticket_date:
            break
        elif len(ticket_date) == 11 and ticket_date[:2].isdigit() and ticket_date[2] == "." and ticket_date[3:5].isdigit() and ticket_date[5] == "." and ticket_date[6:10].isdigit() and ticket_date[10] == ".":
            while True:
                try:
                    ticket_date = datetime.strptime(ticket_date, "%d.%m.%Y.").strftime("%d.%m.%Y.")
                    return ticket_date
                    
                except ValueError:
                    print("Pogresan unos! Molimo vas unesite validan datum.")
                    ticket_date = input("Unesite datum karte (dd.mm.yyyy.): ").upper()
        else:
            print("Pogresan unos! Unesite datum u trazenom formatu.")

def ticket_start_time_valid():        
    while True:
        ticket_start_time = input("Unesite vreme pocetka karte: ").strip().upper()
        if not ticket_start_time:
            break
        elif len(ticket_start_time) == 5 and ticket_start_time[:2].isdigit() and ticket_start_time[2] == ":" and ticket_start_time[3:].isdigit():
            while True:
                try:
                    datetime.strptime(ticket_start_time, "%H:%M")
                    return ticket_start_time
                    
                except ValueError:
                    print("Pogresan unos! Molimo vas unesite validno vreme pocetka.")
                    ticket_start_time = input("Unesite vreme pocetka karte: ").strip().upper()
        else:
            print("Pogresan unos! Unesite vreme u trazenom formatu.")

def ticket_end_time_valid():    
    while True:
        ticket_end_time = input("Unesite vreme kraja karte: ").strip().upper()
        if not ticket_end_time:
            break
        elif len(ticket_end_time) == 5 and ticket_end_time[:2].isdigit() and ticket_end_time[2] == ":" and ticket_end_time[3:].isdigit():
            while True:
                try:
                    datetime.strptime(ticket_end_time, "%H:%M")
                    return ticket_end_time
                    
                except ValueError:
                    print("Pogresan unos! Molimo vas unesite validno vreme kraja.")
                    ticket_end_time = input("Unesite vreme kraja karte: ").strip().upper()
        else:
            print("Pogresan unos! Unesite vreme u trazenom formatu.")

def sale_reserved_ticketsf(seller_username):
    new_seller_username = seller_username
    global reserved_tickets_list
    global search_tickets_list
    sale_reserved_ticket = True
    multicriteria_search_tickets(sale_reserved_ticket)
    sale_reserved_ticket_condition = False
    sale_reserved_tickets_list = []
    while True:
    
        sale_ticket = input("Unesite redni broj karte koju zelite da prodate ([N] Nazad): ").strip()
        if not sale_ticket:
            print("Pogresan unos! Molimo vas pokusajte ponovo.")
        
        elif sale_ticket.upper() == "N":
            break

        elif sale_ticket.isdigit():
            for search_ticket in search_tickets_list:
                if int(int(sale_ticket) + 1) == search_ticket["search_counter"]:
                    search_ticket["search_condition"] = "K"
                    for ticket in reserved_tickets_list:
                        if ticket["card_password"] == search_ticket["search_password"] and ticket["seat"] == search_ticket["search_seat"]:
                            ticket["condition"] = "K"
                            
                            with open("reserved_tickets.txt", "r") as file:
                                lines = file.readlines()
                                #with open("reserved_tickets.txt", "w") as file1:
                                for line in lines:
                                    apart_line = line.split("|")
                                    ticket_password = apart_line[0]
                                    ticket_date = apart_line[1]
                                    ticket_seat = apart_line[2]
                                    ticket_username = apart_line[3]
                                    ticket_condition = apart_line[4]
                                    real_date = apart_line[5]
                                    seller_username = apart_line[6]
                                    card_price = apart_line[7]
                                    if ticket_password == search_ticket["search_password"] and ticket_seat == search_ticket["search_seat"]:
                                        ticket_condition = "K"
                                        seller_username = f"{new_seller_username}"  #####################################

                                        sale_reserved_ticket_condition = True
                                    new_reserved_ticket = {
                                        "ticket_password":ticket_password, 
                                        "ticket_date":ticket_date,
                                        "ticket_seat":ticket_seat,
                                        "ticket_username":ticket_username,
                                        "ticket_condition":ticket_condition,
                                        "ticket_real_date": real_date,
                                        "ticket_seller_username": seller_username,
                                        "ticket_card_price": card_price

                                    }
                                    sale_reserved_tickets_list.append(new_reserved_ticket)
                                    
                                    with open("reserved_tickets.txt", "w") as file1:
                                        pass
                    with open("reserved_tickets.txt", "a") as file1:
                        for new_reserved_ticket in sale_reserved_tickets_list:
                            file1.write("{}|{}|{}|{}|{}|{}|{}|{}|\n" .format(new_reserved_ticket["ticket_password"], new_reserved_ticket["ticket_date"], new_reserved_ticket["ticket_seat"], new_reserved_ticket["ticket_username"], new_reserved_ticket["ticket_condition"], new_reserved_ticket["ticket_real_date"], new_reserved_ticket["ticket_seller_username"], new_reserved_ticket["ticket_card_price"]))
                    break
                #break
            if sale_reserved_ticket_condition == False:
                print("Redni broj koji ste uneli nije dat u tabeli! Pokusajte ponovo.")
            #else:
            #print("Redni broj koji ste uneli nije dat u tabeli! Pokusajte ponovo.")            
            #with open("reserved_tickets.txt", "r") as file:
            #    lines = file.readlines()
            #    with open("reserved_tickets.txt", "w") as file1:
            #        for line in lines:
            #            apart_line = line.split("|")
            #            ticket_password = apart_line[0]
            #            ticket_date = apart_line[1]
            #            ticket_seat = apart_line[2]
            #            ticket_username = apart_line[3]
            #            ticket_condition = apart_line[4]
            #            if ticket_password == search_ticket["search_password"] and ticket_seat == search_ticket["search_seat"]:
            #                ticket_condition = "K"
            #            #with open("reserved_tickets.txt", "w") as file1:
            #                file1.write("{}|{}|{}|{}|{}" .format(ticket_password, ticket_date, ticket_seat, ticket_username, ticket_condition))


                                #break

            
            #else:
            #    print("Redni broj koji ste uneli nije dat u tabeli! Pokusajte ponovo.")
                
            break
        else:
            print("Pogresan unos! Molimo vas pokusajte ponovo.")
    #except ValueError:print("Pogresan unos! Molimo vas pokusajte ponovo.")
            


def ticket_changed(username, condition):
    global reserved_tickets_list
    ######reserved_tickets_list = load_reserved_cards()
    reserved_tickets_read()


    #while True:
    #    input_password = input("Unesite sifru projekcije: ").upper().strip()
    #    found, password = get_password_projection(input_password)
    #    if found:
    #        break
    cinema_screening_term_append()
    while True:
        input_password = input("Unesite šifru projekcije: ").upper().strip()
        seat_available, card_password, card_date = search_projection_by_password(input_password)
        if seat_available == True:
            #rows, columns = overview_of_available_seats(input_password)
            seat_info = overview_of_available_seats(input_password)
            if seat_info is not None:
                rows, columns = seat_info
                seat_matrix = generate_seat_matrix(rows, columns, card_password)       
                matrix(seat_matrix, rows, columns, card_password, card_date, username, condition)
                update_matrix_with_reservations(seat_matrix, reserved_tickets_list, card_password)
            else:
                print("Nisu pronađeni podaci o sedištima za unetu šifru projekcije.")
            break
        else:
            print("Pogresan unos! Molimo vas pokusajte ponovo. ")
            #search_projection_by_password(input_password, projections)
            #enter_projection_by_password()

def change_process_tickets():
    fill_list_append()
    global all_tickets_list

    #global lista_filmova
    #read_film_file()
    with open("reserved_tickets.txt", "w") as file:
        pass #(" ")
    with open("reserved_tickets.txt", "a") as file1:
        #counter = 1
        for ticket_all in all_tickets_list:
            #print(counter, ticket_all["ticket_all_username"], ticket_all["ticket_all_card_price"])
            #counter += 1
            file1.write("{}|{}|{}|{}|{}|{}|{}|{}|\n" .format(ticket_all["ticket_all_password"], ticket_all["ticket_all_date"], ticket_all["ticket_all_seat"], ticket_all["ticket_all_username"], ticket_all["ticket_all_condition"], ticket_all["ticket_all_real_date"], ticket_all["ticket_all_seller_username"], ticket_all["ticket_all_card_price"]))


def ticket_change():
    global cinema_screening_term_list
    cinema_screening_term_append()
    global user_data
    user_data_append()
    global reserved_tickets_list
    global search_tickets_list
    sale_reserved_ticket = False
    #multicriteria_search_tickets(sale_reserved_ticket)
    sale_reserved_ticket_condition = False

    global all_tickets_list
    fill_list_append()
    #global all_tickets_list

    user_exist = 0
    
    changed_tickets_list = []
    while True:
        multicriteria_search_tickets(sale_reserved_ticket)
        change_ticket = input("Unesite redni broj karte koju zelite da izmenite ([N] Nazad): ").strip()
        if not change_ticket:
            print("Pogresan unos! Molimo vas pokusajte ponovo.")
        
        elif change_ticket.upper() == "N":
            break

        elif change_ticket.isdigit():
            for search_ticket in search_tickets_list:
                if 0 <= (int(change_ticket) - 1) < len(search_tickets_list):

                    if int(int(change_ticket) + 1) == search_ticket["search_counter"]:
                        #search_ticket["search_condition"] = "K"
                        for ticket in reserved_tickets_list:
                            if ticket["card_password"] == search_ticket["search_password"] and ticket["seat"] == search_ticket["search_seat"]:
                                #ticket["condition"] = "K"








                                user = next((user for user in user_data if user[0] == ticket["username"]), None)
                                if user:
                                    user_exist = 1
                                    while True:
                                        print("Sta zelite da izmenite?")
                                        print("[1] Termin bioskopske projekcije")
                                        print("[2] Sediste")
                                        print("[N] Nazad")
                                        choose_option = input("Izaberite opciju: ").strip()
                                        if choose_option == "1":
                                            while True:
                                                ticket_all = next((all_ticket for all_ticket in all_tickets_list if all_ticket["ticket_all_password"] == ticket["card_password"] and all_ticket["ticket_all_seat"] == ticket["seat"]), None)
                                                overview_of_available_terms()
                                                change_term = input("Unesite novu sifru termina : ").strip().upper()

                                                #ticket_all["ticket_all_password"] = change_term

                                                for term in cinema_screening_term_list:
                                                    if term["Term_password"] == change_term:
                                                        ticket["card_password"] = change_term
                                                        ticket_all["ticket_all_password"] = change_term
                                                        change_process_tickets()
                                                        print("Uspesno ste izmenili sifru termina.")
                                                        while True:
                                                            inputN = input("[N] Nazad: ").strip().upper()
                                                            if inputN == "N":
                                                                break
                                                            else:
                                                                print("Pogresan unos! Pokusajte ponovo.")
                                                        break
                                                #break
                                                else:
                                                    print("Pogresan unos! Pokusajte ponovo.")
                                                break
                                            
                                        elif choose_option == "2":
                                            
                                            old_seat = ticket["seat"]
                                            password = ticket["card_password"]
                                            seat_info = overview_of_available_seats(password)
                                            if seat_info is not None:
                                                rows, columns = seat_info
                                                seat_matrix = generate_seat_matrix(rows, columns, password)

                                            #seat_matrix = generate_seat_matrix(rows, columns, password)
                                            print("Matrica slobodnih sedišta:")
                                            print_seat_matrix(seat_matrix)

                                            while True:
                                            #try:
                                                seat = input("Unesite oznaku sedista (na primer 3F): ").strip().upper()
                                                if not seat:
                                                    print("Pogresan unos! Molimo vas unesite validno sediste.")

                                                elif seat[:-1].isdigit() and seat[-1].isalpha():
                                                #print("Pogresan unos! Molimo vas pokusajte ponovo.")

                                                    row_number = int(seat[:-1]) - 1
                                                    column_letter = seat[-1]
                                                    try:
                                                        if seat_matrix[row_number][ord(column_letter) - ord('A')] == "X":
                                                            print("Sediste je zauzeto! Molimo vas izaberite drugo sediste.")
                                                        elif 0 <= row_number < rows and 'A' <= column_letter <= chr(ord('A') + columns - 1):
                                                            seat_matrix[row_number][ord(column_letter) - ord('A')] = "X"
                                                            if ticket["condition"] == "R":
                                                                print("Uspesno ste izmenili rezervisanu kartu.")
                                                            elif ticket["condition"] == "K":
                                                                print("Uspesno ste izmenili kupljenu kartu.")
                                                            add_reserved_cards_change(seat, ticket["card_password"], ticket["card_date"], ticket["username"], ticket["condition"], ticket["seller_username"], ticket["real_date"], ticket["card_price"])

                                                            ticket1 = next((ticket1 for ticket1 in reserved_tickets_list if ticket1["seat"] == old_seat and ticket1["card_password"] == ticket["card_password"]), None)

                                                            if ticket1 is not None and ticket == ticket1:
                                                                #print("Nasao sam takvu kartu i obrisao je!")
                                                                #reserved_tickets_list.remove(ticket)
                                                                ticket_all = next((ticket_all for ticket_all in all_tickets_list if ticket_all["ticket_all_seat"] == old_seat and ticket_all["ticket_all_password"] == ticket["card_password"]), None)
                                                                reserved_tickets_list.remove(ticket)
                                                                all_tickets_list.remove(ticket_all)
                                                                change_process_tickets()
                                                                while True:
                                                                    inputN = input("[N] Nazad: ").strip().upper()
                                                                    if inputN == "N":
                                                                        break
                                                                    else:
                                                                        print("Pogresan unos! Pokusajte ponovo.")
                                                                break

                                                            else:
                                                                print("Ne postoji ta karta")
                                                            #all_tickets_list.remove(ticket1)
                                                            update_matrix_with_reservations(seat_matrix, reserved_tickets_list, ticket["card_password"])
                                                            break
                                                    except IndexError:
                                                        print("Sediste nije dostupno!")
                                                        #else:
                                                        #    print("Sediste nije dostupno!")


                                        









#                                            same_username = user[0]
#                                            same_condition = ticket["condition"]
#                                            same_seller_username = ticket["seller_username"]
#                                            #ticket_reservation(same_username, same_condition)
#                                                #ticket_reservation(username, condition)
#                                                    #elif:
                                        elif choose_option.upper() == "N":
                                            break
                                        else:
                                            print("Pogresan unos! Pokusajte ponovo.")
                                        break

                                else:
                                    user_exist = 2
                                    #same_condition2 = ticket["condition"]
                                    #same_seller_username2 = ticket["seller_username"]
                                    while True:
                                        print("Sta zelite da izmenite?")
                                        print("[1] Termin bioskopske projekcije")
                                        print("[2] Ime i prezime")
                                        print("[3] Sediste")
                                        print("[N] Nazad")
                                        input_option = input("Izaberite opciju: ").strip()
                                        if input_option == "1":
                                            while True:
                                                ticket_all = next((all_ticket for all_ticket in all_tickets_list if all_ticket["ticket_all_password"] == ticket["card_password"] and all_ticket["ticket_all_seat"] == ticket["seat"]), None)
                                                overview_of_available_terms()
                                                change_term = input("Unesite novu sifru termina : ").strip().upper()

                                                #ticket_all["ticket_all_password"] = change_term

                                                for term in cinema_screening_term_list:
                                                    if term["Term_password"] == change_term:
                                                        ticket["card_password"] = change_term
                                                        ticket_all["ticket_all_password"] = change_term
                                                        change_process_tickets()
                                                        print("Uspesno ste izmenili sifru termina.")
                                                        while True:
                                                            inputN = input("[N] Nazad: ").strip().upper()
                                                            if inputN == "N":
                                                                break
                                                            else:
                                                                print("Pogresan unos! Pokusajte ponovo.")
                                                        break
                                                #break
                                                else:
                                                    print("Pogresan unos! Pokusajte ponovo.")
                                                break
                                        
                                        elif input_option == "2":
                                            while True:
                                                ticket_all = next((all_ticket for all_ticket in all_tickets_list if all_ticket["ticket_all_password"] == ticket["card_password"] and all_ticket["ticket_all_seat"] == ticket["seat"]), None)
                                                #overview_of_available_terms()
                                                while True:
                                                    change_name = input("Unesite novo ime: ").strip()
                                                    if change_name.isalpha():
                                                        break
                                                    else:
                                                        print("Pogresan unos! Pokusajte ponovo.")
                                                while True:
                                                    change_surname = input("Unesite novo prezime: ").strip()
                                                    if change_surname.isalpha():
                                                        break
                                                    else:
                                                        print("Pogresan unos! Pokusajte ponovo.")

                                                username = change_name + " " + change_surname

                                                #ticket_all["ticket_all_password"] = change_term

                                                #for term in cinema_screening_term_list:
                                                #    if term["Term_password"] == change_term:
                                                ticket["username"] = username
                                                ticket_all["ticket_all_username"] = username
                                                change_process_tickets()
                                                print("Uspesno ste izmenili ime i prezime.")
                                                while True:
                                                    inputN = input("[N] Nazad: ").strip().upper()
                                                    if inputN == "N":
                                                        break
                                                    else:
                                                        print("Pogresan unos! Pokusajte ponovo.")
                                                        
                                                #break
                                                else:
                                                    print("Pogresan unos! Pokusajte ponovo.")
                                                break

                                        elif input_option == "3":
                                            old_seat = ticket["seat"]
                                            password = ticket["card_password"]
                                            seat_info = overview_of_available_seats(password)
                                            if seat_info is not None:
                                                rows, columns = seat_info
                                                seat_matrix = generate_seat_matrix(rows, columns, password)

                                            #seat_matrix = generate_seat_matrix(rows, columns, password)
                                            print("Matrica slobodnih sedišta:")
                                            print_seat_matrix(seat_matrix)

                                            while True:
                                            #try:
                                                seat = input("Unesite oznaku sedista (na primer 3F): ").strip().upper()
                                                if not seat:
                                                    print("Pogresan unos! Molimo vas unesite validno sediste.")

                                                elif seat[:-1].isdigit() and seat[-1].isalpha():
                                                #print("Pogresan unos! Molimo vas pokusajte ponovo.")

                                                    row_number = int(seat[:-1]) - 1
                                                    column_letter = seat[-1]
                                                    try:
                                                        if seat_matrix[row_number][ord(column_letter) - ord('A')] == "X":
                                                            print("Sediste je zauzeto! Molimo vas izaberite drugo sediste.")
                                                        elif 0 <= row_number < rows and 'A' <= column_letter <= chr(ord('A') + columns - 1):
                                                            seat_matrix[row_number][ord(column_letter) - ord('A')] = "X"
                                                            if ticket["condition"] == "R":
                                                                print("Uspesno ste izmenili rezervisanu kartu.")
                                                            elif ticket["condition"] == "K":
                                                                print("Uspesno ste izmenili kupljenu kartu.")
                                                            add_reserved_cards_change(seat, ticket["card_password"], ticket["card_date"], ticket["username"], ticket["condition"], ticket["seller_username"], ticket["real_date"], ticket["card_price"])

                                                            ticket1 = next((ticket1 for ticket1 in reserved_tickets_list if ticket1["seat"] == old_seat and ticket1["card_password"] == ticket["card_password"]), None)

                                                            if ticket1 is not None and ticket == ticket1:
                                                                #print("Nasao sam takvu kartu i obrisao je!")
                                                                #reserved_tickets_list.remove(ticket)
                                                                ticket_all = next((ticket_all for ticket_all in all_tickets_list if ticket_all["ticket_all_seat"] == old_seat and ticket_all["ticket_all_password"] == ticket["card_password"]), None)
                                                                reserved_tickets_list.remove(ticket)
                                                                all_tickets_list.remove(ticket_all)
                                                                change_process_tickets()
                                                                while True:
                                                                    inputN = input("[N] Nazad: ").strip().upper()
                                                                    if inputN == "N":
                                                                        break
                                                                    else:
                                                                        print("Pogresan unos! Pokusajte ponovo.")
                                                                break

                                                            else:
                                                                print("Ne postoji ta karta")
                                                            #all_tickets_list.remove(ticket1)
                                                            update_matrix_with_reservations(seat_matrix, reserved_tickets_list, ticket["card_password"])
                                                            break
                                                    except IndexError:
                                                        print("Sediste nije dostupno!")
                                                        #else:
                                                        #    print("Sediste nije dostupno!")


                                        









#                                            
                                        #elif choose_option.upper() == "N":
                                        #    break
                                        #else:
                                        #    print("Pogresan unos! Pokusajte ponovo.")
                                        #break







                                        elif input_option == "3":
                                            pass
                                        elif input_option.upper() == "N":
                                            break
                







                else:
                    print("Redni broj koji ste uneli nije dat u tabeli! Pokusajte ponovo.")
                    while True:
                        inputN = input("[N] Nazad: ").strip().upper()
                        if inputN == "N":
                            break
                        else:
                            print("Pogresan unos! Pokusajte ponovo.")
                    #break

                                #new_ticket_password = input("Unesite novu sifru karte: ")

#                                with open("reserved_tickets.txt", "r") as file:
#                                    lines = file.readlines()
#                                    #with open("reserved_tickets.txt", "w") as file1:
#                                    for line in lines:
#                                        apart_line = line.split("|")
#                                        ticket_password = apart_line[0]
#                                        ticket_date = apart_line[1]
#                                        ticket_seat = apart_line[2]
#                                        ticket_username = apart_line[3]
#                                        ticket_condition = apart_line[4]
#                                        ticket_real_date = apart_line[5]
#                                        ticket_seller_username = apart_line[6]
#                                        ticket_card_price = apart_line[7]
#                                        if ticket_password == search_ticket["search_password"] and ticket_seat == search_ticket["search_seat"]:
#                                            #ticket_condition = "K"
#                                            changed_ticket_condition = True
#                                            reserved_tickets_list.remove(ticket)
#                                            user = next((user for user in user_data if user[0] == ticket["username"]), None)
#                                            #for user in user_data:
#                                                #if user[0] == ticket["username"]:
#                                            if user:
#                                                user_exist = 1
#                                                same_username = user[0]
#                                                same_condition = ticket["condition"]
#                                                same_seller_username = ticket["seller_username"]
#                                                #ticket_reservation(same_username, same_condition)
#                                                    #ticket_reservation(username, condition)
#                                            #elif:
#                                            else:
#                                                user_exist = 2
#                                                same_condition2 = ticket["condition"]
#                                                same_seller_username2 = ticket["seller_username"]
#                                            
#                                            #else:
#                                            #    print("Nismo pronasli kartu.")
#                                        else:
#                                            changed_ticket = {
#                                                "ticket_password":ticket_password, 
#                                                "ticket_date":ticket_date,
#                                                "ticket_seat":ticket_seat,
#                                                "ticket_username":ticket_username,
#                                                "ticket_condition":ticket_condition,
#                                                "ticket_real_date":ticket_real_date,
#                                                "ticket_seller_username": ticket_seller_username,
#                                                "ticket_card_price": ticket_card_price
#   
#                                            }
#                                            changed_tickets_list.append(changed_ticket)
#   
#                                            #with open("reserved_tickets.txt", "w") as file1:
#                                            #    pass
#                                    with open("reserved_tickets.txt", "w") as file1:
#                                        pass
#                        with open("reserved_tickets.txt", "a") as file1:
#                            for changed_ticket in changed_tickets_list:
#                                file1.write("{}|{}|{}|{}|{}|{}|{}|{}|\n" .format(changed_ticket["ticket_password"], changed_ticket["ticket_date"], changed_ticket["ticket_seat"], changed_ticket["ticket_username"], changed_ticket["ticket_condition"], changed_ticket["ticket_real_date"], changed_ticket["ticket_seller_username"], change_ticket["ticket_card_price"]))
#                            
#                        break
#                    #break
#            if changed_ticket_condition == False:
#                print("Redni broj koji ste uneli nije dat u tabeli! Pokusajte ponovo.")
#            
#            if user_exist == 1:
#                #username = user[0]
#                #condition = ticket["condition"]
#                ticket_reservation(same_username, same_condition, same_seller_username)
#                    #ticket_reservation(username, condition)
#            #elif:
#            elif user_exist == 2:
#                while True:
#                    new_name = input("Unesite novo korisnicko ime: ").strip()
#                    #surname_exists = False
#                    if not new_name:
#                        print("Pogresan unos! Molimo vas pokusajte ponovo.")
#                    elif new_name:
#                        while True:
#                            new_surname = input("Unesite novo korisnicko prezime: ").strip()
#                            if not new_surname:
#                                print("Pogresan unos! Molimo vas pokusajte ponovo.")
#                            elif new_surname:
#                                #surname_exists = True
#                                username = new_name + " " + new_surname
#                                condition = same_condition2
#                                seller_username = same_seller_username2
#                                ticket_reservation(username, condition, seller_username)
#                                break
#                            else:
#                                print("Pogresan unos! Molimo vas pokusajte ponovo.")
#                        break
#                        #if surname_exists:
#                        #    break
#                    else:
#                        print("Pogresan unos! Molimo vas pokusajte ponovo.")
                    #username = name + " " + surname
                    #condition = same_condition2
                    #ticket_reservation(username, condition)

                #ticket_reservation(username, condition)

            #else:
            #print("Redni broj koji ste uneli nije dat u tabeli! Pokusajte ponovo.")            
            #with open("reserved_tickets.txt", "r") as file:
            #    lines = file.readlines()
            #    with open("reserved_tickets.txt", "w") as file1:
            #        for line in lines:
            #            apart_line = line.split("|")
            #            ticket_password = apart_line[0]
            #            ticket_date = apart_line[1]
            #            ticket_seat = apart_line[2]
            #            ticket_username = apart_line[3]
            #            ticket_condition = apart_line[4]
            #            if ticket_password == search_ticket["search_password"] and ticket_seat == search_ticket["search_seat"]:
            #                ticket_condition = "K"
            #            #with open("reserved_tickets.txt", "w") as file1:
            #                file1.write("{}|{}|{}|{}|{}" .format(ticket_password, ticket_date, ticket_seat, ticket_username, ticket_condition))


                                #break

            
            #else:
            #    print("Redni broj koji ste uneli nije dat u tabeli! Pokusajte ponovo.")
                
            break
        else:
            print("Pogresan unos! Molimo vas pokusajte ponovo.")


def overview_of_available_terms():
    global cinema_screening_term_list
    cinema_projection_append()
    table = PrettyTable()
    counter = 1
    table.field_names = ["Br.", "Sifra termina projekcije"]
    for term in cinema_screening_term_list:
        table.add_row([counter, term["Term_password"]])
        counter += 1
    print(table)



def cancellation_reservation_half_an_hour_before():
    global cinema_screening_term_list
    global cinema_projection_list
    cinema_screening_term_append()
    cinema_projection_append()
    valid_tickets_list = []
    current_time = datetime.now()
    half_an_hour_before = current_time - timedelta(minutes=30)
    with open("reserved_tickets.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            apart_line = line.split("|")
            ticket = {
                "ticket_password": apart_line[0],
                "ticket_date": apart_line[1],
                "ticket_seat": apart_line[2],
                "ticket_username": apart_line[3],
                "ticket_condition": apart_line[4],
                "ticket_real_date": apart_line[5],
                "ticket_seller_username": apart_line[6],
                "ticket_card_price": apart_line[7]
            }
            
            for projection in cinema_projection_list:
                #print(f"Projection Time: {projection['Time_start']}")
                #print(f"Current Time: {datetime.now().strftime('%H:%M')}")
                #print(f"Ticket Date: {ticket['ticket_date']}")
                #print(f"Ticket Condition: {ticket['ticket_condition'].strip()}")
                #print("Bezveze")
                #print(f"Ticket Password: {ticket['ticket_password']}")
                #print(f"Projection Password: {projection['Password']}")
                #ticket_sold = next((ticket_sold for ticket_sold in cinema_projection_list if ticket["ticket_condition"].strip() == "K"), None)
                #print(datetime.strptime(ticket["ticket_date"], "%d.%m.%Y.") > datetime.now())
                if (
                    (
                    #(not (datetime.strptime(ticket["ticket_date"], "%d.%m.%Y.") <= current_time)) and #Tacan  
                    (datetime.strptime(ticket["ticket_date"], "%d.%m.%Y.") > datetime.now()) and #Tacan  

                    (ticket["ticket_condition"].strip() == "R") and
                    (projection["Password"] == ticket["ticket_password"][:4]) #and # Tacan
                    #(datetime.strptime(projection["Time_start"], "%H:%M").strftime("%H:%M") >= datetime.now().strftime('%H:%M')) #current_time) 
                    #(datetime.strptime(projection["Time_start"], "%H:%M") >= current_time) #current_time) 

                    ) or 
                    (ticket["ticket_condition"].strip() == "K") or

                    ((datetime.strptime(ticket["ticket_date"], "%d.%m.%Y.") == current_time) and
                     (datetime.strptime(projection["Time_start"], "%H:%M") >= half_an_hour_before))                    #ticket_sold

                ) and ticket not in valid_tickets_list:
                    
                    valid_tickets_list.append(ticket)
                    #print("Dodao sam tiket!!!!!!!!!!!!!")

                #elif ticket["ticket_condition"] == "K":
                #    valid_tickets_list.append(ticket)
                #    print("Dodao sam tiket!!!!!!!!!!!!!")
            
                else:
                    with open("reserved_tickets.txt", "a") as file2:
                        #file2.write("Prazno")
                        pass
                    #print("Nistaaaaaaaaaaaaaaaaaaaaaaa")

    with open("reserved_tickets.txt", "w") as file1:
        pass 
    #print("##############################################33")
    with open("reserved_tickets.txt", "a") as file2:
        for valid_ticket in valid_tickets_list:
            #with open("reserved_tickets.txt", "a") as file1:
            file2.write("{}|{}|{}|{}|{}|{}|{}|{}|\n".format(valid_ticket["ticket_password"], valid_ticket["ticket_date"], valid_ticket["ticket_seat"], valid_ticket["ticket_username"], valid_ticket["ticket_condition"], valid_ticket["ticket_real_date"], valid_ticket["ticket_seller_username"], valid_ticket["ticket_card_price"]))


def add_reserved_cards_change(seat, card_password, card_date, username, condition, seller_username, real_date, old_price):
    global cinema_screening_term_list
    global reserved_tickets_list
    global all_tickets_list
    fill_list_append()

    global all_projections_list
    fill_all_projections_list_append()

    with open("reserved_tickets.txt", "a") as file:
        
#        real_date = datetime.now().strftime("%d.%m.%Y.")
#        
#
#        current_time = datetime.now()
#        last_365_days = current_time - timedelta(days=365)
#        total_price = 0
#        for all_ticket in all_tickets_list:
#            #print("Datummmmmmmmmmmmmmmmm" +  str(datetime.strptime(all_ticket["ticket_all_real_date"], "%d.%m.%Y.")))
#            if all_ticket["ticket_all_username"].strip() == username.strip() and datetime.strptime(all_ticket["ticket_all_real_date"].strip(), "%d.%m.%Y.") >= last_365_days:
#                for all_projection in all_projections_list:
#                    if all_projection["Password"].strip() == all_ticket["ticket_all_password"][:4].strip():
#                        total_price += float(all_projection["Price"])
#        
#        projection = next((proj for proj in all_projections_list if proj["Password"].strip() == card_password[:4].strip()), None)
#        #price = next((proj for proj in all_projections_list if proj["Password"].strip() == card_password[:4].strip()), None)
#
#        #card_price = projection["Price"]
#        weekday = datetime.strptime(card_date, "%d.%m.%Y.").weekday()
#        #print("WEEEEkk dayy" + weekday)
#        if weekday == 1:
#            card_price = float(projection["Price"]) - 50
#        elif weekday in [5, 6]:
#            card_price = float(projection["Price"]) + 50
#        else:
#            card_price = projection["Price"]
#
#
#        if total_price >= 5000:
#            
#            card_price = 0.9 * float(projection["Price"])
#            print("Dobili ste popust zbog kartice lojalnosti.\n")

        if condition.strip() == "R":
            seller_username = ""
        file.write("{}|{}|{}|{}|{}|{}|{}|{}|\n".format(card_password, card_date, seat, username, condition, real_date, seller_username, old_price))

        reserved_ticket = {
            "card_password": card_password,
            "card_date": card_date,
            "seat": seat,
            "username": username,
            "condition": condition,
            "real_date": real_date,
            "seller_username": seller_username,
            "card_price": old_price

        }

        reserved_tickets_list.append(reserved_ticket)

        ticket_all = {
                "ticket_all_password": card_password,
                "ticket_all_date": card_date,
                "ticket_all_seat": seat,
                "ticket_all_username": username,
                "ticket_all_condition": condition,
                "ticket_all_real_date": real_date,
                "ticket_all_seller_username": seller_username,
                "ticket_all_card_price": old_price 
            }
        all_tickets_list.append(ticket_all)


#if __name__ == '__main__': 
    #ticket_reservation(username)