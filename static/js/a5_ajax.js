$(function(){
	$('#search_by_date').click(function(){
		$.ajax({
			url: '/declarations',
			data: $('form').serialize(),
			type: 'GET'
		});
	});
});