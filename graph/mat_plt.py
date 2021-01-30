# Personal Build
from graph.data_filters import *

# Kernel Graphics
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
import matplotlib.patches as mpatches

# Data Management
import pandas as pd

def plot_rank_barh(x, y, rank):
    plt.figure(figsize=(8,8))
    plt.barh(y=y, width=x)

    for i, v in enumerate(x):
        plt.text(v+1, i, str(v), fontweight='bold')

    xlabel = f'Times shown at #{rank} position' 
    plt.xlabel(xlabel)

    header = f'Times an album hit the #{rank} position' 
    plt.title(label=header)

    plt.show()


df = pd.read_parquet('DB/Kaggle/parquet/mx-music.parquet')

def barh_and_scatters(pivot_column, df_info=df, top_rank=5, extracted_info_name='Albums', n_plots=1):

    top = top_rank + 1 
    info = pivot_column
    df = df_info

    for rank in range(1, top):
        
        #Extract Info
        
        extracted_df = rank_info(df, rank, info, extracted_info_name)
        albums = extracted_df[extracted_info_name].to_list()
        info_count = extracted_df['Counts'].to_list()

        #Plot
        plot_rank_barh(info_count, albums, rank)

        # scatter
        rank_df = df[df['Rank'] == rank]
        x = rank_df['Stars']
        y = rank_df['Reviews']
        
        groups = rank_df.groupby(info)        
        markers = ['o', 'x', 'v', 'p']
        fig, ax = plt.subplots()
        m = 0
        p = 0
        

        for name, group in groups:
            if (m % 10 == 0) and (m > 0):
                p += 1
            if p == 4: p = 0

            ax.plot(group.Stars , group.Reviews, marker=markers[p], linestyle='', label=name)
            m += 1

        plt.legend(loc='best', bbox_to_anchor=(1,1), ncol=2)

def barh_plus_scatter(pivot_column, df_info=df, top_rank=5, extracted_info_name='Albums', n_plots=1, w_fig=8, h_fig=8):
    top = top_rank + 1 
    info = pivot_column
    df = df_info

    for rank in range(1, top):
        
        #Extract Info
        
        extracted_df = rank_info(df, rank, info, extracted_info_name)
        albums = extracted_df[extracted_info_name].to_list()
        info_count = extracted_df['Counts'].to_list()

        #Plot
        fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2,figsize=(w_fig, h_fig))
        title = f' Top #{rank} Info' 
        fig.suptitle(title)
        # plt.figure(figsize=(w_fig,h_fig))

        ax1.barh(y=albums, width=info_count)

        for i, v in enumerate(info_count):
            ax1.text(v+1, i, str(v))

        xlabel = f'Times shown at #{rank} position' 
        ax1.set_xlabel(xlabel)

        bar_header = f'Times an {extracted_info_name} hit the #{rank} position' 
        ax1.set_title(label=bar_header)

        # scatter
        rank_df = df[df['Rank'] == rank]
        x = rank_df['Stars']
        y = rank_df['Reviews']
        
        ax2.set_xlabel('Stars')
        ax2.set_title(f'Reviews vs Stars per {extracted_info_name} at the #{rank} position')
        ax2.set_ylabel('Reviews')
        groups = rank_df.groupby(info)        
        markers = ['o', 'x', 'v', 'p']
        
        m = 0
        p = 0
        for name, group in groups:
            if (m % 10 == 0) and (m > 0):
                p += 1
            if p == 4: p = 0
            ax2.plot(group.Stars , group.Reviews, marker=markers[p], linestyle='', label=name)
            
            m += 1

        ax2.legend(loc='best', bbox_to_anchor=(1,1), ncol=2)
        plt.show()
        