
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
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
from yelpapi import YelpAPI
from pprint import pprint 
import json
import os
import pandas as pd

params = {}
# results = []
api_key = "J_wCiYL03se4K_JN7O0A0BKew1Q9F6rnuzdOCzt2IgV6142Hm3sXSQdjIJPmSkleKhXgqWr6WVsCdyhqghoflD4Dcwqwn1wQ9jeAOzex0adIZ1b63L950iMqPYxlY3Yx"

def set_data():
    locaton_choice = location_input.get()
    if locaton_choice:
        term_choice = term_input.get()
        radius_choice = radius_spinbox.get()
        limit_choice = limit_spinbox.get()
        sort_by_choice = sort_by_combobox.get()

        keys = ["location", "term", "radius", "limit", "sort_by"]
        choices = [locaton_choice, term_choice, radius_choice, limit_choice, sort_by_choice]
        # print(choices)
        # print(keys)

        temp_params = dict(map(lambda key, value : (key, value), keys, choices))
        # print(temp_params)

        for keys, values in temp_params.items():
            if temp_params[keys] is not '' or 0:
                params[keys] = values
    else:
        tkinter.messagebox.showwarning(title= "Error", message="Location is required.")

    # print(params)
 

def save_name():
    try: 
        results
    except NameError:
        tkinter.messagebox.showwarning(title= "Error", message="No results to save")
    else:
        save_window = tkinter.Tk()
        save_window.title("Save File")

        save_frame = tkinter.Frame(save_window)
        save_frame.pack()

        input_frame = tkinter.LabelFrame(save_frame, text="Filename")
        input_frame.grid(row=0, column=0)

        input_label = tkinter.Label(input_frame, text= "Name file (without '.csv')")
        input_label.grid(row= 0, column=0)

        global save_input
        save_input = tkinter.Entry(input_frame)
        save_input.grid(row=1, column=0)

        save_file_button = tkinter.Button(save_frame, text="Enter", command=save)
        save_file_button.grid(row=1, column=0)
        # print()
        # print("Name file (without '.csv'):")
        # filename = input() + ".csv"
        # results.to_csv(filename)

        #with open(filename, 'w', encoding='utf-8') as f:
        #    json.dump(results, f, ensure_ascii=False, indent=4)
        
        # print("File successfully saved!")
        save_window.mainloop()

        # json_results = json.dumps(results, indent = 3)
        # pprint(json_results)

def save():
    filename = save_input.get()
    print(filename[-4:])
    if filename[-4:] == '.csv':
        tkinter.messagebox.showwarning(title="Error", message="Incorrect filename - remove '.csv'")
        save_name()
    else:
        filename = filename + '.csv'
        results.to_csv(filename)
    


def format(first_results):
    temp_results = {}
    temp_results = first_results["businesses"]
    for n in temp_results:
        del n["alias"]
        del n["categories"]
        del n["coordinates"]
        del n["display_phone"]
        del n["id"]
        del n["image_url"]
        del n["is_closed"]
        del n["transactions"]
        del n["url"]
        del n["location"]["address1"]
        del n["location"]["address2"]
        del n["location"]["address3"]
        del n["location"]["city"]
        del n["location"]["country"]
        del n["location"]["state"]
        del n["location"]["zip_code"]
        n["location"] = n["location"]["display_address"]
        n["location"] = ', '.join(n["location"])
    
    # pprint(temp_results)
    # print(json.dumps(temp_results, indent = 3))
    return temp_results

def search():
    if not params:
        tkinter.messagebox.showwarning(title= "Error", message="Set terms first before searching.")
    else:
        print("Searching...")
        with YelpAPI(api_key) as yelp_api:
            first_results = yelp_api.search_query(**params)
    
    global results
    results = format(first_results)
    results = pd.DataFrame.from_dict(results)

    root = Tk()
    root.title("Results")
    display_results = tkinter.Text(root)
    display_results.pack(expand=True, fill=BOTH)
    display_results.insert(INSERT, results)
    display_results['state'] = 'disabled'
    
    root.mainloop()

    



window = tkinter.Tk()
window.title("Yelp Business Call List")

frame = tkinter.Frame(window)
frame.pack()

search_terms_frame = tkinter.LabelFrame(frame, text= "Search Terms")
search_terms_frame.grid(row= 0, column=0, padx=20, pady=20)

location_label = tkinter.Label(search_terms_frame, text="Location (required)")
location_label.grid(row=0, column=0)

term_label = tkinter.Label(search_terms_frame, text= "Search Term")
term_label.grid(row=0, column=1)

radius_label = tkinter.Label(search_terms_frame, text="Radius (max = 40000 meters)")
radius_spinbox = tkinter.Spinbox(search_terms_frame, from_=0, to=40000)
radius_label.grid(row=0, column=2)
radius_spinbox.grid(row=1, column=2)

limit_label = tkinter.Label(search_terms_frame, text= "Limit (max = 50)")
limit_spinbox = tkinter.Spinbox(search_terms_frame, from_=0, to=50)
limit_label.grid(row=0, column=3)
limit_spinbox.grid(row=1, column=3)

location_input = tkinter.Entry(search_terms_frame)
location_input.grid(row=1, column=0)
term_input = tkinter.Entry(search_terms_frame)
term_input.grid(row=1, column=1)


sort_by_label = tkinter.Label(search_terms_frame, text="Sort By")
sort_by_combobox = ttk.Combobox(search_terms_frame, values=["", "best_match", "rating", "review_count", "distance"])
sort_by_label.grid(row=2, column=0)
sort_by_combobox.grid(row=3, column=0)

# Buttons
set_button = tkinter.Button(frame, text="Set Terms", command=set_data)
set_button.grid(row=2, column=0)

save_button = tkinter.Button(frame, text="Search and Display", command=search)
save_button.grid(row=3, column=0)

display_button = tkinter.Button(frame, text="Save and Export (as .csv)", command=save_name)
display_button.grid(row=4, column=0)



window.mainloop()
