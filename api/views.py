import json
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, LoginForm
from.models import Hobby, CustomUser, UserHobby



from django.contrib.auth import get_user_model

User = get_user_model()

# Home page
def index(request):
    return render(request, 'api/spa/index.html')

# signup page
def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'api/spa/signup.html', {'form': form})

# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect(main_spa)
    else:
        form = LoginForm()
    return render(request, 'api/spa/login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return redirect('login')

def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})

#Hobby API
def hobbies_api(request):
    """
    Handles POST request for managing hobby.
    """  
    if request.method == "POST": 
        POST = json.loads(request.body)
        hobby = Hobby.objects.create(
            name = POST['name']
        )
        return JsonResponse(hobby.as_dict())
    
    return JsonResponse({
        "hobbies": [
            hobby.as_dict() 
            for hobby in Hobby.objects.all()
            ]
    })
    

def hobby_api(request,hobby_id):
    #check if hobby exists GET
    try:
        hobby =  Hobby.objects.get(id=hobby_id)
    except Hobby.DoesNotExist:
        return JsonResponse({"message": "Hobby not found"}, status=404)
    
    #handles PUT, DELETE requests, update details and delete requests
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            hobby.name = data["name", hobby.name]
            hobby.save()
            return JsonResponse(hobby.as_dict())
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
    if request.method == "DELETE":
        hobby.delete()
        return JsonResponse({"message": "Hobby deleted"})
    
    return JsonResponse(hobby.as_dict())

#User API

def users_api(request):
    if request.method == "POST":
        POST = json.loads(request.body)
        user = CustomUser.objects.create(
            username = POST['username'],
            name = POST['name'],
            email = POST['email'],
            date_of_birth = POST['date_of_birth'],
            password = POST['password']
        )
        return JsonResponse(user.as_dict())
    
    return JsonResponse({
        "users": [
            user.as_dict() 
            for user in CustomUser.objects.all()
            ]
    })
    

def user_api(request,user_id):
    #check if user exists GET
    try:
        user =  CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return JsonResponse({"message": "User not found"}, status=404)
    
    #handles PUT, DELETE requests, update details and delete requests
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            user.username = data["username", user.username]
            user.name = data["name", user.name]
            user.email = data["email", user.email]
            user.date_of_birth = data["date_of_birth", user.date_of_birth]

            
            if 'password' in data and data['password']:
                user.set_password(data['password'])
                
            user.save()
            
            if 'hobbies' in data:
                # Clear existing hobbies and add new ones
                user.userhobby_set.all().delete()
                for hobby_data in data['hobbies']:
                    hobby, _ = Hobby.objects.get_or_create(name=hobby_data['name'])
                    UserHobby.objects.create(user=user, hobby=hobby)

            return JsonResponse(user.as_dict())
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
        
    if request.method == "DELETE":
        user.delete()
        return JsonResponse({"message": "User deleted"})
    
    return JsonResponse(user.as_dict())


#User-Hobby API through model

def user_hobbies_api(request):
    if request.method == "POST":
        POST = json.loads(request.body) #get info for request
        try:
            hobby = Hobby.objects.get(id=POST['hobby_id'])
            user = CustomUser.objects.get(id=POST['user_id'])
            
        except Hobby.DoesNotExist:
            return JsonResponse({"message": "Hobby not found"}, status=404)
        except CustomUser.DoesNotExist: 
            return JsonResponse({"message": "User not found"}, status=404)
        
        user_hobby = UserHobby.objects.create(
        hobby = hobby,
        user = user,
        )
        return JsonResponse(user_hobby.as_dict())
    
    return JsonResponse({
        "user_hobbies": [
            user_hobby.as_dict() 
            for user_hobby in UserHobby.objects.all()
            ]
    })
 

def user_hobby_api(request, user_hobby_id):
    #check if user_hobby exists GET
    try:
        user_hobby =  UserHobby.objects.get(id=user_hobby_id)
    except UserHobby.DoesNotExist:
        return JsonResponse({"message": "User-Hobby not found"}, status=404)
    
    #handles PUT, DELETE requests, update details and delete requests
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            user_hobby.hobby = data["hobby", user_hobby.hobby]
            user_hobby.user = data["user", user_hobby.user]
            user_hobby.save()
            return JsonResponse(user_hobby.as_dict())
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
    if request.method == "DELETE":
        user_hobby.delete()
        return JsonResponse({"message": "User-Hobby deleted"})
    
    return JsonResponse(user_hobby.as_dict())

from django.contrib.auth.decorators import login_required


@login_required
def current_user_api(request):
    # Check if the user is authenticated
    try:
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({"message": "User is not authenticated"}, status=403)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    # Handles GET request to fetch current user data
    if request.method == "GET":
        return JsonResponse(user.as_dict())

    # Handles PUT request to update the current user's details
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            user.name = data.get("name", user.name)
            user.email = data.get("email", user.email)
            user.date_of_birth = data.get("date_of_birth", user.date_of_birth)

            if "password" in data and data["password"]:
                user.set_password(data["password"])

            user.save()

            # Handle hobbies if provided
            if "hobbies" in data:
                user.userhobby_set.all().delete()
                for hobby_data in data["hobbies"]:
                    hobby, _ = Hobby.objects.get_or_create(name=hobby_data["name"])
                    UserHobby.objects.create(user=user, hobby=hobby)

            return JsonResponse(user.as_dict())
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    # Handles DELETE request to delete the current user
    if request.method == "DELETE":
        user.delete()
        return JsonResponse({"message": "User deleted"})

    return JsonResponse({"message": "Unsupported request method"}, status=405)
