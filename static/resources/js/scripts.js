$(document).ready(function(){ 

	/* Add/ Remove Sticky Navigation */ 

	$('.js--features').waypoint(function(direction){
		if (direction == "down") {
			$('nav').addClass('sticky');
		} else {
			$('nav').removeClass('sticky');
		}
	}, {
		offset: '60px;' 
	});

	/* Scroll to section on click event */

	$('.js--scroll-to-plans').click(function(){
		$('html, body').animate({scrollTop: $('.js--section-plans').offset().top}, 1500);
	});

	$('.js--scroll-to-start').click(function(){
		$('html, body').animate({scrollTop: $('.js--features').offset().top}, 1000);
	});

	/* CSS Tricks: Smooth Scrolling to elements with ID */

	$(function() {
  		$('a[href*=#]:not([href=#])').click(function() {
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

	/* Add Animations on scroll */

	$('.js--wp-1').waypoint(function(direction) {
		$('.js--wp-1').addClass('animated fadeIn');
	}, {
		offset: '50%'
	});
	$('.js--wp-2').waypoint(function(direction) {
		$('.js--wp-2').addClass('animated fadeInUp');
	}, {
		offset: '50%'
	});
	$('.js--wp-3').waypoint(function(direction) {
		$('.js--wp-3').addClass('animated fadeIn');
	}, {
		offset: '60%'
	});
	$('.js--wp-4').waypoint(function(direction) {
		$('.js--wp-4').addClass('animated pulse');
	}, {
		offset: '50%'
	});

	/* Mobile Navigation */
	$('.js--nav-icon').click(function() {
		var nav = $('.js--main-nav');
		var icon = $('.js--nav-icon i')

		nav.slideToggle(200);
		/* switch from hamburger to cross icon */
		if (icon.hasClass('ion-navicon-round')){
			icon.addClass('ion-close-round');
			icon.removeClass('ion-navicon-round');
		} else {
			icon.addClass('ion-navicon-round');
			icon.removeClass('ion-close-round');
		}
	});

//	/* gmaps.js: Google Maps plugin */
// 	var map = new GMaps({
//	  div: '.map',
//	  lat: 40.0047528,
//	  lng: -75.0,
//	  zoom: 12
//	});
//
//	map.addMarker({
//	  lat: 40.0047528,
//	  lng: -75.1180329,
//	  title: 'Philadelphia',
//	  infoWindow: {
//		content: '<p>Our Philadelphia HQ</p>'
//	  }
//	});
	$('.popup-gallery').magnificPopup({
		delegate: 'a',
		type: 'image',
		tLoading: 'Loading image #%curr%...',
		mainClass: 'mfp-img-mobile',
		gallery: {
			enabled: true,
			navigateByImgClick: true,
			preload: [0,1] // Will preload 0 - before current, and 1 after the current image
		},
		image: {
			tError: '<a href="%url%">The image #%curr%</a> could not be loaded.',
			titleSrc: function(item) {
				return item.el.attr('title') + '<small>by LuckyVR Ltd.</small>';
			}
		}
	});
    
    $('.matterport-container').magnificPopup({
      delegate: 'a', // child items selector, by clicking on it popup will open
      type: 'iframe'
      // other options
    });
    
    $(".loadingSign").hide();
    
    $('#contact_submit').on('click', function(e) {
        $(".loadingSign").show();
        var form = $('.contact-form');
        var url= form.attr('action');
        var data = form.serialize();

        $.ajax({
            type: "POST",
            url: url,
            data: data,
        }).done(function(result){
            console.log(JSON.stringify(result));
            form.trigger("reset");
            $(".loadingSign").hide();
            $.alert({
                title: 'Dear Customer,',
                content: 'Appreciate your inquiry, our engineer will contact you shortly!',
                animation: 'scale',
                closeAnimation: 'scale',
                buttons: {
                    okay: {
                        text: 'Close',
                        btnClass: 'btn btn-full'
                    }
                }
            });
        }).fail(function() {
            $.alert({
                title: 'Dear Customer,',
                content: 'Appreciate your inquiry, but our contact system under the maintenance.Please send email to <strong>jielin88@hotmail.com</strong>, our engineer will contact you shortly!',
                animation: 'scale',
                closeAnimation: 'scale',
                buttons: {
                    okay: {
                        text: 'Close',
                        btnClass: 'btn btn-full'
                    }
                }
            });
            $(".loadingSign").hide();
        });

        e.preventDefault();
    });

});

	



