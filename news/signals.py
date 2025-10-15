from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import timedelta
from django.utils import timezone
from .models import Post, Category
from django.contrib.auth.models import User
from allauth.account.signals import user_signed_up


# @receiver(m2m_changed, sender=Post.categories.through)
# def notify_subscribers_on_category_add(sender, instance, action, pk_set, **kwargs):
#     if action == 'post_add' and instance.post_type == Post.PostType.NEWS:
#         if timezone.now() - instance.date < timedelta(minutes=1):
#             added_categories = Category.objects.filter(pk__in=pk_set)
#             for category in added_categories:
#                 subscribers = category.subscribers.all()
#                 for user in subscribers:
#                     subject = instance.title
#                     html_message = render_to_string('email_new_post.html', {
#                         'user': user,
#                         'post': instance,
#                         'preview_text': instance.text[:50] + '...' if len(instance.text) > 50 else instance.text,
#                     })
#                     plain_message = strip_tags(html_message)
#                     send_mail(
#                         subject=subject,
#                         message=plain_message,
#                         from_email=None,
#                         recipient_list=[user.email],
#                         html_message=html_message,
#                     )


@receiver(user_signed_up)
def send_welcome_email_allauth(request, user, **kwargs):
    subject = 'Добро пожаловать на сайт!'
    html_message = render_to_string('welcome_email.html', {'user': user})
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, None, [user.email], html_message=html_message)
