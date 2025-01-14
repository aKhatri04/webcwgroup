import json
from django.http import HttpResponse, HttpRequest, JsonResponse
<<<<<<< Updated upstream
from django.shortcuts import render
from.models import Hobby, CustomUser, UserHobby
=======
<<<<<<< Updated upstream
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, LoginForm
from.models import Hobby, CustomUser, UserHobby, FriendRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
=======
from django.shortcuts import render
from.models import Hobby, CustomUser, UserHobby
from django.views.decorators.csrf import csrf_exempt

>>>>>>> Stashed changes
>>>>>>> Stashed changes


def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})

#Hobby API
<<<<<<< Updated upstream
def hobby_api(request):
=======
@csrf_exempt  # Exempt this view from CSRF checks
def hobbies_api(request):
>>>>>>> Stashed changes
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
    
<<<<<<< Updated upstream
=======
<<<<<<< Updated upstream

=======
@csrf_exempt 
>>>>>>> Stashed changes
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
def user_api(request):
=======
<<<<<<< Updated upstream

=======
@csrf_exempt 
>>>>>>> Stashed changes
def users_api(request):
>>>>>>> Stashed changes
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
    
<<<<<<< Updated upstream
=======
<<<<<<< Updated upstream

=======
@csrf_exempt 
>>>>>>> Stashed changes
>>>>>>> Stashed changes
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
            return JsonResponse(user.as_dict())
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
    if request.method == "DELETE":
        user.delete()
        return JsonResponse({"message": "User deleted"})
    
    return JsonResponse(user.as_dict())

<<<<<<< Updated upstream
=======
<<<<<<< Updated upstream

=======
@csrf_exempt 
>>>>>>> Stashed changes
>>>>>>> Stashed changes
#User-Hobby API through model

def user_hobby_api(request):
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
<<<<<<< Updated upstream
    
=======
 
<<<<<<< Updated upstream

=======
@csrf_exempt    
>>>>>>> Stashed changes
>>>>>>> Stashed changes
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