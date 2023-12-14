from django.shortcuts import render
from django.core.paginator import Paginator

# Create your views here.
posts = list(range(1000))

def index(request):
    paginator = Paginator(posts, 9)
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

def post(request):
    return render(
        request,
        'blog/pages/post.html'
    )

def page(request):
    return render(
        request,
        'blog/pages/page.html',
    )