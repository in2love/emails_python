import smtplib
import time

import email_temp
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

email_count = 0  # счётчик отправок
delay = 300      # Задержка выполения кода при достижении лимита от гугл (стартовая)
not_sent = []    # Массив для корявых адресов
start_running = time.time()

with open("recievers.txt", "r") as file:
    for line in file:
        try:
            email_sender = "info@galmet74.ru"  # Знаю,
            password = "20p!lot10"         # не секьюрно!
            email_getter = line.strip()

            msg = MIMEMultipart()
            # msg.attach(MIMEText("Письмо свёрстано на тильде!"))
            msg["From"] = "info@galmet74.ru"
            msg["Subject"] = "Доступные гальванические покрытия"
            msg.attach(MIMEText(email_temp.html, "html"))
            """Описываем файл вложения для писем
            with open("file.txt", "rb") as f:
                file = MIMEApplication(f.read(), Name=basename("file.txt"))
            msg.attach(file)"""

            smtp_server = smtplib.SMTP("smtp.yandex.ru", 587)
            smtp_server.starttls()
            smtp_server.login(email_sender, password)
            # smtp_server.set_debuglevel(1)
            smtp_server.sendmail(email_sender, email_getter, msg.as_string())

            email_count += 1

            print(f"\033[37m{line.strip()} sent! #{email_count}")

            # Обрабатываем блокировку от Google
        except smtplib.SMTPServerDisconnected:
            print(f"\033[32m Задержка выполнения {delay} секунд.")
            time.sleep(delay)  # Зедержка Выполнения отправки
            delay += 120

            # Обрабатываем корявые адреса
        except smtplib.SMTPRecipientsRefused:
            print(f"\033[31m{line} not sent!")
            not_sent.append(line)

end_running = time.time()
total_time = int((end_running - start_running) / 60)

print(f"\033[32m Всего отправлено {email_count} за {total_time} минут")
print(f"\033[32m Кривые адреса: {not_sent}")



