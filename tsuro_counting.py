# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 18:15:20 2022

@author: tobycrisford
"""

import math

def count_possibilities(n_spots_total, tile, current_spot, symmetry_fn):
    
    if current_spot == n_spots_total - 1:
        return 1
    
    if tile[current_spot]:
        return count_possibilities(n_spots_total, tile, current_spot + 1, symmetry_fn)
    
    n_possibilities = 0
    
    for i in range(current_spot+1, n_spots_total):
        if not tile[i]:
            possible = True
            pairs = symmetry_fn(current_spot, i)
            changes = []
            for p in range(len(pairs)):
                if (tile[pairs[p][0]] != tile[pairs[p][1]]):
                    possible = False
                    break
                if not tile[pairs[p][0]]:
                    tile[pairs[p][0]] = True
                    changes.append(pairs[p][0])
                    tile[pairs[p][1]] = True
                    changes.append(pairs[p][1])
            if possible:
                n_possibilities += count_possibilities(n_spots_total, tile,
                                                       current_spot+1, symmetry_fn)
            for changed in changes:
                tile[changed] = False
                tile[changed] = False
            
    return n_possibilities
            

def cyclic_2_4_single(n_edges, n_spots, i):
    
    return int((i + (n_spots * (n_edges / 2)))) % (n_edges * n_spots)

def cyclic_2_4(n_edges, n_spots, i, j):
    
    return [(i,j),(cyclic_2_4_single(n_edges,n_spots,i),
                   cyclic_2_4_single(n_edges,n_spots,j))]

def cyclic_1_4_single(n_edges,n_spots,i,n):
    
    return (i + n*n_spots) % (n_edges * n_spots)

def cyclic_1_4(n_edges,n_spots,i,j):
    
    output = []
    for k in range(4):
        output.append((cyclic_1_4_single(n_edges,n_spots,i,k),
                       cyclic_1_4_single(n_edges,n_spots,j,k)))
        
    return output

def reflect_square_diagonal_single(n_spots, i):
    
    return int((-1 * (i+0.5)) - 0.5) % (4 * n_spots)

def reflect_square_edge_single(n_spots,i):
    
    if n_spots % 2 == 0:
        return reflect_square_diagonal_single(n_spots,i)
    else:
        return (-1 * i) % (4 * n_spots)
    
def reflect_square_diagonal(n_spots, i, j):
    return [(i,j),(reflect_square_diagonal_single(n_spots,i),
                   reflect_square_diagonal_single(n_spots,j))]

def reflect_square_edge(n_spots, i, j):
    return [(i,j),(reflect_square_edge_single(n_spots,i),
                   reflect_square_edge_single(n_spots,j))]
        

def count_square(n_spots):
    
    n_360_symmetry = count_possibilities(n_spots*4,[False for i in range(n_spots*4)],
                                         0,
                                         lambda x,y: cyclic_1_4(4,n_spots,x,y))
    
    n_180_symmetry_alone = (count_possibilities(n_spots*4,[False for i in range(n_spots*4)],
                                         0,
                                         lambda x,y: cyclic_2_4(4,n_spots,x,y)) - n_360_symmetry) / 2
    
    total_permutations = math.factorial(4*n_spots)/((2**(2*n_spots)) * math.factorial(2*n_spots))
    
    unsymmetric = (total_permutations - (n_180_symmetry_alone*2) - n_360_symmetry) / 4
    
    return unsymmetric + n_180_symmetry_alone + n_360_symmetry

def count_flippable_square(n_spots):
    #Using Burnside
    
    reflect_diagonal = count_possibilities(n_spots*4,[False for i in range(n_spots*4)],
                                          0,
                                          lambda x,y: reflect_square_diagonal(n_spots,x,y))
    
    reflect_edge = count_possibilities(n_spots*4,[False for i in range(n_spots*4)],
                                       0,
                                       lambda x,y: reflect_square_edge(n_spots,x,y))
    
    n_360_symmetry = count_possibilities(n_spots*4,[False for i in range(n_spots*4)],
                                         0,
                                         lambda x,y: cyclic_1_4(4,n_spots,x,y))
    
    n_180_symmetry = count_possibilities(n_spots*4,[False for i in range(n_spots*4)],
                                         0,
                                         lambda x,y: cyclic_2_4(4,n_spots,x,y))
    
    total_permutations = math.factorial(4*n_spots)/((2**(2*n_spots)) * math.factorial(2*n_spots))
    
    
    print(total_permutations,n_180_symmetry,n_360_symmetry,reflect_edge,reflect_diagonal)
    return (total_permutations + 2*n_360_symmetry + n_180_symmetry + 2*reflect_diagonal + 2*reflect_edge)/8