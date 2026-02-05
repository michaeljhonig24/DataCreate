let isProcessing = false;
let currentTurn = null;
let moveCount = 0;
const endGameText = document.querySelector('.Endgame');
const CheckersBoard = document.querySelector('tbody');
const turnText = document.querySelector('.turn')
const difficultybtns = document.querySelectorAll('.difficulty-btn');
const end = document.querySelector('.End');
const pickbuttons = document.querySelectorAll('.color-btn');
const boardbuttons = document.querySelectorAll('#game-board tbody button');

boardbuttons.forEach(button => {
    button.disabled = true;
});

pickbuttons.forEach((choice) => {
    choice.addEventListener('click', async() =>{

        const response = await fetch("/checkers/reset", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }
        });

        const data = await response.json();

        if (data.status === 'success') {
            const board = data.board;
            let position = 0;

            if(choice.innerHTML === '⚪️'){
                PlayerChoice = '⚪️';
                OpponentChoice = '⚫️';
                isBoardFlipped = false;
                
                for (let row = 0; row < 8; row += 1) {
                    for (let col = 0; col < 8; col += 1) {
                        if (board[row][col] === '-') {
                            boardbuttons[position].textContent = '';
                        } else {
                            boardbuttons[position].textContent = board[row][col];
                        }
                        position += 1;
                    }
                }
            }
            else {
                PlayerChoice = '⚫️';
                OpponentChoice = '⚪️';
                isBoardFlipped = true;

                for (let row = 7; row >= 0; row -= 1) {
                    for (let col = 7; col >= 0; col -= 1) {
                        if (board[row][col] === '-'){
                            boardbuttons[position].textContent = '';
                        }
                        else{
                                boardbuttons[position].textContent = board[row][col];
                            }
                            position += 1
                    }
                }
            }
            
            
        }
        pickbuttons.forEach(btn => {
            btn.style.animation = 'fadeout 1s linear forwards';
            
            setTimeout(()=> {
                btn.style.display = 'none';
                turnText.innerHTML = 'Pick Difficulty';
                difficultybtns.forEach(difficulty => {
                    difficulty.style.display = 'block';
                    difficulty.style.animation = 'fadein 1s linear forwards';
                })
            }, 1000)
        })
    })
})

difficultybtns.forEach ((button) => {
    button.addEventListener('click', async () => {
        selectedDifficulty = button.dataset.difficulty;

        const response = await fetch("/checkers/set_difficulty", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({difficulty: selectedDifficulty})
        });

        const data = await response.json();
        if (data.status === "success"){
            console.log("Difficutly set to:", selectedDifficulty)
        }

        difficultybtns.forEach(btn => {
            btn.style.animation = 'fadeout 1s linear forwards';
            setTimeout(() => {
                btn.style.display = 'none'}, 1000)
        });

        setTimeout(() => {
            CheckersBoard.style.animation = 'fadein 1s linear forwards';
            turnText.style.animation = 'fadein 1s linear forwards';
            currentTurn = PlayerChoice;
            turnText.innerHTML = "Player's Turn";

            boardbuttons.forEach(btn => {
                btn.disabled = false;
            });
        }, 1000);
    })
})

let selectedPiece = null;
let validMoves = [];
let isBoardFlipped = false;
let playerRegularCaptures = 0;
let playerKingCaptures = 0;
let opponentRegularCaptures = 0;
let opponentKingCaptures = 0;

function convertPosition(position){
    if (!isBoardFlipped){
        return position
    }
    const row = Math.floor(position / 8);
    const col = position % 8;
    const PythonRow = 7 - row;
    const PythonCol = 7 - col;
    return PythonRow * 8 + PythonCol;
}

function convertFromPython(position){
    if(!isBoardFlipped){
        return position;
    }
    const row = Math.floor(position / 8);
    const col = position % 8;
    
    const flippedRow = 7 - row;
    const flippedCol = 7 - col;
    
    return flippedRow * 8 + flippedCol;
}
    

function isPieceForCurrentPlayer(pieceText) {
    if (currentTurn === '⚪️') {
        if (pieceText === '⚪️' || pieceText === '♕') {
            return true;
        }
        return false;
    } else if (currentTurn === '⚫️'){
        if (pieceText === '⚫️' || pieceText === '♛'){
            return true;
        }
        return false;
    }
    return false;
}

function updateCaptureDisplay() {
    document.getElementById('player-regular-piece').textContent = OpponentChoice;
    document.getElementById('player-regular-count').textContent = playerRegularCaptures;
    
    if (OpponentChoice === '⚪️') {
        document.getElementById('player-king-piece').textContent = '♕';
    } else {
        document.getElementById('player-king-piece').textContent = '♛';
    }
    document.getElementById('player-king-count').textContent = playerKingCaptures;
    
    document.getElementById('opponent-regular-piece').textContent = PlayerChoice;
    document.getElementById('opponent-regular-count').textContent = opponentRegularCaptures;

    if (PlayerChoice === '⚪️') {
        document.getElementById('opponent-king-piece').textContent = '♕';
    } else {
        document.getElementById('opponent-king-piece').textContent = '♛';
    }
    document.getElementById('opponent-king-count').textContent = opponentKingCaptures;
    
}
boardbuttons.forEach((button, i) => {
    button.addEventListener('click', async() => {
        if (isProcessing || button.disabled || currentTurn !== PlayerChoice) {
                return;
            }
        isProcessing = true;
            
        if (selectedPiece === null && isPieceForCurrentPlayer(button.textContent)) {
            selectedPiece = i;
            button.classList.add('selected');

            const response = await fetch('/checkers/get_valid_moves', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({position: convertPosition(i),
                    player: button.textContent})
            });

            const data = await response.json();
            if (data.status === 'success'){
                validMoves = data.valid_moves.map(move => convertFromPython(move));

                validMoves.forEach(move => {
                    boardbuttons[move].classList.add('valid-move');
                });
            }
            isProcessing = false;
        }

        else if (selectedPiece === i){
            button.classList.remove('selected');

            validMoves.forEach(move => {
                boardbuttons[move].classList.remove('valid-move');
            });

            selectedPiece = null;
            validMoves = [];
            
            isProcessing = false;
        }

        else if (selectedPiece !== null && validMoves.includes(i)) {

            const response = await fetch('/checkers/make_move', {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({from: convertPosition(selectedPiece),
                    to: convertPosition(i),
                    player: boardbuttons[selectedPiece].textContent})
            });

            // move now being processed
            const data = await response.json();
            if (data.status === 'success'){
                moveCount += 1;
                const board = data.board;
                const PythonPos = convertPosition(i);
                const pythonRow = Math.floor(PythonPos / 8);
                const pythonCol = PythonPos % 8;

                boardbuttons[i].textContent = board[pythonRow][pythonCol];

                boardbuttons[selectedPiece].textContent = '';
                boardbuttons[selectedPiece].classList.remove('selected');
                validMoves.forEach(move => {
                    boardbuttons[move].classList.remove('valid-move');
                });

                if (data.captured){
                    const displayCaptured = convertFromPython(data.captured)
                    const capturedPiece = boardbuttons[displayCaptured].textContent;

                    if(currentTurn === PlayerChoice){
                        if(capturedPiece === OpponentChoice){
                            playerRegularCaptures += 1;
                        } else {
                            playerKingCaptures += 1;
                        }
                    } else {
                        if(capturedPiece === PlayerChoice){
                            opponentRegularCaptures += 1;
                        } else {
                            opponentKingCaptures += 1;
                        }
                    }
                    boardbuttons[displayCaptured].textContent = '';
                    updateCaptureDisplay();
                }

                selectedPiece = null;
                validMoves = [];

                if (data.winner) {
                    boardbuttons.forEach(btn => {
                        btn.disabled = true;
                    })

                    let winnerText = '';
                    if (data.winner === PlayerChoice) {
                        winnerText = "Player Wins!";
                    }
                    else {
                        winnerText = 'Opponent Wins!';
                    }

                    saveGameStats(selectedDifficulty, "Player", moveCount,
                        playerRegularCaptures, opponentRegularCaptures, 
                        playerKingCaptures, opponentKingCaptures
                    );
                    endGameText.textContent = winnerText;
                    end.classList.remove('End');
                    end.style.display = 'block';
                    end.style.animation = 'fadein 1s linear forward';
                    isProcessing = false;
                    return;
                }

                if (data.tie){
                    boardbuttons.forEach(btn => {
                        btn.disabled = true;
                    });
                    endGameText.textContent = "It's a Tie!";
                    end.classList.remove('End');
                    end.style.display = 'block';
                    end.style.animation = 'fadein 1s linear forwards';
                    isProcessing = false;
                    return;
                }
                
                if (currentTurn === PlayerChoice) {
                    currentTurn = OpponentChoice;
                    turnText.innerHTML = "Opponent's Turn";

                    isProcessing = true;
                    setTimeout(async () => {
                        const botResponse = await fetch('/checkers/bot_move', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({difficulty: selectedDifficulty,
                                opponent: OpponentChoice
                            })
                        });

                        const botData = await botResponse.json();
                        if (botData.status === 'success'){
                            const botMove = botData.move;
                            const fromPos = convertFromPython(botMove.from);
                            const toPos = convertFromPython(botMove.to);

                            const board = botData.board;
                            const pythonToPos = botMove.to;
                            const pythonRow = Math.floor(pythonToPos / 8);
                            const pythonCol = pythonToPos % 8
                            boardbuttons[toPos].textContent = board[pythonRow][pythonCol];
                            boardbuttons[fromPos].textContent = '';

                            if (botData.captured) {
                                const capturedPos = convertFromPython(botData.captured);
                                const capturedPiece = boardbuttons[capturedPos].textContent
                                boardbuttons[capturedPos].textContent = '';
                                
                                if (capturedPiece === PlayerChoice) {
                                    opponentRegularCaptures += 1;
                                } else {
                                    opponentKingCaptures += 1;
                                }
                                updateCaptureDisplay();
                            }

                            if (botData.winner) {
                                boardbuttons.forEach(btn => {
                                    btn.disabled = true;
                                });
                                
                                let winnerText = '';
                                if (botData.winner === PlayerChoice) {
                                    winnerText = "Player Wins!";
                                } else {
                                    winnerText = 'Opponent Wins!';
                                }

                                saveGameStats(selectedDifficulty, "Bot", moveCount,
                                    playerRegularCaptures, opponentRegularCaptures, 
                                    playerKingCaptures, opponentKingCaptures
                                );
                                endGameText.textContent = winnerText;
                                end.classList.remove('End');
                                end.style.display = 'block';
                                end.style.animation = 'fadein 1s linear forwards';
                                isProcessing = false;
                                return;
                            }

                            if (botData.tie){
                                boardbuttons.forEach(btn => {
                                    btn.disabled = true;
                                });
                                endGameText.textContent = "It's a Tie!";
                                end.classList.remove('End');
                                end.style.display = 'block';
                                end.style.animation = 'fadein 1s linear forwards';
                                isProcessing = false;
                                return;
                            }

                            currentTurn = PlayerChoice;
                            turnText.innerHTML = "Player's Turn";
                            isProcessing = false;                      
                        }
                        else {
                            currentTurn = PlayerChoice;
                            turnText.innerHTML = "Player's Turn";
                            isProcessing = false;
                        }
                    }, 500)
                } else {
                    currentTurn = PlayerChoice;
                    turnText.innerHTML = "Player's Turn";
                    isProcessing = false;
                }
            }
        }

        else if (selectedPiece !== null && !validMoves.includes(i)){
            boardbuttons[selectedPiece].classList.remove('selected');
            validMoves.forEach(move => {
                boardbuttons[move].classList.remove('valid-move');
            });
            selectedPiece = null;
            validMoves = []
            isProcessing = false;
        }

        else {
            isProcessing = false;
        }
        
    })
});

async function saveGameStats(difficulty, result, moves,
    playerRegularCaptures, opponentRegularCaptures,
    playerKingCaptures, opponentKingCaptures){
    try {
        await fetch('/checkers/save_stats', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                difficulty: difficulty,
                winner: result,
                total_moves: moves,
                player_captures: playerRegularCaptures,
                bot_captures: opponentRegularCaptures,
                player_king_captures: playerKingCaptures,
                bot_king_captures: opponentKingCaptures
            })
        });
    } catch (error) {
        console.error('Error saving game stats:', error);
    }
}

const Restartbtn = document.querySelector('.Restartbtn');
Restartbtn.addEventListener('click', () => {
    moveCount = 0;
    playerRegularCaptures = 0;
    playerKingCaptures = 0;
    opponentRegularCaptures = 0;
    opponentKingCaptures = 0;
    updateCaptureDisplay();
    end.style.opacity = '0';
    end.style.display = 'none';
    end.classList.add('End');
    CheckersBoard.style.animation = 'fadeout 1s linear forwards';
    setTimeout(() => {
        turnText.innerHTML = 'Pick';
        pickbuttons.forEach(btn => {
        btn.style.display = 'flex';
        btn.style.animation = 'fadein 1s linear forwards';
    });
    }, 1000)
    boardbuttons.forEach(btn => {
        btn.textContent = '';
        btn.disabled = true;
        btn.classList.remove('selected', 'valid-move');
    });

    playerRegularCaptures = 0;
    playerKingCaptures = 0;
    opponentRegularCaptures = 0;
    opponentKingCaptures = 0
    updateCaptureDisplay();
    selectedPiece = null;
    validMoves = []
    currentTurn = null;
})



// info panel toggle 
const infoToggle = document.querySelector('.info-toggle');
const infoPanel = document.querySelector('.info-panel');
const menuToggle = document.querySelector('.menu-toggle');
const menuPanel = document.querySelector('.menu-panel');

infoToggle.addEventListener('click', (e) => {
    
    // Close menu panel AND hide menu button
    menuPanel.classList.remove('active');
    menuToggle.classList.remove('active');
    menuToggle.style.display = 'none'; 
    
    // Toggle info panel and show info button
    infoPanel.classList.toggle('active');
    infoToggle.classList.toggle('active');
    
    // If closing info panel, show menu button again
    if (!infoPanel.classList.contains('active')) {
        menuToggle.style.display = 'block';
    }
});

menuToggle.addEventListener('click', (e) => {
    
    // Close info panel and hide info button
    infoPanel.classList.remove('active');
    infoToggle.classList.remove('active');
    infoToggle.style.display = 'none';  // hide info button
    
    // Toggle menu panel and show menu button
    menuPanel.classList.toggle('active');
    menuToggle.classList.toggle('active');
    
    // If closing menu panel, show info button again
    if (!menuPanel.classList.contains('active')) {
        infoToggle.style.display = 'block';
    }
});

// Close panels when clicking outside
document.addEventListener('click', (e) => {
    if (!infoPanel.contains(e.target) && !infoToggle.contains(e.target) && 
        !menuPanel.contains(e.target) && !menuToggle.contains(e.target)) {
        infoPanel.classList.remove('active');
        infoToggle.classList.remove('active');
        menuPanel.classList.remove('active');
        menuToggle.classList.remove('active');
        
        infoToggle.style.display = 'block';
        menuToggle.style.display = 'block';
    }
})

document.addEventListener('keydown', (e) => {
    if (e.key === 'r' && e.ctrlKey) {
        console.log('Emergency reset!');
        isProcessing = false;
        boardbuttons.forEach(btn => btn.disabled = false);
        console.log('Game unlocked!');
    }
});