'''
Created on 22-Mar-2020

@author: sarangsawant
'''

authmsg = 'Auth failure'

class AuthError():
    '''
    Auth Exception
    '''
    def __init__(self, msg=authmsg, code=-1):
        self.msg = msg
        self.ecode = code


class UserNotFoundError():
    '''
    UserNotFoundError Exception
    '''
    def __init__(self, msg=authmsg):
        self.msg = msg
    
