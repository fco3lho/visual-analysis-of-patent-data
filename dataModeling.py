import xml.etree.ElementTree as ET
import pandas as pd

df = pd.DataFrame(columns=['connection_1', 'connection_2'])

tree = ET.parse('PATENTE_IDLATTES_0000111305956227_ID_ESPACENET_PI0702090.xml')
root = tree.getroot()

patent = ""
applicants = []
inventors = []

for field in root.findall('.//field[@name="{}"]'.format('inventor')):
    inventors.append(field.get('value'))

for field in root.findall('.//field[@name="{}"]'.format('applicant')):
    applicants.append(field.get('value'))

for field in root.findall('.//field[@name="{}"]'.format('title.lattes')):
    patent = field.get('value')

# Patents > Inventors
for inventor in inventors:
    df.loc[len(df)] = [patent, inventor]

# Patents > Applicants
for applicant in applicants:
    df.loc[len(df)] = [patent, applicant]

# Inventors > Inventors
for inventor_i in inventors:
    for inventor_j in inventors:
        df.loc[len(df)] = [inventor_i, inventor_j]

# Inventors > Applicants
for inventor in inventors:
    for applicant in applicants:
      df.loc[len(df)] = [inventor, applicant]

# Applicants > Applicants
for applicant_i in applicants:
    for applicant_j in applicants:
        df.loc[len(df)] = [applicant_i, applicant_j]

print(df)

# Save a CSV file
df.to_csv('connections.csv', index = False)