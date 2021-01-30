# Personal Build
from graph.data_filters import *

# Kernel Graphics
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

# Data Management
import pandas as pd

main_colors = px.colors.qualitative.Bold
df = pd.read_parquet('DB/Kaggle/parquet/mx-music.parquet')
# extracted_df = rank_info(df, 1, artist, 'Artist/Band')
# labels = extracted_df['Artist/Band'].to_list()
# labels_count = extracted_df['Counts'].to_list()
# labels = reverse(labels)
album = 'Product Names'
artist = 'Authors/Company'

def plotly_dashboard(pivot_column, rank=1, df_info=df, top_rank=None, extracted_info_name='Albums'):    
    info = pivot_column
    df = df_info
    main_colors = px.colors.qualitative.Bold
    
    if top_rank:
        top = top_rank + 1 
        for rank in range(rank, top):
            plotly_figures(info, df, main_colors, rank, extracted_info_name)
    
    else:
        plotly_figures(info, df, main_colors, rank, extracted_info_name)

def plotly_figures(info, df, main_colors, rank, extracted_info_name):
    extracted_df = rank_info(df, rank, info, extracted_info_name)
    labels = extracted_df[extracted_info_name].to_list()
    labels_count = extracted_df['Counts'].to_list()
    row_1_barh_and_lines(rank, extracted_df, info, extracted_info_name, labels, labels_count, original_df=df, line_colors=main_colors)

    #FIGURE 2
    labels = reverse(labels)
    row_2_rank_boxes(rank, info, extracted_info_name, labels, original_df=df, box_colors=main_colors)

    #FIGURE 3
    #Labels are reversed in order to match with the other graphs
    row_3_boxes_and_scatter(rank, info, labels, original_df=df, scatter_colors=main_colors)

def row_1_barh_and_lines(rank, extracted_df, info, extracted_info_name, labels, labels_count, line_colors, original_df=df):
    df = original_df
    bar_header = f'Times an album hit the top #{rank}'
    line_header = f'{extracted_info_name} Rank History'
    
    
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'bar'}, {'type': 'scatter'}]],
        subplot_titles=(bar_header, line_header)
        )

    #Horizontal Bars
    fig.add_trace(
        go.Bar(
            x = labels_count, y = labels, orientation = 'h',
            showlegend = False,
            text = labels,
                hovertemplate=
                "<b>%{text}</b><br><br>" +
                "Times: %{x}<br>" 
            ), row = 1, col = 1)
    fig.update_traces(marker_color='#F58518')
    fig.update_yaxes(title_text=extracted_info_name, row=1, col=1)
    # fig.update_xaxes(title_text=f'Times hited the top#{rank}', row=1, col=1)
    

    #lines
    labels = reverse(labels)
    color = 0
    for label in labels:
        best_seller = df[df[info] == label]
        fig.add_trace(
            go.Scatter(
                x = best_seller.time, y = best_seller.Rank, mode = 'lines', name = label, line=dict(color = line_colors[color]),
                text = best_seller[info],
                hovertemplate=
                "<b>%{text}</b><br><br>" +
                "Time: %{x}<br>" +
                "Rank Position: #%{y:,0f}<br>"
                ), row=1, col=2)
        if color < (len(line_colors)-1):
            color += 1
        else:
            color = 0
    # fig.update_layout(yaxis=dict(autorange = "reversed"), row=1, col=2)
    fig.update_yaxes(title_text='Rank Position', range=[1,50], row=1, col=2, autorange="reversed")
    fig.update_xaxes(title_text='Date' , row=1, col=2)


    fig.update_layout(
        title = {
            'text' : f"Amazon Music's sells at web page. Top #{rank} Info",
            'x' : 0.5,
            'xanchor' : 'center',
            'yanchor' : 'top',
            'y' : 0.9
        },
        title_font_size = 30,
        margin = dict(r=30, t=100, b=0, l=10),
        height = 400,
    )
    
    fig.show()

def row_2_rank_boxes(rank, info,  extracted_info_name, labels, box_colors, original_df=df):
    df = original_df
    ranking_box_header = f'Ranking distribution of the {extracted_info_name} at Top #{rank}:'  

    fig2 = make_subplots(
        rows=1, cols=1,
        specs=[[{'type': 'Box'}]]
        )
    color = 0
    for label in labels:
        info_df = df[df[info] == label]
        fig2.add_trace(
                go.Box(
                    y = info_df.Rank, showlegend = False,
                    name = label,
                    marker_color = box_colors[color]
                ))
        if color < (len(box_colors)-1):
            color += 1
        else:
            color = 0

    fig2.update_layout(
        margin=dict(r=10, t=40, b=50, l=10),
        height=300,
        title_text = ranking_box_header
    )
    fig2.update_yaxes(title_text='Rank Position', range=[1,50], autorange="reversed", row=1, col=1)
    fig2.show()

def row_3_boxes_and_scatter(rank, info, labels, scatter_colors, original_df=df):
    df = original_df
    box_header = f'Stats of of the #{rank} position'
    scatter_header = f'Reviews vs Stars of the #{rank} position'

    fig3 = make_subplots(
        rows=1, cols=5,
        column_widths=[0.19, 0.19, 0.19, 0.005, 0.425],
        specs=[[{'type': 'box'}, {'type': 'box'}, {'type': 'box'}, None, {'type': 'scatter'}]],
        subplot_titles=(None, box_header, None, scatter_header, None)
    )
    
    #BOXES INFO
    top_5 = df[(df['Rank'] >= 1) & (df['Rank']<=5)]
    rank_df = df[df['Rank'] == rank]
    box_info = ['Stars', 'Reviews', 'Price_std_or_min']
    colors = ['#FECB52', 'gold', 'crimson', 'red','green','lightseagreen']

    #Box
    b = 1
    c = 0
    for i in box_info:
        fig3.add_trace(
            go.Box(
                y = top_5[i], showlegend = False,
                name = f'Tops 1-5',
                marker_color = colors[c],
            ), row = 1, col = b)
        
        c += 1

        fig3.add_trace(
            go.Box(
                y = rank_df[i], showlegend = False,
                name = f'Top {rank}',
                marker_color = colors[c],
            ),
            row = 1, col = b)
        if i == 'Price_std_or_min':
            i = 'Price'
        fig3.update_xaxes(title_text=i, row=1, col=b)
        b += 1
        c += 1 

    #Scatter
    groups = rank_df.groupby(info)
    color = 0 
    for label in labels:
        best_seller = df[df[info] == label]
        fig3.add_trace(
            go.Scatter(
                x = best_seller.Stars, y = best_seller.Reviews, mode = 'markers', name = label, marker=dict(color = scatter_colors[color]),
                text = best_seller[artist],
                hovertemplate=
                "<b>%{text}</b><br><br>" +
                "Stars: %{x}<br>" +
                "Reviews: %{y:,0f}<br>"
                ), row = 1, col = 5)
        if color < (len(scatter_colors)-1):
            color += 1
        else:
            color = 0

    fig3.update_yaxes(title_text="Reviews", row=1, col=5)
    fig3.update_xaxes(title_text="Stars",range=[0,5], row=1, col=5)
    fig3.update_layout(
        margin=dict(r=10, t=40, b=50, l=10),
        height=300,
    )

    fig3.show()
