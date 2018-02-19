def register(collection):
    def registrar(storage_class):
        collection.storage = storage_class

    return registrar
