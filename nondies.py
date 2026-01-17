import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

import os
os.chdir("C:/Users/cex/Desktop/Rugby Streamlit")


# datasets = [
#     #'Middlesbrough vs Ilkley 20250410.xlsx',
#     r"C:\Users\cex\Desktop\Rugby Streamlit\Middlesbrough vs Ilkley 20250410.xlsx",
#     #'Middlesbrough vs York 10112024.xlsx',
#     r"C:\Users\cex\Desktop\Rugby Streamlit\Middlesbrough vs York 10112024.xlsx",
#     #"Middlesbrough vs Kendall 20251018.xlsx",
#     r"C:\Users\cex\Desktop\Rugby Streamlit\Middlesbrough vs Kendall 20251018.xlsx",
#     #"Middlesbrough vs Alnwick 08112025.xlsx",
#     r"C:\Users\cex\Desktop\Rugby Streamlit\Middlesbrough vs Alnwick 08112025.xlsx"
# ]
    
home_team = 'Middlesbrough'
teams = [
    #'Harrogate(A)',
    #'Driffield(H)',
    #'Heath(A)',
        #'Ilkley(H)',
        'York(A)',
        'Kendall(H)',
        #'Sandal(A)',
        'Alnwick(A)',
        #'Penrith(H)',
        #'Blaydon(A)',
        #'Cleckheaton(H)'
        ]

matchdays = {
    # 'Ilkley' : {
    #     'home':{
    #         'file':'Middlesbrough vs Ilkley 20250410.xlsx',
    #         'date': ''
    #             },
    #     'away':{
    #         'file':'',
    #         'dtae':''
    #     }
    # },
    'York' : {
        'away':{
                 'file' :"Middlesbrough vs York 10112024.xlsx",
                 'date' : '11 October 2025'
                },
        'home':{
                'file': None,
                'date': '17 January 2026'
                }
             },
    'Kendall' : {
        'home':{
            'file' : "Middlesbrough vs Kendall 20251018.xlsx",
            'date' : '18 October 2025'},
        'away':{
            'file' : None,
            'date' : None
        }
    },
    #'Heath' : {
    #     'home':{
    #         'file':'',
    #         'date': ''
    #             },
    #     'away':{
    #         'file':'',
    #         'dtae':''
    #     }
    # },
    'Alnwick' : {
        'away':{
            'file' : "Middlesbrough vs Alnwick 08112025.xlsx",
            'date' : '8 November 2025'
        },
        'home':{
            'file' : None,
            'date' : None
        }
    },
    #'Harrogate' : {
    #     'home':{
    #         'file':'',
    #         'date': ''
    #             },
    #     'away':{
    #         'file':'',
    #         'dtae':''
    #     }
    # },
    #'Sandal' : {
    #     'home':{
    #         'file':'',
    #         'date': ''
    #             },
    #     'away':{
    #         'file':'',
    #         'dtae':''
    #     }
    # },
    #'Penrith' : {
    #     'home':{
    #         'file':'',
    #         'date': ''
    #             },
    #     'away':{
    #         'file':'',
    #         'dtae':''
    #     }
    # },
    #'Blaydon' : {
    #     'home':{
    #         'file':'',
    #         'date': ''
    #             },
    #     'away':{
    #         'file':'',
    #         'dtae':''
    #     }
    # },
    #'Driffield' : {
    #     'home':{
    #         'file':'',
    #         'date': ''
    #             },
    #     'away':{
    #         'file':'',
    #         'dtae':''
    #     }
    # },
    #'Cleckheaton' : {
    #     'away':{
    #         'file':'',
    #         'date': ''
    #             },
    #     'away':{
    #         'file':'',
    #         'dtae':''
    #     }
    # },
}
home_team = 'Middlesbrough'

home_dataset = []
opponent_dataset = []

for index,key in matchdays.items():
    if key['home']['file'] is not None:
        df_home_h = pd.read_excel(key['home']['file'], sheet_name=index)
        home_dataset.append(df_home_h.fillna(0))
    if key['away']['file'] is not None:
        df_home_a = pd.read_excel(key['away']['file'], sheet_name=index)
        home_dataset.append(df_home_a.fillna(0))


for index,key in matchdays.items():
    if key['home']['file'] is not None:
        df_away_h = pd.read_excel(key['home']['file'], sheet_name=index)
        opponent_dataset.append(df_away_h.fillna(0))
    if key['away']['file'] is not None:
        df_away_a = pd.read_excel(key['away']['file'], sheet_name=index)
        opponent_dataset.append(df_away_a.fillna(0))


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
# Key { 0: 'event_values'
#        : 'Key for the numeric values of events.'
#       1: 'ranges'
#        : 'Key for the letter symbols measuring distance',
#       2: 'Distance_avg',
#        ; 'Function to derive the average distance in a given sequence'
#       3: 'count_line_breaks',
#        ; 'Function to count number of line breaks in a sequence. Has to be more than 5 meyters to be considered a line break'
#       4: 'get_values'
#        ; 'Function to derive the numeric values of the letter symbols. Useful for plotting graphs.',
#       5: 'get_time'
#        ; 'Function to derive the time in the 'minute:second' format',}
event_values = {
    'T' : 5,
    'P' : 3,
    'C' : -5,
    'Q' : -3,
    'N' : 0
}

ranges = {
    'A' : {'title':'0-5',
            'average': 2.5,
            'code' : 1
          },
    'B' : {'title': '5-20',
            'average' : 12.5,
             'code' : 2
          },
    'C' : {'title':'20-30',
            'average': 25,
            'code' : 3
          },
    'D' : {'title':'30-40',
            'average': 35,
            'code' : 4
          },
    'E' : {'title':'40-50',
            'average': 45,
             'code' : 5
          },
    'F' : {'title':'50-60',
            'average': 55,
            'code' : 6
          },
    'G' : {'title':'60-70',
            'average': 65,
            'code' : 7
          },
    'H' : {'title':'70-80' ,
            'average': 75,
            'code' : 8
          },
    'I' : {'title':'80-90' ,
            'average': 85,
            'code' : 9
          },
    'J' : {'title':'90-100' ,
            'average': 95,
            'code' : 0
          },
    'Z' : {'title': 'Negative carry',
            'average': -1,
            'code' : 0
          },
    'X' : {'title': 'Dropped ball',
            'average': 0,
            'code' : 0
        },
    }
ranges_avg = {
    'A' : 2.5,
    'B' : 12.5,
    'C' : 25,
    'D' : 35,
    'E' : 45,
    'F' : 55,
    'G' : 65,
    'H' : 75,
    'I' : 85,
    'J' : 95,
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
                    new_list.append(ranges[word.upper()]['average'])
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
            if carry.upper() == code:
                if value['average']/2 < 5:
                    pass
                else:
                    line_breakz.append(value)

    return len(line_breakz)

def get_values(series, ranges_avg):
    
    chars = list(''.join(series.astype('str').to_list()))
    return [ranges_avg[char] for char in chars if char in ranges_avg]

def get_time(x):
    try:
        x = int(x)  # ensure numeric
    except (ValueError, TypeError):
        return "Missing data"
    else:
        time = x/60
        minute = x//60
        second = x - (minute*60)
        return f"{minute}:{second:02d} minutes"


def state_distribution(seq):
    new_seq = pd.Series(list(seq))
    distr_list = new_seq.value_counts().to_dict()
    # Replace keys using ranges
    mapped_distr = {
        ranges[k]['title']: v
        for k, v in distr_list.items()
        if k in ranges
    }

    return mapped_distr

# MACHINE LEARNING
def build_transition_matrix(series, seq=None):
    transitions = {}
    series = pd.Series(series)
    for s in series.astype(str):
        for a, b in zip(s, s[1:]):
            transitions.setdefault(a, {})
            transitions[a][b] = transitions[a].get(b, 0) + 1

    # convert to DataFrame
    index = sorted(transitions.keys())
    cols = sorted({b for a in transitions for b in transitions[a]})
    matrix = pd.DataFrame(0, index=index, columns=cols)

    for a in transitions:
        for b in transitions[a]:
            matrix.loc[a, b] = transitions[a][b]

    # convert counts → probabilities
    matrix = matrix.div(matrix.sum(axis=1), axis=0).fillna(0)
    
    if seq is None:
    
        return matrix
    # Create a dictionary to get the probabilities of a sequence occuring from the transition matrix above
    else:
        if seq != 0:
            probs = []
            for i in range(len(seq)-1):
                s1, s2 = seq[i], seq[i+1]
                if s1 in matrix.index and s2 in matrix.columns:
                    p = matrix.loc[s1, s2]
                    if p > 0:
                        probs.append(p)
            if not probs:
                return {'Mean Transition Probability':0,
                'Minimum Transition Probbility':0,
                'Maximum Transition Probability':0,
                'Predictability of Sequence':0  # sequence surprisal
                       }
            
            return {
                'Mean Transition Probability':np.mean(probs),
                'Minimum Transition Probbility':np.min(probs),
                'Maximum Transition Probability':np.max(probs),
                'Predictability of Sequence':-np.sum(np.log(np.array(probs)))  # sequence surprisal
                    }
        else:
            return {'Mean Transition Probability':0,
                'Minimum Transition Probbility':0,
                'Maximum Transition Probability':0,
                'Predictability of Sequence':0  # sequence surprisal
                   }
            
def sequence_stats(seq):
    if seq != 0:
        probs = []
        for i in range(len(seq)-1):
            s1, s2 = seq[i], seq[i+1]
            if s1 in P.index and s2 in P.columns:
                probs.append(P.loc[s1, s2])
        if not probs:
            return {'Mean Transition Probability':0,
            'Minimum Transition Probbility':0,
            'Maximum Transition Probability':0,
            'Predictability of Sequence':0  # sequence surprisal
                   }
        
        return {
            'Mean Transition Probability':np.mean(probs),
            'Minimum Transition Probbility':np.min(probs),
            'Maximum Transition Probability':np.max(probs),
            'Predictability of Sequence':-np.sum(np.log(np.array(probs)))  # sequence surprisal
                }
    else:
        return {'Mean Transition Probability':0,
            'Minimum Transition Probbility':0,
            'Maximum Transition Probability':0,
            'Predictability of Sequence':0  # sequence surprisal
                   }
        
def mtp_interpretation(x):
    if x >= 0.6:
        return "The attack relied on repeated carry patterns, indicating a structured but predictable phase strategy."
    elif 0.4 <= x < 0.6:
        return "The carry sequences balanced structure with adaptability, suggesting effective phase control."
    elif 0.2 <= x < 0.4:
        return "The carry sequences were shaped by moment-to-moment opportunities rather than sustained structure."
    else:
        return "The carry sequences reflected breakdown scenarios, with decisions driven by defensive pressure."

def surprisal_interpretation(x):
    if x < 0.6:
        return "Attacking phases were highly repeatable, with limited deviation from established carry patterns."
    elif 0.6 <= x < 1.0:
        return "Attacking phases retained structure while incorporating controlled variation."
    elif 1.0 <= x < 1.4:
        return "Attacking phases featured high decision-making freedom and attacking initiative."
    else:
        return "Attacking phases were predominantly reactive, driven by breakdown speed and defensive disruption."

def combined_attack_interpretation(mtp,surprisal):
    
    if mtp >= 0.6 and surprisal < 0.6:
        return (
            "The attack relied on repeated carry patterns within highly repeatable phases, "
            "indicating a stable and well-defined phase structure with limited variation."
        )

    elif mtp >= 0.6 and surprisal >= 0.6:
        return (
            "The attack was built on consistent carry structures, but phases evolved dynamically, "
            "suggesting controlled variation layered onto a stable framework."
        )

    elif 0.4 <= mtp < 0.6 and 0.6 <= surprisal < 1.0:
        return (
            "The carry sequences balanced structure and adaptability, "
            "with phases adjusting in response to defensive cues while maintaining overall control."
        )

    elif 0.4 <= mtp < 0.6 and surprisal >= 1.0:
        return (
            "The attack showed flexible carry patterns, but phase progression became increasingly volatile, "
            "reflecting a shift toward opportunistic decision-making."
        )

    elif mtp < 0.4 and surprisal >= 1.0:
        return (
            "The carry sequences lacked sustained structure and were driven by reactive decisions, "
            "suggesting phases shaped primarily by defensive pressure and breakdown speed."
        )

    else:
        return (
            "The attack displayed limited structural continuity, "
            "with phases emerging on a moment-to-moment basis rather than from planned patterns."
        )

def hash_sequence(seq):
    if seq != 0:
        s = str(seq)
        return int(hashlib.md5(s.encode()).hexdigest(), 16) % (10**8)
    else:
        return 0

def numeric_sequence(x):
    if not isinstance(x, (list, tuple, str)):
        return []

    numeric = [int(ranges[c.upper()]['code']) for c in x if c.upper() in ranges]
    return numeric

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
        total_tries = len(dataset[dataset['Event'] == 'T'])
        difference_tries = len(dataset[dataset['Event'] == 'T']) - len(dataset1[dataset1['Event'] == 'T'])

        # Penalties
        total_penalties = len(dataset[dataset['Event'] == 'P'])
        difference_penalties = len(dataset[dataset['Event'] == 'P']) - len(dataset1[dataset1['Event'] == 'P'])

        # 22 entries
        total_22_entries = dataset['22 Entries For'].sum()
        total_22_entries_1 = dataset1['22 Entries For'].sum()
        difference_22_entries = dataset['22 Entries For'].sum() - dataset1['22 Entries For'].sum()
        convert22 = []
        convert22_1 = []
        for team in home_dataset:
            if '22 Entries For' in team.columns:
                
                con22r = (len(team[team['Event'] == 'T'])/ team['22 Entries For'].sum()) *100
                convert22.append(con22r)
            
            else:
                pass
        conversionrate22 = str(round(sum(convert22) /len(convert22), 2)) + '%'
        for team in home_dataset[:-1]:
            if '22 Entries For' in team.columns:
                
                con22r = (len(team[team['Event'] == 'T'])/ team['22 Entries For'].sum()) *100
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

         # Kicks
        straight_out_kicks = len(get_values(dataset['Straight Out Kick'], ranges_avg))
        difference_so_kicks = len(get_values(dataset['Straight Out Kick'], ranges_avg)) - len(get_values(dataset1['Straight Out Kick'], ranges_avg))
        
        territorial_kicks = len(get_values(dataset['Territorial Kick'], ranges_avg))
        difference_t_kicks = len(get_values(dataset['Territorial Kick'], ranges_avg)) - len(get_values(dataset1['Territorial Kick'], ranges_avg))
        kpi = {
            'Points': {'Tries': [total_tries, difference_tries],
                       'Penalties': [total_penalties, difference_penalties],
                      },
            '22 Entries' : {'22 entries' : [total_22_entries, difference_22_entries],
                          '22 Conversion rate': [conversionrate22, difference_conversionrate22], },
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
            'Kicks' : {'Straight Out Kicks' : [straight_out_kicks, difference_so_kicks],
                       'Territorial Kicks' : [territorial_kicks, difference_t_kicks]}
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
        total_tries = len(dataset[dataset['Event'] == 'T'])
        difference_tries = len(dataset[dataset['Event'] == 'T']) - len(dataset1[dataset1['Event'] == 'T'])

        convert22 = []
        convert22_1 = []
        for team in opponent_dataset:
            if '22 Entries For' in team.columns:
                con22r = (len(team[team['Event'] == 'T'])/ team['22 Entries For'].sum()) *100
                convert22.append(con22r)
            
            else:
                pass
        conversionrate22 = str(round(sum(convert22) /len(convert22), 2)) + '%'
        for team in opponent_dataset[:-1]:
            if '22 Entries For' in team.columns:
                con22r = (len(team[team['Event'] == 'T'])/ team['22 Entries For'].sum()) *100
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

         # Kicks
        straight_out_kicks = len(get_values(dataset['Straight Out Kick'], ranges_avg))
        difference_so_kicks = len(get_values(dataset['Straight Out Kick'], ranges_avg)) - len(get_values(dataset1['Straight Out Kick'], ranges_avg))
        
        territorial_kicks = len(get_values(dataset['Territorial Kick'], ranges_avg))
        difference_t_kicks = len(get_values(dataset['Territorial Kick'], ranges_avg)) - len(get_values(dataset1['Territorial Kick'], ranges_avg))

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
            'Kicks' : {'Straight Out Kicks' : [straight_out_kicks, difference_so_kicks],
                       'Territorial Kicks' : [territorial_kicks, difference_t_kicks]}
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
            c_dataset = dataset.drop('Event', axis=1)
            c_dataset1 = dataset1.drop('Event', axis=1)
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
        segments = st.segmented_control('',['Overview', 'Match Report', 'Analyses'])
 
        
        #for dataset in datasets:
         #   df_home = pd.read_excel(dataset, sheet_name=home_team) 
        if team[:-3] in matchdays.keys():
            if '(A)' in team:
                df_home = pd.read_excel(matchdays[team[:-3]]['away']['file'], sheet_name=home_team, header=0)
                home_df = df_home.fillna(0)
                df_opponent = pd.read_excel(matchdays[team[:-3]]['away']['file'], sheet_name=team[:-3], header=0)
                opponent_df = df_opponent.fillna(0)
                date = matchdays[team[:-3]]['away']['date']
            else:
                df_home = pd.read_excel(matchdays[team[:-3]]['home']['file'], sheet_name=home_team, header=0)
                home_df = df_home.fillna(0)
                df_opponent = pd.read_excel(matchdays[team[:-3]]['home']['file'], sheet_name=team[:-3], header=0)
                opponent_df = df_opponent.fillna(0)
                date = matchdays[team[:-3]]['home']['date']
                # st.write(opponent_df.columns)
        if segments == 'Overview':
            #Scores
            home_tries = len(home_df[home_df['Event'] == 'T'])
            opp_tries = len(opponent_df[opponent_df['Event'] == 'T'])
            
            home_penalties = len(home_df[home_df['Event'] == 'P'])
            opp_penalties = len(opponent_df[opponent_df['Event'] == 'P'])
            
            home_scores = (home_tries * 5) + (home_penalties * 3)
            opp_scores = (opp_tries * 5) + (opp_penalties * 3)
            
            #Passes
            home_pass_acc = (home_df['Complete Pass'].sum()/(home_df['Complete Pass'].sum() + home_df['Incomplete Pass'].sum())) * 100
            opp_pass_acc =(opponent_df['Complete Pass'].sum()/(opponent_df['Complete Pass'].sum() + opponent_df['Incomplete Pass'].sum())) * 100
            #Tackle completion
            home_tackle_comp = (home_df['Complete Tackle'].sum()/(home_df['Complete Tackle'].sum() + home_df['Incomplete Tackle'].sum())) * 100
            opp_tackle_comp = (opponent_df['Complete Tackle'].sum()/(opponent_df['Complete Tackle'].sum() + opponent_df['Incomplete Tackle'].sum())) * 100
            #Lineout success
            home_lineout_succ = (home_df['Lineout won'].sum()/(home_df['Lineout won'].sum() + home_df['Lineout lost'].sum())) * 100
            opp_lineout_succ = (opponent_df['Lineout won'].sum()/(opponent_df['Lineout won'].sum() + opponent_df['Lineout lost'].sum())) * 100
            #Scrum success
            home_scrum_succ = (home_df['Scrum won'].sum()/(home_df['Scrum won'].sum() + home_df['Scrum lost'].sum())) * 100
            opp_scrum_succ = (opponent_df['Scrum won'].sum()/(opponent_df['Scrum won'].sum() + opponent_df['Scrum lost'].sum()))* 100
            
            # Average Carry Metres
            home_carry_metres = distance_avg(''.join(home_df['AVG metres'].astype(str).to_list()).replace('0',''))
            opp_carry_metres = distance_avg(''.join(opponent_df['AVG metres'].astype(str).to_list()).replace('0',''))
            
            # Number of Territorial Kicks
            home_terr_num = len(''.join(home_df['Territorial Kick'].astype(str).to_list()).replace('0',''))
            opp_terr_num = len(''.join(opponent_df['Territorial Kick'].astype(str).to_list()).replace('0',''))
            # Average Territorial Kick Metres
            home_terr_metres = distance_avg(''.join(home_df['Territorial Kick'].astype(str).to_list()).replace('0',''))
            opp_terr_metres = distance_avg(''.join(opponent_df['Territorial Kick'].astype(str).to_list()).replace('0',''))
            
            # Number of Territorial Kicks
            home_so_num = len(''.join(home_df['Straight Out Kick'].astype(str).to_list()).replace('0',''))
            opp_so_num = len(''.join(opponent_df['Straight Out Kick'].astype(str).to_list()).replace('0',''))
            # Average Straight Out Kicks
            home_so_metres = distance_avg(''.join(home_df['Straight Out Kick'].astype(str).to_list()).replace('0',''))
            opp_so_metres = distance_avg(''.join(opponent_df['Straight Out Kick'].astype(str).to_list()).replace('0',''))
            
            def pct(val, decimals=0):
                if val is None or pd.isna(val):
                    return 0
                return f"{val:.{decimals}f}%"
            metric_kpi= {
                '':[home_team, team],
                'Scores' : [home_scores, opp_scores],
                'Tries' : [home_tries, opp_tries],
                'Penalties' : [home_penalties, opp_penalties],
                'Pass accuracy': [pct(home_pass_acc), pct(opp_pass_acc)],
                 'Tackle completion': [pct(home_tackle_comp), pct(opp_tackle_comp)],
                  'Lineout success': [ pct(home_lineout_succ), pct(opp_lineout_succ)],
                  'Scrum success': [pct(home_scrum_succ), pct(opp_scrum_succ)],
                   'Penalties':[home_df['Penalty For'].sum(), opponent_df['Penalty For'].sum()],
                   'Turnover':[home_df['Turnover'].sum(), opponent_df['Turnover'].sum()],
                   '22 Entries':[home_df['22 Entries For'].sum(), opponent_df['22 Entries For'].sum()],
                   'Number of Carries':[home_df['Carries'].sum(), opponent_df['Carries'].sum()],
                   'Average Carry Metres':[f'{home_carry_metres:.1f}m', f'{opp_carry_metres:.1f}m'],
                   'Number of Territorial Kicks':[home_terr_num, opp_terr_num],
                    'Average Territorial Kicks metres':[f'{home_terr_metres:.1f}m', f'{opp_terr_metres:.1f}m'],
                   'Number of Straight Out Kicks':[home_so_num, opp_so_num],
                   'Average Straight Out Kicks metres':[f'{home_so_metres:.1f}m', f'{opp_so_metres:.1f}m'],
                   # 'Kick Metres':[],
            }
            #                                 hasClicked = card(title="Game Statistics",
            #                                                   text = [
            #                                                             f"{v[0]:<50}  {k:>200}   {v[1]:>50}"
            #                                                             for k, v in metric_kpi.items()
            #                                                         ]
            # ,
            #                                                  )
            st.markdown("""
                        <style>
                            .match-card {
                                background: linear-gradient(90deg, #c0392b, #7b0000);
                                padding: 10px 14px;          /* ⬅ reduced */
                                border-radius: 10px;
                                margin: 10px 0;              /* ⬅ reduced */
                                display: flex;
                                justify-content: space-between;
                                align-items: center;
                            }
                            
                            /* Score boxes */
                            .stat-box {
                                background: black;
                                color: white;
                                font-size: 26px;             /* ⬅ reduced */
                                font-weight: 800;
                                padding: 6px 12px;           /* ⬅ reduced */
                                border-radius: 6px;
                                min-width: 70px;             /* ⬅ reduced */
                                text-align: center;
                            }
                            
                            /* VERSUS text */
                            .versus {
                                color: white;
                                font-size: 14px;             /* ⬅ reduced */
                                letter-spacing: 2px;         /* ⬅ tighter */
                                font-weight: 700;
                            }
                            
                            /* Section title (Penalty Count, etc.) */
                            .section-title {
                                text-align: center;
                                font-size: 18px;             /* ⬅ reduced */
                                font-weight: 800;
                                margin: 8px 0;               /* ⬅ reduced */
                            }
                            
                            /* Header */
                            .header-title {
                                text-align: center;
                                font-size: 30px;             /* ⬅ reduced */
                                font-weight: 900;
                            }
                            
                            .header-sub {
                                text-align: center;
                                font-size: 20px;             /* ⬅ reduced */
                                font-weight: 900;
                                color: #8b0000;
                            }
            
                            .text {
                                font-size: 14px;
                                color: #888;
                            }
                            </style>
            
                        """, unsafe_allow_html=True)
            st.markdown(f"""
                        <div class="header-title">MATCH STAT</div>
                        <div class="header-sub">{home_team} VS {team}</div>
                        <div class="text">{date}</div>
                        """, unsafe_allow_html=True)
            
            def vs_bar(title, left, right):
                st.markdown(f"""
                <div class="section-title">{title}</div>
                <div class="match-card">
                    <div class="stat-box">{left}</div>
                    <div class="versus">VERSUS</div>
                    <div class="stat-box">{right}</div>
                </div>
                """, unsafe_allow_html=True)
            for title,metric in metric_kpi.items():
                vs_bar(title,metric[0],metric[1])
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
                
                if '22 Entries For' in home_df.columns:
                    entry22 = home_df['22 Entries For'].sum()
                    con22r = (len(home_df[home_df['Event'] == 'T'])/ home_df['22 Entries For'].sum()) *100
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
            
                carry_distribution = state_distribution(''.join(home_df['AVG metres'].astype('str').to_list()).replace('0',''))
                df = pd.DataFrame(carry_distribution.items())
                df.columns = ['Distance', 'Number']
                st.subheader('Number of Carry metres')
                st.table(df.sort_index())
                st.markdown(f'Carry sequences showed {combined_attack_interpretation(
                    build_transition_matrix(opponent_df['AVG metres'],''.join(home_df['AVG metres'].astype('str').to_list()).replace('0',''))['Mean Transition Probability'],
                    build_transition_matrix(opponent_df['AVG metres'],''.join(home_df['AVG metres'].astype('str').to_list()).replace('0',''))['Predictability of Sequence']
                )}')    
                
            
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
                    avg_m = str(round(opponent_df['AVG metres'].apply(distance_avg).mean(), 2)) + ' mean'
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
                
                if '22 Entries For' in opponent_df.columns:
                    entry22 = opponent_df['22 Entries For'].sum()
                    con22r = (len(opponent_df[opponent_df['Event'] == 'T'])/ opponent_df['22 Entries For'].sum()) *100
                    convert22.append(con22r)
                    conversionrate22 = str(round(sum(convert22) /len(convert22), 2)) + '%'
                else:
                    entry22 = 'No data'
                    conversionrate22 = 'No data'
                kpi = {
            'Tackles' : {'Total tackles' :total_tackles,
                     'Tackle completion' : tackle_success},
            'Ball Carries': {'Opposition Total Carries': total_carries,
                         'Opposition Average Carry metres': avg_m},
            # 'Metres Gained' : {'Dropped balls': [dropped_balls, difference_dropped_balls]
            #                   'Negative Carries': [negative_carries, difference_negative_carries]},
            'Defensive Work Rate' : {'Opposition Total Line Breaks': line_breaks,
                         'Opposition Complete Phases until Turnover': phases},
            '22 Entries' : {'Opposition Total 22 Entries': entry22,
                       'Opposition Gold Zone Conversion Rate': conversionrate22}
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
            
                
                st.markdown(f'Carry sequences showed {combined_attack_interpretation(
                    build_transition_matrix(opponent_df['AVG metres'],''.join(opponent_df['AVG metres'].astype('str').to_list()).replace('0',''))['Mean Transition Probability'],
                    build_transition_matrix(opponent_df['AVG metres'],''.join(opponent_df['AVG metres'].astype('str').to_list()).replace('0',''))['Predictability of Sequence']
                )}')    
                
        if segments == 'Match Report':
                for n in range(len(home_df)):
                    if home_df['Event'].iloc[n] == 'T':
                        event = st.checkbox(f'Try by {home_team}', key=f"try_{home_team}_{n}")
                    elif opponent_df['Event'].iloc[n] == 'T':
                         event = st.checkbox(f'Try by {team}', key=f"try_{team}_{n}")
                    elif home_df['Event'].iloc[n] == 'P':
                        event = st.checkbox(f'Penalty by {home_team}', key=f"try_{home_team}_{n}")
                    elif opponent_df['Event'].iloc[n] == 'P':
                         event = st.checkbox(f'Penalty by {team}', key=f"try_{team}_{n}")
                    else:
                        if (home_df.iloc[n] != home_df.iloc[-1]).any():
                            event = st.checkbox('Halftime', key=f"try_{team}_{n}")
                        else:
                             event = st.checkbox('Fulltime', key=f"try_{team}_{n}")
                            
                    if event:
                        time = get_time(home_df['Time'].iloc[n])
                        st.write(f'Duration : {time}' if time != None else 'Data yet to be recorded' )
                        #Pass accuracy
                        home_pass_acc = (home_df['Complete Pass'].iloc[n]/(home_df['Complete Pass'].iloc[n] + home_df['Incomplete Pass'].iloc[n])) * 100
                        opp_pass_acc =(opponent_df['Complete Pass'].iloc[n]/(opponent_df['Complete Pass'].iloc[n] + opponent_df['Incomplete Pass'].iloc[n])) * 100
                        #Tackle completion
                        home_tackle_comp = (home_df['Complete Tackle'].iloc[n]/(home_df['Complete Tackle'].iloc[n] + home_df['Incomplete Tackle'].iloc[n])) * 100
                        opp_tackle_comp = (opponent_df['Complete Tackle'].iloc[n]/(opponent_df['Complete Tackle'].iloc[n] + opponent_df['Incomplete Tackle'].iloc[n])) * 100
                        #Lineout success
                        home_lineout_succ = (home_df['Lineout won'].iloc[n]/(home_df['Lineout won'].iloc[n] + home_df['Lineout lost'].iloc[n])) * 100
                        opp_lineout_succ = (opponent_df['Lineout won'].iloc[n]/(opponent_df['Lineout won'].iloc[n] + opponent_df['Lineout lost'].iloc[n])) * 100
                        #Scrum success
                        home_scrum_succ = (home_df['Scrum won'].iloc[n]/(home_df['Scrum won'].iloc[n] + home_df['Scrum lost'].iloc[n])) * 100
                        opp_scrum_succ = (opponent_df['Scrum won'].iloc[n]/(opponent_df['Scrum won'].iloc[n] + opponent_df['Scrum lost'].iloc[n]))* 100

                         # Average Carry Metres
                        home_carry_metres = distance_avg(home_df['AVG metres'].iloc[n])
                        opp_carry_metres = distance_avg(opponent_df['AVG metres'].iloc[n])
    
                        # Number of Territorial Kicks
                        home_terr_num = [len(home_df['Territorial Kick'].iloc[n]) if home_df['Territorial Kick'].iloc[n] != 0 else 0]
                        opp_terr_num = [len(opponent_df['Territorial Kick'].iloc[n]) if opponent_df['Territorial Kick'].iloc[n] != 0 else 0]
                        # Average Territorial Kick Metres
                        home_terr_metres = distance_avg(home_df['Territorial Kick'].iloc[n])
                        opp_terr_metres = distance_avg(opponent_df['Territorial Kick'].iloc[n])
    
                        # Number of Territorial Kicks
                        home_so_num = [len(home_df['Straight Out Kick'].iloc[n]) if home_df['Straight Out Kick'].iloc[n] != 0 else 0]
                        opp_so_num = [len(opponent_df['Straight Out Kick'].iloc[n]) if opponent_df['Straight Out Kick'].iloc[n] != 0 else 0]
                        # Average Straight Out Kicks
                        home_so_metres = distance_avg(home_df['Straight Out Kick'].iloc[n])
                        opp_so_metres = distance_avg(opponent_df['Straight Out Kick'].iloc[n])
                        def pct(val, decimals=0):
                            if val is None or pd.isna(val):
                                return 0
                            return f"{val:.{decimals}f}%"
                        metric_kpi= {
                            '':[home_team, team],
                            'Pass accuracy': [pct(home_pass_acc), pct(opp_pass_acc)],
                             'Tackle completion': [pct(home_tackle_comp or 0), pct(opp_tackle_comp)],
                              'Lineout success': [ pct(home_lineout_succ), pct(opp_lineout_succ)],
                              'Scrum success': [pct(home_scrum_succ), pct(opp_scrum_succ)],
                               'Penalties':[home_df['Penalty For'].iloc[n], home_df['Penalty For'].iloc[n]],
                               'Turnover':[home_df['Turnover'].iloc[n], opponent_df['Turnover'].iloc[n]],
                               '22 Entries':[home_df['22 Entries For'].iloc[n], home_df['22 Entries For'].iloc[n]],
                               'Number of Carries':[home_df['Carries'].iloc[n], opponent_df['Carries'].iloc[n]],
                            'Average Carry Metres':[f'{home_carry_metres:.1f}m', f'{opp_carry_metres:.1f}m'],
                           'Number of Territorial Kicks':[home_terr_num, opp_terr_num],
                            'Average Territorial Kicks metres':[f'{home_terr_metres:.1f}m', f'{opp_terr_metres:.1f}m'],
                           'Number of Straight Out Kicks':[home_so_num, opp_so_num],
                           'Average Straight Out Kicks metres':[f'{home_so_metres:.1f}m', f'{opp_so_metres:.1f}m'],
                               # 'Carry Metres':[],
                               # 'Number of Kicks':[home_df['Turnover'].iloc[n], opponent_df['Turnover'].iloc[n]],
                               # 'Kick Metres':[],
                        }
                        df = pd.DataFrame(metric_kpi).T.reset_index()
                        df.columns = ["Metric", "Home", "Opp"]
                        df_long = df.melt(id_vars="Metric", var_name="Team", value_name="Value")
                        pd.set_option('display.colheader_justify', 'center')
                        st.markdown(
                            df[["Home", "Metric", "Opp"]]
                            .to_html(index=False, justify="center"),
                            unsafe_allow_html=True
                        )

                        st.subheader('')

        if segments == 'Analyses':

            carry_distribution_h = state_distribution(''.join(home_df['AVG metres'].astype('str').to_list()).replace('0',''))
            carry_distribution_a = state_distribution(''.join(opponent_df['AVG metres'].astype('str').to_list()).replace('0',''))
            dfch = pd.DataFrame(carry_distribution_h.items(), columns=['Ranges','Carries'])
            dfca = pd.DataFrame(carry_distribution_a.items(), columns=['Ranges','Carries'])
            st.subheader('Carry Metres')
            st.table(dfch.merge(dfca, on='Ranges', suffixes=['_boro','_opponents']))
            
            terr_k_distribution_h = state_distribution(''.join(home_df['Territorial Kick'].astype('str').to_list()).replace('0',''))
            terr_k_distribution_a = state_distribution(''.join(opponent_df['Territorial Kick'].astype('str').to_list()).replace('0',''))
            dftkh = pd.DataFrame(terr_k_distribution_h.items(), columns=['Ranges','Territorial Kicks'])
            dftka = pd.DataFrame(terr_k_distribution_a.items(), columns=['Ranges','Territorial Kicks'])
            st.subheader('Territorial Kick Metres')
            st.table(dftkh.merge(dftka, on='Ranges', suffixes=['_boro','_opponents']))
            
            so_k_distribution_h = state_distribution(''.join(home_df['Straight Out Kick'].astype('str').to_list()).replace('0',''))
            so_k_distribution_a = state_distribution(''.join(opponent_df['Straight Out Kick'].astype('str').to_list()).replace('0',''))
            dfsokh = pd.DataFrame(so_k_distribution_h.items(), columns=['Ranges','Straight Out Kicks'])
            dfsoka = pd.DataFrame(so_k_distribution_a.items(), columns=['Ranges','Straight Out Kicks'])
            st.subheader('Straight Out Kick Metres')
            st.table(dfsokh.merge(dfsoka, on='Ranges', suffixes=['_boro','_opponents']))
            
            #st.table(dfa)
            pick_team = st.pills("",[home_team, team])
            home_df['Event_Impact'] = home_df['Event'].apply(lambda x: event_values.get(x))
            home_df['Score_Before'] = home_df['Event_Impact'].cumsum().shift(1).fillna(0)
            opponent_df['Event_Impact'] = opponent_df['Event'].apply(lambda x: event_values.get(x))
            opponent_df['Score_Before'] = opponent_df['Event_Impact'].cumsum().shift(1).fillna(0)
            home_features = home_df.drop(['Event','Event_Impact'], axis=1)
            opponent_features = opponent_df.drop(['Event','Event_Impact'], axis=1)
            if 'Time' in home_df.columns:
                home_features['Game Time'] = home_features['Time'].cumsum()
            else:
                home_features['Time'] = 0
                home_features['Game Time'] = 0
            if 'Time' in opponent_features.columns:
                opponent_features['Game Time'] = opponent_features['Time'].cumsum()
            else:
                opponent_features['Time'] = 0
                opponent_features['Game Time'] = 0
            home_features['Transition_Probability'] = home_features['AVG metres'].apply(lambda x:build_transition_matrix(home_features['AVG metres'], seq=x)['Mean Transition Probability'])
            home_features['Sequence_Predictability'] = home_features['AVG metres'].apply(lambda x:build_transition_matrix(home_features['AVG metres'], seq=x)['Predictability of Sequence'])
            opponent_features['Transition_Probability'] = opponent_features['AVG metres'].apply(lambda x:build_transition_matrix(home_df['AVG metres'], seq=x)['Mean Transition Probability'])
            opponent_features['Sequence_Predictability'] = opponent_features['AVG metres'].apply(lambda x:build_transition_matrix(home_df['AVG metres'], seq=x)['Predictability of Sequence'])
            # Convert pass,tackle,lineout and scrums to percentage to capture efficiency of the numbers
            # Pass accuracy
            home_features['Pass Accuracy'] = home_features['Complete Pass']/(home_features['Complete Pass'] + home_features['Incomplete Pass'])
            opponent_features['Pass Accuracy'] = opponent_features['Complete Pass']/(opponent_features['Complete Pass'] + opponent_features['Incomplete Pass'])
            
            # Tackle completion
            home_features['Tackle Completion'] = home_features['Complete Tackle']/(home_features['Complete Tackle'] + home_features['Incomplete Tackle'])
            opponent_features['Tackle Completion'] = opponent_features['Complete Tackle']/(opponent_features['Complete Tackle'] + opponent_features['Incomplete Tackle'])
            
            # Lineout success 
            home_features['Lineout Success'] = home_features['Lineout won']/(home_features['Lineout won'] + home_features['Lineout lost'])
            opponent_features['Lineout Success'] = opponent_features['Lineout won']/(opponent_features['Lineout won'] + opponent_features['Lineout lost'])
            
            # Scrum success
            home_features['Scrum Success'] = home_features['Scrum won']/(home_features['Scrum won'] + home_features['Scrum lost'])
            opponent_features['Scrum Success'] = opponent_features['Scrum won']/(opponent_features['Scrum won'] + opponent_features['Scrum lost'])
            
            # Add relevant columns
            # ***list = ['Line Breaks', 'Mean Transition Probability', 'Opponent line breaks', 'Phases for opponents to lose ball' , 'Straight Out Kicks Number', 'Territorial Kicks Number']***
            # Line Breaks
            home_features['Offensive Line Breaks'] = home_features['AVG metres'].apply(count_line_breaks)
            opponent_features['Offensive Line Breaks'] = opponent_features['AVG metres'].apply(count_line_breaks)
            
            # Phases to loss of ball
            # home_features['Offensive Phases'] = 
            # opponent_features['Offensive Phases'] =
            
            # Opponent line breaks
            home_features['Defensive Line Breaks'] = opponent_features['AVG metres'].apply(count_line_breaks)
            opponent_features['Defensive Line Breaks'] = home_features['AVG metres'].apply(count_line_breaks)
            
            #Phases for opponents to lose ball
            # home_features['Defensive Phases'] = 
            # opponent_features['Defensive Phases'] =
            
            #Straight Out Kick Number
            home_features['Number of Straight Out Kicks'] = home_features['Straight Out Kick'].apply(lambda x: len(list(x)) if x != 0 else 0)
            opponent_features['Number of Straight Out Kicks'] = opponent_features['Straight Out Kick'].apply(lambda x: len(list(x)) if x != 0 else 0)

            #Territorial Kicks
            home_features['Number of Territorial Kicks'] = home_features['Territorial Kick'].apply(lambda x: len(list(x)) if x != 0 else 0)
            opponent_features['Number of Territorial Kicks'] = opponent_features['Territorial Kick'].apply(lambda x: len(list(x)) if x != 0 else 0)

            import hashlib

            def hash_sequence(seq):
                if seq != 0:
                    s = str(seq)
                    return int(hashlib.md5(s.encode()).hexdigest(), 16) % (10**8)
                else:
                    return 0
            
            #Convert to a number sequence
               #  Carries
            home_features['AVG metres'] = home_features['AVG metres'].apply(numeric_sequence).apply(hash_sequence)
            opponent_features['AVG metres'] = home_features['AVG metres'].apply(numeric_sequence).apply(hash_sequence)
               # Straight Out Kicks
            home_features['Straight Out Kick'] = home_features['Straight Out Kick'].apply(numeric_sequence).apply(hash_sequence)
            opponent_features['Straight Out Kick'] = opponent_features['Straight Out Kick'].apply(numeric_sequence).apply(hash_sequence)
               #  Territorial Kick
            home_features['Territorial Kick'] = home_features['Territorial Kick'].apply(numeric_sequence).apply(hash_sequence)
            opponent_features['Territorial Kick'] = opponent_features['Territorial Kick'].apply(numeric_sequence).apply(hash_sequence)
            
            home_features_ml1 = home_features.drop(['Complete Pass', 'Incomplete Pass', 'Complete Tackle', 'Incomplete Tackle','Lineout won','Lineout lost', 'Scrum won', 'Scrum lost'], axis=1).fillna(0)
            opponent_features_ml1 = opponent_features.drop(['Complete Pass', 'Incomplete Pass', 'Complete Tackle', 'Incomplete Tackle','Lineout won','Lineout lost', 'Scrum won', 'Scrum lost'], axis=1).fillna(0)

        
            if pick_team == home_team:
                range_columns=['Transition_Probability', 'Pass Accuracy','Tackle Completion', 'Lineout Success', 'Scrum Success']
                arbitrary_columns=['Penalty For','Penalty Against', 'Knock-on', 'Forward', 'Turnover', 'Time', 'Carries', '22 Entries For', '22 Entries Against', 'Offensive Line Breaks', 'Defensive Line Breaks','Number of Straight Out Kicks', 'Number of Territorial Kicks','Game Time' , 'Score_Before']
                from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, Normalizer, StandardScaler, RobustScaler
                from sklearn.compose import ColumnTransformer
                from sklearn.pipeline import Pipeline,make_pipeline
                
                from sklearn.ensemble import RandomForestClassifier
                from sklearn.base import clone
                
                model = RandomForestClassifier(n_estimators=500, random_state=42)
                range_processor = Pipeline(
                                    steps=[('MInMax', MinMaxScaler())
                                          ])
                arbitrary_processor = Pipeline(
                                    steps=[('robust', RobustScaler())
                                          ])
                ct1 = ColumnTransformer(
                    [("Minmax", range_processor, range_columns),
                     ('robust', arbitrary_processor, arbitrary_columns)],
                        remainder="passthrough")
                
                rugby_pipeline = make_pipeline(
                    ct1,
                    model
                )
                t_model = clone(rugby_pipeline).fit(home_features_ml1, (home_df['Event'] == 'T').astype('int'))
                c_model = clone(rugby_pipeline).fit(home_features_ml1, (home_df['Event'] == 'C').astype('int'))

                t_feature_names = t_model.named_steps['columntransformer'].get_feature_names_out()
                c_feature_names = c_model.named_steps['columntransformer'].get_feature_names_out()
                
                #st.write(f'{t_model.named_steps}')
                t_importances = pd.Series(
                    t_model.named_steps['randomforestclassifier'].feature_importances_,
                    index=t_feature_names
                ).sort_values(ascending=False)
                t_importances.index = t_importances.index.str.split('__').str[-1]


                # st.header('Rank of feature importance to scoring a try.')
                # st.table(t_importances.index.head(5))
                c_importances = pd.Series(
                    c_model.named_steps['randomforestclassifier'].feature_importances_,
                    index=c_feature_names
                ).sort_values(ascending=False)
                c_importances.index = c_importances.index.str.split('__').str[-1]
                # st.header('Rank of feature importance to conceding a try.')
                # st.table(c_importances.index.head(5))
                
            if pick_team == team:
                range_columns=['Transition_Probability', 'Pass Accuracy','Tackle Completion', 'Lineout Success', 'Scrum Success']
                arbitrary_columns=['Penalty For','Penalty Against', 'Knock-on', 'Forward', 'Turnover', 'Time', 'Carries', '22 Entries For', '22 Entries Against', 'Offensive Line Breaks', 'Defensive Line Breaks','Number of Straight Out Kicks', 'Number of Territorial Kicks','Game Time' ]
                from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, Normalizer, StandardScaler, RobustScaler
                from sklearn.compose import ColumnTransformer
                from sklearn.pipeline import Pipeline,make_pipeline
                
                from sklearn.ensemble import RandomForestClassifier
                from sklearn.base import clone
                from sklearn.inspection import permutation_importance
                
                model = RandomForestClassifier(n_estimators=500, random_state=42)
                range_processor = Pipeline(
                                    steps=[('MInMax', MinMaxScaler())
                                          ])
                arbitrary_processor = Pipeline(
                                    steps=[('robust', RobustScaler())
                                          ])
                ct1 = ColumnTransformer(
                    [("Minmax", range_processor, range_columns),
                     ('robust', arbitrary_processor, arbitrary_columns)],
                        remainder="passthrough")
                
                rugby_pipeline = make_pipeline(
                    ct1,
                    model
                )
                t_model = clone(rugby_pipeline).fit(opponent_features_ml1, (opponent_df['Event'] == 'T').astype('int'))
                c_model = clone(rugby_pipeline).fit(opponent_features_ml1, (opponent_df['Event'] == 'C').astype('int'))

                t_feature_names = t_model.named_steps['columntransformer'].get_feature_names_out()
                c_feature_names = c_model.named_steps['columntransformer'].get_feature_names_out()
                
                # Feature Importance
                t_importances = pd.Series(
                    t_model.named_steps['randomforestclassifier'].feature_importances_,
                    index=t_feature_names
                ).sort_values(ascending=False)
                t_importances.index = t_importances.index.str.split('__').str[-1]
                c_importances = pd.Series(
                    c_model.named_steps['randomforestclassifier'].feature_importances_,
                    index=c_feature_names
                ).sort_values(ascending=False)
                c_importances.index = c_importances.index.str.split('__').str[-1]
                # st.header('Rank of feature importance to scoring a try.')
                # st.table(t_importances.head(5).index)
                
                # st.header('Rank of feature importance to conceding a try.')
                # st.table(c_importances.head(5).index)

                # Permutation importance
                
