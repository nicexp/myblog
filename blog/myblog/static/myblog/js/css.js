$(function(){
  	var submenu2 = $("#menu-item-2")
	var submenu3 = $("#menu-item-3")

	$(".menu-has-children").on({mouseenter:function(e){
		var point = this
		$(point).find("ul").css({
			"display":"block"
		})
		setTimeout(function(){
			$(point).find("ul").css({
			"transition":"opacity 1s",
			"-webkit-transition":"opacity 1s",
			"-moz-transition":"opacity 1s",
			"-o-transition":"opacity 1s",
			"opacity":"1"
			});
		}, 100)
		$(".headbg").css({
			"background":"rgba(255,255,255, 1)"
		})
		},mouseleave:function(e){
			var point = this
			$(point).find("ul").css({
			"transition":"opacity 1s",
			"-webkit-transition":"opacity 1s",
			"-moz-transition":"opacity 1s",
			"-o-transition":"opacity 1s",
			"opacity":"0"
			})
			setTimeout(function(){
				$(point).find("ul").css({
					"display":"none"
				})}, 100)
			$(".headbg").css({
			"background":"rgba(255,255,255, 0.8)"
		})
		}
	})

	$(".menu-item").on({
		mouseenter:function(e){
			$(".headbg").css({
			"background":"rgba(255,255,255, 1)"
		})
		},
		mouseleave:function(e){
			$(".headbg").css({
			"background":"rgba(255,255,255, 0.8)"
		})
		}
	})
});

$(document).ready(function(){
	$(".tab-hd span:first").addClass("current");
	$(".tab-bd-con:gt(0)").hide();
	$(".tab-hd span").mouseover(function(){
	$(this).addClass("current").siblings("span").removeClass("current");
	$(".tab-bd-con:eq("+$(this).index()+")").show().siblings(".tab-bd-con").hide().addClass("current");
	});
});

$(document).ready(function(){
	$(".mark-nav li").on({
		mouseenter:function(e){
			var tLeft = this.offsetLeft+30;
			var tTop = this.offsetTop-30;
			var content = this.innerHTML;
			var num = content.match(/(\d+)/);
			var str = num[0]+"个话题";
			var tooltip = $(".tooltip")
			tooltip.html(str);
			tooltip.css({"left":tLeft, "top":tTop})
			tooltip.show()
		},
		mouseleave:function(e){
			$(".tooltip").hide();
		}
		})
});

