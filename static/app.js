const $form = $('#word-form')
const $wordInput = $('#word')
const $resultField = $('#result')
const $scoreField = $('#score')
const $timer = $('#timer')
const $finalScore = $('#final-score')
const $gameOver = $('#game-over')
const $highScoreAlert = $('#high-score-alert')

const BASE_URL = 'http://127.0.0.1:5000'
let totalScore = 0
let gameOver = false

// this function "submits" the form without actually submitting the form
// it will prevent the form itself from making a post request and instead make the post request manually through axios
// this is so we can keep the same page shown for an entire game
$form.on('submit', async function (evt) {
    evt.preventDefault()
    if (!gameOver) {
        const word = $wordInput.val()
        $wordInput.val('')
        const score = word.length
        const response = await axios.get(`${BASE_URL}/guess`, { params: { key: word } })
        const result = response.data.result
        const validWord = displayResult(result, word, score)
        if (validWord) { addScore(score) }
    }
})

// this function checks the result from the server and adds an appropriate message to the DOM
// returns true if word is valid, false if word is not valid
function displayResult(result, word, score) {
    if (result == 'ok') {
        $resultField.html(`Correct! <b>${word.toUpperCase()}</b> is worth ${score} points!`)
        return true
    } else if (result == 'not-word') {
        $resultField.html(`Invalid guess! <b>${word.toUpperCase()}</b> is not in the dictionary!`)
        return false
    } else if (result == 'not-on-board') {
        $resultField.html(`Invalid guess! <b>${word.toUpperCase()}</b> is not on the board!`)
        return false
    }
}

// this function adds the word's score to the player's total score and updates the DOM
// it will only be called if a word is valid
function addScore(score) {
    totalScore += score
    $scoreField.text(totalScore)
}

let time = 60
let timing = setInterval(timer, 1000)

// this function will be called by setInterval
// it will count down to zero from 1 minute, after which the game will be over
function timer() {
    time -= 1
    let timeStr = time.toString()
    if (timeStr.length == 1) { timeStr = `0${timeStr}` }
    $timer.text(`0:${timeStr}`)
    if (time == '00') {
        clearInterval(timing)
        endGame()
    }
}

// this function will be called when the timer reaches zero
// it will display a Game Over message along with the player's final score
// it will also prevent any further guesses from being entered using the gameOver variable
async function endGame() {
    gameOver = true
    $finalScore.text(totalScore)
    const newHighScore = false // this will be a get request to the server to see if a new high score has been set
    if (newHighScore) { $highScoreAlert.css('display', 'block') }
    $gameOver.css('display', 'inline-block')
}