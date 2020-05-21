
routes = [["neyyatinkara", "aalumoodu", "tb junction", "moonnukallumoodu", "pathamkallu",
 "aaralumoodu", "vazhimukk", "balaramapuram", "mudavoorpara", "vedivechankoil", "pallichal",
  "pravachambalam", "nemom", "vellayani", "karakkamandapam",  "pappanamcode", "kaimanam",
   "karamana", "kilipalam", "thampanoor", "eastfort" 
], ['eastfort', 'ayurveda college', 'collectorate', 'gen hospital', 'vanchiyoor', 'patoor',
 'nalumukku', 'pallimukku', 'kannanmoola', 'kumarapuram',  'murinjapalam','medical college',
 'kesavadasapuram', 'paruthipara','panavila jn','parottukonam' 
], ['eastfort', 'statue', 'palayam','musuem', 'vellayambalam','nanthancode',
'kowdiar', 'ambalamukku', 'peroorkada', 'kudapanakunn', 'civil station'
]]

def orgRoute(route):
    if route[0]=="neyyatinkara" and route[len(route)-1]=="eastfort":
        return routes[0]
    elif route[0]=="eastfort" and route[len(route)-1]=="parottukonam":
        return routes[1]
    elif route[0]=="eastfort" and route[len(route)-1]=="civil station":
        return routes[2]
    elif route[0]=="eastfort" and route[len(route)-1]=="neyyatinkara":
        return routes[0][::-1]
    elif route[0]=="parottukonam" and route[len(route)-1]=="eastfort":
        return routes[1][::-1]
    elif route[0]=="civil station" and route[len(route)-1]=="eastfort":
        return routes[2][::-1]
    else:
        return ['Error']


        


        
