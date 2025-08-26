# backend/game.py

class OmokGame:
    def __init__(self, board_size=19):
        self.board_size = board_size
        self.reset()

    def reset(self):
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_turn = 1  # 1: 흑돌, 2: 백돌
        self.winner = None
        self.game_over = False
        self.moves = []

    def place_stone(self, x, y):
        # 1. 기본 유효성 검사
        if self.game_over:
            return False, "게임이 이미 종료되었습니다."
        if not (0 <= x < self.board_size and 0 <= y < self.board_size):
            return False, "보드 범위를 벗어났습니다."
        if self.board[y][x] != 0:
            return False, "이미 돌이 놓인 자리입니다."

        # 2. 흑돌 차례일 경우, 금수(Forbidden moves) 확인
        if self.current_turn == 1:
            is_forbidden, reason = self._is_forbidden_move(x, y)
            if is_forbidden:
                self.winner = 2 # 흑이 금수 위치에 두면 백의 승리
                self.game_over = True
                return False, f"금수입니다: {reason}. 백의 승리!"

        # 3. 돌 놓기
        self.board[y][x] = self.current_turn
        self.moves.append((x, y))

        # 4. 승리 조건 확인
        if self.check_win(x, y):
            self.winner = self.current_turn
            self.game_over = True
            return True, f"게임 종료! 플레이어 {self.winner}의 승리입니다."

        # 5. 턴 전환
        self.current_turn = 2 if self.current_turn == 1 else 1
        return True, "돌을 놓았습니다."

    def check_win(self, x, y):
        player = self.board[y][x]
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for dx, dy in directions:
            count = 1
            for sign in [1, -1]:
                nx, ny = x + dx * sign, y + dy * sign
                while 0 <= nx < self.board_size and 0 <= ny < self.board_size and self.board[ny][nx] == player:
                    count += 1
                    nx += dx * sign
                    ny += dy * sign
            
            # 렌주룰 적용: 흑은 정확히 5목, 백은 5목 이상이면 승리
            if player == 1 and count == 5:
                return True
            if player == 2 and count >= 5:
                return True
        return False

    def _is_forbidden_move(self, x, y):
        """흑돌의 금수 여부를 확인합니다: 3-3, 4-4, 장목"""
        # 가상으로 돌을 놓아보고 판단
        self.board[y][x] = 1

        # 1. 장목 (6목 이상) 확인
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            for sign in [1, -1]:
                nx, ny = x + dx * sign, y + dy * sign
                while 0 <= nx < self.board_size and 0 <= ny < self.board_size and self.board[ny][nx] == 1:
                    count += 1
                    nx += dx * sign
                    ny += dy * sign
            if count > 5:
                self.board[y][x] = 0 # 가상으로 놓았던 돌 제거
                return True, "장목"

        # 2. 3-3 및 4-4 확인
        open_threes = 0
        open_fours = 0
        
        for dx, dy in directions:
            result = self._check_line(x, y, dx, dy)
            if result == "open_three":
                open_threes += 1
            elif result == "four":
                # 4-3을 만들기 위해 4를 만드는 경우는 허용. 
                # 따라서 이 수로 인해 5가 완성되지 않을 때만 4로 카운트
                if not self.check_win(x, y):
                    open_fours += 1

        self.board[y][x] = 0 # 가상으로 놓았던 돌 제거

        if open_threes >= 2:
            return True, "3-3"
        if open_fours >= 2:
            return True, "4-4"

        return False, ""

    def _check_line(self, x, y, dx, dy):
        """특정 방향의 라인을 분석하여 열린 3, 4 등을 판단합니다."""
        player = self.board[y][x]
        
        # 양쪽으로 연속된 돌의 개수 세기
        count = 1
        empty_sides = 0
        
        # 정방향
        line_forward = []
        nx, ny = x + dx, y + dy
        while 0 <= nx < self.board_size and 0 <= ny < self.board_size:
            line_forward.append(self.board[ny][nx])
            nx += dx
            ny += dy

        # 역방향
        line_backward = []
        nx, ny = x - dx, y - dy
        while 0 <= nx < self.board_size and 0 <= ny < self.board_size:
            line_backward.append(self.board[ny][nx])
            nx -= dx
            ny -= dy
        
        # 패턴 분석 (매우 단순화된 버전)
        # 예: OXXXO -> 열린 3. X: player, O: empty
        
        # 정방향으로 연속된 같은 색 돌
        count_f = 0
        for i in range(len(line_forward)):
            if line_forward[i] == player:
                count_f += 1
            else:
                break
        
        # 역방향으로 연속된 같은 색 돌
        count_b = 0
        for i in range(len(line_backward)):
            if line_backward[i] == player:
                count_b += 1
            else:
                break
        
        total_count = count_f + count_b + 1

        # 양 끝이 비어있는지 확인
        side_f_empty = len(line_forward) > count_f and line_forward[count_f] == 0
        side_b_empty = len(line_backward) > count_b and line_backward[count_b] == 0

        if side_f_empty and side_b_empty:
            if total_count == 3:
                return "open_three"
        
        if total_count == 4:
            # 4는 한쪽만 열려있어도 4로 간주 (상대방이 막지 않으면 5가 되므로)
            if side_f_empty or side_b_empty:
                 return "four"
                 
        return None

    def print_board(self):
        stone_map = {0: '.', 1: '●', 2: '○'}
        print("  " + " ".join([f"{i:2}" for i in range(self.board_size)]))
        for i, row in enumerate(self.board):
            print(f"{i:2} " + " ".join([stone_map[cell] for cell in row]))

# --- 테스트 코드 ---
if __name__ == '__main__':
    game = OmokGame()
    print("렌주룰 오목 게임 테스트를 시작합니다.")

    # 3-3 금수 테스트 시나리오
    moves_for_3x3 = [
        (9, 9), (1, 1),   # 흑, 백
        (9, 10), (1, 2),  # 흑, 백
        (10, 9), (1, 3),  # 흑, 백
    ]
    for x, y in moves_for_3x3:
        game.place_stone(x, y)
    
    print("\n--- 3-3 금수 상황 ---")
    game.print_board()

    print("\n이제 흑이 (10, 10)에 두어 3-3을 만들려고 시도합니다...")
    success, message = game.place_stone(10, 10)
    print(f"결과: {success}, 메시지: {message}")
    if game.game_over:
        print(f"게임이 종료되었으며 승자는 플레이어 {game.winner} 입니다.")