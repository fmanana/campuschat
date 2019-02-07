$(".messages").animate({ scrollTop: $(document).height() }, "fast");

function newMessage(json) {
	if($.trim(json.msg) == '') {
		return false;
	}
	const sentPlaceholder = $('#cc_user-id').attr('data-user-id') == json.sender_id ? 'sent' : 'replies';
	const avatarPlaceholder = $('#cc_user-id').attr('data-user-id') == json.sender_id ? '1' : '2';
	let newHtml = '<li class="' + sentPlaceholder + '"><img src="../static/images/avatar' + avatarPlaceholder + '.png" alt=""/>'
	+ '<p><label class="cc_sender">' + json.sender_name + '</label><br />' + json.msg + 
	'<br/><label class="cc_sent-time">' + json.sent_time + '</label></p></li>';
	$(newHtml).appendTo($('.messages-' + json.chat_id + ' ul'));
	$(".messages").animate({ scrollTop: $(document).height() }, "fast");
};

jQuery(document).ready(function($) {
	let socket = io.connect('http://' + document.domain + ':' + location.port);

	socket.on('connect', function() {
	});

	socket.on('receive_message', function(json) {
		newMessage(json);
	});

	$('.submit').on('click', function(e) {
		const time = new Date();
		socket.emit('send_message', {
			msg: $('#myMessage').val(),
			sender_id: $('#cc_user-id').attr('data-user-id'),
			sender_name: $('.wrap > p').text(),
			sent_time: time.getHours() + ":" + time.getMinutes(),
			chat_id: $('.messages').attr('data-active-chat-id')
		});
		$('#myMessage').val(null);
	});

	$(window).on('keydown', function(e) {
		if (e.which == 13) {
			$('.submit').click();
			return false;
		}
	});
});