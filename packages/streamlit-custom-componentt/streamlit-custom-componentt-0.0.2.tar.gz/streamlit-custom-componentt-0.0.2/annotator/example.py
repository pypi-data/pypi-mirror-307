import streamlit as st
import fitz
import base64
from tempfile import NamedTemporaryFile

from annotator import annotator

st.subheader("PDF Annotator")

user_id = 2
doc_id = 1
supabase_url = 'https://lndnrkmllszfkltxmqqw.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxuZG5ya21sbHN6ZmtsdHhtcXF3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzEwNjMzOTYsImV4cCI6MjA0NjYzOTM5Nn0.Z8PPI83b3uyhc19GskQgOMHVJmuS7DHZ3EexFE8LFzY'

args = {
    'user_id': user_id,
    'doc_id': doc_id,
    'supabase_url': supabase_url,
    'supabase_key': supabase_key
}

num_clicks = annotator(args)