from github import Auth

# define static variables
AccessToken = None
user = None
g = None

def GetAccessToken():
    global AccessToken
    AccessToken = input("GitHub access token: ")

def AuthUser():
    GetAccessToken()
    g = Auth.Token(AccessToken)