from django.shortcuts import render, get_object_or_404, redirect
from .models import Poll, Response, Histogram
from .forms import ResponseForm
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for rendering plots
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import io
import urllib, base64

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

    plt.figure(figsize=(10, 6),dpi=100)
    plt.hist(response_texts, bins=6, edgecolor='black',color='#660000')
    plt.title(f'Histogram: "{poll.question_text}"')
    plt.xlabel('Answers')
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10])
    plt.ylabel('Frequency')
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()

    image_base64 = base64.b64encode(image_png).decode('utf-8')
    image_uri = f"data:image/png;base64,{image_base64}"

    return render(request, 'results.html', {'poll': poll, 'image_uri': image_uri})