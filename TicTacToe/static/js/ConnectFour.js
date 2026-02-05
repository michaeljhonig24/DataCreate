let PlayerChoice = '';
let OpponentChoice = '';
let moveCount = 0;
let selectedDifficulty = '';
let isProcessing = false;
let currentPlayer = null;
let board = Array(6).fill(null).map(() => Array(7).fill(null));

const ConnectFourBoard = document.querySelector('tbody');
const turnText = document.querySelector('.turn');
const difficultybtns = document.querySelectorAll('.difficulty-btn');
const end = document.querySelector('.end');
const pickbuttons = document.querySelectorAll('.symbol-btn');
const boardbuttons = document.querySelectorAll('#game-board tbody button');

boardbuttons.forEach(button => {
    button.disabled = true;
});

pickbuttons.forEach((choice) => {
    choice.addEventListener('click', async () => {
        const response = await fetch("/connectfour/reset", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (choice.innerHTML === '🔴') {
            PlayerChoice = '🔴';  
            OpponentChoice = '🟡';
        } else {
            PlayerChoice = '🟡';
            OpponentChoice = '🔴';
        }

        pickbuttons.forEach(btn => {
            btn.style.animation = 'fadeout 1s linear forwards';
            setTimeout(() => {
                btn.style.display = 'none';
                turnText.innerHTML = 'Pick Difficulty';
                difficultybtns.forEach(difficulty => {
                    difficulty.style.display = 'block';
                    difficulty.style.animation = 'fadein 1s linear forwards';
                });
            }, 1000);
        });
    });
});

difficultybtns.forEach((button) => {
    button.addEventListener('click', async () => {
        selectedDifficulty = button.dataset.difficulty;

        const response = await fetch("/connectfour/set_difficulty", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({difficulty: selectedDifficulty})
        });

        const data = await response.json();
        if (data.status === 'success') {
            console.log("Difficulty set to:", selectedDifficulty);
        }

        difficultybtns.forEach(btn => {
            btn.style.animation = 'fadeout 1s linear forwards';
            setTimeout(() => {
                btn.style.display = 'none';
            }, 1000);
        });

        setTimeout(() => {
            ConnectFourBoard.style.animation = 'fadein 1s linear forwards';
            turnText.style.animation = 'fadein 1s linear forwards';
            currentPlayer = PlayerChoice;
            turnText.innerHTML = "Player's Turn";

            boardbuttons.forEach(btn => {
                btn.disabled = false;
            });
        }, 1000);
    });
});

boardbuttons.forEach((button, index) => {
    button.addEventListener('click', async () => {
        if (isProcessing || button.disabled || currentPlayer !== PlayerChoice) {
            return;
        }

        const col = index % 7;


        isProcessing = true;

        const playerName = PlayerChoice === '🔴' ? 'Red' : 'Yellow';

        const response = await fetch('/connectfour/make_move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                column: col,
                player: playerName
            })
        });

        const data = await response.json();
        if (data.status === 'success') {
            updateBoard(data.board);
            moveCount += 1;

            if (data.winner) {
                endGame(data.winner, 'Player');
                return;
            }

            if (data.tie) {
                endGame('tie', 'Tie');
                return;
            }

            currentPlayer = OpponentChoice;
            turnText.innerHTML = "Opponent's Turn";

            setTimeout(async () => {
                try {
                    const opponentName = OpponentChoice === '🔴' ? 'Red' : 'Yellow';
                    const botResponse = await fetch('/connectfour/bot_move', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            difficulty: selectedDifficulty,
                            player: opponentName
                        })
                    });

                    const botData = await botResponse.json();
                    if (botData.status === 'success') {
                        updateBoard(botData.board);
                        moveCount += 1;

                        if (botData.winner) {
                            endGame(botData.winner, 'Bot');
                            return;
                        }

                        if (botData.tie) {
                            endGame('tie', 'Tie');
                            return;
                        }

                        currentPlayer = PlayerChoice;
                        turnText.innerHTML = "Player's Turn";
                        isProcessing = false;
                    } else {
                        console.error('Bot move failed');
                        currentPlayer = PlayerChoice;
                        turnText.innerHTML = "Player's Turn";
                        isProcessing = false;
                    }
                } catch (error) {
                    console.error('Bot move error:', error);
                    currentPlayer = PlayerChoice;
                    turnText.innerHTML = "Player's Turn";
                    isProcessing = false;
                }
            }, 500);
        } else {
            isProcessing = false;
        }
    });
});

function findLowestRow(col) {
    for (let row = 5; row >= 0; row--) {
        const buttonIndex = row * 7 + col;
        if (boardbuttons[buttonIndex].textContent === '') {
            return row;
        }
    }
    return -1;
}

function updateBoard(boardData) {
    for (let row = 0; row < 6; row++) {
        for (let col = 0; col < 7; col++) {
            const visualRow = 5-row;
            const buttonIndex = visualRow * 7 + col;
            const piece = boardData[row][col];
            
            if (piece === 'R') {
                boardbuttons[buttonIndex].textContent = '🔴';
            } else if (piece === 'Y') {
                boardbuttons[buttonIndex].textContent = '🟡';
            } else {
                boardbuttons[buttonIndex].textContent = '';
            }
        }
    }
}

function endGame(winner, Who_Won) {
    isProcessing = false;
    boardbuttons.forEach(btn => btn.disabled = true);

    const endGameText = document.querySelector('.Endgame');
    
    if (winner === 'tie') {
        endGameText.textContent = "It's a Tie!";
    } else if (winner === 'Red') {
        endGameText.textContent = `🔴 Wins!`;
    } else if (winner === 'Yellow') {
        endGameText.textContent = `🟡 Wins!`;
    }

    saveGameStats(selectedDifficulty, Who_Won, moveCount,
        PlayerChoice);

    end.classList.remove('end');
    end.style.display = 'table-row-group';
    end.style.animation = 'fadein 1s linear forwards';
}

async function saveGameStats(difficulty, winner, total_moves, player_symbol) {
    try {
        await fetch("/connectfour/save_stats", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                difficulty: difficulty,
                winner: winner,
                total_moves: total_moves,
                player_color: player_symbol
            })
        });
    } catch (error) {
        console.error("Error saving game stats:", error);
    }
}

const RestartButton = document.querySelector('.Restartbtn');
RestartButton.addEventListener('click', () => {
    reset();
});

function reset() {
    moveCount = 0;
    end.style.animation = 'fadeout 1s linear forwards';
    ConnectFourBoard.style.animation = 'fadeout 1s linear forwards';
    
    setTimeout(() => {
        end.style.display = 'none';
        end.classList.add('end');
        
        boardbuttons.forEach(button => {
            button.textContent = '';
            button.disabled = true;
        });

        PlayerChoice = '';
        OpponentChoice = '';
        currentPlayer = null;
        isProcessing = false;
        board = Array(6).fill(null).map(() => Array(7).fill(null));
        
        turnText.innerHTML = 'Pick';
        difficultybtns.forEach(difficulty => {
            difficulty.style.display = 'none';
        });
        pickbuttons.forEach(btn => {
            btn.style.display = 'block';
            btn.style.animation = 'fadein 1s linear forwards';
        });
    }, 1000);
}

// Info/Menu panel toggles
const infoToggle = document.querySelector('.info-toggle');
const infoPanel = document.querySelector('.info-panel');
const menuToggle = document.querySelector('.menu-toggle');
const menuPanel = document.querySelector('.menu-panel');

infoToggle.addEventListener('click', () => {
    menuPanel.classList.remove('active');
    menuToggle.classList.remove('active');
    menuToggle.style.display = 'none';

    infoPanel.classList.toggle('active');
    infoToggle.classList.toggle('active');

    if (!infoPanel.classList.contains('active')) {
        menuToggle.style.display = 'block';
    }
});

menuToggle.addEventListener('click', () => {
    infoPanel.classList.remove('active');
    infoToggle.classList.remove('active');
    infoToggle.style.display = 'none';

    menuPanel.classList.toggle('active');
    menuToggle.classList.toggle('active');

    if (!menuPanel.classList.contains('active')) {
        infoToggle.style.display = 'block';
    }
});

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
});