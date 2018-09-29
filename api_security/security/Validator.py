from ..models import Administration as admn
from django.core.exceptions import ObjectDoesNotExist, MultipleOgjectsReturned

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
        
    def is_valid_user(self, user_id):
        try:
            user_secret_key = admn.objects.get(username = user_id).secret_key
            return (True, user_secret_key)
        except (ObjectDoesNotExist, MultipleOgjectsReturned) as err:
            return (False, None)