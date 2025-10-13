from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import Category, Post, User

def send_weekly_newsletter():
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