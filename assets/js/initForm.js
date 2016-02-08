function enableControl(form) {
	var controlElements = form.find('input, textarea, button');
	controlElements.prop('disabled', false);
};

function disableControl(form) {
	var controlElements = form.find('input, textarea, button');
	controlElements.prop('disabled', true);
};

function initForm(form){
	initDatepicker();
	var loading = $('<h2>Loading...</h2>');
	var formContainer = $('.form-container');
	if (!form) {
		var form = $('#editForm');
	};
	enableControl(form);
	form.ajaxForm({
		'dataType': 'html',
		'error': function(){
			alert('Server error :(');
			return false;
		},
		
		'success': function(data, status, xhr) {
			var html = $(data), newForm = html.find('#editForm');
			form.remove();
			if (newForm.length > 0) {
				setTimeout(function() {
					loading.remove();
					newForm.appendTo(formContainer);
					initForm(newForm);
				}, 500);
			} else {
				// if no form, it means success and we need to go to main page
				location.href = "/";
			}
		},

		'beforeSend': function() {
			form.prepend(loading);
			disableControl(form);
		},
	});
};
$(document).ready(function() {
	initForm();
});
