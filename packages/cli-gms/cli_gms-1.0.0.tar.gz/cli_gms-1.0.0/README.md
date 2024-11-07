
**GMS (Gym Management System)**
=============================

A Command-Line Interface (CLI) Application for Managing Gym Members and thier Plans


**Overview**
------------

cli-gms is a command-line gym management system (GMS) application. 
It provides a user-friendly interface for managing members, their plans, packages, and payments. 
The application also allows you to view member details, payment history, and plan details. 

The CLI application is built using Python and leverages the Click library for command-line interface functionality. 
It stores data in a MySQL database and uses the Rich library for enhanced user interface experience.


**Features**
------------

* Manage members and packages: add, modify, delete
* Manage member plans: create, renew, remove, make payment
* View member details, payment history, and plan details
* Store data in a MySQL database
* Enhanced user interface experience using Rich library


**Compatibility**
---------------

cli-gms runs on Linux, macOS, and Windows. Spotidex requires Python 3.9.5 or above.


**Installation**
---------------

Install GMS via pipx:

```console
pipx install cli-gms
```

if you dont have pipx installed then install via: 

```console
pip install pipx
```

**Usage**
-----

To use GMS, run the following command:
```
gms <command> [options]
```
**Demo**
-----

https://github.com/user-attachments/assets/91cfdb71-384e-42e0-820e-03dc6344e327

**Available Commands**
--------------------

* `gms view-members`: View gym members
* `gms view-member_plan <member_id>`: View a member's plan
* `gms manage-members`: Manage gym members
	
    + `add`   : Add a new member

    + `modify`: Modify an existing member
    + `delete`: Delete a member
* `gms manage-member-plan <member_id>`: Manage a member's plan
	
    - `create`      : Create a new plan for the member


    - `renew`       : Renew the member's existing plan
    - `remove`      : Remove the member's plan
    - `make payment`: Make a payment for the member's plan
* `gms view-packages`: View packages
* `gms manage-packages`: Manage packages

    - `add`   : Add a new package

    - `modify`: Modify an existing package
    - `delete`: Delete a package
* `gms view-payment-history`: View payment history
* `gms reset_database`: Reset the database


**License**
-------

GMS is licensed under the MIT License.


**Author**
-------

Libin Lalu <libinlalu000@gmail.com>

**Acknowledgments**
----------------

* Click library for command-line interface functionality
* Rich library for enhanced user interface experience
* MySQL database for storing data
* mysql-connector-python library for connecting to MySQL database
* keyring library for storing sensitive data
* questionary library for prompting user input
