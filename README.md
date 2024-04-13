# Library DRF Project

This project aims to create a web application using Django REST Framework (DRF) for managing library operations. It provides users with the ability to reserve and pay for books online, offering a convenient way to access library resources remotely.

---

## Features

- **User Authentication**: 
  The project includes user authentication functionality to allow users to create accounts, log in, and manage their profiles.

- **Book Reservation**: 
  Users can browse the library's collection, select books they wish to borrow, and reserve them for a specific period.

- **Payment Integration**: 
  Integration with payment gateways enables users to pay for reserved books securely online.

- **Book Management**: 
  Librarians or administrators have the ability to add, update, and delete books from the library's collection.

- **User Profiles**: 
  Users can view their borrowing history, manage their reservations, and update their profile information.

-------------------------------------------------------------------------------------

## Installation using GitHub
 
For beginning you have to install Python3+, PostgresSQL and create db
 
**In terminal write down following command:**

```shell

git clone https://github.com/shaiduchyk/library-group-project.git
python -m venv venv

* MacOS *
source venv/bin/activate
* Windows *
venv/scripts/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
 
```
## Run with docker
 
Docker should be installed
```shell
docker-compose build
docker-compose up
 
```

-------------------------------------------------------------------------------------

## API Reference

#### Before start using this API Project, u should use register(if not yet) or use JWT Token for authentication if u already register.

#### For register:

```http
  POST api/user/register/
```

| Key | Type     | Description                |
| :-------- | :------- | :------------------------- |
| Email | Email | **Required**. Your Email |
| Password | Password | **Required**. Your Password |

#### For authentication (you should use your credentials for authentication)

```http
  GET api/user/token/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| Email    | Email | **Required**. Your Email |
| Password    | Password | **Required**. Your Password |

### You can see information about your account inc. email, are you staff etc. (update account info as well)


```http
  GET api/user/me/
```

------------------------------------------------------------------------------------

## RESOURCES

Note: You can get further resources if you are authenticated (**ex. Book List page**)
 
#### Get list of Books and create new one (if you have admin permissions)

```http
   GET /api/books/
```

#### Create a new book (You need admin permissions) 

```http
   POST /api/books/ 
```

#### Get detail info about book

```http
   GET, PATCH, PUT, DELETE /api/books/<int:pk>/
```
---------------------------------------------------------------------------------------
#### Get list of your borrowings (You can see all ones if you have admin permissions)

```http
   GET /api/borrowings/
```

#### Create a new borrow (only for authenticated user)

```http
   POST /api/borrowings/
```

#### Get detail info about your borrow (only for authenticated user)

```http
   GET /api/borrowings/<int:pk>/
```

#### Return your borrow 

```http
   POST /api/borrowings/<int:pk>/return-borrowing/
```
---------------------------------------------------------------------------------------

#### Get list of Payments (You can see all ones if you have admin permissions)

```http
   GET /api/payments/
```
#### Get info about your payment (if you already have one, and it is success)

```http
   GET /api/payments/<int:pk>/success/
```

#### Get info about your payment (if you already have one, and it is failed)

```http
   GET /api/payments/<int:pk>/cancel/
```
---------------------------------------------------------------------------------------

#### Get SWAGGER schema about this API

```http
   GET /api/doc/swagger-ui/
```

#### Get SWAGGER schema about this API (another version)

```http
   GET /api/doc/redoc/
```

#### Download SWAGGER schema

```http
   GET /api/doc/schema/
```

----------------------------------------------------------------------------------
## Admin Panel

#### You can join admin panel through this endpoint:

```http
GET /admin
```
*Example*: http://127.0.0.1:8000/admin/

#### Information about superuser:


| *Parameter* | *Type*           | 
| :-------- |:-----------------|
| **Nickname**   | krixn2@gmail.com |
| **Password**    | gsi579738059     |
----------------------------------------------------------------------------------
