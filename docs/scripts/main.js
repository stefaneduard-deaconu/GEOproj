window.onload = function(e) {
    // var wrapper = document.getElementById('wrapper-with-image')
    // wrapper.style.backgroundImage = '/images/triangles.svg'
    // var sliver = document.select('#wrapper-with-image .after-content .sliver')
    // console.log(sliver)
    // var footer = document.select('#wrapper-with-image .after-content')
    // console.log(footer)
    // footer.style.background = 'linear-gradient(120deg, black 5%, white 5%, black, black)'
    var footer = document.getElementsByClassName('after-content')[0]
    footer.style.background = 'linear-gradient(120deg, black 5%, white 5%, black, black)'

    var millis = 0
    function animateFooter() {
        // console.log(millis)
        millis += 10
        if (millis > 0) {
            black = 5 + millis / 10
            white = 5
            footer.style.background = `linear-gradient(120deg, black ${black}%, white ${white}%, black, black)`
        } else {if (millis < -618){
            footer.style.background = 'black'
        } else {
            fblack = 0
            r = 255 / (-millis / 6)
            g = 255 / (-millis / 6)
            b = 255 / (-millis / 6)
            white = `rgb(${r},${g},${b})`
            footer.style.background = `linear-gradient(120deg, black 5%, ${white} 5%, black 50%)`
        }}

        // console.log(millis)
        if (millis > 1000){
            millis = -1500
            console.log('one more sec')
        }
    }
    // animateFooter.seconds = 0

    var interval = setInterval(animateFooter, 40) // every 30 / 10 = 3 secs
    // console.log(footerBackground)


    var content = document.querySelector('#wrapper-with-image .content')
    content.addEventListener('scroll', function() {
        console.log('scroll')
    })
}
