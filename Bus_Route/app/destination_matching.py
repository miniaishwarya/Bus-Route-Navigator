from difflib import SequenceMatcher as sm
import textdistance as td

matched_dest = []

def matching_loop(input,route,check = 0): #check value equals 0 means, no match has been found
    test_ratio = 0
    if(check == 0 ):
        for i in range(len(route)):
            test_ratio = sm(None, input, route[i]).ratio()
            if(test_ratio >= 0.9 ):
                matched_dest.append(route[i])
                return 1
            
        if(test_ratio < 0.9):
            return 0
        
        
    elif(check == 1 ):
        return 1
    
  

        
def initialize():
    matched_dest.clear()

def destination_validation(input):
    
    initialize()
    
    found = 0
    
    input = input.lower()
    
    route_1 = ['neyyatinkara','aalumoodu','tb Junction','moonnukallumoodu','pathamkallu','aaralumoodu','vazhimukk','balaramapuram','mudavoorpaara','vedivechankoil','pallichal','pravachambalam','nemom','vellayani','karakkamandapam','pappanamcode', 'kaimanam', 'karamana','kilipalam','thampanoor','kizhakkekotta','eastfort' ]
    
    route_2 = ['eastfort', 'ayurveda college', 'collectorate','general hospital' 'vanchiyoor', 'pattoor', 'nalumukku', 'pallimukku', 'kannanmoola', 'kumarapuram',  'murinjapalam','medical college','kesavadasapuram', 'paruthipara','panavila','parottukonam' ]

    route_3 = ['eastfort', 'statue', 'palayam','musuem', 'vellayambalam','nanthancode','kowdiar', 'ambalamukk', 'peroorkada', 'kudapanakunn', 'civil station']
    
    
    found = matching_loop(input, route_1)
    found = matching_loop(input, route_2,found) 
    found = matching_loop(input, route_3,found)
    
    destination = ''    
    
    if(found == 0 ):
        destination = input             #No possible match
    elif(found == 1):
        destination = matched_dest[0]   #The matched destination
        
    return destination
        
