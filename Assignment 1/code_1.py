import json
with open("kb.json","r") as file:
    jsonData = json.load(file)

def add_new_destination(jsonData):
    print("Great!")
    location = input("Enter the location name: ")
    budget = input("Enter your Budget in Rupees: ")
    weather = input("Enter the weather at that location: ")
    activities = input("Enter the activities you can do there: ")
    places = input("Enter the places to visit there: ")
    transport = input("Enter the transport facilties there: ")
    food = input("Please tell if food is available there (Yes/No): ")
    review = input("Please enter a review: ")
    rating = input("Please enter the rating of the destination (0-10): ")
    reviews=[]
    reviews.append(review)
    new_entry = {
        "Location": location,
        "Budget_(in_Rupees)": budget,
        "Weather": weather,
        "Activities": activities,
        "Places_to_visit": places,
        "Transport_Connectivity": transport,
        "Rating":rating,
        "Good_Food_Availability": food,
        "Reviews": reviews
    }
    jsonData.append(new_entry)
    with open("kb.json", "w") as file:
        json.dump(jsonData, file)

    print("\nGreat!!!\nYour new destination has been added.\nThis will definitely help new users to choose their destintaion.\nThank You!")
    print("\n")


def recommend_destination(jsonData):
    weather = input("Enter the preferred weather condition for the place: ")
    food_availability = input("Do you want the place to have good food? (Yes/No): ")
    budget = input("What is your budget (in Rupees): ")
    locations = []
    c=0
    for i in jsonData:
        if(i["Good_Food_Availability"]==food_availability and i["Weather"]==weather and int(i["Budget_(in_Rupees)"])<=int(budget)):
            locations.append(i["Location"])
            # c=c+1
    if(len(locations)==0):
        print("No location meets your desire!\nEnding Program...")
        exit()
    else: 
        print("Following are the locations that meet your needs:")
        for i in range(len(locations)):
            print(locations[i])
    return locations

def add_new_feedback(jsonData):
    target_index = next((index for index, item in enumerate(jsonData) if item["Location"] == destination), None)
    new_rev = input("Please enter your review: ")
    i["Reviews"].append(new_rev)
    print(i["Reviews"])

    if target_index is not None:
        jsonData[target_index]["Reviews"] = i["Reviews"]
        print(f"Reviews for {destination} updated.")
        print("Thank You so much for your feedback!")
        print("Ending Program...")

    with open("kb.json", "w") as file:
        json.dump(jsonData, file, indent=4)


# Program Starts here
print("Welcome to our Travel Guide\nHere, you can find your dream Destination and see its reviews\nOur travel guide also allows you to add reviews and new Destinations")
print("First lets see what you want to do here...")
add = input("Are you here to add a new location? (Yes/No): ")
if(add=="Yes"):
    add_new_destination(jsonData)
else:
    print("No worries! We also have a huge number of destinations for you to explore...")

start=input("Now, would you like to see a destination suitable for you? (Yes/No): ")
if(start=="Yes"):
    locations=recommend_destination(jsonData)

    destination = input("Enter a location from the above locations that you would like to visit (or \"q\" to exit): ")
    if(destination=="q"):
        print("Thank You for your time")
        print("Ending Program...")
        exit()
    else:
        for dest in locations:
            if dest==destination:
                print("Great Choice!")
                for i in jsonData:
                    if(i["Location"]==destination):
                        print("In "+destination+", you can do various activities like "+i["Activities"]+" , visit famous places like "+i["Places_to_visit"]+" with an incredible transport service that includes "+i["Transport_Connectivity"])
                        print("Also, the place is rated"+i["Rating"]+"by the users")
                        rev = input("Would you like to see its reviews? (Yes/No): ")
                        if(rev=="Yes"):
                            print("Sure")
                            print("Here are the reviews for the destination: "+destination)
                            reviews = i["Reviews"]
                            print(reviews)
                            add_rev = input("Would you like to add a review for this place? (Yes/No): ")
                            if(add_rev=="Yes"):
                                add_new_feedback(jsonData)
                        else: 
                            print("No problem!")
                            print("Ending program...")
                            exit()
else: 
    print("No Problem")
    print("Thank You for your time")
    print("We hope to see you again!!")

