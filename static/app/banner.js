Vue.component('text-banner', {
    props: ['node'],

    query: `
        PREFIX : <http://antroporama.iolanta.tech/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?content
        WHERE {
            ?node rdfs:comment ?content .
            FILTER(?node = {{ node }})
        }
    `,

    data: function() {
        return {
            content: null,
            is_visible: false
        }
    },

    computed: {
        style: function() {
            return 'background-image: url(' + this.image.href + ')';
        }
    },

    created: function () {
        var app = this,
            q = this.$options.query.replace('{{ node }}', this.node);

        window.storage.execute(q, function(err, results) {
            var result = results[0];

            app.content = result.content.value;

            // Turn the component on
            app.is_visible = true;
        });
    },

    template: `
        <section v-if="is_visible" class="holmes">
            <div class="container pb-5 pt-5">
                <span v-html="content"></span>
            </div>
        </section>
    `
});
