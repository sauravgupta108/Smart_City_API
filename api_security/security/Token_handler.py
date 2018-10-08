from datetime import datetime as dt
from .. import models as mdl
from django.db import transaction as trsxn
from .Key_handler import Key_handler as kh
import base64, json, time
import threading as thrd

class Token_handler:
    def generate_token(self, user_id, role):
        curr_dt = dt.now()

        self.user = user_id
        self.token_str = str(user_id) + '~' + str(curr_dt) + '~' + role
        self.token_key = kh().generate_key()
        self.save_token()
        self.start_scheduler(self.user)
        return base64.urlsafe_b64encode(self.token_key.encode())
        
    def start_scheduler(self, user):
        life = None
        with open('/opt/app/django/restFulAPI/api_security/security/config/token_config.json','r') as tkconf:
            life = json.load(tkconf)["life"]
        
        schdlr = thrd.Thread(target = self.delete_token, args = (user, int(life),))
        schdlr.start()
        
    def save_token(self):
        with trsxn.atomic():
            user_token = mdl.Token.objects.select_for_update().get(user = self.user)
            user_token.tkn_key = self.token_key; user_token.value = self.token_str
            user_token.save()
    
    def delete_token(self, user, delay = 0):
        try:
            time.sleep(delay)
            with trsxn.atomic():
                token_to_delete = mdl.Token.objects.select_for_update().get(user = user)
                token_to_delete.tkn_key = token_to_delete.user.username
                token_to_delete.value = token_to_delete.user.username
                token_to_delete.save()
        except:
            pass
        finally:
            del(token_to_delete)

    def update_token_history(self, user_id, operation, smry):
        user = mdl.Administration.objects.get(username = user_id)
        mdl.Token_usage_history.objects.create(user = user, operation = operation, summary = smry)
        self.delete_token(user_id)
        