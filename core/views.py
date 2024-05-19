from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Chatbot, QuestionAnswer
from django.shortcuts import render
from .qdrant_client.qdrant_utils import create_vector_collection, get_answer
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from .forms import ChatbotCreationForm 
import pandas as pd
import os
from uuid import uuid4
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404


def chat_view(request, chatbot_id):
    chatbot = get_object_or_404(Chatbot, pk=chatbot_id)
    context = {'chatbot': chatbot}
    return render(request, 'chat.html', context)

def login_(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to the chatbot page
            return redirect("chatbot_page")  # Replace 'chatbot_page' with your URL name for the chatbot page
        else:
            # Redirect back to login page on authentication failure
            return redirect("login")
    else:
        form = AuthenticationForm()
        return render(request, 'login_form.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after signup
            # Redirect to some page after successful signup
            return redirect('home')  # Replace 'home' with your desired URL name
    else:
        form = UserCreationForm()
    return render(request, 'form_view.html', {'form': form})


def logout_(request):
    logout(request)
    return redirect("login")

@login_required
def chatbots_page(request):
    # Assuming 'user_id' is the field in the Chatbot model representing the user's ID
    chatbots = Chatbot.objects.filter(user_id=request.user.id)
    return render(request, 'chatbot_page.html', {'chatbots': chatbots})

def view_chatbot(request):
    # coming from the chatbots_page
    pass

def handle_uploaded_file(f):
    ext = f.name.split(".")[-1]
    filepath = f'upload_dir/{str(uuid4())}.{ext}'   
    with open(filepath, 'wb+') as destination:
        for chunk in f.chunks(): 
            destination.write(chunk)   
    return filepath

@login_required
def create_chatbot(request):
    if request.method == 'POST':
        filename = handle_uploaded_file(request.FILES.get('csv_file'))
        if filename.endswith(".csv"):
            df = pd.read_csv(filename)
        else:
            df = pd.read_excel(filename)
        questions = [str(q) for q in df.Question]
        answers = [str(a) for a in df.Answer]
        os.remove(filename)
        collection_id = create_vector_collection(questions, answers)
        key = (str(uuid4())).replace('-', '')
        chatbot = Chatbot.objects.create(
            name = request.POST["name"],
            key = key,
            collection_id = collection_id,
            user_id = request.user.id,
        )
        questions_answers_objs = [
            QuestionAnswer(
                chatbot_id = chatbot.id,
                question = question,
                answer = answer
            )
            for question, answer in zip(questions, answers)
        ]
        QuestionAnswer.objects.bulk_create(
            questions_answers_objs
        )
        return redirect("chatbot_page")
    else:
        form = ChatbotCreationForm()
        return render(request, 'create_chatbot.html', {"form" : form})

def create_chatbot_collection(request, chatbot_id):
    chatbot = Chatbot.objects.get(id=chatbot_id)
    questions = [qa.question for qa in chatbot.question_answers.all()]
    answers = [qa.answer for qa in chatbot.question_answers.all()]
    collection_name = create_vector_collection(questions, answers)
    # store information in the database
    return JsonResponse({'collection_name': collection_name})

@csrf_exempt
def chatbot_answer(request):
    if request.method == 'POST':
        collection_name = request.POST.get('collection_name')
        question = request.POST.get('question')
        answer = get_answer(collection_name, question)
        return JsonResponse({'answer': answer})
    else:

        return JsonResponse({'error': 'Invalid request method'})