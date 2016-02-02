String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}

$(document).ready(function() {
    var defaultTitle = document.title;
    var newRequestsCounter = 0;
    // remember id of newest request
    var newestId = $('.request:first').attr('id');
    
    function updateRequests() {
    	var url = "/requests_api/?pk=" + newestId.toString();
    	$.get(url, function(data, status){
    	newestId = data[0]['id'];
    	data.reverse().forEach(function(obj, i, data) {
    		if ($('tr.request').length == 10) {           
					$('tr.request:last').remove();
			};
    		// create new row
    		var row = $('<tr/>', {          
				'class': 'row request new',
				'id': obj.id
			});
    		// add method col
    		$('<td/>', {
				'class': 'col-xs-1',
				text: obj.method
			}).appendTo(row);
    		// add path col
    		$('<td/>', {
				'class': 'col-xs-7',
				text: obj.absolute_path     
			}).appendTo(row);
    		// add is_ajax col
    		$('<td/>', {
				'class': 'col-xs-1',
				text: obj.is_ajax.toString().capitalize()
			}).appendTo(row);
    		// add timestamp
    		$('<td/>', {
    			'class': 'col-xs-3',
    			text: Date(obj.timestamp).toString()
    		}).appendTo(row);
    		// increment counter
    		newRequestsCounter ++;
    		document.title = '(' + newRequestsCounter.toString() + ') ' + defaultTitle;
    		$('.header').after(row).fadeIn();
    	});
    });
};
    setInterval(function(){ 
       updateRequests();
	}, 1000);

	function setAsViewed() {
    	$('tr.request.new').removeClass('new');
    	document.title = defaultTitle;
    	newRequestsCounter = 0;
    };

    $(window).focus(function(){
    	setTimeout(function(){
    		setAsViewed();
    	}, 500);
    });

    $(document).bind('mousemove keydown scroll', function(){
    	setAsViewed();
    });
});
