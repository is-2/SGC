from django.http import HttpResponse
from adm.models import Project, Phase
from des.models import BaseLine, Item
import json

def graph(request, id_project):
    def get_relations(project):
        links = []
        phases = project.phase_set.all()
        for phase in phases:
            items = phase.item_set.all()
            if items.exists():
                for item in items:
                    # the links relationship consists like this: (parent,child)
                    links.append(("nombre-fase: "+phase.name, "nombre-item: "+item.name+" ;costo: "+str(item.cost))) 
            else:
                links.append(("nombre-fase: "+phase.name, "vacio"))
        return links
    
    if request.method == "GET":
        project = Project.objects.get(id=id_project)
        links = get_relations(project)
        parents, children = zip(*links)
        root_nodes = {x for x in parents if x not in children}
        for node in root_nodes:
            links.append((project.name, node)) # Create the top tier root relationship
            
        def get_nodes(node):
            d = {}
            d['name'] = node
            children = get_children(node)
            if children:
                d['children'] = [get_nodes(child) for child in children]
            return d
        
        def get_children(node):
            return [x[1] for x in links if x[0] == node]
        
        tree = get_nodes(project.name) # This sets the root node!
        return HttpResponse(json.dumps(tree), content_type = "application/json")