import genealogy, genealogy_multitraits, csv_creator, dot_creator

def multitrait(dot,csv):
    genealogy_multitraits.init_genealogy()
    gen_data = genealogy_multitraits.make_genealogy( name="MULTITRAIT_TEST", generations=2, generation_sizes_function=lambda x: 10 ,parents=1, balanced=False, trait_factor=1, trait_weights=[3,2,1] )
    if dot:
        dot_creator.create_dot(gen_data)
    if csv:
        csv_creator.create_csv(gen_data)


def singletrait(dot,csv):
    genealogy.init_genealogy()
    gen_data = genealogy.make_genealogy( name="SINGLETRAIT", generations=20, generation_sizes_function=lambda x: 10, parents=1, balanced=True, trait_factor=1, age_factor=2, trait_weights=[1,1] )
    if dot:
        dot_creator.create_dot(gen_data)
    if csv:
        csv_creator.create_csv(gen_data)


dot = True
csv = True
singletrait(dot,csv)