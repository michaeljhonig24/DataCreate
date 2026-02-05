const infoToggle = document.querySelector('.info-toggle');
const infoPanel = document.querySelector('.info-panel');
const statsToggle = document.querySelector('.stats-toggle-btn');
const statsPanel = document.querySelector('.stats-panel');

infoToggle.addEventListener('click', () => {
    infoPanel.classList.toggle('active');
    infoToggle.classList.toggle('active');

});


statsToggle.addEventListener('click', () => {

    statsPanel.classList.toggle('active');
    statsToggle.classList.toggle('active');

    if (statsPanel.classList.contains('active')) {
        loadStats();
    }

});

async function loadStats() {
    try {
        const response = await fetch('/stats');
        const data = await response.json();
        // Tic-Tac-Toe stats
        const ttt = data.tictactoe;

        document.getElementById('ttt-total').textContent = ttt.total_games;
        document.getElementById('ttt-player-wins').textContent = ttt.player_wins;
        document.getElementById('ttt-bot-wins').textContent = ttt.bot_wins;
        document.getElementById('ttt-ties').textContent = ttt.ties;
        document.getElementById('ttt-average-moves').textContent = Math.round(ttt.avg_moves);

        let tttWinRate = 0;
        if (ttt.total_games > 0) {
            tttWinRate = Math.round((ttt.player_wins / ttt.total_games) * 100);
        }
        document.getElementById('ttt-win-rate').textContent = tttWinRate + '%';

        const checkers = data.checkers;
        document.getElementById('checkers-total').textContent = checkers.total_games;
        document.getElementById('checkers-player-wins').textContent = checkers.player_wins;
        document.getElementById('checkers-bot-wins').textContent = checkers.bot_wins;
        document.getElementById('checkers-player-captures').textContent = checkers.player_captures;
        document.getElementById('checkers-bot-captures').textContent = checkers.bot_captures;
        document.getElementById('checkers-player-king-captures').textContent = checkers.player_king_captures;
        document.getElementById('checkers-bot-king-captures').textContent = checkers.bot_king_captures;
        document.getElementById('checkers-average-moves').textContent = Math.round(checkers.avg_moves);

        let checkersWinRate = 0;
        if (checkers.total_games > 0) {
            checkersWinRate = Math.round((checkers.player_wins / checkers.total_games) * 100);
        }
        document.getElementById('checkers-win-rate').textContent = checkersWinRate + '%';

        const connectfour = data.connectfour;
        document.getElementById('connectfour-total').textContent = connectfour.total_games;
        document.getElementById('connectfour-player-wins').textContent = connectfour.player_wins;
        document.getElementById('connectfour-bot-wins').textContent = connectfour.bot_wins;
        document.getElementById('connectfour-ties').textContent = connectfour.ties;
        document.getElementById('connectfour-average-moves').textContent = Math.round(connectfour.avg_moves);

        let cfWinRate = 0;
        if (connectfour.total_games > 0) {
            cfWinRate = Math.round((connectfour.player_wins / connectfour.total_games) * 100);
        }
        document.getElementById('connectfour-win-rate').textContent = cfWinRate + '%';

    } catch (error) {
        console.error('Error loading stats:', error);
        alert('Failed to load statistics. Please try again later.');
    }
}
document.addEventListener('click', (e) => {
    if (!infoPanel.contains(e.target) && !infoToggle.contains(e.target) &&
        !statsPanel.contains(e.target) && !statsToggle.contains(e.target)) {
        infoPanel.classList.remove('active');
        infoToggle.classList.remove('active');
        statsPanel.classList.remove('active');
        statsToggle.classList.remove('active');
        
        infoToggle.style.display = 'block';
        statsToggle.style.display = 'block';
    }
});