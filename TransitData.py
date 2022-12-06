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
df['hours'] = df['Time'].astype(str).str[:2]
df_on = df[df['On off'].str.contains('on')]
df_off = df[df['On off'].str.contains('off')]

# choose the sources of interest
routes = ['All Routes'] + [route for route in df.Route.unique()]
option = st.sidebar.selectbox('Choose a Route', routes)

#create charts

if option == 'All Routes':
    st.title('Transportation Data')

    df1 = df_on.groupby(['month','hours','Route','Stop'])['Count'].sum().reset_index()
    option_month = st.multiselect('Choose month',df1['month'].unique(), default=None)
    option_route = st.multiselect('Choose Route',df1['Route'].unique(), default=None)
    source_month = df1[df1['month'].isin(option_month)]
    source1 = source_month[source_month['Route'].isin(option_route)]

    df_group1 = source1.groupby(['Route','month'])['Count'].sum().reset_index()
    df_mean1 = source1.groupby(['Route','month'])['Count'].mean().reset_index()
    
    if st.sidebar.checkbox('Total Passageners'):
        total_chart = alt.Chart(df_group1).mark_bar().encode(
            x=alt.X('Route', sort = '-y', title = 'Route'),
            y=alt.Y('Count', title = '# of passageners'),
            color='Route:N',
            column='month'
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

    hour_sum = source1.groupby(['Route','hours','month'])['Count'].sum().reset_index()
    hour_mean = source1.groupby(['Route','hours','month'])['Count'].mean().reset_index()

    if st.sidebar.checkbox('Hours'):
        hour_chart = alt.Chart(hour_sum).mark_bar().encode(
            x=alt.X('hours', title = 'Hours'),
            y=alt.Y('Count', title = '# of passageners'),
            color='Route:N',
            column='month',
            tooltip = ['Route','Count']
        ).properties(
            title = 'Total Passengers per Month',
            height = 300,
            width = 200
        )
        
        st.write(hour_chart)


    
    df_stop1 = source1.groupby(['Route','Stop'])['Count'].sum().reset_index()
    df_mean_stop1 = source1.groupby(['Route','Stop'])['Count'].mean().reset_index()

    clickon=alt.selection(type='single', empty='all', fields=['Stop'])
    
    if st.sidebar.checkbox('Stops Passengers Getting On'):
        chart_stops_on1 = alt.Chart(df_mean_stop1).mark_bar().encode(
            x=alt.X('Stop',sort='-y', title='Transit Stops'),
            y=alt.Y('Count', title='Total # of Passengers at Stop'),
            color=alt.condition(clickon, 'Stop:N', alt.value('lightgray'), legend=None),
        ).add_selection(
            clickon
        ).properties(
            title = 'Average Passengers for Each Stop',
            height = 300,
            width = 550
        ).interactive()
        
        chart_stop_on2 =alt.Chart(df_stop1).mark_bar().encode(
            x=alt.X('Stop',sort='-y', title='Transit Stops'),
            y=alt.Y('Count', title='Total # of Passengers at Stop'),
            color=alt.condition(clickon, 'Stop:N', alt.value('lightgray'), legend=None) 
        ).add_selection(
            clickon
        ).properties(
            title = 'Total Passengers Getting On at Each Stop',
            height = 300,
            width = 550
        ).interactive()
        
        st.altair_chart((chart_stop_on2 | chart_stops_on1), use_container_width = True)

    df2 = df_off.groupby(['month','hours','Route','Stop'])['Count'].sum().reset_index()
    source_month1 = df2[df2['month'].isin(option_month)]
    source2 = source_month1[source_month1['Route'].isin(option_route)]
    
    df_stop2 = source2.groupby(['Route','Stop'])['Count'].sum().reset_index()
    df_mean_stop2 = source2.groupby(['Route','Stop'])['Count'].mean().reset_index()

    clickon1=alt.selection(type='single', empty='all', fields=['Stop'])
    
    if st.sidebar.checkbox('Stops on Passengers Getting Off'):
        chart_stops_off1 = alt.Chart(df_mean_stop2).mark_bar().encode(
            x=alt.X('Stop',sort='-y', title='Transit Stops'),
            y=alt.Y('Count', title='Total # at Stop'),
            color=alt.condition(clickon1, 'Stop:N', alt.value('lightgray'), legend=None),
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
        
        st.write(chart_stop_off2 | chart_stops_off1)

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

    df3 = df_route.groupby(['month','hours','Route','Stop'])['Count'].sum().reset_index()
    option_month = st.multiselect('Choose month',df3['month'].unique(), default=df3['month'].unique())
    source_month = df3[df3['month'].isin(option_month)]

    df_sum = source_month.groupby(['month','hours'])['Count'].sum().reset_index()
    df_mean = source_month.groupby(['month','hours'])['Count'].mean().reset_index()
    
    if st.sidebar.checkbox('Total/Average'):
        chart_sum = alt.Chart(df_sum).mark_bar().encode(
            x=alt.X('hours', title='Hours'),
            y=alt.Y('Count', title='# of Passageners'),
            column = 'month',
            tooltip = ['Count']
        ).properties(
            title=option + ' Route Total Passengers On',
            height = 300,
            width = 200
        )

        chart_mean = alt.Chart(df_mean).mark_bar().encode(
            x=alt.X('hours', title='Hours'),
            y=alt.Y('Count', title='# of Passageners'),
            column = 'month',
            tooltip = ['Count']
        ).properties(
            title=option + ' Route Average Passengers On',
            height = 300,
            width = 200
        )

        st.write(chart_sum)
        st.write(chart_mean)

    df_stop_sum = source_month.groupby(['Stop'])['Count'].sum().reset_index()
    df_stop_mean = source_month.groupby(['Stop'])['Count'].mean().reset_index()

    if st.sidebar.checkbox('Totat/Average Passengers getting On at Stop'):
        chart_stop = alt.Chart(df_stop_sum).mark_bar().encode(
            x=alt.X('Stop',sort=alt.EncodingSortField('Count', op='min', order='descending'), title = 'Transit Stops'),
            y=alt.Y('Count', title = 'Total # at Stop'),
            tooltip = ['Count']
        ).properties(
            title = option +' Route Total Passengers Getting On',
            height = 300,
            width = 550
        )

        chart_stop_mean = alt.Chart(df_stop_mean).mark_bar().encode(
            x=alt.X('Stop',sort='-y', title = 'Transit Stops'),
            y=alt.Y('Count', title = 'Average # of passageners at Stop'),
            tooltip=['Count']
        ).properties(
            title = option +' Route Average getting On',
            height = 300,
            width = 550
        )

        st.write(chart_stop | chart_stop_mean)

    df4 = df_route_off.groupby(['month','hours','Route','Stop'])['Count'].sum().reset_index()
    source_month1 = df4[df4['month'].isin(option_month)]

    df_stop_sum1 = source_month1.groupby(['Stop'])['Count'].sum().reset_index()
    df_stop_mean1 = source_month1.groupby(['Stop'])['Count'].mean().reset_index()    
    
    if st.sidebar.checkbox('Totat/Average Passengers getting Off at Stop'):
        chart_stop1 = alt.Chart(df_stop_sum1).mark_bar().encode(
            x=alt.X('Stop',sort=alt.EncodingSortField('Count', op='min', order='descending'), title = 'Transit Stops'),
            y=alt.Y('Count', title = 'Total # at Stop'),
            tooltip = ['Count']
        ).properties(
            title = option +' Route Total Passengers Getting Off',
            height = 300,
            width = 550
        )

        chart_stop_mean1 = alt.Chart(df_stop_mean1).mark_bar().encode(
            x=alt.X('Stop',sort='-y', title = 'Transit Stops'),
            y=alt.Y('Count', title = 'Average # of passageners at Stop'),
            tooltip = ['Count']
        ).properties(
            title = option +' Route Average getting Off',
            height = 300,
            width = 550
        )

        st.write(chart_stop1 | chart_stop_mean1)