function initDatepicker(){
	$('.datepicker').datetimepicker({
		'format': 'YYYY-MM-DD'
	});
};

$(document).ready(function() {
	initDatepicker();
});
