Vue.component('properties', {
    props: ['node'],
    query: `
        PREFIX : <http://antroporama.iolanta.tech/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?property ?node
        WHERE {
            {{ node }} ?property ?node .
            ?property a :SpeciesProperty .
        }
    `,
    data: function() { return {
        properties: [],
        is_visible: false
    }},
    created: function() {
        var app = this,
            q = this.$options.query.replace('{{ node }}', this.node);

        window.storage.execute(q, function(err, results) {
            console.log(results);
            app.properties = results.map(function(obj) {
                return obj.node.value;
            });

            console.log(app.properties);

            app.is_visible = true;
        });
    },
    template: `
        <section v-if="is_visible" class="text-center properties">
            <div class="container">
                <property v-for="item in properties" :node="item" :key="item"></property>
            </div>
        </section>
    `
});