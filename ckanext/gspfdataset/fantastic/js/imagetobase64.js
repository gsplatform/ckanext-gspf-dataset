"use strict";
ckan.module('imagetobase64', function ($, _) {
	return {
		initialize: function() {
			$('#image-upload').on('change', function() {
				var file = this.files[0];
        var reader = new FileReader();
				reader.onload = function() {
          $('#form_thumbnail').val(this.result);
				}
				reader.readAsDataURL(file);;
			});
		}
	};
});
