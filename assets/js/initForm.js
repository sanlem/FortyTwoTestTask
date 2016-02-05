function initForm(form){
	initDatepicker();
	var loading = $('<h2>Loading...</h2>');

	var formContainer = $('.form-container');

	if (!form) {
		var form = $('#editForm');
	};

	form.ajaxForm({
		'dataType': 'html',
		'error': function(){
			alert('Server error :(');
			return false;
		},
		
		'success': function(data, status, xhr) {
			var html = $(data), newForm = html.find('#editForm');
			setTimeout(function() {
				loading.remove();
				newForm.appendTo(formContainer);
			}, 500);
			

			if (newForm.length > 0) {
				initForm(newForm);
			} else {
				// if no form, it means success and we need to go to main page
				location.href = "/";
			}
		},

		'beforeSend': function() {
			form.remove();
			loading.appendTo(formContainer);
		},
	});
};
$(document).ready(function() {
	initForm();
});