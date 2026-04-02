import os
import bcrypt
from flask import session, redirect
from dotenv import load_dotenv
from supabase import create_client, Client
from functools import wraps

load_dotenv()

supabase: Client = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_PUBLISHABLE_KEY")
)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    
    return decorated_function


def get_passid_hash(entered_username, entered_password):

    response = (
    supabase.table("users")
    .select("id, password_hash, username")
    .eq("username", entered_username)
    .execute()
    )

    user_data = response.model_dump()
    hashed_pass = user_data["data"][0]["password_hash"].encode("utf-8")

    check = bcrypt.checkpw(
        password=entered_password,
        hashed_password=hashed_pass
    )

    if check: 
        return user_data["data"][0]["id"]

    return []

def retrieve_created():

    user_id = session.get("user_id")

    response = (
        supabase.table("Personal_data")
        .select("licence_no, product_name, time_of_create")
        .eq("created_by", user_id)
        .execute()
    )

    user_created = response.model_dump()["data"]



    return user_created

def create_personal_data(dictlist):

    try:
        response = (
            supabase.table("Personal_data")
            .insert(dictlist)
            .execute()
        )
        return response.data
    except Exception as e:
        return str(e)

def delete_entry(licence):

    response = (
        supabase.table("Personal_data")
        .delete()
        .eq("licence_no", licence)
        .execute()
    )
