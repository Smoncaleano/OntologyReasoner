import os
from owlready2 import *
from datetime import datetime

def describeEntity(obj):
    print("\n" + "*"*20)
    print("[Entity Name: " + str(obj.name) + "]")
    print("[Base Entity: " + str(obj.is_a) + "]")       
    print("[Ancestors: " + str(list(obj.ancestors())) + "]")
    print("[Descendants: " + str(list(obj.descendants())) + "]")
    print("[Instances: " + str(list(obj.instances())) + "]") 
    print("*"*20)	
    	
def describeIndividual(obj):
    print("\n" + "*"*20)
    print("[Instance Name: " + str(obj.name) + "]")
    print("[Instance of: " + str(obj.is_a) + "]")    
    print("[Properties: ")
    for prop in obj.get_properties():
        for value in prop[obj]:
            print("   .%s == %s" % (prop.python_name, value))
    print("]")
    print("*"*20)


#onto = get_ontology("http://localhost:9000/Company.owl")
#onto = get_ontology("http://localhost:9000/StockExchangeShares.owl")
#onto = get_ontology("http://localhost:9000/CompaniesRecord.owl")
onto = get_ontology("http://localhost:9000/CompaniesRecord.owl")

onto.load()

print("\n\n================INTELLIGENT INVESTOR================")

print("\nImported ontologies: ")
print(onto.imported_ontologies)
#onto.imported_ontologies.append(onto0)

clases = list(onto.classes())
for cls in clases:
    describeEntity(cls)

obj_prop = list(onto.object_properties())
print(obj_prop)

individuals = list(onto.individuals())
for ind in individuals:
    describeIndividual(ind)

with onto:
    sync_reasoner(infer_property_values = True)

print(list(default_world.inconsistent_classes()))




with onto:
    class BuscarEmpresa(Thing): pass
    class nombreEmpresa(BuscarEmpresa >> str, FunctionalProperty): pass

with onto:
    rule = Imp()
    rule.set_as_rule("""BuscarEmpresa(?i),
http://localhost:9000/Company#Company(?s),
http://localhost:9000/Company#hasEnrollmentNumber(?s, ?t),
http://localhost:9000/Company#hasName(?s, ?n),
equal(?t,"932578325") -> nombreEmpresa(?i, ?n)""")
    inv = BuscarEmpresa()
    sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True)

describeIndividual(inv)



with onto:
    class Auditoria(Thing): pass
    class Empresa(Auditoria >> str, FunctionalProperty): pass
    

with onto:
    rule = Imp()
    rule.set_as_rule("""Auditoria(?i),
http://localhost:9000/Company#Company(?s),
http://localhost:9000/Company#hasDateOfRenovation(?s, ?t),
http://localhost:9000/Company#hasName(?s, ?n),
lessThan(?t, 2023) -> Empresa(?i, ?n)""")
    inv = Auditoria()
    sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True)


describeIndividual(inv)

with onto:
    class Find(Thing): pass
    class Representante(Find >> str, FunctionalProperty): pass
    

with onto:
    rule = Imp()
    rule.set_as_rule("""Find(?i),
http://localhost:9000/Company#Company(?s),

http://localhost:9000/Company#hasLegalRepresentative(?s, ?r),
http://localhost:9000/RepresentanteLegal#RepresentanteLegal(?r),
http://localhost:9000/RepresentanteLegal#hasName(?r, ?p),
http://localhost:9000/Company#hasName(?s, ?n),
equal(?n, "The Coca Cola Company") -> Representante(?i, ?p)""")
    inv = Find()
    sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True)


describeIndividual(inv)

