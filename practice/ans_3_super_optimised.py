#!/usr/bin/env pypy
from functools import lru_cache
from collections import defaultdict
import glob
files = glob.glob("./c_many_ingredients.txt")
files = list(map(lambda x: x.replace(".\\", ""), files))
k = 0
pizza_dict = {}
new_files = []
for file in files:
    k += 1
    new_files.append(f"ans_3_super.txt")
    pizza_map = defaultdict(list)
    ing_map = {}
    data = []
    with open(file) as f:
        count = 0
        i = 0
        for line in f:
            line = line.strip()
            if count == 0:
                data = line.split()
                data = list(map(lambda x: int(x), data)) 
            else:
                d = line.split()          
                for v in d[1:]:
                    pizza_map[i].append(v) 
                pizza_dict[i] = int(d[0])
                i += 1
            count += 1


    # sort pizza dict
    sorted_list = sorted(pizza_dict.items(), key = lambda x: x[1], reverse= True)
    # print(*[x[1] for x in sorted_list], sep=",")
    sorted_pizza = [x[0] for x in sorted_list]

    # num_ingredients_greater_than_150 = list(filter(lambda x: x > 30 , [y[1] for y in sorted_list]))
    # print(len(num_ingredients_greater_than_150), len(sorted_list))

    # filtered_list = list(filter(lambda x: x[1] > 30, sorted_list))
    # pizza_dict = {x[0]: x[1] for x in filtered_list}

    def calc_unique_ingredients(selected: set,  candidate: list):
        unique = 0

        for val in candidate:
            if val not in selected:
                unique += 1
        
        return unique


    # get the number of ingredients that the pizza with the most ingredients has  
    max_ing_on_a_pizza = max([y for _,y in pizza_dict.items()])

    # @lru_cache(maxsize=None)
    def calc_num_ingredients(n):
        used_set = set()
        i = max_ing_on_a_pizza - 300
        x = -1
        z = 20
        chosen = set() 
        if len(picked) + n > data[0]:
            return len(chosen), chosen

        while len(chosen) == 0:
            x += 1
            for pizza in sorted_pizza:
                ingredient_list = pizza_map[pizza]
                if len(ingredient_list) >= max_ing_on_a_pizza-x and len(chosen) == 0 and pizza not in picked:
                    for v in ingredient_list:
                        used_set.add(v)
                    chosen.add(pizza)
                    break

        while len(chosen) < n:
            for pizza in sorted_pizza:
                ingredient_list = pizza_map[pizza]
                unique_ingredients = calc_unique_ingredients(used_set,ingredient_list)
                if len(chosen) < n and pizza not in picked and unique_ingredients >= i:
                    for v in ingredient_list:
                        used_set.add(v)
                    chosen.add(pizza)
                elif len(chosen) == n:
                    break
            z -= 1
            if z < 0:
                i -= 2
            else:
                i -= (2*z)

        return len(used_set), chosen
    
    teams = [4,3,2]
    picked = set()
    global_chosen = defaultdict(list)
    loops = 0

    for v in teams:
        for _ in range(data[v-1]):
            curr_score, chosen = calc_num_ingredients(v)
            for x in chosen:
                picked.add(x)
            global_chosen[v].append(chosen)
            loops+=1

            print(loops)

    f = open(new_files[k-1], "w")
    toWrite = str(loops) + "\n"
    f.write(toWrite)
    for t, ch_sets in global_chosen.items():
        for ch in ch_sets:
            temp = str(t)
            ch = list(ch)
            ch = map(lambda x: str(x), ch)        
            spec = " ".join(ch)       
            toWrite = f"{temp} {spec}\n"    
            f.write(toWrite)    