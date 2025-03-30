# Vulnerable Blog Website - Docker Project

## 1. Introduction

This report presents the development of a **blog web application** implemented using **Django**, **MariaDB**, and deployed within a **Docker** container. The project aims to demonstrate web application development using modern containerized architectures while providing a controlled environment for security testing.

## 2. Project Objectives

The main objectives of this project are:

- To build a functional **blog platform** using **Django**.
- To set up a **database-driven web application** with **MariaDB**.
- To containerize the application using **Docker** for ease of deployment and scalability.

## 3. System Architecture

The system follows a **three-tier architecture**:

1. **Frontend:** Django templates for rendering HTML pages.
2. **Backend:** Django framework handling requests and processing business logic.
3. **Database Layer:** MariaDB storing user and blog data.

Docker is used to manage the different services in separate containers, ensuring portability and scalability.

## 4. Technologies Used

- **Django** (Web Framework)
- **MariaDB** (Relational Database)
- **Docker** (Containerization)
- **Debian-based system (Python 3.13 image)**

## 5. Implementation Details

### 5.1 Database Design

The database consists of the following tables:

- **accounts_user:** Stores user credentials and profile information.
- **accounts_post:** Stores blog posts with titles, content, timestamps, and authors.
- **accounts_comment:** Stores user comments on blog posts.

### 5.2 Backend Functionality

- **User Authentication:** Login, registration, and password .
- **CRUD Operations:** Users can create, read, update, and delete blog her posts.
- **Comment System:** Registered users can leave comments on posts.

### 5.3 Dockerization

The project is containerized with the following services:

- **Django Application** (`python:3.13` image)
- **MariaDB Database**

### 5.4 Deployment

#### Prerequisites

Ensure **Docker** and **Docker Compose** are installed.
#### Steps to Run the Project

1. Clone the repository:
    
    ```sh
    git clone https://github.com/Mgh-Zakariae/Vulnerable_web_app.git
	cd Vulnerable_web_app
    ```
    
2. Build and run the Docker containers:
    
    ```sh
    docker-compose up --build -d
    ```
    
3. Access the web application at:
    
    ```
    http://localhost:8000
    ```
    

## 6. SQL Injection Vulnerabilities and Prevention

### 6.1 SQL Injection in the Project

This project contains two types of **SQL Injection (SQLi) vulnerabilities**:

1. **Normal SQL Injection:** A vulnerability in user input fields where unescaped SQL queries allow unauthorized data access.
2. **Blind SQL Injection (ORDER BY Exploit):** Exploiting ORDER BY clauses to extract database information indirectly.

Example of a vulnerable SQL query:

```
query = f"SELECT title, content, category FROM accounts_post WHERE id = '{id}'"
conn.execute(query)
```

If a attacker enters ` ' UNION SELECT database() -- -`, the query returns database name.

```
query = f"SELECT * FROM accounts_post WHERE author_id = '{id_user}' ORDER BY {sort_by} DESC"
con.execute(query)
```
> For more information on how they work, go to [exploitation quide](https://github.com/Mgh-Zakariae/Vulnerable_web_app/blob/acd12df4270e2e490743d943c58d159858a57c3d/Exploitation_Guide.md)
### 6.2 Preventing SQL Injection

To prevent SQL Injection, the following best practices should be applied:

- **Use Parameterized Queries:**
    
    ```
    cursor.execute("SELECT * FROM users WHERE username = %s", (user_input,))
    ```
    
- **Utilize Django ORM:** Instead of raw SQL queries, Django’s ORM handles user input safely:
    
    ```
    User.objects.filter(username=user_input)
    ```
    
- **Input Validation & Sanitization:** Ensure input fields accept only expected formats.
- **Use Web Application Firewalls (WAF):** Detect and block SQLi attempts.
- **Limit Database Privileges:** Restrict database permissions to minimize damage from potential attacks.

## 7. Testing and Validation

The application was tested for:

- **Functionality:** Ensuring users can register, log in, and post blogs.
- **Database Integrity:** Verifying that CRUD operations work as expected.
- **Security:** Identifying and mitigating SQLi vulnerabilities.

## 8. Conclusion

This project demonstrates the **development and deployment of a web application** using Django, MariaDB, and Docker. It provides a **scalable**, **modular**, and **secure** architecture for further development and improvements.

