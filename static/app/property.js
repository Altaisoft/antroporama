Vue.component('property', {
    props: ['node'],
    data: function() { return {
        image: null,
        label: null
    }},

    query: `
        PREFIX : <http://antroporama.iolanta.tech/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?image ?label
        WHERE {
            <{{ node }}> :href ?image .
            <{{ node }}> rdfs:label ?label .
        }
    `,

    created: function () {
        var app = this,
            q = this.$options.query.replace(/{{ node }}/g, this.node);

        console.log(q);

        window.storage.execute(q, function(err, results) {
            var result = results[0];

            app.label = result.label.value;
            app.image = result.image.value;

            // Turn the component on
            app.is_visible = true;
        });
    },

    template: `
        <div class="col-lg-4">
            <div class="mx-auto mb-5 mb-lg-0 mb-lg-3">
                <img class="img-fluid" :src="image">
                <p class="text-muted">{{ label }}</p>
            </div>
        </div>
    `
});