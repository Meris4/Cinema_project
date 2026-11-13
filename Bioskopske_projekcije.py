from datetime import datetime, timedelta
from Films import read_films, read_film_file, lista_filmova, overview_of_available_movies
from prettytable import PrettyTable
#from Novi_program import user_data_append, user_data
from Reports_second import all_tickets_list, fill_list_append
from Reports_second import fill_all_projections_list_append, all_projections_list, fill_all_term_append, all_terms_list

cinema_projection_list = []
data_loaded = False

def add_projection():
    global data_loaded
    global cinema_projection_list

    global all_projections_list
    fill_all_projections_list_append()
    
    update_projection_status_check()
    #update_projection_status()
    #while True:
        #try:
    password = input("Unesite sifru bioskopske projekcije (4 cifre): ")
    #if not data_loaded:
    #    cinema_projection_read()
    #    data_loaded = True
    cinema_projection_append()
    password = valid_projection_password(password)

    print("Sale: [A1], [A2], [A3]")
    hall_choice = input("Unesite salu u kojoj se projekcija odrzava: ").upper()
    hall_choice = halls_valid(hall_choice)
    #hall_available(hall_choice)

    time_start = input("Unesite vreme pocetka projekcije (hh:mm): ")
    time_start = projection_start_time_valid(time_start)

    time_end = input("Unesite vreme kraja projekcije (hh:mm): ")
    time_end = projection_end_time_valid(time_end, time_start)

    while True:
        print("'ponedeljak', 'utorak', 'sreda', 'cetvrtak', 'petak', 'subota', 'nedelja'")
        day = input("Unesite dane u nedelji kada se projekcija održava (razdvojite zarezom): ").split(", ")
        valid_days = ["ponedeljak", "utorak", "sreda", "cetvrtak", "petak", "subota", "nedelja"]
        if all(day1 in valid_days for day1 in day ):
            break
        else:
            print("Vas unos nije ispravan! Molimo vas pokusajte ponovo.\n")
    day_dates = []

    for selected_day in day:
        # Pronalaženje broja dana u nedelji na osnovu unosa korisnika
        days_of_week = ["ponedeljak", "utorak", "sreda", "cetvrtak", "petak", "subota", "nedelja"]
        selected_day_index = days_of_week.index(selected_day.lower())

        # Izračunavanje sledećeg datuma za odabrani dan
        next_date = next_weekday(datetime.now(), selected_day_index)

        # Dodavanje formiranog datuma u listu
        day_dates.append(next_date.strftime("%d.%m.%Y."))

    overview_of_available_movies()
    choice_film = input("Unesite film koji se prikazuje (od dostupnih filmova): ")
    #read_films()
    read_film_file()
    choice_film = film_valid(choice_film)

    while True:
        try:
            price = float(input("Unesite cenu karte: "))
            break
        except ValueError:
            print("Pogresan unos. Molimo vas pokusajte ponovo! ")

    projection = {
        "Password": password,
        "Hall": hall_choice,
        "Time_start": datetime.strptime(time_start, "%H:%M").strftime("%H:%M"),
        "Time_end": datetime.strptime(time_end, "%H:%M").strftime("%H:%M"),
        "Day": day,
        "Film": choice_film,
        "Price": price
    }
    cinema_projection_write(projection)

    cinema_projection_list.append(projection)

    add_cinema_screening_term(projection)

    all_projection = {
        "Password": password,
        "Hall": hall_choice,
        "Time_start": datetime.strptime(time_start, "%H:%M").strftime("%H:%M"),
        "Time_end": datetime.strptime(time_end, "%H:%M").strftime("%H:%M"),
        "Day": day,
        "Film": choice_film,
        "Price": price
    }
    all_projections_list.append(all_projection)

    return cinema_projection_list
             
def next_weekday(d, weekday):
    days_until = weekday - d.weekday()
    if days_until <= 0:  # Ako je odabrani dan već prošao u ovoj nedelji, dodajte 7 dana
        days_until += 7
    return d + timedelta(days_until)

def generate_next_two_weekdays(selected_day):
    current_date = datetime.now()
    next_weekdays = []

    # Pronalaženje broja dana u nedelji na osnovu unosa korisnika
    days_of_week = ["ponedeljak", "utorak", "sreda", "cetvrtak", "petak", "subota", "nedelja"]
    selected_day_index = days_of_week.index(selected_day.lower())

    for _ in range(2):
        next_day = next_weekday(current_date, selected_day_index)#.strftime("%d.%m.%Y.")
        next_weekdays.append(next_day.strftime("%d.%m.%Y."))
        #next_weekdays.append(datetime.strptime(next_day, "%d.%m.%Y.").strftime("%d.%m.%Y."))
        current_date = next_day + timedelta(days=1)  # Idemo na sledeći odabrani dan

    return next_weekdays


update_projection_status_loaded = False

def update_projection_status_check():
    global update_projection_status_loaded
    if not update_projection_status_loaded:
        update_projection_status()
        update_projection_status_loaded = True
    return update_projection_status()


def update_projection_status():
    global cinema_screening_term_list
    today = datetime.now()

    for term in cinema_screening_term_list:
        term_date = datetime.strptime(term["Date"], "%d.%m.%Y.")
        if term_date < today and term["Valid"] == "V":
            term["Valid"] = "N"
            update_projection_file(term)
            #return update_projection_file(term)

def update_projection_file(term):
    global cinema_screening_term_list
    with open("projection_term.txt", "r") as file:
        lines = file.readlines()
    with open("projection_term.txt", "w") as file:
        for line in lines:
            line_data = line.split("|")
            if line_data[0] == term["Term_password"]:
                #date = term["Date"]
                #line_data[2] = "N"
                line = "{}|{}|{}\n".format(term["Term_password"], term["Date"], term["Valid"])
                #line = "{}|{}|{}\n".format(term["Term_password"], date, line_data[2])
            file.write(line)
        #for i, line in enumerate(lines):
        #    line_data = line.split("|")
        #    if line_data[0] == term["Term_password"]:
        #        lines[i] = "{}|{}|{}\n".format(term["Term_password"], term["Date"], term["Valid"])
        #file.writelines(lines)

def cinema_projection_write(projection):
    with open("cinema_projections.txt", "a") as file:
        file.write("{}|{}|{}|{}|{}|{}|{}\n".format(projection['Password'], projection['Hall'], projection['Time_start'], projection['Time_end'], ", ".join(projection['Day']), projection['Film'], projection['Price'] ))


def cinema_projection_read():   
    global data_loaded
    global cinema_projection_list
    with open("cinema_projections.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            apart_line = line.strip().split("|")
            projekcija = {
                "Password": apart_line[0],
                "Hall": apart_line[1],
                "Time_start": apart_line[2],
                "Time_end":apart_line[3],
                "Day": apart_line[4].split(", "),
                "Film": apart_line[5],
                "Price": apart_line[6]
            }
            cinema_projection_list.append(projekcija)

cinema_projection_loaded = False
def cinema_projection_append():
    global cinema_projection_loaded
    if not cinema_projection_loaded:
        cinema_projection_read()
        cinema_projection_loaded = True
        #return cinema_projection_read()              


halls = []
halls_loaded_data2 = False

def read_halls():
    global halls
    with open("halls.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            apart_line = line.strip().split("|")
            hall = {
                "hall_password": apart_line[0],
                "hall_name": apart_line[1]
            }
            halls.append(hall) # Dodavanje sale u listu
    return halls



def halls_loaded_data():
    global halls
    global halls_loaded_data2

    if not halls_loaded_data2:
        halls = read_halls()
        halls_loaded_data2 = True
    return halls

        
    
def halls_valid(hall_choice):
    global halls
    halls_loaded_data()
    while True:
        for hall in halls:
            if hall["hall_password"] == hall_choice:
                return hall_choice
        hall_choice = input("Vasa sala je nepostojeca. Pokusajte ponovo: ").upper()


# Proveraa
def projection_start_time_valid(time_start):
    while True:

        if len(time_start) == 5 and time_start[2] == ":" and time_start[:2].isdigit() and time_start[3:].isdigit():
            try:
                datetime.strptime(time_start, "%H:%M")
                return time_start
            except ValueError:
                time_start = input("Pogresan unos. Unesite vreme u trazenom formatu (hh:mm): ")
        else:
            time_start = input("Pogresan unos. Unesite vreme u trazenom formatu (hh:mm): ")


def projection_end_time_valid(time_end, time_start):
    while True:
        if len(time_end) == 5 and time_end[2] == ":" and time_end[:2].isdigit() and time_end[3:].isdigit():
            try:
                datetime.strptime(time_end, "%H:%M")
                if datetime.strptime(time_end, "%H:%M")>datetime.strptime(time_start, "%H:%M"):
                    return time_end
                else:
                    time_end = input("Pogresan unos. Vreme kraja mora biti posle vremena pocetka. Pokusajte ponovo: ")
            except ValueError:
                time_end = input("Pogresan unos. Unesite vreme u trazenom formatu (hh:mm): ")
        else:
            time_end = input("Pogresan unos. Unesite vreme u trazenom formatu (hh:mm): ")

      

def valid_projection_password(password):

    while True:
        if password.isdigit() and len(password) == 4:
            for projekcija in cinema_projection_list:
                    
                if projekcija["Password"] == password:
                    print("Data sifra projekcije je vec u upotrebi. Molimo vas pokusajte neku drugu. ")
                    password = input("Unesite sifru bioskopske projekcije (4 cifre): ") 
                    break
                    
            else:
                    #print("Data sifra projekcije je vec u upotrebi. Molimo vas pokusajte neku drugu! ")
                    #password = input("Data sifra projekcije je vec u upotrebi. Molimo vas pokusajte neku drugu: ")
                print("Sifra je validna")
                return password
        else:
            password = input("Sifra mora sadrzati tacno 4 cifre! Pokusajte ponovo: ")

def film_valid(choice_film):
    #read_films()
    while True:
        for film in lista_filmova:
            if film["Naziv"] == choice_film:
                print("Film je validan!")
                return choice_film
        else:
            print("Film ne postoji!")
            choice_film = input("Unesite film koji se prikazuje (od dostupnih filmova): ")

generator = []
def generator_read():
    global generator
    with open("generator.txt", "r") as file1:
        lines = file1.readlines()
        for line in lines:
            generator.append(line)


generator_loaded = False
def term_letter_generator():
    global generator
    global generator_loaded

    if not generator_loaded:
        generator_read()
        generator_loaded = True
    

        
    if generator and generator[-1]:  # Provera da li postoji poslednji element i da li je prazan
        last_letters = generator[-1]

        left_letter = ord(last_letters[0])
        right_letter = ord(last_letters[1]) + 1

    else:
        left_letter = ord('A')
        right_letter = ord('A')

    #left_letter = ord('A')
    while left_letter <= ord('Z'):
        #right_letter = ord('A')
        while right_letter <= ord('Z'):
            password = chr(left_letter) + chr(right_letter)
            if password not in generator:
                generator.append(password)
                with open("generator.txt", "a") as file2:
                    file2.write(password + "\n")
                yield password
            #yield password
            right_letter += 1
##
        left_letter += 1
        right_letter = ord('A')
    
            

cinema_screening_term_list = []

term_passwords = []
def cinema_screening_term_password():
    global term_passwords
    global cinema_projection_list
    gen = term_letter_generator()

    for projection in cinema_projection_list:
        first_part = projection["Password"] 
        second_part = next(gen)

        term_password = first_part + second_part
        term_passwords.append(term_password)
    return term_passwords

generated_dates = []
def generate_dates_for_next_two_weeks():
    global cinema_projection_list
    global generated_dates

    current_date = datetime.now()

    for date in range(14):
        generated_dates.append(current_date.strftime("%d.%m.%Y."))
        current_date += timedelta(days=1)

    return generated_dates

def cinema_screening_term_write(projection_term):
    with open("projection_term.txt", "a") as file:
        file.write("{}|{}|{}\n".format(projection_term["Term_password"], projection_term["Date"], projection_term["Valid"]))


screening_term_loaded = False
def cinema_screening_term_append():
    global screening_term_loaded
    if not screening_term_loaded:
        cinema_screening_term_read()
        screening_term_loaded = True
    return cinema_screening_term_list

def cinema_screening_term_read():
    global cinema_screening_term_list
    today = datetime.now()
    #cinema_screening_term_list = []  # Obrisi staru listu pre punjenja novim vrednostima
    with open("projection_term.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            apart_line = line.split("|")
            projection_term = {
                "Term_password": apart_line[0],
                "Date": apart_line[1].strip(),
                "Valid": apart_line[2].strip()
            }
            # Provera da li je datum prosao
            term_date = datetime.strptime(projection_term["Date"], "%d.%m.%Y.")
            if term_date >= today and projection_term["Valid"] == "V":
                cinema_screening_term_list.append(projection_term)

def add_cinema_screening_term(projection):
    global cinema_screening_term_list
    global screening_term_loaded

    global all_terms_list
    fill_all_term_append()

    if not screening_term_loaded:
        cinema_screening_term_read()
        screening_term_loaded = True
             
    gen = term_letter_generator()


    selected_days = projection["Day"]

    for selected_day in selected_days:
        for date in generate_next_two_weekdays(selected_day):
            term_password = projection["Password"] + next(gen)

            projection_term = {
                "Term_password": term_password,
                "Date": date, 
                "Valid": "V" if datetime.strptime(date, "%d.%m.%Y.") >= datetime.now() else "N"
            }

            all_projection_term = {
                "Term_password": term_password,
                "Date": date, 
                "Valid": "V" if datetime.strptime(date, "%d.%m.%Y.") >= datetime.now() else "N"
            }

            #cinema_screening_term_list.append(projection_term)
            #cinema_screening_term_write(projection_term)

            hall_available1 = hall_available(projection["Hall"], date, projection["Time_start"], projection["Time_end"])

            if hall_available1:
                cinema_screening_term_list.append(projection_term)
                cinema_screening_term_write(projection_term)
                all_terms_list.append(all_projection_term)
                print("Uspesno ste dodali projekciju!")
            else:
                print("Projekcija nije dodata jer je sala zauzeta!")

    today = datetime.now()
    cinema_screening_term_list = [term for term in cinema_screening_term_list if datetime.strptime(term["Date"], "%d.%m.%Y.") >= today and term["Valid"] == "V"]

    return cinema_projection_list

#def add_cinema_screening_term(projection):
#    global cinema_screening_term_list
#    global screening_term_loaded
#
#    if not screening_term_loaded:
#        cinema_screening_term_read()
#        screening_term_loaded = True
#             
#    gen = term_letter_generator()
#
#
#    selected_days = projection["Day"]
#
#    for selected_day in selected_days:
#        for date in generate_next_two_weekdays(selected_day):
#            term_password = projection["Password"] + next(gen)
#
#            hall_info = next((hall for hall in halls if hall["hall_password"] == projection["Hall"]), None)
#
#            if hall_info:
#                num_rows = hall_info["num_rows"]
#                seat_label = hall_info["seat_label"]
#
#                projection_term = {
#                    "Term_password": term_password,
#                    "Date": date, 
#                    "Valid": "V" if datetime.strptime(date, "%d.%m.%Y.") >= datetime.now() else "N"
#                }
#
#            #cinema_screening_term_list.append(projection_term)
#            #cinema_screening_term_write(projection_term)
#
#                hall_available1 = hall_available(projection["Hall"], date, projection["Time_start"], projection["Time_end"])
#
#                if hall_available1:
#                    cinema_screening_term_list.append(projection_term)
#                    cinema_screening_term_write(projection_term)
#
#                    for row in range(1, num_rows + 1):
#                        for seat_label in seat_label:
#                            seat = f"{row}{seat_label}"
#                            ticket_data = {
#                                "Term_password": term_password,
#                                "Seat_number": seat,
#                                "Status": "Free"
#                            }
#                            write_ticket(ticket_data)
#
#                    print("Uspesno ste dodali projekciju!")
#                else:
#                    print("Projekcija nije dodata jer je sala zauzeta!")
#            else:
#                print("Izabrana sala nije pronadjena")
#
#    today = datetime.now()
#    cinema_screening_term_list = [term for term in cinema_screening_term_list if datetime.strptime(term["Date"], "%d.%m.%Y.") >= today and term["Valid"] == "V"]
#
#    return cinema_projection_list

#def read_tickets():
#    tickets = []
#    try:
#        with open("tickets.txt", "r") as file:
#            lines = file.readlines()
#            for line in lines:
#                ticket_data = line.strip().split("|")
#                ticket = {
#                    "Term_password": ticket_data[0],
#                    "Seat_number": ticket_data[1],
#                    "Status": ticket_data[2]
#                }
#                tickets.append(ticket)
#    except FileNotFoundError:
#        print("Datoteka sa kartama ne postoji.")
#    return tickets

#def write_ticket(ticket):
#    with open("tickets.txt", "a") as file:
#        file.write("{}|{}|{}\n".format(ticket["Term_password"], ticket["Seat_number"], ticket["Status"]))



def hall_available(hall_choice, date, time_start, time_end):
    global cinema_projection_list

    halls_loaded_data()

    #cinema_screening_term_append()
    
    for projekcija in cinema_projection_list:
 
        if projekcija["Day"] == date and projekcija["Hall"] == hall_choice:
        #if projekcija["Day"] == date and projekcija["Hall"] == hall_choice:
            

            if not (
                    (datetime.strptime(time_start, "%H:%M") < datetime.strptime(projekcija["Time_start"], "%H:%M") and datetime.strptime(time_end, "%H:%M") < datetime.strptime(projekcija["Time_start"], "%H:%M")) or
                    (datetime.strptime(time_start, "%H:%M") > datetime.strptime(projekcija["Time_end"], "%H:%M") and datetime.strptime(time_end, "%H:%M") > datetime.strptime(projekcija["Time_end"], "%H:%M"))

            ):
                print(f"Sala {hall_choice} nije dostupna za projekciju dana {date} od {time_start} do {time_end}.")
                return False
            
        #else:
    print(f"Sala {hall_choice} je dostupna za projekciju dana {date} od {time_start} do {time_end}.")
    return True
    


def multicriteria_search_projections():
    global data_loaded
    global cinema_projection_list

    cinema_projection_append()
    #if not data_loaded:
    #    cinema_projection_read()
    #    data_loaded = True

    update_projection_status_check()
    #cinema_screening_term_append()

    print("Visekriterijumska pretraga: ")
    print("\nUnesite kriterijume pretrage (ili pritisnite Enter da preskocite):")
    criterions = {
        "film": input("Naziv filma: ").strip().lower(),
        "sala": input("Oznaka sale: ").strip().upper(),
        "datum": "",            #input("Datum odrzavanja (dd.mm.yyyy.): ").strip(),
        "vreme_pocetka": "",    #input("Vreme pocetka (hh:mm): ").strip(),
        "vreme_kraja": "",      #input("Vreme kraja (hh:mm): ").strip()
    }

    date_valid(criterions)
    start_time_valid(criterions)
    end_time_valid(criterions)
    #while True:
    #    datum = input("Datum odrzavanja (dd.mm.yyyy.): ").strip()
    #    if not datum:
    #        break
    #    elif len(datum) == 11 and datum[:2].isdigit() and datum[2] == "." and datum[3:5].isdigit() and datum[5] == "." and datum[6:10].isdigit() and datum[10] == ".":
    #        datum = datetime.strptime(datum, "%d.%m.%Y.").strftime("%d.%m.%Y.")
    #        criterions["datum"] = datum
    #        break
    #    else:
    #        print("Pogresan unos! Unesite datum u trazenom formatu.")


    #while True:
    #    vreme_pocetka = input("Vreme pocetka (hh:mm): ").strip()
    #    if not vreme_pocetka:
    #        break
    #    elif len(vreme_pocetka) == 5 and vreme_pocetka[2] == ":" and vreme_pocetka[:2].isdigit() and vreme_pocetka[3:].isdigit():
    #        try:
    #            datetime.strptime(vreme_pocetka, "%H:%M")
    #            criterions["vreme_pocetka"] = vreme_pocetka
    #            break
    #        except ValueError:
    #            vreme_pocetka = input("Pogresan unos. Unesite vreme u trazenom formatu (hh:mm): ")
    #    else:
    #        print("Pogresan unos. Unesite vreme u trazenom formatu (hh:mm). ")
    
    #while True:
    #    vreme_kraja = input("Vreme kraja (hh:mm): ").strip()
    #    if not vreme_kraja:
    #        break
    #    elif len(vreme_kraja) == 5 and vreme_kraja[2] == ":" and vreme_kraja[:2].isdigit() and vreme_kraja[3:].isdigit():
    #        try:
    #            datetime.strptime(vreme_kraja, "%H:%M")
    #            criterions["vreme_kraja"] = vreme_kraja
    #            break
    #        except ValueError:
    #            vreme_kraja = input("Pogresan unos. Unesite vreme u trazenom formatu (hh:mm): ")
    #    else:
    #        print("Pogresan unos. Unesite vreme u trazenom formatu (hh:mm). ")


            

    search_results = cinema_projection_search(cinema_projection_list, criterions)
    show_results(search_results)

def date_valid(criterions):
    while True:
        datum = input("Datum odrzavanja (dd.mm.yyyy.): ").strip()
        if not datum:
            break
        elif len(datum) == 11 and datum[:2].isdigit() and datum[2] == "." and datum[3:5].isdigit() and datum[5] == "." and datum[6:10].isdigit() and datum[10] == ".":
            while True:
                try:
                    datum = datetime.strptime(datum, "%d.%m.%Y.").strftime("%d.%m.%Y.")
                    criterions["datum"] = datum
                    break
                except ValueError:
                    datum = input("Pogresan unos! Unesite datum u trazenom formatu (dd.mm.yyyy.): ")
            break


            #datum = datetime.strptime(datum, "%d.%m.%Y.").strftime("%d.%m.%Y.")
            #criterions["datum"] = datum
            #break
        else:
            print("Pogresan unos! Unesite datum u trazenom formatu.")

def start_time_valid(criterions):
    while True:
        vreme_pocetka = input("Vreme pocetka (hh:mm): ").strip()
        if not vreme_pocetka:
            break
        elif len(vreme_pocetka) == 5 and vreme_pocetka[2] == ":" and vreme_pocetka[:2].isdigit() and vreme_pocetka[3:].isdigit():
            try:
                datetime.strptime(vreme_pocetka, "%H:%M")
                criterions["vreme_pocetka"] = vreme_pocetka
                break
            except ValueError:
                vreme_pocetka = input("Pogresan unos. Unesite vreme u trazenom formatu (hh:mm): ")
        else:
            print("Pogresan unos. Unesite vreme u trazenom formatu (hh:mm). ")

def end_time_valid(criterions):
    while True:
        vreme_kraja = input("Vreme kraja (hh:mm): ").strip()
        if not vreme_kraja:
            break
        elif len(vreme_kraja) == 5 and vreme_kraja[2] == ":" and vreme_kraja[:2].isdigit() and vreme_kraja[3:].isdigit():
            try:
                datetime.strptime(vreme_kraja, "%H:%M")
                criterions["vreme_kraja"] = vreme_kraja
                break
            except ValueError:
                vreme_kraja = input("Pogresan unos. Unesite vreme u trazenom formatu (hh:mm): ")
        else:
            print("Pogresan unos. Unesite vreme u trazenom formatu (hh:mm). ")


def cinema_projection_search(projections, criterions):
    results = []

    for projection in projections:
        projection_date = get_projection_date(projection["Password"])

        #for projection_date1 in projection_date:
        #projection_date = datetime.strptime(projection["Day"], "%d.%m.%Y.")
        #search_date = datetime.strptime(criterions["datum"], "%d.%m.%Y.")
        if (
            (not criterions["film"] or criterions["film"] == projection["Film"].lower()) and
            (not criterions["sala"] or criterions["sala"] == projection["Hall"].upper()) and
            #(not criterions["datum"] or datetime.strptime(criterions["datum"], "%d.%m.%Y.") == projection_date) and 
            #(not criterions["datum"] or search_date == projection_date) and
            (not criterions["datum"] or criterions["datum"] in projection_date) and
            #(not criterions["datum"] or any(criterion_date in projection_date for criterion_date in criterions["datum"])) and
            #(not criterions["datum"] or any(criterion_date in projection_date for criterion_date in [criterions["datum"]])) and
            (not criterions["vreme_pocetka"] or datetime.strptime(criterions["vreme_pocetka"], "%H:%M") <= datetime.strptime(projection["Time_start"], "%H:%M")) and
            (not criterions["vreme_kraja"] or datetime.strptime(criterions["vreme_kraja"], "%H:%M") >= datetime.strptime(projection["Time_end"], "%H:%M")) #and
        ):
            results.append(projection)
        
    return results

    
def get_projection_date(term_password):
    global cinema_screening_term_list
    cinema_screening_term_append()
    
    matching_dates = []
    for term in cinema_screening_term_list:
        #if term["Term_password"].startswith(term_password):
        if term["Term_password"][:4] == term_password:
            matching_dates.append(datetime.strptime(term["Date"], "%d.%m.%Y.").strftime("%d.%m.%Y."))
    
    return matching_dates #if matching_dates else "N/A"
    #if matching_dates:
    #    return matching_dates


    #return ', '.join(matching_dates) if matching_dates else "N/A"
    #return matching_dates if matching_dates else "N/A"

#    # Primer poziva funkcije
#    term_password = "neki_password"
#    result = get_projection_dates(term_password)
#
#    if result != "N/A":
#        print(f"Datumi za termin sa početkom '{term_password}': {', '.join(result)}")
#    else:
#        print(f"Nema podudaranja za termin sa početkom '{term_password}'.")


def show_results(results):

    global cinema_screening_term_list
    #cinema_screening_term_read()
    cinema_screening_term_append()

    if not results:
        print("Nema rezultata pretrage.\n")
        return

    table = PrettyTable()
    table.field_names = ["Br.", "Naziv filma", "Oznaka sale", "Datum odrzavanja", "Vreme pocetka", "Vreme kraja"]

    row_counter1 = 1
    #for i, result in enumerate(results, start = 1):
    for result in results:
        date_str = get_projection_date(result["Password"])
        #date_rows = ', '.join(date_str)
        date_rows = date_str
        for date_row in date_rows:

            table.add_row([row_counter1, result["Film"], result["Hall"], date_row, result["Time_start"], result["Time_end"]])
            row_counter1 += 1
        #table.add_row([result["Film"], result["Hall"], date_str, result["Time_start"], result["Time_end"]])

    print(table)

    while True:
        inputN = input("[N] NAZAD: ").upper()
        if inputN == "N":
            break
        else:
            print("Pogrešan unos. Molim vas unesite 'N' da biste se vratili nazad.\n")


def multicriteria_search_projections1(username, condition, seller_username):
    global data_loaded
    global cinema_projection_list

    #if not data_loaded:
    #    cinema_projection_read()
    #    data_loaded = True
    cinema_projection_append()

    update_projection_status_check()
    #cinema_screening_term_append()

    print("Visekriterijumska pretraga: ")
    print("\nUnesite kriterijume pretrage (ili pritisnite Enter da preskocite):")
    criterions = {
        "film": input("Naziv filma: ").strip().lower(),
        "sala": input("Oznaka sale: ").strip().upper(),
        "datum": "",            #input("Datum odrzavanja (dd.mm.yyyy.): ").strip(),
        "vreme_pocetka": "",    #input("Vreme pocetka (hh:mm): ").strip(),
        "vreme_kraja": "",      #input("Vreme kraja (hh:mm): ").strip()
    }

    date_valid(criterions)
    start_time_valid(criterions)
    end_time_valid(criterions)

    search_results = cinema_projection_search(cinema_projection_list, criterions)
    show_results1(search_results, username, condition, seller_username)


def show_results1(results, username, condition, seller_username):

    global cinema_screening_term_list
    #cinema_screening_term_read()
    cinema_screening_term_append()

    if not results:
        print("Nema rezultata pretrage.\n")
        return

    table = PrettyTable()
    table.field_names = ["Br.", "Naziv filma", "Oznaka sale", "Datum odrzavanja", "Vreme pocetka", "Vreme kraja"]

    #for date_row in date_rows:
    user_input_counter = 0

    selected_dates = []                                                       #!!!!!!!
    for result in results:
        date_str = get_projection_date(result["Password"])
        #date_rows = ', '.join(date_str)
        date_rows = date_str
        for date_row in date_rows:
            dates = date_row.split(", ")
            for date in dates:
                user_input_counter += 1
                table.add_row([user_input_counter, result["Film"], result["Hall"], date, result["Time_start"], result["Time_end"]])
                selected_dates.append(date)                             #!!!!!!!!!!!!


    #for result in results:
    #    date_str = get_projection_date(result["Password"])
    #    date_rows = date_str.split(", ")
#
    #    for date in date_rows:
    #        user_input_counter += 1
    #        table.add_row([user_input_counter, result["Film"], result["Hall"], date, result["Time_start"], result["Time_end"]])
    #        selected_dates.append(date)

    print(table)

    while True:
        #try:
        
        #selected_row = int(input("Unesite redni broj za odabir datuma: ")).strip()  #(ili 'N' za nazad)
        selected_row = input("Unesite redni broj za odabir datuma ([N] Nazad): ").strip()  #(ili 'N' za nazad)

        if not selected_row:
            print("Pogresan unos! Molimo vas pokusajte ponovo.")
        
        elif selected_row.upper() == "N":
            print("Izabrali ste opciju Nazad. \n")
            break

        elif selected_row.isdigit():
            #if selected_row == 'N' or selected_row == 'n':
            #    break

            #if 1 <= selected_row <= len(results):
            if 1 <= int(selected_row) <= user_input_counter:
            #if 1 <= selected_row <= (sum(len(date_rows) for date_rows in results) - 1):
                selected_date = get_projection_date(results[int(selected_row) - 1]["Password"])

                #print(user_input_counter)

                selected_date = selected_dates[int(selected_row) - 1]            #!!!!!!!!!!!!!!

                write_to_reserved_tickets(selected_date, username, condition, seller_username)
                #print(f"Odabrali ste datum: {', '.join(selected_date)}")
                #print(f"Odabrali ste datum: {date}")
                break
            

        else:
                print("Pogresan unos! Pokusajte ponovo.")
        #except ValueError:
        #    print("Pogrešan unos. Unesite broj reda ili 'N' za nazad.")    

def get_password_projection1(selected_date):
    global cinema_screening_term_list

    for term in cinema_screening_term_list:
        if term["Date"] == selected_date:
            return term["Term_password"]
        

##def write_to_reserved_tickets(selected_date):
##    with open("reserved_tickets.txt", "a") as file:
##        #for date in selected_date:
##            #pass
##        password = get_password_projection1(selected_date)
##        seat_info = overview_of_available_seats(password)
##        if seat_info is not None:
##            rows, columns = seat_info
##            seat_matrix = generate_seat_matrix(rows, columns, password)
##            
##            reserved_cards_list = load_reserved_cards()
##
##            matrix(seat_matrix, rows, columns, password, selected_date, reserved_cards_list)
##            file.write(f"{password}|{selected_date}|{seat}\n")
##            update_matrix_with_reservations(seat_matrix, reserved_cards_list)
##        else:
##            print("Nisu pronađeni podaci o sedištima za unetu šifru projekcije.")

def write_to_reserved_tickets(selected_date, username, condition, seller_username):
    with open("reserved_tickets.txt", "a") as file:
        #for date in selected_date:
            #pass
        password = get_password_projection1(selected_date)
        seat_info = overview_of_available_seats(password)
        if seat_info is not None:
            rows, columns = seat_info
            seat_matrix = generate_seat_matrix(rows, columns, password)
            
            reserved_tickets_read()
            ########reserved_tickets_list = load_reserved_cards()

            seat, card_password, card_date = matrix(seat_matrix, rows, columns, password, selected_date, reserved_tickets_list, username, condition, seller_username)
            #seller_username = ""
            #seat, card_password, card_date = matrix(seat_matrix, rows, columns, password, selected_date, username, condition, seller_username)


            #add_reserved_cards(seat, card_password, card_date)
            #file.write(f"{password}|{selected_date}|{seat}\n")
            update_matrix_with_reservations(seat_matrix, reserved_tickets_list, card_password)

            while True:     
                print("Da li zelite da rezervisete jos karata?")  
                print("[1] DA")      
                print("[2] NE") 
                more_cards = input("Izaberite opciju: ")
                if more_cards == "1":
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


                            #file.write(f"{password}|{selected_date}|{seat}\n")
                            #update_matrix_with_reservations(seat_matrix, reserved_cards_list)
                                #break
                    
                        #else:
                        #    print("Pogresan unos! Molimo vas unesite validno sediste.")
                            

                    #seat = input("Unesite oznaku sedista (na primer 3F): ").strip().upper()
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

        else:
            print("Nisu pronađeni podaci o sedištima za unetu šifru projekcije.")


        #file.write(f"{password}|{selected_date}\n")
        #print(f"Odabrali ste datum: {selected_date}")


#def search_projection():

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

def load_reserved_cards():
    
    reserved_cards = []
    try:
        with open("reserved_tickets.txt", "r") as file:
            for line in file:
                apart_line = line.strip().split("|")
                #term_password, _, seat = line.strip().split("|")
                term_password = apart_line[0]
                card_date = apart_line[1]
                seat = apart_line[2]
                username = apart_line[3]
                condition = apart_line[4]
                real_date = apart_line[5],
                seller_username = apart_line[6]
                card_price = apart_line[7]
                reserved_cards.append({"card_password": term_password, "card_date": card_date, "seat": seat, "username": username, "condition": condition, "real_date": real_date, "seller_username": seller_username, "card_price": card_price})
    except FileNotFoundError:
        print("Fajl nije pronadjen!")
        #pass  
    return reserved_cards

#reserved_tickets_list_loaded = False
#def load_reserved_cards():
#    if not reserved_tickets_list_loaded:
#        reserved

def reserved_tickets_list_read():
    reserved_cards = []
    try:
        with open("reserved_tickets.txt", "r") as file:
            for line in file:
                apart_line = line.strip().split("|")
                #term_password, _, seat = line.strip().split("|")
                term_password = apart_line[0]
                card_date = apart_line[1]
                seat = apart_line[2]
                username = apart_line[3]
                condition = apart_line[4]
                real_date = apart_line[5],
                seller_username = apart_line[6]
                card_price = apart_line[7]
                reserved_cards.append({"card_password": term_password, "card_date": card_date, "seat": seat, "username": username, "condition": condition, "real_date": real_date, "seller_username": seller_username, "card_price": card_price})
    except FileNotFoundError:
        print("Fajl nije pronadjen!")
        #pass  
    return reserved_cards


reserved_tickets_list = []



def matrix(seat_matrix, rows, columns, card_password, card_date, reserved_tickets_list, username, condition, seller_username):
    update_matrix_with_reservations(seat_matrix, reserved_tickets_list, card_password)
    print("Matrica slobodnih sedišta:")
    print_seat_matrix(seat_matrix)
    while True:
        #try:
        seat = input("Unesite oznaku sedista (na primer 3F): ").strip().upper()
        if not seat:
            print("Pogresan unos! Molimo vas unesite validno sediste.")
        #elif seat_matrix[row_number][ord(column_letter) - ord('A')] == "X":
        #    print("Sediste je zauzeto! Molimo vas izaberite drugo sediste.")
        elif seat[:-1].isdigit() and seat[-1].isalpha():
            #print("Pogresan unos! Molimo vas pokusajte ponovo.")

            #try:
            row_number = int(seat[:-1]) - 1
            column_letter = seat[-1]
            #except ValueError:
            #    print("Uneto sediste ne postoji! Molimo vas pokusajte ponovo.")

            try:
                if seat_matrix[row_number][ord(column_letter) - ord('A')] == "X":
                    print("Sediste je zauzeto! Molimo vas izaberite drugo sediste.")
                elif 0 <= row_number < rows and 'A' <= column_letter <= chr(ord('A') + columns - 1):
                    seat_matrix[row_number][ord(column_letter) - ord('A')] = "X"
                    print("Uspesno ste rezervisali sediste")
                    add_reserved_cards(seat, card_password, card_date, username, condition, seller_username)
                    return seat, card_password, card_date
            except IndexError:
                print("Sediste nije dostupno!") 
                #else:
                #    print("Sediste nije dostupno!")    
                       
            #break
        else:
            print("Pogresan unos! Molimo vas unesite validno sediste.")
        #except ValueError:
        #    print("Pogresan unos! Molimo vas unesite validno sediste.")

def update_matrix_with_reservations(seat_matrix, reserved_cards, card_password):
    for reserved_card in reserved_cards:
        if reserved_card["card_password"] == card_password:
            seat = reserved_card["seat"]
            row_number = int(seat[:-1]) - 1
            column_letter = seat[-1]
            if 0 <= row_number < len(seat_matrix) and 'A' <= column_letter <= chr(ord('A') + len(seat_matrix[0]) - 1):
                seat_matrix[row_number][ord(column_letter) - ord('A')] = "X"

def add_reserved_cards(seat, card_password, card_date, username, condition, seller_username):
    global cinema_screening_term_list
    #global reserved_tickets_list    
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
        #print("WEEEEkk dayy" + str(weekday))
        if weekday == 1:
            card_price = float(projection["Price"]) - 50
            #print("Manja cena")
        elif weekday in [5, 6]:
            card_price = float(projection["Price"]) + 50
            #print("Uvecana cena")
        else:
            card_price = projection["Price"]
            #print("Nista")

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

        #print("Ubacena karta u listu")

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
    #if not data_loaded:
    #    cinema_projection_read()
    #    data_loaded = True
    
    cinema_projection_append()

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

def add_change_delete_projections():
    global cinema_screening_term_list
    cinema_screening_term_append()
    global reserved_tickets_list
    reserved_tickets_read()
    global cinema_projection_list
    cinema_projection_append()
    while True:
        print("[1] Dodavanje projekcija")
        print("[2] Izmena projekcija")
        print("[3] Brisanje projekcija")
        print("[N] Nazad")
        choose_option = input("Izaberite opciju: ").strip()
        if choose_option == "1":
            add_projection()
            while True:
                print("Da li zelite da nastavite sa dodavanjem projekcija?")
                print("[D] Da")
                print("[N] Ne")
                choose = input("Izaberite opciju: ").strip().upper()
                if choose == "D":
                    add_projection()
                elif choose == "N":
                    break
                else:
                    print("Pogresan unos! Pokusajte ponovo.")

        elif choose_option == "2":
            change_projection()
            while True:
                print("Da li zelite da nastavite sa izmenom projekcija?")
                print("[D] Da")
                print("[N] Ne")
                choose = input("Izaberite opciju: ").strip().upper()
                if choose == "D":
                    change_projection()
                elif choose == "N":
                    break
                else:
                    print("Pogresan unos! Pokusajte ponovo.")

        elif choose_option == "3":
            delete_projection()
            while True:
                print("Da li zelite da nastavite sa brisanjem projekcija?")
                print("[D] Da")
                print("[N] Ne")
                choose = input("Izaberite opciju: ").strip().upper()
                if choose == "D":
                    delete_projection()
                elif choose == "N":
                    break
                else:
                    print("Pogresan unos! Pokusajte ponovo.")
        elif choose_option.upper() == "N":
            break
        else:
            print("Pogresan unos! Pokusajte ponovo.")


def overview_of_available_projections():
    global cinema_projection_list
    cinema_projection_append()
    table = PrettyTable()
    counter = 1
    table.field_names = ["Br.", "Sifra_projekcije", "Sala", "Vreme pocetka", "Vreme kraja", "Dan", "Film", "Cena"]
    for projection in cinema_projection_list:
        #if projection not in table:
        table.add_row([counter, projection["Password"], projection["Hall"], projection["Time_start"], projection["Time_end"], (", ").join(projection["Day"]), projection["Film"], projection["Price"]])
        counter += 1
    
    if table:
        print(table)
    else:
        print("Nema dostupnih projekcija")


def delete_projection():
    global reserved_tickets_list
    global cinema_projection_list
    cinema_projection_append()

    global cinema_screening_term_list
    cinema_screening_term_append()
    global all_terms_list
    fill_all_term_append()
    while True:
        overview_of_available_projections()
        delete_projection = input("Unesite redni broj projekcije koju zelite da obrisete ([N] Nazad): ").strip()
        if delete_projection.isdigit():
            delete_projection_index = int(delete_projection) - 1
            if 0 <= delete_projection_index < len(cinema_projection_list):
                for reserved_ticket in reserved_tickets_list:
                    if cinema_projection_list[delete_projection_index]["Password"].strip() == reserved_ticket["card_password"][:4]:
                        print("Ne mozete da obrisete zeljenu projekciju jer su vec rezervisane\prodane karte!\n")
                        while True:
                            inputN = input("[N] Nazad: ").strip()
                            if inputN.upper() == "N":
                                break
                            else:
                                print("Pogresan unos! Pokusajte ponovo.")
                        break
                
                

                else:
                    new_list = []

                    for term in cinema_screening_term_list:
                        if cinema_projection_list[delete_projection_index]["Password"].strip() != term["Term_password"][:4]:
                            new_list.append(term)
                    
                    cinema_screening_term_list = new_list


                    new_list1 = []
                    for all_term in all_terms_list:
                        if cinema_projection_list[delete_projection_index]["Password"].strip() != all_term["Term_password"][:4]:
                            new_list1.append(all_term)
                    all_terms_list = new_list1

                    bad_password = cinema_projection_list[delete_projection_index]["Password"].strip()
                    new_list3 = []
                    for projection in cinema_projection_list:
                        if projection["Password"] != bad_password:
                            new_list3.append(projection)
                    cinema_projection_list = new_list3


#                    for term in cinema_screening_term_list:
#                        if cinema_projection_list[delete_projection_index]["Password"].strip() == term["Term_password"][:4]:
#                            cinema_screening_term_list.remove(term)
#
#
#                    for all_term in all_terms_list:
#                        if cinema_projection_list[delete_projection_index]["Password"].strip() == all_term["Term_password"][:4]:
#                            all_terms_list.remove(all_term)




                    
#                    cinema_screening_term_list = [term for term in cinema_screening_term_list if cinema_projection_list[delete_projection_index]["Password"].strip() != term["Term_password"][:4]]
#                    
#                    all_terms_list = [term for term in all_terms_list if cinema_projection_list[delete_projection_index]["Password"].strip() != term["Term_password"][:4]]
#
#                    cinema_projection_list = [projection for i, projection in enumerate(cinema_projection_list) if i != delete_projection_index]


                            #del all_term
                    #all_terms_list = [term for term in all_terms_list if cinema_projection_list[delete_projection_index]["Password"].strip() != term["Term_password"][:4]]

                    with open("projection_term.txt", "w") as file3:
                        pass
                    with open("projection_term.txt", "a") as file4:
                        for all_term in all_terms_list:
                            #print("Novi fajl")
                            file4.write("{}|{}|{}\n".format(all_term["Term_password"], all_term["Date"], all_term["Valid"]))
                        

#                   del cinema_projection_list[delete_projection_index]
                    with open("cinema_projections.txt", "w") as file:
                        pass
                    with open("cinema_projections.txt", "a") as file1:
                        for projection in cinema_projection_list:
                            file1.write("{}|{}|{}|{}|{}|{}|{}\n".format(projection["Password"], projection["Hall"], projection["Time_start"], projection["Time_end"], (", ").join(projection["Day"]), projection["Film"], projection["Price"]))
                        break
            else:
                print("Redni broj koji ste uneli nije dat u tabeli! Pokusajte ponovo.")
            
        elif delete_projection.upper() == "N":
            break
        else:
            print("Pogresan unos! Pokusajte ponovo.")

def change_projection():
    global cinema_projection_list
    cinema_projection_append()
    while True:
        overview_of_available_projections()
        change_projection = input("Unesite redni broj projekcije koju zelite da izmenite ([N] Nazad): ").strip()
        if change_projection.isdigit():
            change_projection_index = int(change_projection) - 1
            if 0 <= change_projection_index < len(cinema_projection_list):
                for reserved_ticket in reserved_tickets_list:
                    if cinema_projection_list[change_projection_index]["Password"].strip() == reserved_ticket["card_password"][:4]:
                        print("Ne mozete da izmenite zeljenu projekciju jer su vec rezervisane\prodane karte!\n")
                        while True:
                            inputN = input("[N] Nazad: ").strip()
                            if inputN.upper() == "N":
                                break
                            else:
                                print("Pogresan unos! Pokusajte ponovo.")
                        break
                else:
                    while True:
                        print("Sta zelite da izmenite? ")
                        #print("[1] Sifra projekcije")
                        print("[1] Sala projekcije")
                        print("[2] Vreme pocetka i kraja projekcije")
                        print("[3] Dane projekcije")
                        print("[4] Film projekcije")
                        print("[5] Cena projekcije")
                        print("[N] Nazad")
                        choose_change = input("Izaberite opciju: ").strip()
                        #if choose_change == "1":
                        #    while True:
                        #        #valid_projection_password(input_new_password)
                        #        input_new_password = input("Unesi novu sifru projekcije: ").strip()
                        #        #valid_projection_password(input_new_password)
                        #        input_new_password = valid_projection_password(input_new_password)
                        #        cinema_projection_list[change_projection_index]["Password"] = input_new_password
                        #        change_projection_process()
                        #        print("Uspesno ste izmenili sifru projekcije.\n")
                        #        break

                        if choose_change == "1":
                            while True:
                                #valid_projection_password(input_new_password)
                                print("Sale: [A1], [A2], [A3]")
                                input_new_hall = input("Unesi novu salu projekcije: ").strip().upper()
                                #valid_projection_password(input_new_password)
                                input_new_hall = halls_valid(input_new_hall)
                                cinema_projection_list[change_projection_index]["Hall"] = input_new_hall
                                change_projection_process()
                                print("Uspesno ste izmenili salu projekcije.\n")
                                break
                        elif choose_change == "2":
                            while True:
                                #valid_projection_password(input_new_password)
                                input_new_time_start = input("Unesi novo vreme pocetka projekcije (hh:mm): ").strip()
                                #valid_projection_password(input_new_password)
                                input_new_time_start = projection_start_time_valid(input_new_time_start)
                                cinema_projection_list[change_projection_index]["Time_start"] = input_new_time_start
                                change_projection_process()
                                print("Uspesno ste izmenili vreme pocetka projekcije.\n")
                                break
                        #elif choose_change == "4":
                            while True:
                                #valid_projection_password(input_new_password)
                                input_new_time_end = input("Unesi novo vreme kraja projekcije (hh:mm): ").strip()
                                #valid_projection_password(input_new_password)
                                input_new_time_end = projection_end_time_valid(input_new_time_end, input_new_time_start)
                                cinema_projection_list[change_projection_index]["Time_end"] = input_new_time_end
                                change_projection_process()
                                print("Uspesno ste izmenili vreme kraja projekcije.\n")
                                break
                        elif choose_change == "3":
                            while True:

                                print("'ponedeljak', 'utorak', 'sreda', 'cetvrtak', 'petak', 'subota', 'nedelja'")
                                input_new_day = input("Unesite dane u nedelji kada se projekcija održava (razdvojite zarezom): ").split(", ")
                                valid_days = ["ponedeljak", "utorak", "sreda", "cetvrtak", "petak", "subota", "nedelja"]
                                if all(day1 in valid_days for day1 in input_new_day ):
                                    cinema_projection_list[change_projection_index]["Day"] = input_new_day
                                    change_projection_process()
                                    print("Uspesno ste izmenili dane projekcije.\n")
                                    break

                                else:
                                    print("Vas unos nije ispravan! Molimo vas pokusajte ponovo.\n")



                                ##valid_projection_password(input_new_password)
                                #input_new_day = input("Unesi nove dane projekcije: ").strip()
                                ##valid_projection_password(input_new_password)
                                #input_new_day = projection_end_time_valid(input_new_day)
                                #cinema_projection_list[change_projection_index]["Day"] = input_new_day
                                #change_projection_process()
                        elif choose_change == "4":
                            while True:
                                overview_of_available_movies()
                                input_new_film = input("Unesi novi film projekcije: ").strip()
                                #valid_projection_password(input_new_password)
                                input_new_film = film_valid(input_new_film)
                                cinema_projection_list[change_projection_index]["Film"] = input_new_film
                                change_projection_process()
                                print("Uspesno ste izmenili film projekcije.\n")
                                break



                            #film_valid(choice_film)
                        elif choose_change == "5":
                            while True:
                                try:
                                    input_new_price = float(input("Unesite novu cenu karte: "))
                                    cinema_projection_list[change_projection_index]["Price"] = input_new_price
                                    change_projection_process()
                                    print("Uspesno ste izmenili cenu karte projekcije.\n")
                                    break
                                except ValueError:
                                    print("Pogresan unos. Molimo vas pokusajte ponovo! ")

                        elif choose_change.upper() == "N":
                            break
                        else:
                            print("Pogresan unos! Pokusajte ponovo.")


                    #del cinema_projection_list[change_projection_index]
                        #with open("cinema_projections.txt", "w") as file:
                        #    pass
                        #with open("cinema_projections.txt", "a") as file1:
                        #    for projection in cinema_projection_list:
                        #        file1.write("{}|{}|{}|{}|{}|{}|{}\n".format(projection["Password"], projection["Hall"], projection["Time_start"], projection["Time_end"], (", ").join(projection["Day"]), projection["Film"], projection["Price"]))
                        #    break
            else:
                print("Redni broj koji ste uneli nije dat u tabeli! Pokusajte ponovo.")
            
        elif change_projection.upper() == "N":
            break
        else:
            print("Pogresan unos! Pokusajte ponovo.")

def change_projection_process():
    global cinema_projection_list
    cinema_projection_append()
    with open("cinema_projections.txt", "w") as file:
        pass #(" ")
    with open("cinema_projections.txt", "a") as file1:
        for cinema in cinema_projection_list:
            file1.write("{}|{}|{}|{}|{}|{}|{}\n" .format(cinema["Password"], cinema["Hall"], cinema["Time_start"], cinema["Time_end"], (", ").join(cinema["Day"]), cinema["Film"], cinema["Price"]))
#def selection_projection_dates_by_search():
#    multicriteria_search_projections1()
#    overview_of_available_seats()


reserved_tickets_loaded = False
def reserved_tickets_read():
    global reserved_tickets_loaded
    global reserved_tickets_list
    if not reserved_tickets_loaded:
        reserved_tickets_list = load_reserved_cards()
        reserved_tickets_loaded = True
        return reserved_tickets_list




#def write_to_reserved_tickets(selected_date, seats):
#    with open("reserved_tickets.txt", "a") as file:
#        password = get_password_projection1(selected_date)
#        seat_info = overview_of_available_seats(password)
#
#        if seat_info is not None:
#            rows, columns = seat_info
#            seat_matrix = generate_seat_matrix(rows, columns, password)
#            
#            reserved_cards_list = load_reserved_cards()
#            
#            for seat in seats:
#                matrix(seat_matrix, rows, columns, password, selected_date, reserved_cards_list, seat)
#                file.write(f"{password}|{selected_date}|{seat}\n")  # Dodajte sedište u zapis
#
#            update_matrix_with_reservations(seat_matrix, reserved_cards_list)
#            print(f"Odabrali ste datum: {selected_date}, sedišta: {', '.join(seats)}")
#        else:
#            print("Nisu pronađeni podaci o sedištima za unetu šifru projekcije.")
#
#def matrix(seat_matrix, rows, columns, card_password, card_date, reserved_cards_list, selected_seat):
#    update_matrix_with_reservations(seat_matrix, reserved_cards_list)
#    print("Matrica slobodnih sedišta:")
#    print_seat_matrix(seat_matrix)
#    
#    seat = selected_seat
#    row_number = int(seat[:-1]) - 1
#    column_letter = seat[-1]
#
#    if 0 <= row_number < rows and 'A' <= column_letter <= chr(ord('A') + columns - 1):
#        if seat_matrix[row_number][ord(column_letter) - ord('A')] != "X":
#            seat_matrix[row_number][ord(column_letter) - ord('A')] = "X"
#            print("Uspesno ste rezervisali sediste")
#            add_reserved_cards(seat, card_password, card_date, reserved_cards_list)
#        else:
#            print("Sediste je vec rezervisano!")
#
#    else:
#        print("Sediste nije dostupno!")
#    
#    return seat
#
#def add_reserved_cards(seat, card_password, card_date, reserved_cards_list):
#    reserved_ticket = {
#        "card_password": card_password,
#        "card_date": card_date,
#        "seat": seat
#    }
#    reserved_cards_list.append(reserved_ticket)

if __name__ == '__main__':
    #read_films()
    #add_projection()
    #cinema_screening_term()
    multicriteria_search_projections()
