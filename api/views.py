import json
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, LoginForm

from.models import Hobby, CustomUser, UserHobby, FriendRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt



from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token

User = get_user_model()

# Home page
def index(request):
    return render(request, 'api/spa/index.html')



def csrf_token_view(request):
    return JsonResponse({"csrfToken": get_token(request)})

def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})

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

#Hobby API

# Hobbies API: Fetch all hobbies or add a new hobby
@login_required
@csrf_exempt
def hobbies_api(request: HttpRequest) -> JsonResponse:
    """
    Handles fetching all hobbies or creating a new hobby.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            hobby, created = Hobby.objects.get_or_create(name=data["name"].strip())
            return JsonResponse(hobby.as_dict(), status=201 if created else 200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    hobbies = [hobby.as_dict() for hobby in Hobby.objects.all()]
    return JsonResponse({"hobbies": hobbies})
@csrf_exempt
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
            hobby.name = data.get["name", hobby.name]
            hobby.save()
            return JsonResponse(hobby.as_dict())
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
    if request.method == "DELETE":
        hobby.delete()
        return JsonResponse({"message": "Hobby deleted"})
    
    return JsonResponse(hobby.as_dict())

#User API
@csrf_exempt
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
    
@csrf_exempt
@login_required
def user_api(request: HttpRequest, user_id: int) -> JsonResponse:
    """
    Handles fetching, updating, or deleting a user profile.
    """
    try:
        user = CustomUser.objects.get(id=user_id)

        if request.method == "PUT":
            data = json.loads(request.body)
            user.name = data.get("name", user.name)
            user.email = data.get("email", user.email)
            user.date_of_birth = data.get("date_of_birth", user.date_of_birth)

            if "password" in data and data["password"]:
                user.set_password(data["password"])

            user.save()

            if "hobbies" in data:
                user.userhobby_set.all().delete()
                for hobby_data in data["hobbies"]:
                    hobby, _ = Hobby.objects.get_or_create(name=hobby_data["name"])
                    UserHobby.objects.create(user=user, hobby=hobby)

            return JsonResponse(user.as_dict())

        if request.method == "DELETE":
            user.delete()
            return JsonResponse({"message": "User deleted"}, status=200)

        return JsonResponse(user.as_dict())

    except CustomUser.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
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
            user_hobby.hobby = Hobby.objects.get(id=data.get("hobby", user_hobby.hobby_id))["hobby_id"]
            user_hobby.user = data.get["user", user_hobby.user]
            user_hobby.save()
            return JsonResponse(user_hobby.as_dict())
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
    if request.method == "DELETE":
        user_hobby.delete()
        return JsonResponse({"message": "User-Hobby deleted"})
    
    return JsonResponse(user_hobby.as_dict())


@csrf_exempt
@login_required
@require_POST
def send_friend_request(request):
    """
    Sends a friend request from the logged-in user to another user by username.
    """
    try:
        data = json.loads(request.body)
        to_username = data.get('to_username')
        if not to_username:
            return JsonResponse({'error': 'Username is required'}, status=400)

        try:
            to_user = CustomUser.objects.get(username=to_username)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        from_user = request.user

        # Check if the users are already friends
        if FriendRequest.objects.filter(
            from_user=from_user, to_user=to_user, is_accepted=True
        ).exists() or FriendRequest.objects.filter(
            from_user=to_user, to_user=from_user, is_accepted=True
        ).exists():
            return JsonResponse({'message': 'You are already friends with this user'}, status=400)

        # Check if a pending request already exists
        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user, is_accepted=False).exists():
            return JsonResponse({'error': 'Friend request already sent'}, status=400)

        # Create the friend request
        friend_request = FriendRequest.objects.create(from_user=from_user, to_user=to_user)
        return JsonResponse(friend_request.as_dict(), status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request payload'}, status=400)
@login_required
def view_friend_requests(request):
    """
    Returns all pending friend requests for the logged-in user.
    """
    # Fetch all pending friend requests where the logged-in user is the recipient
    pending_requests = FriendRequest.objects.filter(to_user=request.user, is_accepted=False)

    # Serialize the data
    data = {
        "pending_requests": [fr.as_dict() for fr in pending_requests]
    }

    # Log for debugging
    print("Logged-in user:", request.user.username)
    print("Pending FriendRequests Queryset:", pending_requests)
    print("Serialized Data:", data)

    return JsonResponse(data, status=200)

@csrf_exempt
@login_required
@require_POST
def handle_friend_request(request: HttpRequest) -> JsonResponse:
    """
    Handles accepting or rejecting a friend request and returns updated pending requests.
    """
    try:
        data = json.loads(request.body)
        friend_request = FriendRequest.objects.get(id=data['request_id'], to_user=request.user)

        if data['action'] == 'accept':
            friend_request.is_accepted = True
            friend_request.save()
        elif data['action'] == 'reject':
            friend_request.delete()
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)

        # Return the updated pending requests
        pending_requests = FriendRequest.objects.filter(to_user=request.user, is_accepted=False)
        return JsonResponse({
            "pending_requests": [req.as_dict() for req in pending_requests]
        }, status=200)

    except FriendRequest.DoesNotExist:
        return JsonResponse({'error': 'Friend request not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

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
        # Add hobbies to the user data
        hobbies = [{"id": hobby.id, "name": hobby.name} for hobby in user.hobbies.all()]
        user_data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "date_of_birth": str(user.date_of_birth),
            "hobbies": hobbies  # Include hobbies in the response
        }
        return JsonResponse(user_data)

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

            # Return the updated user data with hobbies
            hobbies = [{"id": hobby.id, "name": hobby.name} for hobby in user.hobbies.all()]
            updated_user_data = {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "date_of_birth": str(user.date_of_birth),
                "hobbies": hobbies
            }

            return JsonResponse(updated_user_data)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    # Handles DELETE request to delete the current user
    if request.method == "DELETE":
        user.delete()
        return JsonResponse({"message": "User deleted"})

    return JsonResponse({"message": "Unsupported request method"}, status=405)

