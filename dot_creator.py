import os
import file_manager
import dot_colors
import math

# [NAME,GENERATION_COUNTS,MEMBERS]
genealogy_data = None

dot_file = None
generations_labels = []

def create_dot(gen_data,pdf=False):
    global genealogy_data, dot_file

    genealogy_data = gen_data

    directory = "outputs/dot/"

    # first couple of lines
    dot_file = file_manager.FileManager(directory,get_genealogy_name()+".dot")
    dot_file.write("graph \"" + get_genealogy_name() + "\"{")

    # create the dot stuff
    config_graph()
    create_generations_labels()
    create_generations()
    create_member_attributes()
    create_relations()

    finish()

    if pdf:
        os.system("sudo dot " + directory + get_genealogy_name() + ".dot -Tpdf -o " + directory + get_genealogy_name() + ".pdf")
        os.system("sudo rm " + directory + get_genealogy_name() + ".dot")



def get_genealogy_name():
    return genealogy_data[0]



def get_generation_sizes():
    return genealogy_data[1]



def get_generation_size(gen_num):
    return get_generation_sizes()[gen_num]



def get_members():
    return genealogy_data[2]



def get_member(gen_num, mem_num):

    if gen_num == 0:

        return get_members()[mem_num]

    else:
        
        # sum the number of members before this generation
        prev = sum(get_generation_sizes()[:gen_num])

        return get_members()[prev + mem_num]



def get_member_raw(mem_ind):

    return get_members()[mem_ind]



def set_graph_label(s):
    dot_file.write("   label=<<FONT POINT-SIZE='50'>\"" + s + "\"</FONT>>;")
    dot_file.write("   labelloc=tp;")



def set_graph_attribute(attr,val):
    dot_file.write("   graph [" + str(attr) + "=" +  str(val) + "];")



def set_node_attribute(attr,val):
    dot_file.write("   node [" + str(attr) + "=" +  str(val) + "];")



def set_edge_attribute(attr,val):
    dot_file.write("   edge [" + str(attr) + "=" + str(val) + "];")



def create_generations_labels():
    global generations_labels

    dot_file.write("   subgraph generations_labels {")
    dot_file.write("       node[color=grey style=filled fontsize=12 shape=cds fontcolor=black fixedsize=false style=invis];edge[style=invis]")
    
    s = ""
    
    # for each generation
    for i in range(len(get_generation_sizes())):
        lab = "Gen" + str(i)
        generations_labels.append(lab)
        s += lab + " -- "
    s = s[:-4]
    
    dot_file.write("      " + s + ";")
    dot_file.write("   }")



def create_generations():
    for j in range(len(get_generation_sizes())):

        s = "   {rank=same;" + generations_labels[j] + ";"
        
        for i in range(get_generation_size(j)):
        
            s += index_to_name(j,i) + ";"
        
        s += "}"
        
        dot_file.write(s)



def index_to_name(gen_num,mem_num):
    return "\"" + str(gen_num) + ":" + str(mem_num) + "\""

def index_raw_to_name(mem_ind):
    normalized = to_normal_index(mem_ind)

    return index_to_name(normalized[0],normalized[1])



def create_relations():
    # for all the members

    mem_ind = 0

    for i in range(len(get_generation_sizes())):
        for j in range(get_generation_size(i)):

            m = get_member(i,j)

            children = get_children(m)

            for child in children:

                s = "   " + index_to_name(i,j) + " -- " + index_raw_to_name(child)
                
                edge_color = calculate_edge_color(m,child)
                pen_width = calculate_edge_width(m,child)
                s += " ["
                s += "color=\"" + str(edge_color) + "\""
                s += " penwidth=" + str(pen_width)
                s += "];"

                dot_file.write(s)

            mem_ind += 1



def create_member_attributes():
    gen_ind = 0

    for gen in get_generation_sizes():
        for i in range(gen):

            m = get_member(gen_ind,i)

            color = calculate_member_color(m)
            shape = calculate_member_shape(m)
            width = calculate_member_width(m)
            fontsize = calculate_member_fontsize(m)

            # referene is one more than # of generations
            fitness = calculate_member_fitness(m)
            
            s = "    " + index_to_name(gen_ind,i) + " ["
            s += "color=\"" + str(color) + "\""
            s += " shape=" + str(shape)
            s += " width=" + str(width)
            s += " fontsize=" + str(fontsize)
            s += " label=\"" + str(fitness) + "\""
            s += "];"
            dot_file.write(s)

        gen_ind += 1



def finish():
    dot_file.write("}")
    dot_file.close()

# setup all basic attributes
def config_graph():
    # set_graph_label(get_genealogy_name())
    
    # set_graph_attribute("splines","splines")
    set_graph_attribute("nodesep","0.1")
    set_graph_attribute("ranksep",1)

    set_graph_attribute("size",5)
    set_graph_attribute("ratio","fill")

    set_node_attribute("style","filled")
    set_node_attribute("fontcolor","white")
    set_node_attribute("fixedsize","true")

def calculate_edge_color(parent,child):
    return dot_colors.num_to_color(get_trait(parent))

def calculate_edge_width(parent,child):
    total = sum(get_generation_sizes())

    percent_children = float(get_children_count_of(parent) / total)
    w = float(30) * percent_children
    if w < 0.5:
        w = 0.5 

    w = 4
    return w

def calculate_member_color(m):

    return dot_colors.num_to_color(get_trait(m))

# all circles for now
def calculate_member_shape(m):
    return "circle"

# percent children * 100
def calculate_member_width(m):
    # variable sizes
    # total = 0
    # for gen in genealogy.generations:
    #     total += len(gen)

    # percent_children = float(len(member.get_children(m))) / total
    # w = float(10) * percent_children
    # if w < 0.2:
    #     w = 0.2

    w = 1
    return w

# width * 20
def calculate_member_fontsize(m):
    return calculate_member_width(m) * float(20)

def calculate_member_fitness(m):
    return get_fitness(m)

def get_member_trait(gen_num,mem_num):

    return get_member(gen_num,mem_num)[1]



def get_member_raw_trait(mem_ind):

    return get_member_raw(mem_ind)[1]


def get_member_children_count(gen_num,mem_num):

    return get_member(gen_num,mem_num)[0][0]



def get_member_raw_children_count(gen_num,mem_num):

    return get_member_raw(gen_num,mem_num)[0][0]



def get_member_children(gen_num,mem_num):

    return get_member(gen_num,mem_num)[0][1]



def get_member_raw_children(gen_num,mem_num):

    return get_member_raw(gen_num,mem_num)[0][1]


def to_normal_index(mem_ind):

    gen_ind = 0
    prev_total = 0
    total = 0

    # stops when total goes over
    # prev_total is the total before total goes over
    while True:

        if total + get_generation_size(gen_ind) > mem_ind:

            return [gen_ind, mem_ind - total]

        else:

            prev_total = total

            gen_ind += 1

            total += get_generation_size(gen_ind)

# Structure of a single member (an lement of MEMBERS):
# - [0]: [number of children, [array of children indecies]]
# - [1]: trait value
# - [2]: fitness (not including age affect)

def get_trait(m):
    return m[1]

def get_fitness(m):
    return int(m[2])

def get_children_count_of(m):
    return m[0][0]

def get_children(m):
    return m[0][1]


def get_member_fitness(gen_num,mem_num,ref_gen):

    return get_member_raw_fitness(to_raw_index(gen_num,mem_num),ref_gen)