from datetime import datetime, timedelta
from prettytable import PrettyTable
from Bioskopske_projekcije import cinema_projection_list, cinema_screening_term_list
from Bioskopske_projekcije import cinema_projection_append, cinema_screening_term_append
from Reports_second import fill_list_append, all_tickets_list, report_date_valid
from Reports_second import fill_all_projections_list_append, all_projections_list, fill_all_term_append, all_terms_list
from Tickets import ticket_date_valid, user_data_append, user_data
from Films import overview_of_available_movies

def reports():
    global all_tickets_list
    #fill_list()
    fill_list_append()

    #global cinema_projection_list
    #global cinema_screening_term_list
    #
    #cinema_projection_append()
    #cinema_screening_term_append()

    global all_projections_list
    global all_terms_list
    fill_all_projections_list_append()
    fill_all_term_append()

    global user_data
    user_data_append()

    while True:
        print("Izvestaji: ")
        print("[A] Lista prodatih karata za odabran datum prodaje")
        print("[B] Lista prodatih karata za odabran datum termina bioskopske projekcije")
        print("[C] Lista prodatih karata za odabran datum prodaje i odabranog prodavca")
        print("[D] Ukupan broj i ukupna cena prodatih karata za izabran dan (u nedelji) prodaje")
        print("[E] Ukupan broj i ukupna cena prodatih karata za izabran dan (u nedelji) održavanja projekcije")
        print("[F] Ukupna cena prodatih karata za zadati film u svim projekcijama")
        print("[G] Ukupan broj i ukupna cena prodatih karata za izabran dan prodaje i odabranog prodavca")
        print("[H] Ukupan broj i ukupna cena prodatih karata po prodavcima (za svakog prodavca) u poslednjih 30 dana.")
    #while True:
        report = input("Izaberite opciju ([N] Nazad): ").strip().upper()
        if report == "A":
            print("Izabrali ste izvestaj A.")
            #report_date = input("Unesite datum: ").strip()
            report_real_date = report_date_valid()
            tableA = PrettyTable()
            tableA.field_names = ["Br", "Oznaka", "Naziv filma", "Datum", "Vreme pocetka", "Vreme kraja", "Sediste"]
            counter = 1
            for all_ticket in all_tickets_list:
                #if ticket["username"] == username:
                try:
                    if datetime.strptime(all_ticket["ticket_all_real_date"].strip(), "%d.%m.%Y.") == datetime.strptime(report_real_date, "%d.%m.%Y."):

                        #projection = next((proj for proj in cinema_projection_list if proj["Password"] == all_ticket["ticket_all_password"][:4]), None)
                        #term = next((term for term in cinema_screening_term_list if term["Term_password"] == all_ticket["ticket_all_password"]), None)
                        projection = next((proj for proj in all_projections_list if proj["Password"] == all_ticket["ticket_all_password"][:4]), None)
                        term = next((term for term in all_terms_list if term["Term_password"] == all_ticket["ticket_all_password"]), None)


                        #if projection and term:
                        tableA.add_row([counter, all_ticket["ticket_all_password"], projection["Film"], term["Date"], projection["Time_start"], projection["Time_end"], all_ticket["ticket_all_seat"]])
                        counter += 1
                except TypeError:
                    print("Nema prodatih karata za datum koji ste uneli.")
            else:
                print("Nema prodatih karata za datum koji ste uneli.")
                    #print("Ne prolazi kroz listu")
            #:
            #    print("Nemate rezervisanih karti.")
            print(tableA)
            if not tableA:
                print("Nemate rezervisanih karti.")
            while True:
                inputN = input("[N] Nazad: ").strip().upper()
                if inputN == "N":
                    break
                else:
                    print("Pogresan unos! Pokusajte ponovo.")
            #break
            #n
            # break
            #for all_ticket in all_tickets_list:
            #    tableA = PrettyTable()
            #    tableA.field_names = [""]
            #break
        elif report == "B":
            print("Izabrali ste izvestaj B.")
            
            report_date = report_date_valid()
            tableB = PrettyTable()
            tableB.field_names = ["Br", "Oznaka", "Naziv filma", "Datum", "Vreme pocetka", "Vreme kraja", "Sediste"]
            counter = 1
            for all_ticket in all_tickets_list:
                #if ticket["username"] == username:
                if datetime.strptime(all_ticket["ticket_all_date"], "%d.%m.%Y.").strftime("%d.%m.%Y.") == datetime.strptime(report_date, "%d.%m.%Y.").strftime("%d.%m.%Y."):
                    
                    #projection = next((proj for proj in cinema_projection_list if proj["Password"] == all_ticket["ticket_all_password"][:4]), None)
                    #term = next((term for term in cinema_screening_term_list if term["Term_password"] == all_ticket["ticket_all_password"]), None)

                    projection = next((proj for proj in all_projections_list if proj["Password"] == all_ticket["ticket_all_password"][:4]), None)
                    term = next((term for term in all_terms_list if term["Term_password"] == all_ticket["ticket_all_password"]), None)

                    #if projection and term:
                    tableB.add_row([counter, all_ticket["ticket_all_password"], projection["Film"], term["Date"], projection["Time_start"], projection["Time_end"], all_ticket["ticket_all_seat"]])
                    counter += 1
                else:
                    pass
                    #print("Ne prolazi kroz listu")
            #:
            #    print("Nemate rezervisanih karti.")
            print(tableB)
            if not tableB:
                print("Nemate rezervisanih karti.")
            while True:
                inputN = input("[N] Nazad: ").strip().upper()
                if inputN == "N":
                    break
                else:
                    print("Pogresan unos! Pokusajte ponovo.")
            #break




        elif report == "C":
            print("Izabrali ste izvestaj C.")
            report_real_date = report_date_valid()
            while True:
                choose_seller = input("Unesite ime prodavca: ").strip()
                if choose_seller:
                    break
                else:
                    print("Pogresan unos! Pokusajte ponovo.")
            tableC = PrettyTable()
            tableC.field_names = ["Br", "Oznaka", "Naziv filma", "Datum", "Vreme pocetka", "Vreme kraja", "Sediste"]
            counter = 1
            for all_ticket in all_tickets_list:
                #if ticket["username"] == username:
                if ((datetime.strptime(all_ticket["ticket_all_real_date"].strip(), "%d.%m.%Y.") == datetime.strptime(report_real_date, "%d.%m.%Y.")) and
                    (choose_seller == all_ticket["ticket_all_seller_username"].strip())
                    ):
                    
                    #projection = next((proj for proj in cinema_projection_list if proj["Password"] == all_ticket["ticket_all_password"][:4]), None)
                    #term = next((term for term in cinema_screening_term_list if term["Term_password"] == all_ticket["ticket_all_password"]), None)
                    projection = next((proj for proj in all_projections_list if proj["Password"] == all_ticket["ticket_all_password"][:4]), None)
                    term = next((term for term in all_terms_list if term["Term_password"] == all_ticket["ticket_all_password"]), None)


                    #if projection and term:
                    tableC.add_row([counter, all_ticket["ticket_all_password"], projection["Film"], term["Date"], projection["Time_start"], projection["Time_end"], all_ticket["ticket_all_seat"]])
                    counter += 1
                else:
                    pass
                    #print("Ne prolazi kroz listu")
            #:
            #    print("Nemate rezervisanih karti.")
            print(tableC)
            if not tableC:
                print("Nemate rezervisanih karti.")
            while True:
                inputN = input("[N] Nazad: ").strip().upper()
                if inputN == "N":
                    break
                else:
                    print("Pogresan unos! Pokusajte ponovo.")
            #break
            
        elif report == "D":
            print("Izabrali ste izvestaj D.")
            #report_real_date = report_date_valid()
            while True:
                print("Dani u nedelji: ")
                print("[0] Ponedeljak ")
                print("[1] Utorak ")
                print("[2] Sreda ")
                print("[3] Cetvrtak ")
                print("[4] Petak ")
                print("[5] Subota ")
                print("[6] Nedelja ")
                print("[N] Nazad")
                choose_day = input("Izaberite dan: ").strip()
                if choose_day in ["0", "1", "2", "3", "4", "5", "6"]:
                    tableD = PrettyTable()
                    tableD.field_names = ["Br", "Ukupna cena"]
                    total_price = 0
                    counter = 0
                    for all_ticket in all_tickets_list:
                        #if ticket["username"] == username:
                        #print(datetime.strptime(all_ticket["ticket_all_real_date"].strip(), "%d.%m.%Y.").weekday())
                        if ((datetime.strptime(all_ticket["ticket_all_real_date"].strip(), "%d.%m.%Y.").weekday() == int(choose_day))# and
                            #(choose_seller == all_ticket["ticket_all_seller_username"].strip())
                            ):
                            #projection = next((proj for proj in all_projections_list if proj["Password"] == all_ticket["ticket_all_password"][:4]), None)
                            #total_price += float(projection["Price"])
                            total_price += float(all_ticket["ticket_all_card_price"])
                            counter += 1
                            
                    tableD.add_row([counter, total_price])
                    #else:
                    #    pass
                        #print("Nemate rezervisanih karti.")
                    print(tableD)
                    if not tableD:
                        print("Nemate rezervisanih karti.")
                    while True:
                        inputN = input("[N] Nazad: ").strip().upper()
                        if inputN == "N":
                            break
                        else:
                            print("Pogresan unos! Pokusajte ponovo.")
                    #else:
                    #    pass
                    #break
                elif choose_day.upper() == "N":
                    break
                else:
                    print("Pogresan unos! Pokusajte ponovo.")
#            tableD = PrettyTable()
#            tableD.field_names = ["Br", "Ukupna cena"]
#            total_price = 0
#            counter = 0
#            for all_ticket in all_tickets_list:
#                #if ticket["username"] == username:
#                #print(datetime.strptime(all_ticket["ticket_all_real_date"].strip(), "%d.%m.%Y.").weekday())
#                if ((datetime.strptime(all_ticket["ticket_all_real_date"].strip(), "%d.%m.%Y.").weekday() == int(choose_day))# and
#                    #(choose_seller == all_ticket["ticket_all_seller_username"].strip())
#                    ):
#                    #projection = next((proj for proj in all_projections_list if proj["Password"] == all_ticket["ticket_all_password"][:4]), None)
#                    #total_price += float(projection["Price"])
#                    total_price += float(all_ticket["ticket_all_card_price"])
#
#
#                    counter += 1
#                else:
#                    pass
#                    #print("Ne prolazi kroz listu")
#            #:
#            #    print("Nemate rezervisanih karti.")
#            tableD.add_row([counter, total_price])
#            print(tableD)
#            if not tableD:
#                print("Nemate rezervisanih karti.")
#            while True:
#                inputN = input("[N] Nazad: ").strip().upper()
#                if inputN == "N":
#                    break
#                else:
#                    print("Pogresan unos! Pokusajte ponovo.")
            #break
            
        elif report == "E":
            print("Izabrali ste izvestaj E.")
            while True:
                print("Dani u nedelji: ")
                print("[0] Ponedeljak ")
                print("[1] Utorak ")
                print("[2] Sreda ")
                print("[3] Cetvrtak ")
                print("[4] Petak ")
                print("[5] Subota ")
                print("[6] Nedelja ")
                print("[N] Nazad")
                choose_day = input("Izaberite dan: ").strip()
                if choose_day in ["0", "1", "2", "3", "4", "5", "6"]:
                    tableE = PrettyTable()
                    tableE.field_names = ["Br", "Ukupna cena"]
                    total_price = 0
                    counter = 0
                    for all_ticket in all_tickets_list:
                        #if ticket["username"] == username:
                        #print(datetime.strptime(all_ticket["ticket_all_real_date"].strip(), "%d.%m.%Y.").weekday())
                        if ((datetime.strptime(all_ticket["ticket_all_date"].strip(), "%d.%m.%Y.").weekday() == int(choose_day))# and
                            #(choose_seller == all_ticket["ticket_all_seller_username"].strip())
                            ):
                            #projection = next((proj for proj in all_projections_list if proj["Password"] == all_ticket["ticket_all_password"][:4]), None)
                            #total_price += float(projection["Price"])
                            total_price += float(all_ticket["ticket_all_card_price"])


                            #if projection and term:
                            #tableD.add_row([counter, total_price])
                            counter += 1
                    tableE.add_row([counter, total_price])
                    print(tableE)
                    if not tableE:
                        print("Nemate rezervisanih karti.")
                    while True:
                        inputN = input("[N] Nazad: ").strip().upper()
                        if inputN == "N":
                            break
                        else:
                            print("Pogresan unos! Pokusajte ponovo.")

                elif choose_day.upper() == "N":
                    break            
                else:
                    print("Pogresan unos! Pokusajte ponovo.")
            


        elif report == "F":
            print("Izabrali ste izvestaj F.")
            while True:
                overview_of_available_movies()
                choose_film = input("Unesite ime filma: ").strip()
                if choose_film:
                    break
                else:
                    print("Pogresan unos! Pokusajte ponovo.")
            tableF = PrettyTable()
            tableF.field_names = ["Ukupna cena"]
            total_price = 0
            #counter = 0
            for projection in all_projections_list:
                #if ticket["username"] == username:
                #print(datetime.strptime(all_ticket["ticket_all_real_date"].strip(), "%d.%m.%Y.").weekday())
                if projection["Film"].strip() == choose_film:
                    for all_ticket in all_tickets_list:
                        if projection["Password"] == all_ticket["ticket_all_password"][:4] and all_ticket["ticket_all_condition"].strip() == "K":
                     # and
                    #for all_ticket in all_tickets_list:
                    #    if 
                    
                    #projection = next((proj for proj in all_projections_list if proj["Password"] == all_ticket["ticket_all_password"][:4]), None)
                            #total_price += float(projection["Price"])
                            total_price += float(all_ticket["ticket_all_card_price"])

                    #counter += 1
                else:
                    pass
                    #print("Ne prolazi kroz listu")
            #:
            #    print("Nemate rezervisanih karti.")
            tableF.add_row([total_price])
            print(tableF)
            if not tableF:
                print("Nemate rezervisanih karti.")
            while True:
                inputN = input("[N] Nazad: ").strip().upper()
                if inputN == "N":
                    break
                else:
                    print("Pogresan unos! Pokusajte ponovo.")
            #break
        elif report == "G":
            print("Izabrali ste izvestaj G.")
            #report_real_date = report_date_valid()
            while True:
                print("Dani u nedelji: ")
                print("[0] Ponedeljak ")
                print("[1] Utorak ")
                print("[2] Sreda ")
                print("[3] Cetvrtak ")
                print("[4] Petak ")
                print("[5] Subota ")
                print("[6] Nedelja ")
                print("[N] Nazad")
                choose_day = input("Izaberite dan: ").strip()
                if choose_day in ["0", "1", "2", "3", "4", "5", "6"]:

                    while True:
                        overview_of_sellers()
                        choose_seller = input("Unesite username prodavca: ").strip()
                        if choose_seller:
                            tableG = PrettyTable()
                            tableG.field_names = ["Br", "Ukupna cena"]
                            total_price = 0
                            counter = 0
                            for all_ticket in all_tickets_list:
                                #if ticket["username"] == username:
                                if ((datetime.strptime(all_ticket["ticket_all_real_date"].strip(), "%d.%m.%Y.").weekday() == int(choose_day)) and
                                    (choose_seller == all_ticket["ticket_all_seller_username"].strip()) and
                                    (all_ticket["ticket_all_condition"].strip() == "K")
                                    ):

                                    #projection = next((proj for proj in all_projections_list if proj["Password"] == all_ticket["ticket_all_password"][:4]), None)

                                    #total_price += float(projection["Price"])
                                    total_price += float(all_ticket["ticket_all_card_price"])

                                    #if projection and term:
                                    #tableG.add_row([counter, total_price])
                                    counter += 1
                            tableG.add_row([counter, total_price])
                            print(tableG)
                            if not tableG:
                                print("Nemate rezervisanih karti.")
                            while True:
                                inputN = input("[N] Nazad: ").strip().upper()
                                if inputN == "N":
                                    break
                                else:
                                    print("Pogresan unos! Pokusajte ponovo.")
                            break
                        else:
                            print("Pogresan unos! Pokusajte ponovo.")
                        #tableG = PrettyTable()
                        #tableG.field_names = ["Br", "Ukupna cena"]
                        #total_price = 0
                        #counter = 0
                        #for all_ticket in all_tickets_list:
                        #    #if ticket["username"] == username:
                        #    if ((datetime.strptime(all_ticket["ticket_all_real_date"].strip(), "%d.%m.%Y.").weekday() == int(choose_day)) and
                        #        (choose_seller == all_ticket["ticket_all_seller_username"].strip()) and
                        #        (all_ticket["ticket_all_condition"].strip() == "K")
                        #        ):
#
                        #        #projection = next((proj for proj in all_projections_list if proj["Password"] == all_ticket["ticket_all_password"][:4]), None)
#
                        #        #total_price += float(projection["Price"])
                        #        total_price += float(all_ticket["ticket_all_card_price"])
#
                        #        #if projection and term:
                        #        #tableG.add_row([counter, total_price])
                        #        counter += 1
                        #    else:
                        #        pass
                        #tableG.add_row([counter, total_price])
                        #print(tableG)
                        #if not tableG:
                        #    print("Nemate rezervisanih karti.")
                        #while True:
                        #    inputN = input("[N] Nazad: ").strip().upper()
                        #    if inputN == "N":
                        #        break
                        #    else:
                        #        print("Pogresan unos! Pokusajte ponovo.")
                elif choose_day.upper() == "N":
                    break
                else:
                    print("Pogresan unos! Pokusajte ponovo.")
            #while True:
            #    choose_seller = input("Unesite username prodavca: ").strip()
            #    if choose_seller:
            #        break
            #    else:
            #        print("Pogresan unos! Pokusajte ponovo.")
            #tableG = PrettyTable()
            #tableG.field_names = ["Br", "Ukupna cena"]
            #total_price = 0
            #counter = 0
            #for all_ticket in all_tickets_list:
            #    #if ticket["username"] == username:
            #    if ((datetime.strptime(all_ticket["ticket_all_real_date"].strip(), "%d.%m.%Y.").weekday() == int(choose_day)) and
            #        (choose_seller == all_ticket["ticket_all_seller_username"].strip()) and
            #        (all_ticket["ticket_all_condition"].strip() == "K")
            #        ):
            #        
            #        #projection = next((proj for proj in all_projections_list if proj["Password"] == all_ticket["ticket_all_password"][:4]), None)
#
            #        #total_price += float(projection["Price"])
            #        total_price += float(all_ticket["ticket_all_card_price"])
#
            #        #if projection and term:
            #        #tableG.add_row([counter, total_price])
            #        counter += 1
            #    else:
            #        pass
            #        #print("Ne prolazi kroz listu")
            #:
            #    print("Nemate rezervisanih karti.")
            #tableG.add_row([counter, total_price])
            #print(tableG)
            #if not tableG:
            #    print("Nemate rezervisanih karti.")
            #while True:
            #    inputN = input("[N] Nazad: ").strip().upper()
            #    if inputN == "N":
            #        break
            #    else:
            #        print("Pogresan unos! Pokusajte ponovo.")
            #break
        elif report == "H":
            print("Izabrali ste izvestaj H.")
            tableH = PrettyTable()
            tableH.field_names = ["Ime prodavca", "Broj prodatih karata", "Ukupna cena"]
            #total_price = 0
            #counter = 0
            #last_30_days = datetime.now() - 30 days
            current_time = datetime.now()
            last_30_days = current_time - timedelta(days=30)

            for user in user_data:
                total_price = 0
                counter = 0
                if user[4].strip() == "prodavac":
                    #total_price = 0
                    #counter = 0
                    for all_ticket in all_tickets_list:
                        if ((all_ticket["ticket_all_seller_username"].strip() == user[0].strip()) and 
                            (all_ticket["ticket_all_condition"].strip() == "K") and
                            (datetime.strptime(all_ticket["ticket_all_real_date"], "%d.%m.%Y.") >= last_30_days)
                            ):

                            #projection = next((proj for proj in all_projections_list if proj["Password"] == all_ticket["ticket_all_password"][:4]), None)
                            #total_price += float(projection["Price"])
                            total_price += float(all_ticket["ticket_all_card_price"])

                            #tableH.add_row([counter, total_price])
                            counter += 1
                    name_and_surname = user[2] + " " + user[3]
                    tableH.add_row([name_and_surname, counter, total_price])
            if tableH:                
                print(tableH)
            else:
                print("Nema dostupnih informacija.")
            while True:
                inputN = input("[N] Nazad: ").strip().upper()
                if inputN == "N":
                    break
                else:
                    print("Pogresan unos! Pokusajte ponovo.")
            #break

                    
            #break
        elif report == "N":
            break
        else:
            print("Pogresan unos! Molimo vas pokusajte ponovo.")

user_data1 = []
def read_user_data1():
    global user_data1
    with open("users.txt", "r") as file1:
        lines = file1.readlines()
        for line in lines:
            user_data1.append(line.strip().split("|"))
        return user_data1
    
user_data_loaded1 = False
def user_data_append1():
    global user_data1
    global user_data_loaded1

    if user_data_loaded1 == False:
        user_data1 = read_user_data1()
        user_data_loaded1 = True
    return user_data1

def overview_of_sellers():
    global user_data1
    user_data_append1()
    table = PrettyTable()
    table.field_names = ["Br.", "Username prodavca"]
    counter = 1
    for user1 in user_data1:
        if user1[4].strip() == "prodavac":
            table.add_row([counter, user1[0]])
            counter += 1
    if table:
        print(table)
    else:
        print("Nema prodavaca.")




def loyalty_card_discounts():
    global all_tickets_list
    #fill_list()
    fill_list_append()
    





#all_tickets_list = []
#def fill_list():
#    global all_tickets_list
#    with open("tickets.txt", "r") as file:
#        lines = file.readlines()
#        for line in lines:
#            apart_line = line.split("|")
#            ticket_all = {
#                "ticket_all_password": apart_line[0],
#                "ticket_all_date": apart_line[1],
#                "ticket_all_seat": apart_line[2],
#                "ticket_all_username": apart_line[3],
#                "ticket_all_condition": apart_line[4]
#            }
#            all_tickets_list.append(ticket_all)
#
#fill_list_read = False
#def fill_list_append():
#    global fill_list_read
#    if fill_list_read == False:
#       fill_list()
#       fill_list_read = True
