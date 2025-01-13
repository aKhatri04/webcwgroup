import json
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, LoginForm
from.models import Hobby, CustomUser, UserHobby, FriendRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST



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

@login_required
@require_POST
def send_friend_request(request: HttpRequest) -> JsonResponse:
    """
    Sends a friend request from the logged-in user to another user.

    Request body:
        - to_user_id (int): The ID of the user to whom the request is being sent.
    """
    try:
        data = json.loads(request.body)
        to_user = CustomUser.objects.get(id=data['to_user_id'])
        from_user = request.user

        # Check if the request already exists
        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            return JsonResponse({'error': 'Friend request already sent'}, status=400)

        # Create the friend request
        friend_request = FriendRequest.objects.create(from_user=from_user, to_user=to_user)
        return JsonResponse(friend_request.as_dict(), status=201)

    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except KeyError:
        return JsonResponse({'error': 'Invalid request payload'}, status=400)
@login_required
def view_friend_requests(request: HttpRequest) -> JsonResponse:
    """
    Returns all pending friend requests for the logged-in user.
    """
    pending_requests = FriendRequest.objects.filter(to_user=request.user, is_accepted=False)
    return JsonResponse({
        "pending_requests": [fr.as_dict() for fr in pending_requests]
    })
@login_required
@require_POST
def handle_friend_request(request: HttpRequest) -> JsonResponse:
    """
    Accepts or rejects a friend request.

    Request body:
        - request_id (int): The ID of the friend request.
        - action (str): 'accept' or 'reject'.
    """
    try:
        data = json.loads(request.body)
        friend_request = FriendRequest.objects.get(id=data['request_id'], to_user=request.user)

        if data['action'] == 'accept':
            # Accept the request
            friend_request.is_accepted = True
            friend_request.save()

            # Add mutual friendship
            friend_request.from_user.friends.add(friend_request.to_user)
            friend_request.to_user.friends.add(friend_request.from_user)

            return JsonResponse({'success': 'Friend request accepted'}, status=200)

        elif data['action'] == 'reject':
            # Reject the request
            friend_request.delete()
            return JsonResponse({'success': 'Friend request rejected'}, status=200)

        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)

    except FriendRequest.DoesNotExist:
        return JsonResponse({'error': 'Friend request not found'}, status=404)
    except KeyError:
        return JsonResponse({'error': 'Invalid request payload'}, status=400)
