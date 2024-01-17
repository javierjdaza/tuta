
import pandas as pd
import plotly.graph_objects as go



def get_all_team_names(data_list):
    listado_equipos = []
    for k,jornada in data_list.items():
        for partido in jornada:
            for k,v in partido.items():
                listado_equipos.append(k.split('_')[0])
                
    return sorted(list(set(listado_equipos)))
def gana_pierde_empate(x):
    if x >0:
        return 'gano'
    elif x<0:
        return 'perdio'
    else:
        return 'empato'
# get all matches for team given
def get_all_matches_by_team(busqueda, data_list):
    estadisticas_buscadas = []
    for k,jornada in data_list.items():
        for partido in jornada:
            for equipo,estadisticas in partido.items():
                if busqueda in equipo:
                    estadisticas_new = {**{'equipo': equipo},**estadisticas}
                    estadisticas_buscadas.append(estadisticas_new)
    stats_df = pd.DataFrame(estadisticas_buscadas)
    stats_df['fecha_partido'] = pd.to_datetime(stats_df['fecha_partido'],dayfirst=True)
    stats_df.sort_values(by = ['fecha_partido'], inplace=True)
    stats_df.reset_index(inplace=True, drop=True)
    stats_df.fillna(0,inplace=True)
    try:
        stats_df.rename(columns = {'vs':'equipo_contrario','goles_vs':'goles_recibidos','goles':'goles_anotados'}, inplace = True)
    except:
        pass
    try:
        stats_df['goles_esperados'] = stats_df['goles_esperados'].apply(lambda x: float(x))
    except:
        pass
    columns_to_int = ['remates_a_puerta', 'remates_fuera', 'remates_rechazados',
    'tiros_libres', 'corneres', 'fueras_de_juego', 'saques_de_banda',
    'paradas', 'faltas', 'tarjetas_amarillas', 'ataques',
    'ataques_peligrosos', 'goles_anotados', 'tarjetas_rojas','remates','jornada','goles_recibidos','goles','goles_vs']
    for i in columns_to_int:
        try:
            stats_df[i] = stats_df[i].apply(lambda x: int(x))
        except:
            pass
        
    try:
        stats_df['posesion_de_balon'] = stats_df['posesion_de_balon'].apply(lambda x: int(x.replace('%','')))
    except:
        pass
    
    stats_df['resultado'] = stats_df['goles_anotados'] - stats_df['goles_recibidos']
    stats_df['resultado'] = stats_df['resultado'].apply(lambda x: gana_pierde_empate(x))


    
    return stats_df



def all_matches_plot(estadistico_a_mirar:str, equipo_1_df, equipo_2_df, equipo_1_name:str, equipo_2_name:str):

    # --- Local ---
    y_l = equipo_1_df[estadistico_a_mirar] # eje x, equipo 1
    x_l = equipo_1_df['jornada'] # eje y, equipo 1
    # --- Visitante ---
    y_v = equipo_2_df[estadistico_a_mirar] # eje x, equipo 2
    x_v = equipo_2_df['jornada'] # eje y, equipo 2

    fig = go.Figure(data=[
        go.Bar(name=equipo_1_name.title(), x=x_l, y=y_l,marker_color = ['#9AE66E'] * len(x_l)),
        go.Bar(name=equipo_2_name.title(), x=x_v, y=y_v,marker_color = ['#FF6868'] * len(x_v)),
        
    ])
    # Change the bar mode
    fig.add_hline(y=0,line_width=1,line_color="#FFFFFF",opacity = 0.8)

    fig.add_hline(y=y_l.mean(),line_width=1.5, layer='below',line_color="#9AE66E",opacity=0.8,annotation_text=f"    ({round(y_l.mean(),2)})", annotation_position="right", line_dash="dot")
    fig.add_hline(y=y_v.mean(),line_width=1.5, layer='below', line_color="#FF6868",opacity=1,annotation_text=f"    ({round(y_v.mean(),2)})", annotation_position="right", line_dash="dot")
    fig.update_layout(barmode='group')

    fig.update_layout(
        title=dict(text=f'<b>{equipo_1_name.title()} vs {equipo_2_name.title()}</b><br><sup><i>{estadistico_a_mirar.title()}</i><sup>', font=dict(size=25,color="#FFFFFF"), x = 0.5, xanchor = 'center'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor = 'rgba(0,0,0,0)',
        xaxis_tickfont_size=13,
        yaxis=dict(
            title=estadistico_a_mirar.title(),
            titlefont_size=14,
            tickfont_size=12,
        ),
        xaxis=dict(
            title='Jornada',
            titlefont_size=14,
            tickfont_size=12,
            tickmode = 'array',
            tickvals = equipo_2_df['jornada'],
            # ticktext = equipo_1_df['jornada'],
        ),
        legend=dict(
            yanchor="top",
            y=-0.2,
            xanchor="left",
            x=0,
            orientation="h"
        ),
        margin=dict(r=50),
        modebar_remove=['zoom', 'pan', 'select', 'zoomIn', 'zoomOut', 'autoScale', 'lasso2d'],
        barmode='group',
        bargap=0.3, # gap between bars of adjacent location coordinates.
        bargroupgap=0, # gap between bars of the same location coordinate.

    )
    fig.update_xaxes(
        mirror=True,
        # ticks='outside',
        showline=True,
        gridcolor='lightgrey'
    )
    fig.update_yaxes(
        mirror=True,
        # ticks='outside',
        showline=True,
        gridcolor='lightgrey'
    )
    # fig.show()
    return fig

def h2h_plot(equipo_local, equipo_visitante, equipo_local_df,equipo_visitante_df, estadistico_a_mirar):
    # --- Local ---
    y_l = equipo_local_df[estadistico_a_mirar]
    x_l = [i.split('_')[0].title() for i in equipo_local_df['equipo']]
    # --- Visitante ---
    y_v = equipo_visitante_df[estadistico_a_mirar]
    x_v = [i.split('_')[0].title() for i in equipo_visitante_df['equipo']]

    fig = go.Figure(data=[
        go.Bar(name=equipo_local.title(), x=x_l, y=y_l,marker_color = ['#9AE66E'] * len(x_l)),
        go.Bar(name=equipo_visitante.title(), x=x_v, y=y_v,marker_color = ['#FF6868'] * len(x_l)),
        
    ])
    # Change the bar mode
    fig.add_hline(y=0,line_width=1,line_color="#414141",opacity = 0.8)

    # fig.add_hline(y=y_l.mean(),line_width=1.5, layer='below',line_color="#9AE66E",opacity=0.8,annotation_text=f"   ({round(y_l.mean(),2)}) mean", annotation_position="right", line_dash="dot")
    # fig.add_hline(y=y_v.mean(),line_width=1.5, layer='below', line_color="#FF6868",opacity=0.8,annotation_text=f"   ({round(y_v.mean(),2)}) mean", annotation_position="right", line_dash="dot")
    fig.update_layout(barmode='group')

    fig.update_layout(
        title=dict(text=f'<b>{equipo_local.title()} vs {equipo_visitante.title()}</b><br><sup><i>{estadistico_a_mirar.title()}</i><sup>', font=dict(size=25,color="#FFFFFF"), x = 0.5, xanchor = 'center'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor = 'rgba(0,0,0,0)',
        xaxis_tickfont_size=13,
        yaxis=dict(
            title=estadistico_a_mirar.title(),
            titlefont_size=14,
            tickfont_size=12,
        ),
        xaxis=dict(
            title='Equipo',
            titlefont_size=14,
            tickfont_size=12,
            tickmode = 'array',
            # tickvals =  ['sdsdsd','sdsds'],
            # ticktext = ['sdsdsd','sdsds'],
        ),
        modebar_remove=['zoom', 'pan', 'select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale','lasso2d'],
        barmode='group',
        bargap=0.3, # gap between bars of adjacent location coordinates.
        bargroupgap=0, # gap between bars of the same location coordinate.
        showlegend = False,
        margin=dict(r=20),
    )
    fig.update_xaxes(
        mirror=True,
        # ticks='outside',
        showline=True,
        gridcolor='lightgrey'
    )
    fig.update_yaxes(
        mirror=True,
        # ticks='outside',
        showline=True,
        gridcolor='lightgrey'
    )

    # fig.show()
    return fig