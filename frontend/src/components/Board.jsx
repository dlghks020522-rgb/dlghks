// frontend/src/components/Board.jsx

import React from 'react';

function Board({ boardData, onCellClick }) {
    return (
        <div className="board">
            {boardData.map((row, y) =>
                row.map((cell, x) => (
                    <div key={`${y}-${x}`} className="cell" onClick={() => onCellClick(x, y)}>
                        {cell === 1 && <div className="stone black"></div>}
                        {cell === 2 && <div className="stone white"></div>}
                    </div>
                ))
            )}
        </div>
    );
}

export default Board;