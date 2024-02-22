from django.shortcuts import render, get_object_or_404, redirect
from .models import CustomUser as User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum



@login_required(login_url='/user/login/')
def index(request):
    """ Dashbord Page."""
    context = {}
    context["users"] = User.objects.filter(is_active=True).count()
    
    return render(request, 'user/index.html', context)


def admin_login(request):
    """ Admin Login Method. """
    message = None
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email, is_staff=True)
        except:
            user = None
        if user:
            if user.check_password(password):
                login(request, user)
                next = request.GET.get('next', None)
                if next:
                    return redirect(next)
                return redirect('index')
        message = "Invalid Credentials."
    return render(request, 'user/login.html', {'message': message})


@login_required
def user_logout(request):
    """ Logout method for users"""
    logout(request)
    return redirect('login')


@login_required
def user_list(request):
    """ All Customers Listing. """
    context = {
        'title': "Users",
        'users': User.objects.filter(is_staff=False)
    }
    return render(request, 'user/list.html', context)

