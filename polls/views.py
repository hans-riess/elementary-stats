import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for rendering to a file
import matplotlib.pyplot as plt
import io
import urllib, base64
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ResponseForm
from .models import Poll, Response

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

    # Prepare data for histogram
    responses = [r.answer for r in responses]

    # Create the histogram
    plt.figure(figsize=(10, 6))
    plt.hist(responses, bins=10, edgecolor='black')
    plt.title(f'Results for "{poll.question_text}"')
    plt.xlabel('Answers')
    plt.ylabel('Frequency')

    # Save the plot to a BytesIO object
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()  # Close the plot to free memory

    # Encode the image to base64 to render in HTML
    image_base64 = base64.b64encode(image_png).decode('utf-8')
    image_uri = f"data:image/png;base64,{image_base64}"

    return render(request, 'poll_results.html', {'poll': poll, 'image_uri': image_uri})