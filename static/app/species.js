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
        time: null,
        place: null,

        description: null,

        properties: null
    }},

    created: function () {
        var app = this,
            q = this.$options.query.replace('{{ node }}', this.node);

        window.storage.execute(q, function(err, results) {
            var result = results[0];

            console.log(result);

            // Turn the component on
            app.is_visible = true;
        });
    },

    template: `
        <div class="row no-gutters">
          <!--div class="col-lg-6 text-white showcase-img{% if even %} order-lg-2{% endif %}" style="background-image: url('{{ item.image.href or '/media/' + item.image.filename }}');">
            {{ macros.source(item.image.author, 'pull-right') }}
          </div-->
        
          <div class="col-lg-6 my-auto showcase-text">
            Something
          </div>
        </div>    
    `
});