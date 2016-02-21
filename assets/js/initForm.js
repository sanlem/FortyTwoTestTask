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
	// image preview
	$('#id_image').change(function(){
  		var out = $('#output');
  		out.attr('src', window.URL.createObjectURL(this.files[0]));
  	});
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
			setTimeout(function (){
				loading.remove();
				enableControl();
				if (successMessage.length > 0) {
					formContainer.before(successMessage);
				} else {
					var newErrors = html.find('p.errors');
					var oldErrors = $('p.errors');
					removeSuccessMessage();
					oldErrors.each(function(i){
						$(this).text($(newErrors.get(i)).text());
					});
				}
			}, 500);
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
