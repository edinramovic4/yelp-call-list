
#    Copyright (c) 2013, Triad National Security, LLC
#    All rights reserved.

#    Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
#    following conditions are met:

#    * Redistributions of source code must retain the above copyright notice, this list of conditions and the following
#      disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
#      following disclaimer in the documentation and/or other materials provided with the distribution.
#    * Neither the name of Triad National Security, LLC nor the names of its contributors may be used to endorse or
#      promote products derived from this software without specific prior written permission.

#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
#    INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
#    WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import tkinter
from yelpapi import YelpAPI 

window = tkinter.Tk()

window.mainloop()


def search(api_key):
    start_params = {
        "location": False,
        "term": False,
        "radius": False,
        "limit": False,
        "sort_by": False
    }
    
    sort_by_choices = {"best_match", "rating", "review_count", "distance"}


    start_params["location"] = input("Type location (required): ")
    print()
    finish = True

    while(finish): # enclose switch statement into loop so it only finishes when the user is ready
        print("Change additional terms:")
        print("Term (String): a")
        print("Radius in Meters (Max 40,000m = 25 mi) (Int): b")
        print("Limit (Max 50) (Int): c")
        print("Sort By ('best-match', 'rating', 'review_count', 'distance') (String): d")
        print("Search : e")
        print()
        choice = input()
        match choice:
            case 'a':
                print()
                user_term = input("Input term: ")
                if type(user_term) is not str:
                    print("Invalid input, please put a correct input.")
                    continue # place continue statements in case of incorrect inputs
                else:
                    start_params['term'] = user_term
            case 'b':
                user_radius = input("Input radius: ")
                
                if type(int(user_radius)) is not int:
                    print("Invalid input, please put a correct input.")
                    continue
                else:
                    start_params['radius'] = int(user_radius)
            case 'c':
                user_limit = input("Input limit (int): ")
                if type(int(user_limit)) is not int:
                    print("Invalid input, please put a correct input.")
                    continue
                else:
                    start_params['limit'] = int(user_limit)
            case 'd':
                user_sort_by = {input("Input sort by: ")}
                if not user_sort_by.issubset(sort_by_choices):
                    print("Invalid input, please put a correct input.")
                    continue 
                else:
                    start_params['sort_by'] = user_sort_by.pop()
            case 'e':
                finish = False
            case _:
                print("\nInvalid character. Please select a valid character.\n")
                continue

    params = {}
    print(start_params)

    for keys, values in start_params.items():
        if start_params[keys] is not False:
            params[keys] = values
    
    print(params)
        
    with YelpAPI(api_key, timeout_s=3.0) as yelp_api:
        search_results = yelp_api.search_query(**params)
        pprint(search_results)
        print("Search complete! Results saved.")
        menu()
   
# def format():

# def display():


# def save():

def menu():
    print("Select options:")
    print("Search: 'a'")
    print("Display: 'b'")
    print("Save: 'c'")
    choice = input() # call  input function to get decision

    match choice:
        case 'a':
            search(api_key)
        case 'b':
            display()
        case 'c':
            save()
        case _:
            print("\nInvalid character. Please select a valid character.\n")
            menu()

api_key = input("Please enter your Yelp API key: ")
print()
menu() # loop back to menu start to continue program