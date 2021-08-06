from Cube_Setup import *
import pprint

#to do 1) detect when parity happens 2) detect when edge flips/corner flips happen

solved_cube = [['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'], ['G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G'], ['R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R'],
               ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'], ['Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y']]
T_perm = ["R", "U", "Ri", "Ui", "Ri", "F", "R2", "Ui", "Ri", "Ui", "R", "U", "Ri", "Fi"]
J_perm = ['R', 'U', 'Ri', 'Fi', 'R', 'U', 'Ri', 'Ui', 'Ri', 'F', 'R2', 'Ui', 'Ri', 'Ui']
Y_perm = ['R', 'Ui', 'Ri', 'Ui', 'R', 'U', 'Ri', 'Fi', 'R', 'U', 'Ri', 'Ui', 'Ri', 'F', 'R']
parity = ['R', 'Ui', 'Ri', 'Ui', 'R', 'U', 'R', 'D', 'Ri', 'Ui', 'R', 'Di', 'Ri', 'U2', 'Ri', 'Ui']


def create_piece_array():
    #lmao this is a 5 dimensional array don't worry about it :)
    #piece_index, 3 indexes is coordinate of 3x3 piece labeled
    #the next index is code for the surface on a specific 1x1x1 piece
    #k, j, i is the order the faces are indexed where those represent the unit normal vectors to the piece faces
    #the final index represents the coordinates via the face + 3x3 grid index coordinate schema used in the Cube class
    coords = [[[0, 0], [3, 2], [4, 0]], [[0, 1], [3, 1]], [[0, 2], [3, 0], [2, 2]], [[0, 3], [4, 1]],
              [[0, 4]], [[0, 5], [2, 1]], [[0, 6], [1, 0], [4, 2]], [[0, 7], [1, 1]], [[0, 8], [1, 2], [2, 0]],
              [[3, 5], [4, 3]], [[3, 4]], [[3, 3], [2, 5]], [[4, 4]], [], [[2, 4]], [[1, 3], [4, 5]], [[1, 4]],
              [[1, 5], [2, 3]], [[5, 6], [3, 8], [4, 6]], [[5, 7], [3, 7]], [[5, 8], [3, 6], [2, 8]], [[5, 3], [4, 7]], [[5, 4]],
              [[5, 5], [2, 7]], [[5, 0], [1, 6], [4, 8]], [[5, 1], [1, 7]], [[5, 2], [1, 8], [2, 6]]]
    pieces = []
    for i in range(27):
        pieces.append(coords[i])
    return pieces

def invert_move_seq(seq):
    seq.reverse()
    invert = []
    for x in seq:
        if 'i' in x:
            invert.append(x[0])
        elif '2' in x:
            invert.append(x)
        else:
            invert.append(x + 'i')
    return invert

#edge function stuff
def check_solved(edges):
    #checks if all the edges have been solved
    for e in edges:
        if [0, 5] in e[0]:
            continue
        elif e[1] == 0:
            return False
    return True


def current_edge_solved(edges, edge):
    #checks in solved_edges array if a current edge is solved
    for e in edges:
        if edge in e[0]:
            if e[1] == 1:
                return True
    return False

def find_edge_origin(edges, color1, coord1, cube):
    for e in edges:
        if e[0][0] == coord1:
            coord2 = e[0][1]
            color2 = cube.cube_coords[coord2[0]][coord2[1]]
        elif e[0][1] == coord1:
            coord2 = e[0][0]
            color2 = cube.cube_coords[coord2[0]][coord2[1]]
    for ed in edges:
        if solved_cube[ed[0][0][0]][ed[0][0][1]] == color1 and solved_cube[ed[0][1][0]][ed[0][1][1]] == color2:
            return ed[0][0]
        elif solved_cube[ed[0][0][0]][ed[0][0][1]] == color2 and solved_cube[ed[0][1][0]][ed[0][1][1]] == color1:
            return ed[0][1]
    return 0


def edge_seq(cube):
    solved_edges = []
    for piece in piece_index:
        if len(piece) == 2:
            solved_edges.append([piece, 0])
    edge_seq = []
    current_coord = [0, 5]
    for z in solved_edges:
        if cube.cube_coords[z[0][0][0]][z[0][0][1]] == solved_cube[z[0][0][0]][z[0][0][1]] and cube.cube_coords[z[0][1][0]][z[0][1][1]] == solved_cube[z[0][1][0]][z[0][1][1]]:
            z[1] = 1
    for x in solved_edges:
        if current_coord in x[0]:
            x[1] = 1
    while not check_solved(solved_edges):
        color = cube.cube_coords[current_coord[0]][current_coord[1]]
        current_coord = find_edge_origin(solved_edges, color, current_coord, cube)
        if current_edge_solved(solved_edges, current_coord):
            for y in solved_edges:
                if y[1] == 0:
                    current_coord = y[0][0]
                    edge_seq.append(current_coord)
                    break
            continue
        edge_seq.append(current_coord)
        for x in solved_edges:
            if current_coord in x[0]:
                x[1] = 1
    return edge_seq

def edge_alg_moves(edge_seq):
    edge_setup = {(0, 1): ['l2', 'Di', 'l2'], (0, 7):['l2', 'D', 'l2'], (0, 3): [], (4, 1):['L', 'di', 'L'], (4, 5):['di', 'L'], (4, 7):['Li', 'di', 'L'],
                  (4, 3):['d', 'Li'], (1, 1):['l', 'Di', 'L2'], (1, 5):['d2', 'L'], (1, 7):['l', 'D', 'L2'], (1, 3):['Li'], (2, 5):['d', 'L'],
                  (2, 7):['Di', 'l', 'D', 'L2'], (2, 3):['di', 'Li'], (3, 1):['li', 'D', 'L2'], (3, 5):['L'], (3, 7):['li', 'Di', 'L2'], (3,3):['d2', 'Li']
                  , (5, 1):['Di', 'L2'], (5, 5):['D2', 'L2'], (5, 7):['D', 'L2'], (5, 3):['L2']}
    move_seq = []
    for x in edge_seq:
        t = tuple(x)
        move_seq += edge_setup[t]
        move_seq += T_perm
        move_seq += invert_move_seq(edge_setup[t])
    return move_seq

#corner function stuff

def all_corners_solved(corners):
    for c in corners:
        if [0, 0] in c[0]:
            continue
        elif c[1] == 0:
            return False
    return True

def current_corner_solved(corners, corner):
    for c in corners:
        if corner in c[0]:
            if c[1] == 1:
                return True
    return False

def find_corner_origin(corners, color1, coord1, cube):
    for c in corners:
        if c[0][0] == coord1:
            coord2, coord3 = c[0][1], c[0][2]
            color2, color3 = cube.cube_coords[coord2[0]][coord2[1]], cube.cube_coords[coord3[0]][coord3[1]]
        elif c[0][1] == coord1:
            coord2, coord3 = c[0][0], c[0][2]
            color2, color3 = cube.cube_coords[coord2[0]][coord2[1]], cube.cube_coords[coord3[0]][coord3[1]]
        elif c[0][2] == coord1:
            coord2, coord3 = c[0][0], c[0][1]
            color2, color3 = cube.cube_coords[coord2[0]][coord2[1]], cube.cube_coords[coord3[0]][coord3[1]]
    for co in corners:
        if solved_cube[co[0][0][0]][co[0][0][1]] == color1 and solved_cube[co[0][1][0]][co[0][1][1]] == color2 and solved_cube[co[0][2][0]][co[0][2][1]] == color3:
            return co[0][0]
        elif solved_cube[co[0][0][0]][co[0][0][1]] == color1 and solved_cube[co[0][1][0]][co[0][1][1]] == color3 and solved_cube[co[0][2][0]][co[0][2][1]] == color2:
            return co[0][0]
        elif solved_cube[co[0][0][0]][co[0][0][1]] == color2 and solved_cube[co[0][1][0]][co[0][1][1]] == color1 and solved_cube[co[0][2][0]][co[0][2][1]] == color3:
            return co[0][1]
        elif solved_cube[co[0][0][0]][co[0][0][1]] == color3 and solved_cube[co[0][1][0]][co[0][1][1]] == color1 and solved_cube[co[0][2][0]][co[0][2][1]] == color2:
            return co[0][1]
        elif solved_cube[co[0][0][0]][co[0][0][1]] == color2 and solved_cube[co[0][1][0]][co[0][1][1]] == color3 and solved_cube[co[0][2][0]][co[0][2][1]] == color1:
            return co[0][2]
        elif solved_cube[co[0][0][0]][co[0][0][1]] == color3 and solved_cube[co[0][1][0]][co[0][1][1]] == color2 and solved_cube[co[0][2][0]][co[0][2][1]] == color1:
            return co[0][2]
    return 0

def corner_seq(cube):
    solved_corners = []
    for piece in piece_index:
        if len(piece) == 3:
            solved_corners.append([piece, 0])
    corner_seq = []
    current_coord = [4, 0]
    for z in solved_corners:
        if cube.cube_coords[z[0][0][0]][z[0][0][1]] == solved_cube[z[0][0][0]][z[0][0][1]] and \
                cube.cube_coords[z[0][1][0]][z[0][1][1]] == solved_cube[z[0][1][0]][z[0][1][1]] and \
                cube.cube_coords[z[0][2][0]][z[0][2][1]] == solved_cube[z[0][2][0]][z[0][2][1]]:
            z[1] = 1
    for x in solved_corners:
        if current_coord in x[0]:
            x[1] = 1
    while not all_corners_solved(solved_corners):
        color = cube.cube_coords[current_coord[0]][current_coord[1]]
        current_coord = find_corner_origin(solved_corners, color, current_coord, cube)
        if current_corner_solved(solved_corners, current_coord):
            for y in solved_corners:
                if y[1] == 0:
                    current_coord = y[0][0]
                    corner_seq.append(current_coord)
                    break
            continue
        corner_seq.append(current_coord)
        for x in solved_corners:
            if current_coord in x[0]:
                x[1] = 1
    return corner_seq


def corner_alg_moves(corner_seq):
    corner_setup = {(0, 2): ['R2'], (0, 8): ['F2', 'D'], (0, 6): ['F2'], (4, 2):['Fi', 'D'], (4, 8):['Fi'], (4, 6):['Di', 'R'], (1, 0):['F', 'Ri'], (1, 2):['Ri'],
    (1, 8):['Fi', 'Ri'], (1, 6):['F2', 'Ri'], (2, 0):['F'], (2, 2):['Ri', 'F'], (2, 8):['R2', 'F'], (2, 6):['R', 'F'], (3, 0):['R', 'Di'], (3, 8):['D', 'Fi'],
                    (3, 6):['R'], (5, 0):['D'], (5, 2): [], (5, 8):['Di'], (5, 6):['D2']}
    move_seq = []
    for x in corner_seq:
        t = tuple(x)
        move_seq += corner_setup[t]
        move_seq += Y_perm
        move_seq += invert_move_seq(corner_setup[t])
    return move_seq

scramble = convert("D2 F2 R2 B' F R' B U2 L' D' U' L' D L2 D' L B' D' B' F2 L2 D2 L' R2 B' D B' F D' L2")
cube = Cube(solved_cube)
cube.execute_move_seq(scramble)
cube.display()
piece_index = create_piece_array()
edge_s = edge_seq(cube)
edge_moves = edge_alg_moves(edge_s)
cube.execute_move_seq(edge_moves)
corner_s = corner_seq(cube)
corner_moves = corner_alg_moves(corner_s)
moves = edge_moves + corner_moves
print(len(moves))
print(moves)
cube.execute_move_seq(corner_moves)
cube.display()


