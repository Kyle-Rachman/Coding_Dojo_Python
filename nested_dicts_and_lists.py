# Problem 1

x = [ [5,2,3], [10,8,9] ] 
students = [
    {'first_name':  'Michael', 'last_name' : 'Jordan'},
    {'first_name' : 'John', 'last_name' : 'Rosales'}
]
sports_directory = {
    'basketball' : ['Kobe', 'Jordan', 'James', 'Curry'],
    'soccer' : ['Messi', 'Ronaldo', 'Rooney']
}
z = [ {'x': 10, 'y': 20} ]

x[1][0] = 15
students[0]["last_name"] = "Bryan"
sports_directory["soccer"][0] = "Andres"
z[0]["y"] = 30

# Problem 2

def iterateDictionary(some_list):
    for dictionary in some_list:
        pair = ""
        for key, val in dictionary.items():
            pair += key + " - " + val + ", "
        print(pair[:-2])

# Problem 3

def iterateDictionary2(key_name,some_list):
    for dictionary in some_list:
        for key in dictionary.keys():
            if key == key_name:
                print(dictionary[key])

# Problem 4

def printInfo(some_dict):
    for key, info in some_dict.items():
        print(len(info), key.upper())
        for val in info:
            print(val)
        print("\n")

dojo = {
    'locations': ['San Jose', 'Seattle', 'Dallas', 'Chicago', 'Tulsa', 'DC', 'Burbank'],
    'instructors': ['Michael', 'Amy', 'Eduardo', 'Josh', 'Graham', 'Patrick', 'Minh', 'Devon']
}
printInfo(dojo)