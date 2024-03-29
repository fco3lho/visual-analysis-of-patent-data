import os
import xml.etree.ElementTree as ET
import pandas as pd
import threading
from tqdm import tqdm

def patentsToInventors(patent, inventors, df):
    for inventor in inventors:
        df.loc[len(df)] = [patent, inventor]

def patentsToApplicants(patent, applicants, df):
    for applicant in applicants:
        df.loc[len(df)] = [patent, applicant]

def inventorsToInventors(inventors, df):
    for inventor_i in inventors:
        for inventor_j in inventors:
            df.loc[len(df)] = [inventor_i, inventor_j]

def applicantsToApplicants(applicants, df):
    for applicant_i in applicants:
        for applicant_j in applicants:
            df.loc[len(df)] = [applicant_i, applicant_j]

def inventorsToApplicants(inventors, applicants, df):
    for inventor in inventors:
        for applicant in applicants:
            df.loc[len(df)] = [inventor, applicant]


df = pd.DataFrame(columns=['connection_1', 'connection_2'])
threads = []

with tqdm(total=len(os.listdir("./patents")), desc="Processing files") as progress_bar: 
    for file in os.listdir("./patents"):
        if file.endswith(".xml"):
            tree = ET.parse(os.path.join("./patents", file))
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

        
            t1 = threading.Thread(target=patentsToInventors, args=(patent, inventors, df))
            t2 = threading.Thread(target=patentsToApplicants, args=(patent, applicants, df))
            t3 = threading.Thread(target=inventorsToInventors, args=(inventors, df))
            t4 = threading.Thread(target=applicantsToApplicants, args=(applicants, df))
            t5 = threading.Thread(target=inventorsToApplicants, args=(inventors, applicants, df))

            t1.start()
            t2.start()
            t3.start()
            t4.start()
            t5.start()

            threads.extend([t1, t2, t3, t4, t5])

        for t in threads:
            t.join()
        
        progress_bar.update(1)

# Save a CSV file
print("Saving CSV file...")
df.to_csv('connections.csv', index = False)
print("Completed!")