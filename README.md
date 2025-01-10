# first open vs code 
# check conda is there or not in a terminal

conda -V

# if you want to create new envirnoment for this project 
   # first deactivate conda 
   conda decativate
   # create new envirnoment
   conda create --name venv python==3.11
# create requirment.txt file and list your liblibraries useing in your project as requirment
  # code to run requirment.txt
  pip install -r requirements.txt
# create your api_key
   pincecone.com
# keep your key safe in .cond 
  # code for this in conda 
  conda env config vars set PINECONE_API_KEY="past yor key here"
# .csv file is created when you run the code no need to with this csvfile 
# run main.py as 
streamlit run main.py 
