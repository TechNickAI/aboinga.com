var home = function() {

    // Doesn't strictly need to be global, but handy for debugging
    window.moments = new window.MomentCollection();

    var renderMoments = function() {
        var cont = jQuery("#moments").append("<ul>");
	    for (var i = 0; i < window.moments.models.length; i++ ){
            var m = window.moments.models[i].attributes;
            // Why is icanhaz returning an array of jquery objects?!
		    cont.find("ul").append(window.ich.momentSummary(m));
	    }
        // Set up the handlers
        cont.find("img.delete").click(function() {
            var img = $(this);
            var m = window.moments.get(img.attr("data-id"));
            m.destroy();
            $("#moment_" + img.attr("data-id")).fadeOut().empty();
        });
        cont.show();
    };

    window.fetchMoments = function() {
	    jQuery("#moments").empty();
        window.moments.fetch({
            data: {order_by: "-created_at", format: "json"},
            success: renderMoments
        });
    };

    window.fetchMoments();
};
