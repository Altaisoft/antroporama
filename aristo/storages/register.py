def register(collection_class):
    def registrar(translation_class):
        collection_class.storage = translation_class

    return registrar
