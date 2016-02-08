function enableControl() {
	var form = $('#editForm');
	var controlElements = form.find('input, textarea, button');
	controlElements.prop('disabled', false);
};

function disableControl() {
	var form = $('#editForm');
	var controlElements = form.find('input, textarea, button');
	controlElements.prop('disabled', true);
};

function removeSuccessMessage() {
	var successMessage = $('p.message');
	if (successMessage.length > 0){
		successMessage.remove();
	};
}

function clearErrors() {
	$('p.errors').text('');
};

function initForm(){
	var loading = $('<h2>Loading...</h2>');
	var formContainer = $('.form-container');
	var form = $('#editForm');

	enableControl(form);
	form.ajaxForm({
		'dataType': 'html',
		'error': function(){
			alert('Server error :(');
			removeSuccessMessage();
			enableControl();
			return false;
		},
		
		'success': function(data, status, xhr) {
			var html = $(data), successMessage = html.find('p.message');
			enableControl();
			loading.remove();
			if (successMessage.length > 0) {
				setTimeout(function() {
					formContainer.before(successMessage);
					// initForm(newForm);
				}, 500);
			} else {
				var newErrors = html.find('p.errors');
				var oldErrors = $('p.errors');
				removeSuccessMessage();
				// $('p.errors:first').text('hello');
				oldErrors.each(function(i){
					$(this).text($(newErrors.get(i)).text());
				});
			}
		},

		'beforeSend': function() {
			form.prepend(loading);
			disableControl();
			clearErrors();
		},
	});
};
$(document).ready(function() {
	initForm();
});
