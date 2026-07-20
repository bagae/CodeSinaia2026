l=[1,"hello",3.14,True]
print(l)
for i in range (len(l)):
    print(type(l[i]))
q=[type(l[i]) for i in range(len(l))]
print(q)
print(type(q[0]))