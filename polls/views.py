from django.shortcuts import render, get_object_or_404, redirect
from .models import Poll, Response
from .forms import ResponseForm
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for rendering plots
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import io
import urllib, base64
import numpy as np

def poll_view(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    form = ResponseForm()
    if request.method == "POST":
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.poll = poll
            response.save()
            return redirect('poll_results', poll_id=poll.id)
    return render(request, 'poll.html', {'poll': poll, 'form': form})

def poll_results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    responses = Response.objects.filter(poll=poll)
    response_texts = [r.answer for r in responses]
    int_response_texts = [int(r.answer) for r in responses]
    float_response_texts = [float(r.answer) for r in responses]

    plt.figure(figsize=(10, 6),dpi=100)
    plt.hist(response_texts, bins=6, edgecolor='black',color='#660000')
    plt.title(f'Histogram: "{poll.question_text}"')
    plt.xlabel('Answers')
    plt.ylabel('Frequency')
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))


    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()

    image_base64 = base64.b64encode(image_png).decode('utf-8')
    image_uri = f"data:image/png;base64,{image_base64}"

    # summary statistics
    count = len(response_texts)
    try:
        mean = np.mean(float_response_texts)
        median = np.median(float_response_texts)
        mode = np.argmax(np.bincount(int_response_texts))
        std_dev = np.std(float_response_texts)
        variance = np.var(float_response_texts)
        interquartile = np.percentile(float_response_texts, 75) - np.percentile(float_response_texts, 25)
        range = max(float_response_texts) - min(float_response_texts)
        minimum = min(float_response_texts)
        maximum = max(float_response_texts)
    except:
        mean = None
        median = None
        mode = None
        std_dev = None
        variance = None
        interquartile = None
        range = None
        minimum = None
        maximum = None

    return render(request, 'results.html', {'poll': poll, 
                                            'image_uri': image_uri,
                                            'responses':int_response_texts,
                                            'count':count,
                                            'mean':mean,
                                            'median':median,
                                            'mode':mode,
                                            'std_dev':std_dev,
                                            'minimum':minimum,
                                            'maximum':maximum,
                                            'variance':variance,
                                            'interquartile':interquartile,
                                            'range':range
                                            })

def home(request):
    polls = Poll.objects.all()
    return render(request, 'index.html', {'polls': polls})