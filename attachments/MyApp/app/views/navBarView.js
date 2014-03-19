$(function () {

    App.Views.navBarView = Backbone.View.extend({
        tagName: "ul",
        className: "nav",
        id: "itemsinnavbar",
        authorName: null,
        template1: _.template($('#template-nav-logged-in').html()),
        template0: _.template($('#template-nav-log-in').html()),
        initialize: function (option) {
            if (option.isLoggedIn == 0) {
                this.template = this.template0
            } else {
                this.template = this.template1
            }
            var temp = Backbone.history.location.href
            temp = temp.split('#')
            
    		var version=''
    	 
    	 	if(!App.configuration)
    	 	{
        		var config = new App.Collections.Configurations()
    	    	config.fetch({async:false})
    	    	var con=config.first()
            	App.configuration = config.first()
    	 	}

            if(! App.languageDict){
                var clanguage = App.configuration.get("currentLanguage")
                var languageDict;
                // fetch dict for the current/selected language from the languages db/table
                $.ajax({
                    type: 'GET',
                    url: '/languages/_all_docs?include_docs=true',
                    dataType: 'json',
                    success: function (response) {
                        var languageDicts = response.rows[0].doc; // put json of all dictionaries in var
                        // now get the selected language dict from that var
                        languageDict = languageDicts[clanguage];
//                    console.log("doc attrib when str === english: " + JSON.stringify(languageDict));
                    },
                    data: {},
                    async: false
                });

                App.languageDict = languageDict;
            }



//            var languageDict = App.configuration.get(clanguage);
//            console.log("App.configuration.get(clanguage): " + JSON.stringify(languageDict));
            version=App.configuration.get('version')
        	this.data = {
                uRL: temp[1],
                versionNO:version,
                languageDict:App.languageDict
            } 
            this.$el.append(this.template(this.data))
            ///////if login then fetch member
            if(!App.member && $.cookie('Member._id'))
            {
            	 var member = new App.Models.Member()
            	 member.set('_id', $.cookie('Member._id'))
            	 member.fetch({
                	async: false
                })
                App.member = member
            }
        },

        render: function () {}

    })

})