import os
import xml.etree.ElementTree as ET
import pandas as pd
import threading
from tqdm import tqdm

df = pd.DataFrame(columns=['connection_1', 'connection_2'])
lock = threading.Lock()

def patentsToInventors(patent, inventors, lock):
    global df
    
    for inventor in inventors:
        lock.acquire()
        df = df._append({'connection_1': patent, 'connection_2': inventor}, ignore_index=True)
        lock.release()

def patentsToApplicants(patent, applicants, lock):
    global df
    
    for applicant in applicants:
        lock.acquire()
        df = df._append({'connection_1': patent, 'connection_2': applicant}, ignore_index=True)
        lock.release()
        
def inventorsToInventors(inventors, lock):
    global df

    for i in range(len(inventors)):
        for j in range(i+1, len(inventors)):
            lock.acquire()
            df = df._append({'connection_1': inventors[i], 'connection_2': inventors[j]}, ignore_index=True)
            lock.release()

def applicantsToApplicants(applicants, lock):
    global df
    
    for i in range(len(applicants)):
        for j in range(i+1, len(applicants)):
            lock.acquire()
            df = df._append({'connection_1': applicants[i], 'connection_2': applicants[j]}, ignore_index=True)
            lock.release()

def inventorsToApplicants(inventors, applicants, lock):
    global df
    
    for inventor in inventors:
        for applicant in applicants:
            lock.acquire()
            df = df._append({'connection_1': inventor, 'connection_2': applicant}, ignore_index=True)
            lock.release()

def createEdges():
    df_temp = pd.DataFrame(columns=['patent'])
    
    with tqdm(total=len(os.listdir("./patents")), desc="Creating edge table") as progress_bar: 
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
                    patent = (field.get('value')).upper()

                if df_temp['patent'].isin([patent]).any() == False:
                    df_temp = df_temp._append({'patent': patent}, ignore_index=True)

                    t1 = threading.Thread(target=patentsToInventors, args=(patent, inventors, lock))
                    t2 = threading.Thread(target=patentsToApplicants, args=(patent, applicants, lock))
                    t3 = threading.Thread(target=inventorsToInventors, args=(inventors, lock))
                    t4 = threading.Thread(target=applicantsToApplicants, args=(applicants, lock))
                    t5 = threading.Thread(target=inventorsToApplicants, args=(inventors, applicants, lock))

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
    df.to_csv('edgeTable.csv', index = False)
    print("Completed!")