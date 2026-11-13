from prettytable import PrettyTable
from datetime import datetime


lista_filmova = []
data_loaded = False

def add_film():
    while True:
        naziv = input("Unesite naziv filma: ").strip()
        #if naziv == "" or naziv == "\n":
        if not naziv.strip():
            print("Ime filma nije validno! Pokusajte ponovo.")
        else:
            break

    while True:
        zanr = input("Unesite zanr: ").strip().lower().split(", ")
        if not zanr:
            print("Ime zanra nije validno! Pokusajte ponovo.")
        else:
            break
        
    while True:
        trajanje = input("Unesite trajanje (u minutama): ").strip()
        if trajanje.isdigit() == True:
            break
        else:
            print("Molimo vas unesite broj minuta trajanja!")
    while True:
        reziseri = input("Unesite rezisere (razdvojite zarezom): ").split(", ")
        if all(reziser.strip() != "" for reziser in reziseri):
            break
        else:
            print("Vas unos nije ispravan! Molimo vas pokusajte ponovo.")

    while True:
        uloge = input("Unesite uloge (razdvojite zarezom): ").split(", ")
        if all(uloga.strip() != "" for uloga in uloge):
            break
        else:
            print("Vas unos nije ispravan! Molimo vas pokusajte ponovo.")

    while True:
        zemlja_porekla = input("Unesite zemlju porekla: ")
        if not zemlja_porekla.strip():
            print("Vas unos nije ispravan! Molimo vas pokusajte ponovo.")
        else:
            break
    while True:
        try:
            godina_proizvodnje = int(input("Unesite godinu proizvodnje: "))
            break
        except ValueError:
            print("Molimo vas da unesete validan broj!")


    film = {"Naziv": naziv,
            "Zanr": zanr,
            "Trajanje": trajanje,
            "Reziseri": reziseri,
            "Uloge": uloge,
            "Zemlja_porekla": zemlja_porekla,
            "Godina_proizvodnje": godina_proizvodnje
            }
    lista_filmova.append(film)
    save_film_file(film)

    # Dodavanje novog filma u listu ako već nije tamo
    if film not in lista_filmova:
        lista_filmova.append(film)
    
def save_film_file(film):
    with open("film_file.txt", "a") as file:
        #file.write(f"{film['Naziv']} | {film['Zanr']} | {film['Trajanje']} | {', '.join(film['Reziseri'])} | {', '.join(film['Uloge'])} | {film['Zemlja_porekla']} | {film['Godina_proizvodnje']} \n")    # Ovde sam stao !!!!!!!!!!!     
        file.write("{}|{}|{}|{}|{}|{}|{}\n".format(film['Naziv'], (", ").join(film['Zanr']), film['Trajanje'], ', '.join(film['Reziseri']), ', '.join(film['Uloge']), film['Zemlja_porekla'], film['Godina_proizvodnje']))

def read_films():
    global lista_filmova
    #lista_filmova = []  # Resetovanje podataka pre ponovnog ucitavanja
    with open("film_file.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            line_apart = line.strip().split("|")
            film = {
                "Naziv": line_apart[0],
                "Zanr": line_apart[1].split(", "),
                "Trajanje": line_apart[2],
                "Reziseri": line_apart[3].split(", "),
                "Uloge": line_apart[4].split(", "),
                "Zemlja_porekla": line_apart[5],
                "Godina_proizvodnje": line_apart[6]
            }

            lista_filmova.append(film)
    return lista_filmova

def read_film_file():
    global data_loaded
    global lista_filmova

    if not data_loaded:
        lista_filmova = read_films()
        data_loaded = True
        return lista_filmova

def overview_of_available_movies():
    
    #global lista_filmova
    global data_loaded

    #if not data_loaded:
    #    lista_filmova = read_films()
    #    data_loaded = True
    read_film_file()                       
    table = PrettyTable()
    # Redosled kolona u tabeli
    table.field_names = ["Br.", "Naziv filma", "Zanr", "Trajanje", "Reziseri", "Uloge", "Zemlja porekla", "Godina proizvodnje"]

    for i, film in enumerate(lista_filmova, start = 1):
        #for naziv, information in film.items():
        table.add_row([
            i,
            film["Naziv"],
            ", ".join(film["Zanr"]),
            film["Trajanje"],
            ", ".join(film["Reziseri"]),
            ", ".join(film["Uloge"]),
            film["Zemlja_porekla"],
            film["Godina_proizvodnje"]
        ])
    
    print(table)
    #while True:
    #    inputN = input("[N] Nazad \n").strip()
    #    if inputN.upper() == "N":
    #        break
    #    #else:
    #    print("Pogrešan unos. Molim vas unesite 'N' da biste se vratili nazad.\n")

def simple_search():
    global lista_filmova
    print("\nObična pretraga:")
    print("Kriterijumi pretrage: [1]naziv, [2]zanr, [3]min_trajanje, [4]max_trajanje, [5]reziser, [6]uloga, [7]zemlja, [8]godina ")
    while True:
        criterion = input("Unesite kriterijum pretrage: ", ).strip().lower()
        if criterion == "1":
            criterion = "naziv"
            break
        elif criterion == "2":
            criterion = "zanr"
            break
        elif criterion == "3":
            criterion = "min_trajanje"
            break
        elif criterion == "4":
            criterion = "max_trajanje"
            break
        elif criterion == "5":
            criterion = "reziser"
            break
        elif criterion == "6":
            criterion = "uloga"
            break
        elif criterion == "7":
            criterion = "zemlja"
            break
        elif criterion == "8":
            criterion = "godina"
            break
        else:
            print("Pogresan unos! Pokusajte ponovo.\n")
    value = input("Unesite vrednost pretrage: ").strip().lower()

    if criterion == "min_trajanje":
        while True:
            min_duration = value
            if not min_duration:
                break  # Preskoci unos minimalnog trajanja ako je pritisnuto Enter
            elif not min_duration.isdigit():
                print("Molimo vas unesite validan broj za minimalno trajanje!")
            else:
                value = min_duration
                break
            value = input("Unesite vrednost pretrage: ").strip().lower()

    if criterion == "max_trajanje":
        while True:
            max_duration = value
            if not max_duration:
                break  # Preskoci unos minimalnog trajanja ako je pritisnuto Enter
            elif not max_duration.isdigit():
                print("Molimo vas unesite validan broj za minimalno trajanje!")
            else:
                value = max_duration
                break
            value = input("Unesite vrednost pretrage: ").strip().lower()
    
    if criterion == "godina":
        while True:
            godina = value
            if not godina:
                break   # Preskoci unos godine ako je pritisnuto Enter 
            elif not godina.isdigit():
                print("Molimo vas unesite validan broj godine.")
            else:
                value = godina
                break
    #if criterion == "min_trajanje":
    #    while True:
    #        value = input("Minimalno trajanje (u minutama): ").strip()
    #        if not value:
    #            break  # Preskoci unos minimalnog trajanja ako je pritisnuto Enter
    #        elif not value.isdigit():
    #            print("Molimo vas unesite validan broj za minimalno trajanje!")
    #        else:
    #            criterions["min_trajanje"] = value
    #            break

    #if criterion == "min_trajanje":
    #    min_duration_valid(value)

    #if criterion in ["min_trajanje", "max_trajanje", "godina"]:
    #    single_value = single_value_valid(value)
    #    while not single_value:
    #        value = input("Unesite validnu vrednost pretrage: ").strip().lower()
    #        single_value = single_value_valid(value)
    #
    #    value = single_value  # Ažuriranje vrednosti nakon provere

    read_film_file()
    search_results = movie_search(lista_filmova, {criterion: value})
    show_results(search_results)

    #while True:
    #    inputN = input("[N] Nazad \n").upper()
    #    if inputN == "N":
    #        break
    #    else:
    #        print("Pogrešan unos. Molim vas unesite 'N' da biste se vratili nazad.\n")

#def single_value_valid(value):
#    if not value.strip():
#        print("Vrednost nije validna! Molimo vas pokusajte ponovo.")
#        return None
#    return value

def multicriteria_search():
    global lista_filmova

    read_film_file()
    print("Visekriterijumska pretraga: ")
    print("\nUnesite kriterijume pretrage (ili pritisnite Enter da preskocite):")
    criterions = {
        "naziv": input("Naziv filma: ").strip().lower(),
        "zanr": input("Zanr: ").strip().lower(),    
        "min_trajanje": "",         #input("Minimalno trajanje (u minutama): ").strip(),
        "max_trajanje": "",         #input("Maksimalno trajanje (u minutama): ").strip(),
        "reziser": input("Reziser: ").strip().lower(),
        "uloga": input("Glavna uloga: ").strip().lower(),
        "zemlja": input("Zemlja porekla: ").strip().lower(),
        "godina": ""               #input("Godina proizvodnje: ").strip()
    }

    min_duration_valid(criterions)
    max_duration_valid(criterions)
    year_valid(criterions)

    search_results = movie_search(lista_filmova, criterions)
    show_results(search_results)

def min_duration_valid(criterions):
    while True:
        min_duration = input("Minimalno trajanje (u minutama): ").strip()
        if not min_duration:
            break  # Preskoci unos minimalnog trajanja ako je pritisnuto Enter
        elif not min_duration.isdigit():
            print("Molimo vas unesite validan broj za minimalno trajanje!")
        else:
            criterions["min_trajanje"] = min_duration
            break

def max_duration_valid(criterions):
    while True:
        max_duration = input("Maksimalno trajanje (u minutama): ").strip()
        if not max_duration:
            break  # Preskoci unos maksimalnog trajanja ako je pritisnuto Enter
        elif not max_duration.isdigit():
            print("Molimo vas unesite validan broj za maksimalno trajanje!")
        elif criterions["min_trajanje"] and int(max_duration) < int(criterions["min_trajanje"]):
            print("Maksimalno trajanje ne može biti manje od minimalnog trajanja!")
        else:
            criterions["max_trajanje"] = max_duration
            break

def year_valid(criterions):
    while True:
        godina = input("Godina proizvodnje: ")
        if not godina:
            break   # Preskoci unos godine ako je pritisnuto Enter 
        elif not godina.isdigit():
            print("Molimo vas unesite validan broj godine.")
        else:
            criterions["godina"] = godina
            break

def movie_search(lista_filmova, criterions):
    search_results = []

    for film in lista_filmova:
        conditions_correct = True
        for criterion, value in criterions.items():
            if value and (
                criterion == "naziv" and value.lower() not in film["Naziv"].lower() or
                criterion == "zanr" and value.lower() not in film["Zanr"].lower() or

                #criterion == "min_trajanje" and int(film["Trajanje"].split()[0]) < int(value) or
                #criterion == "max_trajanje" and int(film["Trajanje"].split()[0]) > int(value) or

                criterion == "min_trajanje" and int(film["Trajanje"].split()[0]) < int(value) or
                criterion == "max_trajanje" and int(film["Trajanje"].split()[0]) > int(value) or
                criterion == "reziser" and value.lower() not in [r.lower() for r in film["Reziseri"]] or
                criterion == "uloga" and value.lower() not in [r.lower() for r in film["Uloge"]] or
                criterion == "zemlja" and value.lower() != film["Zemlja_porekla"].lower() or
                criterion == "godina" and value != str(film["Godina_proizvodnje"]) 
            ):
                conditions_correct = False
                break
        if conditions_correct == True:
            search_results.append(film)
    return search_results

def show_results(results):
    if not results:
        print("Nema rezultata koji zadovoljavaju kriterijum pretrage. \n")
        #return
    else:
        table = PrettyTable()
        table.field_names = ["Br.", "Naziv filma", "Zanr", "Trajanje", "Reziseri", "Uloge", "Zemlja porekla", "Godina proizvodnje"]

        for i, film in enumerate(results, start = 1):
            table.add_row([
                i,
                film["Naziv"],
                film["Zanr"],
                film["Trajanje"],
                ", ".join(film["Reziseri"]),
                ", ".join(film["Uloge"]),
                film["Zemlja_porekla"],
                film["Godina_proizvodnje"]
            ])
        print(table)
    
    while True:
        inputN = input("[N] Nazad: ").strip()
        if inputN.upper() == "N":
            break
        else:
            print("Pogrešan unos. Molim vas unesite 'N' da biste se vratili nazad.\n")


def add_change_delete_films():
    global lista_filmova
    read_film_file()
    while True:
        print("[1] Dodavanje filmova")
        print("[2] Izmena filmova")
        print("[3] Brisanje filmova")
        print("[N] Nazad")
    #while True:
        choose = input("Izaberite opciju: ").strip().upper()
        if choose == "1":
            add_film()
            while True:
                print("Da li zelite da nastavite sa dodavanjem filmova?")
                print("[D] Da")
                print("[N] Ne")
                inputN = input("Izaberite opciju: ").strip().upper()
                if inputN == "D":
                    add_film()
                elif inputN == "N":
                    break
                else:
                    print("Pogresan unos! Pokusajte ponovo.")
            #pass
        elif choose == "2":
            change_film()
            while True:
                print("Da li zelite da nastavite sa izmenom filmova?")
                print("[D] Da")
                print("[N] Ne")
                inputN = input("Izaberite opciju: ").strip().upper()
                if inputN == "D":
                    change_film()
                elif inputN == "N":
                    break
                else:
                    print("Pogresan unos! Pokusajte ponovo.")


            
        elif choose == "3":
            delete_film()
            while True:
                print("Da li zelite da nastavite sa brisanjem filmova?")
                print("[D] Da")
                print("[N] Ne")
                inputN = input("Izaberite opciju: ").strip().upper()
                if inputN == "D":
                    delete_film()
                elif inputN == "N":
                    break
                else:
                    print("Pogresan unos! Pokusajte ponovo.")
            #overview_of_available_movies()
            #while True:
            #    choose = input("Unesite redni broj filma koji zelite da izbrisete: ").strip().upper()
            #    #if not choose:
            #    #    print("Pogresan unos! Pokusajte ponovo.")
            #    if choose.isdigit():
            #        choose_index = int(choose) - 1
            #        if 0 <= choose_index <= len(lista_filmova):
            #            del lista_filmova[choose_index]#lista_filmova[choose_index]#.remove(choose_index)
            #            with open("film_file.txt", "w") as file:
            #                pass
            #            with open("film_file.txt", "a") as file1:
#
            #                for film in lista_filmova:
            #                    file1.write("{}|{}|{}|{}|{}|{}|{}\n" .format(film["Naziv"], film["Zanr"], film["Trajanje"], (", ").join(film["Reziseri"]), (", ").join(film["Uloge"]), film["Zemlja_porekla"], film["Godina_proizvodnje"]))
            #                break
            #        
            #        else:
            #            print("Broj koji ste uneli nije dat u tabeli! Pokusajte ponovo.")
            #        #for film in lista_filmova:
            #        #    if film == choose:
#
#
            #
            #    elif choose == "N":
            #        break
            #    else:
            #        print("Pogresan unos! Pokusajte ponovo.")
            
        elif choose == "N":
            break
        else:
            print("Pogresan unos! Pokusajte ponovo")

def delete_film():
    global cinema_projection_list
    cinema_projection_append()
    #overview_of_available_movies()
    while True:
        overview_of_available_movies()
        choose = input("Unesite redni broj filma koji zelite da izbrisete ([N] Nazad): ").strip().upper()
        #if not choose:
        #    print("Pogresan unos! Pokusajte ponovo.")
        if choose.isdigit():
            choose_index = int(choose) - 1
            if 0 <= choose_index < len(lista_filmova):
                for projection in cinema_projection_list:
                    if lista_filmova[choose_index]["Naziv"].strip() == projection["Film"]:
                        print("Ne mozete da obrisete zeljeni film jer vec postoji njegova projekcija!\n")
                        while True:
                            inputN = input("[N] Nazad: ").strip()
                            if inputN.upper() == "N":
                                break
                            else:
                                print("Pogresan unos! Pokusajte ponovo.")
                        break
                else:
                    del lista_filmova[choose_index]#lista_filmova[choose_index]#.remove(choose_index)
                    with open("film_file.txt", "w") as file:
                        pass
                    with open("film_file.txt", "a") as file1:
                        for film in lista_filmova:
                            file1.write("{}|{}|{}|{}|{}|{}|{}\n" .format(film["Naziv"], (", ").join(film["Zanr"]), film["Trajanje"], (", ").join(film["Reziseri"]), (", ").join(film["Uloge"]), film["Zemlja_porekla"], film["Godina_proizvodnje"]))
                            #break
                break
            
            else:
                print("Broj koji ste uneli nije dat u tabeli! Pokusajte ponovo.")
            #for film in lista_filmova:
            #    if film == choose:
    
        elif choose == "N":
            break
        else:
            print("Pogresan unos! Pokusajte ponovo.")

def change_film():
    global cinema_projection_list
    cinema_projection_append()
    #overview_of_available_movies()
    while True:
        overview_of_available_movies()
        choose = input("Unesite redni broj filma koji zelite da izmenite ([N] Nazad): ").strip().upper()
        if choose.isdigit():
            choose_index = int(choose) - 1
            if 0 <= choose_index < len(lista_filmova):
                for projection in cinema_projection_list:
                    if lista_filmova[choose_index]["Naziv"].strip() == projection["Film"]:
                        print("Ne mozete da izmenite zeljeni film jer vec postoji njegova projekcija!\n")
                        while True:
                            inputN = input("[N] Nazad: ").strip()
                            if inputN.upper() == "N":
                                break
                            else:
                                print("Pogresan unos! Pokusajte ponovo.")
                        break

                else:
                    while True:
                        print("Sta zelite da izmenite?")
                        print("[1] Zanr")
                        print("[2] Trajanje")
                        print("[3] Reziseri")
                        print("[4] Uloge")
                        print("[5] Zemlja porekla")
                        print("[6] Godina proizvodnje")
                        print("[N] Nazad")
                        choose_option = input("Izaberite opciju: ").strip()
                        if choose_option == "1":
                            while True:
                                choose_genre = input("Unesite zanr: ").strip().split(", ")
                                #if choose_genre.upper() == "N":
                                #    break
                                if choose_genre:
                                    lista_filmova[choose_index]["Zanr"] = choose_genre
                                    change_process()
                                    print("Uspesno ste izmenili zanr.\n")
                                    break
                                #elif choose_genre.upper() == "N":
                                #    break
                                else:
                                    print("Pogresan unos! Pokusajte ponovo.")

                        elif choose_option == "2":
                            while True:
                                choose_during = input("Unesite trajanje: ").strip()
                                if choose_during.isdigit():
                                    lista_filmova[choose_index]["Trajanje"] = choose_during
                                    change_process()
                                    print("Uspesno ste izmenili trajanje filma.\n")
                                    break
                                elif choose_during.upper() == "N":
                                    break
                                else:
                                    print("Pogresan unos! Pokusajte ponovo.")
                        elif choose_option == "3":
                            while True:
                                choose_director = input("Unesite rezisere: ").strip().split(", ")
                                #if choose_director.upper() == "N":
                                #    break
                                if choose_director:
                                    lista_filmova[choose_index]["Reziseri"] = choose_director
                                    change_process()
                                    print("Uspesno ste izmenili rezisere.\n")
                                    break
                                #elif choose_director.upper() == "N":
                                #    break
                                else:
                                    print("Pogresan unos! Pokusajte ponovo.")
                        elif choose_option == "4":
                            while True:
                                choose_actor = input("Unesite uloge: ").strip().split(", ")
                                #if choose_actor.upper() == "N":
                                #    break
                                if choose_actor:
                                    lista_filmova[choose_index]["Uloge"] = choose_actor
                                    change_process()
                                    print("Uspesno ste izmenili uloge.\n")
                                    break
                                #elif choose_actor.upper() == "N":
                                #    break
                                else:
                                    print("Pogresan unos! Pokusajte ponovo.")
                        elif choose_option == "5":
                            while True:
                                choose_country = input("Unesite zemlju porekla: ").strip()
                                #if choose_country.upper() == "N":
                                #    break
                                if choose_country:
                                    lista_filmova[choose_index]["Zemlja_porekla"] = choose_country
                                    change_process()
                                    print("Uspesno ste izmenili zemlju porekla.\n")
                                    break
                                #elif choose_country.upper() == "N":
                                #    break
                                else:
                                    print("Pogresan unos! Pokusajte ponovo.")
                        elif choose_option == "6":
                            while True:
                                #choose_year = input("Unesite godinu dd.mm.yyyy. ([N] Nazad): ").strip()
                                choose_year = year_valid()
                                if choose_year.upper() == "N":
                                    break
                                if choose_year:
                                    lista_filmova[choose_index]["Godina_proizvodnje"] = choose_year
                                    change_process()
                                    print("Uspesno ste izmenili godinu proizvodnje.\n")
                                    break
                                #elif choose_year.upper() == "N":
                                #    break
                                else:
                                    print("Pogresan unos! Pokusajte ponovo.")
                        elif choose_option.upper() == "N":
                            break
                        else:
                            print("Pogresan unos! Pokusajte ponovo.")

            else:
                print("Broj koji ste uneli nije dat u tabeli! Pokusajte ponovo.")
        elif choose == "N":
            break
        else:
            print("Pogresan unos! Pokusajte ponovo.")

def year_valid():
    while True:
        produce_year = input("Unesite godinu proizvodnje 'yyyy'. ([N] Nazad) : ").strip()
        #if not ticket_date:
        #    break
        if len(produce_year) == 4 and produce_year.isdigit():
            #while True:
                #try:
                #    produce_year = datetime.strptime(produce_year, "%d.%m.%Y.").strftime("%d.%m.%Y.")
            return produce_year
                    
                #except ValueError:
                    #print("Pogresan unos! Molimo vas unesite validan datum.")
                    #produce_year = input("Unesite godinu proizvodnje 'yyyy'. ([N] Nazad): ").upper()
                    #if produce_year.upper() == "N":
                    #    return produce_year
        elif produce_year.upper() == "N":
            return produce_year
            #break
        else:
            print("Pogresan unos! Unesite godinu u trazenom formatu.")

def change_process():
    global lista_filmova
    read_film_file()
    with open("film_file.txt", "w") as file:
        pass #(" ")
    with open("film_file.txt", "a") as file1:
        for film in lista_filmova:
            file1.write("{}|{}|{}|{}|{}|{}|{}\n" .format(film["Naziv"], (", ").join(film["Zanr"]), film["Trajanje"], (", ").join(film["Reziseri"]), (", ").join(film["Uloge"]), film["Zemlja_porekla"], film["Godina_proizvodnje"]))

cinema_projection_list = []
cinema_projection_loaded = False
def cinema_projection_append():
    global cinema_projection_loaded
    if not cinema_projection_loaded:
        cinema_projection_read()
        cinema_projection_loaded = True
        return cinema_projection_read()     
    
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
    
    #while True:
    #    print("Da li zelite da nastavite sa brisanjem?")
    #    print("[D] Da")
    #    print("[N] Ne")
    #    inputN = input("Izaberite opciju ([N] Nazad): ").strip().upper()
    #    if inputN == "D":
    #        pass
    #    elif inputN == "N":
    #        break
    #    else:
    #        print("Pogresan unos! Pokusajte ponovo.")

#if __name__ == '__main__':
    #read_film_file()
    #overview_of_available_movies()
#    simple_search()
    #multicriteria_search()
    #add_film()