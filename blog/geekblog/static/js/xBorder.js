jQuery(function(a) {
	a("#expand_collapse,.archives-yearmonth").css({
		cursor: "pointer"
	});
	a("#archives ul li ul.archives-monthlisting").hide();
	a("#archives ul li ul.archives-monthlisting:first").show();
	a("#archives ul li span.archives-yearmonth").click(function() {
		a(this).next().slideToggle("fast");
		return false
	});
	a("#expand_collapse").toggle(function() {
		a("#archives ul li ul.archives-monthlisting").slideDown("fast"),
		a(this).text("折叠所有")
	},
	function() {
		a("#archives ul li ul.archives-monthlisting").slideUp("fast"),
		a(this).text("展开所有")
	})
});

$(function() {
	$("#content .post-content img, #content a,header a,#footer a, .same_cat_posts a,#content .postinfo img,aside a,.wumii-image-block a").each(function(b) {
		if (this.title) {
			var c = this.title;
			var a = 30;
			$(this).mouseover(function(d) {
				this.title = "";
				$("body").append('<div id="tooltip">' + c + "</div>");
				$("#tooltip").css({
					left: (d.pageX + a) + "px",
					top: d.pageY + "px",
					opacity: "0.8"
				}).show(250)
			}).mouseout(function() {
				this.title = c;
				$("#tooltip").remove()
			}).mousemove(function(d) {
				$("#tooltip").css({
					left: (d.pageX + a) + "px",
					top: d.pageY + "px"
				})
			})
		}
	})
});
jQuery(document).ready(function(a) {
	a("#shang").mouseover(function() {
		up()
	}).mouseout(function() {
		clearTimeout(fq)
	}).click(function() {
		a("body").fadeTo("100", 0.5,
		function() {
			$body.animate({
				scrollTop: 0
			},
			700,
			function() {
				a("body").fadeTo("100", 1)
			})
		})
	});
	a("#xia").mouseover(function() {
		dn()
	}).mouseout(function() {
		clearTimeout(fq)
	}).click(function() {
		a("body").fadeTo("100", 0.5,
		function() {
			$body.animate({
				scrollTop: a(document).height()
			},
			700,
			function() {
				a("body").fadeTo("100", 1)
			})
		})
	});
	a(".comments_number").click(function() {
		a("body").fadeTo("100", 0.5,
		function() {
			$body.animate({
				scrollTop: a("#comment").offset().top
			},
			700,
			function() {
				a("body").fadeTo("100", 1)
			})
		})
	})
});
function up() {
	$wd = $(window);
	$wd.scrollTop($wd.scrollTop() - 1);
	fq = setTimeout("up()", 10)
}
function dn() {
	$wd = $(window);
	$wd.scrollTop($wd.scrollTop() + 1);
	fq = setTimeout("dn()", 10)
} (jQuery);
$("html,body").dblclick(function(b) {
	var a = $.event.fix(b);
	if (a.target.tagName == "BODY") {
		$('#layout').fadeTo("100", 0.5,
		function() {
			$body.animate({
				scrollTop: 0
			},
			800,
			function() {
				$('#layout').fadeTo("100", 1)
			})
		})
	}
});
$('#layout').dblclick(function(e) {
	e.stopPropagation()
});

$(function() {
	$('#content h2 a').click(function(e) {
		e.preventDefault();
		var htm = '页面加载中...',
		i = 9,
		t = $(this).html(htm).unbind('click'); (function ct() {
			i < 0 ? (i = 9, t.html(htm), ct()) : (t[0].innerHTML += '.', i--, setTimeout(ct, 200))
		})();
		window.location = this.href
	})
});
$("html,body").dblclick(function(b) {
	var a = $.event.fix(b);
	if (a.target.tagName == "BODY") {
		$('#layout').fadeTo("100", 0.5,
		function() {
			$body.animate({
				scrollTop: 0
			},
			800,
			function() {
				$('#layout').fadeTo("100", 1);
			});
		});
	}
});
$('#layout').dblclick(function(e) {
	e.stopPropagation();
});

$(document).ready(function() {
	$(".toggle_content").hide();
	$(".toggle_title").click(function() {
		$(this).toggleClass("active").next().slideToggle("fast");
		return false
	})
});

$(".link-back2top").hide();
$(window).scroll(function() {
	if ($(this).scrollTop() > 100) {
		$(".link-back2top").fadeIn();
	} else {
		$(".link-back2top").fadeOut();
	}
});
$(".link-back2top a").click(function() {
	$("body,html").animate({
		scrollTop: 0
	},
	800);
	return false;
});

$(".pingpart").click(function() {
	$(this).css({
		color: "#b3b3b3"
	});
	$(".commentshow").hide(400);
	$(".pingtlist").show(400);
	$(".commentpart").css({
		color: "#A0A0A0"
	})
});
$(".commentpart").click(function() {
	$(this).css({
		color: "#b3b3b3"
	});
	$(".pingtlist").hide(400);
	$(".commentshow").show(400);
	$(".pingpart").css({
		color: "#A0A0A0"
	})
});
$('.report, .report1').click(function() {
	$body.animate({
		scrollTop: $('#comment').offset().top
	},
	400)
});

$body=(window.opera)?(document.compatMode=="CSS1Compat"?$('html'):$('body')):$('html,body');$('.commentnav a').live('click', function(e){e.preventDefault();$.ajax({type: "GET",url: $(this).attr('href'),beforeSend: function(){$('.commentnav').remove();$('.commentlist').remove();$('#loading-comments').slideDown();},dataType: "html",success: function(out){result = $(out).find('.commentlist');nextlink = $(out).find('.commentnav');$('#loading-comments').slideUp(500);$('#loading-comments').after(result.fadeIn(800));$('.commentlist').after(nextlink);}});})

jQuery(document).ready(function($){
$('.reply').click(function() {
    var atid = '"#' + $(this).parent().parent().attr("id") + '"';
    var atname = $(this).parent().find('.name').text();
$("#comment").attr("value","<a href=" + atid + ">@" + atname + " </a>").focus();
});
$('.cancel_comment_reply a').click(function() {
$("#comment").attr("value",'');
});
})

$(".readmore a").hover(function(){ 
							if(!$(this).is(":animated")){
							$(this).animate({right:'-6px'},210).animate({right:'0px'},180)
							.animate({right:'-3px'},150).animate({right:'0px'},130)
							.animate({right:'-1px'},100).animate({right:'0px'},80);
							}
				});




