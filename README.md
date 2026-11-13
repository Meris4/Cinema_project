# 🎬 Cinema Reservation System (CLI Application)

## 📌 Project Information

- **Course:** Introduction to Programming
- **Programming Language:** Python
- **Semester:** 1st
- **Academic Year:** 2023/2024
- **Project Type:** Console-Based Application

---

## 📖 Overview

Cinema Reservation System is a terminal-based application developed in Python that simulates a cinema ticket reservation and management system.

The application supports multiple user roles (Customer, Seller, and Manager), each with different permissions and functionalities. Users interact with the system through a structured, role-based console menu.

The system allows users to browse movies, view projection schedules, check seat availability, reserve and cancel tickets, and manage user accounts.

---

## 👥 User Roles and Permissions

### 🧑 Unregistered Customer
- View available movies.
- Browse projection schedules.
- Check movie information.
- Reserve tickets only through a seller, either by phone or in person.

### 🧑 Registered Customer
- Register and log in to their account.
- Browse movies and available projections.
- Reserve and cancel tickets.
- View current reservations.
- Pay for reserved tickets at the cinema at least 30 minutes before the projection starts.

### 💼 Seller
- Reserve and sell tickets for all customers.
- View and manage existing reservations.
- Edit or cancel reservations.

### 🧑‍💼 Manager
- Register new sellers and managers.
- Access internal system reports.
- Manage administrative operations.

---

## 🔍 Key Features

- 🔐 User registration, login, and logout.
- 🎞️ Movie browsing and projection search.
- 🎟️ Ticket reservation and cancellation.
- 💺 Seat availability checking.
- 👥 Role-based access control and menus.
- 💾 File-based data persistence.
- ✅ Input validation and user feedback.
- 📊 Internal system reports for managers.

---

## 🛠️ Technologies Used

- **Python** – Core programming language.
- **Pickle** – Object serialization and data persistence.
- **File Handling** – Data storage using `.pkl` and `.txt` files.
- **Console UI** – Interactive text-based user interface.

---

## 💾 Data Persistence

The application uses Python's `pickle` module to serialize and deserialize objects, allowing user accounts, movies, projections, reservations, and other system data to be stored locally.

Data is maintained through `.pkl` and `.txt` files, ensuring persistence between application executions.

---

## 🚀 Application Interface

The application runs entirely in the terminal and provides an interactive menu system based on the currently logged-in user's role.

Each user is presented with the operations available according to their permissions.

---

## 🎓 Academic Context

This project was developed as part of the **Introduction to Programming** course during the first semester of the 2023/2024 academic year.

It demonstrates fundamental Python programming concepts, including object-oriented programming, file handling, data serialization, input validation, and role-based application logic.
