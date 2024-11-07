from prompt_toolkit.validation import Validator, ValidationError
from datetime import datetime
from .database import Database
from rich.panel import Panel
from rich.layout import Layout


def clear_display(n):
    print("\033[F\033[K" * n, end="")


def get_member_plan_table(
    member_id,
    member_name,
    current_plan,
    renewed_plan,
    expired_plan,
    expiring_date,
    amount_pending,
    amount_paid,
):
    plan_template = """Plan Name     : {}\nStart Date    : {}\nPlan Duration : {}\nTraining Type : {}"""

    layout = Layout(name="member plan details", size=90)
    layout.split(
        Layout(name="plans", size=6),
        Layout(size=3, name="cards"),
    )
    layout["plans"].split_row(
        Layout(name="current plan", ratio=1),
        Layout(name="renewed plan", ratio=1),
    )
    layout["cards"].split_row(
        Layout(name="expiring on", ratio=1),
        Layout(name="amount pending", ratio=1),
        Layout(name="amount paid", ratio=1),
    )

    if list(current_plan.values()) == [None, None, None, None]:
        for key in current_plan:
            current_plan[key] = "--"

    if list(renewed_plan.values()) == [None, None, None, None]:
        for key in renewed_plan:
            renewed_plan[key] = "--"

    if list(expired_plan.values()) != [None, None, None, None]:
        plan_template = (
            """Expired Plan    : {}\nExpiry Date    : {}\nAmount Pending : {}"""
        )
        plan_name = expired_plan["plan_name"]
        expired_date = "-".join(expired_plan["expired_date"].split("-")[::-1])
        amount_pending = expired_plan["total_amount"] - expired_plan["paid_amount"]
        renderable = plan_template.format(plan_name, expired_date, amount_pending)
        expired_plan_panel = Panel(
            renderable, title=f"[ {member_id}. {member_name} ]", expand=False
        )
        return expired_plan_panel

    if not expiring_date:
        expiring_date = "--"
    if amount_pending == None:
        amount_pending = "--"
    if amount_paid == None:
        amount_paid = "--"

    layout["plans"]["current plan"].update(
        Panel(plan_template.format(*current_plan.values()), title="Current Plan")
    )
    layout["plans"]["renewed plan"].update(
        Panel(plan_template.format(*renewed_plan.values()), title="Renewed Plan")
    )
    layout["cards"]["expiring on"].update(Panel(f"Expiring On: {expiring_date}"))
    layout["cards"]["amount pending"].update(Panel(f"Pending Amount: {amount_pending}"))
    layout["cards"]["amount paid"].update(Panel(f"Amount Paid: {amount_paid}"))

    return Panel(
        layout,
        height=11,
        title=f"[ {member_id}. {member_name} ]",
        expand=False,
        width=90,
    )


class DateValidator(Validator):
    def __init__(self, type: str):
        self.type = type
        super().__init__()

    def validate(self, document):
        try:
            date = datetime.strptime(document.text, "%d-%m-%Y")
            if self.type == "dob" and date.date() >= datetime.today().date():
                raise ValidationError(message="The date must be before today.")
            elif self.type == "start_date" and date.date() < datetime.today().date():
                raise ValidationError(message="The date must be on or after today.")
        except ValueError:
            raise ValidationError(message="Invalid date format")


class PhoneValidator(Validator):
    def validate(self, phone: str):
        phone = phone.text
        if not phone.isdigit():
            raise ValidationError(message="Phone number must only contain digits.")
        elif len(phone) != 10:
            raise ValidationError(message="Phone number must be 10 digits long.")


class IDValidator(Validator):
    def __init__(self, type: str):
        self.type = type

    def validate(self, document):
        id_type = self.type.upper()
        if str(document.text) == "":
            raise ValidationError(message=f"{id_type} ID should be a number")
        try:
            id = int(document.text)

        except Exception:
            raise ValidationError(message=f"{id_type} ID should be a number")
        database = Database()
        table = (
            database.retrive_members()
            if self.type == "member"
            else database.retrive_packages()
        )
        ids = [int(i[f"{self.type}_id"]) for i in table]
        if id not in ids:
            raise ValidationError(message=f"Invlaid {id_type} ID")


class PaymentAmountValidator(Validator):
    def __init__(self, amount_pending):
        self.amount_pending = amount_pending
        super().__init__()

    def validate(self, document):
        try:
            if document.text == "":
                raise ValidationError(message="Amount cannot be empty")
            amount = int(document.text)
            if self.amount_pending and amount > self.amount_pending:
                raise ValidationError(
                    message="Amount should be less than pending amount"
                )
            elif amount < 100:
                raise ValidationError(message="Minimum payment amount is 100")
        except ValueError:
            raise ValidationError(message=f"Amount should be a number")


class NameValidator(Validator):
    def __init__(self, type, exclude=None):
        self.type = type
        self.exclude = exclude
        if self.exclude:
            self.exclude = self.exclude.strip().lower()
        super().__init__()

    def validate(self, name):
        name: str = name.text
        database = Database()
        table = (
            database.retrive_members()
            if self.type == "member"
            else database.retrive_packages()
        )
        names = [i[f"{self.type}_name"].strip().lower() for i in table]
        if self.exclude:
            names.remove(self.exclude)
        if name.strip().lower() in names:
            raise ValidationError(message=f"{self.type.upper()} already exists.")
        elif name.strip().lower() == "":
            raise ValidationError(message=f"{self.type.upper()} name cannot be empty.")
        elif not name.replace(" ", "").lower().isalpha():
            raise ValidationError(
                message=f"{self.type.upper()} name cannot include a number."
            )

class DigitValidator(Validator):
    def validate(self, document):
        try:
            if document.text == "":
                raise ValidationError(message="Input cannot be empty")
            number = int(document.text)
        except ValueError:
            raise ValidationError(message="Input should be a number")

class NumberValidator(Validator):
    def validate(self, document):
        try:
            if document.text == "":
                raise ValidationError(message="Input cannot be empty")
            number = int(document.text)
            if number > 10:
                raise ValidationError(
                    message="Cannot add more than 10 members at a time"
                )
        except ValueError:
            raise ValidationError(message="Input should be a number")
