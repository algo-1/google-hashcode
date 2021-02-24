from collections import defaultdict
from itertools import permutations
import glob
files = glob.glob("./*.txt")
files = list(map(lambda x: x.replace(".\\", ""), files))
k = 0
new_files = []
for file in files:
    k += 1
    new_files.append(f"ans_{k}.txt")
    pizzas = []
    pizza_map = defaultdict(set)
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
                    pizza_map[i].add(v) 
                i += 1
            count += 1

    # print(pizza_map)
    # print(data)
    
    def calc_diff(selected: list[set],  candidate: set):
        curr_ingredients = set()
        num_present = 0
        candidate_list = list(candidate)

        for v in selected:
            v_list = list(v)
            for elem in v_list:
                curr_ingredients.add(elem)
        for val in candidate_list:
            if val in curr_ingredients:
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
    # print(max_ing_on_a_pizza)
    #print(ing_map)

    def calc_num_ingredients(n):
        used = []
        i = 0
        x = -1
        chosen = set() 
        global_used = set()
        if len(picked) + n > data[0]:
            return len(global_used), chosen

        while len(used) == 0:
            x += 1
            for pizza, iset in pizza_map.items():
                if len(iset) == max_ing_on_a_pizza-x and len(used) == 0 and pizza not in picked:
                    used.append(iset)
                    picked.add(pizza)
                    chosen.add(pizza)

        for pizza, iset in pizza_map.items():
            if len(used) == n:
                break
            if len(iset) == max_ing_on_a_pizza and pizza not in picked:
                used.append(iset)
                picked.add(pizza)
                chosen.add(pizza)
            else:
                if pizza not in picked:
                    diff = calc_diff(used,iset) 
                    if diff <= 0:
                        used.append(iset)
                        picked.add(pizza)
                        chosen.add(pizza)

        while len(used) < n:
            i += 1
            for pizza, iset in pizza_map.items():
                diff = calc_diff(used,iset)
                if pizza not in picked and diff <= i and len(used) < n:
                    used.append(iset)
                    picked.add(pizza)
                    chosen.add(pizza)
        
        for value in used:
            for v in value:
                global_used.add(v)

        return len(global_used), chosen
    
    perms = permutations([2,3,4], 3)
    perm_list = list(perms)
    res = {}
    counter_dict = {}
    for permutation in perm_list:
        score = 0
        picked = set()
        counter = 0
        for v in permutation:
            for _ in range(data[v-1]):
                curr_score, chosen = calc_num_ingredients(v)
                print(v, ": ", curr_score, chosen)
                score += curr_score
                if curr_score > 0:
                    counter += 1
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

   
    