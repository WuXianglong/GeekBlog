jQuery(document).ready(function() {
    // add click event for search button.
    $('img.sb-submit').click(function() {
        var keyword = $('input.sb-text').val().trim();
        if (keyword == undefined || keyword == "") {
            return false;
        }
        window.location.href = "/search/" + keyword + "/";
    });

    // implete to use left and right key to turn page.
    window.addEventListener("keydown", function(event) {
        if (event.keyCode == 37) {
            $('a.sp-prev').click();
        } else if (event.keyCode == 39) {
            $('a.sp-next').click();
        } else if (event.keyCode == 13) {
            $('img.sb-submit').click();
        }
    });
});
