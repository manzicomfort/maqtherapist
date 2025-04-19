$('#start-record').click(function() {
    recognition.start();
    $('.circle').addClass('glow'); // Start glowing
});

$('#stop-record').click(function() {
    recognition.stop();
    $('.circle').removeClass('glow'); // Stop glowing
});
