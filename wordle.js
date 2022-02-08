// list of all lower case letters
const alph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'];
//MISS - 0   MISPLACED - 1   EXACT - 2
const num = [0, 1, 2];
const colors = ['#808080', '#b59f3b', '#538d4e'];

document.addEventListener("DOMContentLoaded", () => {
    setup()
    display()
    var session = new Session();

    /* document.getElementById('maze-submit').addEventListener('click', () => {
        setup();
    }); */
});

window.addEventListener("keydown", function (event) {
    if (event.defaultPrevented) {
        return; // Do nothing if the event was already processed
    }
    // conditional between typing numbers and letters
    if (!session.numbers) {
        //if finished typing letters
        if (event.key == 'Enter' && session.curr_col === 5 && session.curr_row < 6) {
            session.curr_col = 0;
            session.numbers = true;
        } else if (event.key == 'Backspace') {
            //Replaces current letter with 0
            session.curr_col = Math.min(session.curr_col, 4);

            // If starting too far, it backs by 1 (can be solved later with something when adding +1 first)
            if (session.guesses[session.curr_row][session.curr_col][0] == ' ' && session.curr_col > 0) {
                session.curr_col -= 1;
            }


            session.guesses[session.curr_row][session.curr_col][0] = ' ';

            //goes back 1 col if curr index is > 0
            session.curr_col = session.curr_col > 0 ? session.curr_col - 1 : session.curr_col;

        } else if (session.curr_col < 5 && alph.includes(event.key.toLowerCase())) {
            // If valid character pressed updates mat and increments pointer location
            session.guesses[session.curr_row][session.curr_col] = [event.key.toLowerCase(), 0];
            session.curr_col += 1;

        }
    } else {
        if (event.key == 'Enter' && session.curr_col === 5 && session.curr_row < 6) {
            session.curr_col = 0;
            session.curr_row += 1;
            session.numbers = false;
        } else if (event.key == 'Backspace') {
            // TODO -> First backspace takes two because index moves forward
            //Replaces current letter with 0
            session.curr_col = Math.min(session.curr_col, 4);

            session.guesses[session.curr_row][session.curr_col][1] = 0;

            //goes back 1 col if curr index is > 0
            session.curr_col = session.curr_col > 0 ? session.curr_col - 1 : session.curr_col;

        } else if (session.curr_col < 5 && num.includes(parseInt(event.key))) {
            // If valid character pressed updates mat and increments pointer location
            session.guesses[session.curr_row][session.curr_col] = [session.guesses[session.curr_row][session.curr_col][0], parseInt(event.key)];
            session.curr_col += 1;

        }
    }

    display();
    // Cancel the default action to avoid it being handled twice
    event.preventDefault();
}, true);



function setup() {
    session = new Session();
}

function display() {
    var canvas = document.getElementById('input-field');
    if (canvas.getContext) {
        let ctx = canvas.getContext('2d');

        ctx.font = '55px sans-serif';

        ctx.clearRect(0, 0, 1000, 1000);

        //size of rectangle
        let size = 92;
        //size of margin between ^
        let buffer = 10;
        // arbitrary number formatting the drawing to center
        let center_displacement = 158
        for (let i = 0; i < 6; i++) {
            for (let j = 0; j < 5; j++) {
                // Color of wordle
                ctx.fillStyle = colors[session.guesses[i][j][1]];
                ctx.fillRect(center_displacement + size * j + buffer * j, size * i + buffer * i, size, size);
                //outline
                ctx.strokeRect(center_displacement + size * j + buffer * j, size * i + buffer * i, size, size);
                //reset color
                ctx.fillStyle = '#000000';
                //prints leter
                ctx.fillText(session.guesses[i][j][0].toUpperCase(), center_displacement + size * j + buffer * (j + 2) + 6, size * (i + 1) + buffer * (i - 2) - 6);
            }
        }
    }
}

class Session {
    constructor() {
        // whether the input is typing results or not
        this.numbers = false;
        // typing row
        this.curr_row = 0;
        //typing col
        this.curr_col = 0;
        /*  array of guesses, complete [
            ['c', 0],
            ['r', 1],
            ['a', 0],
            ['n', 2],
            ['e', 0]
        ] */
        this.guesses = [];

        //TODO -> implement

        // computationally what level is the session at
        this.level = 0;

        // an array of the avalible words sorted from best ratio
        this.best_words = [];

        for (let i = 0; i < 6; i++) {
            this.guesses.push(new Array(5).fill([' ', 0]));
        }
    }
}