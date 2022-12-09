To open the website, double click any html link in the folder.

- Map Page
Currently only 3 routes display the full monday-sunday wait times which includes:

-- Silver Route --
CRI (Far left)
Union East (Middle, slight right)
-- Green Route --
North Deck (Very Top)

- Chart Page
The chart page uses streamlit and is hosted locally through a terminal prompt
Install Requirements:
pip install streamlit
pip install openpyxl
pip install matplotlib

To run type "streamlit run TransitData.py" into the terminal

The Netowork URL will display, ensure that the url in line 26 of "charts.html" matches this url.
If it doesn't, stop running streamlit, change the url in line 26, then run again

The chart page should now be functioning.
