import os
import xml.etree.ElementTree as ET
import pandas as pd
import threading
from tqdm import tqdm

df_nodes = pd.read_csv('nodeTable.csv')
df = pd.DataFrame(columns=['source', 'target'])
lock = threading.Lock()

def patentsToInventors(patent, inventors, lock):
    global df
    patent_index = df_nodes.loc[df_nodes['label'] == patent, 'id'].index[0]
    
    for inventor in inventors:
        lock.acquire()
        df = df._append({
            'source': patent_index, 
            'target': df_nodes.loc[(df_nodes['label'] == inventor) & (df_nodes['role'] == 'inventor')].index[0]}, 
            ignore_index=True
        )
        lock.release()

def patentsToApplicants(patent, applicants, lock):
    global df
    patent_index = df_nodes.loc[df_nodes['label'] == patent, 'id'].index[0]
    
    for applicant in applicants:
        lock.acquire()
        df = df._append({
            'source': patent_index, 
            'target': df_nodes.loc[(df_nodes['label'] == applicant) & (df_nodes['role'] == 'applicant')].index[0]}, 
            ignore_index=True
        )
        lock.release()
        
def inventorsToInventors(inventors, lock):
    global df

    for i in range(len(inventors)):
        for j in range(i+1, len(inventors)):
            lock.acquire()
            df = df._append({
                'source': df_nodes.loc[(df_nodes['label'] == inventors[i]) & (df_nodes['role'] == 'inventor')].index[0], 
                'target': df_nodes.loc[(df_nodes['label'] == inventors[j]) & (df_nodes['role'] == 'inventor')].index[0]}, 
                ignore_index=True
            )
            lock.release()

def applicantsToApplicants(applicants, lock):
    global df
    
    for i in range(len(applicants)):
        for j in range(i+1, len(applicants)):
            lock.acquire()
            df = df._append({
                'source': df_nodes.loc[(df_nodes['label'] == applicants[i]) & (df_nodes['role'] == 'applicant')].index[0], 
                'target': df_nodes.loc[(df_nodes['label'] == applicants[j]) & (df_nodes['role'] == 'applicant')].index[0]}, 
                ignore_index=True
            )
            lock.release()

def inventorsToApplicants(inventors, applicants, lock):
    global df
    
    for inventor in inventors:
        for applicant in applicants:
            lock.acquire()
            df = df._append({
                'source': df_nodes.loc[(df_nodes['label'] == inventor) & (df_nodes['role'] == 'inventor')].index[0], 
                'target': df_nodes.loc[(df_nodes['label'] == applicant) & (df_nodes['role'] == 'applicant')].index[0]}, 
                ignore_index=True
            )
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

                if df_temp['patent'].isin([patent]).any() == False and df_nodes['label'].isin([patent]).any() == True:
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