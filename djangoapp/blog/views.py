from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import redirect
from blog.models import Post, Page
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404, HttpRequest, HttpResponse
from django.views.generic import ListView, DetailView

# Create your views here.
PER_PAGE = 9

class PostListView(ListView):
    model = Post
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    ordering = ('-pk', )
    paginate_by = PER_PAGE
    queryset = Post.my_objects.isPublished()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'HOME - ',
        })
        return context

# def index(request):
#     posts = Post.my_objects.isPublished()
#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     context = {
#         'page_obj': page_obj,
#     }
#     return render(
#         request,
#         'blog/pages/index.html',
#         context
#     )

class CreatedByListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context = {}

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        author_pk = self.kwargs.get('author_pk')
        user = User.objects.filter(pk=author_pk).first()
        if user is None:
            raise Http404()
        
        self._temp_context.update({
            'author_pk': author_pk,
            'user': user,
        })
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self._temp_context.get('user')
        user_name = user.username
        if user.first_name:
            user_name = f'{user.first_name} {user.last_name}'
        
        page_title = f'Posts de {user_name} - '
        context.update({
            'page_title': page_title,
        })
        return context
    
    def get_queryset(self) -> QuerySet[Any]:
        query_set = super().get_queryset()
        query_set = query_set.filter(created_by__pk=self._temp_context.get('user').pk)
        
        return query_set

# def created_by(request, author_pk):
#     user = User.objects.filter(pk=author_pk).first()
#     if user == None:
#         raise Http404()

#     user_name = user.username
#     if user.first_name:
#         user_name = f'Posts de {user.first_name} {user.last_name} - '

#     page_title = user_name

#     posts = Post.my_objects.isPublished().filter(created_by__pk=author_pk)
#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     context = {
#         'page_obj': page_obj,
#         'page_title': page_title,
#     }
#     return render(
#         request,
#         'blog/pages/index.html',
#         context
#     )

class CategoryListView(PostListView):
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        query_set = super().get_queryset().filter(category__slug=self.kwargs.get('slug'))
        return query_set
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_title = f'Categoria {self.object_list[0].category.name} - '
        context.update({
            'page_title': page_title,
        })
        return context

# def category(request, slug):
#     posts = Post.my_objects.isPublished().filter(category__slug=slug)

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     if len(page_obj) == 0:
#         raise Http404()

#     page_title = f'Categoria - {page_obj[0].category.name} - '

#     context = {
#         'page_obj': page_obj,
#         'page_title': page_title,
#     }
#     return render(
#         request,
#         'blog/pages/index.html',
#         context
#     )

class TagListView(PostListView):
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        query_set = super().get_queryset().filter(tags__slug=self.kwargs.get('slug'))
        return query_set
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_title = f'Tag {self.object_list[0].tags.first().name} - '
        context.update({
            'page_title': page_title,
        })
        return context

# def tag(request, slug):
#     posts = Post.my_objects.isPublished().filter(tags__slug=slug)

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     if len(page_obj) == 0:
#         raise Http404()

#     page_title = f'Tag - {page_obj[0].tags.first().name} - '

#     context = {
#         'page_obj': page_obj,
#         'page_title': page_title,
#     }
#     return render(
#         request,
#         'blog/pages/index.html',
#         context
#     )

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/pages/post.html'
    context_object_name = 'post'
    slug_field = 'slug'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        post_title = 'Página ' + post.title + ' - '
        context.update({
            'page_title': post_title,
        })
        return context
    
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(is_published=True)

# def post(request, slug):
#     post_obj = Post.my_objects.isPublished().filter(slug=slug).first()
#     if post_obj is None:
#         raise Http404()

#     page_title = f'Post - {post_obj.title} - '
#     context = {
#         'post': post_obj,
#         'page_title': page_title,
#     }
#     return render(
#         request,
#         'blog/pages/post.html',
#         context,
#     )

class SearchListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._search_value = ''

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self._search_value = request.GET.get('search', '').strip()
        return super().setup(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        query_set = super().get_queryset()
        query_set = query_set.filter(
            Q(title__icontains=self._search_value) |
            Q(excerpt__icontains=self._search_value) |
            Q(content__icontains=self._search_value),            
        )
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_title = f'Busca - {self._search_value[:30]} - '
        context.update({
            'page_title': page_title,
            'search_value': self._search_value,
        })
        return context

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if self._search_value == '':
            return redirect('blog:index')
        return super().get(request, *args, **kwargs)

# def search(request):
#     search_value = request.GET.get('search').strip()
#     posts = Post.my_objects.isPublished().filter(
#         Q(title__icontains=search_value) |
#         Q(excerpt__icontains=search_value) |
#         Q(content__icontains=search_value),
#     )

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     page_title = f'Busca - {search_value[:30]} - '

#     context = {
#         'page_obj': page_obj,
#         'search_value': search_value,
#         'page_title': page_title,
#     }
#     return render(
#         request,
#         'blog/pages/index.html',
#         context
#     )

class PageDetailView(DetailView):
    model = Page
    template_name = 'blog/pages/page.html'
    context_object_name = 'page'
    slug_field = 'slug'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        page = self.get_object()
        page_title = 'Página ' + page.title + ' - '
        context.update({
            'page_title': page_title,
        })
        return context
    
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(is_published=True)

# def page(request, slug):
#     page_obj = Page.my_objects.isPublished().filter(slug=slug).first()
#     if page_obj is None:
#         raise Http404()

#     page_title = f'Página - {page_obj.title} - '
#     context = {
#         'page': page_obj,
#         'page_title': page_title,
#     }
#     return render(
#         request,
#         'blog/pages/page.html',
#         context,
#     )