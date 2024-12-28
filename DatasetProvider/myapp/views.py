import re
from django.shortcuts import render
from crewai import Crew
from .agents import dataset_provider_agent
from .tasks import dataset_provider
from crewai import Process
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse

from django.shortcuts import render,HttpResponseRedirect,redirect
import re


def index(request):
    # Get the username from the session
    username = request.session.get('username', '')
    if not username:
        return redirect('signin')  # Redirect to the signin URL or name
    # Get the query parameter from the request
    query = request.GET.get('query', '')
    # Get the last query from the session
    last_query = request.session.get('last_query', '')
    # If there is a query, process it
    if query and query != last_query:
        # Store the current query in the session
        request.session['last_query'] = query
        crew = Crew(
            agents=[dataset_provider_agent],
            tasks=[dataset_provider],
            process=Process.sequential,
        )

        # Use the query as input
        result = crew.kickoff(inputs={'input': query})

        # Extract the 'raw' content from the task output
        raw_text = None
        for item in result:
            if item[0] == 'raw':
                raw_text = item[1]
                break

        # Find all URLs in the raw text
        links = re.findall(r'(https?://\S+)', raw_text)

        return render(request, 'index.html', {'links': links, 'username': username})

    # If no query, just render the index page
    return render(request, 'index.html', {'username': username})


def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)
        user = User.objects.create_user(username=name, email=email, password=password)
        user.save()

        # # Sending welcome email
        # subject = 'Welcome to Your Personal Chatbot'
        # html_message = render_to_string('testapp/welcome_email.html', {'name': name})
        # plain_message = strip_tags(html_message)
        # from_email = 'personalchatbot911@gmail.com'  # Update with your email
        # to_email = [email]
        # send_mail(subject, plain_message, from_email, to_email, html_message=html_message,fail_silently=False)
        #
        return HttpResponseRedirect('http://192.168.1.5:8000/signin/')
    return render(request, 'signup.html')


from django.contrib.auth import login


def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Authentication successful
            user = form.get_user()
            username = user.username

            # Store the username in the session
            request.session['username'] = username

            # Log the user in
            login(request, user)

            # Redirect to the desired URL after successful login
            return redirect('index')
        else:
            print(form.errors)  # Print form errors for debugging

    # Render the login form
    form = AuthenticationForm()
    return render(request, 'signin.html', {'form': form})

def landing(request):
    return render(request,'landing.html')