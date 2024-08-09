from sheet.models import Cleaned_d
from sheet.models import Cleaned_da
from sheet.models import Cleaned_pens
from sheet.models import Cleaned_data
from sheet.models import Clean
from sheet.models import Sher
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import todo
from base.Custom_KB import custom_kb
from dotenv import load_dotenv 
import os
from django.conf import settings
from django.core.management import call_command
from accounts.models import assistant,collection
import pandas as pd
from django.apps import apps


load_dotenv()
api_key =  os.getenv('OPEN_AI_API_KEY')
os.environ["OPEN_AI_API_KEY"] = api_key

def insert_into_database(filepath,table_name):
    filepath = os.path.join(settings.MEDIA_ROOT, filepath)
    model_class = apps.get_model('sheet', table_name)
    all_fields = model_class._meta.get_fields()
    field_names = [field.name for field in all_fields]
    data = pd.read_excel(filepath)
    cols = [col for col in data.columns]
    print(f'feature name in table',field_names)
    print(f'feature name in dataframe',cols)
    for index, row in data.iterrows():
        entery = {}
        for i in range(0, len(cols)):
            entery[field_names[i+1]] = row.iloc[i]
        print(f'the data to be inserted is',entery)
        model_class.objects.create(**entery)
        
def todo_saved():
        data = todo.objects.all()
        for obj in data:
            if obj.name == 'embed':
                print(f'object element {obj.name} {obj.resources} {obj.assistant_id}')
                md_path = os.path.join(settings.MEDIA_ROOT, f'{obj.resources}.pdf')
                kb = custom_kb()
                kb.embed_file(api_key, md_path, embeding_directory='base/chroma_db', Collection_name = obj.resources.split(' ')[0])
                assistant.objects.filter(assistant_id=obj.assistant_id).update(collection_id=obj.resources.split(' ')[0])
                assistant_instance = assistant.objects.get(assistant_id = obj.assistant_id)
                collection_instance = collection(
                    collection_name = obj.resources.split(' ')[0],
                    assistant_id = assistant_instance
                    )
                collection_instance.save()

        for obj in data:
            if obj.name == 'migrate':
                call_command('makemigrations')
                call_command('migrate')
        for obj in data:
            if obj.name == 'store':
                table_name = obj.resources
                file_path = obj.path
                insert_into_database(file_path,table_name)
        data.delete()

todo_saved()

