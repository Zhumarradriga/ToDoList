from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


from .forms import CustomRegisterForm, CustomLoginForm
from .models import CustomUser


# Create your views here.
def register_view(request):
    if request.method=='POST':
        form=CustomRegisterForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            phone_number=form.cleaned_data['phone_number']
            user=CustomUser.objects.create_user(
                email=email, password=password, first_name=first_name,
                last_name=last_name, phone_number=phone_number
            )
            messages.success(request, f"Аккаунт создан для {email}!")
            return redirect("login")
    else:
        form=CustomRegisterForm()
    return render(request,'ToDoAuth/register.html', {'form': form})
def login_view(request):
    if request.method=="POST":
        form=CustomLoginForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            user=authenticate(request,email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request,f"Добро пожаловать, {user.email}!")
                return  redirect("base")
            else:
                messages.error(request, 'Неверный email  или пароль.')
    else:
        form=CustomLoginForm()
    return  render(request,'ToDoAuth/login.html', {'form': form})
def logout_view(request):
    logout(request)
    messages.info(request, "Вы вышли из системы")
    return redirect('login')
def home_view(request):
    return render(request,"ToDoAuth/home.html", {'user': request.user})