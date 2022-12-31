from accounts.models import User, Token


class PasswordlessAuthenticationBackend(object):
    def authenticate(self, request, uid):
        token = Token.objects.get(uid=uid)
        try:
            return User.objects.get(email=token.email)
        except User.DoesNotExist:
            return User.objects.create(email=token.email)
        except Token.DoesNotExist:
            return None
        
        
    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
# import sys
# from accounts.models import ListUser, Token
#
#
# class PasswordlessAuthenticationBackend(object):
#
#     def authenticate(self, request, uid):
#         print('uid', uid, file=sys.stderr)
#         if not Token.objects.filter(uid=uid).exists():
#             print('no token found', file=sys.stderr)
#             return None
#         token = Token.objects.get(uid=uid)
#         print('got token', file=sys.stderr)
#         try:
#             user = ListUser.objects.get(email=token.email)
#             print('got user', file=sys.stderr)
#             return user
#         except ListUser.DoesNotExist:
#             print('new user', file=sys.stderr)
#             return ListUser.objects.create(email=token.email)
#
#     def get_user(self, email):
#         return ListUser.objects.get(email=email)
