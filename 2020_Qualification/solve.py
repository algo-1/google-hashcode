#!/usr/bin/env pypy
from collections import defaultdict
import glob

files = glob.glob("./*.txt")
files = list(map(lambda x: x.replace(".\\", ""), files))
k = 0
res_files = []
for file in files:   
    libraries = defaultdict(list)
    k += 1
    res_files.append(f"ans_{k}.txt")
    with open(file) as f:
        i = -1
        count = 0
        for line in f:
            line = line.strip()
            if line:
                if count == 0:
                    data = line.split()
                    data = list(map(lambda x: int(x), data))
                    B, L, D = data[0], data[1], data[2]
                elif count == 1:
                    book_score = line.split()
                    book_score = list(map(lambda x: int(x), book_score))
                elif count % 2 == 0:
                    i += 1
                    vals = line.split()
                    vals = tuple(map(lambda x: int(x), vals))
                    libraries[i].append(vals)
                else:
                    vals = line.split()
                    vals = list(map(lambda x: int(x), vals))
                    libraries[i].append(sorted(vals, key = lambda x: book_score[x], reverse=True))
                    libraries[i].append(sum(map(lambda x: book_score[x], libraries[i][1])))
            count += 1
            
    # print(D)
    # for x,y in libraries.items():
    #     print(f"{x}, {y}")
  
    # libraries_sorted_by_total_score = sorted(libraries.items(), key= lambda x: x[1][2], reverse=True)
    # libraries_sorted_by_signup_time = sorted(libraries.items(), key= lambda x: x[1][0][1])
    # libraries_sorted_by_books_shipped_per_day = sorted(libraries.items(), key= lambda x: x[1][0][2], reverse=True)
    libraries_sorted_by_books_shipped_per_day_divided_by_signup_time = sorted(libraries.items(), key= lambda x: x[1][0][2]/x[1][0][1], reverse=True)
    # print(libraries_sorted_by_total_score)
    # print(libraries_sorted_by_signup_time)
    # print(libraries_sorted_by_books_shipped_per_day)
    # print(libraries_sorted_by_books_shipped_per_day_divided_by_signup_time)

    scanned_books  = set()
    selected_libraries = defaultdict(list)

    for lib, y in libraries_sorted_by_books_shipped_per_day_divided_by_signup_time:
        days_to_sign_up = y[0][1]
        books_shipped_per_day = y[0][2]
        book_ids = y[1]
        if  D > 0:
            D -= days_to_sign_up
            fuax_D = D
            i = 0
            while fuax_D >= 1 and i < len(book_ids):
                curr_book = book_ids[i]
                if curr_book not in selected_libraries:
                    selected_libraries[lib].append(curr_book)
                    scanned_books.add(curr_book)
                i += 1
                fuax_D -= (1/books_shipped_per_day)
        else:
            break
        
    # print(selected_libraries)

    f = open(res_files[k-1], "w")
    toWrite = f"{len(selected_libraries)}\n"
    f.write(toWrite)
    for lib, bk_ids in selected_libraries.items():
        lib = str(lib)
        num_bks = str(len(bk_ids))
        f.write(f"{lib} {num_bks}\n")
        bks = map(lambda x: str(x), bk_ids)        
        bks = " ".join(bks)       
        toWrite = f"{bks}\n"    
        f.write(toWrite)    
