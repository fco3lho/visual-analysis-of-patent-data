import os
import xml.etree.ElementTree as ET
import pandas as pd
import threading
from tqdm import tqdm

df = pd.DataFrame(columns=['id', 'label', 'role'])
lock = threading.Lock()
count = 0

def savePatent(patent, lock):
  global df, count

  if df['label'].isin([patent]).any() == False:
    lock.acquire()
    df = df._append({'id': count, 'label': patent, 'role': "patent"}, ignore_index=True)
    count+=1
    lock.release()
   
def saveApplicants(applicants, lock):
  global df, count

  for applicant in applicants:
    isThereSuchAnApplicant = (df['label'] == applicant) & (df['role'] == "applicant")

    if isThereSuchAnApplicant.any() == False:
      lock.acquire()
      df = df._append({'id': count, 'label': applicant, 'role': "applicant"}, ignore_index=True)
      count+=1
      lock.release()
   
def saveInventors(inventors, lock):
  global df, count

  for inventor in inventors:
    isThereSuchAnInventor = (df['label'] == inventor) & (df['role'] == "inventor")

    if isThereSuchAnInventor.any() == False:
      lock.acquire()
      df = df._append({'id': count, 'label': inventor, 'role': "inventor"}, ignore_index=True)
      count+=1
      lock.release()

def createNodes():
  with tqdm(total=len(os.listdir("./patents")), desc="Creating node table") as progress_bar:
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
          patent = field.get('value').upper()

        t1 = threading.Thread(target=savePatent, args=(patent, lock))
        t2 = threading.Thread(target=saveApplicants, args=(applicants, lock))
        t3 = threading.Thread(target=saveInventors, args=(inventors, lock))

        t1.start()
        t2.start()
        t3.start()
    
        t1.join()
        t2.join()
        t3.join()

      progress_bar.update(1)
  
  # Save a CSV file
  print("Saving CSV file...")
  df.to_csv('nodeTable.csv', index = False)
  print("Completed!")