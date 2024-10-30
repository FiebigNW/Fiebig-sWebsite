var height = 6; //num of guesses
var width = 5; //length of word

var row = 0; // current guess
var col = 0; //current letter

var gameOver = false;

const fiveLetterWords = [
    "APPLE",
    "BRAVE",
    "CHAIR",
    "DANCE",
    "EAGLE",
    "FLAME",
    "GRAPE",
    "HOUSE",
    "IRONY",
    "JOLLY",
    "KNACK",
    "LUCKY",
    "MANGO",
    "NOBLE",
    "OCEAN",
    "PEARL",
    "QUEST",
    "ROVER",
    "SUNNY",
    "TIGER",
    "UNITY",
    "VIVID",
    "WITTY",
    "XENON",
    "YACHT",
    "ZEBRA"
];


const randomIndex = Math.floor(Math.random() * fiveLetterWords.length);
const word = fiveLetterWords[randomIndex];


window.onload = function(){
    initialize();
}

function initialize(){ 
    //Create game board
    for(let r = 0; r < height; r++){
        for(let c = 0; c < width; c++){
            //creates <span id = 0-0 class = tile> </span>
            let tile = document.createElement("span");
            tile.id = r.toString() + "-" + c.toString();
            tile.classList.add("tile");
            document.getElementById("board").appendChild(tile);
        }
    }


    document.addEventListener("keyup", (e) => {
        if(gameOver){
           return;
        
        } 
        else if("KeyA" <= e.code && e.code <= "KeyZ"){
            if(col < width){
                let currTile = document.getElementById(row.toString() + '-' + col.toString());
                if(currTile.innerText == ""){
                    currTile.innerText = e.code[3];
                    col +=1;
                }
            }
        }
        else if(e.code == "Backspace"){
            if(0 < col && col <= width){
                col -=1;
                let currTile = document.getElementById(row.toString() + '-' + col.toString());
                currTile.innerText = "";

            }
        }
        else if(e.code == "Enter" && col == 5){
            update();
            row += 1;
            col = 0;
        }
                
        if(!gameOver && row == height){
            gameOver == true;
            document.getElementById('answer').innerText = word;
        }
  
    })
}

function update(){
    let correct = 0;
    for(let c = 0; c < width; c++){
        let currTile = document.getElementById(row.toString() + '-' + c.toString());
        let letter = currTile.innerText;

       
        if(word[c] == letter){
            currTile.classList.add("correct");
            correct += 1;
        } else if(word.includes(letter)){
            currTile.classList.add("present");
        } else {
            currTile.classList.add('absent');
        }

        if(correct == width){
            gameOver == true;
        }
    }
}

