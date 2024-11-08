import pyanimalconverter.convert as convert
import sys

def min(meas: list) -> str:
    """
        Takes in a list of measurements as strings and returns 
        the smallest of them as a string. If any unit is incompatible
        with the others in the list (i.e. m with lb), an error is thrown.
        If list is empty, an error message is given. If the minimum appears 
        multiple times (possibly in different units), the earliest instance 
        is returned.
    """
    cur_min = ""
    minval = -1
    if(len(meas) == 0):
        print("List cannot be empty!")
        raise SystemExit(1)
    
    #otherwise check the first item, will define 'unit family'
    first: list = meas[0].split(" ")
    try:
        minval = float(first[0])
    except:
        return -3
    cur_min = meas[0]
    units = first[1]
    for i in range(1, len(meas)):
        item = meas[i].split(" ")
        try:
            val = convert.convert(float(item[0]), item[1], units)
        except SystemExit as e:
            raise e #something that wasn't a number was there
        except:
            return -3
        if val < 0:
            return val
        elif val < minval:
            #print("replacing", minval, "with", val)
            minval = val
            cur_min = meas[i]
        #else:
            #print("we have", val, "but min is",minval)
    return cur_min
    
def max(meas: list) -> str:
    """
        Takes in a list of measurements as strings and returns 
        the largest of them as a string. If any unit is incompatible
        with the others in the list (i.e. m with lb), an error is thrown.
        If list is empty, an error message is given. If the maximum appears 
        multiple times (possibly in different units), the earliest instance 
        is returned.
    """
    cur_max = ""
    maxval = -1
    if(len(meas) == 0):
        print("List cannot be empty!")
        raise SystemExit(1)
    
    #otherwise check the first item, will define 'unit family'
    first: list = meas[0].split(" ")
    try:
        maxval = float(first[0])
    except:
        return -3
    cur_max = meas[0]
    units = first[1]
    for i in range(1, len(meas)):
        item = meas[i].split(" ")
        try:
            val = convert.convert(float(item[0]), item[1], units)
        except SystemExit as e:
            raise e #something that wasn't a number was there
        except:
            return -3
        if val < 0:
            return val
        elif val > maxval:
            maxval = val
            cur_max = meas[i]
    return cur_max

# print(convert.convert(1, "m", "in"))
# print(convert.convert(1, "ft", "in"))
# input3 = ["24 in", "42 in", "1 ft", "1 m", "4 km"]
# print(min(input3))
#print(min(["4 nm", "2 in", "8 in"]))