$(document).ready(function() {
    var queryhash = window.location.hash
    switch (queryhash) {
        case "#about":
            initialShowAbout();
            break;
        case "#contact":
            initialShowContact();
            break;
        default:
            initialShowContact();
            break;
    }
    $("h2").hide();
    $("#vcard a").hover(showVcardLabel, hideVcardLabel);
    $("#nav-about a").click(showAbout);
    $("#nav-contact a").click(showContact);
});

function showVcardLabel() {
    $("#vcard a span").show();
    $("#vcard a span").animate({
        top: "-40px",
        opacity: 1
    }, 250);
}

function hideVcardLabel() {
    $("#vcard a span").animate({
        top: "-35px",
        opacity: 0
    }, 250);
    setTimeout("$('#vcard a span').hide();", 250);
    $("#vcard a span").animate({ 
        top: "-45px",
    }, 250);
}

function initialShowAbout() {
    $("#content").hide();
    $("#geekblog").removeClass();
    $("#geekblog").addClass("about");
    $(".node").hide();
    $("#about").show();
    setTimeout("$('#content').slideDown('slow');", 1000);
}

function initialShowContact() {
    $("#content").hide();
    $("#geekblog").removeClass();
    $("#geekblog").addClass("contact");
    $(".node").hide();
    $("#contact").show();
    setTimeout("$('#content').slideDown('slow');", 1000);
}

function showAbout() {
    if ($("#geekblog").hasClass("about")){ }
    else {
        $("#content").slideUp(500);
        $(".node").fadeOut(500);
        setTimeout("$('.node').hide();", 500);
        setTimeout("$('#about').show();", 500);
        $("#content").slideDown(500);
        $("#geekblog").removeClass();
        $("#geekblog").addClass("about");
    }
}

function showContact() {
    if ($("#geekblog").hasClass("contact")){ }
    else {
        $("#content").slideUp(500);
        $(".node").fadeOut(500);
        setTimeout("$('.node').hide();", 500);
        setTimeout("$('#contact').show();", 500);
        $("#content").slideDown(500);
        $("#geekblog").removeClass();
        $("#geekblog").addClass("contact");
    }
}
