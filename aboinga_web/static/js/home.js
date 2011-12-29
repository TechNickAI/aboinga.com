var home = function() {

    // Doesn't strictly need to be global, but handy for debugging
    window.Moments = new window.MomentCollection();

    var renderMoments = function() {
        var cont = jQuery("#moments").append("<ul>");
	    for (var i = 0; i < window.Moments.models.length; i++ ){
            var m = window.Moments.models[i].attributes;
            // Why is icanhaz returning an array of jquery objects?!
		    cont.find("ul").append(window.ich.momentSummary(m));
	    }
        // Set up the handlers
        window.setupMomentHandlers(cont);
        cont.show();
    };

    window.setupMomentHandlers = function(container) {
        // Set up the handlers
        container.find("img.delete").click(function() {
            var img = $(this);
            var id = img.attr("data-id");
            if (! id) {
                // Safety net so we don't delete all
                return;
            }
            $.ajax({
                url: window.Moments.url() + id,
                type: 'DELETE',
                success: function() {
                    $("#moment_" + img.attr("data-id")).fadeOut(900);
                    window.setTimeout(function() {
                        $("#moment_" + img.attr("data-id")).remove();
                    }, 950);
                }
            });
        });

    };

    window.fetchMoments = function() {
	    jQuery("#moments").empty();
        window.Moments.fetch({
            data: {order_by: "-created_at", format: "json"},
            success: renderMoments
        });
    };

    window.fetchMoments();
};
