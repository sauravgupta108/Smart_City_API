from ..models import Administration as admn

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
        
    