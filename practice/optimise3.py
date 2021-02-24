from collections import defaultdict
from itertools import permutations
import glob
files = glob.glob("./c_many_ingredients.txt")
files = list(map(lambda x: x.replace(".\\", ""), files))
k = 0
new_files = []
for file in files:
    k += 1
    new_files.append(f"ans_3_optimised.txt")
    pizzas = []
    pizza_map = defaultdict(list)
    ingredients = set()
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
                i += 1
            count += 1

    # print(pizza_map)
    # print(data)
    
    def calc_diff(selected: set,  candidate: list):
        num_present = 0

        for val in candidate:
            if val in selected:
                num_present += 1
        
        return num_present


    # get ingredients 
    max_ing_on_a_pizza = 0
    for i, values in pizza_map.items():
        for v in values:
            ingredients.add(v)
        max_ing_on_a_pizza = max(max_ing_on_a_pizza, len(values))
        ing_map[i] = len(values)
    # print(len(ingredients))
    print(max_ing_on_a_pizza)
    # print(len(ing_map))

    def calc_num_ingredients(n):
        used_set = set()
        i = 0
        x = -1
        chosen = set() 
        if len(picked) + n > data[0]:
            return len(chosen), chosen

        while len(chosen) == 0:
            x += 1
            for pizza, ingredient_list in pizza_map.items():
                if len(ingredient_list) >= max_ing_on_a_pizza-x and len(chosen) == 0 and pizza not in picked:
                    for v in ingredient_list:
                        used_set.add(v)
                    picked.add(pizza)
                    chosen.add(pizza)
                    break

        while len(chosen) < n:
            for pizza, ingredient_list in pizza_map.items():
                diff = calc_diff(used_set,ingredient_list)
                if len(chosen) < n and pizza not in picked and diff <= i:
                    for v in ingredient_list:
                        used_set.add(v)
                    picked.add(pizza)
                    chosen.add(pizza)
                elif len(chosen) == n:
                    break
            i += 1
        return len(used_set), chosen
    
    # perms = permutations([2,3,4], 3)
    perm_list = [(4,3,2)] # list(perms)
    res = {}
    counter_dict = {}
    for permutation in perm_list:
        score = 0
        picked = set()
        counter = 0
        for v in permutation:
            for _ in range(data[v-1]):
                curr_score, chosen = calc_num_ingredients(v)
                # print(v, ": ", curr_score, chosen)
                score += curr_score
                if curr_score > 0:
                    counter += 1
            print("\ndone")
        print(permutation, score)
        res[permutation] = score
        counter_dict[permutation] = counter
        

    optimal_score = max([y for x,y in res.items()])
    print("\n\n")
    for val in res:
        if res[val] == optimal_score:
            picked = set()
            score = 0
            counter = 0
            f = open(new_files[k-1], "w")
            f.write(str(counter_dict[val]) + "\n")
            for v in val:
                for _ in range(data[v-1]):
                    curr_score, ch = calc_num_ingredients(v)
                    #print(v, ": ", curr_score, ch)
                    if curr_score > 0:
                        counter += 1
                        ch = list(ch)
                        ch = map(lambda x: str(x), ch)
                        spec = " ".join(ch)
                        toWrite = f"{v} {spec}\n"
                        f.write(toWrite)
                    score += curr_score
            break

    print(score, counter)
    print("\n")

   
    