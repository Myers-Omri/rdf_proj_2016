from json import JSONEncoder

class GraphObjectEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

subjectsPerson = {#'person': "http://dbpedia.org/ontology/Person",
                          'politician': "http://dbpedia.org/ontology/Politician",
                          'soccer_player': "http://dbpedia.org/ontology/SoccerPlayer",
                          'baseball_players': "http://dbpedia.org/ontology/BaseballPlayer",
                          'comedian': "http://dbpedia.org/ontology/Comedian",
                          "Company": "http://dbpedia.org/ontology/Company",
                          "EducationalInstitution": "http://dbpedia.org/ontology/EducationalInstitution"}


subjectsPlaces = {#'Place': "http://dbpedia.org/ontology/Place",
                  'NaturalPlace': "http://dbpedia.org/ontology/NaturalPlace",
                  'HistoricPlace': "http://dbpedia.org/ontology/HistoricPlace",
                  'CelestialBody': "http://dbpedia.org/ontology/CelestialBody",
                  'architectural_structure': "http://dbpedia.org/ontology/ArchitecturalStructure"}

subjectsLive = {#'Animal': "http://dbpedia.org/ontology/Animal",
                'Plant': "http://dbpedia.org/ontology/Plant",
                'Insect': "http://dbpedia.org/ontology/Insect",
                'Fish': "http://dbpedia.org/ontology/Fish",
                'Mammal': "http://dbpedia.org/ontology/Mammal",
                'Play': "http://dbpedia.org/ontology/Play"}

dictionaries = [subjectsPerson, subjectsPlaces, subjectsLive]



dictionariest = [{'politician': "http://dbpedia.org/ontology/Politician"}]



# def get_p_dict(self,quick, uri):
#
#     p_dict = {}
#     if quick:
#
#         p_dict["http://dbpedia.org/ontology/birthPlace"] = 0
#         #p_dict["http://dbpedia.org/ontology/residence"] = 0
#     else:
#         query_text = ("""
#             SELECT ?p (COUNT (?p) AS ?cnt)
#             WHERE {
#                 {
#                 SELECT DISTINCT ?s
#                 WHERE {
#                     ?s a <%s>.
#                 }LIMIT 500000
#                 }
#                 ?s ?p ?o
#                 FILTER regex(?p, "^http://dbpedia.org/property", "i")
#             }GROUP BY ?p
#              ORDER BY DESC(?cnt)
#              LIMIT 100
#             """ % uri)
#         self.sparql.setQuery(query_text)
#         self.sparql.setReturnFormat(JSON)
#         results_inner = self.sparql.query().convert()
#
#         for inner_res in results_inner["results"]["bindings"]:
#             p = inner_res["p"]["value"]
#             # cnt = inner_res["cnt"]["value"]
#             p_dict[p] = 0
#     p_dict_file = open('p_dict.dump', 'w')
#     pickle.dump(p_dict, p_dict_file)
#     p_dict_file.close()
#     print "get p_dict done"
#     return p_dict
