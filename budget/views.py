from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


mock_projects = [
    {"id": 1, "title": "Yol qurilishi", "region": "Toshkent shahri", "district": "Chilonzor", "budget": 500000000, "description": "Chilonzor tumanidagi yo'l qurilishi loyihasi."},
    {"id": 2, "title": "Maktab qurilishi", "region": "Andijon viloyati", "district": "Andijon shahri", "budget": 300000000, "description": "Andijon shahrida yangi maktab qurilishi."},
    {"id": 3, "title": "Park rekonstruksiyasi", "region": "Samarqand viloyati", "district": "Samarqand shahri", "budget": 200000000, "description": "Samarqand shahridagi parkni yangilash."},
]

def index(request):
    selected_region = request.GET.get('region', 'all')
    selected_district = request.GET.get('district', '')
    filtered_projects = mock_projects
    if selected_region != 'all':
        filtered_projects = [p for p in filtered_projects if p['region'] == selected_region]
        if selected_district:
            filtered_projects = [p for p in filtered_projects if p['district'] == selected_district]

    context = {
        'projects': filtered_projects,
        'selected_region': selected_region,
        'selected_district': selected_district,
    }
    return render(request, 'index.html', context)

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        region = request.POST.get('region')
        district = request.POST.get('district')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone = request.POST.get('phone')
        card = request.POST.get('card')

        if password != confirm_password:
            messages.error(request, "Parollar mos kelmadi!")
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Bu login band!")
            return render(request, 'register.html')

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name
        )
        user.save()
        messages.success(request, "Ro'yxatdan o'tish muvaffaqiyatli!")
        return redirect('login')
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Tizimga muvaffaqiyatli kirdingiz!")
            if user.is_staff:
                return redirect('admin_page')
            else:
                return redirect('tuman')
        else:
            messages.error(request, "Login yoki parol xato!")
            return render(request, 'login.html')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Tizimdan chiqdingiz!")
    return redirect('login')

def detail(request, project_id):
    project = next((p for p in mock_projects if p['id'] == int(project_id)), None)
    if not project:
        messages.error(request, "Loyiha topilmadi!")
        return redirect('index')
    return render(request, 'detail.html', {'project': project})

def feedback(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f"Fikr-mulohaza: {name}, {email}, {message}")
        messages.success(request, "Fikr-mulohazangiz qabul qilindi!")
        return redirect('index')
    return render(request, 'feedback.html')

@login_required
def admin_page(request):
    if not request.user.is_staff:
        messages.error(request, "Sizda bu sahifaga kirish huquqi yo'q!")
        return redirect('index')
    return render(request, 'admin.html', {'projects': mock_projects})

@login_required
def tuman(request):
    user_region = "Toshkent shahri" 
    user_district = "Chilonzor" 
    projects = [p for p in mock_projects if p['region'] == user_region and p['district'] == user_district]
    return render(request, 'tuman.html', {'projects': projects})

@login_required
def user_page(request):
    user_projects = mock_projects
    return render(request, 'user.html', {'projects': user_projects})