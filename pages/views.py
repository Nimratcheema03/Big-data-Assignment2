# pages/views.py
from django.shortcuts import render, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.views.generic import TemplateView
import pickle
import statsmodels.api as sm
import sklearn  # You must perform a pip install.
import pandas as pd
import plotly.graph_objects as go


def homePageView(request):
    return render(request, 'home.html')


def homePost(request):
    # Use request object to extract choice.

    concave_points_worst = -999
    perimeter_worst = -999
    concave_points_mean = -999
    radius_worst = -999
    perimeter_mean = -999
    area_worst = -999
    try:
        # Extract value from request object by control name.
        concave_points_worst1 = request.POST['concave_points_worst']
        perimeter_worst1 = request.POST['perimeter_worst']
        concave_points_mean1 = request.POST['concave_points_mean']
        radius_worst1 = request.POST['radius_worst']
        perimeter_mean1 = request.POST['perimeter_mean']
        area_worst1 = request.POST['area_worst']

        concave_points_worst = float(concave_points_worst1)
        perimeter_worst = float(perimeter_worst1)
        concave_points_mean = float(concave_points_mean1)
        radius_worst = float(radius_worst1)
        perimeter_mean = float(perimeter_mean1)
        area_worst = float(area_worst1)
    except:
        return render(request, 'home.html', {
            'errorMessage': 'The data submitted is invalid. Please try again.'})
    else:
        return HttpResponseRedirect(reverse('results', kwargs={'concave_points_worst': concave_points_worst,
                                                               'perimeter_worst': perimeter_worst,
                                                               'concave_points_mean': concave_points_mean,
                                                               'radius_worst': radius_worst,
                                                               'perimeter_mean': perimeter_mean,
                                                               'area_worst': area_worst}, ))


def results(request, concave_points_worst, perimeter_worst, concave_points_mean, radius_worst, perimeter_mean,
            area_worst):
    # load saved model and scaler
    with open('logreg.pkl', 'rb') as f:
        loadedModel = pickle.load(f)
    with open('scaler.pkl', 'rb') as s:
        scaler = pickle.load(s)

    # create a single prediction
    singleSampleDf = pd.DataFrame(
        columns=['concave_points_worst', 'perimeter_worst', 'concave_points_mean', 'radius_worst', 'perimeter_mean',
                 'area_worst'])

    concave_points_worst = float(concave_points_worst)
    perimeter_worst = float(perimeter_worst)
    concave_points_mean = float(concave_points_mean)
    radius_worst = float(radius_worst)
    perimeter_mean = float(perimeter_mean)
    area_worst = float(area_worst)
    singleSampleDf = singleSampleDf.append(
        {'concave_points_worst': concave_points_worst, 'perimeter_worst': perimeter_worst,
         'concave_points_mean': concave_points_mean, 'radius_worst': radius_worst, 'perimeter_mean': perimeter_mean,
         'area_worst': area_worst},
        ignore_index=True)
    scaled = scaler.transform(singleSampleDf)
    singlePrediction = loadedModel.predict(scaled)
    cancer = " "
    recommendations = []
    # set bar colors based on prediction
    if singlePrediction == 0:
        cancer = "Benign"
        colors = ['green', 'red']
        recommendations.append("Keep up with regular screenings to detect any potential issues early on.")
        recommendations.append("Eat a balanced diet and maintain a healthy weight.")
        recommendations.append("Exercise regularly to maintain overall health and wellbeing.")
    else:
        cancer = "Malignant"
        colors = ['red', 'green']
        recommendations.append("Consult with a specialist to determine the best course of treatment.")
        recommendations.append(
            "Consider joining a support group to connect with others going through a similar experience.")
        recommendations.append("Prioritize self-care and seek out resources for managing stress.")

    # create the bar plot
    fig = go.Figure(go.Bar(
        x=[1, 0],
        y=['Severity Level'],
        orientation='h',
        marker=dict(
            color=colors,
        ),
    ))

    # update the layout
    fig.update_layout(title='Cancer Severity', xaxis_title='Probability', yaxis_title='', showlegend=False)

    # pass the plot to the template context
    plot_div = fig.to_html(full_html=False)

    context = {
        'concave_points_worst': concave_points_worst,
        'perimeter_worst': perimeter_worst,
        'concave_points_mean': concave_points_mean,
        'radius_worst': radius_worst,
        'perimeter_mean': perimeter_mean,
        'area_worst': area_worst,
        'prediction': cancer,
        'recommendations': recommendations,
        'plot_div': plot_div,
    }
    return render(request, 'results.html', context)


