# Welcome to Python in Visual Studio Code!
# Click the green Run button in the top right corner
# of this editor to run your first Python program.

#Written By: Josh Gilberstadt
import pandas as pd
from dateutil.parser import parse

#Change name of data transfer
input_csv = pd.read_csv('Data Transfers/A3-45_PROD_C2N_BM_FULL_202212021.csv', usecols=['LBREFID', 'LBTESTCD', 'LBORRES']).drop_duplicates(keep='first')
other_columns_csv=pd.read_csv('Data Transfers/A3-45_PROD_C2N_BM_FULL_202212021.csv', usecols=['USUBJID', 'LBREFID', 'VISIT', 'LBDTC', 'LBREASND']).drop_duplicates(keep='first')
duplicates_csv=pd.read_csv('Data Transfers/A3-45_PROD_C2N_BM_FULL_202212021.csv', usecols=['USUBJID', 'LBREFID'])

#Change name of Abeta file
input_abeta_csv=pd.read_csv('Lab Data/All Abeta Data_02DEC2022.csv', usecols=['Plasma Barcodes', 'A?40 (pg/mL)', 'A?42 (pg/mL)', 'A?42/40', 'Comments', 'Date of collection', 'SubjectID']).drop_duplicates(keep='first')

#Change name of ApoE File
input_apoe_csv=pd.read_csv('Lab Data/All ApoE Data_02DEC2022.csv', usecols=['Plasma Barcodes', 'Proteotype']).drop_duplicates(keep='first')

#Create QC file
pivot_file=input_csv.pivot(index='LBREFID', columns='LBTESTCD', values='LBORRES').reset_index()
abeta_merged_file=pd.merge(pivot_file, input_abeta_csv, left_on='LBREFID', right_on='Plasma Barcodes', how='left')
apoe_merged_file=pd.merge(abeta_merged_file, input_apoe_csv, on='Plasma Barcodes', how='left')
QC_file=pd.merge(apoe_merged_file, other_columns_csv, on='LBREFID', how='left')
QC_file=QC_file.reindex(columns=QC_file.columns.tolist()+['New Visit', 'AB40 Equal', 'AB42 Equal', 'AB4240 Equal', 'APOE Equal', 'Date of Collection Equal', 'SubjectID Equal', 'Comments Equal', 'Visit Equal'])
file_length=len(QC_file)
AB_cols={'A?40 (pg/mL)', 'A?42 (pg/mL)', 'A?42/40'}

for i in range(file_length):
   if type(QC_file.loc[i, 'Date of collection'])!=str:
      QC_file.loc[i, 'Date of collection']=str(QC_file.loc[i, 'Date of collection'])
   if QC_file.loc[i, 'Date of collection']!="nan":
      QC_file.loc[i, 'Date of collection']=parse(QC_file.loc[i, 'Date of collection'])
      QC_file.loc[i, 'LBDTC']=parse(QC_file.loc[i, 'LBDTC'])
      QC_file.loc[i, 'New Visit']="sc1a"
   else:
      QC_file.loc[i, 'New Visit']="sc1" 

#Check if AB40, AB42, and AB4240 values are equal
   for column in AB_cols:
      if type(QC_file.loc[i, column])!=str:
         QC_file.loc[i, column]=str(QC_file.loc[i, column])
      if ('.' in QC_file.loc[i, column]):
         QC_file.loc[i, column]=float(QC_file.loc[i, column])
         QC_file.loc[i, column]=round(QC_file.loc[i, column], 3)
         QC_file.loc[i, column]=str(QC_file.loc[i, column])
   if QC_file.loc[i, 'AB40']==QC_file.loc[i, 'A?40 (pg/mL)']:
      QC_file.loc[i, 'AB40 Equal']="TRUE"
   else:
      QC_file.loc[i, 'AB40 Equal']="FALSE"
   if QC_file.loc[i, 'AB42']==QC_file.loc[i, 'A?42 (pg/mL)']:
      QC_file.loc[i, 'AB42 Equal']="TRUE"
   else:
      QC_file.loc[i, 'AB42 Equal']="FALSE"
   if QC_file.loc[i, 'AB4240']==QC_file.loc[i, 'A?42/40']:
      QC_file.loc[i, 'AB4240 Equal']="TRUE"
   else:
      QC_file.loc[i, 'AB4240 Equal']="FALSE"

#Check if ApoE values are equal
   if type(QC_file.loc[i, 'Proteotype'])!=str:
      QC_file.loc[i, 'Proteotype']=str(QC_file.loc[i, 'Proteotype'])
   QC_file.loc[i, 'Proteotype']=QC_file.loc[i, 'Proteotype'].replace('/', '_')
   if QC_file.loc[i, 'APOE']==QC_file.loc[i, 'Proteotype']:
      QC_file.loc[i, 'APOE Equal']="TRUE"
   else:
      QC_file.loc[i, 'APOE Equal']="FALSE"

#Check if other values are equal
   if QC_file.loc[i, 'USUBJID']==QC_file.loc[i, 'SubjectID']:
      QC_file.loc[i, 'SubjectID Equal']="TRUE"
   else:
      QC_file.loc[i, 'SubjectID Equal']="FALSE"
   if QC_file.loc[i, 'LBREASND']=="Patient age missing":
      QC_file=QC_file.drop(i-1)
   QC_file.loc[i, 'Comments']=str(QC_file.loc[i, 'Comments'])
   QC_file.loc[i, 'LBREASND']=str(QC_file.loc[i, 'LBREASND'])
   if QC_file.loc[i, 'Comments']==QC_file.loc[i, 'LBREASND']:
      QC_file.loc[i, 'Comments Equal']="TRUE"
   else:
      QC_file.loc[i, 'Comments Equal']="FALSE"
   if QC_file.loc[i, 'VISIT']==QC_file.loc[i, 'New Visit']:
      QC_file.loc[i, 'Visit Equal']="TRUE"
   else:
      QC_file.loc[i, 'Visit Equal']="FALSE"
   if QC_file.loc[i, 'LBDTC']==QC_file.loc[i, 'Date of collection']:
      QC_file.loc[i, 'Date of Collection Equal']="TRUE"
   else:
      QC_file.loc[i, 'Date of Collection Equal']="FALSE"

#Check for duplicates
LBREFID_duplicates=duplicates_csv.pivot_table(columns=['LBREFID'], aggfunc='size').reset_index()
LBREFID_duplicates.columns=['LBREFID', 'LBREFID Duplicates']
USUBJID_duplicates=duplicates_csv.pivot_table(columns=['USUBJID'], aggfunc='size').reset_index()
USUBJID_duplicates.columns=['SubjectID', 'USUBJID Duplicates']
LBREFID_duplicates_file=pd.merge(QC_file, LBREFID_duplicates, on='LBREFID', how='left')
full_file=pd.merge(LBREFID_duplicates_file, USUBJID_duplicates, on='SubjectID', how='left')

#Change name of output file
full_file.to_csv('QC Files/A3-45_PROD_C2N_BM_FULL_202212021_QC.csv', index=False)

print("QC File Generated")