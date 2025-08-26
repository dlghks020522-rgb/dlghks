// frontend/src/components/Game.jsx (props 이름 완전 수정)
"use client";

// frontend/src/components/Game.jsx (props 이름 완전 수정)

import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import Board from './Board';

const API_URL = "http://127.0.0.1:8000";

function Game({ settings, onGoBack }) {
    const { mode, difficulty } = settings;

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
        console.log(`--- Cell Clicked (${x}, ${y}) ---`);
        console.log(`현재 props: mode='${mode}', difficulty='${difficulty}'`);

        if (!gameId || (gameState && gameState.game_over)) {
            console.log("-> 게임이 종료되었거나 gameId가 없어 동작 중지.");
            return;
        }
        if (mode === 'pvai' && gameState.current_turn !== 1) {
            console.log("-> AI 턴이므로 플레이어 클릭 무시.");
            setMessage("AI의 차례입니다. 잠시만 기다려주세요...");
            return;
        }

        try {
            const playerMoveResponse = await axios.post(`${API_URL}/api/game/${gameId}/move`, { x, y });
            const newGameState = playerMoveResponse.data;
            setGameState(newGameState);

            if (!newGameState.game_over && mode === 'pvai') {
                setMessage("AI가 생각 중입니다...");
                const aiMoveResponse = await axios.post(`${API_URL}/api/game/${gameId}/ai-move`, {
                    difficulty,
                });
                setGameState(aiMoveResponse.data);
                setMessage("당신 차례입니다.");
            }
        } catch (error) {
            console.error("에러 발생:", error.response ? error.response.data : error.message);
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
            <h1>리액트 렌주룰 오목 - {difficulty} 모드</h1>
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