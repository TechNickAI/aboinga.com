/* Model definitions for backbone.js to interact with API */
var API_URL = "/api/v1/";

// http://documentcloud.github.com/backbone/#Model
var MomentCollection = Backbone.Collection.extend({
    url : function() {
        return API_URL + "moment/";
    },
    parse: function(data){
        return data.objects;
    }
});
