const musicCountainer = document.querySelector('.music-container')
const playBtn = document.querySelector('#play')
const prevBtn = document.querySelector('#prev')
const nextBtn = document.querySelector('#next')
const audio = document.querySelector('#audio')
const progress = document.querySelector('.progress')
const progressContainer = document.querySelector('.progress-container')
const title = document.querySelector('#title')
const cover = document.querySelector('#cover')

// Song titles
const songs = ['Wisp - candlegrove']

// Keep track of songs
let songIndex = 0

// Initially load song info DOM
loadSong(songs[songIndex])

//Update song details
function loadSong(song) {
    title.innerText = song
    audio.src = `muse/${song}.mp3`
    if (typeof maybeObject != "undefined") {
        cover.src = `cove/${song} Cover Art.jpg`
    } else {
        cover.src = `cove/ellsee.gif`
    }
}

function playSong() {
    musicCountainer.classList.add('play')
}

function pauseSong() {

}

// Event Listeners
playBtn.addEventListener('click', () => {
    const isPlaying = musicCountainer.classList.contains('play')

    if(isPlaying) {
        pauseSong()
    } else {
        playSong()
    }
})