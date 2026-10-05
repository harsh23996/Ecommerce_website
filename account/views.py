from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.models import User

# ───────────────────── LOGIN ──────────────────────
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'home_page')  # smart redirect
            return redirect(next_url)
        else:
            return render(request, 'login.html', {
                'error': 'Invalid credentials'
            })

    return render(request, 'login.html')

# ───────────────────── LOGOUT ─────────────────────
def logout_view(request):
    logout(request)                 # logs out on any request (GET/POST)
    return redirect('home_page')


# ─────────────────── REGISTER ─────────────────────
def register_view(request):
    if request.method == 'POST':
        username          = request.POST.get('username')
        password          = request.POST.get('password')
        confirm_password  = request.POST.get('confirm_password')
        email             = request.POST.get('email')

        if password != confirm_password:
            return render(request, 'register.html',
                          {'error': 'Passwords do not match'})

        # Optional: check if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html',
                          {'error': 'Username already taken'})

        # Create user then redirect
        User.objects.create_user(username=username,
                                 password=password,
                                 email=email)
        return redirect('login')             # ✅ use URL‑name

    # GET request → blank form
    return render(request, 'register.html')
