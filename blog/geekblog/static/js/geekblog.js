/* turn to the page with given page num when click pagination buttons */
function turnToPage(page_num) {
    var url = window.location.href, pathName = window.location.pathname, retUrl = "";
    // if pathName is empty, means current page is home page.
    if (pathName === "" || pathName === undefined) {
        retUrl = url + "/page/" + page_num + "/";
    } else if (pathName === "/") {
        retUrl = url + "page/" + page_num + "/";
    } else {
        // match page & cate & tag.
        var matchs = pathName.match(/^\/(page|tag(?:\/[a-z_]+)|search(?:\/.+)|cate(?:\/[a-z_]+))\/(?:(\d+)\/)?/i);
        if (matchs && matchs[1] && matchs[2]) {
            retUrl = url.replace(/(page|tag(?:\/[a-z_]+)|search(?:\/.+)|cate(?:\/[a-z_]+))\/\d+/, matchs[1] + "/" + page_num);
        } else if (matchs && matchs[1] && matchs[2] === undefined) {
            retUrl = url + page_num + "/";
        }
    }
    if (retUrl != "")
        window.location.href = retUrl;
}

jQuery(document).ready(function() {
    // add click event for search button.
    $('img.sb-submit').click(function() {
        var keyword = $('input.sb-text').val().trim();
        if (keyword == undefined || keyword == "") {
            return false;
        }
        window.location.href = window.location.origin + "/search/" + keyword + "/";
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
