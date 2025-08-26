// frontend/src/App.jsx (디버깅용 console.log 추가 버전)
"use client";

import React, { useState } from 'react';
import Lobby from './components/Lobby';
import Game from './components/Game';
import './App.css';

function App() {
    const [gameSettings, setGameSettings] = useState(null);

    const handleStartGame = (mode, difficulty) => {
        console.log(`%c[App.jsx] Lobby에서 게임 시작 버튼 클릭! mode: ${mode}, difficulty: ${difficulty}`, 'color: purple; font-weight: bold;');
        setGameSettings({ mode, difficulty });
    };

    const handleGoBackToLobby = () => {
        setGameSettings(null);
    };

    // --- 렌더링 직전에 gameSettings 상태를 확인하는 로그 ---
    console.log("%c[App.jsx] 컴포넌트 렌더링 중... 현재 gameSettings:", "color: purple; font-weight: bold;", gameSettings);

    return (
        <div className="App">
            {!gameSettings ? (
                <Lobby onStartGame={handleStartGame} />
            ) : (
                <Game settings={gameSettings} onGoBack={handleGoBackToLobby} />
            )}
        </div>
    );
}

export default App;