from datetime import datetime as dt
from .. import models as mdl
from .Key_handler import Key_handler as kh
import base64

class Token_handler:
    def generate_token(user_id, designation):
        curr_dt = dt.now()
        if designation == "Secretary":  permission = "200201"               #for GET and PATCH
        elif designation == "ZoneHead": permission = "200201203"            #for GET, PUT, POST, PATCH and DELETE
        else: raise ValueError
        
        #user_id, date and permission
        token_str = str(user_id) + str(curr_dt) + permission
        token_key = kh.generate_key()
        new_tkn = mdl.Token(user_id, token_key,token_str.encode())
        #new_tkn.save()
        del(token_str); del(new_tkn)
        return base64.urlsafe_b64encode(token_key.encode())