import smtplib
import time

import email_temp
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

email_count = 0
delay = 300
not_sent = []
start_running = time.time()

with open("receivers.txt", "r") as file:
    for line in file:
        try:
            email_sender = "your email"  # For mor secure you can add variables to system path and
            password = "your password"   # use the here
            email_getter = line.strip()

            msg = MIMEMultipart()
            # msg.attach(MIMEText("You can add some text to letter"))
            msg["From"] = "email From..."
            msg["Subject"] = "Input Subject here"
            msg.attach(MIMEText(email_temp.html, "html"))

            # with open("filename.pdf", "rb") as f:   # If you need to add attachment to letter, just uncomment this
            #     file = MIMEApplication(f.read(), Name=basename("filename.pdf"))  #  and add file to same directory
            # msg.attach(file)

            smtp_server = smtplib.SMTP("smtp.google.com", 587)
            smtp_server.starttls()
            smtp_server.login(email_sender, password)
            # smtp_server.set_debuglevel(1)
            smtp_server.sendmail(email_sender, email_getter, msg.as_string())

            email_count += 1

            print(f"\033[37m{line.strip()} sent! #{email_count}")

# Google block account with high automatic activity. If you sent more 80 letters server will disconnect you.
# Code bellow helps you to pass this error but only if you will send only 100 - 120 letters at start.
# If you will send many letters Google will block your account.

            # After sent 80 letters you will catch this error
        except smtplib.SMTPServerDisconnected:
            print(f"\033[32m Execution delay {delay} sec.")
            time.sleep(delay)
            delay += 120

            # Bad addresses collects here
        except smtplib.SMTPRecipientsRefused:
            print(f"\033[31m{line} not sent!")
            not_sent.append(line)

end_running = time.time()
total_time = int((end_running - start_running) / 60)

print(f"\033[32m Total sent {email_count} in {total_time} minutes")
print(f"\033[32m Bad addresses: {not_sent}")



