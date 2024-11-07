import mysql.connector as sql
from dateutil.relativedelta import relativedelta
from datetime import datetime
import questionary as qt
import keyring

# tables in gms database

MEMBER_DETAILS = """
CREATE TABLE member_details(
    member_id INT AUTO_INCREMENT primary key,
    member_name VARCHAR(255) NOT NULL,
    gender VARCHAR(255) NOT NULL,
    dob DATE NOT NULL,
    phone VARCHAR(255) NOT NULL)"""

CURRENT_PLAN = """
CREATE TABLE current_plan(
    member_name VARCHAR(255) NOT NULL primary key,
    plan_name VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    duration INT NOT NULL,
    training_type VARCHAR(255) NOT NULL,
    paid_amount INT NOT NULL,
    total_amount INT NOT NULL)"""

RENEWED_PLAN = """
CREATE TABLE renewed_plan(
    member_name VARCHAR(255) NOT NULL primary key,
    plan_name VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    duration INT NOT NULL,
    training_type VARCHAR(255) NOT NULL,
    paid_amount INT NOT NULL,
    total_amount INT NOT NULL)"""
EXPIRED_PLAN = """
CREATE TABLE expired_plan(
    member_name VARCHAR(255) NOT NULL primary key,
    plan_name VARCHAR(255) NOT NULL,
    expired_date DATE NOT NULL,
    paid_amount INT NOT NULL,
    total_amount INT NOT NULL)"""

PACKAGES = """
CREATE TABLE packages(
    package_id INT AUTO_INCREMENT primary key,
    package_name VARCHAR(255) NOT NULL,
    duration INT NOT NULL,
    total_amount INT NOT NULL,
    training_type VARCHAR(255) NOT NULL)"""

PAYMENT_HISTORY = """
CREATE TABLE payment_history(
    member_name VARCHAR(255) NOT NULL,
    plan_name VARCHAR(255) NOT NULL,
    payment_amount INT NOT NULL,
    payment_date DATE NOT NULL,
    payment_mode VARCHAR(255) NOT NULL)"""

DATABASE_TABLES = [
    MEMBER_DETAILS,
    CURRENT_PLAN,
    PACKAGES,
    RENEWED_PLAN,
    EXPIRED_PLAN,
    PAYMENT_HISTORY,
]


class Database:
    def __init__(self) -> None:
        # ----------getting mysql creds from user--------------#
        while True:
            username = keyring.get_password("my_sql", "username")
            password = keyring.get_password("my_sql", "password")
            try:
                sql.connect(host="localhost", user=username, password=password)
                break
            except:
                username = input(" Enter MySQL username: ")
                password = qt.password("Enter MySQL password:", qmark="").ask()
                print("\033[F\033[K" * 3, end="")
                keyring.set_password("my_sql", "username", username)
                keyring.set_password("my_sql", "password", password)
        # ---------- establishing mysql connection --------------#
        try:
            self.connection = sql.connect(
                host="localhost",
                user=keyring.get_password("my_sql", "username"),
                password=keyring.get_password("my_sql", "password"),
            )
        except:
            print("MySQL not installed")
            exit()
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"SHOW DATABASES LIKE 'gms'")

        if not self.cursor.fetchone():
            self.cursor.execute("CREATE DATABASE gms")
            self.cursor.execute("USE gms")
            for table in DATABASE_TABLES:
                self.cursor.execute(table)
        self.cursor.execute("USE gms")
        self.connection.commit()
        # ----------update member plans --------------#
        self.cursor.execute("SELECT * FROM current_plan")
        current_plans = self.cursor.fetchall()
        for plan in current_plans:
            member_name, start_date, duration = plan[0], plan[2], plan[3]
            expiring_date = start_date + relativedelta(months=duration)
            if expiring_date < datetime.today().date():
                self.cursor.execute(
                    f"SELECT paid_amount, total_amount FROM current_plan WHERE member_name = '{member_name}'"
                )
                payment_details = self.cursor.fetchone()
                self.remove_current_plan(member_name)
                if payment_details[0] != payment_details[1]:
                    self.cursor.execute(
                        f"INSERT INTO expired_plan VALUES('{member_name}', '{plan[1]}', '{expiring_date.strftime('%Y-%m-%d')}', {payment_details[0]}, {payment_details[1]})"
                    )
                    self.connection.commit()
                else:
                    self.cursor.execute(
                        f"SELECT * FROM renewed_plan WHERE member_name = '{member_name}'"
                    )
                    renewed_plan = self.cursor.fetchone()
                    if renewed_plan:
                        self.create_plan(member_name, *renewed_plan[1:])
                        self.remove_renewed_plan(member_name)

    # --------------current plan-----------------#
    def retrive_current_plan(self, member_name: str):
        self.cursor.execute(
            f"SELECT * FROM current_plan WHERE member_name = '{member_name}'"
        )
        current_plan = self.cursor.fetchone()
        if current_plan:
            field_names = [i[0] for i in self.cursor.description]
            return {key: value for key, value in zip(field_names, current_plan)}
        return None

    def create_plan(
        self,
        member_name: str,
        plan_name: str,
        start_date,
        duation: int,
        training_type: str,
        paid_amount: int,
        total_amount: int,
    ):
        self.cursor.execute(
            f"INSERT INTO current_plan VALUES('{member_name}','{plan_name}','{start_date}',{duation},'{training_type}',{paid_amount},{total_amount})"
        )
        self.connection.commit()

    def remove_current_plan(self, member_name: str):
        self.cursor.execute(
            f"DELETE FROM current_plan WHERE member_name = '{member_name}'"
        )
        self.connection.commit()

    # --------------renewed plan---------------#
    def retrive_renewed_plan(self, member_name: str):
        self.cursor.execute(
            f"SELECT * FROM renewed_plan WHERE member_name = '{member_name}'"
        )
        renewed_plan = self.cursor.fetchone()
        if renewed_plan:
            field_names = [i[0] for i in self.cursor.description]
            return {key: value for key, value in zip(field_names, renewed_plan)}
        return None

    def renew_plan(
        self,
        member_name: str,
        plan_name: str,
        start_date,
        duation: int,
        training_type: str,
        paid_amount: int,
        total_amount: int,
    ):
        self.cursor.execute(
            f"INSERT INTO renewed_plan VALUES('{member_name}','{plan_name}','{start_date}',{duation},'{training_type}',{paid_amount},{total_amount})"
        )
        self.connection.commit()

    def remove_renewed_plan(self, member_name: str):
        self.cursor.execute(
            f"DELETE FROM renewed_plan WHERE member_name = '{member_name}'"
        )
        self.connection.commit()

    # --------------expired plan-----------------#
    def retrive_expired_plan(self, member_name: str):
        self.cursor.execute(
            f"SELECT * FROM expired_plan WHERE member_name = '{member_name}'"
        )
        expired_plan = self.cursor.fetchone()
        if expired_plan:
            field_names = [i[0] for i in self.cursor.description]
            return {key: value for key, value in zip(field_names, expired_plan)}
        return None

    # --------------manage members-----------------#
    def retrive_member_name(self, member_id: int):
        query = "SELECT member_name FROM member_details WHERE member_id = "
        self.cursor.execute(query + member_id)
        result = self.cursor.fetchone()
        return result[0] if result else None

    def retrive_members(self):
        self.cursor.execute("SELECT * FROM member_details")
        member_details = self.cursor.fetchall()
        member_fields = [i[0] for i in self.cursor.description]
        members: list[dict] = []
        for member in member_details:
            member_dict = {key: value for key, value in zip(member_fields, member)}
            self.cursor.execute(
                "SELECT * FROM current_plan WHERE member_name = %s",
                (member_dict["member_name"],),
            )
            member_dict["status"] = "🟩" if self.cursor.fetchone() else "🟥"
            members.append(member_dict)
        return members

    def add_member(self, member_name: str, gender: str, dob: str, phone: str):
        query = "INSERT INTO member_details(member_name, gender, dob, phone) VALUES(%s, %s, %s, %s)"
        self.cursor.execute(query, (member_name, gender, dob, phone))
        self.connection.commit()

    def modify_member(
        self,
        initial_member_name: str,
        member_name: str,
        gender: str,
        dob: str,
        phone: str,
    ):
        self.cursor.execute(
            f"UPDATE member_details SET member_name = '{member_name}', gender = '{gender}', dob = '{dob}', phone = '{phone}' WHERE member_name = '{initial_member_name}'"
        )
        self.cursor.execute(
            f"UPDATE current_plan SET member_name = '{member_name}' WHERE member_name = '{initial_member_name}'"
        )
        self.cursor.execute(
            f"UPDATE renewed_plan SET member_name = '{member_name}' WHERE member_name = '{initial_member_name}'"
        )
        self.connection.commit()

    def delete_member(self, member_name: str):
        self.cursor.execute(
            f"DELETE FROM current_plan WHERE member_name = '{member_name}'"
        )
        self.cursor.execute(
            f"DELETE FROM member_details WHERE member_name = '{member_name}'"
        )
        self.cursor.execute("SELECT * FROM member_details")
        member_details = self.cursor.fetchall()
        self.cursor.execute("DROP TABLE member_details")
        self.cursor.execute(MEMBER_DETAILS)
        for member_detail in member_details:
            self.add_member(*member_detail[1:])
        self.connection.commit()

    # -----------manage member plan--------------#
    def retrive_member_plan(self, member_id: int):
        member_name = self.retrive_member_name(member_id)
        current_plan = self.retrive_current_plan(member_name)
        renewed_plan = self.retrive_renewed_plan(member_name)
        expired_plan = self.retrive_expired_plan(member_name)
        renewed_member_plan = {
            "plan_name": None,
            "start_date": None,
            "duration": None,
            "training_type": None,
        }
        current_member_plan = {
            "plan_name": None,
            "start_date": None,
            "duration": None,
            "training_type": None,
        }
        expired_member_plan = {
            "plan_name": None,
            "expired_date": None,
            "paid_amount": None,
            "total_amount": None,
        }
        expiring_date, amount_pending, amount_paid = (None, None, None)
        if renewed_plan:
            for key in renewed_plan:
                renewed_member_plan[key] = renewed_plan[key]
        if current_plan:
            for key in current_plan:
                current_member_plan[key] = current_plan[key]
        if expired_plan:
            for key in expired_plan:
                expired_member_plan[key] = expired_plan[key]
        if renewed_plan and current_plan:
            expiring_date = renewed_plan["start_date"] + relativedelta(
                months=renewed_plan["duration"]
            )
            amount_pending = renewed_plan["total_amount"] - renewed_plan["paid_amount"]
            amount_paid = renewed_plan["paid_amount"]
        elif current_plan:
            expiring_date = current_plan["start_date"] + relativedelta(
                months=current_plan["duration"]
            )
            amount_pending = current_plan["total_amount"] - current_plan["paid_amount"]
            amount_paid = current_plan["paid_amount"]
        elif expired_plan:
            expiring_date = expired_plan["expired_date"]
            amount_pending = expired_plan["total_amount"] - expired_plan["paid_amount"]
            amount_paid = expired_plan["paid_amount"]
        return {
            "current_member_plan": current_member_plan,
            "renewed_member_plan": renewed_member_plan,
            "expired_member_plan": expired_member_plan,
            "expiring_date": expiring_date,
            "amount_pending": amount_pending,
            "amount_paid": amount_paid,
        }

    # --------------manage packages-----------------#
    def retrive_packages(self):
        self.cursor.execute("SELECT * FROM packages")
        package_details = self.cursor.fetchall()
        package_fields = [i[0] for i in self.cursor.description]
        packages = [
            {key: value for key, value in zip(package_fields, package)}
            for package in package_details
        ]
        return packages

    def create_package(
        self, package_name: str, duration: int, total_amount: int, training_type: str
    ) -> None:
        """Create a package in the database."""
        query = "INSERT INTO packages (package_name, duration, total_amount, training_type) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(
            query, (package_name, duration, total_amount, training_type)
        )
        self.connection.commit()

    def modify_package(
        self,
        initial_package_name: str,
        package_name: str,
        duration: int,
        total_amount: int,
        training_type: str,
    ) -> None:
        """Modify a package in the database."""
        query = "UPDATE packages SET package_name = %s, duration = %s, total_amount = %s, training_type = %s WHERE package_name = %s"
        self.cursor.execute(
            query,
            (package_name, duration, total_amount, training_type, initial_package_name),
        )
        self.connection.commit()

    def delete_package(self, package_name: str):
        self.cursor.execute(
            f"DELETE FROM packages WHERE package_name = '{package_name}'"
        )
        self.cursor.execute("SELECT * FROM packages")
        package_details = self.cursor.fetchall()
        self.cursor.execute("DROP TABLE packages")
        self.cursor.execute(PACKAGES)
        for package_detail in package_details:
            self.create_package(*package_detail[1:])
        self.connection.commit()

    # --------------payment history-----------------#
    def retrive_payment_history(self):
        query = "SELECT * FROM payment_history"
        self.cursor.execute(query)
        payment_history = self.cursor.fetchall()
        if payment_history:
            field_names = [i[0] for i in self.cursor.description]
            return [
                {key: value for key, value in zip(field_names, values)}
                for values in payment_history
            ]
        return []

    def make_payment(
        self,
        member_name: str,
        payment_amount: int,
        payment_date: str,
        payment_mode: str,
    ):
        renewed_plan = self.retrive_renewed_plan(member_name)
        current_plan = self.retrive_current_plan(member_name)
        expired_plan = self.retrive_expired_plan(member_name)
        if renewed_plan:
            self.cursor.execute(
                f"UPDATE renewed_plan SET paid_amount = paid_amount + {payment_amount} WHERE member_name = '{member_name}'"
            )
            self.cursor.execute(
                f"INSERT INTO payment_history VALUES('{member_name}','{renewed_plan['plan_name']}',{payment_amount},'{payment_date}','{payment_mode}')"
            )
        elif current_plan:
            self.cursor.execute(
                f"UPDATE current_plan SET paid_amount = paid_amount + {payment_amount} WHERE member_name = '{member_name}'"
            )
            self.cursor.execute(
                f"INSERT INTO payment_history VALUES('{member_name}','{current_plan['plan_name']}',{payment_amount},'{payment_date}','{payment_mode}')"
            )
        elif expired_plan:
            self.cursor.execute(
                f"UPDATE expired_plan SET paid_amount = paid_amount + {payment_amount} WHERE member_name = '{member_name}'"
            )
            self.cursor.execute(
                f"INSERT INTO payment_history VALUES('{member_name}','{expired_plan['plan_name']}',{payment_amount},'{payment_date}','{payment_mode}')"
            )
        self.connection.commit()

    # --------------reset database---------------#
    def reset_database(self):
        self.cursor.execute("DROP DATABASE gms")
        self.connection.close()
        self.__init__()
