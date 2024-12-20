from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now
from .models import Post, Category


def index(request):
    post_list = Post.objects.filter(
        is_published=True,
        pub_date__lte=now(),
        category__is_published=True
    ).order_by('-pub_date')[:5]
    return render(request, 'blog/index.html', {'post_list': post_list})


def post_detail(request, pk):
    post = get_object_or_404(
        Post,
        pk=pk,
        is_published=True,
        pub_date__lte=now(),
        category__is_published=True
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug, is_published=True)
    post_list = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=now()
    ).order_by('-pub_date')
    return render(request, 'blog/category.html',
                  {'category': category, 'post_list': post_list})
