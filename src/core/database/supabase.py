from supabase import create_client
from src.config.settings import SUPABASE_URL, SUPABASE_KEY

def get_supabase_client():
    return create_client(SUPABASE_URL, SUPABASE_KEY) 