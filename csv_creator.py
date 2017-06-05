import csv, dot_colors

csv_dir = "outputs/csv/"

"""
Structure of a single member (an element of MEMBERS):
- [0]: [number of children, [array of children indecies]]
- [1]: trait value
- [2]: fitness (not including age affect)
"""
# [NAME,GENERATION_COUNTS,MEMBERS]

def create_csv(gen_data):
    with open(csv_dir + str(gen_data[0]) + '_nodes.csv', 'w+') as csvfile:
        fieldnames = ['Id', 'Generation [z]', 'color']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        ind = 0
        gen = 0
        for gen_size in gen_data[1]:
            for i in range(gen_size):
                member = gen_data[2][ind]
                writer.writerow({
                        "Id": ind,
                        "Generation [z]": gen,
                        "color": dot_colors.num_to_hex(member[1])
                    })
                ind += 1
            gen += 1

    with open(csv_dir + str(gen_data[0]) + '_edges.csv', 'w+') as csvfile:
        fieldnames = ['Source','Target','color']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        ind = 0
        for member in gen_data[2]:
            for child in member[0][1]:
                writer.writerow({
                        "Source": ind,
                        "Target": child,
                        "color": dot_colors.num_to_hex(member[1])
                    })
            ind += 1