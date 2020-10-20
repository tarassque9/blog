from blog_project.celery import app
from django.core.mail import send_mail


def send(user_emails, link):
    send_mail(
        'Post notification',
        f'Your following user create new post {link}',
        'my_test_email@gmail.com',
        [user_emails],
        fail_silently=False
    )


@app.task
def send_post_notification(emails_list, link):
    send(emails_list, link)
