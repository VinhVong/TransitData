import streamlit as st
import pandas as pd
import altair as alt
import datetime
import matplotlib.pyplot as plt

@st.cache(allow_output_mutation=True)
def load_data():
    df = pd.read_excel('TransportData/niner-transit-data/2018-2019 Stop Data PART 1.xlsx')
    return df

st.set_page_config(page_title="Transit Data",layout='wide')

# load the data
df = load_data()

df['month'] = pd.DatetimeIndex(df['Date']).month
df_on = df[df['On off'].str.contains('on')]
df_off = df[df['On off'].str.contains('off')]

# choose the sources of interest
routes = ['All Routes'] + [route for route in df.Route.unique()]
option = st.sidebar.selectbox('Choose a Route', routes)

#create charts

if option == 'All Routes':
    st.title('Transportation Data')
    df_group1 = df_on.groupby(['Route','month'])['Count'].sum().reset_index()
    df_bar = df_on[['Route','Date','Count','month']]
    df_mean1 = df_on.groupby(['Route','month'])['Count'].mean().reset_index()
    
    if st.sidebar.checkbox('Total Passageners'):
        total_chart = alt.Chart(df_bar).mark_bar().encode(
            x=alt.X('month', title = 'Month'),
            y=alt.Y('Count', title = '# of passageners'),
            color='Route:N',
            column='Route'
        ).properties(
            title = 'Total Passengers per Month',
            height = 300,
            width = 100
        )
        
        bar_chart_mean = alt.Chart(df_mean1).mark_bar().encode(
            x=alt.X('Route',sort = '-y', title = 'Routes'),
            y=alt.Y('Count', title = 'Average # of Passageners'),
            color = 'Route:N',
            column = 'month',
        ).properties(
            title = 'Average Passengers getting on',
            height = 300,
            width = 100
        ).interactive()
        
        st.write(total_chart)
        st.write(bar_chart_mean)
    
    df_stop1 = df_on.groupby(['Stop'])['Count'].sum().reset_index()
    df_mean_stop1 = df_on.groupby(['Stop'])['Count'].mean().reset_index()

    clickon=alt.selection(type='single', empty='all', fields=['Stop'])
    
    if st.sidebar.checkbox('Stops Passengers Getting On'):
        chart_stops_on1 = alt.Chart(df_mean_stop1).mark_arc().encode(
            theta=alt.Theta(field='Count', type="quantitative"),
            color=alt.condition(clickon, 'Stop:N', alt.value('lightgray'), legend=None),
            text='Stop:N'
        ).add_selection(
            clickon
        ).properties(
            title = 'Average Passengers for Each Stop',
            height = 300,
            width = 600
        ).interactive()
        
        chart_stop_on2 =alt.Chart(df_stop1).mark_bar().encode(
            x=alt.X('Stop',sort='-y', title='Transit Stops'),
            y=alt.Y('Count', title='Total # of Passengers at Stop'),
            color=alt.condition(clickon, 'Stop:N', alt.value('lightgray'), legend=None) 
        ).add_selection(
            clickon
        ).properties(
            title = 'total Passengers Getting On at Each Stop',
            height = 300,
            width = 600
        ).interactive()
        
        st.altair_chart((chart_stop_on2 | chart_stops_on1), use_container_width = True)
    
    df_stop2 = df_off.groupby(['Stop'])['Count'].sum().reset_index()
    df_mean_stop2 = df_off.groupby(['Stop'])['Count'].mean().reset_index()

    clickon1=alt.selection(type='single', empty='all', fields=['Stop'])
    
    if st.sidebar.checkbox('Stops on Passengers Getting Off'):
        chart_stops_off1 = alt.Chart(df_mean_stop2).mark_arc().encode(
            theta=alt.Theta(field='Count', type="quantitative"),
            color=alt.condition(clickon1, 'Stop:N', alt.value('lightgray'), legend=None),
            text='Stop:N'
        ).add_selection(
            clickon1
        ).properties(
            title = 'Average Passengers off for Each Stop',
            height = 300,
            width = 550
        ).interactive()
        
        chart_stop_off2 =alt.Chart(df_stop2).mark_bar().encode(
            x=alt.X('Stop',sort='-y', title='Transit Stops'),
            y=alt.Y('Count', title='Total # at Stop'),
            color=alt.condition(clickon1, 'Stop:N', alt.value('lightgray'), legend=None)
        ).add_selection(
            clickon1
        ).properties(
            title = 'Total Passengers Getting off at Each Stop',
            height = 300,
            width = 550
        ).interactive()
        
        st.write(chart_stops_off1 | chart_stop_off2)

else:
    st.title(option + ' Route Data')
    df_route = df_on[df_on['Route'].str.contains(option)]
    df_route_off = df_off[df_off['Route'].str.contains(option)]

    chart1 = alt.Chart(df_route).mark_line().encode(
        x=alt.X('Date', title='Months'),
        y=alt.Y('Count', title='# of Passageners')
    ).properties(
        title=option + ' Route',
        height= 300,
        width=1000,
    ).interactive()

    st.write(chart1, use_container_width=True)

    df_sum = df_route.groupby(['month'])['Count'].sum().reset_index()
    df_mean = df_route.groupby(['month'])['Count'].mean().reset_index()
    
    if st.sidebar.checkbox('Total/Average'):
        chart_sum = alt.Chart(df_sum).mark_bar().encode(
            x=alt.X('month', title='Months'),
            y=alt.Y('Count', title='# of Passageners')
        ).properties(
            title=option + ' Route Total Passengers On',
            height = 300,
            width = 250
        )

        chart_mean = alt.Chart(df_mean).mark_bar().encode(
            x=alt.X('month', title='Months'),
            y=alt.Y('Count', title='# of Passageners')
        ).properties(
            title=option + ' Route Average Passengers On',
            height = 300,
            width = 250
        )

        st.write(chart_sum | chart_mean)

    df_stop_sum = df_route.groupby(['Stop'])['Count'].sum().reset_index()
    df_stop_mean = df_route.groupby(['Stop'])['Count'].mean().reset_index()

    if st.sidebar.checkbox('Totat/Average Passengers getting On at Stop'):
        chart_stop = alt.Chart(df_stop_sum).mark_bar().encode(
            x=alt.X('Stop',sort=alt.EncodingSortField('Count', op='min', order='descending'), title = 'Transit Stops'),
            y=alt.Y('Count', title = 'Total # at Stop')
        ).properties(
            title = option +' Route Total Passengers Getting On',
            height = 300,
            width = 550
        )

        chart_stop_mean = alt.Chart(df_stop_mean).mark_bar().encode(
            x=alt.X('Stop',sort='-y', title = 'Transit Stops'),
            y=alt.Y('Count', title = 'Average # of passageners at Stop')
        ).properties(
            title = option +' Route Average getting On',
            height = 300,
            width = 550
        )

        st.write(chart_stop | chart_stop_mean)

    df_stop_sum1 = df_route_off.groupby(['Stop'])['Count'].sum().reset_index()
    df_stop_mean1 = df_route_off.groupby(['Stop'])['Count'].mean().reset_index()    
    
    if st.sidebar.checkbox('Totat/Average Passengers getting Off at Stop'):
        chart_stop1 = alt.Chart(df_stop_sum1).mark_bar().encode(
            x=alt.X('Stop',sort=alt.EncodingSortField('Count', op='min', order='descending'), title = 'Transit Stops'),
            y=alt.Y('Count', title = 'Total # at Stop')
        ).properties(
            title = option +' Route Total Passengers Getting Off',
            height = 300,
            width = 550
        )

        chart_stop_mean1 = alt.Chart(df_stop_mean1).mark_bar().encode(
            x=alt.X('Stop',sort='-y', title = 'Transit Stops'),
            y=alt.Y('Count', title = 'Average # of passageners at Stop')
        ).properties(
            title = option +' Route Average getting Off',
            height = 300,
            width = 550
        )

        st.write(chart_stop1 | chart_stop_mean1)