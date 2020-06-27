from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from urllib.parse import urlencode
from website.dictionary_functions import *
from website.forms import *

def home(request):

	form = WordSearchForm()

	return render(request, 'index.html', {'form': form})

def search(request):

	if 'word_id' in request.GET:

		url_word_id = request.GET['word_id']

		base_url = reverse('word details')

		query_string =  urlencode({'word_id': url_word_id})

		url = '{}?{}'.format(base_url, query_string)

		return redirect(url)

	else:

		url_word = request.GET['word']

		results = combine_words(text = url_word)

		if len(results) == 0:

			return HttpResponse('Nothing matches the search term. Try again :-)')

		elif len(results) == 1:

			one_result = results[0]

			base_url = reverse('word details')

			query_string =  urlencode({'word_id': one_result['id']})

			url = '{}?{}'.format(base_url, query_string)

			return redirect(url)

		else:

			word_choices = []

			for i, a in enumerate(results):

				word_id = a['id']

				word = a['full_word']

				choice = (word_id, word)

				word_choices.append(choice)

			form = WordChooseForm(word_choices)

			return render(request, 'results_form.html', {'form': form})

def details(request):

	url_word_id = request.GET['word_id']

	response = get_total(word_id = url_word_id)

	return render(request, 'results_details.html', {'word_details': response})









