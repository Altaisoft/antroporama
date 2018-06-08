Vue.component('species', {
    props: ['node', 'image-position'],

    query: `
        PREFIX : <http://antroporama.iolanta.tech/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?title ?subtitle ?time_from ?time_to ?place ?description
        WHERE {
            ?node rdfs:label ?title .
            ?node :scientific-name ?subtitle .
            
            ?node :time-range ?time .
            ?time :from ?time_from .
            ?time :to ?time_to .
            
            ?node :location ?place .
            ?node rdfs:comment ?description . 
        
            FILTER(?node = {{ node }})
        }
    `,

    data: function() { return {
        title: null,
        subtitle: null,

        time_from: null,
        time_to: null,

        place: null,

        description: null,

        properties: null
    }},

    created: function () {
        var app = this,
            q = this.$options.query.replace('{{ node }}', this.node);

        window.storage.execute(q, function(err, results) {
            var result = results[0];

            app.title = result.title.value;
            app.subtitle = result.subtitle.value;
            app.time_from = result.time_to.value;
            app.time_to = result.time_from.value;
            app.place = result.place.value;
            app.description = result.description.value;

            // Turn the component on
            app.is_visible = true;

            console.log(app);
        });
    },

    template: `
        <section class="showcase">
            <div class="container-fluid p-0">
                <div class="row no-gutters">
                    <showcase node=":proconsul-photo"></showcase>
                    
                    <div class="col-lg-6 my-auto showcase-text">
                        <h2>{{ title }}<br/><small class="text-muted">{{ subtitle }}</small></h2>
                        
                        <p class="lead mb-0"><strong>Время:</strong> {{ time_from }} ... {{ time_to }}</p>
                        <p class="lead"><strong>Место:</strong> {{ place }}</p>
                        
                        <div v-html="description"></div>
                        
                        <properties node=":proconsul"></properties>
                    </div>
                </div>             
            </div>
        </section>
    `
});