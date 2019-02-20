a= [[1,-2,-1,2],[4,5,6]]
for c in a:
    for var in c:
        if var>0:
            a.remove(c)
print(a)