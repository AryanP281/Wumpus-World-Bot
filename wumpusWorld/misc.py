#**********************************Imports******************************
import copy
import math

#*******************************Functons********************************
"""def bubble_sort(lst, return_copy=False) :
    if(not return_copy) :
        swapped = True
	    while swapped	:
			swapped = False
		    for a in range(1, len(lst)) :
			    if(lst[a] < lst[a - 1]) :
				    temp = lst[a - 1]
				    lst[a - 1]  = lst[a]
				    lst[a] = temp
				    swapped = True
    else :
        lst_cpy = copy.copy(lst)
        swapped = True
	    while swapped	:
		    swapped = False
		    for a in range(1, len(lst_cpy)) :
			    if(lst_cpy[a] < lst_cpy[a - 1]) :
				    temp = lst_cpy[a - 1]
				    lst_cpy[a - 1]  = lst_cpy[a]
				    lst_cpy[a] = temp
				    swapped = True"""

def re_lu(val) :
	"""The ReLu function"""

	if(val > 0) :
		return val
	else :
		return 0

def to_radians(degrees) :
	"""Converts degrees to radians"""

	return degrees * math.pi / 180.0

def get_occurrences(lst, element) :
	"""Returns the indices of all the occurrences of element in index"""

	occurrences = []

	for index in range(0, len(lst)) :
		if(lst[index] == element) :
			occurrences.append(index)

	return occurrences

def get_num_of_occurrences(lst, element) :
	"""Returns the number of times the element has occures in the list"""

	return len(get_occurrences(lst, element))

def intersection(lst1, lst2) :
	"""Returns the intersection of the two lists"""

	ints = []
	if(len(lst1) > len(lst2)) :
		for e in lst2 :
			if(e in lst1) :
				ints.append(e)
	else :
		for e in lst1 :
			if(e in lst2) :
				ints.append(e)

	return ints