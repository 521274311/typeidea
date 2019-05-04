from django.shortcuts import render
from .models import Tag, Post, Category
from configs.models import SideBar
from django.views.generic import DetailView,ListView
from django.shortcuts import get_object_or_404
# Create your views here.
def post_list(request, category_id=None, tag_id=None):
    tag = None
    category = None
    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list, category = Post.get_by_category(category_id)
    else:
        post_list = Post.lastest_posts()

    context = {
        'category' : category,
        'tag' : tag,
        'post_list': post_list,
        'sidebars': SideBar.ge_all(),
    }
    context.update(Category.get_navs())

    return render(request, 'blog/list.html', context=context)

def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None
    context = {
        'post': post,
        'sidebars' : SideBar.ge_all(),
    }
    context.update(Category.get_navs())
    return render(request,'blog/detail.html',context)


class PostDetailView(DetailView):
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    template_name = 'blog/detail.html'


class PostListView(ListView):
    queryset = Post.lastest_posts()
    paginate_by = 1
    context_object_name = 'post_list'
    template_name = 'blog/list2.html'


class CommonViewMixin:
    '''
    导入公共视图信息
    '''
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars' : SideBar.ge_all(),
        })
        context.update(Category.get_navs())
        return context


class IndexView(CommonViewMixin,ListView):
    queryset = Post.lastest_posts()
    paginate_by = 1
    context_object_name = 'post_list'
    template_name = 'blog/list2.html'


class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category' : category,
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        print(self.kwargs)
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Category, pk=tag_id)
        context.update({
            'tag' : tag,
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        print(queryset.all())
        print(self.kwargs)
        print(type(self.kwargs))
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)