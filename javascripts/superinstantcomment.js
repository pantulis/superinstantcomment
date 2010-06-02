var SIC = {
	setup_keys: function() {
		//code.which == 48 ('0') 
		$(document).keydown(function(code) {
			if (code.which >= 48 && code.which <= 57) {
				value = code.which - 48; 
				selector = "#audio" + value;
				SIC.play_media($(selector));
			};
		})
	},
	play_media: function(el) {
		if (el[0]) { 
			el[0].load();
			el[0].play();
		}
	},
	setup_links: function() {
		$(".click2play").click(function(eventObject){
			SIC.play_media($(this).next());
		})
	}
};

$(document).ready(function() {
	SIC.setup_keys();
	SIC.setup_links();
});

