# Algorithm to find the route map

# Abbreviations used:
#   N - Neyyatinkara
#   E - Eastfort
#   routes_obtained are the routes obtained from the image
#   destination is the user entered destination
#   location is the GPS location obtained

# Inputs: routes_obtained, destination, location
# Ouput: Final route 

from app import testing_current as tc
from app import routemap
import sys


# Prints the route.
# Input: Final route
# Output: Route to be displayed to the user

# Check if location is in routemap
# Input: Location
# Output: Boolean. 
#           If location in routemap returns True
#           If location not in routemap returns False 
def checkLocation(location, route_number):
    checkLoc = False
    for j in range(0,len(routemap.routes[route_number])):
        if location in routemap.routes[route_number][j]:
            checkLoc = True
            break
        else:
            checkLoc = False
    return checkLoc

# Check if user has entered a destination that is present in route map
# Input: Destination
# Output: Boolean. 
#           If destination in routemap returns True
#           If destination not in routemap returns False 
def checkDestination(dest, route_number):
    checkDest = checkLocation(dest, route_number)
    return checkDest

# Check if routes obtained from image is in route map
# Input: Routes obtained from image
# Output: Boolean. 
#           If Routes obtained from image is in routemap returns True
#           If Routes obtained from image is not in routemap returns False 

def checkRoutesObtained(routes_obtained, route_number):
    routeCheck = False
    for i in range(0,len(routes_obtained)):
        routeCheck = checkLocation(routes_obtained[i], route_number)  
        if not routeCheck:
            break 
    return routeCheck

# If more than 2 routes are in routes_obtained, shrink it to two routes
# i.e. only source and destination is required, intermediate stops are not required
# Input: routes_obtained

# Output: List
#           shrinked routes_obtained
def shrinkRoute(routes_obtained, route_number):
    shrinked_routes = routes_obtained

    if(checkRoutesObtained(routes_obtained, route_number)):
        # Case 1: When only one location is  obtained from the image
        if len(shrinked_routes)<2:
            shrinked_routes = 'Cannot process'

        # Case 2: When exactly two locations are  obtained from the image
        elif len(shrinked_routes) == 2:
            pass

        # Case 3: When more than two locations are obtained from the image
        elif len(shrinked_routes) > 2:
            new_routes_obtained = []
            new_routes_obtained.append(routes_obtained[0])
            new_routes_obtained.append(routes_obtained[(len(routes_obtained)-1)])
            shrinked_routes = new_routes_obtained
        else:
                pass
    else:
        shrinked_routes = ' \n Please take another bus.'

    return shrinked_routes

# To get the direction of the route. N -> E or E -> N
# Input: Shrinked routes_obtained, i.e. src and dest 
# Output: List 
#           N -> E or E -> N 
def getRoute(routes_obtained, route_number):
    routes = shrinkRoute(routes_obtained, route_number)
    if len(routes) == 1:
        return routes                           #routes is error string
    else:
        source_index = routemap.routes[route_number].index(routes[0])
        destination_index = routemap.routes[route_number].index(routes[1])
        length_route = len(routemap.routes[route_number])-1

        # E -> N
        if source_index > destination_index:
            reversedRoutes = []
            for i in range(length_route,-1,-1):
                reversedRoutes.append(routemap.routes[route_number][i])
            return reversedRoutes
        # N -> E
        elif source_index < destination_index:
            return routemap.routes[route_number]
        else:
            pass
    

# Case 1: Display all the routes from the user_entered_destination and the destination
#         Location is the GPS location from the user
# Inputs: Route, routes_obtained, location, dest
# Output: If route found, call printRoute else display error
def findRouteWithLocation(routes_obtained, location, dest, route_number):
    routes = shrinkRoute(routes_obtained, route_number)
    if len(routes) == 1:
        return routes                                   #routes is error string
    else:
        route = getRoute(routes, route_number)
        
        source = routes[0]
        destination = routes[1]

        location_index = route.index(location)
        destination_index = len(routemap.routes[route_number]) - 1 
        source_index = route.index(source)
        
        your_route = []
        goes = False

        for i in range(location_index,destination_index+1):
            your_route.append(route[i])
            if dest in your_route:
                goes = True
        
        if (goes):
            return your_route
        else:
            your_route = ['\n Please take another(opposite) bus stop ']
            return your_route                       #error string
    


# Case 2: Display all the routes from the user_entered_destination and the default destination
# Inputs: Route, routes_obtained, dest
# Output: If route found, call printRoute else display error
def findRouteWithoutLocation(routes_obtained, dest, route_number):
    routes = shrinkRoute(routes_obtained, route_number)
    if len(routes) == 1:
        return routes                               #routes is error string
    else:
        route = getRoute(routes, route_number)

        source = routes[0]
        destination = routes[1]

        default_destination_index = len(routemap.routes[route_number]) - 1
        default_source_index = routes.index(source)
        
        your_route = []
        goes = False

        for i in range(default_source_index, default_destination_index+1):
            your_route.append(route[i])
            if dest in your_route:
                goes = True

        if (goes):
            return your_route
        else:
            your_route = ['\n Please take another(opposite) bus stop']
            return your_route


# Case 3: Display all the routes
# Inputs: Destination
# Output: If route found, call printRoute
def findRouteWithoutDestination(routes_obtained, route_number):
    if(checkRoutesObtained(routes_obtained, route_number)):
        routes = shrinkRoute(routes_obtained, route_number)
        if len(routes) == 1:
            return routes                           #routes is error string if type(routes) == list:
        else:
            route = getRoute(routes, route_number)
            return route
    else:
        pass

# Main function to find the route
def findRoute(routes_obtained, route_number, dest = "", location = ""):

    result=[]

    if (routes_obtained is not None) & (routes_obtained != []):
        if(checkRoutesObtained(routes_obtained, route_number)):
            if (shrinkRoute(routes_obtained, route_number)=='Cannot process'):
                result=['Cannot process']
            else:
                if(dest is not None) & (dest != ""):
                    if(checkDestination(dest, route_number)):
                        if (location is not None) & (location != ""):
                            if(checkLocation(location, route_number)):
                                result = findRouteWithLocation(routes_obtained, location, dest, route_number)

                            else:
                                result = ['Please find another bus.']
                        else:
                            result = findRouteWithoutLocation(routes_obtained, dest, route_number)
                    else:
                        result = ['Error']
                else:
                    result=findRouteWithoutDestination(routes_obtained, route_number)
                    print(result)
        else:
            result = ['Error']
    else:
        result = ['Error']

    return result

def mainFindRoute(imagepath, dest, loc):
        
    routes_obtained=[]
    del routes_obtained[:]
    routes_obtained=tc.testing(imagepath)  #import the file 

    
    destination = dest
    location = loc

    routes_extract = routes_obtained[0]
    route_number= routes_obtained[1]

    if route_number>2:
        return ['Error']

    # Call this function to find the route
    result = findRoute(routes_extract, route_number, destination, location)

    return result