$(".messages").animate({ scrollTop: $(document).height() }, "fast");

function newMessage(message) {
	if($.trim(message) == '') {
		return false;
	}
	$('<li class="sent"><img src="../static/images/dragi.png" alt="" /><p>' + message + '</p></li>').appendTo($('.messages ul'));
	$('.message-input input').val(null);
	$('.contact.active .preview').html('<span>You: </span>' + message);
	$(".messages").animate({ scrollTop: $(document).height() }, "fast");
};

// $('.submit').click(function() {
//   newMessage();
// });

// $(window).on('keydown', function(e) {
//   if (e.which == 13) {
//     newMessage();
//     return false;
//   }
// });

jQuery(document).ready(function($) {
	var socket = io.connect('http://' + document.domain + ':' + location.port);

	socket.on('message', function(msg) {
		newMessage(msg);
	});

	$('.submit').on('click', function() {
		socket.send($('#myMessage').val(), $('#myMessage').attr('name'));
		$('#myMessage').val(null);
	});
});