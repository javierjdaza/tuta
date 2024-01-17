import os
from dotenv import load_dotenv
load_dotenv()
from supabase import create_client, Client




def get_users_auth():
    url: str = os.getenv("SUPABASE_URL")
    key: str = os.getenv("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    response = supabase.table('users_db').select("*").execute()
    
    data = response.data
    
    return data