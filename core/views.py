from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .models import Project, Client, Contact, Newsletter, HeroSection

from openai import OpenAI
import json

WEBSITE_CONTEXT = """
You are an AI assistant for a professional construction and real estate company named Real Trust.
Your role is to answer user queries strictly based on the company’s services, projects, and construction expertise.

Company Overview:
Real Trust is a full-service construction, real estate, and interior solutions company.
We work as builders, developers, and consultants for residential, commercial, and mixed-use projects.

Core Services:
- Residential building construction (houses, villas, apartments)
- Commercial construction (offices, retail spaces, showrooms)
- Interior design and execution
- Structural design and planning
- Renovation and remodeling
- Turnkey construction solutions
- Real estate investment consultation
- Property marketing and sales strategy

Construction Process:
1. Client consultation and requirement analysis
2. Site evaluation and feasibility study
3. Architectural and structural planning
4. Cost estimation and project timeline
5. Material selection and procurement
6. Construction execution with quality control
7. Interior finishing and final handover

Quality & Standards:
- High-quality materials
- Safety & building regulations
- On-time delivery
- Transparent costing
- Skilled professionals

Goal:
Answer construction, design, cost, timeline, and project-related questions professionally.
"""
def landing_page(request):
    hero = HeroSection.objects.first()
    projects = Project.objects.all()
    clients = Client.objects.all()

    if request.method == "POST":
        if "contact" in request.POST:
            Contact.objects.create(
                full_name=request.POST.get("name"),
                email=request.POST.get("email"),
                mobile=request.POST.get("mobile"),
                city=request.POST.get("city"),
            )

        elif "newsletter" in request.POST:
            Newsletter.objects.create(
                email=request.POST.get("email")
            )

        return redirect("/")

    return render(request, "landing.html", {
        "hero": hero,
        "projects": projects,
        "clients": clients,
    })

def project_detail(request, id):
    project = get_object_or_404(Project, id=id)
    return render(request, "project_detail.html", {"project": project})

def client_detail(request, id):
    client = get_object_or_404(Client, id=id)
    return render(request, "client_detail.html", {"client": client})

client = OpenAI(api_key=settings.OPENAI_API_KEY)

@csrf_exempt
def ai_chat(request):

    # GET request (health check)
    if request.method == "GET":
        return JsonResponse({
            "message": "AI Chat API is running"
        })

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "").strip()

            # Initialize session chat memory
            if "chat_history" not in request.session:
                request.session["chat_history"] = []

            chat_history = request.session["chat_history"]

            # Add user message to memory
            chat_history.append({
                "role": "user",
                "content": user_message
            })

            # Build message payload (limit memory)
            messages = [{"role": "system", "content": WEBSITE_CONTEXT}]
            messages.extend(chat_history[-6:])

            # OpenAI request
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )

            ai_reply = response.choices[0].message.content

            # Save AI reply to memory
            chat_history.append({
                "role": "assistant",
                "content": ai_reply
            })

            request.session["chat_history"] = chat_history

            return JsonResponse({"reply": ai_reply})

        except Exception as e:
            print("AI ERROR:", e)
            return JsonResponse({
                "reply": "AI service error. Please try again later."
            }, status=500)
