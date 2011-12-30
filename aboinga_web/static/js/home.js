// Doesn't strictly need to be global, but handy for debugging
window.Moments = new window.MomentCollection();

window.renderMoments = function() {
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

    container.find("img.rate").click(function() {
        var img = $(this);
        var id = img.attr("data-id");
        var stars = img.attr("data-rating");
        if (! id || ! stars ) {
            // Safety net
            return;
        }
        $("#status").html("Sending your rating...").show();
        $.ajax({
            url: window.Moments.url() + 'slot_machine',
            type: 'POST',
            data: {
                moment_id: id,
                stars: stars
            },
            success: function(data) {
                $("#moment_" + img.attr("data-id")).fadeOut();
                window.newMoment(data);
                $("#status").html("Thanks for rating! Other people think it is " + data.previous_results.avg_rating + '(' + data.previous_results.ratings + ')');
            }
        });
    });
};

window.newMoment = function(data) {
    var newMoment = $(window.ich.momentSummary(data)).hide();
    jQuery("#moments").prepend(newMoment);
    window.setupMomentHandlers(newMoment);
    newMoment.fadeIn(900);
};

window.fetchMoments = function() {
    jQuery("#moments").empty();
    window.Moments.fetch({
        data: {order_by: "-created_at", format: "json"},
        success: window.renderMoments
    });
};

// Pull in the first one
$("#status").html("Loading...").show().delay(1500).fadeOut();
$.ajax({
    url: window.Moments.url() + 'slot_machine',
    success: function(data) {
        window.newMoment(data);
        $("#status").hide();
    }
});

$(function () {
    $('#fileupload').fileupload({
        dataType: 'json',
        url: 'http://upload.aboinga.com/php/',
        limitConcurrentUploads: 2,
        limitMultiFileUploads: 4,
        done: function (e, data) {
            $.each(data.result, function (index, file) {
                $.ajax({
                    type: 'POST',
                    url: "/api/v1/moment/upload/",
                    data: { "file": file.name,
                            "expires_at": jQuery("input[name=expires_at]:checked").val(),
                            "public": jQuery("input[name=public]:checked").val()
                    },
                    success: function(data) {
                            window.newMoment(data);
                            $("#status").html("Thanks for uploading. You are awesome!").show().delay(1500).fadeOut();
                    }
                });
            });
        },
        // Callback for global upload progress events:
        progressall: function (e, data) {
            $('.fileupload-progressbar div').css('width', parseInt(data.loaded / data.total * 100, 10) + '%');
        },
        // Callback for uploads start, equivalent to the global ajaxStart event:
        start: function () {
            $('.fileupload-progressbar div').css('width', '0%');
            $('.fileupload-progressbar').fadeIn();
        },
        // Callback for uploads stop, equivalent to the global ajaxStop event:
        stop: function () {
            $('.fileupload-progressbar').fadeOut();
        }
    });
});
