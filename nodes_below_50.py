import json

with open('G.json','r') as json_file:
    neighbour_list = json.load(json_file)

#new_list = {k: v for k, v in neighbour_list.items() if int(v[0]) > 50}

new_dict = {}

for k,v in neighbour_list.items():
    if int(k) > 50:
        break
    new_list = [i for i in v if int(i)<=50]
    new_dict[k] = new_list    

with open('G2.json','w') as json_file:
    json.dump(new_dict, json_file)