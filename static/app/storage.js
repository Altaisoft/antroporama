define(['rdfstore'], function(rdfstore) {
    return {
        'storage': function(callback) {
            rdfstore.create(function(err, store) {
                $.get('/data/data.n3', function(data) {
                    store.load('text/n3', data, function(err) {
                        if (err) {
                            console.log('Error loading data:', err);
                        }

                        // Hack!
                        window.storage = store;

                        callback();
                    });
                })
            });

        }
    }
});