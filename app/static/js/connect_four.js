// Single-machine Connect Four

const redPlayer = "red";
const bluePlayer = "blue";
var winCondition = 0;
var turnCount = 0;
var gravityEnabled = true;
var bottom = null;
let gameTable = [
  [0,0,0,0,0,0],
  [0,0,0,0,0,0],
  [0,0,0,0,0,0],
  [0,0,0,0,0,0],
  [0,0,0,0,0,0],
  [0,0,0,0,0,0],
  [0,0,0,0,0,0]
];

const rows = [...document.querySelectorAll(".row")];
const overlayWin = document.getElementById("overlayWin");
const overlayReset = document.getElementById("overlayReset");
const winText = document.getElementById("winText");
const selectorBlockTop = document.querySelector('.selectorBlockTop');
const modeText = document.getElementById('output');

// Gravity-enabled
// Iterate to find clicked upon object and change to player color

baseGame();

function baseGame() {
  for (let i=0; i < 6; i++) {
    for (let j=0; j < 7; j++) {
        const piecePressed = [...rows[i].children][j]
        piecePressed.addEventListener("click", function() {
          if (gravityEnabled) {
          // Regular Mode
            bottom = columnFloor(j);
            var piece = [...rows[bottom].children][j]
            if (piecePressed.classList.length === 1 && turnCount % 2 === 0) {
              turnCount += 1;
              gameTable[j][bottom] = 1;
              piece.classList.add(redPlayer)
              } else if (piecePressed.classList.length === 1 && turnCount % 2 === 1) {
              turnCount += 1;
              gameTable[j][bottom] = 2;
              piece.classList.add(bluePlayer)
            }} else {
            // 0G Mode
              if (piecePressed.classList.length === 1 && turnCount % 2 === 0) {
                turnCount += 1;
                gameTable[j][i] = 1;
                piecePressed.classList.add(redPlayer)
              } else if (piecePressed.classList.length === 1 && turnCount % 2 === 1) {
                turnCount += 1;
                gameTable[j][i] = 2;
                piecePressed.classList.add(bluePlayer)
          }
        }
        if (winCheck() === 1) {
          overlayOn(1);
          overlayWin.addEventListener("click", function() {
            changeMode(1);
          })
        } else if (winCheck() === 2) {
          overlayOn(2);
          overlayWin.addEventListener("click", function() {
            changeMode(1);
          })
        }
      })
    }
  }
}

function winCheck() {
	if (turnCount < 7) { return winCondition; }
  
	function horizontalCheck() {
		for (let row= 0; row < 6; row++) {
      const rowSet = [];
			for (let column = 6; column >= 0; column--) {
        rowSet.push(gameTable[column][row]);
      }
      
			var start = 0;
      // Check going from index 0 onwards for 4 in a row in each row iteration (loop above)
      for (let k = 0; k < rowSet.length; k++) {
      	if (k === 0) {
          start = k;
        }
        // In play if !== 0
        if (rowSet[k] !== 0) {
        	// If next piece in play and current piece and next piece are the same
        	if (rowSet[k+1] !== 0 && (rowSet[k] + rowSet[k+1]) !== 0) {
          	// If current and next three pieces the same value, win condition
          	if (rowSet[k]===rowSet[k+1] && 
            		rowSet[k+1]===rowSet[k+2] && 
                rowSet[k+2]===rowSet[k+3]) {
                
              if (rowSet[k] === 1) {
              // Red wins
								console.log("Start red horizontal win at index " + (start + 1) + 
                " in row: " + (row + 1) + ", difference: " + (k + 4 - start));
                winCondition = 1;   
              } else if (rowSet[k] === 2) {
                // Blue wins
                console.log("Start blue horizontal win at index " + (start + 1) + 
                " in row: " + (row + 1) + ", difference: " + (k + 4 - start));
                winCondition = 2;
            	}	
          	} else { start += 1;}
        	} else { start += 1;}
      	} else {start += 1;}
    	}
		}
  }
  
	function verticalCheck() {
  	for (let column = 6; column >= 0; column--) {
      const columnSet = [];
      for (let row = 0; row < 6; row++) {
        columnSet.push(gameTable[column][row]);
      }
      
    	var start = 0;
    // Check going from index 0 onwards for 4 in a row in each row iteration (loop above)
    	for (let k = 0; k < columnSet.length; k++) {
      	if (k === 0) {
        	start = k;
      	}
      	// In play if !== 0
      	if (columnSet[k] !== 0) {
        	// If next piece in play and current piece and next piece are the same
        	if (columnSet[k+1] !== 0 && (columnSet[k] + columnSet[k+1]) !== 0) {
          // If current and next three pieces the same value, win condition
          	if (columnSet[k]===columnSet[k+1] && 
            		columnSet[k+1]===columnSet[k+2] && 
            		columnSet[k+2]===columnSet[k+3]) {
                
            	if (columnSet[k] === 1) {
              	// Red wins
               	console.log("Start red vertical win at index " + 
                (start + 1) + " in row: " + (column + 1) + 
                ", difference: " + (k + 4 - start));
              	winCondition = 1;            
            	} else if (columnSet[k] === 2) {
              	// Blue wins
               	console.log("Start blue vertical win at index " + 
                (start + 1) + " in row: " + (column + 1) + 
                ", difference: " + (k + 4 - start));
              	winCondition = 2;
            	}	
          	} else { start += 1;}
        	} else { start += 1;}
      	} else {start += 1;}
    	}
  	}
  }
  
	function diagonalCheck() {
    for (let column = 0; column <= 6; column++) {
      for (let row = 0; row <= 5; row++) {
      	try {
        	if (gameTable[column][row] !== 0 && 
          (gameTable[column+1][row+1] !== 0 ||
           gameTable[column+1][row-1] !== 0 || 
           gameTable[column-1][row+1] !== 0 || 
           gameTable[column-1][row-1] !== 0)) {
           
            if (gameTable[column][row] === gameTable[column+1][row+1] && 
            		gameTable[column+1][row+1] === gameTable[column+2][row+2] && 
                gameTable[column+2][row+2] === gameTable[column+3][row+3]) {
                
              if (gameTable[column][row] === 1) {
                winCondition = 1;
               	console.log("Start red diagonal win at index " + (row + 1) + " in column " + (column + 1));
              } else if (gameTable[column][row] === 2) {
                winCondition = 2;
               	console.log("Start blue diagonal win at index " + (row + 1) + " in column " + (column + 1));
              }
              
            } else if (gameTable[column][row] === gameTable[column+1][row-1] && 
            					 gameTable[column+1][row-1] === gameTable[column+2][row-2] && 
                       gameTable[column+2][row-2] === gameTable[column+3][row-3]) {
                       
              if (gameTable[column][row] === 1) {
                winCondition = 1;
               	console.log("Start red diagonal win at index " + (row + 1) + " in column " + (column + 1));
              } else if (gameTable[column][row] === 2) {
                winCondition = 2;
               	console.log("Start blue diagonal win at index " + (row + 1) + " in column " + (column + 1));
              }
              
            } else if (gameTable[column][row] === gameTable[column-1][row+1] && 
            					 gameTable[column-1][row+1] === gameTable[column-2][row+2] && 
                       gameTable[column-2][row+2] === gameTable[column-3][row+3]) {
                       
              if (gameTable[column][row] === 1) {
                winCondition = 1;
               	console.log("Start red diagonal win at index " + (row + 1) + " in column " + (column + 1));
              } else if (gameTable[column][row] === 2) {
                winCondition = 2;
               	console.log("Start blue diagonal win at index " + (row + 1) + " in column " + (column + 1));
              }
              
            } else if (gameTable[column][row] === gameTable[column-1][row-1] && 
            					 gameTable[column-1][row-1] === gameTable[column-2][row-2] && 
                       gameTable[column-2][row-2] === gameTable[column-3][row-3]) {
                       
              if (gameTable[column][row] === 1) {
                winCondition = 1;
               	console.log("Start red diagonal win at index " + (row + 1) + " in column " + (column + 1));
              } else if (gameTable[column][row] === 2) {
                winCondition = 2;
               	console.log("Start blue diagonal win at index " + (row + 1) + " in column " + (column + 1));
              }
            }
          }
        } catch (err) {}
      }
    }
  }
  
  horizontalCheck();
  verticalCheck();
  diagonalCheck();
  return winCondition;
}

function resetBoard() {
	gameTable = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]];
  turnCount = 0;
  winCondition = 0;
	for (let i=0; i < 6; i++) {
		for (let j=0; j < 7; j++) {
   		const piecePressed = [...rows[i].children][j]
      if (piecePressed.classList.length > 1) {
        piecePressed.classList.remove(redPlayer)
        piecePressed.classList.remove(bluePlayer)
    	}
  	}
	}
}

function changeMode(n) {
	if (n === 0) { gravityEnabled = false; } else { gravityEnabled = true; }
  resetBoard();
	inputMode();
}

function inputMode() {
	if (gravityEnabled) {
  	modeText.innerHTML = "Regular Mode"
  } else {
  	modeText.innerHTML = "0G Mode"
  }
}

function columnFloor(j) {
  for (let i=0; i < 6; i++) {
    if (gameTable[j][i] === 0) {
      bottom = i;
    }
  }
  return bottom;
}

function overlayOn(n) {
	if (n === 1) {
    overlayWin.style.display = "block";
    overlayWin.style.background = "darkred";
    overlayWin.style.opacity = ".5";
    winText.innerHTML = "Red wins! Click to reset."
    winText.style.color = "white";
    winText.style.opacity = "1";
    return;
	} if (n === 2) {
    overlayWin.style.display = "block";
    overlayWin.style.background = "blue";
    overlayWin.style.opacity = ".5";
    winText.innerHTML = "Blue wins! Click to reset."
    winText.style.color = "white";
    winText.style.opacity = "1";
    return;
  } else {
 	 overlayReset.style.display = "block";
   return;
  }
}

function overlayOff() {
  overlayWin.style.display = "none";
  overlayReset.style.display = "none";
  winText.innerHTML = "";
}

function matchMakeGraphic() {
  selectorBlockTop.classList.add("matchmaking");
  selectorBlockTop.insertAdcjacentHTML('afterend', );
}

function matchMakeGraphicDisable() {
  selectorBlockTop.classList.remove("matchmaking");

}
    // POST TO BACKEND

function matchMake() {
  var ws = new WebSocket("ws://localhost:1337/");

  ws.onopen = function() {
    console.log("Connection established");
    ws.send(gameTable)
  }

  ws.onmessage = function(event) {
    var receivedMsg = event.data;
    console.log(receivedMsg);
  }
}