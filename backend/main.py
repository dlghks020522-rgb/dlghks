# backend/main.py
#.venv\Scripts\activate
# cd backend > python -m uvicorn main:app --reload
# 새 터미널 cd frontend > npm run dev

import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai import find_best_move

# 1단계에서 만든 OmokGame 클래스를 가져옵니다.
from game import OmokGame

app = FastAPI()

# CORS 설정: React 앱(예: localhost:3000)에서 오는 요청을 허용합니다.
# 중요: 프로덕션 환경에서는 "*" 대신 실제 프론트엔드 도메인을 명시해야 합니다.
origins = [
    "http://localhost:3000",
    "http://localhost:5173", # Vite 사용 시 기본 포트
    "*" # 개발 편의를 위해 모든 출처 허용 (배포 시에는 수정 필요)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 여러 게임 세션을 관리하기 위한 인-메모리 딕셔너리
# key: game_id, value: OmokGame 인스턴스
games = {}

# 요청 Body의 데이터 형식을 정의하기 위한 Pydantic 모델
class MoveRequest(BaseModel):
    x: int
    y: int

# --- API 엔드포인트 정의 ---
class AIRequest(BaseModel):
    difficulty: str

@app.post("/api/game/new")
def new_game():
    """새로운 오목 게임을 생성합니다."""
    game_id = str(uuid.uuid4())
    game = OmokGame(board_size=19)
    games[game_id] = game
    print(f"새 게임 생성됨: {game_id}")
    return {"game_id": game_id}

@app.get("/api/game/{game_id}")
def get_game_state(game_id: str):
    """특정 게임의 현재 상태를 반환합니다."""
    game = games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="게임을 찾을 수 없습니다.")
    
    return {
        "board": game.board,
        "current_turn": game.current_turn,
        "winner": game.winner,
        "game_over": game.game_over
    }

@app.post("/api/game/{game_id}/move")
def place_stone_api(game_id: str, move: MoveRequest):
    """게임에 돌을 놓습니다."""
    game = games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="게임을 찾을 수 없습니다.")
    
    success, message = game.place_stone(move.x, move.y)
    
    if not success:
        # 유효하지 않은 수(예: 이미 돌이 있는 곳)에 대한 처리
        raise HTTPException(status_code=400, detail=message)

    return {
        "message": message,
        "board": game.board,
        "current_turn": game.current_turn,
        "winner": game.winner,
        "game_over": game.game_over
    }

@app.post("/api/game/{game_id}/ai-move")
def ai_move_api(game_id: str, request: AIRequest):
    """AI의 다음 수를 계산하고 게임 상태를 업데이트합니다."""
    game = games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="게임을 찾을 수 없습니다.")
    if game.game_over:
        raise HTTPException(status_code=400, detail="게임이 이미 종료되었습니다.")

    # AI 로직을 호출하여 최적의 수를 찾음
    move = find_best_move(game, request.difficulty)

    if move is None:
        raise HTTPException(status_code=500, detail="AI가 수를 찾을 수 없습니다.")

    x, y = move
    success, message = game.place_stone(x, y)

    if not success:
        # AI가 잘못된 수를 선택한 경우 (이론상 발생하기 어려움)
        raise HTTPException(status_code=500, detail=f"AI의 내부 오류: {message}")

    return {
        "message": f"AI가 ({x}, {y})에 수를 두었습니다.",
        "board": game.board,
        "current_turn": game.current_turn,
        "winner": game.winner,
        "game_over": game.game_over
    }