from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template

from .forms import ContactForm
from blog.models import BlogPost

def home_page(request):
    my_title = "Hello there.."
    qs = BlogPost.objects.all()[:5]
    context = {"title": "Welcome to Try Django", 'blog_list':qs}
    # if request.user.is_authenticated:
    #      context  = {"title": my_title, "my_list": [1,2,3,4,5]}
    return render(request, "home.html", context)


def about_page(request):
    #return HttpResponse("<h1>This is about page</h1>")
    return render(request, "about.html", {"title": "About us"})


def contact_page(request):
    #return HttpResponse("<h1>This is contact page</h1>")
    #print(request.POST)
    form = ContactForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        form = ContactForm()
    context = {
        "title": "Contact", 
        "form":form
        }
    return render(request, "form.html", context)

#Rendering Any Kind of Template
def example_page(request):
    context = {"title": "Example"}
    template_name = "hello_world.html"
    template_obj = get_template(template_name)
    render_item = template_obj.render(context)
    return HttpResponse(render_item)