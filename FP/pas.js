$(function() {
    $('#nav_toggle').click(function(){
            $("header").toggleClass('open');
        $('nav').slideToggle(500);
    });

});