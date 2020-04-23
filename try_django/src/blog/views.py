from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .models import BlogPost
from .forms import BlogPostForm, BlogPostModlelForm


# def blog_post_detail_page(request, slug):
#     print("Django says", request.method, request.path, request.user)
    # try:
    #     obj = BlogPost.objects.get(id=post_id)
    # except BlogPost.DoesNotExist:
    #     raise Http404
    # except ValueError:
    #     raise Http404
    # queryset = BlogPost.objects.filter(slug=slug)
    # if queryset.count() ==0:
    #     raise Http404
        
    
    # obj = queryset.first()
    
    # obj = get_object_or_404(BlogPost, slug=slug)
    # template_name = 'blog_post_detail.html'
    # context = {"object": obj}
    # return render(request, template_name, context)


#GET -> retrieve/ List
#POST -> Create / Update / DELETE
#CRUD

def blog_post_list_view(request):
    # list out objects
    # could be search
    #qs = BlogPost.objects.filter(title__icontains='hello') 
    qs = BlogPost.objects.all().published() #queryet -> list of python object
    template_name = 'blog/list.html'
    context = {"object_list": qs}
    return render(request, template_name, context)

#@login_required()
@staff_member_required
def blog_post_create_view(request):
    # create objects
    # use a form
    # form = BlogPostForm(request.POST or None)
    # if form.is_valid():
    #     print(form.cleaned_data)
    #     obj = BlogPost.objects.create(**form.cleaned_data)
    #     form = BlogPostForm()
    # if not request.user.is_authenticated:
    #     return render(request, "not-a-user.html", context)
    form = BlogPostModlelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        # form.save()
        obj = form.save(commit=False)
        #obj.title = form.cleaned_data.get("title") + "0"
        obj.user = request.user
        obj.save()
        form = BlogPostModlelForm()
    template_name  = 'blog/form.html'
    context = {'form': form}
    return render(request, template_name, context)

def blog_post_detail_view(request, slug):
    # 1 object -> detail view
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = 'blog/detail.html'
    context = {"object": obj}
    return render(request, template_name, context)

@staff_member_required
def blog_post_update_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    print(obj)
    form = BlogPostModlelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
    template_name = 'form.html'
    context = {"title": f"Update {obj.title}", "form": form}
    return render(request, template_name, context) 

@staff_member_required
def blog_post_delete_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = 'blog/delete.html'
    if request.method == "POST":
        obj.delete()
        return redirect("/blog")
    context = {"object": obj}
    return render(request, template_name, context)
