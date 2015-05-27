$(document).ready(function() {
    $(".nav-toggle").on("click", function () {
        $(".navigation").slideToggle(function () {
            $(".navigation").css('overflow', 'visible');
        })
    });

    $(".tothetop").click(function () {
        $("html, body").animate({scrollTop: 0}, 500);
    });
});