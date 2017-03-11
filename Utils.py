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



dictionariest = [{#"Company": "http://dbpedia.org/ontology/Company",
                  #'comedian': "http://dbpedia.org/ontology/Comedian",
                  #'Mammal': "http://dbpedia.org/ontology/Mammal",
                  #"EducationalInstitution": "http://dbpedia.org/ontology/EducationalInstitution",
                  'politician': "http://dbpedia.org/ontology/Politician",
                  #'architectural_structure': "http://dbpedia.org/ontology/ArchitecturalStructure",
                    'Fish': "http://dbpedia.org/ontology/Fish" }]

dictionariesq = [{'comedian': "http://dbpedia.org/ontology/Comedian",
                  "EducationalInstitution": "http://dbpedia.org/ontology/EducationalInstitution",
                    'Play': "http://dbpedia.org/ontology/Play"}]


if __name__ == '__main__':
    import smtplib

    # Import the email modules we'll need
    from email.mime.text import MIMEText

    # Open a plain text file for reading.  For this example, assume that
    # the text file contains only ASCII characters.
    #fp = open(textfile, 'rb')
    # Create a text/plain message
    msg = MIMEText("just checking emails")
    #fp.close()

    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = 'The contents of subj'
    msg['From'] = 'omri.myers@gmail.com'
    msg['To'] = 'omri.myers@gmail.com'

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('localhost')
    s.sendmail('omri.myers@gmail.com', ['omri.myers@gmail.com'], msg.as_string())
    s.quit()