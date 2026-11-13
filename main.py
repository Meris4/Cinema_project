from Films import lista_filmova
from Films import overview_of_available_movies, multicriteria_search, simple_search, add_change_delete_films
from Bioskopske_projekcije import add_projection, multicriteria_search_projections, add_change_delete_projections
from Tickets import ticket_reservation, overview_of_reserved_tickets, cancellation_ticket_reservation
from Tickets import overview_of_reserved_tickets_seller, cancellation_reserved_sold_tickets
from Tickets import multicriteria_search_tickets
#from Tickets_Second import sale_reserved_tickets
from Tickets import sale_reserved_ticketsf, ticket_change, cancellation_reservation_half_an_hour_before
from Reports import reports

#user_data = []  # Globalna promenljiva za čuvanje podataka o korisnicima


#def read_user_data():
#    user_data = []  # Resetovanje podataka pre ponovnog ucitavanja
#    with open("users.txt", "r") as file1:
#        lines = file1.readlines()
#        user_data = []
#        for line in lines:
#            user_data.append(line.strip().split("|"))
#        return user_data
    
user_data = []
def read_user_data():
    global user_data
    with open("users.txt", "r") as file1:
        lines = file1.readlines()
        for line in lines:
            user_data.append(line.strip().split("|"))
        return user_data


def start_menu():
    print("[P] Prijava na sistem")
    print("[R] Registracija")
    print("[F] O Filmovima")
    print("[I] Izlazak iz aplikacije \n")

user_data_loaded = False
def user_data_append():
    global user_data
    global user_data_loaded

    if user_data_loaded == False:
        user_data = read_user_data()
        user_data_loaded = True
    return user_data

#user_data_loaded = False
def start():
    user_data_append()
    #global user_data

    while True:
        start_menu()
        input1 = input("Izaberite jednu od ponudjenih opcija: ")

        if input1.upper() == "P":
            print("Izabrana je opcija P.\n")

            username = input("Unesite korisnicko ime: ")
            max_attempts = 6
            attempts = 0
            while not username_valid(username) and attempts < max_attempts:
                print("Korisnicko ime koje ste uneli ne postoji! Pokusajte ponovo.")
                username = input("Unesite korisnicko ime: ")
                attempts += 1

            if attempts == max_attempts:
                print("Dostigli ste maksimalan broj pokušaja. Izlazak iz aplikacije.")
                break

            password = input("Unesite lozinku: ")
            max_attempts = 6
            attempts = 0
            while not password_valid(password, username) and attempts < max_attempts:
                print("Uneli ste pogresnu lozinku! Pokusajte ponovo.")
                password = input("Unesite lozinku: ")
                attempts += 1
            
            if attempts == max_attempts:
                print("Dostigli ste maksimalan broj pokušaja. Izlazak iz aplikacije.")
                break

            
            if manager(username) == True:
                continue  # Nastavak glavne petlje
            elif seller(username) == True:
                continue
            else:
                login_menu(username)
            

        elif input1.upper() == "R":
            print("Izabrana je opcija R.\n")

            # !!!!!
            while True:
                username = input("Unesite korisnicko ime: ").strip()
                if username_unique(username):
                    break
                else:
                    print("Korisničko ime već postoji! Probajte neko drugo korisničko ime.")
            # !!!!!! Dobar primer petlje
            # !!!!! Ova je bitna
            password = input("Unesite lozinku: ").strip()
            if len(password) < 6 or not any(char.isdigit() for char in password):
                while len(password) < 6 or not any(char.isdigit() for char in password):
                    print("Lozinka mora biti duža od 6 karaktera i mora sadržati barem jednu cifru. Pokušajte ponovo.")
                    password = input("Unesite lozinku: ")
            # Ako smo došli do ovde, znači da je lozinka dovoljno duga i sadrži cifru
            # !!!!!!

            name = input("Unesite vase ime: ").strip()
            surname = input("Unesite vase prezime: ").strip()
            writing(username, password, name, surname)

        elif input1.upper() == "F":
            print("Izabrana je opcija F.\n")
            film_menu()

        elif input1.upper() == "I":
            print("Izabrana je opcija I.\n")
            print("Izlazak iz aplikacije!")
            break
        else:
            print("Pogrešan unos. Molim vas unesite validan broj stavke.\n")

def writing(username, password, name, surname):
    global user_data
    user_data.append([username, password, name, surname, "registrovan kupac"])
    with open("users.txt", "a") as file1:
        file1.write("{}|{}|{}|{}|{}\n".format(username, password, name, surname, "registrovan kupac"))
    print("Registracija uspešna!")

def username_unique(username):
    for user in user_data:
        if username == user[0].strip():
            return False
    return True



def username_valid(username):
    for user in user_data:
        if username == user[0]:
            return True
    return False


def password_valid(password, username):
    for user in user_data:
        if password == user[1] and username == user[0]:
            return True
    return False


# Funkcija za meni menadzera
def manager_menu(username):
    while True:
        print("[1] Pregled dostupnih filmova")
        print("[2] Pretraga filmova")
        print("[3] Višekriterijumska pretraga filmova")
        print("[4] Pretraga termina bioskopskih projekcija")
        print("[5] Izmena ličnih podataka")
        print("[6] Registracija novih prodavaca")
        print("[7] Registracija novih menadzera")
        print("[8] Dodavanje, izmena i brisanje filmova")
        print("[9] Dodavanje, izmena i brisanje projekcija")
        print("[10] Izvestavanje")
        print("[11] Odjava sa sistema")
        input_login = input("Izaberite jednu od ponudjenih opcija: ")
        if input_login == "1":
            print("Izabrali ste opciju 1.\n")
            overview_of_available_movies()
            while True:
                inputN = input("[N] Nazad: ").strip()
                if inputN.upper() == "N":
                    break
                else:
                    print("Pogresan unos! Pokusajte ponovo.")

        elif input_login == "2":
            print("Izabrali ste opciju 2.\n")
            simple_search()
            
        elif input_login == "3":
            print("Izabrali ste opciju 3.\n")
            multicriteria_search()

        elif input_login == "4":
            print("Izabrali ste opciju 4.\n")
            multicriteria_search_projections()
        elif input_login == "5":
            print("Izabrali ste opciju 5.\n")
            while True:
                print("[1] Lozinku")
                print("[2] Ime")
                print("[3] Prezime")
                print("[4] NAZAD")
                change = input("Izaberite sta zelite da izmenite: ")
                if change == "1":
                    old_password = get_user_data(username, "password")
                    if old_password is not None:
                        print("Vasa stara lozinka je ", old_password)
                        new_password = input("Unesite novu lozinku: ")
                        update_user_data(username, "password", new_password)
                        print("Lozinka uspešno ažurirana.")
                    else:
                        print("Došlo je do greške u pronalaženju podataka korisnika.")
                    #return
                
                elif change == "2":
                    old_name = get_user_data(username, "name")
                    if old_name is not None:
                        print("Vase staro ime je ", old_name)
                        new_name = input("Unesite novo ime: ")
                        update_user_data(username, "name", new_name)
                        print("Ime uspešno ažurirano.")
                    else:
                        print("Došlo je do greške u pronalaženju podataka korisnika.")
                    #return
                
                elif change == "3":
                    old_surname = get_user_data(username, "surname")
                    if old_surname is not None:
                        print("Vase staro prezime je", old_surname)
                        new_surname = input("Unesite novo prezime: ")
                        update_user_data(username, "surname", new_surname)
                        print("Prezime uspešno ažurirano.")
                    else:
                        print("Došlo je do greške u pronalaženju podataka korisnika.")  
                    #return
                
                elif change == "4":
                    print("Izabrali ste opciju NAZAD")
                    break
            
                else:
                    print("Pogrešan unos. Molim vas unesite validan broj stavke.\n")
                
        elif input_login == "6":
            print("Izabrali ste opciju 6.\n")
            while True:
                username = input("Unesite korisnicko ime: ")
                if username_unique(username):
                    break
                else:
                    print("Korisničko ime već postoji! Probajte neko drugo korisničko ime.")
            # !!!!!! Dobar primer petlje

            # !!!!! Ova je bitna
            password = input("Unesite lozinku: ")
            if len(password) < 6 or not any(char.isdigit() for char in password):
                while len(password) < 6 or not any(char.isdigit() for char in password):
                    print("Lozinka mora biti duža od 6 karaktera i mora sadržati barem jednu cifru. Pokušajte ponovo.")
                    password = input("Unesite lozinku: ")
            # Ako smo došli do ovde, znači da je lozinka dovoljno duga i sadrži cifru
            # !!!!!!

            name = input("Unesite vase ime: ")
            surname = input("Unesite vase prezime: ")
            writing_saller(username, password, name, surname)

        elif input_login == "7":
            print("Izabrali ste opciju 7.\n")
            while True:
                username = input("Unesite korisnicko ime: ")
                if username_unique(username):
                    break
                else:
                    print("Korisničko ime već postoji! Probajte neko drugo korisničko ime.")
            # !!!!!! Dobar primer petlje

            # !!!!! Ova je bitna
            password = input("Unesite lozinku: ")
            if len(password) < 6 or not any(char.isdigit() for char in password):
                while len(password) < 6 or not any(char.isdigit() for char in password):
                    print("Lozinka mora biti duža od 6 karaktera i mora sadržati barem jednu cifru. Pokušajte ponovo.")
                    password = input("Unesite lozinku: ")
            # Ako smo došli do ovde, znači da je lozinka dovoljno duga i sadrži cifru
            # !!!!!!

            name = input("Unesite vase ime: ")
            surname = input("Unesite vase prezime: ")
            writing_manager(username, password, name, surname)

        elif input_login == "8":
            print("Izabrali ste opciju 8.")
            add_change_delete_films()

        elif input_login == "9":
            print("Izabrali ste opciju 9.")
            add_change_delete_projections()
            #add_projection()

        elif input_login == "10":
            print("Izabrali ste opciju 10.")
            reports()
        elif input_login == "11":
            print("Izabrali ste opciju 11. Odjava sa sistema.\n")
            print("Uspešno ste se odjavili.\n")
            break
        else:
            print("Pogrešan unos. Molim vas unesite validan broj stavke.\n")
    
def seller_menu(username):
    global user_data
    seller_username = username
    user_data_append()
    while True:
        #print("Uspesno ste se prijavili kao prodavac")
        print("[1] Pregled dostupnih filmova")
        print("[2] Pretraga filmova")
        print("[3] Višekriterijumska pretraga filmova")
        print("[4] Pretraga termina bioskopskih projekcija")
        print("[5] Izmena ličnih podataka")
        print("[6] Rezervacija karata")
        print("[7] Pregled rezervisanih karata")
        print("[8] Ponistavanje rezervisanih/prodatih karata")
        print("[9] Pretraga karata")
        print("[10] Direktna prodaja karata")
        print("[11] Prodaja rezervisane karte")
        print("[12] Izmena karte")
        print("[13] Ponistavanje rezervacije pola sata pre pocetka projekcije")
        print("[14] Odjava sa sistema")
        input_login = input("Izaberite jednu od ponudjenih opcija: ")
        if input_login == "1":
            print("Izabrali ste opciju 1.\n")
            overview_of_available_movies()
            while True:
                inputN = input("[N] Nazad: ").strip().upper()
                if inputN == "N":
                    break
                else:
                    print("Pogresan unos! Pokusajte ponovo.")

        elif input_login == "2":
            print("Izabrali ste opciju 2.\n")
            simple_search()

        elif input_login == "3":
            print("Izabrali ste opciju 3.\n")
            multicriteria_search()

        elif input_login == "4":
            print("Izabrali ste opciju 4.\n")
            multicriteria_search_projections()

        elif input_login == "5":
            print("Izabrali ste opciju 5.\n")
            while True:
                print("[1] Lozinku")
                print("[2] Ime")
                print("[3] Prezime")
                print("[4] NAZAD")
                change = input("Izaberite sta zelite da izmenite: ")
                if change == "1":
                    old_password = get_user_data(username, "password")
                    if old_password is not None:
                        print("Vasa stara lozinka je ", old_password)
                        new_password = input("Unesite novu lozinku: ")
                        update_user_data(username, "password", new_password)
                        print("Lozinka uspešno ažurirana.")
                    else:
                        print("Došlo je do greške u pronalaženju podataka korisnika.")
                    #return
                
                elif change == "2":
                    old_name = get_user_data(username, "name")
                    if old_name is not None:
                        print("Vase staro ime je ", old_name)
                        new_name = input("Unesite novo ime: ")
                        update_user_data(username, "name", new_name)
                        print("Ime uspešno ažurirano.")
                    else:
                        print("Došlo je do greške u pronalaženju podataka korisnika.")
                    #return
                
                elif change == "3":
                    old_surname = get_user_data(username, "surname")
                    if old_surname is not None:
                        print("Vase staro prezime je", old_surname)
                        new_surname = input("Unesite novo prezime: ")
                        update_user_data(username, "surname", new_surname)
                        print("Prezime uspešno ažurirano.")
                    else:
                        print("Došlo je do greške u pronalaženju podataka korisnika.")  
                    #return
                
                elif change == "4":
                    print("Izabrali ste opciju NAZAD")
                    break
            
                else:
                    print("Pogrešan unos. Molim vas unesite validan broj stavke.\n")

        elif input_login == "6":
            print("Izabrali ste opciju 6. \n")

            #print("Zelite da rezervisete kartu za: ")
            #print("[1] Registrovanog kupca")
            #print("[2] Neregistrovanog kupca")
            
            while True: 
                print("Zelite da rezervisete kartu za: ")
                print("[1] Registrovanog kupca")
                print("[2] Neregistrovanog kupca")

                user = input("Izaberite opciju: ").strip()
                if user == "1":
                    print("Izabrali ste registrovanog kupca.")
                    while True:
                        username = input("Unesite korisnicko ime: ").strip()
                        user_exists = False
                        for user in user_data:
                            if user[0] == username and user[4] == "registrovan kupac":
                                print("Uneli ste postojece korisnicko ime. \n")
                                user_exists = True
                                break
                                #return username
                        if user_exists:
                            break
                        
                        else:
                            print("Uneli ste nepostojece korisnicko ime! Molimo vas pokusajte ponovo. ")
                    break
                elif user == "2":
                    print("Izabrali ste neregistrovanog kupca.")
                    while True:
                        name = input("Unesite korisnicko ime: ").strip()
                        #surname_exists = False
                        if name:
                            while True:
                                surname = input("Unesite korisnicko prezime: ").strip()
                                if surname:
                                    #surname_exists = True
                                    break
                                else:
                                    print("Pogresan unos! Molimo vas pokusajte ponovo.")
                            break
                            #if surname_exists:
                            #    break

                        else:
                            print("Pogresan unos! Molimo vas pokusajte ponovo.")
                    username = name + " " + surname
                    break
                        #else:
                #elif user.upper() == "N":
                #    break
                

                else:
                    print("Pogresan unos! Molimo vas pokusajte ponovo.")
            condition = "R"
            ticket_reservation(username, condition, seller_username)

        elif input_login == "7":
            print("Izabrali ste opciju 7.")
            overview_of_reserved_tickets_seller()
            while True:
                inputN = input("[N] Nazad: ").upper()
                if inputN.strip() == "N":
                    print("\n")
                    break
                else:
                    print("Pogresan unos! Molimo vas unesite 'N' za povratak.")

        elif input_login == "8":
            print("Izabrali ste opciju 8.")
            cancellation_reserved_sold_tickets()
            while True:
                print("Da li zelite da nastavite sa brisanjem rezervisanih/prodatih karata?")
                print("[D] Da")
                print("[N] Ne")
                choose = input("Izaberite opciju: ").strip().upper()
                if choose == "D":
                    cancellation_reserved_sold_tickets()
                elif choose == "N":
                    break
                else:
                    print("Pogresan unos! Molimo vas pokusajte ponovo.")
            #while True:
            #    inputN = input("[N] Nazad: ").upper()
            #    if inputN.strip() == "N":
            #        print("\n")
            #        break
            #    else:
            #        print("Pogresan unos! Molimo vas unesite 'N' za povratak.")

        elif input_login == "9":
            print("Izabrali ste opciju 9.")
            sale_reserved_tickets = False
            multicriteria_search_tickets(sale_reserved_tickets)
            while True:
                print("Da li zelite da nastavite sa pretragom karata?")
                print("[D] Da")
                print("[N] Ne")
                choose = input("Izaberite opciju: ").strip().upper()
                if choose == "D":
                    sale_reserved_tickets = False
                    multicriteria_search_tickets(sale_reserved_tickets)
                elif choose == "N":
                    break
                else:
                    print("Pogresan unos! Molimo vas pokusajte ponovo.")
                
        elif input_login == "10":
            print("Izabrali ste opciju 10. \n")

            print("Zelite da prodate kartu za: ")
            print("[1] Registrovanog kupca")
            print("[2] Neregistrovanog kupca")
            #user = input("Izaberite opciju: ")
            
            while True: 
                user = input("Izaberite opciju: ")
                if user == "1":
                    print("Izabrali ste registrovanog kupca.")
                    while True:
                        username = input("Unesite korisnicko ime: ").strip()
                        user_exists = False
                        for user in user_data:
                            if user[0] == username and user[4] == "registrovan kupac":
                                print("Uneli ste postojece korisnicko ime. \n")
                                user_exists = True
                                break
                                #return username
                        if user_exists:
                            break
                        
                        else:
                            print("Uneli ste nepostojece korisnicko ime! Molimo vas pokusajte ponovo. ")
                    break
                elif user == "2":
                    print("Izabrali ste neregistrovanog kupca.")
                    while True:
                        name = input("Unesite korisnicko ime: ").strip()
                        #surname_exists = False
                        if name:
                            while True:
                                surname = input("Unesite korisnicko prezime: ").strip()
                                if surname:
                                    #surname_exists = True
                                    break
                                else:
                                    print("Pogresan unos! Molimo vas pokusajte ponovo.")
                            break
                            #if surname_exists:
                            #    break

                        else:
                            print("Pogresan unos! Molimo vas pokusajte ponovo.")
                    username = name + " " + surname
                    break
                        #else:

                else:
                    print("Pogresan unos! Molimo vas pokusajte ponovo.")
            condition = "K"
            ticket_reservation(username, condition, seller_username)

        elif input_login == "11":
            print("Izabrali ste opciju 11.")
            #sale_reserved_ticket = True
            sale_reserved_ticketsf(seller_username)

            while True:
                print("Da li zelite da nastavite sa prodajom rezervisanh karata?")
                print("[D] DA")
                print("[N] NE")
                choose = input("Izaberite opciju: ").upper().strip()
                if choose == "D":
                    sale_reserved_ticketsf(seller_username)
                elif choose == "N":
                    break
                else:
                    print("Pogresan unos! Molimo vas pokusajte ponovo.")

        elif input_login == "12":
            print("Izabrali ste opciju 12.")
            ticket_change()

        elif input_login == "13":
            cancellation_reservation_half_an_hour_before()

            print("Uspesno ste ponistili rezervacije.\n")
            while True:
                inputN = input("[N] Nazad")
                if inputN.upper() == "N":
                    break
                else:
                    print("Pogresan unos! Pokusajte ponovo.")

        elif input_login == "14":
            print("Izabrali ste opciju 14. Odjava sa sistema.\n")
            print("Uspešno ste se odjavili.\n")
            break
        else:
            print("Pogrešan unos. Molim vas unesite validan broj stavke.\n")



def writing_saller(username, password, name, surname):
    user_data.append([username, password, name, surname, "prodavac"])
    with open("users.txt", "a") as file1:
        file1.write("{}|{}|{}|{}|{}\n".format(username, password, name, surname, "prodavac"))
    print("Registracija prodavca uspešna!")
    #with open("users.txt", "a") as file1:
    #    #file1.write(username + "|" + password + "|" + name + "|" + surname + "\n")
    #    file1.write("{}|{}|{}|{}|{}\n".format(username, password, name, surname, "prodavac"))
    #    print("Registracija prodavca uspešna!\n")

def writing_manager(username, password, name, surname):
    user_data.append([username, password, name, surname, "menadzer"])
    with open("users.txt", "a") as file1:
        file1.write("{}|{}|{}|{}|{}\n".format(username, password, name, surname, "menadzer"))
    print("Registracija menadzera uspešna!")
    #with open("users.txt", "a") as file1:
    #    #file1.write(username + "|" + password + "|" + name + "|" + surname + "\n")
    #    file1.write("{}|{}|{}|{}|{}\n".format(username, password, name, surname, "menadzer"))
    #    print("Registracija menadzera uspešna!\n")
    
    #read_user_data()

def manager(username):
    with open("users.txt", "r") as file1:
        lines = file1.readlines()
        for line in lines:
            apart_line = line.split("|")
            if apart_line[4].strip() == "menadzer" and username == apart_line[0].strip():
                print("Uspesno ste se prijavili kao menadzer!\n")
                manager_menu(username)
                return True # Izlazak iz funkcije ako je ulogovan korisnik menadžer
    return False

def seller(username):
    with open("users.txt", "r") as file1:
        lines = file1.readlines()
        for line in lines:
            apart_line = line.split("|")
            if apart_line[4].strip() == "prodavac" and username == apart_line[0].strip():
                print("Uspesno ste se prijavili kao prodavac!\n")
                seller_menu(username)
                return True # Izlazak iz funkcije ako je ulogovan korisnik prodavac
    return False

def film_menu():
    while True:
        print("[1] Pregled dostupnih filmova")
        print("[2] Pretraga filmova")
        print("[3] Višekriterijumska pretraga filmova")
        print("[4] Pretraga termina bioskopskih projekcija")
        print("[5] Nazad")
        input_login = input("Izaberite jednu od ponudjenih opcija: ")
        if input_login == "1":
            print("Izabrali ste opciju 1.\n")
            overview_of_available_movies()
 
        elif input_login == "2":
            print("Izabrali ste opciju 2.\n")
            simple_search()

        elif input_login == "3":
            print("Izabrali ste opciju 3.\n")
            multicriteria_search()

        elif input_login == "4":
            print("Izabrali ste opciju 4.\n")
            multicriteria_search_projections()
        
        elif input_login == "5":
            print("Izabrali ste opciju 5.\n")
            break
        else:
            print("Pogrešan unos. Molim vas unesite validan broj stavke.\n")
        

def login_menu(username):
    print("Uspesno ste se prijavili kao registrovani korisnik!")
    while True:
        #print("Uspesno ste se prijavili kao registrovani korisnik!")
        print("[1] Pregled dostupnih filmova")
        print("[2] Pretraga filmova")
        print("[3] Višekriterijumska pretraga filmova")
        print("[4] Pretraga termina bioskopskih projekcija")
        print("[5] Izmena ličnih podataka")
        print("[6] Rezervacija karata")
        print("[7] Pregled rezervisanih karti")
        print("[8] Ponistavanje rezervacije karata")
        print("[9] Odjava sa sistema")
        input_login = input("Izaberite jednu od ponudjenih opcija: ")
        if input_login == "1":
            print("Izabrali ste opciju 1.\n")
            overview_of_available_movies()
            while True:
                inputN = input("[N] Nazad: ").strip()
                if inputN.upper() == "N":
                    break
                else:
                    print("Pogresan unos! Pokuajte ponovo.")


        elif input_login == "2":
            print("Izabrali ste opciju 2.\n")
            simple_search()

        elif input_login == "3":
            print("Izabrali ste opciju 3.\n")
            multicriteria_search()
            
        elif input_login == "4":
            print("Izabrali ste opciju 4.\n")
            multicriteria_search_projections()

        elif input_login == "5":
            print("Izabrali ste opciju 5.\n")
            while True:
                print("[1] Lozinku")
                print("[2] Ime")
                print("[3] Prezime")
                print("[4] NAZAD")
                change = input("Izaberite sta zelite da izmenite: ")
                if change == "1":
                    old_password = get_user_data(username, "password")
                    if old_password is not None:
                        print("Vasa stara lozinka je ", old_password)
                        new_password = input("Unesite novu lozinku: ")
                        update_user_data(username, "password", new_password)
                        print("Lozinka uspešno ažurirana.")
                    else:
                        print("Došlo je do greške u pronalaženju podataka korisnika.")
                    #return
                
                elif change == "2":
                    old_name = get_user_data(username, "name")
                    if old_name is not None:
                        print("Vase staro ime je ", old_name)
                        new_name = input("Unesite novo ime: ")
                        update_user_data(username, "name", new_name)
                        print("Ime uspešno ažurirano.")
                    else:
                        print("Došlo je do greške u pronalaženju podataka korisnika.")
                    #return
                
                elif change == "3":
                    old_surname = get_user_data(username, "surname")
                    if old_surname is not None:
                        print("Vase staro prezime je", old_surname)
                        new_surname = input("Unesite novo prezime: ")
                        update_user_data(username, "surname", new_surname)
                        print("Prezime uspešno ažurirano.")
                    else:
                        print("Došlo je do greške u pronalaženju podataka korisnika.")  
                    #return
                
                elif change == "4":
                    print("Izabrali ste opciju 6. Odjava sa sistema.\n")
                    print("Uspešno ste se odjavili.\n")
                    break
            
                else:
                    print("Pogrešan unos. Molim vas unesite validan broj stavke.\n")

        elif input_login == "6":
            print("Izabrali ste opciju 6. \n")

            condition = "R"
            seller_username = ""

            ticket_reservation(username, condition, seller_username)
            #ticket_reservation(username)   

        elif input_login == "7":
            print("Izabrali ste opciju 7. \n")
            overview_of_reserved_tickets(username)

            while True:
                inputN = input("[N] Nazad: ").strip().upper()
                if inputN == "N":
                    break
                else:
                    print("Pogresan unos! Molimo vas unesite 'N' za nazad.")
        
        elif input_login == "8":
            print("Izabrali ste opciju 8. \n")
            cancellation_ticket_reservation(username)
            while True:
                print("Da li zelite da nastavite sa brisanjem rezervacija?")
                print("[D] Da")
                print("[N] Ne")
                choose = input("Izaberite opciju: ").strip().upper()
                if choose == "D":
                    cancellation_ticket_reservation(username)
                elif choose == "N":
                    break
                else:
                    print("Pogresan unos! Molimo vas pokusajte ponovo.")


        elif input_login == "9":
            print("Izabrali ste opciju 9.\n")
            break
            
        else:
            print("Pogrešan unos. Molim vas unesite validan broj stavke.\n")
    


def get_user_data(username, data_type):
    global user_data
    for user in user_data:
        if username == user[0]:
            if data_type == "password":
                return user[1].strip()
            elif data_type == "name":
                return user[2].strip()
            elif data_type == "surname":
                return user[3].strip()
    return None

def update_user_data(username, data_type, new_value):
    global user_data
    for user in user_data:
        if username == user[0]:
            if data_type == "password":
                user[1] = new_value
            elif data_type == "name" :
                user[2] = new_value
            elif data_type == "surname":
                user[3] = new_value
    save_user_data()

def save_user_data():
    global user_data
    with open("users.txt", "w") as file1:
        for user in user_data:
            file1.write("{}|{}|{}|{}|{}\n".format(user[0], user[1], user[2], user[3], user[4]))


if __name__ == '__main__':
    #read_user_data()
    start()
    
