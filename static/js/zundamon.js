$(function () {
    const zundamon = $("#zundamon")
    const duration = $("#duration");
    const playButton = $("#play-button");
    const pauseButton = $("#pause-button");

    const keyframe = [
        { transform: 'translateY(0px)' },
        { transform: 'translateY(-300px)' }
    ];

    const timing = {
        duration: 1000,
        iterations: Infinity
    };

    let animation = null;

    playButton.on("click", function() {
        // document.getElementById("zundamon").animate(keyframe, timing);

        animation = document.getElementById("zundamon").animate([
            // keyframes
            { transform: 'rotate(360deg)' }
        ], {
            // timing options
            duration: (duration.val().length >= 1) ? Number(duration.val()) : 1000,
            iterations: Infinity
        });
    });

    pauseButton.on("click", function() {
        animation.pause();
    });
});