function initForm(form){
	initDatepicker();
	var loading = $('<h2>Loading...</h2>');

	var formContainer = $('.form-container');

	if (!form) {
		var form = $('#editForm');
	};
	var controlElements = form.find('input, textarea, button');


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
				// we should enable them again
				// if we not and user refreshes tha page,
				// he would get form with disabled inputs.
				controlElements.prop('disabled', false);
				form.remove();
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
			// form.remove();
			form.prepend(loading);
			controlElements.prop('disabled', true);
		},
	});
};
$(document).ready(function() {
	initForm();
});