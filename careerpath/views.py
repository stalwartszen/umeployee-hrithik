from django.shortcuts import render,redirect
from django.http import JsonResponse, HttpResponse
import requests
import base64
import codecs
import openai
import json

right_ques =0 
no_of_ques=0
# Create your views here.
def guidance(request,skills):

# Set up the OpenAI API client
    openai.api_key = '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'


# this loop will let us ask questions continuously and behave like ChatGPT
    # Set up the model and prompt
    model_engine = "text-davinci-003"
    
    prompt =  f'Please provide me proper guidance related to skills-{skills}'

    # Generate a response
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # extracting useful part of response
    response = completion.choices[0].text
    data=response.split('\n')
    data = [i for i in data if i.strip()]
    
    # printing response
    return JsonResponse(data,safe=False)

 

def courses(request,skills):



    # Replace with your client ID and client secret key
    client_id = 'ZhRIoHAGl9fn31OhJicqXm5bdGwIZUNCqS2ciPqX'
    client_secret = 'tnMP0Mm0rAXWc44onSQv6h7Xf0QZyS192ts7uzyRGkPKfzfDbgrg3pCeFxjNPekCPQlLZY80wMIW2B3CBY8jDtKLmlJP3ySK7AKNizJOjpO6gufEdCPoZnFg1VsXdG6V'

    # Set up the authentication headers
    # Set up the authentication headers
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode('ascii')
    auth_b64_bytes = base64.b64encode(auth_bytes)
    auth_b64 = auth_b64_bytes.decode('ascii')
    auth_headers = {'Authorization': f'Basic {auth_b64}'}

    search_term = skills
    params = {
    'search': search_term,
    'page_size': 10,
    'page': 1,
    'language': 'en',
    'fields[course]': 'title,url,image_480x270'
    } # Category ID for "Web Development"
    response = requests.get('https://www.udemy.com/api-2.0/courses/', auth=(client_id, client_secret), headers=auth_headers, params=params)

    
    data = response.json()

    # Print the response content
    results = data['results']
    data=[]
    for course in response.json()['results']:
        data.append([course['title'],f'https://www.udemy.com{course["url"]}',course['image_480x270']])
   
    return JsonResponse(data,safe=False)


def assesment(request,id,skills):
    
        request.session['noqes'] = int(0)
        request.session['rightques'] = int(0)
        request.session['skills'] = skills
        request.session['id'] = id
        return redirect('quesAns')


def quesAns(request):
# Set up the OpenAI API client
    id=request.session['id'] 
    skills = request.session['skills'] 
    openai.api_key = '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'


# this loop will let us ask questions continuously and behave like ChatGPT
    # Set up the model and prompt
    model_engine = "text-davinci-003"
    
    prompt =  f"provide me json containing one MCQ question, also 4 options and answer. Question is based on skills- {skills}. Please don't provide questions like 'What is the output of the following code?' "

    # Generate a response
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    
    # extracting useful part of response
    response = completion.choices[0].text
    response = json.loads(response)
    response['id'] = id
    response['skills'] = skills

    # printing response
    return render(request,'assesment.html',response)

def submitnext(request):

    if request.method == 'POST':
    

        opt = request.POST.get('radio')
        ans = request.POST.get('ans')

       
        if ans == opt:
           
            request.session['rightques'] = request.session['rightques']+1
            print(request.session['rightques'])


        request.session['noqes'] = request.session['noqes']+1
        print(request.session['noqes'])
        if request.session['noqes'] == 10:
            
            return render(request,'result.html',{'right_ques':request.session['rightques']})
        
        return redirect('quesAns')


