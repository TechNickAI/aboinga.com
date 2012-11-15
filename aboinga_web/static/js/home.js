
// Doesn't strictly need to be global, but handy for debugging
window.Moments = new window.MomentCollection();
window.Captions = new window.CaptionCollection();
window.cachedMoments = {};

var HomeRouter = window.Backbone.Router.extend({
    routes: {
        "/moment/:slug": "pullMoment"
    },
    pullMoment: function( slug ){
        $.ajax({
            url: window.Moments.url() + '?slug=' + escape(slug),
            success: function(data) {
                var moment = window.setupMoment(data.objects[0]);
                jQuery("#moments").empty().append(moment);
                moment.show("clip", "slow");
                jQuery("img[title]").tooltip();
            }
        });
    }
});
HomeRouter.bind("all",function(route, router) {
    Pilotfish('fire', 'core:thickClientView', {path: route});
});


$(document).ready(function() {
    var app_router = new window.HomeRouter();
    // Start Backbone history a neccesary step for bookmarkable URL's
    window.Backbone.history.start();
    jQuery("img[title]").tooltip();
});


window.setupMomentHandlers = function(container) {
    //// Set up the handlers


    // Delete
    container.find("img.delete").click(function() {
        if (! window.confirm ("Delete?") ) {
            return;
        }
        var img = $(this);
        var id = img.attr("data-id");
        if (! id) {
            // Safety net so we don't delete all
            return;
        }
        $(".tooltip").remove();
        $.ajax({
            url: window.Moments.url() + id,
            type: 'DELETE',
            success: function() {
                $("#moment_" + img.attr("data-id")).fadeOut(900);
                window.setTimeout(function() {
                    $("#moment_" + img.attr("data-id")).remove();
                }, 950);
                $(window).trigger("aboinga:delete");
                Pilotfish('recorder', 'delete');
            }
        });
    });

    // Ratings
    container.find("img.rate").click(function() {
        var img = $(this);
        var id = img.attr("data-id");
        var stars = img.attr("data-rating");
        if (! id || ! stars ) {
            // Safety net
            return;
        }
        $(".tooltip").remove();
        $.ajax({
            url: window.Moments.url() + 'slot_machine',
            type: 'POST',
            data: {
                moment_id: id,
                stars: stars
            },
            success: function(data) {
                $("#moment_" + img.attr("data-id")).fadeOut();
                Pilotfish('speaker', "Thanks for rating. The overall rating is <b>" + data.previous_results.avg_rating + '</b> (' + data.previous_results.ratings + ')', {'timeout': 3000, 'type': 'success'});
                window.slugUrlChange(data.slug);
                $(window).trigger("aboinga:rate", stars);
                Pilotfish('recorder', 'rate');
            }
        });
    });


    // Next
    container.find("img.next").click(function() {
        var img = $(this);
        var id = img.attr("data-id");
        $(".tooltip").remove();
        $.ajax({
            url: window.Moments.url() + 'slot_machine',
            success: function(data) {
                $("#moment_" + img.attr("data-id")).fadeOut();
                window.slugUrlChange(data.slug);
                $(window).trigger("aboinga:next");
                Pilotfish('recorder', 'next');
            }
        });
    });

    // Caption
    container.find(".newCaption input").blur(submitCaption).bind("keypress", function(e) {
        var code = e.keyCode || e.which;
        if (code === 13) { //Enter keycode
            submitCaption(e);
        }
    });

    var submittedCaptions = [];
    function submitCaption(e) {
        var target = e.currentTarget || e.srcElement;
        var text = $.trim($(target).val());
        if (! text ) {
            return;
        }
        if (submittedCaptions[text]) {
            // Simple dupe check
            return;
        }
        submittedCaptions[text] = 1;
        var caption = {text: text, moment_id: $(target).attr("data-moment-id")};
        window.Captions.create(caption, {
            success: function() {
                Pilotfish('speaker', "Thanks for adding a caption!", {'timeout': 3000, 'type': 'success'});
                container.find(".momentCaptions").html(window.ich.momentCaptionTemplate(caption));
                $(window).trigger("aboinga:new_caption");
                Pilotfish('recorder', 'new_caption');
            }
        });
    }
};

window.addCaption = function(container, captions) {
    // Pick a random one of the captions
    if (captions.length === 0) {
        return 0;
    }
    var i = Math.floor(Math.random()*captions.length);
    container.find(".momentCaptions").append(window.ich.momentCaptionTemplate(captions[i]));
    return i;
};

window.setupMoment = function(data) {
    var moment = $(window.ich.momentSummaryTemplate(data)).hide();
    window.addCaption(moment, data.captions);
    window.setupMomentHandlers(moment);
    return moment;
};

window.newMoment = function(data, first) {
    if (data.code && data.code === "allseen") {
        jQuery("#moments").html("You've rated all the pictures. Want to upload some for everyone else?<br /><br />");
        return;
    }
    var moment = window.setupMoment(data);
    jQuery("#moments").prepend(moment);
    if (! first) {
        $(window).trigger("aboinga:new_moment");
    }
    moment.show("clip", "slow");
};

window.slugUrlChange = function(slug) {
    window.location.href = "#/moment/" + slug;
};

// Pull in the first one
if (window.location.hash.indexOf("moment") === -1){
    $.ajax({
        url: window.Moments.url() + 'slot_machine',
        success: function(data) {
            window.slugUrlChange(data.slug);
        }
    });
}

$(function () {
    $('#fileupload').fileupload({
        dataType: 'json',
        url: 'http://upload.aboinga.com/php/',
        limitConcurrentUploads: 2,
        limitMultiFileUploads: 4,
        done: function (e, data) {
            $.each(data.result, function (index, file) {
                $(window).trigger("aboinga:uploaded_file", jQuery("input[name=expires_at]:checked").val(), jQuery("input[name=public]:checked").val());
                $.ajax({
                    type: 'POST',
                    url: "/api/v1/moment/upload/",
                    data: { "file": file.name,
                            "expires_at": jQuery("input[name=expires_at]:checked").val(),
                            "public": jQuery("input[name=public]:checked").val()
                    },
                    success: function(data) {
                            window.newMoment(data);
                            Pilotfish('speaker', "Thanks for uploading. You are awesome!", {'timeout': 3000, 'type': 'success'});
                            Pilotfish('recorder', 'upload');
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
            $(window).trigger("aboinga:start_uplaod");
            $('.fileupload-progressbar div').css('width', '0%');
            $('.fileupload-progressbar').fadeIn();
        },
        // Callback for uploads stop, equivalent to the global ajaxStop event:
        stop: function () {
            $('.fileupload-progressbar').fadeOut();
        }
    });
});
