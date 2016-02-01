String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}

$(document).ready(function() {
    var defaultTitle = document.title;
    var newRequestsCounter = 0;
    // remember id of newest request
    var newest_id = $('.request:first').attr('id');
    
    function getRequests() {
    	var url = "/requests_api/?pk=" + newest_id.toString();
    	$.get(url, function(data, status){
    	newest_id = data[0]['id'];
    	// alert(data.length);
    	data.reverse().forEach(function(obj, i, data) {
    		$('tr.request:last').remove();
    		// create new row
    		var row = $('<tr></tr>').attr({ id: obj.id, class: ['request', 'new', 'row'].join(' ')});
    		// add method col
    		$('<td></td>').attr({ class : 'col-xs-1'}).text(obj.method).appendTo(row);
    		// add path col
    		$('<td></td>').attr({ class : 'col-xs-7'}).text(obj.absolute_path).appendTo(row);
    		// add is_ajax vol
    		$('<td></td>').attr({ class : 'col-xs-1'}).text(obj.is_ajax.toString().capitalize()).appendTo(row);
    		// add timestamp
    		$('<td></td>').attr({ class : 'col-xs-3'}).text(Date(obj.timestamp).toString()).appendTo(row);
    		// increment counter
    		newRequestsCounter += 1;
    		document.title = '(' + newRequestsCounter.toString() + ') ' + defaultTitle;
    		$('table.requests').prepend(row).fadeIn();
    	});
    });

    function setAsViewed() {
    	$('tr.request.new').removeClass('new');
    	document.title = defaultTitle;
    	newRequestsCounter = 0;
    };

    //$(body).on('mousemove', setAsViewed());
    $(document).on('keyup', setAsViewed());
};
    setInterval(function(){ 
       getRequests();
	}, 5000);
});
