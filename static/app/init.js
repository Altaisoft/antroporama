requirejs.config({
    appDir: ".",
    urlArgs: "bust=" + (new Date()).getTime(),
    paths: {
        /* Load jquery from google cdn */
        //'jquery': ['//ajax.googleapis.com/ajax/libs/jquery/2.0.3/jquery.min'],
        /* Load bootstrap from cdn */
        //'bootstrap': ['//netdna.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min'],

        'rdfstore': '/static/lib/rdfstore_min',
        'antroporama': '/static/app/antroporama',
        'storage': '/static/app/storage'
    },
    shim: {
        /* Set bootstrap dependencies (just jQuery) */
        //'bootstrap': ['jquery']
    }
});

requirejs([
    'antroporama', 'storage'
], function(antroporama, storage) {
    storage.storage(antroporama.app);
});