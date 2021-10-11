import json
import math

with open('Dist.json','r') as json_file:
    neighbour_list = json.load(json_file)

with open('Coord.json','r') as json_file:
    coord_list = json.load(json_file)


#new_list = {k: v for k, v in neighbour_list.items() if int(v[0]) > 50}

new_dict = {}

for k,v in neighbour_list.items():
    if k == "1269,1241":
        print(k,v)
        dist_1241 = v
    
    if k == "1269,1267":
        print(k,v)
        dist_1267 = v


for k,v in coord_list.items():
    if k == "50":
        print(k,v)
        kv_50 = v

    if k == "1241":
        print(k,v)
        kv_1241 = v

    if k == "1267":
        print(k,v)
        kv_1267 = v

    
co_1241 = (kv_50[0] - kv_1241[0])**2 + (kv_50[1] - kv_1241[1])**2
co_1267 = (kv_50[0] - kv_1267[0])**2 + (kv_50[1] - kv_1267[1])**2
print(math.sqrt(co_1241), dist_1241, math.sqrt(co_1267), dist_1267)