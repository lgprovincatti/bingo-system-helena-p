const letterElement =
    document.getElementById('letter')

const numberElement =
    document.getElementById('number')

const drawButton =
    document.getElementById('draw-button')

const autoButton =
    document.getElementById('auto-button')

const pauseButton =
    document.getElementById('pause-button')

const resetButton =
    document.getElementById('reset-button')

const cardsButton =
    document.getElementById(
        'cards-button'
    )

const fullscreenButton =
    document.getElementById(
        'fullscreen-button'
    )

const intervalSelect =
    document.getElementById(
        'interval-select'
    )

const lastNumberContainer =
    document.getElementById('last-number')

const bingoGrid =
    document.getElementById('bingo-grid')

const historyVisual =
    document.getElementById('history-visual')

const historyText =
    document.getElementById('history-text')

const serverUrlElement =
    document.getElementById(
        'server-url'
    )

const protocol =
    window.location.protocol === 'https:'
        ? 'wss'
        : 'ws'

const socket = new WebSocket(
    `${protocol}://${window.location.host}/ws`
)

let paused = false

let automaticRunning = false

generateGrid()

serverUrlElement.innerText =
    window.location.origin

socket.onmessage = (event) => {

    const data = JSON.parse(event.data)

    switch (data.type) {

        case 'DRAW_NUMBER':

            updateCurrentNumber(
                data.payload.current_number
            )

            updateGrid(
                data.payload.drawn_numbers,
                data.payload.current_number.number
            )

            updateHistory(
                data.payload.drawn_numbers
            )

            break

        case 'RESET_GAME':

            resetScreen()

            break

        case 'GAME_FINISHED':

            automaticRunning = false

            autoButton.disabled = false

            alert(
                'Todos os números foram sorteados.'
            )

            break
    }
}

function generateGrid() {

    for (let i = 1; i <= 75; i++) {

        const cell =
            document.createElement('div')

        cell.classList.add('grid-cell')

        cell.id = `cell-${i}`

        cell.innerText = i

        bingoGrid.appendChild(cell)
    }
}

function updateCurrentNumber(data) {

    letterElement.innerText =
        data.letter

    numberElement.innerText =
        data.number

    lastNumberContainer.classList.remove(
        'animate'
    )

    void lastNumberContainer.offsetWidth

    lastNumberContainer.classList.add(
        'animate'
    )
}

function updateGrid(
    drawnNumbers,
    currentNumber
) {

    document
        .querySelectorAll('.grid-cell')
        .forEach(cell => {

            cell.classList.remove('current')
        })

    drawnNumbers.forEach(number => {

        const cell =
            document.getElementById(
                `cell-${number}`
            )

        if (!cell) {
            return
        }

        cell.classList.add('drawn')
    })

    const currentCell =
        document.getElementById(
            `cell-${currentNumber}`
        )

    if (currentCell) {

        currentCell.classList.add(
            'current'
        )
    }
}

function updateHistory(drawnNumbers) {

    historyVisual.innerHTML = ''

    historyText.innerHTML = ''

    drawnNumbers.forEach(number => {

        const ball =
            document.createElement('div')

        ball.classList.add('history-ball')

        ball.innerText = number

        historyVisual.appendChild(ball)
    })

    historyText.innerHTML =
        drawnNumbers.join(' • ')
}

function resetScreen() {

    letterElement.innerText = '-'

    numberElement.innerText = '--'

    historyVisual.innerHTML = ''

    historyText.innerHTML = ''

    pauseButton.innerText = 'Pausar'

    paused = false

    automaticRunning = false

    autoButton.disabled = false

    document
        .querySelectorAll('.grid-cell')
        .forEach(cell => {

            cell.classList.remove(
                'drawn',
                'current'
            )
        })
}

drawButton.addEventListener(
    'click',
    async () => {

        await fetch('/draw', {
            method: 'POST'
        })
    }
)

autoButton.addEventListener(
    'click',
    async () => {

        if (automaticRunning) {
            return
        }

        automaticRunning = true

        autoButton.disabled = true

        await fetch('/auto/start', {
            method: 'POST'
        })
    }
)

pauseButton.addEventListener(
    'click',
    async () => {

        if (!automaticRunning) {
            return
        }

        if (!paused) {

            await fetch('/auto/pause', {
                method: 'POST'
            })

            pauseButton.innerText =
                'Continuar'

            paused = true
        }
        else {

            await fetch('/auto/resume', {
                method: 'POST'
            })

            pauseButton.innerText =
                'Pausar'

            paused = false
        }
    }
)

resetButton.addEventListener(
    'click',
    async () => {

        const confirmed = confirm(
            'Deseja iniciar um novo bingo?'
        )

        if (!confirmed) {
            return
        }

        await fetch('/reset', {
            method: 'POST'
        })
    }
)

cardsButton.addEventListener(
    'click',
    async () => {

        window.open(
            '/cards/download?quantity=40',
            '_blank'
        )
    }
)

fullscreenButton.addEventListener(
    'click',
    async () => {

        if (!document.fullscreenElement) {

            await document.documentElement
                .requestFullscreen()

            fullscreenButton.innerText =
                'Sair da Tela Cheia'
        }
        else {

            await document.exitFullscreen()

            fullscreenButton.innerText =
                'Tela Cheia'
        }
    }
)

intervalSelect.addEventListener(
    'change',
    async (event) => {

        const seconds =
            event.target.value

        await fetch(
            `/auto/interval/${seconds}`,
            {
                method: 'POST'
            }
        )
    }
)