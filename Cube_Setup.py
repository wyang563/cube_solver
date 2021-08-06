#all face colors W, G, R, B etc. should be denoted using capital letters
import pprint
solved_cube = [['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'], ['G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G'], ['R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R'],
               ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'], ['Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y']]

def convert(s):
    moves = s.split(" ")
    for x in range(len(moves)):
        if '\'' in moves[x]:
            moves[x] = moves[x][0] + 'i'
    return moves

def convert_to_six_moves(seq):
    return 0

class Cube:
    def __init__(self, cube_coords):
        self.colors = ['W', 'G', 'R', 'B', 'O', 'Y']
        self.cube_coords = []
        for i in range(6):
            t = []
            for j in range(9):
                t.append(cube_coords[i][j])
            self.cube_coords.append(t)

    def display(self):
        for i in range(6):
            print(self.colors[i] + " Face:")
            print("")
            for j in range(0, 9, 3):
                print(self.cube_coords[i][j] + " " + self.cube_coords[i][j+1] + " " + self.cube_coords[i][j+2] + "\n")

    def rotate(self, move):
        #doesn't work for the moves l, l'
        rotations = {'R': [[8, 5, 2, 0, 3, 6, 8, 5, 2, 8, 5, 2], [0, 3, 5, 1]], 'Ri': [[2, 5, 8, 2, 5, 8, 2, 5, 8, 6, 3, 0], [0, 1, 5, 3]], 'L': [[0, 3, 6, 0, 3, 6, 0, 3, 6, 8, 5, 2], [0, 1, 5, 3]], 'Li': [[6, 3, 0, 2, 5, 8, 6, 3, 0, 6, 3, 0], [0, 3, 5, 1]], 'U': [[2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0], [1, 4, 3, 2]],
                     'Ui': [[0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2], [1, 2, 3, 4]], 'D': [[6, 7, 8, 6, 7, 8, 6, 7, 8, 6, 7, 8,], [1, 2, 3, 4]], 'Di': [[8, 7, 6, 8, 7, 6, 8, 7, 6, 8, 7, 6], [1, 4, 3, 2]], 'F': [[6, 7, 8, 0, 3, 6, 2, 1, 0, 8, 5, 2], [0, 2, 5, 4]], 'Fi':[[8, 7, 6, 2, 5, 8, 0, 1, 2, 6, 3, 0], [0, 4, 5, 2]],
                     'B': [[2, 1, 0, 0, 3, 6, 6, 7, 8, 8, 5, 2], [0 ,4, 5, 2]], 'Bi': [[0, 1, 2, 2, 5, 8, 8, 7, 6, 6, 3, 0], [0, 2, 5, 4]], 'M': [[7, 4, 1, 1, 4, 7, 7, 4, 1, 7, 4, 1], [0, 3, 5, 1]], 'Mi': [[1, 4, 7, 1, 4, 7, 1, 4, 7, 7, 4, 1], [0, 1, 5, 3]], 'E':[[5, 4, 3, 5, 4, 3, 5, 4, 3, 5, 4, 3], [1, 4, 3, 2]],
                     'Ei':[[3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5], [1, 2, 3, 4]]}
        turn_face = {'R': 2, 'Ri': 2, 'L': 4, 'Li': 4, 'U': 0, 'Ui': 0, 'D': 5, 'Di': 5, 'F': 1, 'Fi': 1, 'B': 3, 'Bi': 3}
        face_shifts = [[6, 3, 0, 7, 4, 1, 8, 5, 2], [2, 5, 8, 1, 4, 7, 0, 3, 6]]
        shift = rotations[move][0]
        faces = rotations[move][1]
        temp = []
        for i in range(6):
            t = []
            for j in range(9):
                t.append(self.cube_coords[i][j])
            temp.append(t)
        face_index = -1
        for j in range(len(shift)):
            if j%3 == 0:
                face_index += 1
            self.cube_coords[faces[(face_index+1)%4]][shift[(j+3)%12]] = temp[faces[face_index]][shift[j%12]]
        if 'i' in move:
            turns = face_shifts[1]
        else:
            turns = face_shifts[0]
        for k in range(9):
            if move in ['M', 'Mi', 'E', 'Ei']:
                break
            self.cube_coords[turn_face[move]][k] = temp[turn_face[move]][turns[k]]

    def execute_move_seq(self, seq):
        for x in range(len(seq)):
            if 'li' == seq[x]:
                self.rotate('M')
                self.rotate('Li')
            elif 'l' in seq[x]:
                if "2" in seq[x]:
                    self.rotate('Mi')
                    self.rotate('Mi')
                    self.rotate('L')
                    self.rotate('L')
                else:
                    self.rotate('Mi')
                    self.rotate('L')
            elif 'di' == seq[x]:
                self.rotate('Di')
                self.rotate('E')
            elif 'd' in seq[x]:
                if "2" in seq[x]:
                    self.rotate("Ei")
                    self.rotate("Ei")
                    self.rotate('D')
                    self.rotate('D')
                else:
                    self.rotate('Ei')
                    self.rotate('D')
            elif "2" in seq[x]:
                self.rotate(seq[x][0])
                self.rotate(seq[x][0])
            else:
                self.rotate(seq[x])











