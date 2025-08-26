// frontend/src/components/Game.jsx (디버깅용 console.log 추가 버전)

import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import Board from './Board';

const API_URL = "http://127.0.0.1:8000";

function Game({ settings, onGoBack }) {
    const { gameMode, aiDifficulty } = settings;

    const [gameId, setGameId] = useState(null);
    const [gameState, setGameState] = useState(null);
    const [message, setMessage] = useState("오목 게임을 시작합니다.");

    const startNewGame = useCallback(async () => {
        try {
            setMessage("새로운 게임을 생성 중입니다...");
            const response = await axios.post(`${API_URL}/api/game/new`);
            const newGameId = response.data.game_id;
            setGameId(newGameId);
            await fetchGameState(newGameId);
            setMessage("당신(흑돌)부터 시작하세요.");
        } catch (error) {
            console.error("새 게임 생성 실패:", error);
            setMessage("게임을 시작할 수 없습니다. 서버 상태를 확인하세요.");
        }
    }, []);

    useEffect(() => {
        startNewGame();
    }, [startNewGame]);

    const fetchGameState = async (id) => {
        try {
            const response = await axios.get(`${API_URL}/api/game/${id}`);
            setGameState(response.data);
        } catch (error) {
            console.error("게임 상태 불러오기 실패:", error);
        }
    };

    const handleCellClick = async (x, y) => {
        // --- 1. 클릭 이벤트 발생 확인 ---
        console.log(`%c--- 1. Cell Clicked (${x}, ${y}) ---`, 'color: blue; font-weight: bold;');
        console.log(`현재 props: gameMode='${gameMode}', aiDifficulty='${aiDifficulty}'`);
        
        if (!gameId || (gameState && gameState.game_over)) {
            console.log("-> 게임이 종료되었거나 gameId가 없어 동작 중지.");
            return;
        }
        if (gameMode === 'pvai' && gameState.current_turn !== 1) {
            console.log("-> AI 턴이므로 플레이어 클릭 무시.");
            setMessage("AI의 차례입니다. 잠시만 기다려주세요...");
            return;
        }

        try {
            // --- 2. 플레이어 수 전송 ---
            console.log("2. 플레이어의 수를 서버로 전송합니다...");
            const playerMoveResponse = await axios.post(`${API_URL}/api/game/${gameId}/move`, { x, y });
            const newGameState = playerMoveResponse.data;
            console.log("3. 서버로부터 플레이어의 수 처리 결과를 받았습니다:", newGameState);
            setGameState(newGameState);

            // --- 4. AI 호출 조건 확인 ---
            console.log("%c4. AI를 호출할 조건인지 확인합니다...", 'color: orange;');
            console.log(`   - 게임 종료 여부 (game_over): ${newGameState.game_over}`);
            console.log(`   - 게임 모드 (gameMode === 'pvai'): ${gameMode === 'pvai'}`);

            if (!newGameState.game_over && gameMode === 'pvai') {
                // --- 5. AI 호출 실행 ---
                console.log("%c5. ✅ 조건 충족. AI의 수를 요청합니다.", 'color: green; font-weight: bold;');
                setMessage("AI가 생각 중입니다...");
                const aiMoveResponse = await axios.post(`${API_URL}/api/game/${gameId}/ai-move`, {
                    difficulty: aiDifficulty,
                });
                console.log("6. 서버로부터 AI의 수 처리 결과를 받았습니다:", aiMoveResponse.data);
                setGameState(aiMoveResponse.data);
                setMessage("당신 차례입니다.");
            } else {
                console.log("%c5. ❌ 조건 불충족. AI 호출을 건너뜁니다.", 'color: red; font-weight: bold;');
            }
        } catch (error) {
            console.error("❗️ 에러 발생:", error.response ? error.response.data : error.message);
        }
    };

    const getGameStatusMessage = () => {
        if (!gameState) return "로딩 중...";
        if (gameState.game_over) {
            const winner = gameState.winner === 1 ? '흑' : '백';
            return `게임 종료! 승자: ${winner}`;
        }
        const currentPlayer = gameState.current_turn === 1 ? '흑(당신)' : '백(AI)';
        return `${currentPlayer} 차례`;
    };

    return (
        <div className="game-container">
            <h1>리액트 렌주룰 오목 - {aiDifficulty} 모드</h1>
            <div className="game-info">{getGameStatusMessage()}</div>
            {gameState ? (
                <Board boardData={gameState.board} onCellClick={handleCellClick} />
            ) : (
                <p>게임 보드를 로딩 중입니다...</p>
            )}
            <div style={{ marginTop: '20px' }}>
                <button onClick={startNewGame} style={{ padding: '10px 20px', fontSize: '1em', marginRight: '10px' }}>
                    재시작
                </button>
                <button onClick={onGoBack} style={{ padding: '10px 20px', fontSize: '1em' }}>
                    로비로 돌아가기
                </button>
            </div>
        </div>
    );
}

export default Game;