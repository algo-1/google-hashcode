from collections import defaultdict
import glob
files = glob.glob("./c_many_ingredients.txt")
files = list(map(lambda x: x.replace(".\\", ""), files))
k = 0
pizza_dict = {}
new_files = []
for file in files:
    k += 1
    new_files.append(f"ans_3_super_optimised.txt")
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

    teams = [4,3,2]
    picked = set()
    global_chosen = defaultdict(list)
    loops = 0
    i = 0
    for v in teams:
        for _ in range(data[v-1]):
            chosen = [sorted_pizza[i+x] for x in range(v)]
            i += v 
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