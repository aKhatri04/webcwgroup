import json
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from .models import Hobby, CustomUser, UserHobby
from django.core.paginator import Paginator
from datetime import date
from django.db.models import F, Count, Q
from collections import defaultdict


def main_spa(request: HttpRequest) -> HttpResponse:
    """
    Render the main Single Page Application (SPA).
    """
    return render(request, 'api/spa/index.html', {})


# Hobby API
def hobbies_api(request):
    """
    Handles CRUD operations for hobbies.
    """
    if request.method == "POST":
        try:
            POST = json.loads(request.body)
            hobby = Hobby.objects.create(name=POST["name"])
            return JsonResponse(hobby.as_dict())
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({
        "hobbies": [hobby.as_dict() for hobby in Hobby.objects.all()]
    })


def hobby_api(request, hobby_id):
    """
    Handles GET, PUT, and DELETE requests for a specific hobby.
    """
    try:
        hobby = Hobby.objects.get(id=hobby_id)
    except Hobby.DoesNotExist:
        return JsonResponse({"message": "Hobby not found"}, status=404)

    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            hobby.name = data.get("name", hobby.name)
            hobby.save()
            return JsonResponse(hobby.as_dict())
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    if request.method == "DELETE":
        hobby.delete()
        return JsonResponse({"message": "Hobby deleted"})

    return JsonResponse(hobby.as_dict())


# User API
def users_api(request):
    """
    API to fetch paginated users and group them by hobbies.
    """
    try:
        # Query parameters
        age_min = int(request.GET.get("age_min", 0))
        age_max = int(request.GET.get("age_max", 120))
        page_number = int(request.GET.get("page", 1))

        # Get all users and filter by age
        today = date.today()
        users = CustomUser.objects.annotate(
            age=today.year - F("date_of_birth__year"),
            common_hobbies=Count("hobbies", filter=Q(hobbies__in=CustomUser.objects.get(id=request.GET.get("current_user_id")).hobbies.all())),
        ).filter(
            age__gte=age_min,
            age__lte=age_max,
        ).order_by("-common_hobbies")

        # Apply pagination
        paginator = Paginator(users, 10)
        page_obj = paginator.get_page(page_number)

        return JsonResponse({
            "users": [
                {
                    **user.as_dict(),
                    "common_hobbies": user.common_hobbies  # Include shared hobbies count
                }
                for user in page_obj.object_list
            ],
            "total_pages": paginator.num_pages,
            "current_page": page_obj.number,
            "total_users": paginator.count,
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def user_api(request, user_id):
    """
    Handles GET, PUT, and DELETE requests for a specific user.
    """
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return JsonResponse({"message": "User not found"}, status=404)

    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            user.username = data.get("username", user.username)
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
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    if request.method == "DELETE":
        user.delete()
        return JsonResponse({"message": "User deleted"})

    return JsonResponse(user.as_dict())


# User-Hobby API
def user_hobbies_api(request):
    """
    Handles POST requests for associating hobbies with a user.
    """
    if request.method == "POST":
        try:
            POST = json.loads(request.body)
            hobby = Hobby.objects.get(id=POST["hobby_id"])
            user = CustomUser.objects.get(id=POST["user_id"])

            user_hobby = UserHobby.objects.create(hobby=hobby, user=user)
            return JsonResponse(user_hobby.as_dict())
        except Hobby.DoesNotExist:
            return JsonResponse({"message": "Hobby not found"}, status=404)
        except CustomUser.DoesNotExist:
            return JsonResponse({"message": "User not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({
        "user_hobbies": [
            user_hobby.as_dict() for user_hobby in UserHobby.objects.all()
        ]
    })


def user_hobby_api(request, user_hobby_id):
    """
    Handles GET, PUT, and DELETE requests for a specific user-hobby relationship.
    """
    try:
        user_hobby = UserHobby.objects.get(id=user_hobby_id)
    except UserHobby.DoesNotExist:
        return JsonResponse({"message": "User-Hobby not found"}, status=404)

    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            user_hobby.hobby = Hobby.objects.get(id=data["hobby_id"])
            user_hobby.user = CustomUser.objects.get(id=data["user_id"])
            user_hobby.save()
            return JsonResponse(user_hobby.as_dict())
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    if request.method == "DELETE":
        user_hobby.delete()
        return JsonResponse({"message": "User-Hobby deleted"})

    return JsonResponse(user_hobby.as_dict())
