# range 0+
colors = ["red", "blue", "darkgreen","black" ,"indigo", "green", "purple", "tan", "cyan"]
def num_to_color(num):
    if num >= len(colors) or num < 0:
        return 0
        
    return colors[num]