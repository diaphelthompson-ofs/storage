import hashlib
import string
import random

def encrypt(item):

    encryption_object = hashlib.md5()
    encryption_object.update(item)

    encrypted_item = encryption_object.hexdigest()

    return encrypted_item



def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))
