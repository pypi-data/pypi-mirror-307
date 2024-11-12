import pypitoken
token = pypitoken.Token.load("pypi-foo")  # a token with "user" privileges
token.restrict(projects=["FEAS"])
print(token.token)  # returns your new token
token.dump()  # returns yew token