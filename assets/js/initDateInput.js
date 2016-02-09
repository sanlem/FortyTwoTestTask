function initDatepicker(){
	$('.datepicker').datetimepicker({
		'format': 'YYYY-MM-DD',
		'keepOpen': true,
	});
};

$(document).ready(function() {
	initDatepicker();
});
