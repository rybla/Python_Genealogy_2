import genealogy, genealogy_multitraits, csv_creator, dot_creator

def multitrait(dot,csv):
    genealogy_multitraits.init_genealogy()
    gen_data = genealogy_multitraits.make_genealogy( name="MULTITRAIT_TEST", generations=10, generation_sizes_function=lambda x: 10 ,parents=2, balanced=False, trait_factor=0, popular_factor=0, age_factor=0 , trait_weights=[1,1,1] )
    if dot:
        dot_creator.create_dot(gen_data)
    if csv:
        csv_creator.create_csv(gen_data)


a = 1
p = 1
t = 1
<<<<<<< Updated upstream
parents = 2
=======
parents = 4
>>>>>>> Stashed changes
trait_weights = [2,1]

def singletrait(dot,csv):
    genealogy.init_genealogy()
    gen_data = genealogy.make_genealogy( name="SINGLETRAIT", generations=100, generation_sizes_function=lambda x: 50, parents=parents, balanced=True, trait_factor=t, age_factor=a, popular_factor=p, trait_weights=trait_weights )
    if dot:
        dot_creator.create_dot(gen_data)
    if csv:
        csv_creator.create_csv(gen_data)


<<<<<<< Updated upstream
dot = True
csv = False
singletrait(dot,csv)
=======
dot = False
csv = True
singletrait(dot,csv)

# multitrait(True,False)
>>>>>>> Stashed changes
