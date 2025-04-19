from django.shortcuts import render

# Create your views here.

from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import google.generativeai as genai
import os

from .forms import SignUpForm
from .models import UserProfile

# Configure Gemini API
genai.configure(api_key=os.getenv("AIzaSyBD4Cro38WjxiOkEHh3ryoFxQjANGOPztg"))
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            bio = form.cleaned_data.get('bio')
            UserProfile.objects.create(user=user, bio=bio)
            login(request, user)
            return redirect('therapist')
    else:
        form = SignUpForm()
    return render(request, 'chatapp/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('therapist')
    else:
        form = AuthenticationForm()
    return render(request, 'chatapp/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def therapist_view(request):
    return render(request, 'chatapp/therapist.html')

@login_required
def get_ai_response(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        user_profile = getattr(request.user, 'profile', None)

        # Get user tone if available, else default to gentle
        user_tone = user_profile.therapist_tone if user_profile and hasattr(user_profile, 'therapist_tone') else 'gentle'

        # The system prompt to instruct Gemini
        system_prompt = (
            "You are MAQ, an AI therapist specialized in providing emotional support, therapeutic conversation, "
            "and basic psychiatric advice for users facing mental health challenges. "
            "You were developed and trained by Manzi Comfort, Asingwire Marvellous, and Kabanda Queen Latifah. "
            "The name 'MAQ' comes from the initials: Manzi, Asingwire, and Queen. "
            "You must behave like a compassionate, supportive, and understanding therapist, offering empathetic, non-judgmental advice. "
            "Your language should be professional, warm, and mental-health-focused. "
            f"Maintain a {user_tone} tone in your answers. "
            "Important: MAQ is not a licensed psychiatrist or therapist. If symptoms persist, kindly recommend visiting a qualified mental health professional."
        )

        # Full prompt to send
        full_prompt = system_prompt + "\n\nUser: " + user_message

        try:
            ai_response = model.generate_content(full_prompt).text
        except Exception as e:
            print(e)  # Print error to console for debugging
            ai_response = "I'm having some trouble responding right now. Please try again later."

        return JsonResponse({'response': ai_response})
