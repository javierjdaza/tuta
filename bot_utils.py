
import unicodedata
from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm
import time



# BOT METHODS
def skip_popups_and_show_more_button(driver):
    try:
        accept_cookies_button_selector = driver.find_element(By.ID, 'onetrust-accept-btn-handler') # accept cookies button selector
        accept_cookies_button_selector.click()
        time.sleep(1.5)
    except:
        pass
    try:
        click_annoying_popu_about_pin_matches_selector = driver.find_element(By.CLASS_NAME,'close.wizard__closeIcon')
        click_annoying_popu_about_pin_matches_selector.click()
        time.sleep(1.5)
    except:
        pass
    try:
        show_more_button_selector = driver.find_element(By.CLASS_NAME,'event__more.event__more--static') # show more matches selector
        show_more_button_selector.click()
    except:
        pass
    time.sleep(4)
    return driver


def find_all_matches_ids(driver):
    matches_list = driver.find_elements(By.CLASS_NAME,'event__match') # lista de todos los partidos de la liga
    id_matches = [i.get_attribute('id').split('_')[-1] for i in matches_list] # listado de ids de todos los partidos
    
    return id_matches


def get_all_data(driver,id_matches):
    match_dict = {}
    for id_match in tqdm(id_matches):
        url_tamplate_matches = f'https://www.flashscore.co/partido/{id_match}/#/resumen-del-partido/estadisticas-del-partido/0'
        driver.get(url_tamplate_matches)
        time.sleep(1.5)

        # CICLO FOR
        equipo_local = driver.find_elements(By.CLASS_NAME,'participant__participantName')[0].text
        equipo_visitante = driver.find_elements(By.CLASS_NAME,'participant__participantName')[-1].text  
        equipo_local = unicodedata.normalize('NFKD', equipo_local).encode('ASCII', 'ignore').decode('utf-8', 'ignore').lower() # remove accents
        equipo_visitante = unicodedata.normalize('NFKD', equipo_visitante).encode('ASCII', 'ignore').decode('utf-8', 'ignore').lower() # remove accents
        liga_jornada = driver.find_element(By.CLASS_NAME,'tournamentHeader__country').text
        jornada = liga_jornada.split('-')[-1].strip().lower().replace('jornada ','')
        if liga_jornada not in match_dict.keys():
            match_dict.update({liga_jornada : []})

        # stats_list = driver.find_elements(By.CLASS_NAME,'_row_lq1k0_9')
        stats_list = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='wcl-statistics']")
        goles_local, goles_visitante = driver.find_element(By.CLASS_NAME,'detailScore__wrapper').text.replace('\n','').split('-')
        fecha_partido = driver.find_element(By.CLASS_NAME,'duelParticipant__startTime').text.split(' ')[0]
        local_estadisticas = {}
        away_estadisticas = {}
        for i in stats_list:
            
            local_stat, name_stat, away_stat = i.text.split('\n')
            name_stat = unicodedata.normalize('NFKD', name_stat).encode('ASCII', 'ignore').decode('utf-8', 'ignore').lower() # remove accents
            name_stat = name_stat.replace(' ','_').replace('_(xg)','')
            
            
            local_estadisticas.update({name_stat:local_stat})
            
            away_estadisticas.update({name_stat:away_stat})
            # print(f'{local_stat} | {name_stat} | {away_stat}')

        local_estadisticas = {**local_estadisticas,**{'goles_anotados': goles_local,'fecha_partido': fecha_partido, 'equipo_contrario' : equipo_visitante, 'goles_recibidos' : goles_visitante, 'jornada' : jornada}}
        away_estadisticas = {**away_estadisticas,**{'goles_anotados': goles_visitante,'fecha_partido': fecha_partido, 'equipo_contrario' : equipo_local, 'goles_recibidos' : goles_local, 'jornada' : jornada}}
        # local_estadisticas.update({'goles': goles_local,'fecha_partido': fecha_partido, 'vs' : equipo_visitante})
        # away_estadisticas.update({'goles': goles_visitante,'fecha_partido': fecha_partido, 'vs' : equipo_local})
        match_dict[liga_jornada].append({f'{equipo_local}_L' : local_estadisticas, f'{equipo_visitante}_V' : away_estadisticas })
    
    return match_dict
    