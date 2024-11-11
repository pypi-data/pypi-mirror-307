from django.contrib.auth import get_user_model
from .jwt_auth import parse_payload
import json

User = get_user_model()


class CorePermission:
    def has_permission(self, request, view) -> bool:
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        elif request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            if request.user:
                user_permission = json.loads(request.auth.user_permission)
                if request.path in user_permission:
                    return True
                else:
                    return False
            return True
        return False
        # return bool(request.user and request.user.is_authenticated)