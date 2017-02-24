# 数组组合
#foods = input()
foods = "食材1,食材2,食材3"
foodList = foods.split(',')
for i in range(0,len(foodList)):
    for j in range(0,len(foodList)):
        if i != j:
            print(foodList[i],foodList[j])


# 简易加密
#s = input()
c = "The Zen of Python"
k = ""
for s in c:
    if (ord(s)>96 and ord(s)<110) or (ord(s)>64 and ord(s)<78):
        k+=chr(ord(s)+13)
    elif (ord(s)>109 and ord(s)<123) or (ord(s)>77 and ord(s)<91):
        k+=chr(ord(s)-13)
    else:
        k+=s

print(k)



