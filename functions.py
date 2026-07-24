import pandas as pd 
import re   
import os

#----------------------------cleaning stage --------------------------
#  remove spaces and unwanted punctuation
def clean(data):
    text = re.sub(r'[().،:]', '' , data)
    # remove unneeded spaces
    text = re.sub(r'\s+' , ' ' ,text)
    return text.strip()


#  prepare the result
def processed(row):
    problem = f"المشكله: {clean(row['problem'])} "
    category = f"النوع: {clean(row['category'])} "
    solution = f"الحل: {clean(row['solution'])} "
    # print(problem)
    # print(category)
    # print(solution)
    return problem + category + solution



def cleaning_data():
    #  to get file 
    path_from = 'Data/CSV files/'
    path_to = 'Data/Processed/'


    #  get files 
    files = [f for f in os.listdir(path_from) if f.endswith('.csv')]
    # files = ['اجهزة صغيرة' ,'السخان' ,'تكييف' , 'تلاجات' , 'حدادة' , 
    #         'خلاط وميكروووف و بوتجااز' , 'سباكه' , 'شاشات' , 'غسالات' ,
    #         'كهرباء و مراوح' , 'نجاره' ,'نقاشه']


    for file in files:
        source = os.path.join(path_from, file)
        destination = os.path.join(path_to, os.path.splitext(file)[0] + '.txt')

        # create a dataframe
        df = pd.read_csv(source , encoding='utf-8-sig')

        #  drop dublicates
        df.drop_duplicates(inplace=True)

        # apply clean on data 
        df['problem'] = df['problem'].apply(clean)
        df['category'] = df['category'].apply(clean)
        df['solution'] = df['solution'].apply(clean)



        # axis=1 ---> for apply on rows
        cleaned_data = df.apply(processed , axis=1)

        # add the cleand part to proceeded folder
        try:
            with open(destination , 'w' , encoding='utf-8-sig') as f:
                #  use join since wite need string not series 
                f.write(''.join(cleaned_data))  
        except (FileExistsError):
            print(f"file {destination} exists.")



#------------------------------------------------------------------------

