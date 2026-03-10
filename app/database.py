import os
from supabase import create_client, Client
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL: str = os.environ.get("SUPABASE_URL")
SUPABASE_KEY: str = os.environ.get("SUPABASE_KEY")
SUPABASE_JWT_SECRET: str = os.environ.get("SUPABASE_JWT_SECRET")

supabase_connection: Client = create_client(SUPABASE_URL, SUPABASE_KEY)