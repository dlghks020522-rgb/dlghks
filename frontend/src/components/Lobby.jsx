// frontend/src/components/Lobby.jsx

import React from 'react';

function Lobby({ onStartGame }) {
    return (
        <div className="lobby-container">
            <h1>리액트 렌주룰 오목</h1>
            <h2>게임 모드 선택</h2>
            <div className="button-container">
                <button onClick={() => onStartGame('pvai', 'beginner')}>AI 대전 (초급)</button>
                <button onClick={() => onStartGame('pvai', 'intermediate')}>AI 대전 (중급)</button>
                <button disabled>AI 대전 (고급) - 준비 중</button>
                <button disabled>PvP 대전 - 준비 중</button>
            </div>
            <style>{`
                .lobby-container { text-align: center; margin-top: 50px; }
                .button-container { display: flex; flex-direction: column; align-items: center; gap: 15px; margin-top: 30px; }
                .button-container button {
                    padding: 15px 30px;
                    font-size: 1.2em;
                    width: 300px;
                    cursor: pointer;
                    border: none;
                    background-color: #4CAF50;
                    color: white;
                    border-radius: 5px;
                    transition: background-color 0.3s;
                }
                .button-container button:hover:not(:disabled) { background-color: #45a049; }
                .button-container button:disabled { background-color: #cccccc; cursor: not-allowed; }
            `}</style>
        </div>
    );
}

export default Lobby;