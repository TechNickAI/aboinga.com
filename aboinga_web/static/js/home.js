
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
});


// pnotify set up defaults
jQuery(document).ready(function() {
    jQuery.pnotify.defaults.pnotify_delay = 3000;
    jQuery.pnotify.defaults.pnotify_animation = 'slide';
    window.hoverTip = $.pnotify({
        pnotify_title: null,
        pnotify_text: "",
        pnotify_hide: false,
        pnotify_closer: false,
        pnotify_sticker: false,
        pnotify_history: false,
        pnotify_animate_speed: 100,
        pnotify_opacity: 0.8,
        pnotify_notice_icon: "",
        // Setting stack to false causes Pines Notify to ignore this notice when positioning.
        pnotify_stack: false,
        pnotify_after_init: function(pnotify) {
            // Remove the notice if the user mouses over it.
            pnotify.mouseout(function() {
                pnotify.pnotify_remove();
            });
        },
        pnotify_before_open: function(pnotify) {
            // This prevents the notice from displaying when it's created.
            pnotify.pnotify({
                pnotify_before_open: null
            });
            return false;
        }
    });

    window.hoverTips = function(collection) {
        jQuery.each(collection.not("[data-title]"), function(i, item) {
            var $item = $(item);
            $item.attr("data-title", $item.attr("title"));
            $item.removeAttr("title");
        });
        collection.mouseover(function() {
            window.hoverTip.find(".ui-pnotify-text").html($(this).attr("data-title"));
            window.hoverTip.pnotify_display();
        });
        collection.mouseout(function() {
            window.hoverTip.pnotify_remove();
        });
        collection.mousemove(function(e) {
            window.hoverTip.css({'top': e.clientY+12, 'left': e.clientX+12});
        });
    };

    window.hoverTips(jQuery("img[title]"));
});

window.setupMomentHandlers = function(container) {
    //// Set up the handlers

    // Mouse overs
    window.hoverTips(container.find("img[title]"));

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
        $.ajax({
            url: window.Moments.url() + id,
            type: 'DELETE',
            success: function() {
                $("#moment_" + img.attr("data-id")).fadeOut(900);
                window.setTimeout(function() {
                    $("#moment_" + img.attr("data-id")).remove();
                }, 950);
                $(window).trigger("aboinga:delete");
                Pilotfish('reporter', 'delete');
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
        $.ajax({
            url: window.Moments.url() + 'slot_machine',
            type: 'POST',
            data: {
                moment_id: id,
                stars: stars
            },
            success: function(data) {
                $("#moment_" + img.attr("data-id")).fadeOut();
                $.pnotify({"pnotify_title": "Thanks!", "pnotify_text": "Thanks for rating. The overall rating is <b>" + data.previous_results.avg_rating + '</b> (' + data.previous_results.ratings + ')'});
                window.slugUrlChange(data.slug);
                $(window).trigger("aboinga:rate", stars);
                Pilotfish('reporter', 'rate');
            }
        });
    });


    // Next
    container.find("img.next").click(function() {
        var img = $(this);
        var id = img.attr("data-id");
        $.ajax({
            url: window.Moments.url() + 'slot_machine',
            success: function(data) {
                $("#moment_" + img.attr("data-id")).fadeOut();
                window.slugUrlChange(data.slug);
                $(window).trigger("aboinga:next");
                Pilotfish('reporter', 'next');
            }
        });
    });

    // Caption
    container.find(".newCaption input").blur(submitCaption).bind("keypress", function(e) {
        var code = (e.keyCode ? e.keyCode : e.which);
        if (code == 13) { //Enter keycode
            submitCaption(e);
        }
    });

    var submittedCaptions = [];
    function submitCaption(e) {
        var target = (e.currentTarget) ? e.currentTarget : e.srcElement;
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
                $.pnotify({pnotify_title: "Thanks", pnotify_text: "Thanks for adding a caption!"});
                container.find(".momentCaptions").html(window.ich.momentCaptionTemplate(caption));
                $(window).trigger("aboinga:new_caption");
                Pilotfish('reporter', 'new_caption');
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
if (window.location.hash.indexOf("moment") == -1){
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
                            $.pnotify({pnotify_title:"Thanks", pnotify_text: "Thanks for uploading. You are awesome!"});
                            Pilotfish('reporter', 'upload');
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
