import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

datasets = [
    'Middlesbrough vs Ilkley 20250410.xlsx',
    'Middlesbrough vs York 10112024.xlsx',
    "Middlesbrough vs Kendall 20251018.xlsx"
]
home_team = 'Middlesbrough'
teams = [
        'Ilkley',
        'York',
        'Kendall',
        #'Heath',
        #'Alnwick',
        #'Harrogate',
        #'Sandal',
        #'Penrith',
        #'Blaydon',
        #'Driffield',
        #'Cleckheaton'
        ]

home_dataset = []
opponent_dataset = []
for dataset in datasets:
    df_home = pd.read_excel(dataset, sheet_name=home_team)
    home_dataset.append(df_home)



for dataset in datasets:
    for team in teams:
        try:
            df_opponent = pd.read_excel(dataset, sheet_name=team)
            opponent_dataset.append(df_opponent)
        except Exception:
            # silently skip if sheet not found
            continue


# Safe concatenation
if opponent_dataset:
    opponent_data = pd.concat(opponent_dataset, ignore_index=True)
    opponent_data1 = pd.concat(opponent_dataset[:-1], ignore_index=True)
else:
    st.warning("No opponent sheets found across datasets.")
    opponent_data = pd.DataFrame()

if home_dataset:
    home_data = pd.concat(home_dataset, ignore_index=True)
else:
    st.warning("No home sheets found across datasets.")
    home_data = pd.DataFrame()

# Code Converter functions
# To get numerical representation of categorical columns in the dataset
# Key { 1: 'ranges', 2: 'Distance_avg', '3': 'line_breaks'}
ranges = {
    'A' : 5,
    'B' : 20,
    'C' : 30,
    'D' : 40,
    'E' : 50,
    'F' : 60,
    'G' : 70,
    'H' : 80,
    'I' : 90,
    'J' : 100,
    'Z' : -1,
    'X' : 0
    }

def distance_avg(x):
    
    if not isinstance(x,str):
        return 0
    if x != 0:
        y = list(x)
        new_list = []
        for word in y:
            for key,value in ranges.items():
                if word.upper() == key:
                    new_list.append(value)
        if sum(new_list) != 0:            
            return sum(new_list)/len(new_list)
        else:
            return 0
    
    else:
        return 0

def count_line_breaks(x):
    line_breakz = []
    if not isinstance(x, str):  # skip NaN or non-string
        return 0
    for carry in list(x):
        for code, value in ranges.items():
            if carry == code:
                if value/2 < 5:
                    pass
                else:
                    line_breakz.append(value)

    return len(line_breakz)


st.set_page_config(layout="centered", initial_sidebar_state="expanded", page_title = "Matchday Stats")
st.title("Matchday Stats")

st.sidebar.header("Menu")

menu =['Home'] + teams
selections = st.sidebar.selectbox('',menu)                             

if selections == 'Home':
    segment_control = st.segmented_control("",["Boro","Opponents"])
    if segment_control == 'Boro':
        st.subheader('Boro Statistics')
        st.markdown('Middlesbrough collective statistics during the season')
        dataset = pd.concat(home_dataset, axis=0, ignore_index=True)
        dataset1= pd.concat(home_dataset[:-1], axis=0, ignore_index=True)
        # dataset1 = home_datset[-2] 

        #Tries
        total_tries = len(dataset[dataset['Try'] == 'Yes'])
        difference_tries = len(dataset[dataset['Try'] == 'Yes']) - len(dataset1[dataset1['Try'] == 'Yes'])

        convert22 = []
        convert22_1 = []
        for team in opponent_dataset:
            if '22 Entries' in team.columns:
                con22r = (len(team[team['Try'] == 'Yes'])/ team['22 Entries'].sum()) *100
                convert22.append(con22r)
            
            else:
                pass
        conversionrate22 = str(round(sum(convert22) /len(convert22), 2)) + '%'
        for team in opponent_dataset[:-1]:
            if '22 Entries' in team.columns:
                con22r = (len(team[team['Try'] == 'Yes'])/ team['22 Entries'].sum()) *100
                convert22_1.append(con22r)

            else:
                pass
        difference_conversionrate22 = str(round(sum(convert22) /len(convert22), 2) - round(sum(convert22_1) /len(convert22_1), 2)) + '%'
        
        # Passes
        total_passes = dataset['Complete Pass'].sum()
        difference_passes = dataset['Complete Pass'].sum() - dataset1['Complete Pass'].sum()
        
        pass_accuracy = round((dataset['Complete Pass'].sum()/(dataset['Complete Pass'].sum() + dataset['Incomplete Pass'].sum())) * 100, 2)
        difference_pass_accuracy =  round((dataset['Complete Pass'].sum()/(dataset['Complete Pass'].sum() + dataset['Incomplete Pass'].sum())) * 100, 2) - round((dataset1['Complete Pass'].sum()/(dataset1['Complete Pass'].sum() + dataset1['Incomplete Pass'].sum())) * 100, 2)
    
    
        # Tackles
        total_tackles = dataset['Complete Tackle'].sum()
        difference_ttackles = dataset['Complete Tackle'].sum() - dataset1['Complete Tackle'].sum()
        
        tackle_success = round((dataset['Complete Tackle'].sum()/(dataset['Complete Tackle'].sum() + dataset['Incomplete Tackle'].sum())) * 100 ,2)
        difference_tsuccess =  round((dataset['Complete Tackle'].sum()/(dataset['Complete Tackle'].sum() + dataset['Incomplete Tackle'].sum())) * 100, 2) -round((dataset1['Complete Tackle'].sum()/(dataset1['Complete Tackle'].sum() +dataset1['Incomplete Tackle'].sum())) * 100, 2)
    
        #Set Pieces
        lineout_success = round((dataset['Lineout won'].sum()/(dataset['Lineout won'].sum() + dataset['Lineout lost'].sum())) * 100, 2)
        difference_lineout =  round((dataset['Lineout won'].sum()/(dataset['Lineout won'].sum() + dataset['Lineout lost'].sum())) * 100, 2) -    round((dataset1['Lineout won'].sum()/(dataset1['Lineout won'].sum() + dataset1['Lineout lost'].sum())) * 100, 2)
        
        scrum_success = round((dataset['Scrum won'].sum()/(dataset['Scrum won'].sum() + dataset['Scrum lost'].sum())) * 100, 2)
        difference_scrum =  round((dataset['Scrum won'].sum()/(dataset['Scrum won'].sum() + dataset['Scrum lost'].sum())) * 100, 2) - round((dataset1['Scrum won'].sum()/(dataset1['Scrum won'].sum() + dataset1['Scrum lost'].sum())) * 100, 2)

        
        # Metres Gained
        avg_m = dataset['AVG metres'].apply(distance_avg).mean()
        difference_avg_m = dataset['AVG metres'].apply(distance_avg).mean() - dataset1['AVG metres'].apply(distance_avg).mean()

        negative_carries = dataset[dataset['AVG metres'].astype(str).str.contains('Z', na=False)]['AVG metres'].astype(str).str.count('Z').sum()
        difference_negative_carries = dataset[dataset['AVG metres'].astype(str).str.contains('Z', na=False)]['AVG metres'].astype(str).str.count('Z').sum() - dataset1[dataset1['AVG metres'].astype(str).str.contains('Z', na=False)]['AVG metres'].astype(str).str.count('Z').sum()

        # Carries
        total_carries = dataset['Carries'].sum()
        difference_carries = dataset['Carries'].sum() - dataset1['Carries'].sum()

        dropped_balls = dataset[dataset['AVG metres'].astype(str).str.contains('X', na=False)]['AVG metres'].astype(str).str.count('X').sum()
        difference_dropped_balls = dataset[dataset['AVG metres'].astype(str).str.contains('X', na=False)]['AVG metres'].astype(str).str.count('X').sum() - dataset1[dataset1['AVG metres'].astype(str).str.contains('X', na=False)]['AVG metres'].astype(str).str.count('X').sum()

        # Line breaks
        line_breaks = dataset['AVG metres'].apply(count_line_breaks).sum()
        difference_line_breaks = dataset['AVG metres'].apply(count_line_breaks).sum() - dataset1['AVG metres'].apply(count_line_breaks).sum()
        # st.metric(label="Temperature", value="70 °F", delta="1.2 °F")
        kpi = {
            'Points': {'Tries': [total_tries, difference_tries],
                      '22 Conversion rate': [conversionrate22, difference_conversionrate22]},
            'Passes' : {'Total passes' :[total_passes, difference_passes],
                         'Pass accuracy' :[pass_accuracy, difference_pass_accuracy]},
            'Tackles' : {'Total tackles' :[total_tackles,difference_ttackles],
                         'Tackle completion' :[tackle_success,difference_tsuccess]},
            'Set Pieces':{'Lineout success':[lineout_success,difference_lineout],
                         'Scrum success': [scrum_success,difference_scrum]},
            'Ball Carries': {'Total Carries': [total_carries, difference_carries],
                             'Dropped balls': [dropped_balls, difference_dropped_balls]},
            'Metres Gained' : {'Average Carry metres': [avg_m, difference_avg_m],
                              'Negative Carries': [negative_carries, difference_negative_carries]},
            'Line Breaks' : {'Total Line Breaks': [line_breaks, difference_line_breaks]},
            }
        
        for category,metrics in kpi.items():
           
            st.subheader(category)
            col1, col2 = st.columns(2)
            with col1:
                for title, performance in list(metrics.items())[:len(metrics)//2]:
                    st.metric(title, value=performance[0], delta=performance[1])
            with col2:
                for title, performance in list(metrics.items())[len(metrics)//2:]:
                    st.metric(title, value=performance[0], delta=performance[1])
                    
        columns = dataset.columns
        
        
        pills = st.pills("Metric",(columns))

        def compare_bar_chart(metric_name):
            if dataset[metric_name].dtype != 'O':
                
                fig, ax = plt.subplots()
                ax.bar(['Recent', 'Previous'], [dataset[metric_name].mean(), dataset1[metric_name].mean()])
                ax.set_title(f'{metric_name} average comparison to previous game')
                ax.set_ylabel('Average value')
                st.pyplot(fig)

        for column in columns:
            if pills == column:
                compare_bar_chart(column)
    
    if segment_control == 'Opponents':
        st.subheader('Opponent Statistics')
        st.markdown('Opponent collective statistics against Midlesbrough during the season')
        # dataset = pd.concat(opponent_dataset, axis=0, ignore_index=True)
        dataset = opponent_data
        dataset1 = opponent_data1
        # dataset1= pd.concat(opponent_dataset, axis=0, ignore_index=True)

        #Tries
        total_tries = len(dataset[dataset['Try'] == 'Yes'])
        difference_tries = len(dataset[dataset['Try'] == 'Yes']) - len(dataset1[dataset1['Try'] == 'Yes'])

        convert22 = []
        convert22_1 = []
        for team in opponent_dataset:
            if '22 Entries' in team.columns:
                con22r = (len(team[team['Try'] == 'Yes'])/ team['22 Entries'].sum()) *100
                convert22.append(con22r)
            
            else:
                pass
        conversionrate22 = str(round(sum(convert22) /len(convert22), 2)) + '%'
        for team in opponent_dataset[:-1]:
            if '22 Entries' in team.columns:
                con22r = (len(team[team['Try'] == 'Yes'])/ team['22 Entries'].sum()) *100
                convert22_1.append(con22r)

            else:
                pass
        difference_conversionrate22 = str(round(sum(convert22) /len(convert22), 2) - round(sum(convert22_1) /len(convert22_1), 2)) + '%'
        
        # Passes
        total_passes = dataset['Complete Pass'].sum()
        difference_passes = dataset['Complete Pass'].sum() - dataset1['Complete Pass'].sum()
        
        pass_accuracy = round((dataset['Complete Pass'].sum()/(dataset['Complete Pass'].sum() + dataset['Incomplete Pass'].sum())) * 100, 2)
        difference_pass_accuracy =  round((dataset['Complete Pass'].sum()/(dataset['Complete Pass'].sum() + dataset['Incomplete Pass'].sum())) * 100, 2) - round((dataset1['Complete Pass'].sum()/(dataset1['Complete Pass'].sum() + dataset1['Incomplete Pass'].sum())) * 100, 2)
    
    
        # Tackles
        total_tackles = dataset['Complete Tackle'].sum()
        difference_ttackles = dataset['Complete Tackle'].sum() - dataset1['Complete Tackle'].sum()
        
        tackle_success = round((dataset['Complete Tackle'].sum()/(dataset['Complete Tackle'].sum() + dataset['Incomplete Tackle'].sum())) * 100 ,2)
        difference_tsuccess =  round((dataset['Complete Tackle'].sum()/(dataset['Complete Tackle'].sum() + dataset['Incomplete Tackle'].sum())) * 100, 2) -round((dataset1['Complete Tackle'].sum()/(dataset1['Complete Tackle'].sum() +dataset1['Incomplete Tackle'].sum())) * 100, 2)
    
        #Set Pieces
        lineout_success = round((dataset['Lineout won'].sum()/(dataset['Lineout won'].sum() + dataset['Lineout lost'].sum())) * 100, 2)
        difference_lineout =  round((dataset['Lineout won'].sum()/(dataset['Lineout won'].sum() + dataset['Lineout lost'].sum())) * 100, 2) -    round((dataset1['Lineout won'].sum()/(dataset1['Lineout won'].sum() + dataset1['Lineout lost'].sum())) * 100, 2)
        
        scrum_success = round((dataset['Scrum won'].sum()/(dataset['Scrum won'].sum() + dataset['Scrum lost'].sum())) * 100, 2)
        difference_scrum =  round((dataset['Scrum won'].sum()/(dataset['Scrum won'].sum() + dataset['Scrum lost'].sum())) * 100, 2) - round((dataset1['Scrum won'].sum()/(dataset1['Scrum won'].sum() + dataset1['Scrum lost'].sum())) * 100, 2)

        # Metres Gained
        avg_m = dataset['AVG metres'].apply(distance_avg).mean()
        difference_avg_m = dataset['AVG metres'].apply(distance_avg).mean() - dataset1['AVG metres'].apply(distance_avg).mean()

        negative_carries = dataset[dataset['AVG metres'].astype(str).str.contains('Z', na=False)]['AVG metres'].astype(str).str.count('Z').sum()
        difference_negative_carries = dataset[dataset['AVG metres'].astype(str).str.contains('Z', na=False)]['AVG metres'].astype(str).str.count('Z').sum() - dataset1[dataset1['AVG metres'].astype(str).str.contains('Z', na=False)]['AVG metres'].astype(str).str.count('Z').sum()

        # Carries
        total_carries = dataset['Carries'].sum()
        difference_carries = dataset['Carries'].sum() - dataset1['Carries'].sum()

        dropped_balls = dataset[dataset['AVG metres'].astype(str).str.contains('X', na=False)]['AVG metres'].astype(str).str.count('X').sum()
        difference_dropped_balls = dataset[dataset['AVG metres'].astype(str).str.contains('X', na=False)]['AVG metres'].astype(str).str.count('X').sum() - dataset1[dataset1['AVG metres'].astype(str).str.contains('X', na=False)]['AVG metres'].astype(str).str.count('X').sum()

         # Line breaks
        line_breaks = dataset['AVG metres'].apply(count_line_breaks).sum()
        difference_line_breaks = dataset['AVG metres'].apply(count_line_breaks).sum() - dataset1['AVG metres'].apply(count_line_breaks).sum()

        # # Straight Out Kicks
        # total_so_kicks = 
        # st.metric(label="Temperature", value="70 °F", delta="1.2 °F")
        kpi = {
            'Points': {'Tries': [total_tries, difference_tries],
                       '22 Conversion rate': [conversionrate22, difference_conversionrate22]},
            'Passes' : {'Total passes' :[total_passes, difference_passes],
                         'Pass accuracy' :[pass_accuracy, difference_pass_accuracy]},
            'Tackles' : {'Total tackles' :[total_tackles,difference_ttackles],
                         'Tackle completion' :[tackle_success,difference_tsuccess]},
            'Set Pieces':{'Lineout success':[lineout_success,difference_lineout],
                         'Scrum success': [scrum_success,difference_scrum]},
            'Ball Carries': {'Total Carries': [total_carries, difference_carries],
                             'Dropped balls': [dropped_balls, difference_dropped_balls]},
            'Metres Gained' : {'Average Carry metres': [avg_m, difference_avg_m],
                              'Negative Carries': [negative_carries, difference_negative_carries]},
            'Line Breaks' : {'Total Line Breaks': [line_breaks, difference_line_breaks]}
            }
        
        for category,metrics in kpi.items():
           
            st.subheader(category)
            col1, col2 = st.columns(2)
            with col1:
                for title, performance in list(metrics.items())[:len(metrics)//2]:
                    st.metric(title, value=performance[0], delta=performance[1])
            with col2:
                for title, performance in list(metrics.items())[len(metrics)//2:]:
                    st.metric(title, value=performance[0], delta=performance[1])
                    
        columns = dataset.columns
        
        
        pills = st.pills("Metric",(columns))

        def compare_bar_chart(metric_name):
            c_dataset = dataset.drop('Try', axis=1)
            c_dataset1 = dataset1.drop('Try', axis=1)
            if c_dataset[metric_name].dtype != 'O':
                
                fig, ax = plt.subplots()
                ax.bar(['Recent', 'Previous'], [c_dataset[metric_name].mean(), c_dataset1[metric_name].mean()])
                ax.set_title(f'{metric_name} average comparison to previous game')
                ax.set_ylabel('Average value')
                st.pyplot(fig)

            else:
                fig, ax = plt.subplots()
                ax.bar(['Recent', 'Previous'], [c_dataset[metric_name].apply(distance_avg).mean(), c_dataset1[metric_name].apply(distance_avg).mean()])
                ax.set_title(f'{metric_name} average comparison to previous game')
                ax.set_ylabel('Average value')
                st.pyplot(fig)

        for column in columns:
            if pills == column:
                compare_bar_chart(column)
                

for team in teams:
    if selections == team:
        st.header(team)
        for dataset in datasets:
            if team in dataset:
                home_df = pd.read_excel(dataset, sheet_name=home_team)
                opponent_df = pd.read_excel(dataset, sheet_name=team)

                penalties = [len(home_df[home_df['Try'] == 'Yes']), len(opponent_df[opponent_df['Try'] == 'Yes'])]
                col1,col2 = st.columns(2)
                col3,col4 = st.columns(2)
                col5, col6 = st.columns(2)
                with col1:
                    fig, ax = plt.subplots(figsize=[5,5])
                    ax.pie(
                            penalties,
                            labels=[f"{home_team} ({penalties[0]})", f"{team} ({penalties[1]})"],
                        )
                    ax.set_title('Tries', fontweight='bold')
                    st.pyplot(fig)
                    st.write('Number of tries per team.')
                with col2:
                    mistakes_home = round(((home_df['Complete Pass'].sum() + home_df['Complete Tackle'].sum() + home_df['Turnover'].sum() + home_df['Lineout won'].sum() + home_df['Scrum won'].sum())/(home_df['Complete Pass'].sum() + home_df['Incomplete Pass'].sum() + home_df['Complete Tackle'].sum() + home_df['Incomplete Tackle'].sum() + home_df['Knock-on'].sum() + home_df['Forward'].sum() + home_df['Turnover'].sum() + opponent_df['Turnover'].sum() + home_df['Lineout won'].sum() + home_df['Lineout lost'].sum() + home_df['Scrum won'].sum() + home_df['Scrum lost'].sum()))* 100,2)
                    
                    mistakes_opp = round(((opponent_df['Complete Pass'].sum() + opponent_df['Complete Tackle'].sum() + opponent_df['Turnover'].sum() + opponent_df['Lineout won'].sum() + opponent_df['Scrum won'].sum())/(opponent_df['Complete Pass'].sum() +opponent_df['Incomplete Pass'].sum() + opponent_df['Complete Tackle'].sum() + opponent_df['Incomplete Tackle'].sum() + opponent_df['Knock-on'].sum() + opponent_df['Forward'].sum() + opponent_df['Turnover'].sum() + home_df['Turnover'].sum() + opponent_df['Lineout won'].sum() + opponent_df['Lineout lost'].sum() + opponent_df['Scrum won'].sum() + opponent_df['Scrum lost'].sum())) * 100,2)
                    fig, ax = plt.subplots(figsize=[5,5])
                    ax.bar(['Middlesbrough', team],[mistakes_home, mistakes_opp], width=0.5, color=[ '#D9534F', '#0047AB'])
                    ax.set_ylabel('Percentage %')
                    ax.set_xlabel('Team')
                    ax.set_title("Overall Team Accuracy Comparison", fontweight='bold')
                    ax.set_ylim(0, 100)
                    for i, v in enumerate([mistakes_home, mistakes_opp]):
                        ax.text(i, v + 1, f"{v}%", ha='center', fontweight='bold')
                    st.pyplot(fig)
                    st.write( f"**Team Accuracy Analysis:** This chart compares the overall game accuracy between **Middlesbrough** and **{team}**, "
    "based on successful passes, tackles, turnovers won, and set-piece completions. "
    "A higher percentage indicates greater efficiency and fewer technical mistakes during play.")


                with col3:
                    # home_tackle_ratio = home_df['Complete Tackle'].sum()/(home_df['Complete Tackle'].sum() + home_df['Incomplete Tackle'].sum())
                    # home_tackle_success = f"{home_tackle_ratio * 100:.2f}%"
                    # opp_tackle_ratio = opponent_df['Complete Tackle'].sum()/(opponent_df['Complete Tackle'].sum() + opponent_df['Incomplete Tackle'].sum())
                    # opp_tackle_success = f"{opp_tackle_ratio * 100:.2f}%"
                    # st.metric('Tackle completion', value=home_tackle_success)
                    h_lineout_success = round((home_df['Lineout won'].sum()/(home_df['Lineout won'].sum() + home_df['Lineout lost'].sum())) * 100, 2)
                    opp_lineout_success = round((opponent_df['Lineout won'].sum()/(opponent_df['Lineout won'].sum() + opponent_df['Lineout lost'].sum())) * 100, 2)
                    fig, ax = plt.subplots(figsize=[5,5])
                    ax.bar(['Middlesbrough', team],[h_lineout_success, opp_lineout_success], width=0.5, color=[ '#D9534F', '#0047AB'])
                    ax.set_ylabel('Percentage %')
                    ax.set_xlabel('Team')
                    ax.set_title("Lineout Success", fontweight='bold')
                    ax.set_ylim(0, 100)
                    for i, v in enumerate([h_lineout_success, opp_lineout_success]):
                        ax.text(i, v + 1, f"{v}%", ha='center', fontweight='bold')
                    st.pyplot(fig)
        

                with col4:
                    # if 'AVG metres' in home_df.columns:
                        
                    #     home_line_breaks = home_df['AVG metres'].apply(count_line_breaks).sum()
                    #     opp_line_breaks = opponent_df['AVG metres'].apply(count_line_breaks).sum()
                    # else:
                    #     home_line_breaks = 'No data'
                    #     opp_line_breaks = 'No data'

                    
                    # st.metric('Opponent line breaks', value=opp_line_breaks)
                    h_scrum_success = round((home_df['Scrum won'].sum()/(home_df['Scrum won'].sum() + home_df['Scrum lost'].sum())) * 100, 2)
                    opp_scrum_success = round((opponent_df['Scrum won'].sum()/(opponent_df['Scrum won'].sum() + opponent_df['Scrum lost'].sum())) * 100, 2)
                    fig, ax = plt.subplots(figsize=[5,5])
                    ax.bar(['Middlesbrough', team],[h_scrum_success, opp_scrum_success], width=0.5, color=[ '#D9534F', '#0047AB'])
                    ax.set_ylabel('Percentage %')
                    ax.set_xlabel('Team')
                    ax.set_title("Scrum Success", fontweight='bold')
                    ax.set_ylim(0, 100)
                    for i, v in enumerate([h_scrum_success, opp_scrum_success]):
                        ax.text(i, v + 1, f"{v}%", ha='center', fontweight='bold')
                    st.pyplot(fig)
        
                segment_control = st.segmented_control("",["Attack","Defence"])
                if segment_control == "Attack":
                     # Passes
                    if 'Complete Pass' in home_df.columns:
                        total_passes = home_df['Complete Pass'].sum()
                        pass_accuracy = str(round((home_df['Complete Pass'].sum()/(home_df['Complete Pass'].sum() + home_df['Incomplete Pass'].sum())) * 100, 2)) + '%'
                    else:
                        total_passes = 'No data'
                        pass_accuracy = 'No data'
                    # Carries
                    if 'Carries' in home_df.columns:
                        total_carries = home_df['Carries'].sum()
                        dropped_balls = home_df[home_df['AVG metres'].astype(str).str.contains('X', na=False)]['AVG metres'].astype(str).str.count('X').sum()
                    else:
                        total_carries = 'No data'
                        dropped_balls = 'No data'
                        
                    # Metres Gained
                    if 'AVG metres' in home_df.columns:
                        avg_m = str(round(home_df['AVG metres'].apply(distance_avg).mean(), 2)) + ' metres'
                        negative_carries = home_df[home_df['AVG metres'].astype(str).str.contains('Z', na=False)]['AVG metres'].astype(str).str.count('Z').sum()
                    else:
                        avg_m = 'No data'
                        negative_carries = 'No data'
                        
                    # Line breaks
                    if 'AVG metres'in home_df.columns:
                        line_breaks = home_df['AVG metres'].apply(count_line_breaks).sum()
                        phases = round(total_carries/(home_df['Knock-on'].sum() + home_df['Turnover'].sum()))
                    else:
                        line_breaks = 'No data'
                        phases = 'No data'
                    # 22 Entries
                    
                    
                    convert22 = []
                    
                    if '22 Entries' in home_df.columns:
                        entry22 = home_df['22 Entries'].sum()
                        con22r = (len(home_df[home_df['Try'] == 'Yes'])/ home_df['22 Entries'].sum()) *100
                        convert22.append(con22r)
                        conversionrate22 = str(round(sum(convert22) /len(convert22), 2)) + '%'
                    else:
                        entry22 = 'No data'
                        conversionrate22 = 'No data'
                    
                    kpi = {
            'Passes' : {'Total passes' :total_passes,
                         'Pass accuracy' :pass_accuracy},
            'Ball Carries': {'Total Carries': total_carries,
                             'Dropped balls': dropped_balls},
            'Metres Gained' : {'Average Carry metres': avg_m,
                              'Negative Carries': negative_carries},
            'Attack Efficiency' : {'Total Line Breaks': line_breaks,
                             'Complete Phases until Turnover': phases},
            '22 Entries' :{'Total 22 Entries': entry22,
                           'Gold Zone Conversion Rate': conversionrate22}
            }

                    for category,metrics in kpi.items():
                        st.subheader(category)
                        col1, col2 = st.columns(2)
                        with col1:
                            for title, performance in list(metrics.items())[:len(metrics)//2]:
                                st.metric(title, value=performance)
                        with col2:
                            for title, performance in list(metrics.items())[len(metrics)//2:]:
                                st.metric(title, value=performance)

                        st.write()
                        
                if segment_control =="Defence":
                    # Tackles
                    if 'Complete Tackle' in home_df.columns:
                        total_tackles = home_df['Complete Tackle'].sum()
                        tackle_success = str(round((home_df['Complete Tackle'].sum()/(home_df['Complete Tackle'].sum() + home_df['Incomplete Tackle'].sum())) * 100 ,2)) + '%'
                    else:
                        total_tackles = 'No data'
                        tackle_success = 'No data'

                    # Carries
                    if 'Carries' in opponent_df.columns:
                        total_carries = opponent_df['Carries'].sum()
                        avg_m = str(round(opponent_df['AVG metres'].apply(distance_avg).mean(), 2)) + ' metres'
                    else:
                        total_carries = 'No data'
                        avg_m = 'No data'
                        
                     # Line breaks
                    if 'AVG metres'in opponent_df.columns:
                        line_breaks = opponent_df['AVG metres'].apply(count_line_breaks).sum()
                        phases = round(opponent_df['Carries'].sum()/(opponent_df['Knock-on'].sum() + opponent_df['Turnover'].sum()))
                    else:
                        line_breaks = 'No data'
                        phases = 'No data'
                    # 22 Entries
                    
                    
                    convert22 = []
                    
                    if '22 Entries' in opponent_df.columns:
                        entry22 = opponent_df['22 Entries'].sum()
                        con22r = (len(opponent_df[opponent_df['Try'] == 'Yes'])/ opponent_df['22 Entries'].sum()) *100
                        convert22.append(con22r)
                        conversionrate22 = str(round(sum(convert22) /len(convert22), 2)) + '%'
                    else:
                        entry22 = 'No data'
                        conversionrate22 = 'No data'
                    kpi = {
            'Tackles' : {'Total tackles' :total_tackles,
                         'Tackle completion' : tackle_success},
            'Ball Carries': {'Total Carries': total_carries,
                             'Average Carry metres': avg_m},
            # 'Metres Gained' : {'Dropped balls': [dropped_balls, difference_dropped_balls]
            #                   'Negative Carries': [negative_carries, difference_negative_carries]},
            'Defensive Work Rate' : {'Total Line Breaks': line_breaks,
                             'Complete Phases until Turnover': phases},
            '22 Entries' : {'Total 22 Entries': entry22,
                           'Gold Zone Conversion Rate': conversionrate22}
            }
                    for category,metrics in kpi.items():
                        st.subheader(category)
                        col1, col2 = st.columns(2)
                        with col1:
                            for title, performance in list(metrics.items())[:len(metrics)//2]:
                                st.metric(title, value=performance)
                        with col2:
                            for title, performance in list(metrics.items())[len(metrics)//2:]:
                                st.metric(title, value=performance)

                        st.write()
                # with col5:
                #     if '22 Entries' in home_df.columns:
                #         home_22_entries = home_df['22 Entries'].sum()
                #         opp_22_entries = opponent_df['22 Entries'].sum()

                #     else:
                #         home_22_entries = 'No data'
                #         opp_22_entries = 'No data'

                #     st.metric('22 Entries', value=home_22_entries)
                #     st.metric('Opposition 22 Entries', value=opp_22_entries)
                    
# if selections == 'Display Data':
#     st.subheader("Display Data")
#     st.dataframe(data)
    
#     if st.checkbox("Show data"):
#         st.write("Data Shape: ")
#         st.write('{} rows and {} columns'.format(data.shape[0],data.shape[1]))
        
#         st.markdown("Descriptive statistics")
#         st.write(data.describe())
    
    
