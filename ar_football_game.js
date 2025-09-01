AFRAME.registerComponent('game-logic', {
  init: function () {
    console.log('Game logic component initialized.');
    this.player = document.getElementById('player');
    this.aiOpponent = document.getElementById('ai-opponent');
    this.ball = document.getElementById('ball');
    this.scoreDisplay = document.getElementById('score-display');

    this.keys = {};
    this.speed = 0.05;
    this.possessionDistance = 0.3;
    this.goalZ = 1.5;
    this.playerScore = 0;
    this.aiScore = 0;

    this.gameState = 'loose_ball';

    this.apiKey = 'test-api-key';

    this.ballVelocity = new THREE.Vector3();
    this.shootForce = 0.1;

    this.onKeyDown = this.onKeyDown.bind(this);
    this.onKeyUp = this.onKeyUp.bind(this);

    window.addEventListener('keydown', this.onKeyDown);
    window.addEventListener('keyup', this.onKeyUp);
  },

  onKeyDown: function (event) {
    this.keys[event.key] = true;
    if (event.key === ' ' && this.gameState === 'player_possession') {
      this.shootBall();
    }
  },

  onKeyUp: function (event) {
    this.keys[event.key] = false;
  },

  tick: function () {
    this.updatePlayerPosition();
    this.updateGameState();
    if (this.gameState === 'ai_possession' || this.gameState === 'loose_ball') {
      this.getAIAction();
    }
    this.updateBallPosition();
    this.checkGoal();
  },

  updatePlayerPosition: function () {
    const position = this.player.getAttribute('position');

    if (this.keys['w']) {
      position.z -= this.speed;
    }
    if (this.keys['s']) {
      position.z += this.speed;
    }
    if (this.keys['a']) {
      position.x -= this.speed;
    }
    if (this.keys['d']) {
      position.x += this.speed;
    }

    this.player.setAttribute('position', position);
  },

  updateGameState: function () {
    if (this.gameState === 'loose_ball') {
      const playerPosition = this.player.getAttribute('position');
      const aiOpponentPosition = this.aiOpponent.getAttribute('position');
      const ballPosition = this.ball.getAttribute('position');

      const playerDistanceToBall = playerPosition.distanceTo(ballPosition);
      const aiDistanceToBall = aiOpponentPosition.distanceTo(ballPosition);

      if (playerDistanceToBall < this.possessionDistance) {
        this.gameState = 'player_possession';
      } else if (aiDistanceToBall < this.possessionDistance) {
        this.gameState = 'ai_possession';
      }
    }
  },

  getAIAction: async function () {
    const ballOwner = this.gameState === 'player_possession' ? 'player' : (this.gameState === 'ai_possession' ? 'ai' : 'none');
    try {
      const response = await fetch('/api/football/ai/action', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': this.apiKey,
        },
        body: JSON.stringify({ ball_owner: ballOwner }),
      });
      const data = await response.json();
      this.updateAIOpponentPosition(data.action);
    } catch (error) {
      console.error('Error getting AI action:', error);
    }
  },

  updateAIOpponentPosition: function (action) {
    const position = this.aiOpponent.getAttribute('position');
    const ballPosition = this.ball.getAttribute('position');

    switch (action) {
      case 'dribble_forward':
        position.z -= this.speed;
        break;
      case 'track_opponent':
        const direction = ballPosition.clone().sub(position).normalize();
        position.add(direction.multiplyScalar(this.speed));
        break;
      // Other actions can be implemented here
    }
    this.aiOpponent.setAttribute('position', position);
  },

  updateBallPosition: function () {
    const ballComponent = this.ball.components.position;
    if (!ballComponent) return; // Ensure component is ready
    const ballPosition = ballComponent.data;


    if (this.gameState === 'player_possession') {
      const playerPosition = this.player.getAttribute('position');
      ballPosition.copy(playerPosition);
      ballPosition.z -= 0.3;
    } else if (this.gameState === 'ai_possession') {
      const aiOpponentPosition = this.aiOpponent.getAttribute('position');
      ballPosition.copy(aiOpponentPosition);
      ballPosition.z -= 0.3;
    } else { // loose_ball
      ballPosition.add(this.ballVelocity);
      this.ballVelocity.multiplyScalar(0.98);
    }

    this.ball.setAttribute('position', ballPosition);
  },

  shootBall: function () {
    this.gameState = 'loose_ball';
    this.ballVelocity.z = -this.shootForce;
  },

  checkGoal: function () {
    const ballPosition = this.ball.getAttribute('position');

    if (ballPosition.z < -this.goalZ) {
      this.playerScore++;
      this.updateScoreDisplay();
      this.resetGame();
    } else if (ballPosition.z > this.goalZ) {
      this.aiScore++;
      this.updateScoreDisplay();
      this.resetGame();
    }
  },

  updateScoreDisplay: function () {
    this.scoreDisplay.textContent = `Player: ${this.playerScore} - AI: ${this.aiScore}`;
  },

  resetGame: function () {
    this.player.setAttribute('position', { x: 0, y: 0.25, z: 0.5 });
    this.aiOpponent.setAttribute('position', { x: 0, y: 0.25, z: -0.5 });
    this.ball.setAttribute('position', { x: 0, y: 0.1, z: -0.1 });
    this.ballVelocity.set(0, 0, 0);
    this.gameState = 'loose_ball';
  }
});
