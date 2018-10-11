import random, json, base64
from ..models import Administration as admn, Token as tkn

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

import base64
from Crypto.Cipher import AES

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
        
    def is_valid(self, key, client_id):
        try:
            secret_key = admn.objects.get(username = client_id).secret_key
            cipher = AES.new((secret_key + '#').encode())
        except (ObjectDoesNotExist, MultipleObjectsReturned) as e:
            return [False, None]

        try:
            url_key = base64.urlsafe_b64decode(key)
            decrypted_key = ((cipher.decrypt(url_key)).decode())[:10]
            tkn_val = tkn.objects.get(tkn_key = decrypted_key).value
            user, date, role = tkn_val.split('~')
            if user == client_id:
                return [True, role]
            else:
                return [False, None]
        except:
            return [False, None]