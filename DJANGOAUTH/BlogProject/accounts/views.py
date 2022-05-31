from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render, resolve_url
from .forms import UserForm, UserFormLogin

from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth import authenticate, login

from django.contrib.contenttypes.models import ContentType
import blog.models as m


# Create your views here.


def register_user(request: HttpRequest):
    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            new_user = User.objects.create_user(user_form.cleaned_data["username"], user_form.cleaned_data["email"],
                                                user_form.cleaned_data["password"])
            new_user.save()

            return redirect(resolve_url('blog:index'))

    return render(request, 'accounts/register.html', {'form': UserForm()})


def login_user(request: HttpRequest):
    if request.method == 'POST':
        user_form = UserFormLogin(request.POST)

        if user_form.is_valid():

            username = user_form.cleaned_data["username"]
            password = user_form.cleaned_data["password"]

            authenticate_user = authenticate(request, username=username, password=password)

            if authenticate_user is not None:
                login(request, authenticate_user)
                return redirect(resolve_url('blog:index'))
            else:
                return redirect(resolve_url('accounts:login'))

    return render(request, 'accounts/login.html', {'form': UserFormLogin()})


def add_blog_permission(requst: HttpRequest):
    if not requst.user.has_perm("blog.add_blog"):
        contentType = ContentType.objects.get_for_model(m.Post)
        permission = Permission.objects.get(codename="add_blog", content_type=contentType)
        requst.user.user_permissions.add(permission)

    return HttpResponse("The permission is added")


def add_to_group_editors(request: HttpRequest):
    if not request.user.groups.filter(name="editors").exists():
        group = Group.objects.get(name="editors")
        request.user.groups.add(group)

    return HttpResponse("Added successfully")
