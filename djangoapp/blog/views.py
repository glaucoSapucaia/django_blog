from django.shortcuts import render
from django.core.paginator import Paginator
from blog.models import Post, Page
from django.db.models import Q

# Create your views here.
PER_PAGE = 9

def index(request):
    posts = Post.my_objects.isPublished()
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(
        request,
        'blog/pages/index.html',
        context
    )

def created_by(request, author_pk):
    posts = Post.my_objects.isPublished().filter(created_by__pk=author_pk)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(
        request,
        'blog/pages/index.html',
        context
    )

def category(request, slug):
    posts = Post.my_objects.isPublished().filter(category__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(
        request,
        'blog/pages/index.html',
        context
    )

def tag(request, slug):
    posts = Post.my_objects.isPublished().filter(tags__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(
        request,
        'blog/pages/index.html',
        context
    )

def post(request, slug):
    post = Post.my_objects.filter(slug=slug).first()
    context = {
        'post': post,
    }
    return render(
        request,
        'blog/pages/post.html',
        context,
    )

def search(request):
    search_value = request.GET.get('search').strip()
    posts = Post.my_objects.isPublished().filter(
        Q(title__icontains=search_value) |
        Q(excerpt__icontains=search_value) |
        Q(content__icontains=search_value),
    )

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_value': search_value,
    }
    return render(
        request,
        'blog/pages/index.html',
        context
    )

def page(request, slug):
    page = Page.my_objects.isPublished().filter(slug=slug).first()

    context = {
        'page': page,
    }
    return render(
        request,
        'blog/pages/page.html',
        context,
    )