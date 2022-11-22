import bcrypt

clienthash = "$2b$12$S0JsqH4t87pLBM1AWTXeTOPMh2/fSskcygTF171Ro8MgdOtyLpbEu"
pwd = "AdminAdmin"
salt = bcrypt.gensalt(12)
dbHash = bcrypt.hashpw(pwd.encode('utf-8'), salt).decode('utf-8')
print(dbHash)
print(bcrypt.checkpw(pwd.encode('utf-8'), dbHash.encode('utf8')))