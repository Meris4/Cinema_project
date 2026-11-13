from datetime import datetime

all_tickets_list = []
def fill_list():
    global all_tickets_list
    with open("reserved_tickets.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            apart_line = line.split("|")
            ticket_all = {
                "ticket_all_password": apart_line[0],
                "ticket_all_date": apart_line[1],
                "ticket_all_seat": apart_line[2],
                "ticket_all_username": apart_line[3],
                "ticket_all_condition": apart_line[4],
                "ticket_all_real_date": apart_line[5],
                "ticket_all_seller_username": apart_line[6].strip(),
                "ticket_all_card_price": apart_line[7].strip()
            }
            all_tickets_list.append(ticket_all)

fill_list_read = False
def fill_list_append():
    global fill_list_read
    if fill_list_read == False:
       fill_list()
       fill_list_read = True
 
def report_date_valid():
    while True:
        ticket_date = input("Unesite datum karte (dd.mm.yyyy.): ").strip()
        #if not ticket_date:
        #    break
        if len(ticket_date) == 11 and ticket_date[:2].isdigit() and ticket_date[2] == "." and ticket_date[3:5].isdigit() and ticket_date[5] == "." and ticket_date[6:10].isdigit() and ticket_date[10] == ".":
            while True:
                try:
                    ticket_date = datetime.strptime(ticket_date, "%d.%m.%Y.").strftime("%d.%m.%Y.")
                    return ticket_date
                    
                except ValueError:
                    print("Pogresan unos! Molimo vas unesite validan datum.")
                    ticket_date = input("Unesite datum karte (dd.mm.yyyy.): ").upper()
        else:
            print("Pogresan unos! Unesite datum u trazenom formatu.")

all_projections_list = []
def fill_projections_list():
    global all_projections_list
    with open("cinema_projections.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            apart_line = line.split("|")
            projection = {
                "Password": apart_line[0],
                "Hall": apart_line[1],
                "Time_start": apart_line[2],
                "Time_end": apart_line[3],
                "Day": apart_line[4],
                "Film": apart_line[5],
                "Price": apart_line[6].strip()
            }
            all_projections_list.append(projection)

all_projections_list_read = False
def fill_all_projections_list_append():
    global all_projections_list_read
    if all_projections_list_read == False:
       fill_projections_list()
       all_projections_list_read = True

all_terms_list = []
def fill_terms_list():
    global all_terms_list
    with open("projection_term.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            apart_line = line.split("|")
            projection_term = {
                "Term_password": apart_line[0],
                "Date": apart_line[1].strip(),
                "Valid": apart_line[2].strip()
            }
            all_terms_list.append(projection_term)

all_terms_list_read = False
def fill_all_term_append():
    global all_terms_list_read
    if all_terms_list_read == False:
        fill_terms_list()
        all_terms_list_read = True