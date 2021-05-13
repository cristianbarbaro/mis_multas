import smtplib


def send_email():
    TO = 'user@gmail.com'
    SUBJECT = 'Multas'
    TEXT = 'Texto.'

    # Gmail Sign In
    gmail_sender = 'username@gmail.com'
    gmail_passwd = 'xxxx'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)

    BODY = '\r\n'.join(['To: %s' % TO,
                        'From: %s' % gmail_sender,
                        'Subject: %s' % SUBJECT,
                        '', TEXT])

    try:
        server.sendmail(gmail_sender, [TO], BODY)
        print ('email sent')
    except:
        print ('error sending mail')

    server.quit()


send_email()