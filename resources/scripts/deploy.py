import os
import re
import shutil
import subprocess
import sys
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "it.ipese@epfl.ch"
sender_user = "it.ipese"
sender_password = "sender_password_value"
recipient_email = "joao.ferreiradasilva@epfl.ch"
log_file_path = "quarto_logs.log" 

def notify_it_support(message):
    if message is not None:
        print(f"Error: {message}")
    print("Trying again")

    if not sender_password.startswith("sender_password_v"):
        print("sending email")
        subject = "IPESE-BLOG-V2 error"

        email_message = MIMEMultipart()
        email_message["From"] = sender_email
        email_message["To"] = recipient_email
        email_message["Subject"] = subject

        email_message.attach(MIMEText(message, "plain"))

        with smtplib.SMTP("mail.epfl.ch", 587) as server:
            server.starttls()  # Enable TLS for security
            server.login(sender_user, sender_password)  # Login to your email account
            server.sendmail(sender_email, recipient_email, email_message.as_string())  # Send the email

def trydeploy(type,skiped_folders):
    subprocess.run("quarto render --to "+type+"> "+log_file_path+" 2>&1", shell=True)
    try:
        last_line = None

        # Wait for last_line to be not None
        while last_line is None:
            with open(log_file_path, "a+") as log_file:
                log_file.seek(0)
                lines = log_file.readlines()
                last_line = next((line.strip() for line in reversed(lines) if line.strip()), None)

        if last_line.startswith("Output created: _site"):
            print("Quarto render successful!")
        else:
            pattern = re.compile(r'\[\s*\d+/\d+\] .+\.qmd')
            matched_line= next((line.strip() for line in reversed(lines) if pattern.match(line)), None)
            matched_line, matched_index = next(((line.strip(), i) for i, line in enumerate(reversed(lines)) if pattern.match(line)), (None, None))
            error_path = re.sub(r'\[\s*\d+/\d+\]\s*', '', matched_line)

            if error_path:
                for line in lines[len(lines) - matched_index:]:
                    print(line)
                    
                error_path= error_path.split(".qmd")[0]+".qmd"
                error_path_split = error_path.split("/")
                underscored_path = os.path.join(error_path_split[0], "_" +error_path_split[1])

                shutil.move(error_path, underscored_path)
                skiped_folders.append(underscored_path)

                print(f"Ipese-blog-v2 found an error in folder {error_path}, now ignoring error and trying to build again.")
                skiped_folders=trydeploy(type, skiped_folders)
            else:
                print("Quarto render failed. Check logs for details.")
                with open("quarto_logs.log", "a+") as log_file:
                    log_file.seek(0)
                    print(log_file.readlines())
        
        return skiped_folders

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)






main_folder="html"
print(f"building {main_folder}")
trydeploy(main_folder,[])
