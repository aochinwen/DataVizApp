import streamlit as st
import pandas as pd
import numpy as np 
import pydeck as pdk
import plotly.express as px
#import plotly.graph_objects as go
from datetime import time
from pydeck.types import String



st.title("Petuum Data Visualisation")
st.markdown("This dashboard visualise Petuum resource management data")

token1="sk.eyJ1IjoicmF5MTExMzIwMDIiLCJhIjoiY2twZ2R4cThiMDh1YTJycGJtMzFzdDc5OCJ9.2gfPdQ7o0YSNn8ToxKgaQw"
token2="pk.eyJ1IjoicmF5MTExMzIwMDIiLCJhIjoiY2tvY3kwb3Y5MmliZDJub24wdnpjMTB5NiJ9.kPPmudTylSbhH27w2lwsoQ"
data_url=("https://docs.google.com/spreadsheets/d/e/2PACX-1vSbAVatpnRxlm3_zbMF-fSYlRh2GU-jgcSqlzgKXS-bHvh0mLVzn-PArjj3QcqAiof1oTR3_3BqNXMp/pub?output=xlsx")
xls= pd.ExcelFile("https://docs.google.com/spreadsheets/d/e/2PACX-1vSbAVatpnRxlm3_zbMF-fSYlRh2GU-jgcSqlzgKXS-bHvh0mLVzn-PArjj3QcqAiof1oTR3_3BqNXMp/pub?output=xlsx")
stand_url=("https://docs.google.com/spreadsheets/d/e/2PACX-1vQE-ZDG4s9XU3Eaiz5KBqnEiFT2Bxl3Cb9ACXJTWcfmbU2R4CXtsW45z7vohy4YiXMCjjpmbleci2N8/pub?output=xlsx")
icon_url=("https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/icon-atlas.png")
map_styles=['mapbox://styles/ray11132002/ckph07pq60bd417phjepn5sc3','open_street_map']
@st.cache(allow_output_mutation=True, persist=False)



def load_data(time_period):
	data = pd.read_excel(data_url, time_period, parse_dates=True)
	lowercase = lambda x: str(x).lower() ##convert to lowercase
	data.rename(lowercase, axis='columns', inplace=True)
	data["stand"] = data["stand"].astype(str)
	return data


def load_stand():
	stand_pt = pd.read_excel(stand_url)
	lowercase = lambda x: str(x).lower() ##convert to lowercase
	stand_pt.rename(lowercase, axis='columns', inplace=True)
	return stand_pt


time_period = st.sidebar.selectbox("data sheet to open", xls.sheet_names)
data = load_data(time_period)
stand_pt = load_stand()
stand_pt["stand name"] = stand_pt["stand name"].astype(str)

data_length = len(data["disrupted"])
x=0
while x < data_length:
	#st.write(data["disrupted"][x])
	if data["disrupted"][x] != "0":
		#st.write(data["stand"][x])
		stand_pt.loc[data["stand"][x] == stand_pt["stand name"], "disrupted"]="1"
		x += 1
	else:
		x += 1

maps_colors_list = ["green","red"]
stand_pt["disrupted"] = stand_pt["disrupted"].astype(str)

maps = px.scatter_mapbox(
	stand_pt, 
	lat='latitude', 
	lon='longitude', 
	hover_name="stand name", 
	color="disrupted",
	zoom=13, 
	height=600,
	)


expander_map = st.beta_expander("Expand Map Options", expanded=False)
with expander_map:
	"Options"
	if st.checkbox("show raw stand information", False):
		st.write(stand_pt[['stand name','longitude','latitude','disrupted']])
# map_tilt=st.sidebar.slider ("map rotation", 0, 360, value=0)
# map_pitch=st.sidebar.slider ("map viewing angle", 0, 60, value=25)
stand_size=st.sidebar.slider("size of stand point", 0,10, value=5)
	# st.selectbox("map styles",())

maps.update_layout(mapbox_style='mapbox://styles/ray11132002/ckph07pq60bd417phjepn5sc3', mapbox_accesstoken=token2)
maps.update_layout(autosize=True, height=800)
maps.update_layout(margin=dict(l=5,r=5,b=5))
maps.update_layout( legend=dict(
	yanchor ='top',
	y=0.99,
	xanchor ='left',
	x=0.01
	))
# maps.update_mapboxes(pitch=map_pitch, bearing=map_tilt)
st.plotly_chart(maps, use_container_width=True)

total_disrupted = sum(list(map(int,data['disrupted'])))
st.markdown("in total **%i** stands disrupted" % (total_disrupted))

st.header("Aircraft Stand Allocation Map")

data["disrupted"] = data["disrupted"].astype(str)

config = dict({

	'scrollZoom': False, 
	'displayModeBar':True,
	'modeBarButtonsToRemove' : ['zoom2d','select2d','lasso2d','pan'],
	#'dragmode': ['pan']
})

fig = px.timeline(
	data, x_start='start_time', 
	x_end="end_time", 
	y="stand", 
	color = "disrupted", 
	color_discrete_sequence=["green", "red"],
	hover_data=["stand","start_time","end_time","flt"], 
	labels={"normal", "disrupted"}
	#texttemplate = "%{label}",
	#textposition = "inside"

)

annots =  [dict(x='start_time',y='stand',text="flt", align='center', showarrow=False, font=dict(color='white'))]

fig.update_yaxes(autorange="reversed")
#fig.layout.yaxis.fixedrange = True
fig.update_layout(
	title="Petuum Data" + " " + time_period,
	autosize=True, 
	#width=1000, 
	height=3000,
	dragmode = 'pan',
	annotations = annots,
)
fig.layout.xaxis.fixedrange = True


#now = datetime.now()
#t0 = now.strftime(%H:%M)

t0=pd.to_datetime(2019_05_13_06, format='%Y%m%d%H')
#fig.add_vline(x=t0, line_width=3, line_dash='dash', line_color='red')


st.plotly_chart(fig, config=config)
#st.write(fig)


# def refresher(seconds):
#     while True:
#         mainDir = os.path.dirname(__file__)
#         filePath = os.path.join(mainDir, 'dummy.py')
#         with open(filePath, 'w') as f:
#             f.write(f'# {randint(0, 10000)}')
#         time.sleep(seconds)

# refresher(60)
