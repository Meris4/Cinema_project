🎬 Cinema Reservation System (CLI App)
Course: Introduction to Programming
Language: Python
Semester: 1st
Academic Year: 2023/2024
Project Type: Console-based application

📌 Overview
This is a terminal-based cinema reservation system built in Python. The system supports multiple user roles (Customer, Seller, Manager) and allows for complete interaction via a role-based console menu.

Users can search movies, reserve seats, view available projections, and manage their accounts — all through a structured and interactive terminal interface.

👥 User Roles & Permissions
🧑‍💻 Unregistered Customer
View movies and projection schedules
Can only reserve tickets through a seller (by phone or in person)
🧑 Registered Customer
Log in and reserve/cancel tickets
View current reservations
Must pay for the ticket at least 30 minutes before the projection by visiting the cinema
💼 Seller
Reserve and sell tickets to all customers
Edit or cancel existing reservations
🧑‍💼 Manager
Register new sellers and managers
Access internal system reports
🔍 Features
🔐 User registration, login, logout
🎞️ Movie and projection search
🎟️ Ticket reservation & cancellation
💺 Seat availability lookup
🧾 Role-based menu system
💾 File-based persistence using Python pickle
✅ Input validation and user feedback
🛠 Technologies Used
Language: Python
Persistence: pickle module for object serialization
Storage: .pkl and .txt files
Interface: Text-based (Console UI)
