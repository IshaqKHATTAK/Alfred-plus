import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')

# Initialize Django
django.setup()

# from accounts.models import chats

# deleted_count = todo.objects.filter(name='embed').delete()
# print(f'Deleted {deleted_count[0]} records.')

# from django.db import connection
# cursor = connection.cursor()
# cursor.execute("SELECT * FROM sheet_clean WHERE mix_type = %s", ['LMLC'])
# rows = cursor.fetchall()
# print(rows)