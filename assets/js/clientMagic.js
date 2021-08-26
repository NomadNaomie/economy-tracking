/*
*   Yes, JQuery is here solely so I can do the fade in easily. 
*   I now can't find the StackOverflow I copypasted. Oops.
*/
$(window).scroll(function () {
    $('.fade-in').each(function (i) {
        var bottom_of_object = $(this).offset().top;
        var bottom_of_window = $(window).scrollTop() + $(window).height();
        if (bottom_of_window > bottom_of_object) {
            $(this).animate({
                'opacity': '1'
            }, 1500);
         }
     });
});