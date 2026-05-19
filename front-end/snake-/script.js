const grid = document.getElementById('grid')
const food = {'x':8,'y':8}
const snake = {
    'alive': true,
    'bits' : [{'x':0,'y':0}],
    'move' : (x,y) => {
        let pos = snake.bits[snake.bits.length-1]
        let new_pos = {
            'x': pos.x+x,
            'y': pos.y+y
        }
        if ( 16 > new_pos.x || new_pos.x > 0 || 16 > new_pos.y || new_pos.y > 0)
        {console.log()}

        if ( 16 < new_pos.x || new_pos.x < 0 || 16 < new_pos.y || new_pos.y < 0) {
            snake.alive = false
            alert('DEATH!')
        }
        if (grid_elements[new_pos.x][new_pos.y].html.classList.contains('snake') && (x != 0 || y != 0)) {
            snake.alive = false
            alert('DEATH!')
        }

        if (snake.alive) {
            if (! grow) {snake.bits.shift()} else {grow=false}
            if (grid_elements[new_pos.x][new_pos.y].html.classList.contains('food')) {eat()}
            snake.bits.push(new_pos)
        }
    }
}
let moved = false
let grow = false
let direction = [0,0]
let grid_elements = []
let started = false
let next_dir = [0,0]

document.addEventListener('keydown', (event) => {
    console.log(event.key)
    if (event.key == 'ArrowUp' || event.key == 'w')    {
        if (direction[1] == 0) {
            next_dir = [ 0,-1]
            moved = true
        }
    }
    if (event.key == 'ArrowLeft' || event.key == 'a')  {
        if (direction[0] == 0) {
            next_dir = [-1, 0]
            moved = true
        }
    }
    if (event.key == 'ArrowDown' || event.key == 's')  {
        if (direction[1] == 0) {
            next_dir = [ 0, 1]
            moved = true
        }
    }
    if (event.key == 'ArrowRight' || event.key == 'd') {
        if (direction[0] == 0) {
            next_dir = [ 1, 0]
            moved = true
        }
    }

    if (moved) {
        snake.move(next_dir[0],next_dir[1])
        for (let line of grid_elements) {
            for (let square of line) {
                square.html.classList.remove('snake')
                }
            }
        for (let line of grid_elements) {
            for (let square of line) {
                square.html.classList.remove('food')
                }
            }
        grid_elements[food.x][food.y].html.classList.add('food')
        for (let bit of snake.bits) {
                grid_elements[bit.x][bit.y].html.classList.add('snake')
        }
    }
})

function start() {
    if (! started) {
        let x = 0
        for (x = 0; x < 16; x++) {
            let line = []
            let current_line_div = document.createElement('div')
            current_line_div.className = 'line'
            current_line_div.id = String(x)
            grid.appendChild(current_line_div)
            let y = 0
            for (y = 0; y < 16; y++) {
                let square = document.createElement('div')
                square.className = 'square'
                current_line_div.appendChild(square)
                line.push({
                    'html' : square,
                    'pos'  : {'x':x,'y':y}
                })
            }
            grid_elements.push(line)
        }
        started = true
        snake.bits = [
            {
                'x' : 8,
                'y' : 8
            }
        ]

        while (food.x == 8 && food.y == 8) {
            food.x = Math.floor(Math.random()*15)
            food.y = Math.floor(Math.random()*15)
        }
        

        setTimeout(movement,300)
    }
}

function eat () {
    let valid = false

    grow = true

    while (! valid) {
        food.x = Math.floor(Math.random()*15)
        food.y = Math.floor(Math.random()*15)
        valid = true
        for (let bit of snake.bits) {
            if ((bit.x == food.x || bit.y == food.y)) {
                valid = false
            }
        }
    }
}


function movement () {
    if (snake.alive) {
        direction = next_dir

        if (moved) {
            moved = false
        } else {
            snake.move(direction[0],direction[1])

            for (let line of grid_elements) {
                for (let square of line) {
                    square.html.classList.remove('snake')
                    }
                }
            for (let line of grid_elements) {
                for (let square of line) {
                    square.html.classList.remove('food')
                    }
                }
            grid_elements[food.x][food.y].html.classList.add('food')
            for (let bit of snake.bits) {
                    grid_elements[bit.x][bit.y].html.classList.add('snake')
                }
            }
            setTimeout(movement,300)
        }
}
