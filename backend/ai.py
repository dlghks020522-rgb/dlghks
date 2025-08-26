# backend/ai.py
import random

def find_best_move(game, difficulty):
    """난이도에 따라 최적의 수를 찾는 메인 함수"""
    if difficulty == 'beginner':
        return find_random_move(game)
    elif difficulty == 'intermediate':
        return find_heuristic_move(game)
    # 추후 고급 난이도 추가
    # elif difficulty == 'advanced':
    #     return find_minimax_move(game)
    else:
        return find_random_move(game)

def find_random_move(game):
    """초급 난이도: 비어있는 모든 칸 중에서 무작위로 하나를 선택"""
    empty_cells = []
    for y in range(game.board_size):
        for x in range(game.board_size):
            if game.board[y][x] == 0:
                empty_cells.append((x, y))
    
    if not empty_cells:
        return None # 둘 곳이 없음
    return random.choice(empty_cells)

def find_heuristic_move(game):
    """중급 난이도: 휴리스틱 점수 기반으로 최적의 수를 찾음"""
    best_score = -1
    best_move = None
    
    empty_cells = []
    for y in range(game.board_size):
        for x in range(game.board_size):
            if game.board[y][x] == 0:
                empty_cells.append((x, y))

    for x, y in empty_cells:
        # 각 빈 칸에 대한 점수 계산
        score = _calculate_score_for_cell(game, x, y)
        if score > best_score:
            best_score = score
            best_move = (x, y)
            
    return best_move if best_move is not None else find_random_move(game)

def _calculate_score_for_cell(game, x, y):
    """특정 칸에 돌을 놓았을 때의 점수를 계산 (공격 점수 + 수비 점수)"""
    ai_player = game.current_turn
    human_player = 2 if ai_player == 1 else 1

    # 공격 점수 계산
    game.board[y][x] = ai_player
    offensive_score = _get_score(game, x, y, ai_player)
    game.board[y][x] = 0 # 가상으로 놓았던 돌 제거

    # 수비 점수 계산 (상대방이 여기에 뒀을 때 얼마나 좋은 자리인지)
    game.board[y][x] = human_player
    defensive_score = _get_score(game, x, y, human_player)
    game.board[y][x] = 0 # 가상으로 놓았던 돌 제거
    
    # 공격 점수에 약간의 가중치를 더 줌
    return offensive_score * 1.1 + defensive_score

def _get_score(game, x, y, player):
    """특정 위치의 4방향 라인에 대한 점수를 합산"""
    scores = {
        'five': 100000,
        'four': 1000,
        'three': 100,
        'two': 10,
    }
    total_score = 0
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    for dx, dy in directions:
        count = 1
        for sign in [1, -1]:
            nx, ny = x + dx * sign, y + dy * sign
            while 0 <= nx < game.board_size and 0 <= ny < game.board_size and game.board[ny][nx] == player:
                count += 1
                nx += dx * sign
                ny += dy * sign
        
        if count >= 5: total_score += scores['five']
        elif count == 4: total_score += scores['four']
        elif count == 3: total_score += scores['three']
        elif count == 2: total_score += scores['two']
        
    return total_score