String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
};

$(document).ready(function() {
    var defaultTitle = document.title;
    var newRequestsCounter = 0;
    // remember id of newest request
    // var newestId = $('.request:first').attr('id');
    var newestId = 0;
    // 1 if descending 0 if ascending
    var ordering = 1;
    
    function updateRequests(orderChanged) {
        var url = apiUrl;
        // re-rendering
        if (ordering == 0) {
            // should pass something for asc
            url += '?order=0';
            // and nothing for desc
        };
                
        $.get(url, function(data, status){
            data.reverse().forEach(function(obj, i, data) {
                if ($('tr.request').length == 10) {           
                        $('tr.request:last').remove();
                };
                // create new row
                var row = $('<tr/>', {          
                    'class': 'row request',
                    'id': obj.id
                });
                if (obj.id > newestId) {
                    // check if this request is new
                    newestId = obj.id;
                    row.addClass('new');
                    // increment counter
                    newRequestsCounter ++;
                };
                // add method col
                $('<td/>', {
                    'class': 'col-xs-1',
                    text: obj.method
                }).appendTo(row);
                // add path col
                $('<td/>', {
                    'class': 'col-xs-6',
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
                // add priority
                $('<td/>', {
                    'class': 'col-xs-1',
                    text: obj.priority.toString()
                }).appendTo(row);
                if (newRequestsCounter > 0) {
                    document.title = '(' + newRequestsCounter.toString() + ') ' + defaultTitle;
                };
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

    $('#priorityOrder').val(1);

    $('#priorityOrder').change(function(){
        var newOrd = $(this).val();
        if (ordering != newOrd) {
            // re-rendering all requests
            $('tr.request').remove();
            ordering = newOrd;
            updateRequests(true);
        };
    });
});
