import json
import pandas as pd
from dash import dcc, html, ctx, MATCH, ALL
from dash.dependencies import Input, Output, State

import plotly.express as px
from plotly.offline import plot
import chart_studio.plotly as py
import chart_studio
chart_studio.tools.set_config_file(world_readable=False, sharing='private')
import plotly.graph_objects as go
from django_plotly_dash import DjangoDash

from django.contrib.auth.models import User
from defs.models import Shiftplan, Jobtype, Job
from .models import UserJobRating

RATES = range(1, 6)
styles = {
    'app':{
        'height': '100%',
        'width': '100%',
        'overflowX': 'show',
        'overflowY': 'show'
        }
    }
app = DjangoDash('thechart', add_bootstrap_links=True)
app.layout = html.Div([
    dcc.Input(id='df_inp'),
    dcc.Store(id="cache", data=[]),
    html.H1("Preferences", style={"text-align": "center"}),
    html.Div([
            dcc.Markdown("""
                **Click Data**

                Click on points in the graph.
            """),
            html.Pre(id='click-data', children=[]),
    ], className='three columns'),
    html.Br(),
    dcc.Graph(id="chart_plot")
], style=styles['app'])


@app.callback(
    Output('chart_plot', 'figure'),
    [Input('df_inp', 'value')])
def generate_graph(df_inp, session_state=None, *args, **kwargs):
    if df_inp is None:
        django_dash = kwargs["request"].session.get("django_dash")
        df = pd.read_json(django_dash.get('df'))
        df['begin'] = pd.to_datetime(df['begin'], format="%Y-%m-%d %H:%M:%S")
        df['end'] = pd.to_datetime(df['end'], format="%Y-%m-%d %H:%M:%S")
        # print("df_inp none")
    else:
        df = pd.read_json(df_inp)
        df['begin'] = pd.to_datetime(df['begin'], format="%Y-%m-%d %H:%M:%S")
        df['end'] = pd.to_datetime(df['end'], format="%Y-%m-%d %H:%M:%S")
    # print("generae_graph", df)
    dff = df.copy()
    fig = chart_plot(dff)
    fig.update_layout(clickmode='event+select')
    # fig.show()
    return fig

@app.callback(
    Output('click-data', 'children'),
    Input('chart_plot', 'clickData'))
def display_click_data(clickData):
    if clickData:
        print(clickData)
        pref_inp = html.Div([
            html.P('Rate job: {name}'.format(name=clickData["points"][0]["label"])),
            dcc.Dropdown(
                id={
                    'type': 'pref_inp',
                    'index': clickData["points"][0]["pointIndex"]
                },
                options=[
                    {'label': i, 'value': i} for i in RATES
                ],
                multi=False,
                clearable=False,
                style={'width': '49%', "position": "relative"},
                maxHeight=500,
                className="dropdown_row"
            ),
            html.Button(
                id={
                    'type': 'pref_inp_btn',
                    'index': clickData["points"][0]["pointIndex"]
                },
                children="Submit",
                style={"position": "relative", "display": "inline-block"}
                )

        ], style={'display': 'inline', "height": "80%"})
        # return json.dumps(clickData, indent=2)
        return pref_inp


@app.callback(
    Output('df_inp', 'value'),
    Input({'type': 'pref_inp_btn', 'index': ALL}, 'n_clicks'),
    State({'type': 'pref_inp', 'index': ALL}, 'value'))
def alter_data(pref_inp_btn, pref_inp, *args, **kwargs):
    django_dash = kwargs["request"].session.get("django_dash")
    if pref_inp != [None] and kwargs['callback_context'].triggered != []:
        pref = int(pref_inp[0])
        current_user = kwargs['user']
        context_trigger = kwargs['callback_context'].triggered[0]
        trigg_id = json.loads(context_trigger['prop_id'].split('.')[0])['index']
        df = generate_df(current_user)
        django_index = df.loc[df.index == int(trigg_id), 'db_idx']
        job_selected = Job.objects.get(id=int(django_index))
        # job_selected = Job.objects.all()[int(trigg_id)]
        
        # user_job_rating = UserJobRating.objects.filter(user=current_user).values()
        # print(user_job_rating)
        try:
            ujr = UserJobRating.objects.get(job=job_selected, user=current_user)
        except UserJobRating.DoesNotExist:
            ujr = UserJobRating(job=job_selected, user=current_user, rating=int(pref))
            # print("New UserJobRating instance.")
        setattr(ujr, "rating", pref)
        # print("ujr ", ujr)
        ujr.save()
        # df.loc[df["db_idx"] == int(trigg_id), 'rating'] = pref
        df = generate_df(current_user)
        df_json = df.to_json()
        django_dash['df'] = df_json
        print("exiting alter_data, df: ", df)
        return df_json
    

def chart_plot(df):
    print(df)
    tl = px.timeline(
        df, x_start="begin", x_end="end", y="name", color="rating", opacity=0.5)
    # fig = px.bar(df, x='during', y='name', color='name')
    tl.update_yaxes(autorange="reversed")
    # fig['layout']['xaxis'].update({'type': None})
    # fig.update_xaxes(type='category')
    # gantt_plot = plot(fig)#, output_type="div")
    # tl.update_traces()
    # print(tl.data)
    return tl
# @app.callback(
#     Output(component_id="chart_plot", component_property="figure"),
#     [Input(component_id="job_pref_input", component_property="value")]
# )
# def update_graph(pref_selected, session_state=None, **kwargs):
#     print(pref_selected)
#     print(type(pref_selected))
#     if session_state is None:
#         raise NotImplementedError("Cannot handle a missing session state")
#     df = session_state.get('df')
#     print(df)
#     dff = df.copy()
#     dff.loc['rating'] = pref_selected

    
#     # fig.update_traces(marker_size=20)
#     return fig

def generate_df(user):
    user_ratings = UserJobRating.objects.filter(user=user)
    l = []
    for ur in user_ratings:
        d = ur.as_dict()
        job = ur.job.as_dict()
        job["db_idx"] = ur.job.id
        jobtype = ur.job.jobtype.as_dict()
        d.update(job)
        d.update(jobtype)
        l.append(d)
    df = pd.DataFrame(l)
    df['begin'] = pd.to_datetime(df['begin_date'].astype(str) + ' ' + df['begin_time'].astype(str))
    df['end'] = pd.to_datetime(df['end_date'].astype(str) + ' ' + df['end_time'].astype(str))
    return df
