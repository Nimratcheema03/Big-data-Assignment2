# pages/views.py
from django.shortcuts import render, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.views.generic import TemplateView
import pickle
import statsmodels.api as sm
import sklearn # You must perform a pip install.
import pandas as pd
import plotly.graph_objects as go

def homePageView(request):
    return render(request, 'home.html')


def homePost(request):
    # Use request object to extract choice.

    Rank = -999
    NA_Sales = -999
    EU_Sales = -999
    JP_Sales = -999
    Other_Sales = -999
    try:
        # Extract value from request object by control name.
        Rank1 = request.POST['Rank']
        NA_Sales1 = request.POST['NA_Sales']
        EU_Sales1 = request.POST['EU_Sales']
        JP_Sales1 = request.POST['JP_Sales']
        Other_Sales1 = request.POST['Other_Sales']

        Rank = int(Rank1)
        NA_Sales = NA_Sales1
        EU_Sales  = EU_Sales1
        JP_Sales = JP_Sales1
        Other_Sales =Other_Sales1
    except:
        return render(request, 'home.html', {
            'errorMessage': 'The data submitted is invalid. Please try again.'})
    else:
        return HttpResponseRedirect(reverse('results', kwargs={'Rank': Rank, 'NA_Sales': NA_Sales,'EU_Sales': EU_Sales, 'JP_Sales': JP_Sales, 'Other_Sales': Other_Sales}, ))


def results(request, Rank, NA_Sales, EU_Sales, JP_Sales, Other_Sales):
    print("*** Inside reults()")
    # load saved model
    with open('model_pkl', 'rb') as f:
        loadedModel = pickle.load(f)

    # Create a single prediction.
    singleSampleDf = pd.DataFrame(columns=['Rank','NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales'])

    Rank = int(Rank)
    NA_Sales = float(NA_Sales)
    EU_Sales = float(EU_Sales)
    JP_Sales = float(JP_Sales)
    Other_Sales = float(Other_Sales)
    singleSampleDf = singleSampleDf.append({'Rank': Rank, 'NA_Sales': NA_Sales,'EU_Sales': EU_Sales, 'JP_Sales': JP_Sales, 'Other_Sales': Other_Sales},
                                           ignore_index=True)
    singlePrediction = loadedModel.predict(singleSampleDf)[0]
    singlePrediction = round(singlePrediction, 1)
    # Create the bar plot
    fig = go.Figure()
    fig.add_trace(go.Bar(x=['NA', 'EU', 'JP', 'Other'], y=[NA_Sales, EU_Sales, JP_Sales, Other_Sales], name='Sales'))
    fig.add_trace(go.Bar(x=['Prediction'], y=[singlePrediction], name='Prediction'))

    # Update the layout
    fig.update_layout(title='Sales and Prediction', xaxis_title='Region', yaxis_title='Sales')

    # Pass the plot to the template context
    plot_div = fig.to_html(full_html=False)

    context = {
        'Rank': Rank,
        'NA_Sales': NA_Sales,
        'EU_Sales': EU_Sales,
        'JP_Sales': JP_Sales,
        'Other_Sales': Other_Sales,
        'prediction': singlePrediction,
        'plot_div': plot_div,
    }

    return render(request, 'results.html', context)
