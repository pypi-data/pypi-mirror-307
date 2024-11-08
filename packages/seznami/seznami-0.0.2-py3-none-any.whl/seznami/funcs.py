def matrix(a,b,c):
    for i in range(a):
        line = []
        for q in range(b):
            x = int(input(f"Vnesi število na {i+1}, {q+1}: "))
            line.append(x)
        c.append(line)
def prints(s):
    for i in s:
        print(i)