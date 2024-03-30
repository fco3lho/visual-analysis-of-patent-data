import os
import xml.etree.ElementTree as ET
import pandas as pd
import threading
from tqdm import tqdm

def patentsToInventors(patent, inventors, df, lock):
    for inventor in inventors:
        lock.acquire()
        df.loc[len(df)] = [patent, inventor]
        lock.release()

def patentsToApplicants(patent, applicants, df, lock):
    for applicant in applicants:
        lock.acquire()
        df.loc[len(df)] = [patent, applicant]
        lock.release()
        
def inventorsToInventors(inventors, df, lock):
    for inventor_i in inventors:
        for inventor_j in inventors:
            lock.acquire()
            df.loc[len(df)] = [inventor_i, inventor_j]
            lock.release()

def applicantsToApplicants(applicants, df, lock):
    for applicant_i in applicants:
        for applicant_j in applicants:
            lock.acquire()
            df.loc[len(df)] = [applicant_i, applicant_j]
            lock.release()

def inventorsToApplicants(inventors, applicants, df, lock):
    for inventor in inventors:
        for applicant in applicants:
            lock.acquire()
            df.loc[len(df)] = [inventor, applicant]
            lock.release()

def createConnections():
    df = pd.DataFrame(columns=['connection_1', 'connection_2'])
    lock = threading.Lock()

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

            
                t1 = threading.Thread(target=patentsToInventors, args=(patent, inventors, df, lock))
                t2 = threading.Thread(target=patentsToApplicants, args=(patent, applicants, df, lock))
                t3 = threading.Thread(target=inventorsToInventors, args=(inventors, df, lock))
                t4 = threading.Thread(target=applicantsToApplicants, args=(applicants, df, lock))
                t5 = threading.Thread(target=inventorsToApplicants, args=(inventors, applicants, df, lock))

                t1.start()
                t2.start()
                t3.start()
                t4.start()
                t5.start()
            
            t1.join()
            t2.join()
            t3.join()
            t4.join()
            t5.join()

            progress_bar.update(1)

    # Save a CSV file
    print("Saving CSV file...")
    df.to_csv('connections.csv', index = False)
    print("Completed!")