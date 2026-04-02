import bcrypt
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from flask import Flask, session

import csv
from services.medicine_service import get_ingredientlicence_by_name
from services.sessions_service import create_personal_data
# pw = b''
# s = bcrypt.gensalt()

# h = bcrypt.hashpw(pw, s) # Hash password
# print(s)
# print(h)


# load_dotenv()

# supabase: Client = create_client(
#     os.environ.get("SUPABASE_URL"),
#     os.environ.get("SUPABASE_PUBLISHABLE_KEY")
# )

# response = (
#     supabase.table("users")
#     .select("id, password_hash, username")
#     .eq("username", "zebrahorses")
#     .execute()
# )

# user_pass = "!Filipinowarrior@123"
# user_data = response.model_dump()
# hashed_pass = user_data["data"][0]["password_hash"].encode("utf-8")
# print(hashed_pass)
# check = bcrypt.checkpw(
#     password=user_pass.encode("utf-8"),
#     hashed_password=hashed_pass
# )

# if check: 
#     print(user_data["data"][0]["id"])


# To insert admin users: doesnt work due to RLS check again later
load_dotenv()

supabase: Client = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_PUBLISHABLE_KEY")
)

# pw = b'!Filipinowarrior@123'
# s = bcrypt.gensalt()

# h = bcrypt.hashpw(pw, s) # Hash password
# print(h)
# h = h.decode("utf-8")
# print(h)

# response = (
#     supabase.table("users")
#     .insert({"username": "zennithlennith", "password_hash": h})
#     .execute()
# )

# to_update = []

# with open("Medicine Data/ListingofRegisteredTherapeuticProducts.csv", 'r', encoding='utf-8') as file:
#     csvreader = csv.DictReader(file)
#     #licence_no, product_name, license_holder, approval_d, forensic_classification, atc_code, dosage_form, route_of_administration, manufacturer, country_of_manufacturer, active_ingredients, strength
#     for row in csvreader:

#         #  licence_no = row["licence_no"]
#         #  product_name = row["product_name"]
#         #  license_holder = row["license_holder"]
#         #  approval_d = row["approval_d"]
#         #  forensic_classification = row["forensic_classification"]
#         #  atc_code = row["atc_code"]
#         #  dosage_form = row["dosage_form"]
#         #  route_of_administration = row["route_of_administration"]
#         #  manufacturer = row["manufacturer"]
#         #  country_of_manufacturer = row["country_of_manufacturer"]
        
#         row["product_name"] = row["product_name"].upper()

#          # remove && replace with ,
#         row["active_ingredients"] = ", ".join(row["active_ingredients"].split("&&"))
        

#         row["strength"] = ", ".join(row["strength"].split("&&"))

#         to_update.append(row)

# print(to_update)
         
# with open('Medicine Data/updated.csv', 'w', newline='', encoding='utf-8') as csvfile:
#     fieldnames = ['licence_no', 'product_name', 'license_holder', 'approval_d', 'forensic_classification', 'atc_code', 'dosage_form', 'route_of_administration', 'manufacturer', 'country_of_manufacturer', 'active_ingredients', 'strength']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()
#     writer.writerows(to_update)

# data = get_ingredientlicence_by_name("CONSU CAPSULE")

# print(data["licence_no"])

from services.medicine_service import get_similar_medicines, get_known_licences

to = "Paracetamol Tablet 500 Mg".upper()
print(to)
name = get_ingredientlicence_by_name(to)
print(name)
data = get_similar_medicines(name["active_ingredients"], name["licence_no"])
length = len(data)
print(length)
known_medicines = get_known_licences()
# for i in range(len(data)):
#         if data[i]["licence_no"] in known_medicines:
#             data.pop(i)

if data[45]["licence_no"] in known_medicines:
             data.pop(45)

print(data)
