#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os # for file manipulation
import re # for regex
import pandas as pd # for csv conversion
import spacy # for NLP
import pdfminer # for pdf2txt


# In[2]:


#!python3 -m spacy download en_core_web_sm


# In[3]:


import pdf2txt


# ### Convert PDF to Text

# In[4]:


def convert_pdf(f):
    output_filename = os.path.basename(os.path.splitext(f)[0]) + ".txt"
    output_filepath = os.path.join("output/txt/", output_filename)
    pdf2txt.main(args=[f, "--outfile", output_filepath]) #pdf to txt and saves it at given location
    print(output_filepath + " saved successfully")
    return open(output_filepath).read()


# ### Loading language model

# In[5]:


nlp = spacy.load("en_core_web_sm")


# ### Capture Important Components from Resume

# In[6]:


result_dict = {'name': [], 'phone': [], 'email': [], 'skills':[]}
# placeholder lists below
names = []
phones = []
emails = []
skills = []


# In[7]:


def parse_content(text):
    skillset = re.compile("python|java|sql|hadoop|tableau")
    phone_num = re.compile("(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})")
    # phone_num credit : https://stackoverflow.com/questions/3868753/find-phone-numbers-in-python-script/3868861#3868861
    doc = nlp(text)
    name = [entity.text for entity  in doc.ents if entity.label_ == "PERSON"][0]
    #print(name)
    email = [word for word in doc if word.like_email == True][0]
    #print(email)
    phone = str(re.findall(phone_num, text.lower()))
    skills_list = re.findall(skillset, text.lower()) # convert to lowercase to account for anyone spelling sql as "SQL" or "Sql", etc
    unique_skills_list = str(set(skills_list)) # converting to set removes redundancy and then converting to string to be stored in unique_skills
    names.append(name)
    emails.append(email)
    phones.append(phone)
    skills.append(unique_skills_list)
    print("Extraction completed successfully")
    


# In[8]:


for file in os.listdir('resumes/'):
    if file.endswith('.pdf'):
        print('Reading...' + file)
        txt = convert_pdf(os.path.join('resumes/', file))
        parse_content(txt)


# In[9]:


result_dict['name'] = names
result_dict['phone'] = phones
result_dict['email'] = emails
result_dict['skills'] = skills


# In[10]:


#print(result_dict)


# In[12]:


result_df = pd.DataFrame(result_dict)
#result_df


# ### Saving as CSV

# In[13]:


result_df.to_csv('output/csv/parsed_resumes.csv')


# In[ ]:




