Vue.component('introduction', {
    query: `
        PREFIX : <http://antroporama.iolanta.tech/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?title ?content
        WHERE {
            ?node rdfs:label ?title .
            ?node rdfs:comment ?content .
        
            FILTER(?node = :introduction)
        }
    `,

    data: function() {
        return {
            title: null,
            content: null,
        };
    },

    created: function () {
        var app = this;

        window.storage.execute(this.$options.query, function(err, results) {
            var result = results[0];
            app.title = result.title.value;
            app.content = result.content.value;
        });
    },

    template: `
        <section class="showcase">
            <div class="container-fluid p-0">
                <div class="row no-gutters">
                    <showcase node=":human_from_clay"></showcase>
        
                    <div class="col-lg-6 my-auto showcase-text order-lg-1">
                        <h2>{{ title }}</h2>
                        <span v-html="content"></span>
                    </div>
                </div>
            </div>
        </section>
    `
});
