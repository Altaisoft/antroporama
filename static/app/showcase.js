Vue.component('showcase', {
    props: ['node'],
    data: function() {
        return {
            image: null,
            is_visible: false,
            query: `
                PREFIX : <http://antroporama.iolanta.tech/>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                
                SELECT ?href ?author ?seeAlso
                WHERE {
                    ?node :href ?href .
                    ?node :credit ?credit .
                
                    ?credit a :Credit .
                    ?credit rdfs:label ?author .
                    ?credit rdfs:seeAlso ?seeAlso .
                    FILTER(?node = :human_from_clay)
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

        window.storage.execute(this.query, function(err, results) {
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
        <div v-if="is_visible" class="col-lg-6 text-white showcase-img order-lg-2" :style="style">
            <div class="image-source px-3 pull-right">
                <a target="_blank" :href="image.credit.seeAlso">
                    {{ image.credit.label }}
                </a>
            </div>
        </div>
    `
});
