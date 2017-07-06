import random
import numpy as np
import math
import copy
random.seed()

def prod(arr):
    total = 1
    for e in arr:
        total *= e
    return total

def init_genealogy():
    global AGE_FACTOR, POPULAR_FACTOR, TRAIT_FACTOR, TRAITS, NAME, GENERATIONS, PARENTS, GENERATION_COUNTS, MEMBERS, TRAITS_FUNCTION, FITNESS_FUNCTION

    AGE_FACTOR = 0

    POPULAR_FACTOR = 2.00

    TRAIT_FACTOR = 1

    NAME = None
    GENERATIONS = None
    PARENTS = None
    GENERATION_SIZES_FUNCTION = None

    # array of the number of members in each generation, respective to index
    GENERATION_COUNTS = []
    # array of all members
    MEMBERS = []

    FITNESS_FUNCTION = sum

    TRAITS_FUNCTION = prod

    """

    Structure of a single member (an element of MEMBERS):
    - [0]: [number of children, [array of children indecies]]
    - [1]: trait values (array of trues and falses, for each trait)
    - [2]: fitness (not including age affect)

    """


def default_generation_sizes_function(gen_num):
    return 5



# does all the stuff to make a genealogy
def make_genealogy(
            name=None,
            generations=5,
            parents=2,
            generation_sizes_function=default_generation_sizes_function,
            age_factor=-1,
            popular_factor=-1,
            trait_factor=-1,
            traits=None,
            traits_function='prod'
        ):

    global NAME, GENERATIONS, PARENTS, GENERATION_SIZES_FUNCTION, AGE_FACTOR, POPULAR_FACTOR, TRAIT_FACTOR, TRAITS, TRAITS_FUNCTION

    GENERATIONS = generations
    PARENTS = parents
    GENERATION_SIZES_FUNCTION = generation_sizes_function

    # set all the factors if they were given as inputs

    if age_factor != -1:

        AGE_FACTOR = age_factor

    if popular_factor != -1:

        POPULAR_FACTOR = popular_factor

    if trait_factor != -1:

        TRAIT_FACTOR = trait_factor

    if traits != None:

        TRAITS = traits

    if traits_function == 'prod':
        TRAITS_FUNCTION = prod
    elif traits_function == 'sum':
        TRAITS_FUNCTION = sum

    # set the name of genealogy (and file)

    if name == None:
        NAME = "A" + str(AGE_FACTOR) + "_P" + str(POPULAR_FACTOR) + "_T" + str(TRAIT_FACTOR)
    else:
        NAME = name

    # used to start off the trait pools for each parent choice (see choose_parents function)
    create_blank_trait_pool()

    # start creation of genealogy

    # also initializes GENERATION_COUNTS
    create_empty_members()

    for i in range(GENERATIONS):
        
        fill_generation(i)

    return [NAME,GENERATION_COUNTS,MEMBERS]



def create_empty_member():

    return [[0,[]],-1,-1]



def create_empty_members():
    global MEMBERS, GENERATION_COUNTS

    for i in range(GENERATIONS):
        
        # append GENERATION_SIZES_FUNCTION(i) empty members
        size = GENERATION_SIZES_FUNCTION(i)

        for i in range(size):

            MEMBERS.append(create_empty_member())

        GENERATION_COUNTS += [size]



def get_gen_size(gen_num):

    return GENERATION_COUNTS[gen_num]



def get_member(gen_num, mem_num):

    if gen_num == 0:

        return MEMBERS[mem_num]

    else:
        
        # sum the number of members before this generation
        prev = sum(GENERATION_COUNTS[:gen_num])

        return get_member_raw(prev + mem_num)



def get_member_raw(mem_ind):

    return MEMBERS[mem_ind]


def add_member_trait(gen_num,mem_num,trait_index):

    traits = get_member(gen_num,mem_num)[1][trait_index] = True


def remove_member_trait(gen_num,mem_num,trait_index):

    traits = get_member(gen_num,mem_num)[1][trait_index] = False


def set_member_traits(gen_num,mem_num,trait_values):

    get_member(gen_num,mem_num)[1] = trait_values

    update_fitness(gen_num,mem_num)



def get_member_traits(gen_num,mem_num):

    return get_member(gen_num,mem_num)[1]



def get_member_raw_traits(mem_ind):

    return get_member_raw(mem_ind)[1]



def get_memeber_trait_strength(gen_num,mem_num):
    trait_values = get_member_traits(gen_num,mem_num)
    trait_strengths = []
    for i in range(len(trait_values)):
        if trait_values[i]:
            trait_strengths.append(TRAITS[i]) # ratio value (from TRAITS)
        else:
            trait_strengths.append(1) # base value

    return TRAITS_FUNCTION(trait_strengths)



def get_member_raw_trait_strength(mem_ind):
    n = to_normal_index(mem_ind)
    return get_memeber_trait_strength(n[0],n[1])



# child_ind should be the raw index of the child
def add_child_to_member(gen_num,mem_num,child_ind):

    add_child_to_member_raw(to_raw_index(gen_num,mem_num),child_ind)



def add_child_to_member_raw(parent_ind,child_ind):

    MEMBERS[parent_ind][0][0] += 1
    MEMBERS[parent_ind][0][1].append(child_ind)

    update_fitness_raw(parent_ind)



def get_member_children_count(gen_num,mem_num):

    return get_member(gen_num,mem_num)[0][0]



def get_member_raw_children_count(gen_num,mem_num):

    return get_member_raw(gen_num,mem_num)[0][0]



def get_member_children(gen_num,mem_num):

    return get_member(gen_num,mem_num)[0][1]



def get_member_raw_children(mem_ind):

    return get_member_raw(mem_ind)[0][1]    



def set_member_fitness(gen_num,mem_num,fitness):

    get_member(gen_num,mem_num)[2] = fitness



CURRENT_GENERATION = 0
CURRENT_MEMBER = 0



def get_member_fitness(gen_num,mem_num,ref_gen):

    return get_member_raw_fitness(to_raw_index(gen_num,mem_num),ref_gen)



def get_member_raw_fitness(mem_ind,ref_gen):

    normalized_index = to_normal_index(mem_ind)

    age = ref_gen - normalized_index[0]

    return float(get_member_raw(mem_ind)[2]) * math.pow(age,-AGE_FACTOR)



def to_raw_index(gen_num,mem_num):

    if gen_num == 0:

        return mem_num

    return sum(GENERATION_COUNTS[:CURRENT_GENERATION]) + mem_num



def to_normal_index(mem_ind):

    gen_ind = 0
    prev_total = 0
    total = 0

    # stops when total goes over
    # prev_total is the total before total goes over
    while True:

        if total + get_gen_size(gen_ind) > mem_ind:

            return [gen_ind, mem_ind - total]

        else:

            prev_total = total

            gen_ind += 1

            total += get_gen_size(gen_ind)



def fill_generation(gen_num):
    global CURRENT_GENERATION, CURRENT_MEMBER

    CURRENT_GENERATION = gen_num
    CURRENT_MEMBER = 0

    # is the first generation (no parents)
    if gen_num == 0:

        # make the 2**len(TRAITS) different possible members
        # however many times possible (sets of 2**len(TRAITS))
        # then the rest will be random

        gen_size = get_gen_size(gen_num)
        combos_count = 2**len(TRAITS) # length of a set of combos
        randoms_count = gen_size % combos_count # left over after sets of combos

        sets_count = gen_size // combos_count # how many sets of combos there will be

        # needs to have length len(TRAITS)
        def decToBinAr(x):
            b = bin(x)[2:]
            ls = [int(c)==1 for c in b]
            ls.reverse()
            while len(ls) < len(TRAITS):
                ls.append(False)
            return ls

        # balance out the distribution
        for i in range(sets_count): # for each set
            for j in range(combos_count): # create a member for each combo
                trait_values = decToBinAr(j)
                set_member_traits(CURRENT_GENERATION,CURRENT_MEMBER,trait_values)
                CURRENT_MEMBER += 1

        # for the remainders, just make them random
        for i in range(randoms_count):
            # randomly choose if has each trait
            trait_values = [random_boolean() for t in TRAITS]
            set_member_traits(CURRENT_GENERATION,CURRENT_MEMBER,trait_values)
            CURRENT_MEMBER += 1

    else:

        # make an array of all the fitnesses of the possible parents
        # possible parents are members in generations before the current generation
        # ( as determined by get_active_members() )
        possible_parent_fitnesses = []
        for mem_ind in range(get_active_members()):

            possible_parent_fitnesses += [get_member_raw_fitness(mem_ind,CURRENT_GENERATION)]

        # create all the children that will be in the current generation
        for i in range(get_gen_size(gen_num)):

            # return array of raw indecies of the chosen parents
            parents = choose_parents(possible_parent_fitnesses)

            # creates a child based on the chosen parents
            # automatically fetches the next child (based on CURRENT_GEN and CURRENT_MEM,
            # which also automatically update)
            create_child(parents)



# number of members not in the CURRENT_GENERATION 
# they are avaliable to be chosen as parents
def get_active_members():

    if CURRENT_GENERATION == 0:
        return 0

    active = sum(GENERATION_COUNTS[:CURRENT_GENERATION])

    return active



def update_fitness(gen_num,mem_num):

    trait_strength = get_memeber_trait_strength(gen_num,mem_num)

    children_number = get_member_children_count(gen_num,mem_num)

    fitness = FITNESS_FUNCTION([
        ((children_number+1)**POPULAR_FACTOR),
        (trait_strength**TRAIT_FACTOR)
    ])

    get_member(gen_num,mem_num)[2] = fitness



def update_fitness_raw(mem_ind):
    normalized = to_normal_index(mem_ind)
    update_fitness(normalized[0],normalized[1])



# balance_first_gen only works if there are only two traits
def create_random_member(i):
    global CURRENT_MEMBER
        
    # randomly choose if has each trait
    trait_values = [random_boolean() for t in TRAITS]
    
    set_member_traits(CURRENT_GENERATION,CURRENT_MEMBER,trait_values)

    CURRENT_MEMBER += 1



# return the raw indecies of the parents
# (these indecies correspond directly to their index in possible_parent_fitnesses)
def choose_parents(possible_parent_fitnesses):

    # convert to percentages of total
    total = sum(possible_parent_fitnesses)
    for i in range(len(possible_parent_fitnesses)):
        possible_parent_fitnesses[i] = float(possible_parent_fitnesses[i]/total)

    indecies = np.arange(len(possible_parent_fitnesses))

    chosen = []

    done = False

    # choose numbers in range(total)
    # no repeats
    # theses represent the parent choices
    while not done:

        # raw mem index of choice
        choice = np.random.choice(indecies, p=possible_parent_fitnesses)

        if choice not in chosen:

            chosen += [choice]

        # chosen all the parents that need to be chosen
        if len(chosen) == PARENTS:

            done = True

    return chosen



BLANK_TRAIT_POOL = []

def create_blank_trait_pool():
    global BLANK_TRAIT_POOL

    for i in range(len(TRAITS)):

        # for each trait, either has or doesn't have
        BLANK_TRAIT_POOL += [[0,0]]



# parents are the raw indecies of the parents
def create_child(parents):
    global CURRENT_MEMBER

    # organization:
    # - index: trait index
    # - value:
    #   - [0]: don't have trait
    #   - [1]: have trait
    trait_pool = copy.deepcopy(BLANK_TRAIT_POOL)

    for mem_ind in parents:
        traits = get_member_raw_traits(mem_ind)
        for i in range(len(traits)):
            # has trait
            if traits[i]:
                trait_pool[i][1] += 1
            # doesn't have trait
            else:
                trait_pool[i][0] += 1

    new_traits = []

    # normalize to percentages
    for i in range(len(traits)):
        total = sum(trait_pool[i])
        probs = [ p/total for p in trait_pool[i] ]

        # either gets or doesn't get the trait based on the frequencies of
        # either having or not having the trait in the parents
        # traits do not influence the inheritance of each other
        choice = np.random.choice([False,True], p=probs)
        new_traits.append(choice)


    set_member_traits(CURRENT_GENERATION,CURRENT_MEMBER,new_traits)

    for parent_ind in parents:

        add_child_to_member_raw(parent_ind,to_raw_index(CURRENT_GENERATION,CURRENT_MEMBER))

    CURRENT_MEMBER += 1

def random_boolean():
    return random.randint(0,1) == 0