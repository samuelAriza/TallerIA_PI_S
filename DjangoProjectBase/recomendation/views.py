from django.shortcuts import render
from movie.models import Movie
from dotenv import load_dotenv, find_dotenv
import json
import os
from openai import OpenAI
#from openai.embeddings_utils import get_embedding, cosine_similarity
import numpy as np



#Esta función devuelve una representación numérica (embedding) de un texto, en este caso
#la descripción de las películas
    

# Create your views here.
def recomendation(request):
    _ = load_dotenv('../open_ai_api_keys.env')
    client = OpenAI(
        api_key=os.environ.get('openai_api_key'),
    )
    def get_embedding(text, model="text-embedding-3-small"):
        text = text.replace("\n", " ")
        return client.embeddings.create(input = [text], model=model).data[0].embedding

    def cosine_similarity(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    with open('../movie_descriptions_embeddings.json', 'r') as file:
        file_content = file.read()
        movies = json.loads(file_content)
    
    searchTerm = request.GET.get('searchRecomendation') # GET se usa para solicitar recursos de un servidor
    if searchTerm:
        req = searchTerm
        emb = get_embedding(req)

        sim = []
        for i in range(len(movies)):
            sim.append(cosine_similarity(emb,movies[i]['embedding']))
        sim = np.array(sim)
        idx = np.argmax(sim)
        print("XXXXXX")
        print(movies[idx]['title'])
        movies = Movie.objects.filter(title=movies[idx]['title'])
    else:
        movies = Movie.objects.all()
        
    return render(request, 'recomendation.html', {'searchTerm':searchTerm, 'movies':movies})