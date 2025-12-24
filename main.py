from message_generator import message_main
from email_connector import yuletide_mail_sender


if __name__ == "__main__":
    generate_messages = message_main()
    send_emails = yuletide_mail_sender()

