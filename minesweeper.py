MINE_SIGN, NONE_MINE_SIGN, BLANK_SIGN = "@", "*", "#"
NEIGHBOR_OFFSETS = [(1, 0), (1, 1), (0, 1), (1, -1), (0, -1), (-1, 0), (-1, 1), (-1, -1)]

def enumerate_board(board):
    return [(rdx, cdx, col) for rdx, row in enumerate(board) for cdx, col in enumerate(row)]

def find_mines(board):
    board = [row[:] for row in board]  # 복사
    for rdx, cdx, col in filter(lambda x: x[2].isdigit(), enumerate_board(board)):  # 셀에 숫자가 있는 경우로 필터링
        neighbors = list(get_neighbors(board, (rdx, cdx)))
        blank_and_mine_neighbors = list(filter(lambda x: board[x[0]][x[1]] in [MINE_SIGN, BLANK_SIGN], neighbors))  # 지뢰 후보들 개수
        if len(blank_and_mine_neighbors) == int(col):
            for neighbor in blank_and_mine_neighbors:
                board[neighbor[0]][neighbor[1]] = MINE_SIGN  # 지뢰 있는 것 확정
    return board

def find_none_mines(board):
    board = [row[:] for row in board]  # 복사
    for rdx, cdx, col in filter(lambda x: x[2].isdigit(), enumerate_board(board)):  # 셀에 숫자가 있는 경우로 필터링
        neighbors = list(get_neighbors(board, (rdx, cdx)))
        if len(list(filter(lambda x: board[x[0]][x[1]] == MINE_SIGN, neighbors))) == int(col):  # 지뢰 개수 == 현재 값
            for blank_neighbor in filter(lambda x: board[x[0]][x[1]] == BLANK_SIGN, neighbors):  # 나머지 빈 곳들은 지뢰가 없음이 확정.
                board[blank_neighbor[0]][blank_neighbor[1]] = NONE_MINE_SIGN
    return board

def get_neighbors(board, loc):
    in_board = lambda loc: 0 <= loc[0] < len(board) and 0 <= loc[1] < len(board[0])
    return filter(in_board, map(lambda x: (loc[0] + x[0], loc[1] + x[1]), NEIGHBOR_OFFSETS))

with open('mine.txt', 'r') as file:
    board = list(map(list, file.read().splitlines()))
    while True:
        new_board = find_none_mines(find_mines(board))
        if board == new_board:
            break
        board = new_board
    for row in board:
        print("".join(row))
