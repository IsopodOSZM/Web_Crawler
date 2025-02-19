strin = "kdnajkdbnasjkd"
x = 0
while x != len(strin):
    print(strin[x])
    strin = strin.replace("kdnajk", "")
    x += 1