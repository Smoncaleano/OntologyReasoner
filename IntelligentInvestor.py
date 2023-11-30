from owlready2 import *


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


onto = get_ontology("http://localhost:9000/ProceduresRecord.owl")

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
    class FindLegal(Thing): pass
    class RepresentanteLegal(FindLegal >> str, FunctionalProperty): pass
    

with onto:
    rule = Imp()
    rule.set_as_rule("""FindLegal(?i),
http://localhost:9000/Company#Company(?s),

http://localhost:9000/Company#hasLegalRepresentative(?s, ?r),
http://localhost:9000/RepresentanteLegal#RepresentanteLegal(?r),
http://localhost:9000/RepresentanteLegal#hasName(?r, ?p),
http://localhost:9000/Company#hasName(?s, ?n),
equal(?n, "The Coca Cola Company") -> RepresentanteLegal(?i, ?p)""")
    inv = FindLegal()
    sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True)
    
describeIndividual(inv)



with onto:
    class FindSustitute(Thing): pass
    class RepresentanteSuplente(FindSustitute >> str, FunctionalProperty): pass
    

with onto:
    rule = Imp()
    rule.set_as_rule("""FindSustitute(?i),
http://localhost:9000/Company#Company(?s),
http://localhost:9000/Company#hasSustituteRepresentative(?s, ?u),
http://localhost:9000/RepresentanteSuplente#RepresentanteSuplente(?u),
http://localhost:9000/RepresentanteSuplente#hasName(?u, ?p),
http://localhost:9000/Company#hasName(?s, ?n),
equal(?n, "Servientrega S.A") -> RepresentanteSuplente(?i, ?p)""")
    inv = FindSustitute()
    sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True)


describeIndividual(inv)



with onto:
    class HasProcedures(Thing): pass
    class Procedure(HasProcedures >> str, FunctionalProperty): pass
    

with onto:
    rule = Imp()
    rule.set_as_rule("""HasProcedures(?i),
http://localhost:9000/Procedures#Procedures(?s),
http://localhost:9000/Procedures#hasProcedureName(?s, ?p),
http://localhost:9000/Procedures#isUssuedTo(?s, ?n),
http://localhost:9000/Company#Company(?n),
http://localhost:9000/Company#hasEnrollmentNumber(?n, ?m),              
equal(?m, "932578325") -> Procedure(?i, ?p)""")
    inv = HasProcedures()
    sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True)


describeIndividual(inv)




with onto:
    class WhoIsGoingToCancel(Thing): pass
    class Option(WhoIsGoingToCancel >> str, FunctionalProperty): pass
    

with onto:
    rule = Imp()
    rule.set_as_rule("""WhoIsGoingToCancel(?i),
http://localhost:9000/Procedures#Procedures(?s),
http://localhost:9000/Procedures#hasProcedureName(?s, ?p),
http://localhost:9000/Procedures#isUssuedTo(?s, ?n),
http://localhost:9000/Company#Company(?n),
http://localhost:9000/Company#hasName(?n, ?m),              
equal(?p, "Cancelacion de matricula") -> Option(?i, ?m)""")
    inv = WhoIsGoingToCancel()
    sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True)


describeIndividual(inv)









