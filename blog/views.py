from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from .models import Blog,BlogType

# Create your views here.
#将其他函数共同的东西写进下面这个函数
def get_blog_common_data(request,blogs_all_list):
    paginator = Paginator(blogs_all_list,settings.EACH_PAGE_BLOGS_NUMBER)
    page_num = request.GET.get('page',1)  
    page_of_blogs = paginator.get_page(page_num)
    currentr_page_num = page_of_blogs.number  #获取当前页码
    #获取当前页码2页之内的页码
    page_range = list(range(max(currentr_page_num-2,1),currentr_page_num))+\
                 list(range(currentr_page_num, min(currentr_page_num+2,paginator.num_pages)+1))
    #省略页
    if page_range[0] - 1 >= 2:
        page_range.insert(0,'...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    #首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    #获取博客分类的对应数量
    '''
    第一种方法,annotate注释
    BlogType.objects.annotate(blog_count=Count('blog'))
    第二种方法，循环遍历筛选出来的博客，统计数量
    blog_types = BlogType.objects.all()
    blog_type_list = []
    for blog_type in blog_types:
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
        blog_type_list.append(blog_type)
    '''
    
    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))  
    return context


#显示所有博客
def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blog_common_data(request,blogs_all_list)
    return render(request,'blog/blog_list.html',context)

#显示博客分类
def blogs_with_type(request,blog_type_pk):
    blog_type = get_object_or_404(BlogType,pk=blog_type_pk)  #传入博客类型的模型
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_common_data(request,blogs_all_list)  
    context['blog_type'] = get_object_or_404(BlogType,pk=blog_type_pk)  #传入博客类型的模型
    return render(request,'blog/blogs_with_type.html',context)

#显示博客内容
def blog_detail(request,blog_pk):
    blog = get_object_or_404(Blog,pk=blog_pk)
    blog.read_num += 1
    blog.save()
    context = {}
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last() #筛选大于当前博客创建时间的博客，取最后一篇
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first() #筛选小于当前博客创建时间的博客，取第一篇
    context['blog'] = blog
    return render(request,'blog/blog_detail.html',context)

