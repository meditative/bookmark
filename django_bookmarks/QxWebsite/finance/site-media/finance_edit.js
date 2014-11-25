function finance_row_edit() {
	var finance_rows = $('.row');
	finance_rows.addClass('special');
}
$(document).ready( function(){
	$('.row .edit').click(function()
	{
		var row = $(this).parent().parent();
		var cols = $(this).parent().parent().find('.col');
		for(var i=0; i<cols.length;i++)
		{
			var value = cols.eq(i).text().trim()
			var size = value.length+1
			cols.eq(i).text('').append('<input type="text" value="'+value+'" size="'+size+'" />')
		}
		row.addClass('special');
		$('.row .edit').off();
		return false
	});
});

$(document).ready(function()
{
	$('.row .save').click(function(event)
	{
		event.preventDefault();
		var row = $(this).parent().parent();
		var cols = $(this).parent().parent().find('.col');
		var items = [];
		items[0] = row.attr('id')
		for(var i=0; i<cols.length;i++)
		{
			var value = cols.eq(i).children().val();
			// console.log(value)
			items[i+1] = (value);
		}
		console.log(items);
		data = {finance: 'items'};
		console.log(data)
		$.get("/finances/save/", {finance: items}, function (result)
		{
			console.log('finish')
		});
		// $('.row .save').off();
		// return false
	});
});