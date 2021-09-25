#!/usr/bin/env python
# coding: utf-8

# ## News Extraction

# ### Import Packages

# In[1]:


from bs4 import BeautifulSoup
from requests import get
import sys # for argument passing


# ### Creating a Function to Extract only text from `<p>` tags

# In[2]:

if len(sys.argv)>1:
    url = sys.argv[1]
    
else:
    sys.exit("Error: Please enter the URL")


def get_only_text(url):
    """
    return the title and the text of the article at the specific url
    """
    page = get(url)
    soup = BeautifulSoup(page.content, "lxml") # Using 'lxml' parser
    text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    title = ' '.join(soup.title.stripped_strings) # To remove escape strings we use ."stripped_strings"
    return title, text


# ### Calling the function with the desired News URL

# In[3]:


text = get_only_text(url)


# In[4]:


text


# In[5]:


len(str.split(text[1])) # word count in <p> tag


# ## Summarization

# In[6]:


#get_ipython().system('python -m pip install -U gensim==3.8.3')


# In[7]:


from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords


# ### Priting the Summarized Text
# ### Method 1 : Word Count

# In[19]:


print("Title : " + text[0])
print("Summary : ")
print(summarize(repr(text[1]), word_count=75))


# In[20]:


len(str.split((summarize(repr(text[1]), word_count=75))))


# ### Method 2: Ratio

# In[26]:


print("Title : " + text[0])
print("Summary : ")
print(summarize(repr(text[1]), ratio=0.04))


# ### Number of Words - Summarized Text

# In[32]:


len(str.split(summarize(repr(text[1]), ratio=0.04)))


# ### Keywords

# In[37]:


print('\nKeywords:')
print(keywords(text[1], ratio=0.1, lemmatize=True))

