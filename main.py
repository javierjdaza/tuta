import streamlit as st 
from streamlit_option_menu import option_menu
from data_info import dict_ligas
from utils import get_all_team_names,get_all_matches_by_team,all_matches_plot,h2h_plot
import pickle
# ------------------------
# PAGE CONFIGURATION
# ------------------------




_menu_items = {
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
st.set_page_config(page_title='Football Stats', page_icon = '📊', layout="wide", initial_sidebar_state="collapsed", menu_items=_menu_items)
# hide_watermarks()

# ------
# LOGO
# ------
# st.image('./img/svg_flipcase.png',width=250 )


# ------------------------
# NAV BAR
# ------------------------


st.markdown("<h1 style='text-align: center;'>Hola Tutu, que ma'?</h1>", unsafe_allow_html=True)

st.write('---')
menu_bar_selected = option_menu(None, ["All Matches", "H2H", 'Team Stats'], 
                                icons=['graph-up-arrow', 'people-fill', 'person'], 
                                menu_icon="cast", default_index=1, orientation="horizontal")
st.write('---')

a1,a2,a3 = st.columns((1,3,1))

if menu_bar_selected == 'All Matches':
    with a2:
        liga_choosed = st.selectbox("Selecciona La Liga",sorted([i.title() for i in dict_ligas.keys()]),index=10,placeholder="Select contact method...")
        liga_info_dict = pickle.load(open(f'./data/{liga_choosed.lower()}.pkl','rb'))
        all_teams_names = get_all_team_names(liga_info_dict)
        st.write('---')
        if liga_choosed: # si la liga fue escogida
            b1,b2 = st.columns(2)
            st.write('---')
            
            with b1:
                team_1_choosed = st.selectbox('Selecciona Equipo 1:',[i.title() for i in all_teams_names], key = 'equipo_1', index=None, placeholder = 'equipo...')
                if team_1_choosed:
                    equipo_1_all_matches_df = get_all_matches_by_team(team_1_choosed.lower(),data_list=liga_info_dict)
                    # st.dataframe(equipo_1_all_matches_df)
            with b2:
                team_2_choosed = st.selectbox('Selecciona Equipo 2:',[i.title() for i in all_teams_names], key = 'equipo_2', index=None, placeholder = 'equipo...')
                if team_2_choosed:
                    equipo_2_all_matches_df = get_all_matches_by_team(team_2_choosed.lower(),data_list=liga_info_dict)
                    # st.dataframe(equipo_2_all_matches_df)
            
            if team_1_choosed and team_2_choosed: # si el equipo ya fue escogido
                not_items_stats = ['equipo','fecha_partido','jornada','equipo_contrario','distancia_cubierta_(km)']
                stats_items = sorted([i.title().replace('_',' ') for i in equipo_2_all_matches_df.columns if i not in not_items_stats])
                stats_to_look = st.selectbox('Selecciona estadistico:',stats_items, key = 'stat', index=None, placeholder = 'Estadisticos...')
                st.write('---')
                # n_jornadas = st.slider('Numero Partidos', min_value = 1, max_value = equipo_1_all_matches_df['jornada'].max(),value = equipo_1_all_matches_df['jornada'].max())
                # n_jornadas = st.number_input('Insert a number',min_value = 1, max_value = equipo_1_all_matches_df['jornada'].max(),value = equipo_1_all_matches_df['jornada'].max(), step=4)
                
                
                if stats_to_look:
                    c1,c2,c3 = st.columns((1,3,1))
                    with c2:
                        # n_jornadas = st.multiselect(label = 'Numero Partidos',placeholder = ' ',options = [5,10, 'Todos'],default = 5,max_selections = 1)
                        # n_jornadas = st.radio("Numero Partidos",(5, 10, 'Todos'),horizontal=True,index=1, label_visibility='hidden')
                        n_jornadas = option_menu(None, ["5", "10", 'Todos'], 
                                    icons=['eye', 'eye', 'eye'], 
                                    menu_icon="cast", default_index=0, orientation="horizontal")
                    if len(equipo_1_all_matches_df) > 0 and len(equipo_2_all_matches_df) > 0:
                        if  n_jornadas:

                            if  n_jornadas != 'Todos':
                                equipo_1_all_matches_df_for_plot = equipo_1_all_matches_df.tail(int(n_jornadas))
                                equipo_2_all_matches_df_for_plot = equipo_2_all_matches_df.tail(int(n_jornadas))
                            else:
                                equipo_1_all_matches_df_for_plot = equipo_1_all_matches_df.copy()
                                equipo_2_all_matches_df_for_plot = equipo_2_all_matches_df.copy()
                            
                            all_matches_fig = all_matches_plot(estadistico_a_mirar = stats_to_look.lower().replace(' ','_'), equipo_1_df = equipo_1_all_matches_df_for_plot, 
                                                                equipo_2_df = equipo_2_all_matches_df_for_plot, equipo_1_name = team_1_choosed.lower(), equipo_2_name = team_2_choosed.lower())
                            st.write('---')
                            st.plotly_chart(all_matches_fig, use_container_width=True)
                            st.markdown("<p style='text-align: center; color:#414141; font-size:14px;'>**Linea punteada indica el promedio de la estadistica 🔍</p>", unsafe_allow_html=True)
                      
                      
h1,h2,h3 = st.columns((1,3,1))      
if menu_bar_selected == 'H2H':
    with h2:
        liga_choosed = st.selectbox("Selecciona La Liga",sorted([i.title() for i in dict_ligas.keys()]),index=10,placeholder="Select contact method...")
        liga_info_dict = pickle.load(open(f'./data/{liga_choosed.lower()}.pkl','rb'))
        all_teams_names = get_all_team_names(liga_info_dict)
        st.write('---')
        if liga_choosed: # si la liga fue escogida
            b1,b2 = st.columns(2)
            st.write('---')
            
            with b1:
                local_team_choosed = st.selectbox('Selecciona Equipo Local:',[i.title() for i in all_teams_names], key = 'equipo_1', index=None, placeholder = 'equipo...')
                if local_team_choosed:
                    local_team_all_matches_df = get_all_matches_by_team(local_team_choosed.lower(),data_list=liga_info_dict)
                    # st.dataframe(equipo_1_all_matches_df)
            with b2:
                away_team_choosed = st.selectbox('Selecciona Equipo Visitante:',[i.title() for i in all_teams_names], key = 'equipo_2', index=None, placeholder = 'equipo...')
                if away_team_choosed:
                    away_team_all_matches_df = get_all_matches_by_team(away_team_choosed.lower(),data_list=liga_info_dict)
                    # st.dataframe(equipo_2_all_matches_df)
            if (local_team_choosed == away_team_choosed) and local_team_choosed and away_team_choosed :
                st.error('Los equipos escogidos son los mismos!')
            elif local_team_choosed and away_team_choosed:
                if len(local_team_all_matches_df) != 0 and len(away_team_all_matches_df) != 0:
                    equipo_local_filtred_df = local_team_all_matches_df[
                                                                        (local_team_all_matches_df['equipo'].str.startswith(local_team_choosed.lower())) & 
                                                                        (local_team_all_matches_df['equipo'].str.endswith('L')) & 
                                                                        (local_team_all_matches_df['equipo_contrario']).str.startswith(away_team_choosed.lower())
                                                                        ]
                    
                    equipo_visitante_filtred_df = away_team_all_matches_df[
                                                                        (away_team_all_matches_df['equipo'].str.startswith(away_team_choosed.lower())) & 
                                                                        (away_team_all_matches_df['equipo'].str.endswith('V')) & 
                                                                        (away_team_all_matches_df['equipo_contrario']).str.startswith(local_team_choosed.lower())
                                                                        ]
                    if len(equipo_local_filtred_df) == 0:
                        st.warning(f'El {local_team_choosed} en condicion de local no se ha enfrentado con el {away_team_choosed}')
                    # if len(equipo_visitante_filtred_df) == 0:
                    #     st.warning(f'El {away_team_choosed} en condicion de local no se ha enfrentado con el {local_team_choosed}')
                    else:
                        not_items_stats = ['equipo','fecha_partido','jornada','equipo_contrario','distancia_cubierta_(km)']
                        stats_items = sorted([i.title().replace('_',' ') for i in equipo_visitante_filtred_df.columns if i not in not_items_stats])
                        stats_to_look = st.selectbox('Selecciona estadistico:',stats_items, key = 'stat', index=None, placeholder = 'Estadisticos...')
                        st.write('---')
                        # st.dataframe(equipo_local_filtred_df)
                        # st.dataframe(equipo_visitante_filtred_df)
                        if stats_to_look:
                            h2h_fig = h2h_plot(local_team_choosed, away_team_choosed, equipo_local_filtred_df,equipo_visitante_filtred_df, stats_to_look.lower().replace(' ','_'))
                            st.plotly_chart(h2h_fig, use_container_width=True)
