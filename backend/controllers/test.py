import bcrypt

pwd = "AdminAdmin"
hash = "$2b$12$EJN3ChUbxNSjX07f1RCxb.C1ArPJ/bICl0kPzyY4R4.wtzYmn.ZyK"

print(bcrypt.checkpw(pwd.encode("utf-8") , hash.encode("utf-8") ))