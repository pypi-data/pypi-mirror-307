import click

from rich.table import Table
from rich.console import Console
from rich.panel import Panel

import questionary as qt
from prompt_toolkit import prompt

from dateutil.relativedelta import relativedelta

from .database import Database
from .utils import *

database = Database()
console = Console()


@click.group()
def gms(): ...
@gms.command()
def view_members():
    """
    Displays a list of all members along with their details in a tabular format.

    The table includes the following columns: Serial Number, Member Name, Gender,
    Date of Birth, Phone, and Status. The data is retrieved from the database.
    """
    print()
    headers = ["S.No", "Member Name", "Gender", "Date of Birth", "Phone", "Status"]
    members_table = Table(*headers, title="Members")
    for member in database.retrive_members():
        member_details = [str(i) for i in member.values()]
        members_table.add_row(
            *member_details[0:3],
            "-".join(member_details[3].split("-")[::-1]),
            *member_details[4:],
        )
    console.print(members_table)


def add_member(n):
    panel = Panel("", expand=False, title=f"Member Details [{n}]")
    print(f"Member Details[{n}]")
    name = prompt("Enter Member Name: ", validator=NameValidator("member")).title()
    clear_display(2)
    panel.renderable += "\nMember Name   : " + name.title()
    console.print(panel)

    gender = qt.select(
        "Gender", qmark="", choices=["Male", "Female", "Others"]
    ).ask()
    panel.renderable += "\nGender        : " + gender
    clear_display(5)
    console.print(panel)

    dob = prompt("Enter Date of Birth [dd-mm-yy]: ", validator=DateValidator("dob"))
    panel.renderable += "\nDate of Birth : " + dob
    dob = "-".join(dob.split("-")[::-1])
    clear_display(6)
    console.print(panel)

    phone = prompt("Enter Phone Number: ", validator=PhoneValidator())
    panel.renderable += "\nPhone Number  : " + phone
    clear_display(7)
    console.print(panel)

    return name, gender, dob, phone


@gms.command()
def manage_members():
    """
    Provides options to manage members in the gym management system.

    Options:

    1. Add Members   - Adds new members to the system.
    2. Modify Member - Modifies existing member details.
    3. Delete Member - Deletes existing members from the system.
    """
    menu_choices = ["Add Members", "Modify Member", "Delete Member", "Exit"]
    menu = qt.select(
        "Manage Members",
        qmark="",
        choices=menu_choices,
    ).ask()
    clear_display(1)
    print("Option Choose : " + menu)
    if menu == "Add Members":
        i = 1
        total_members = int(
            prompt("Enter number of members to add:", validator=NumberValidator())
        )
        clear_display(1)
        print("Members To Add: " + str(total_members), "\n")
        while i <= total_members:
            member_details = add_member(i)
            if qt.confirm("Are you sure you want to add this member?").ask():
                database.add_member(*member_details)
                clear_display(1)

            else:
                clear_display(8)
                continue
            i += 1
            print()

    elif menu == "Modify Member":
        member_id = int(prompt("Enter Member ID: ", validator=IDValidator("member")))
        clear_display(1)
        print(f"Member ID     : {member_id}", "\n")
        _, name, gender, dob, phone, _ = [
            member.values()
            for member in database.retrive_members()
            if member["member_id"] == member_id
        ][0]
        dob = dob.strftime("%d-%m-%Y")
        initial_name = name
        template = "\nMember Name   :{} \nGender        :{} \nDate of Birth :{} \nPhone Number  :{} "
        panel = Panel(
            template.format(name.title(), gender, dob, phone),
            expand=False,
            title="Member Details",
        )
        console.print(panel)

        name = prompt(
            "Enter Member Name: ",
            validator=NameValidator("member", initial_name),
            default=name,
        )
        clear_display(8)
        panel.renderable = template.format(name.title(), gender, dob, phone)
        console.print(panel)

        gender = qt.select(
            "Gender", qmark="", choices=["Male", "Female", "Others"]
        ).ask()
        clear_display(8)
        panel.renderable = template.format(name.title(), gender, dob, phone)
        console.print(panel)

        dob = prompt(
            "Enter Date of Birth [dd-mm-yy] : ",
            validator=DateValidator("dob"),
            default=dob,
        )
        clear_display(8)
        panel.renderable = template.format(name.title(), gender, dob, phone)
        console.print(panel)

        phone = prompt(
            "Enter Phone Number: ", validator=PhoneValidator(), default=phone
        )
        clear_display(8)
        panel.renderable = template.format(name.title(), gender, dob, phone)
        console.print(panel)
        if qt.confirm("Are you sure you want to modify this member?").ask():
            dob = "-".join(dob.split("-")[::-1])
            database.modify_member(initial_name, name, gender, dob, phone)

    elif menu == "Delete Member":
        print()
        member_list = qt.checkbox(
            "Select Members To Delete",
            choices=[
                f"{member['member_id']}. {member['member_name']}"
                for member in database.retrive_members()
            ],
        ).ask()
        clear_display(1)
        panel = Panel(
            "\n".join(member_list), expand=False, title=f"{len(member_list)} Selections"
        )
        console.print(panel)
        if qt.confirm("Are you sure").ask():
            for member in member_list:
                database.delete_member(member)

    elif menu == "Exit":
        return


@gms.command()
@click.argument("member_id")
def view_member_plan(member_id):
    """
    Displays the plan details of a specific member.

    Retrieves the member's plan information from the database using their ID,
    and displays it in a formatted table. If the member ID is invalid, an error
    message is printed.

    Args:
        member_id : The ID of the member whose plan details are to be viewed.
    """
    member_plan = database.retrive_member_plan(member_id)
    try:
        member_name = [
            member["member_name"]
            for member in database.retrive_members()
            if member["member_id"] == int(member_id)
        ][0]
    except:
        print("Invalid Member ID")
        return
    table = get_member_plan_table(member_id, member_name, *member_plan.values())
    print()
    console.print(table)


@gms.command()
def manage_packages():
    """
    Manages the packages available in the gym.

    Options:
    1. Add Package    - Adds a new package to the system with details such as name, duration, amount, and training type.
    2. Modify Package - Modifies existing package details. Requires package ID and allows modification of name, duration, amount, and training type.
    3. Delete Package - Deletes selected packages from the system.

    The user is prompted to select an option and provide necessary inputs for the chosen action.
    """
    menu_choices = ["Add Package", "Modify Package", "Delete Package", "Exit"]
    menu = qt.select(
        "Manage Members",
        qmark="",
        choices=menu_choices,
    ).ask()

    clear_display(1)
    print("Option Choose : " + menu)
    if menu == "Add Package":
        panel = Panel("", expand=False)

        package_name = prompt(
            "\nEnter Package Name: ", validator=NameValidator("package")
        ).title()
        clear_display(2)
        panel.renderable += "Package Name     : " + package_name
        console.print(panel)

        package_duration = int(
            prompt("Enter Package Duration [in months] : ", validator=DigitValidator())
        )

        clear_display(4)
        panel.renderable += "\nPackage Duration : " + str(package_duration) + " months"
        console.print(panel)

        package_amount = int(
            prompt("Enter Package Amount: ", validator=PaymentAmountValidator(None))
        )
        clear_display(5)
        panel.renderable += "\nPackage Amount   : " + str(package_amount)
        console.print(panel)

        package_training_type = qt.select(
            "Training Type",
            qmark="",
            choices=["General", "Personal"],
        ).ask()
        clear_display(6)
        panel.renderable += "\nTraining Type    : " + package_training_type
        console.print(panel)

        if qt.confirm("Are you sure you want to add this package?").ask():
            database.create_package(
                package_name, package_duration, package_amount, package_training_type
            )

        else:
            clear_display(8)
    elif menu == "Modify Package":
        package_id = prompt("Enter Package ID: ", validator=IDValidator("package"))
        clear_display(1)
        print("Package ID    : " + package_id, "\n")
        _, name, duration, amount, training_type = [
            package.values()
            for package in database.retrive_packages()
            if package["package_id"] == int(package_id)
        ][0]
        initial_name = name
        amount = str(amount)
        duration = str(duration)
        template = "\nPackage Name     :{} \nPackage Duration :{} \nPackage Amount   :{} \nTraining Type    :{} "
        panel = Panel(
            template.format(name, duration, amount, training_type),
            expand=False,
            title="Package Details",
        )
        console.print(panel)

        name = prompt(
            "Enter Package Name: ",
            validator=NameValidator("package", initial_name),
            default=initial_name,
        ).title()
        clear_display(8)
        panel.renderable = template.format(name, duration, amount, training_type)
        console.print(panel)

        duration = int(
            prompt(
                "Enter Package Duration [in months] : ",
                default=duration,
                validator=DigitValidator(),
            )
        )
        clear_display(8)
        panel.renderable = template.format(name, duration, amount, training_type)
        console.print(panel)

        amount = int(
            prompt(
                "Enter Package Amount: ",
                default=amount,
                validator=PaymentAmountValidator(None),
            )
        )
        clear_display(8)
        panel.renderable = template.format(name, duration, amount, training_type)
        console.print(panel)

        training_type = qt.select(
            "Enter Training Type", qmark="", choices=["General", "Personal"]
        ).ask()
        clear_display(8)
        panel.renderable = template.format(name, duration, amount, training_type)
        console.print(panel)
        if qt.confirm("Are you sure you want to modify this package?").ask():
            database.modify_package(initial_name, name, duration, amount, training_type)

    elif menu == "Delete Package":
        print()
        packages = qt.checkbox(
            "Select Packages To Delete",
            choices=[
                f"{package['package_id']}. {package['package_name']}"
                for package in database.retrive_packages()
            ],
        ).ask()
        clear_display(1)
        panel = Panel(
            "\n".join(packages), expand=False, title=f"{len(packages)} Selections"
        )
        console.print(panel)
        if qt.confirm("Are you sure").ask():
            for package_name in packages:
                database.delete_package(package_name)

    elif menu == "Exit":
        return


@gms.command()
def view_packages():
    """
    Displays a list of all packages in the gym.

    Retrieves the package details from the database and displays them in a
    formatted table. The table includes the following columns: Serial Number,
    Package Name, Duration, Amount, and Training Type.
    """
    print()
    headers = [
        "S.No",
        "Package Name",
        "Duration [in months]",
        "Amount",
        "Training Type",
    ]
    packages_table = Table(
        *headers,
        title="Packages",
    )
    for package in database.retrive_packages():
        packages_table.add_row(*[str(i) for i in package.values()])
    console.print(packages_table)


@gms.command()
def view_payment_history():
    """
    Displays the payment history of all members in the gym management system.

    Retrieves the payment details from the database and displays them in a
    formatted table. The table includes the following columns: Member Name,
    Package Name, Payment Amount, Payment Date, and Payment Mode.
    """
    print()
    headers = [
        "Member Name",
        "Package Name",
        "Payment Amount",
        "Payment Date",
        "Payment Mode",
    ]
    payment_table = Table(
        *headers,
        title="Payment History",
    )
    for payment in database.retrive_payment_history():
        payment_table.add_row(*[str(i) for i in payment.values()])
    console.print(payment_table)


@gms.command()
def reset_database():
    """
    Resets the entire database.

    This will delete all data in the database. Only use this if you want to
    start fresh or if you are having some issues with your database.

    """
    if qt.confirm("Are you sure you want to reset database ?").ask():
        database.reset_database()


@gms.command()
@click.argument("member_id")
def manage_member_plan(member_id):
    """
    Manages the plan of a member in the gym.

    Allows the user to create a new plan, renew an existing plan, remove an existing
    plan, or make a payment for the plan.

    Args:
        member_id : The ID of the member for whom the plan needs to be managed.
    """
    member_plan = database.retrive_member_plan(member_id)
    try:
        member_name = [
            member["member_name"]
            for member in database.retrive_members()
            if member["member_id"] == int(member_id)
        ][0]
    except:
        print("Invalid Member ID")
        return
    menu_choices = ["Exit"]

    if (
        list(member_plan["current_member_plan"].values())
        == list(member_plan["expired_member_plan"].values())
        == [None, None, None, None]
    ):
        menu_choices.append("Create Plan")
    elif list(member_plan["current_member_plan"].values()) != [None, None, None, None]:
        menu_choices.append("Remove Plan")
        if member_plan["amount_pending"] in [0, None]:
            menu_choices.append("Renew Plan")
    if member_plan["amount_pending"] not in [0, None]:
        menu_choices.append("Make Payment")

    menu = qt.select("Manage Member Plan", qmark="", choices=menu_choices).ask()

    clear_display(1)
    print("Option Choose : " + menu)

    if menu == "Create Plan":
        package_names = []
        for p in database.retrive_packages():
            values = [
                p["package_name"],
                p["total_amount"],
                p["duration"],
                p["training_type"],
            ]
            package_names.append(
                "{} [{} for {} months] with training type {}".format(*values)
            )
        if package_names == []:
            print("No Packages Available, Please create a package first")
            return
        package_selection = qt.select(
            "Select A Package", qmark="", choices=package_names
        ).ask()
        for package in database.retrive_packages():
            if package["package_name"] in package_selection:
                package_selected = package

        clear_display(1)
        print("\nPackage Selected : " + package_selected["package_name"], "\n")

        start_date = prompt(
            "Enter Start Date [dd-mm-yy] : ",
            validator=DateValidator("start_date"),
            default=datetime.today().strftime("%d-%m-%Y"),
        )
        clear_display(2)
        print("Plan Start Date  : " + start_date, "\n")

        final_offer = int(
            prompt("Enter Final Offer: ", default=str(package_selected["total_amount"]))
        )
        clear_display(2)
        print("Plan Final Offer : " + str(final_offer), "\n")

        if qt.confirm("Are you sure you want to create plan ?").ask():
            package_name = package_selected["package_name"]
            start_date = "-".join(start_date.split("-")[::-1])
            duration = int(package_selected["duration"])
            training_type = package_selected["training_type"]

            database.create_plan(
                member_name,
                package_name,
                start_date,
                duration,
                training_type,
                0,
                final_offer,
            )

    elif menu == "Renew Plan":
        package_names = []
        for p in database.retrive_packages():
            values = [
                p["package_name"],
                p["total_amount"],
                p["duration"],
                p["training_type"],
            ]
            package_names.append(
                "{} [{} for {} months] with training type {}".format(*values)
            )
        package_selection = qt.select(
            "Select A Package", qmark="", choices=package_names
        ).ask()
        for package in database.retrive_packages():
            if package["package_name"] in package_selection:
                package_selected = package
        start_date = (member_plan["expiring_date"] + relativedelta(days=1)).strftime(
            "%d-%m-%Y"
        )
        package_duration = relativedelta(months=int(package_selected["duration"]))
        plan_end_date = (
            datetime.strptime(start_date, "%d-%m-%Y") + package_duration
        ).strftime("%d-%m-%Y")
        clear_display(1)
        print("\nPackage Selected  :", package_selected["package_name"])
        print("Plan Start Date   :", start_date)
        print("Plan Duration     :", str(package_selected["duration"]), "months")
        print("Plan End Date     :", plan_end_date)
        print("Training Type     :", package_selected["training_type"])

        final_offer = int(
            prompt(
                "\nEnter Final Offer: ", default=str(package_selected["total_amount"])
            )
        )
        clear_display(2)
        print("Plan Final Offer  : " + str(final_offer), "\n")

        if qt.confirm("Are you sure you want to create plan ?").ask():
            package_name = package_selected["package_name"]
            start_date = "-".join(start_date.split("-")[::-1])
            duration = int(package_selected["duration"])
            training_type = package_selected["training_type"]

            database.renew_plan(
                member_name,
                package_name,
                start_date,
                duration,
                training_type,
                0,
                final_offer,
            )

    elif menu == "Make Payment":
        print("Amount Pending : ", member_plan["amount_pending"], "\n")
        payment_amount = int(
            prompt(
                "Enter Payment Amount: ",
                validator=PaymentAmountValidator(member_plan["amount_pending"]),
            )
        )
        clear_display(1)
        print("Payment Amount : " + str(payment_amount))

        payment_date = prompt(
            "Enter Payment Date [dd-mm-yy] : ",
            validator=DateValidator("payment_date"),
            default=datetime.today().strftime("%d-%m-%Y"),
        )
        clear_display(1)
        print("Payment Date   : " + str(payment_date))

        payment_mode = qt.select(
            "Select Payment Mode", qmark="", choices=["Cash", "Card", "UPI"]
        ).ask()
        clear_display(1)
        print("Payment Mode   : " + str(payment_mode), "\n")

        if qt.confirm("Are you sure you want to make payment ?").ask():
            database.make_payment(
                member_name,
                payment_amount,
                "-".join(payment_date.split("-")[::-1]),
                payment_mode,
            )

    elif menu == "Remove Plan":
        current_member_plan = list(member_plan["current_member_plan"].values()) != [
            None,
            None,
            None,
            None,
        ]
        renewed_member_plan = list(member_plan["renewed_member_plan"].values()) != [
            None,
            None,
            None,
            None,
        ]
        if current_member_plan and renewed_member_plan:
            if qt.confirm("Are you sure you want to remove renewed plan ?").ask():
                database.remove_renewed_plan(member_name)
        else:
            if qt.confirm("Are you sure you want to remove current plan ?").ask():
                database.remove_current_plan(member_name)

    elif menu == "Exit":
        return


if __name__ == "__main__":
    gms()
