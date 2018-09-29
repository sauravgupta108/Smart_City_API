from datetime import datetime as dt
from .. import models as mdl
from django.db import transaction as trsxn
from .Key_handler import Key_handler as kh
import base64, json, time
import threading as thrd

class Token_handler:
    def generate_token(self, user_id, designation):
        curr_dt = dt.now()
        
        self.user = user_id
        self.token_str = str(user_id) + str(curr_dt)
        self.token_key = kh().generate_key()
        self.save_token()
        self.start_scheduler(self.token_key)
        return base64.urlsafe_b64encode(self.token_key.encode())
        
    def start_scheduler(self, key):
        life = None
        with open('/opt/app/django/restFulAPI/api_security/security/config/token_config.json','r') as tkconf:
            life = json.load(tkconf)["life"]
        
        schdlr = thrd.Thread(target = self.delete_token, args = (key, int(life),))
        schdlr.start()
        
    def save_token(self):
        with trsxn.atomic():
            user_token = mdl.Token.objects.select_for_update().get(user = self.user)
            user_token.key = self.token_key; user_token.value = self.token_str
            user_token.save()
    
    def delete_token(self, token_key, delay = 0):
        try:
            time.sleep(delay)
            with trsxn.atomic():
                token_to_delete = mdl.Token.objects.select_for_update().get(key = token_key)
                token_to_delete.key = token_to_delete.user.username
                token_to_delete.value = token_to_delete.user.username
                token_to_delete.save()                            
        except:
            pass
        finally:
            del(token_to_delete)

    