# users/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomRegisterForm  # <-- import your custom form

def register(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created! You can login now.')
            return redirect('login')
    else:
        form = CustomRegisterForm()
    return render(request, 'users/register.html', {'form': form})
