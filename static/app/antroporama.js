define([], function() {
    var query = `
        PREFIX : <http://antroporama.iolanta.tech/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?heading ?subheading
        WHERE {
            <http://antroporama.iolanta.tech> rdfs:label ?heading .
            <http://antroporama.iolanta.tech> rdfs:comment ?subheading .
        }
    `;

    return {
        'app': function (storage) {
            return new Vue({
                el: '#header',
                data: {
                    heading: null,
                    subheading: null,

                    image: {
                        href: '/media/illustrations/savannah_at_dawn_lurssen.jpg',
                        credit: {
                            label: 'Jean Lurssen',
                            seeAlso: 'http://the-watercolorist.blogspot.ru/2011/05/savannah-dawn.html'
                        }
                    },

                    // Hack
                    background: 'background-image: url(/media/illustrations/savannah_at_dawn_lurssen.jpg)'
                },
                created: function () {
                    var app = this;
                    storage.execute(query, function(err, results) {
                        var result = results[0];
                        app.heading = result.heading.value;
                        app.subheading = result.subheading.value;
                    });
                }
            })
        }
    }
});
