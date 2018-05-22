Vue.component('header-banner', {
    data: function() {
        return {
            heading: null,
            subheading: null,
            image: null,
            is_visible: false,

            text_query: `
                PREFIX : <http://antroporama.iolanta.tech/>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                
                SELECT ?heading ?subheading
                WHERE {
                    <http://antroporama.iolanta.tech> rdfs:label ?heading .
                    <http://antroporama.iolanta.tech> rdfs:comment ?subheading .
                }
            `,

            image_query: `
                PREFIX : <http://antroporama.iolanta.tech/>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                
                SELECT ?href ?author ?seeAlso
                WHERE {
                    ?node :href ?href .
                    ?node :credit ?credit .
                
                    ?credit a :Credit .
                    ?credit rdfs:label ?author .
                    ?credit rdfs:seeAlso ?seeAlso .
                    FILTER(?node = :header)
                }
            `
        }
    },

    computed: {
        style: function() {
            return 'background-image: url(' + this.image.href + ')';
        }
    },

    created: function () {
        var app = this;

        window.storage.execute(this.text_query, function(err, results) {
            var result = results[0];
            app.heading = result.heading.value;
            app.subheading = result.subheading.value;
        });

        window.storage.execute(this.image_query, function(err, results) {
            var result = results[0];

            app.image = {
                href: result.href.value,
                credit: {
                    label: result.author.value,
                    seeAlso: result.seeAlso.value
                }
            };

            // Turn the component on
            app.is_visible = true;
        });


    },

    template: `
        <header class="masthead text-white text-center" v-if="is_visible" :style="style">
            <div class="overlay">
                <div class="image-source px-3 pull-right">
                    <a target="_blank" :href="image.credit.seeAlso">
                        {{ image.credit.label }}
                    </a>
                </div>
            </div>
            <div class="container">
                <div class="row">
                    <div class="col-xl-9 mx-auto">
                        <h1 class="mb-5">
                            {{ heading }}<br>
                            <small>{{ subheading }}</small>
                        </h1>
                    </div>
                </div>
            </div>
        </header>
    `
});