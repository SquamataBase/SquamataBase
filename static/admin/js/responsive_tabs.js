// modified from http://jsfiddle.net/syahrasi/us8uc/
// also works with nested tabs (one level deep max)
$(document).ready(function() {
    
    $(".tabs-menu > li[class='current'] > a").each(function() {
        $($(this).attr("href")).css("display", "block");
    });

    $(".tabs-menu a").click(function(event) {
        event.preventDefault();
        var parent_tab = "#" + $(this).parents(".tab-content").attr("id");
        $(this).parent().addClass("current");
        $(this).parent().siblings().removeClass("current");
        var tab = $(this).attr("href");
        var child_tab = $(tab).find(".tabs-menu > li[class='current'] > a").attr("href");
        $(".tab-content").not(tab).not(parent_tab).css("display", "none");
        $(tab).show();
        $(child_tab).show();
    });
    
});