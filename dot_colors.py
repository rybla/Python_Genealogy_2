import random
random.seed()

# range 0+
colors = ["red", "blue", "darkgreen","black" ,"indigo", "green", "purple", "tan", "cyan"]
def num_to_color(num):
    if isinstance(num, list):
        return num_to_hex(num)

    if num >= len(colors) or num < 0:
        return 0
        
    return colors[num]

hex_colors = ['#FF0000', '#1E00F1', "#03B128"]
def num_to_hex(num):
    if isinstance(num, list):
        return list_to_hex(num)

    if num >= len(hex_colors) or num < 0:
        return 0
        
    return hex_colors[num]

def list_to_hex(ls):
    # only works if can divide into RGB (must have len==3)
    if len(ls) == 3:
        h = "#"
        for l in ls:
            l *= (16*16-1)
            h += to_hex(l)
        if h == "#FFFFFF":
            h = "#AAAAAA"
        return h
    # isn't exactly 3 long
    else:
        return "#000000"


# as a string tho
def to_hex(n):
    h = hex(n).split('x')[-1].upper()
    if len(h) == 1:
        h = "0" + h
    return h