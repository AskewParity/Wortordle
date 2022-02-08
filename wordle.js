const alph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'];


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
    if (event.key == 'Enter' && session.curr_col === 5 && session.curr_row < 6) {
        session.curr_col = 0;
        session.curr_row += 1;
    } else if (event.key == 'Backspace') {
        //Replaces current letter with 0
        if (session.guesses[session.curr_row][session.curr_col] == ' ' && session.curr_col > 0) {
            session.curr_col -= 1;
        }
        session.guesses[session.curr_row][session.curr_col] = ' ';

        //goes back 1 col if curr index is > 0
        session.curr_col = session.curr_col > 0 ? session.curr_col - 1 : session.curr_col;

    } else if (session.curr_col < 5 && alph.includes(event.key.toLowerCase())) {
        session.guesses[session.curr_row][session.curr_col] = event.key.toLowerCase();
        session.curr_col += 1;

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

        let size = 92;
        let buffer = 10;
        let center_displacement = 158
        for (let i = 0; i < 6; i++) {
            for (let j = 0; j < 5; j++) {
                ctx.strokeRect(center_displacement + size * j + buffer * j, size * i + buffer * i, size, size);
                ctx.fillText(session.guesses[i][j].toUpperCase(), center_displacement + size * j + buffer * (j + 2) + 6, size * (i + 1) + buffer * (i - 2) - 6);
            }
        }
    }
}

class Session {
    constructor() {
        this.curr_row = 0;
        this.curr_col = 0;
        this.guesses = [];

        for (let i = 0; i < 6; i++) {
            this.guesses.push(new Array(5).fill(' '));
        }
    }
}