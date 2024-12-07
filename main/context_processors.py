from django.contrib.auth.decorators import login_required

def custom_app_labels(request):
    """
    Customize app labels based on user role.
    """
    if request.user.is_authenticated and request.user.is_superadmin:
        return {"custom_labels": {"main": "Manage Users"}}
    return {"custom_labels": {}}
