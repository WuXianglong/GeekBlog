jQuery(document).ready(function() {
    // scroll button
    var $backToTopEle = $('<div class="mobileBackToTop"></div>').appendTo($("body")).click(function() {
                $("html, body").animate({scrollTop: 0}, 800);
                return false;
            }),
        $backToTopFun = function() {
            var st = $(window).scrollTop(), winh = $(window).height();
            (st > 50) ? $backToTopEle.fadeIn() : $backToTopEle.fadeOut();
            // IE6下的定位
            if (!window.XMLHttpRequest) {
                $backToTopEle.css("top", st + winh - 166);
            }
        };
    $(window).bind("scroll", $backToTopFun);
    $backToTopFun();
    // add click event for search button.
    $('a.submit-button').click(function() {
        var keyword = $('input.search-text').val().trim();
        if (keyword == undefined || keyword == "") {
            return false;
        }
        window.location.href = "/search/" + keyword + "/";
    });
    // header menu and search button
    $('.header-main').on('click', 'a', function() {
        if($(this).hasClass('menu-button')) {
            if($('body').hasClass('menu-active')) {
                $('body').removeClass('menu-active');
                setTimeout(function(){
                    $('#slide-menu').hide();
                }, 300);
            } else {
                $('body').addClass('menu-active');
                $('#slide-menu').show();
            }
        } else if($(this).hasClass('search-button'))
            $('#drop-down-search').slideToggle('fast');
    });
});
