//lel js scoping/binding/whatever it's called
function generate_handler(i) {
    return function () {
        if ($(this).is(':checked')) {
            $("#section-" + (i + 1)).fadeIn('slow');
        }
    }
}

//TODO: switch to event delegation pattern
$(document).ready(function () {
    for (var i = 1; i <= 4; i++) {
        $('#section-' + (i + 1)).hide();
        $(".ing" + i).on("click", generate_handler(i));
    }
});