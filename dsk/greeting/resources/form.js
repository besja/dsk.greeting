(function($) {
     $(document).ready(function() {

        
        $("#dsk-greeting a.images-select-image").on("click", function() {
        	var uid = $(this).attr("data-uid");
        	$("#dsk-greeting a.images-select-image").removeClass("active");
        	$(this).addClass("active"); 
     		$("#dsk-greeting #form-widgets-image").val(uid); 
        	return false; 

        })


     })
})(jQuery);