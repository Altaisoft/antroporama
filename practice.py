import rdflib


def get_data():
    with open('antroporama.n3', 'r') as f:
        content = f.read()

        graph = rdflib.Graph()
        graph.parse(data=content, format='n3')
        return list(graph.predicates(
            subject=None,
            object=None
        ))

print(get_data())
