import pandas as pd
import numpy as np
import random
    
cities = {
    "0":"Arak",
    "1":"Ardebil",
    "2":"Oroomie",
    "3":"Isfahan",
    "4":"Ahwaz",
    "5":"Ilam",
    "6":"Bojnoord",
    "7":"Bandar-Abbas",
    "8":"Boushehr",
    "9":"Birjand",
    "10":"Tabriz",
    "11":"Tehran",
    "12":"Khoram-Abad",
    "13":"Rasht",
    "14":"Zahedan",
    "15":"Zanjan",
    "16":"Sari",
    "17":"Semnan",
    "18":"Sanandaj",
    "19":"Shahr-Kurd",
    "20":"Shiraz",
    "21":"Ghazwin",
    "22":"Ghom",
    "23":"Karaj",
    "24":"Kerman",
    "25":"Kerman-Shah",
    "26":"Gorgan",
    "27":"Mashhad",
    "28":"Hamedan",
    "29":"Yasouj",
    "30":"Yazd",
}

def read_from_excel():
    df = pd.read_excel("ProvinceCenterDistances.xlsx")
    adj_matrix = np.zeros((31,31))
    for i in range(1,32):
        adj_matrix[:,i-1] = df[f"Unnamed: {i}"].to_numpy()[4:]
    return adj_matrix

def initial_solution(adj_matrix, starting_city):
    sol = [starting_city,]
    free_nodes = [i for i in range(adj_matrix.shape[0])]
    free_nodes.remove(starting_city)
    while free_nodes:
        next_node = random.choice(free_nodes)
        sol.append(next_node)
        free_nodes.remove(next_node)
    sol.append(starting_city)
    return sol

def compute_cost(adj_matrix, path):
    cost = 0
    for i in range(len(path)-1):
        cost += adj_matrix[path[i],path[i+1]]
    return cost

def random_successor(path: list):
    size = len(path)
    lower_bound = np.random.randint(low=1, high=size-2)
    higher_bound = np.random.randint(low=lower_bound+1, high=size-1)
    path[lower_bound:higher_bound] = list(reversed(path[lower_bound:higher_bound]))
    return path

def cities_list():
    cities_list=[]
    for i in cities:
        cities_list.append(cities[str(i)])
    return cities_list