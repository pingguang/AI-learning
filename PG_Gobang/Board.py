from copy import deepcopy
from itertools import groupby

import numpy as np


class Board:
    def __init__(self, size=12):
        self.size = size
        self.chess = np.zeros((size, size), int)
        self.update()

    def update(self):
        #map() 会根据提供的函数对指定序列做映射
        #lambda叫做匿名函数，是一种不需要提前对函数进行定义再使用的情况下就可以使用的函数，冒号的左：原函数的参数，右：原函数的返回值。 
        self.vacuity = list(map(lambda x: tuple(x), np.argwhere(self.chess == 0)))

    def move(self, pos, player):
        self.chess[pos[0], pos[1]] = player
        self.update()

    def end(self, player):
        seq = list(self.chess)
        seq.extend(self.chess.transpose())
        fliplr = np.fliplr(self.chess)
        for i in range(-self.size + 1, self.size):
            seq.append(self.chess.diagonal(i))
        for i in range(-self.size + 1, self.size):
            seq.append(fliplr.diagonal(i))
        for seq in map(groupby, seq):
            for v, i in seq:
                if v == 0: continue
                if v == player and len(list(i)) == 5:
                    return v
        return 0

    def defend(self):
        for x, y in self.vacuity:
            origin = map(groupby, [
                self.chess[x],
                self.chess.transpose()[y],
                self.chess.diagonal(y - x),
                np.fliplr(self.chess).diagonal(self.size - 1 - y - x)
            ])
            origin = [x for x in origin]
            chess = deepcopy(self.chess)
            chess[x][y] = -1
            for index, seq in enumerate(
                    map(groupby, [
                        chess[x],
                        chess.transpose()[y],
                        chess.diagonal(y - x),
                        np.fliplr(chess).diagonal(self.size - 1 - y - x)
                    ])):
                seq = [(v, len(list(i))) for v, i in seq]
                org_seq = [(v, len(list(i))) for v, i in origin[index]]
                for i, v in enumerate(seq):
                    if v[0] != -1: continue
                    if v[1] >= 5: return x, y
                    if v[1] == 4 and seq.count((-1, 4)) != org_seq.count((-1, 4)):
                        if i - 1 >= 0 and seq[i - 1][0] == 0 and i + 1 < len(seq) and seq[i + 1][0] == 0: return x, y
        return None


if __name__ == "__main__":
    Board()
