class Minesweeper {
    constructor() {
        this.difficulties = {
            easy: { rows: 9, cols: 9, mines: 10 },
            medium: { rows: 16, cols: 16, mines: 40 },
            hard: { rows: 16, cols: 30, mines: 99 }
        };
        
        this.currentDifficulty = 'easy';
        this.board = [];
        this.revealed = [];
        this.flagged = [];
        this.gameOver = false;
        this.gameWon = false;
        this.firstClick = true;
        this.timer = 0;
        this.timerInterval = null;
        
        this.initializeElements();
        this.bindEvents();
        this.startNewGame();
    }
    
    initializeElements() {
        this.gameBoard = document.getElementById('game-board');
        this.mineCountElement = document.getElementById('mine-count');
        this.flagCountElement = document.getElementById('flag-count');
        this.timerElement = document.getElementById('timer');
        this.restartBtn = document.getElementById('restart-btn');
        this.messageRestartBtn = document.getElementById('message-restart-btn');
        this.gameMessage = document.getElementById('game-message');
        this.messageTitle = document.getElementById('message-title');
        this.messageText = document.getElementById('message-text');
        this.difficultyButtons = document.querySelectorAll('.difficulty-btn');
    }
    
    bindEvents() {
        this.restartBtn.addEventListener('click', () => this.startNewGame());
        this.messageRestartBtn.addEventListener('click', () => {
            this.hideMessage();
            this.startNewGame();
        });
        
        this.difficultyButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.changeDifficulty(e.target.dataset.level);
            });
        });
        
        document.addEventListener('contextmenu', (e) => {
            if (e.target.classList.contains('cell')) {
                e.preventDefault();
            }
        });
    }
    
    changeDifficulty(level) {
        this.currentDifficulty = level;
        this.difficultyButtons.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.level === level);
        });
        this.startNewGame();
    }
    
    startNewGame() {
        this.gameOver = false;
        this.gameWon = false;
        this.firstClick = true;
        this.timer = 0;
        this.stopTimer();
        this.updateTimer();
        
        const config = this.difficulties[this.currentDifficulty];
        this.rows = config.rows;
        this.cols = config.cols;
        this.mines = config.mines;
        
        this.board = Array(this.rows).fill(null).map(() => Array(this.cols).fill(0));
        this.revealed = Array(this.rows).fill(null).map(() => Array(this.cols).fill(false));
        this.flagged = Array(this.rows).fill(null).map(() => Array(this.cols).fill(false));
        
        this.mineCountElement.textContent = this.mines;
        this.flagCountElement.textContent = this.mines;
        
        this.renderBoard();
        this.hideMessage();
    }
    
    renderBoard() {
        this.gameBoard.innerHTML = '';
        this.gameBoard.style.gridTemplateColumns = `repeat(${this.cols}, 30px)`;
        
        for (let row = 0; row < this.rows; row++) {
            for (let col = 0; col < this.cols; col++) {
                const cell = document.createElement('button');
                cell.classList.add('cell');
                cell.dataset.row = row;
                cell.dataset.col = col;
                
                cell.addEventListener('click', () => this.handleCellClick(row, col));
                cell.addEventListener('contextmenu', (e) => {
                    e.preventDefault();
                    this.handleRightClick(row, col);
                });
                
                this.gameBoard.appendChild(cell);
            }
        }
    }
    
    placeMines(excludeRow, excludeCol) {
        let minesPlaced = 0;
        
        while (minesPlaced < this.mines) {
            const row = Math.floor(Math.random() * this.rows);
            const col = Math.floor(Math.random() * this.cols);
            
            if (this.board[row][col] !== -1 && !(row === excludeRow && col === excludeCol)) {
                this.board[row][col] = -1;
                minesPlaced++;
                
                for (let dr = -1; dr <= 1; dr++) {
                    for (let dc = -1; dc <= 1; dc++) {
                        const newRow = row + dr;
                        const newCol = col + dc;
                        
                        if (this.isValidCell(newRow, newCol) && this.board[newRow][newCol] !== -1) {
                            this.board[newRow][newCol]++;
                        }
                    }
                }
            }
        }
    }
    
    isValidCell(row, col) {
        return row >= 0 && row < this.rows && col >= 0 && col < this.cols;
    }
    
    handleCellClick(row, col) {
        if (this.gameOver || this.revealed[row][col] || this.flagged[row][col]) {
            return;
        }
        
        if (this.firstClick) {
            this.firstClick = false;
            this.placeMines(row, col);
            this.startTimer();
        }
        
        this.revealCell(row, col);
        this.checkWinCondition();
    }
    
    handleRightClick(row, col) {
        if (this.gameOver || this.revealed[row][col]) {
            return;
        }
        
        this.flagged[row][col] = !this.flagged[row][col];
        this.updateCell(row, col);
        this.updateFlagCount();
    }
    
    revealCell(row, col) {
        if (!this.isValidCell(row, col) || this.revealed[row][col] || this.flagged[row][col]) {
            return;
        }
        
        this.revealed[row][col] = true;
        this.updateCell(row, col);
        
        if (this.board[row][col] === -1) {
            this.gameOver = true;
            this.stopTimer();
            this.revealAllMines();
            this.showMessage('游戏结束！', '你踩到了地雷！', false);
            return;
        }
        
        if (this.board[row][col] === 0) {
            for (let dr = -1; dr <= 1; dr++) {
                for (let dc = -1; dc <= 1; dc++) {
                    this.revealCell(row + dr, col + dc);
                }
            }
        }
    }
    
    revealAllMines() {
        for (let row = 0; row < this.rows; row++) {
            for (let col = 0; col < this.cols; col++) {
                if (this.board[row][col] === -1) {
                    this.revealed[row][col] = true;
                    this.updateCell(row, col);
                }
            }
        }
    }
    
    updateCell(row, col) {
        const cell = this.getCellElement(row, col);
        if (!cell) return;
        
        cell.classList.remove('revealed', 'flagged', 'mine');
        
        if (this.flagged[row][col]) {
            cell.classList.add('flagged');
            cell.textContent = '';
        } else if (this.revealed[row][col]) {
            cell.classList.add('revealed');
            
            if (this.board[row][col] === -1) {
                cell.classList.add('mine');
                cell.textContent = '';
            } else if (this.board[row][col] > 0) {
                cell.textContent = this.board[row][col];
                cell.classList.add(`number-${this.board[row][col]}`);
            } else {
                cell.textContent = '';
            }
        } else {
            cell.textContent = '';
        }
    }
    
    getCellElement(row, col) {
        return this.gameBoard.querySelector(`[data-row="${row}"][data-col="${col}"]`);
    }
    
    updateFlagCount() {
        const flagCount = this.flagged.flat().filter(f => f).length;
        this.flagCountElement.textContent = this.mines - flagCount;
    }
    
    checkWinCondition() {
        let revealedCount = 0;
        let correctFlags = 0;
        
        for (let row = 0; row < this.rows; row++) {
            for (let col = 0; col < this.cols; col++) {
                if (this.revealed[row][col] && this.board[row][col] !== -1) {
                    revealedCount++;
                }
                if (this.flagged[row][col] && this.board[row][col] === -1) {
                    correctFlags++;
                }
            }
        }
        
        if (revealedCount === this.rows * this.cols - this.mines) {
            this.gameWon = true;
            this.gameOver = true;
            this.stopTimer();
            this.showMessage('恭喜获胜！', `用时 ${this.timer} 秒完成游戏！`, true);
        }
    }
    
    startTimer() {
        this.timerInterval = setInterval(() => {
            this.timer++;
            this.updateTimer();
        }, 1000);
    }
    
    stopTimer() {
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
    }
    
    updateTimer() {
        this.timerElement.textContent = String(this.timer).padStart(3, '0');
    }
    
    showMessage(title, text, isWin) {
        this.messageTitle.textContent = title;
        this.messageText.textContent = text;
        this.gameMessage.classList.remove('hidden');
        
        const messageContent = this.gameMessage.querySelector('.message-content');
        messageContent.classList.remove('win', 'lose');
        messageContent.classList.add(isWin ? 'win' : 'lose');
    }
    
    hideMessage() {
        this.gameMessage.classList.add('hidden');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new Minesweeper();
});
