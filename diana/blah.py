class City:

    def __init__(self, code, name, region, population, latitude, longitude):
        self.code = code
        self.name = name
        self.region = region
        self.population = population
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        #   Using string format will allow for the method to return a string with the
        #   selected instance variables without spaces between the commas.
        return "{},{},{},{}".format(self.name, self.population, self.latitude, self.longitude)

from random import randint

in_file = open("world_cities.txt")
#   This list, city_objects, will hold all the object references with each city's information.
city_objects = []
for line in in_file:
    #   Strip the line to get rid of the newline whitespace character.
    line.strip()
    #   Split to separate info and store them as the instance variables for the city class.
    code, name, region, population, latitude, longitude = line.split(",")
    #   Create a reference to the city class.
    city_information = City(code, name, region, population, latitude, longitude)
    # print(city_information.__str__())
    # Append the previously empty list to hold the strings for the city class reference, that include
    # name, population, latitude, and longitude
    city_objects.append(city_information)
in_file.close()


def partition(city_objects, front_i, back_i, compare_func):
    # Generate a pivot location
    pivot_i = randint(front_i, back_i - 1)  # Might be off by 1, idk. Test it.
    # Swap pivot to front
    city_objects[pivot_i], city_objects[front_i] = city_objects[front_i], city_objects[pivot_i]
    # Set pivot_i to match the pivot's new location
    pivot_i = front_i
    # Set the greater location to be just above the pivot
    for greater_i in range(pivot_i, back_i - 1):
        # If the pivot is less than the target, encompass the target within the greater section.
        if not compare_func(city_objects, pivot_i, greater_i + 1):
            city_objects[pivot_i], city_objects[greater_i + 1] = city_objects[greater_i + 1], city_objects[pivot_i]
            # Swap the pivot into the location at the front of the greater area
            city_objects[pivot_i + 1], city_objects[greater_i + 1] = city_objects[greater_i + 1], city_objects[
                pivot_i + 1]
            # Increment your pivots
            pivot_i += 1
        # Return where the pivot now is, having finished partitioning
    return pivot_i


def compare_population(city_objects, pivot_i, greater_i):
    return city_objects[pivot_i].population <= city_objects[greater_i].population


def quicksort(city_objects, front_i, back_i, compare_func):
    if back_i - front_i > 1:
        pivot_i = partition(city_objects, front_i, back_i, compare_func)
        # print(city_objects[:pivot_i], city_objects[pivot_i], city_objects[pivot_i+1:])
        quicksort(city_objects, front_i, pivot_i, compare_func)
        quicksort(city_objects, pivot_i + 1, back_i, compare_func)


quicksort(city_objects, 0, len(city_objects), compare_population)

#   Create new file that will contain the output information of each city's
#   Name, population, latitude, and longitude.
out_file = open("cities_pop_out.txt", "w")
#   Create a for loop for every item in the list to_write, which is every city in world_cities.txt/
for i in range(len(city_objects)):
    #   Within the output file, write each string that is returned and stored within the to_write list.
    string = city_objects[i].__str__()
    out_file.write(string)
#   Close the file.
out_file.close()
