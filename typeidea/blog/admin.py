from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Post, Category, Tag
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin
from .adminforms import PostAdminForm
from django.contrib.admin.models import LogEntry

class PostInline(admin.TabularInline):
    fields = ('title', 'desc')
    extra = 0
    model = Post


# Register your models here.
@admin.register(Category,site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'is_nav', 'post_count', 'owner', 'created_time')
    fields = ('name', 'status', 'is_nav')
    inlines = [PostInline,]

    def post_count(self,obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'post_count', 'created_time')
    fields = ('name', 'status')

    def post_count(self,obj):
        return obj.post_set.count()
    post_count.short_description = '文章数量'


class CategoryOwnerFilter(admin.SimpleListFilter):
    """  自定义过滤器 """
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.all().filter(owner=request.user).values_list('id','name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'status', 'owner',
        'created_time', 'operator'
    ]
    list_display_links = []
    list_filter = [CategoryOwnerFilter]
    search_fields = ['title', 'category__name']
    fieldsets = (
        ('基础配置', {
            'description' : '基础配置描述',
            'fields' : (
                ('title', 'category'),
                'status',
            ),
        }),
        ('内容', {
            'fields' : (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'classes' : ('collapse',),
            'fields' : ('tag',),

        }),
    )
    # form = PostAdminForm

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )
    # class Media:
    #     css = {
    #         'all' : {'https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css'}
    #     }

@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('object_repr', 'object_id', 'action_flag',
                    'user', 'change_message')
