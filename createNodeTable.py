import os
import xml.etree.ElementTree as ET
import pandas as pd
import threading
from tqdm import tqdm

df = pd.DataFrame(columns=['name', 'role'])
lock = threading.Lock()

def savePatent(patent, lock):
   global df

   lock.acquire()
   df = df._append({'name': patent, 'role': "patent"}, ignore_index=True)
   lock.release()
   
def saveApplicants(applicants, lock):
   global df

   for applicant in applicants:
      lock.acquire()
      df = df._append({'name': applicant, 'role': "applicant"}, ignore_index=True)
      lock.release()
   
def saveInventors(inventors, lock):
  global df

  for inventor in inventors:
    lock.acquire()
    df = df._append({'name': inventor, 'role': "inventor"}, ignore_index=True)
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
            patent = field.get('value')

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

        