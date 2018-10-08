from ..models import Administration as admn
from .Key_handler import Key_handler as kh
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

import json


class Validator:
    def are_valid(crdntls):
        try:
            pwd = admn.objects.get(username = crdntls['user_id'])
            role = pwd.designation
            if pwd.password == crdntls['password']:
                del(pwd)
                return [True, role]
            else: return [False, None]
        except: return [False, None]
        
    def has_permission(self, key, client_id, method):
        valid, role = kh().is_valid(key, client_id)
        if valid:
            with open('/opt/app/django/restFulAPI/api_security/security/config/token_config.json','r') as tkconf:
                permission = json.load(tkconf)["permission"][0][role][0][method]
            return bool(int(permission))

        else: return False