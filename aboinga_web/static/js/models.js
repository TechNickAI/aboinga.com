/* Model definitions for backbone.js to interact with API */
window.API_URL = "/api/v1/";

// http://documentcloud.github.com/backbone/#Model
window.MomentCollection = window.Backbone.Collection.extend({
    url : function() {
        return window.API_URL + "moment/";
    },
    parse: function(data){
        return data.objects;
    }
});

window.Moment = window.Backbone.Model.extend({
    url : function() {
        return window.API_URL + "moment/";
    },
    parse: function(data){
        return data.objects;
    }
});

window.CaptionCollection = window.Backbone.Collection.extend({
    url : function() {
        return window.API_URL + "caption/";
    },
    parse: function(data){
        return data.objects;
    }
});

window.CaptionMoment = window.Backbone.Model.extend({
    url : function() {
        return window.API_URL + "caption/";
    },
    parse: function(data){
        return data.objects;
    }
});
