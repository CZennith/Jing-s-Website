import csv
import os
from dotenv import load_dotenv
from supabase import create_client, Client

#store into memory
medicine_data = []
medicine_by_licence = {}
medicine_name_list = []
active_ingredient_list = []
symptom_name_list = []
symptom_medicine_list = {}

personal_data = {}
known_medicine_list = []
known_medicine_licences = []

load_dotenv()

supabase: Client = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_PUBLISHABLE_KEY")
)



def first_letter_capital(to_cap):
    
    to_cap = to_cap.lower()
    inp_list = to_cap.split(" ")

    for i in range(len(inp_list)):
        inp_list[i] = inp_list[i].capitalize()

    return " ".join(inp_list)



with open("Medicine Data/ListingofRegisteredTherapeuticProducts.csv", 'r', encoding='utf-8') as file:
    csvreader = csv.DictReader(file)

    for row in csvreader:
         medicine_data.append(row)

         licence_no = row["licence_no"]
         # remove && replace with ,
         row["active_ingredients"] = ", ".join(row["active_ingredients"].split("&&"))

         #first letter capitalisation
         row["active_ingredients"] = first_letter_capital(row["active_ingredients"])
         row["product_name"] = first_letter_capital(row["product_name"])
        
         medicine_by_licence[licence_no] = row

         medicine_name_list.append(row["product_name"])
         if row["active_ingredients"] not in active_ingredient_list:
             active_ingredient_list.append(row["active_ingredients"])

def reset_personal_data():
    personal_data.clear
    known_medicine_list.clear()
    known_medicine_licences.clear()

    return 

def get_personal_data_sp():
    response = (
        supabase.table("Personal_data")
        .select("*")
        .execute()
    )
    supabase_data = response.model_dump() 

    for row in supabase_data["data"]:

            row.pop("id")
            licence_no = row["licence_no"]

            known_medicine_licences.append(licence_no)
            known_medicine_list.append(medicine_by_licence[licence_no])


            temp_dict = row
            temp_dict["drug_interaction"] = row["drug_interaction"].split(", ")
            temp_dict["contraindication"] = row["contraindication"].split(", ")
            temp_dict["side_effects"] = row["side_effects"].split(", ")


            personal_data[licence_no] = temp_dict

get_personal_data_sp()

# def update_personal_data_sp():
#     response = (
#         supabase.table("Personal_data")
#         .select("*")
#         .execute()
#     )
#     supabase_data = response.model_dump() 

#     starting_index = len(known_medicine_list)
#     ending_index =  len(supabase_data["data"]) - 1

#     for i in range(starting_index, ending_index):

#             supabase_data["data"][i].pop("id")
#             licence_no = supabase_data["data"][i]["licence_no"]
#             known_medicine_list.append(medicine_by_licence[licence_no])

#             temp_dict = supabase_data["data"][i]
#             temp_dict["drug_interaction"] = supabase_data["data"][i]["drug_interaction"].split(", ")
#             temp_dict["contraindication"] = supabase_data["data"][i]["contraindication"].split(", ")
#             temp_dict["side_effects"] = supabase_data["data"][i]["side_effects"].split(", ")


#             personal_data[licence_no] = temp_dict



# with open("Medicine Data/Jingendata.csv", 'r', encoding='utf-8') as file:
#     csvreader = csv.DictReader(file)

#     for row in csvreader:

#         licence_no = row["licence_no"]
#         known_medicine_list.append(medicine_by_licence[licence_no])

#         temp_dict = row
#         temp_dict["drug_interaction"] = row["drug_interaction"].split(", ")
#         temp_dict["contraindication"] = row["contraindication"].split(", ")
#         temp_dict["side_effects"] = row["side_effects"].split(", ")


#         personal_data[licence_no] = temp_dict

# with open("Medicine Data/Syhmptoms.csv", 'r', encoding='utf-8') as file:
#     csvreader = csv.DictReader(file)

#     for row in csvreader:
#         symptom = row["symptom"]

#         symptom_name_list.append(symptom)
#         symptom_medicine_list[symptom] = row["medication"].split(", ")



def get_personal_data(licence_no):
     
    return personal_data[licence_no]

def get_known_licences():
    
    response = (
        supabase.table("Personal_data")
        .select("id")
        .execute()
    )
    check_data = response.model_dump()
    if len(check_data["data"]) != len(known_medicine_list):
        
        reset_personal_data()
        get_personal_data_sp()

    return known_medicine_licences

def get_known_medicines():

    response = (
        supabase.table("Personal_data")
        .select("id")
        .execute()
    )
    check_data = response.model_dump()
    if len(check_data["data"]) != len(known_medicine_list):
        
        reset_personal_data()
        get_personal_data_sp()

    return known_medicine_list

def get_medicine_list():
    return medicine_name_list

# def get_symptom_list():
#     return symptom_name_list

def search_medicine(query):
    results = []

    for row in medicine_data:
        
        if query.upper() in row["product_name"].upper() or query.upper() in row["active_ingredients"].upper():
            results.append(row)

    return results


def search_medicine_by_licence(returned_licence_no):

    if medicine_by_licence[returned_licence_no]:
        return medicine_by_licence[returned_licence_no]
    else:
        return None
    
# def search_medicine_by_symptom(symptom):

#     if symptom in [symptom to medicine dictionary]:
#         return dictionary[symptom]
#     else:
#         return []


def get_medicine_ingredient(ingredient):
    returned_ingredients = []

    # check for multiple ingrdients
    indiv_ingredients = ingredient.split(", ")

    for split_ingredient in indiv_ingredients:

        # in case there's a EQV        
        if " EQV. TO " in split_ingredient.upper():
            returned_ingredients.append(split_ingredient.upper().split(" EQV. TO ")[-1])
        elif " EQV. " in split_ingredient.upper():
            returned_ingredients.append(split_ingredient.upper().split(" EQV. ")[-1])
        elif " EQV TO " in split_ingredient.upper():
            returned_ingredients.append(split_ingredient.upper().split(" EQV TO ")[-1])
        elif " EQV " in split_ingredient.upper():
            returned_ingredients.append(split_ingredient.upper().split(" EQV ")[-1])
        elif " EQV. TO " in split_ingredient.upper():
            returned_ingredients.append(split_ingredient.upper().split(" EQUV. TO ")[-1])
        elif " EQUV. " in split_ingredient.upper():
            returned_ingredients.append(split_ingredient.upper().split(" EQUV. ")[-1])
        elif " EQUV " in split_ingredient.upper():
            returned_ingredients.append(split_ingredient.upper().split(" EQUV ")[-1])
        elif " EQUIVALENT TO " in split_ingredient.upper():
            returned_ingredients.append(split_ingredient.upper().split(" EQUIVALENT TO ")[-1])
        else:
            returned_ingredients.append(split_ingredient.upper())

    return returned_ingredients

def replace_and_symbol(input):

    return input.split("&&")
    

def get_ingredientlicence_by_name(name):

    response = (
        supabase.table("gov_data")
        .select("licence_no, active_ingredients")
        .eq("product_name", name)
        .execute()
    )

    data = response.model_dump()["data"][0]

    return data

def get_similar_medicines(ingredient, licence):

    response = (
        supabase.table("gov_data")
        .select("licence_no, product_name")
        .eq("active_ingredients", ingredient)
        .execute()
    )

    data = response.model_dump()["data"]

    for i in range(len(data)):

        if data[i]["licence_no"] == licence:

            data.pop(i)
            return data
        
    
    
    return data

def get_product_name(licence):

    response = (
        supabase.table("gov_data")
        .select("product_name")
        .eq("licence_no", licence)
        .execute()
    )

    data = response.model_dump()["data"][0]["product_name"]

    return data

