from django.contrib.auth.decorators import login_required

def custom_app_labels(request):
    if request.user.is_authenticated:
        if request.user.is_superadmin:
            return {"custom_labels": {"main": "Manage Users"}}
        elif request.user.is_admin:
            return {"custom_labels": {"main": "User Administration"}}
    return {"custom_labels": {}}
