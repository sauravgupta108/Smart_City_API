from datetime import datetime as dt
from .. import models as mdl
from django.db import transaction as trsxn
from .Key_handler import Key_handler as kh
import base64

class Token_handler:
    def generate_token(self, user_id, designation):
        curr_dt = dt.now()
        if designation == "Secretary":  permission = "200201"               #for GET and PATCH
        elif designation == "ZoneHead": permission = "200201203"            #for GET, PUT, POST, PATCH and DELETE
        else: raise ValueError
        
        #user_id, date and permission
        self.user = user_id
        self.token_str = str(user_id) + "*" + str(curr_dt) + "*" + permission           #Need to store encoded value of token_str
        self.token_key = kh().generate_key()
        self.save_token()
        
        return base64.urlsafe_b64encode(self.token_key.encode())
        
    def save_token(self):
        with trsxn.atomic():
            user_token = mdl.Token.objects.select_for_update().get(user = self.user)
            user_token.key = self.token_key; user_token.value = self.token_str
            user_token.save()
            
    def delete_token(self, token_key):
        with trsxn.atomic():
            try:
                token_to_delete = mdl.Token.objects.select_for_update().get(key = token_key)
                token_to_delete.key = token_to_delete.user.username
                token_to_delete.value = token_to_delete.user.username
                token_to_delete.save(['key','value'])
            except:
                pass