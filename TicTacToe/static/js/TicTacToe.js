let PlayerChoice = '';
let OpponentChoice = '';
let moveCount = 0;
let isProcessing = false;
const tieText = document.querySelector('.Tie');
const TTTboard = document.querySelector('tbody')
const turnText = document.querySelector('.turn');
const difficultybtns = document.querySelectorAll('.difficulty-btn');
const end = document.querySelector('.end');
const pickbuttons = document.querySelectorAll('.symbol-btn');
const boardbuttons = document.querySelectorAll('#game-board tbody button');

boardbuttons.forEach(button => {
    button.disabled = true;
});

pickbuttons.forEach((choice) => {
    choice.addEventListener('click', () =>{

        const response = fetch("/tictactoe/reset", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }
        });
        if(choice.innerHTML === 'X'){
            PlayerChoice = 'X';
            OpponentChoice = 'O'
        }
        else{
            PlayerChoice = 'O';
            OpponentChoice = 'X'
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

        const response = await fetch("/tictactoe/set_difficulty", {
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
            TTTboard.style.animation = 'fadein 1s linear forwards';
            turnText.style.animation = 'fadein 1s linear forwards';
            turnText.innerHTML = `Player's Turn`;

            boardbuttons.forEach(btn => {
                btn.disabled = false;
            });
        }, 1000);
    })
})

boardbuttons.forEach((button, i) => {
    button.addEventListener('click', async() =>{
        if (isProcessing || button.textContent !== '' || button.disabled) {
            return; 
        }
        
        isProcessing = true;

        if (button.textContent === ''){
            button.textContent = PlayerChoice;
            moveCount += 1;
            turnText.innerHTML = `Opponent's Turn`;
    
            const response = await fetch("/tictactoe/get_index", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({choice: button.textContent, position: i})
            });

            const data = await response.json();
            if (data.status === "success"){
                console.log('location saved');
                console.log('Current board:', data.board);

                if (data.winner === PlayerChoice){
                    tieText.innerHTML = `Player Wins!`;
                    saveGameStats(selectedDifficulty, "Player", moveCount, PlayerChoice);
                    end.style.display = 'block';
                    tieText.style.color = 'green';
                    end.style.animation = 'fadein 1s linear forwards';
                    boardbuttons.forEach(btn => btn.disabled = true);
                    isProcessing = false;
                    return;
                }

                if(data.bot_move !== null){
                    console.log('Bot move position:', data.bot_move);
                    console.log('OpponentChoice:', OpponentChoice);
                    boardbuttons[data.bot_move].textContent = OpponentChoice;
                    moveCount += 1;
                    turnText.innerHTML = "Player's Turn";

                    if (data.winner === OpponentChoice){
                        tieText.innerHTML = `Bot Wins!`;
                        saveGameStats(selectedDifficulty, "Bot", moveCount, OpponentChoice);
                        tieText.style.color = 'red';
                        boardbuttons.forEach(btn => btn.disabled = true);
                        end.style.display = 'block';
                        end.style.animation = 'fadein 1s linear forwards';
                        isProcessing = false;
                        return;
                    }
                }
            
                let isBoardFull = Array.from(boardbuttons).every(button => button.textContent !== '');
                    if (isBoardFull){
                        tieText.innerHTML = 'Tie!'
                        saveGameStats(selectedDifficulty, "Tie", moveCount, 'None');
                        end.style.display = 'block'
                        end.style.animation = 'fadein 1s linear forwards';
                    }

            }
            else{
                console.error("backend error:", data.message);
                 console.error("Full error data:", data);
            }
            isProcessing = false;
        }
    })
});

async function saveGameStats(difficulty, winner, total_moves, player_symbol){
    try {
        await fetch("/tictactoe/save_stats", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                difficulty: difficulty,
                winner: winner,
                total_moves: total_moves,
                player_symbol: player_symbol
            })
        });
    } catch (error) {
        console.error("Error saving game stats:", error);
    }
    
}

const RestartButton = document.querySelector('.Restartbtn');
    RestartButton.addEventListener('click', () => {
        moveCount = 0;
        reset();
    });

function reset(){
    end.style.animation = 'fadeout 1s linear forwards';
    TTTboard.style.animation = 'fadeout 1s linear forwards';
    setTimeout(() =>{
        tieText.style.color = 'black'
        end.style.display = 'none';
        boardbuttons.forEach(button => {
            button.textContent = ''
            button.disabled = true;
        });
        PlayerChoice = '';
        OpponentChoice = '';
        turnText.innerHTML = 'Pick';
         difficultybtns.forEach(btn => {
            btn.style.display = 'none';
        });
        pickbuttons.forEach(btn => {
            btn.style.display = 'block';
            btn.style.animation = 'fadein 1s linear forwards';
        });
    }, 1000);
}

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
    
    // Close info panel AND hide info button
    infoPanel.classList.remove('active');
    infoToggle.classList.remove('active');
    infoToggle.style.display = 'none';  // HIDE info button
    
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