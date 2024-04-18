# This file contains all the required routines to make an A* search algorithm.
#
__authors__ = '1630568'
__group__ = 'DM.12'
# _________________________________________________________________________________________
# Intel.ligencia Artificial
# Curs 2022 - 2023
# Universitat Autonoma de Barcelona
# _______________________________________________________________________________________

from SubwayMap import *
from utils import *
import os
import math
import copy


#DONE
def expand(path, map):
    """
     It expands a SINGLE station and returns the list of class Path.
     Format of the parameter is:
        Args:
            path (object of Path class): Specific path to be expanded
            map (object of Map class):: All the information needed to expand the node
        Returns:
            path_list (list): List of paths that are connected to the given path.
    """
    path_list = []
    last = path.route[-1]
    for i in map.connections[last]:
        aux_path = Path(path.route[:])
        aux_path.add_route(i)
        path_list.append(aux_path)
    
    return path_list
    

#DONE
def remove_cycles(path_list):
    """
     It removes from path_list the set of paths that include some cycles in their path.
     Format of the parameter is:
        Args:
            path_list (LIST of Path Class): Expanded paths
        Returns:
            path_list (list): Expanded paths without cycles.
    """
    new_list = []
    for path in path_list:
        cycle = False
        for i in path.route:
            if path.route.count(i) > 1:
                cycle = True
        if cycle == False:
            new_list.append(path)
                
    return new_list


#DONE
def insert_depth_first_search(expand_paths, list_of_path):
    """
     expand_paths is inserted to the list_of_path according to DEPTH FIRST SEARCH algorithm
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            list_of_path (LIST of Path Class): The paths to be visited
        Returns:
            list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """
    aux_list = []
    for path in expand_paths:
        aux_list.insert(0, path)
    for path in aux_list:
        list_of_path.append(path)
    
    return list_of_path


#DONE
def depth_first_search(origin_id, destination_id, map):
    """
     Depth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): the route that goes from origin_id to destination_id
    """
    list_of_path = [Path(origin_id)]
    while list_of_path[-1].route[-1] != destination_id and len(list_of_path) != 0:
        c = list_of_path.pop()
        e = expand(c, map)
        e = remove_cycles(e)
        list_of_path = insert_depth_first_search(e, list_of_path)

    return list_of_path[-1]


#DONE (modificat 2a entrega)
def insert_breadth_first_search(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to BREADTH FIRST SEARCH algorithm
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """
    aux_list = []
    for path in expand_paths:
        aux_list.insert(0, path)
    for path in aux_list:
        list_of_path.append(path)
    
    return list_of_path


#DONE (modificat 2a entrega)
def breadth_first_search(origin_id, destination_id, map):
    """
     Breadth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    list_of_path = [Path(origin_id)]
    while len(list_of_path) != 0 and list_of_path[0].route[-1] != destination_id:
        c = list_of_path.pop(0)
        e = expand(c, map)
        e = remove_cycles(e)
        list_of_path = insert_breadth_first_search(e, list_of_path)

    return list_of_path[0]


#DONE
def calculate_cost(expand_paths, map, type_preference=0):
    """
         Calculate the cost according to type preference
         Format of the parameter is:
            Args:
                expand_paths (LIST of Paths Class): Expanded paths
                map (object of Map class): All the map information
                type_preference: INTEGER Value to indicate the preference selected:
                                0 - Adjacency
                                1 - minimum Time
                                2 - minimum Distance
                                3 - minimum Transfers
            Returns:
                expand_paths (LIST of Paths): Expanded path with updated cost
    """
    match type_preference:
        case 0:
            for path in expand_paths:
                path.update_g(len(path.route) - 1)
        case 1:
            for path in expand_paths:
                for i in range(len(path.route) - 1):
                    current_station = path.route[i]
                    next_station = path.route[i+1]
                    time_between_stations = map.connections[current_station][next_station]
                    path.update_g(time_between_stations)
        case 2:
            for path in expand_paths:
                for i in range(len(path.route) - 1):
                    current_station = path.route[i]
                    next_station = path.route[i+1]
                    time_between_stations = map.connections[current_station][next_station]
                    line = map.stations[current_station]['line']
                    if (map.stations[current_station]['name'] == map.stations[next_station]['name']):
                        velocity = 1
                    else:
                        velocity = map.velocity[line]
                    path.update_g(time_between_stations*velocity)
        case 3:
            for path in expand_paths:
                for i in range(len(path.route) - 1):
                    current_station = path.route[i]
                    next_station = path.route[i+1]
                    current_station_line = map.stations[current_station]['line']
                    next_station_line = map.stations[next_station]['line']
                    if (current_station_line != next_station_line):
                        path.update_g(1)
        
    return expand_paths


#DONE
def insert_cost(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to COST VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to cost
    """
    if (len(expand_paths) != 0):
        if (len(list_of_path) == 0):
            k = 1
            list_of_path.append(expand_paths[0])
        else:
            k = 0
        for i in range(k, len(expand_paths)):
            current_path = expand_paths[i]
            in_list = (current_path in list_of_path)
            for j in range(len(list_of_path)):
                aux_path = list_of_path[j]
                if (not in_list and current_path.g < aux_path.g):
                    list_of_path.insert(j, current_path)
                    in_list = True
            if (not in_list):
                list_of_path.append(current_path)

    return list_of_path


#DONE
def uniform_cost_search(origin_id, destination_id, map, type_preference=0):
    """
     Uniform Cost Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    list_of_path = [Path(origin_id)]
    while len(list_of_path) != 0 and list_of_path[0].route[-1] != destination_id:
        c = list_of_path.pop(0)
        e = expand(c, map)
        e = remove_cycles(e)
        e = calculate_cost(e, map, type_preference)
        list_of_path = insert_cost(e, list_of_path)
        
    if (len(list_of_path) != 0): return list_of_path[0]
    

#DONE
def calculate_heuristics(expand_paths, map, destination_id, type_preference=0):
    """
     Calculate and UPDATE the heuristics of a path according to type preference
     WARNING: In calculate_cost, we didn't update the cost of the path inside the function
              for the reasons which will be clear when you code Astar (HINT: check remove_redundant_paths() function).
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            map (object of Map class): All the map information
            destination_id (int): Final station id
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            expand_paths (LIST of Path Class): Expanded paths with updated heuristics
    """
    for path in expand_paths:
        match type_preference:
            case 0:
                if path.last != destination_id: path.update_h(1)
                else: path.update_h(0)
            case 1:
                destination_coords = [map.stations[destination_id]['x'], map.stations[destination_id]['y']]
                vel = max(map.velocity.values())
                for path in expand_paths:
                    current_coords = [map.stations[path.last]['x'], map.stations[path.last]['y']]
                    dist = euclidean_dist(current_coords, destination_coords)
                    path.update_h(dist/vel)
            case 2:
                destination_coords = [map.stations[destination_id]['x'], map.stations[destination_id]['y']]
                vel = max(map.velocity.values())
                for path in expand_paths:
                    current_coords = [map.stations[path.last]['x'], map.stations[path.last]['y']]
                    path.update_h(euclidean_dist(current_coords, destination_coords))
            case 3:
                destination_line = map.stations[destination_id]['line']
                for path in expand_paths:
                    current_line = map.stations[path.last]['line']
                    if (current_line != destination_line): path.update_h(1)
                    else: path.update_h(0)
                
    return expand_paths
    
    
#DONE
def update_f(expand_paths):
    """
      Update the f of a path
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
         Returns:
             expand_paths (LIST of Path Class): Expanded paths with updated costs
    """
    for path in expand_paths:
        path.update_f()
    
    return expand_paths


#DONE
def remove_redundant_paths(expand_paths, list_of_path, visited_stations_cost):
    """
      It removes the Redundant Paths. They are not optimal solution!
      If a station is visited and have a lower g-cost at this moment, we should remove this path.
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
             list_of_path (LIST of Path Class): All the paths to be expanded
             visited_stations_cost (dict): All visited stations cost
         Returns:
             new_paths (LIST of Path Class): Expanded paths without redundant paths
             list_of_path (LIST of Path Class): list_of_path without redundant paths
             visited_stations_cost (dict): Updated visited stations cost
    """
    for path in expand_paths:
        if path.last in visited_stations_cost:
            if path.g < visited_stations_cost[path.last]:
                visited_stations_cost[path.last] = path.g
                for aux in list_of_path:
                    if aux != path and aux.last == path.last:
                        list_of_path.remove(aux)
            else:
                expand_paths.remove(path)
            
        else:
            visited_stations_cost[path.last] = path.g

    return expand_paths, list_of_path, visited_stations_cost


#DONE
def insert_cost_f(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to f VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to f
    """
    if (len(expand_paths) != 0):
        if (len(list_of_path) == 0):
            k = 1
            list_of_path.append(expand_paths[0])
        else:
            k = 0
        for i in range(k, len(expand_paths)):
            current_path = expand_paths[i]
            in_list = (current_path in list_of_path)
            for j in range(len(list_of_path)):
                aux_path = list_of_path[j]
                if (not in_list and current_path.f < aux_path.f):
                    list_of_path.insert(j, current_path)
                    in_list = True
            if (not in_list):
                list_of_path.append(current_path)

    return list_of_path
        


#DONE
def coord2station(coord, map):
    """
        From coordinates, it searches the closest stations.
        Format of the parameter is:
        Args:
            coord (list):  Two REAL values, which refer to the coordinates of a point in the city.
            map (object of Map class): All the map information
        Returns:
            possible_origins (list): List of the Indexes of stations, which corresponds to the closest station
    """
    possible_origins = []
    min = 1000000
    for station in map.stations:
        dist = euclidean_dist(coord, (map.stations[station]["x"], map.stations[station]["y"]))
        if dist < min:
            min = dist
            possible_origins.clear()
            possible_origins.append(station)
        elif dist == min:
            possible_origins.append(station)
            
    return possible_origins


#DONE
def Astar(origin_id, destination_id, map, type_preference=0):
    """
     A* Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    list_of_path = [Path(origin_id)]
    tcp = {}
    while len(list_of_path) != 0 and list_of_path[0].route[-1] != destination_id:
        c = list_of_path.pop(0)
        e = expand(c, map)
        e = remove_cycles(e)
        e = calculate_cost(e, map, type_preference)
        e = calculate_heuristics(e, map, destination_id, type_preference)
        update_f(e)
        e, list_of_path, tcp = remove_redundant_paths(e, list_of_path, tcp)
        list_of_path = insert_cost_f(e, list_of_path)
        
    if (len(list_of_path) != 0): return list_of_path[0]
    
    
#DONE
def Astar_multiple_origins(coords, destination_id, map, type_preference=0):
    origin_id = []
    mindist = 1000000000
    for station in map.stations:
        distance = euclidean_dist(coords, [map.stations[station]['x'], map.stations[station]['y']])
        if distance == mindist:
            origin_id.append(station)
        elif distance < mindist:
            origin_id.clear()
            origin_id.append(station)
            mindist = distance

    mindist = 1000000000
    for n in origin_id:
        aux = Astar(n, destination_id, map, type_preference)
        if aux.g < mindist:
            final_path = aux
            mindist = aux.g
    
    return final_path
