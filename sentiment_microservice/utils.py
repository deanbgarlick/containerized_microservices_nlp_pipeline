def take_top_email_from_chain(text):
    top_email = text.split('-- Forwarded by')[0]
    top_email = text.split('--Forwarded by')[0]
    top_email = top_email.split('-- Original Message')[0]
    top_email = top_email.split('--Original Message')[0]
    return top_email
