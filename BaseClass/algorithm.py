# 数组组合
#foods = input()
foods = "食材1,食材2,食材3"
foodList = foods.split(',')
for i in range(0,len(foodList)):
    for j in range(0,len(foodList)):
        if i != j:
            print(foodList[i],foodList[j])






