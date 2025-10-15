from celery import shared_task
import time
from .models import *
from datetime import timedelta
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

@shared_task
def new_post_in_category_email(post_id):
    instance = Post.objects.get(id=post_id)
    added_categories = instance.categories.all()
    for category in added_categories:
            subscribers = category.subscribers.all()
            for user in subscribers:
                subject = instance.title
                html_message = render_to_string('email_new_post.html', {
                    'user': user,
                    'post': instance,
                    'preview_text': instance.text[:50] + '...' if len(instance.text) > 50 else instance.text,
                })
                plain_message = strip_tags(html_message)
                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email=None,
                    recipient_list=[user.email],
                    html_message=html_message,
                )

@shared_task
def send_email_every_monday():
    one_week_ago = timezone.now() - timedelta(days=7)
    categories = Category.objects.all()
    
    for category in categories:
        if not category.subscribers.exists():
            continue  
        
        
        category.last_newsletter_date = timezone.now()
        category.save()
        
       
        subscribers = category.subscribers.all()
        new_posts_in_category = Post.objects.filter(
            categories=category,
            date__gte=one_week_ago,
            post_type__in=[Post.PostType.NEWS, Post.PostType.ARTICLE]  
        ).distinct().order_by('-date')
        
        if not new_posts_in_category.exists():
            continue  
        
        for user in subscribers:
            user_categories = user.subscribed_categories.all()
            user_new_posts = Post.objects.filter(
                categories__in=user_categories,
                date__gte=one_week_ago,
                post_type__in=[Post.PostType.NEWS, Post.PostType.ARTICLE]
            ).distinct().order_by('-date')
            
            if not user_new_posts.exists():
                continue
            
          
            subject = f'Новые статьи за неделю в твоих категориях ({user_new_posts.count()} шт.)'
            html_message = render_to_string('email_weekly_newsletter.html', {
                'user': user,
                'new_posts': user_new_posts[:10],  
                'site_domain': settings.SITE_DOMAIN,
            })
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )

