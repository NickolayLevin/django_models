import django_filters 
from .models import Post, Category
from django import forms

class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Название содержит'
    )


    post_type = django_filters.ModelMultipleChoiceFilter(
        field_name='categories',
        queryset=Category.objects.all(), 
        widget=forms.CheckboxSelectMultiple,
        label='Категории'   
    )


    date_after = django_filters.DateFilter(
        field_name='date',
        lookup_expr='gte',
        label='Дата публикации (позже чем)',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = ['title', 'post_type', 'date_after']

