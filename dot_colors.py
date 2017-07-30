import random
random.seed()

# range 0+
colors = ["red", "blue", "darkgreen", "black" ,"indigo", "green", "purple", "tan", "cyan"]
def num_to_color(num):
    if isinstance(num, list):
        return num_to_hex(num)

    if num >= len(colors) or num < 0:
        return 0
        
    return colors[num]

hex_colors = ['#FF0000', '#FFFFFF', "#03B128"]
def num_to_hex(num):
    if isinstance(num, list):
        return list_to_hex(num)

    if num >= len(hex_colors) or num < 0:
        return 0
        
    return hex_colors[num]

# works up to 3
def list_to_hex(ls):
    if len(ls) == 3:
        h = "#"
        for l in ls:
            l *= (16*16-1)
            h += to_hex(l)
        if h == "#FFFFFF":
            h = "#AAAAAA"
        return h
    elif len(ls) == 2:
        h = "#"
        for l in ls:
            l *= (16*16-1)
            h += to_hex(l)
        h += "00"
        return h
    elif len(ls) == 1:
        if(ls[0]):
            return "#FF0000"
        else:
            return "#000000"
    else:
        return "#000000"


# as a string tho
def to_hex(n):
    h = hex(n).split('x')[-1].upper()
    if len(h) == 1:
        h = "0" + h
    return h

def to_bin(x):
    return int(bin(x)[2:])

def to_bin_arr(x):
    n = to_bin(x)
    return [int(i) for i in list(str(n))]

for i in range(2**3):
    print(to_bin(i))