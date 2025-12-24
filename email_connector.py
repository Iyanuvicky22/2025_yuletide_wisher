import os
import pandas as pd
import datetime as dt
import smtplib
from dotenv import load_dotenv

load_dotenv()


def yuletide_mail_sender():
    """
    Function to send the email to all persons.
    """
    file_path = r"data\fourth_trial.xlsx"
    data = pd.read_excel(file_path)
    try:
        for _, row in data.iterrows():
            full_name = row["full_name"]
            email = row['email']
            name = row['first_name']
            message = row["ai_message"].strip('"')
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(user=os.getenv("my_email"),
                                 password=os.getenv("gmail_password"))
                connection.sendmail(
                    from_addr=os.getenv("my_email"),
                    to_addrs="iyanuvicky@gmail.com",
                    msg=f"Subject: Merry Xmas {full_name}\n\n{message}\n\nYours Sincerely\nArowosegbe Victor".encode("utf-8")
                )
    except FileNotFoundError:
        file_path = r"data\fourth_trial.excel"
        data = pd.read_excel(file_path)


if __name__ == "__main__":
    yuletide_mail_sender()

