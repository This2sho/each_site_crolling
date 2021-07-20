i = 0
a = 100
for i in range(1, 4):
    a= a >> i
    print(a)
    a += 1
    print(a)
print(a)