num1 = 42 # variable declaration, initialize Numbers
num2 = 2.3 # variable declaration, initialize Numbers
boolean = True # variable declaration, initialize Boolean
string = 'Hello World' # variable declaration, initialize Strings
pizza_toppings = ['Pepperoni', 'Sausage', 'Jalepenos', 'Cheese', 'Olives'] # variable declaration, initialize List
person = {'name': 'John', 'location': 'Salt Lake', 'age': 37, 'is_balding': False} # variable declaration, initialize Dict
fruit = ('blueberry', 'strawberry', 'banana') # variable declaration, initialize Tuple
print(type(fruit)) # log statement, type check
print(pizza_toppings[1]) # log statement, access value (List)
pizza_toppings.append('Mushrooms') # add value (List)
print(person['name']) # log statement, access value (Dict)
person['name'] = 'George' # change value (Dict)
person['eye_color'] = 'blue' # add value (Dict)
print(fruit[2]) # log statement, access value (Tuple)

if num1 > 45: # if
    print("It's greater") # log statement
else: # else
    print("It's lower") # log statement

if len(string) < 5: # if, length check
    print("It's a short word!") # log statement
elif len(string) > 15: # else if, length check
    print("It's a long word!") # log statement
else: # else
    print("Just right!") # log statement

for x in range(5): # stop for loop
    print(x) # log statement
for x in range(2,5): # start for loop, stop for loop
    print(x) # log statement
for x in range(2,10,3): # start for loop, stop for loop, increment for loop
    print(x) # log statement
x = 0 # variable declaration, initialize Numbers
while(x < 5): # start while loop
    print(x) # log statement
    x += 1 # increment while loop

pizza_toppings.pop() # delete value (List)
pizza_toppings.pop(1) # delete value (List)

print(person) # log statement
person.pop('eye_color') # delete key:value (Dict)
print(person) # log statement

for topping in pizza_toppings: # sequence for loop
    if topping == 'Pepperoni': # if
        continue # continue for loop
    print('After 1st if statement') # log statement
    if topping == 'Olives': # if
        break # break for loop

def print_hello_ten_times(): # function
    for num in range(10): # stop for loop
        print('Hello') # log statement

print_hello_ten_times() # function

def print_hello_x_times(x): # function, parameter
    for num in range(x): # stop for loop
        print('Hello') # log statement

print_hello_x_times(4) # function, argument

def print_hello_x_or_ten_times(x = 10): # function, parameter
    for num in range(x): # stop for loop
        print('Hello') # log statement

print_hello_x_or_ten_times() # function
print_hello_x_or_ten_times(4) # function, argument


"""
Bonus section
"""

# print(num3)
# num3 = 72
# fruit[0] = 'cranberry'
# print(person['favorite_team'])
# print(pizza_toppings[7])
#   print(boolean)
# fruit.append('raspberry')
# fruit.pop(1)