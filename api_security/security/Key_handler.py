import random, json, base64
from ..models import Administration as adm
from .Validator import Validator as vldtr
from django.core.exceptions import ObjectDoesNotExist, MultipleOgjectsReturned

class Key_handler:
    def generate_key(self):
        cptlLetrs = [chr(i) for i in range(65, 91)]
        smlLetrs = [chr(i) for i in range(97, 123)]
        digits = [chr(i) for i in range(48, 58)]
        
        rndmLst = self.divideNumber(10, 3)
        key = []

        key.extend(random.sample(cptlLetrs, rndmLst[0]))
        key.extend(random.sample(smlLetrs, rndmLst[1]))
        key.extend(random.sample(digits, rndmLst[2]))
        
        return "".join(random.sample(key,len(key)))
        
    def divideNumber(self, intgr = 10, prts = 10):
        grpMdulus = int(intgr / prts)
        grpRmndr = intgr % prts
        fnlLst = [grpMdulus]*prts

        for i in range(grpRmndr):
          tmp = random.randint(0,prts-1)
          fnlLst[tmp]+=1

        return fnlLst
        
    def validate_key(self, key, user_id):
        valid_tpl = vldtr.is_valid_user(user_id)
        if valid_tpl[0]:
            secret_key = valid_tpl[1] + "#"
            
        else:
            return "401"