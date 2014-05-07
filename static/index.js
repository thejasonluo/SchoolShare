// background cycling thing

function cycleImages() {
    var $active = $('#background_cycler .active');
    var $next = ($('#background_cycler .active').next().length > 0) ? $('#background_cycler .active').next() : $('#background_cycler img:first');
    $next.css('z-index',2);
    $active.fadeOut(1500,function(){
	$active.css('z-index',1).show().removeClass('active');
	$next.css('z-index',3).addClass('active');
    });
}

$(window).load(function(){
    $('#background_cycler').fadeIn(1500);
    setInterval('cycleImages()', 8000);
})

// scrolling thing

$(function() {
  $('a[href*=#description]:not([href=#])').click(function() {
    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
      if (target.length) {
        $('html,body').animate({
          scrollTop: target.offset().top
        }, 1000);
        return false;
      }
    }
  });
});
