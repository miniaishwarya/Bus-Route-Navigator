from difflib import SequenceMatcher as sm
import textdistance as td
import string


count_final = []
list_final = []


def find_route_list(list_eng, route, check = 0 ):   #check value determines whether the function find number of dest(check = 0) or get the list of matched dest
    count = 0
    index = 0
    for i in range(len(list_eng)):
        ratio = 0
        for j in range(len(route)):
            test_ratio = sm(None, list_eng[i], route[j]).ratio()            #for calculating similarity ratio between strings
            val = td.levenshtein(list_eng[i],route[j])          #for calculating levenshtein distance between strings
            if((test_ratio > 0.73) and (test_ratio > ratio )and (val < 5)):
                ratio = test_ratio
                index = j           #index of most probable destination
                            
        if(ratio > 0.73):            
            if (check ==0):
                #print(list_eng[i]," has ratio ",ratio, "with" ,route[index]," AT", index,"\n") 
                count = count+1
            elif(check == 1):
                list_final.append(route[index])
    
    if(check == 0):    
        count_final.append(count)
        #print(count_final)

def cleaning():             #for clearing the global variables
    count_final.clear()
    list_final.clear()
    index_max=0

def replace_with_actual():          #for replacing the matched words with the actual destination name
    
    if(list_final.count('camp')!=0):
        index_rep = list_final.index('camp')
        list_final[index_rep] = 'palayam'
    if(list_final.count('civil')!=0):
        index_rep = list_final.index('civil')
        list_final[index_rep] = 'civil station'
    if(list_final.count('m college')!=0):
        index_rep = list_final.index('m college')
        list_final[index_rep] = 'medical college'
    
    
def matching(list_eng):
    
    route_1 = ['neyyatinkara','aalumoodu','tb Junction','moonnukallumoodu','pathamkallu','aaralumoodu','vazhimukk','balaramapuram','mudavoorpaara','vedivechankoil','pallichal','pravachambalam','nemom','vellayani','karakkamandapam','pappanamcode', 'kaimanam', 'karamana','kilipalam','thampanoor','kizhakkekotta','eastfort','east' ]
    
    route_2 = ['eastfort','east','kizhakkekotta','ayurveda college', 'collectorate','gen','gen hospital', 'vanchiyoor', 'patur', 'pattoor', 'nalumukku', 'pallimukku', 'kannanmoola', 'kumarapuram',  'murinjapalam','m college','medical','kesavadasapuram', 'paruthipara','panavila jn','parottukonam' ]

    route_3 = ['eastfort','east','kizhakkekotta','statue', 'palayam','camp','the camp','musuem', 'vellayambalam','nanthancode','kowdiar', 'ambalamukk', 'peroorkada', 'kudapanakunn', 'civil', 'civil station']

   
    cleaning()
    
    #0.0 This piece of code is for removing punctuations from the words
    table = str.maketrans('', '', string.punctuation) #maketrans() create a table for the translate used here

    for x in range(len(list_eng)):
        list_eng[x] = list_eng[x].lower()
        list_eng[x] = list_eng[x].translate(table) 
        # ^ removes the punctuations by matching them with empty string mentioned in maketrans
    #0.0    
   
    #Now, list_eng is a string with special chara, punctuations removed and contains only lower case letters
   

    find_route_list(list_eng, route_1 )
    find_route_list(list_eng, route_2 )
    find_route_list(list_eng, route_3 )
    
    max_val = 0
    index_max = 0
    
    max_val = max(count_final)
    m = []
   # occ_max = count_final.count(max_val)
    
    if( count_final.count(0)== 3):#If no match is found with all three routes
        index_max = 0
    else:
        index_max = count_final.index(max_val) + 1
        
    #print("THIS IS COUNT_FINAL",count_final)
       
  
    if(index_max == 1):
        find_route_list(list_eng,route_1,1) 
        m = route_1
    elif(index_max == 2):
        find_route_list(list_eng,route_2,1)
        m = route_2
    elif(index_max == 3):
        find_route_list(list_eng,route_3,1)
        m = route_3
        
    replace_with_actual()
          
   # print("\nThe count value is", count_final)
    return list_final , index_max, m

