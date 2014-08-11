jQuery(document).ready(function () {
    $(".omo-list:gt(0), .all-month:gt(0)").hide();
    $(".one-month:first").addClass("selected");
    $(".year:first").addClass("selected");
    $(".omo-toggle").click(function () {
        var E = $(this),
            F = E.closest(".one-month"),
            A = F.children(".omo-list");
        if (!F.hasClass("selected")) {
            var _current = $(".one-month.selected"),
                _list = _current.children(".omo-list");
            F.addClass("selected");
            _current.removeClass("selected");
            _list.slideUp();
            A.slideDown()
        } else {
            F.removeClass("selected");
            A.slideUp()
        }
    });
    $(".year-title").click(function (A) {
        A.preventDefault();
        var G = $(this),
            F = G.parent().parent(".year"),
            H = F.children(".all-month");
        if (!F.hasClass("selected")) {
            var _cyear = $(".year.selected"),
                _mons = _cyear.children(".all-month"),
                _cmon = _mons.children(".one-month.selected"),
                _clist = _cmon.children(".omo-list");
            _cyear.removeClass("selected");
            _cmon.removeClass("selected");
            _mons.slideUp();
            _clist.slideUp();
            F.addClass("selected");
            H.slideDown();
            H.children(".one-month").eq(0).addClass("selected").children(".omo-list").show()
        } else {
            var _cmon = H.children(".one-month.selected"),
                _clist = _cmon.children(".omo-list");
            _cmon.removeClass("selected");
            _clist.slideUp();
            F.removeClass("selected");
            H.slideUp()
        }
    })
});
