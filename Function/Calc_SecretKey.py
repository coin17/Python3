# 简易加密
#s = input()
c = "Hello Python"
c = "Aa Bb Cc Dd Ee Ff Gg Hh Ii Jj Kk Ll Mm Nn Oo Pp Qq Rr Ss Tt Uu Vv Ww Xx Yy Zz"
k = ""
for s in c:
    if (ord(s)>96 and ord(s)<110) or (ord(s)>64 and ord(s)<78):
        k+=chr(ord(s)+13)
    elif (ord(s)>109 and ord(s)<123) or (ord(s)>77 and ord(s)<91):
        k+=chr(ord(s)-13)
    else:
        k+=s
print("原始串：" + c)
print("对称后：" + k)