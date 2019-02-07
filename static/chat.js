$(".messages").animate({ scrollTop: $(document).height() }, "fast");

function newMessage(message) {
	if($.trim(message) == '') {
		return false;
	}
	$('<li class="sent"><img src="../static/images/avatar1.png" alt="" /><p>' + message + '</p></li>').appendTo($('.messages ul'));
	$('.message-input input').val(null);
	$(".messages").animate({ scrollTop: $(document).height() }, "fast");
};

jQuery(document).ready(function($) {
	let socket = io.connect('http://' + document.domain + ':' + location.port);

	socket.on('message', function(msg) {
		newMessage(msg);
	});

	$('.submit').on('click', function() {
		socket.send($('#myMessage').val(), $('#myMessage').attr('name'));
	});

	$(window).on('keydown', function(e) {
		if (e.which == 13) {
			socket.send($('#myMessage').val(), $('#myMessage').attr('name'));
			return false;
		}
	});
});