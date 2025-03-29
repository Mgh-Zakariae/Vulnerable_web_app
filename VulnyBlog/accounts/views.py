import re
from django.shortcuts import redirect, render
from .forms import registerUser, loginUser
from .models import User
from django.contrib.auth.hashers import check_password, make_password
from django.core.validators import validate_email #############
from django.core.exceptions import ValidationError

from django.contrib import messages
# Create your views here.

def is_valid_password(password):
    min_length = 8
    uppercase_pattern = re.compile(r'[A-Z]')
    lowercase_pattern = re.compile(r'[a-z]')
    digit_pattern = re.compile(r'\d')
    special_char_pattern = re.compile(r'[!@#$%^&*()]')

    if len(password) < min_length:
        return False, "Password must be at least 8 characters long."
    if not uppercase_pattern.search(password):
        return False, "Password must contain at least one uppercase letter."
    if not lowercase_pattern.search(password):
        return False, "Password must contain at least one lowercase letter."
    if not digit_pattern.search(password):
        return False, "Password must contain at least one digit."
    if not special_char_pattern.search(password):
        return False, "Password must contain at least one special character (e.g., !@#$%^&*())."

    return True, "Password is valid."

def register_user(req):
    if req.method == 'POST':
        form = registerUser(req.POST)
        email=req.POST['email']
        name=req.POST['username']
        passwd = req.POST['password']
        password=make_password(req.POST['password'])
        if form.is_valid():
            valid, message = is_valid_password(passwd)
            try:
                validate_email(email)
                #chech if password is valid
                if not valid:
                    messages.error(req, message)
                else:
                    checkUserEmail = User.objects.filter(email=email).exists()
                    checkUserName = User.objects.filter(username=name).exists()
                    if checkUserEmail or checkUserName :
                        messages.error(req, 'Username or email already exist')
                    else:
                        User.objects.create(username=name, email=email, password=password)
                        return redirect('login')
            except ValidationError:
                messages.error(req, 'email not valid')
            
    return render(req, 'registration/register.html', {'form': registerUser})


def login_user(req):
    if req.method == 'POST':
        form = loginUser(req.POST)
        name = req.POST['username']
        password = req.POST['password']           

        if form.is_valid():
            
            try:
                try:
                    validate_email(name)
                    user = User.objects.get(email=name)
                except ValidationError:
                    user = User.objects.get(username=name)
                if check_password(password, user.password):
                    # Store user info in session
                    req.session['user_id'] = user.id
                    req.session['isAdmin'] = user.is_admin
                    req.session['username'] = user.username
                    req.session['email'] = user.email
                    req.session['is_authenticated'] = True
                    return redirect('posts')
                else:
                    messages.error(req, 'Incorrect password')
            except User.DoesNotExist:
                messages.error(req, 'Username not found')
            
    return render(req, 'registration/login.html', {'form': loginUser()})


def logout_user(req):
    print('Logging out...')
    # Clear session data
    req.session.flush()
    # Redirect to posts or home page
    return redirect('posts')

