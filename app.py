import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import pandas as pd

st.set_page_config(
    page_title="H4B S3 Certificates",
    page_icon=":trophy:"
)

def draw_text_on_image(name, team, name_y, team_y, font_path, font_size, text_color, template):
    draw = ImageDraw.Draw(template)
    font = ImageFont.truetype(font_path, font_size)

    name_bbox = draw.textbbox((0, 0), name, font=font)
    team_bbox = draw.textbbox((0, 0), team, font=font)
    
    name_width = name_bbox[2] - name_bbox[0]
    team_width = team_bbox[2] - team_bbox[0]
    
    image_width = template.width

    name_position = ((image_width - name_width) / 2, name_y)
    team_position = ((image_width - team_width) / 2, team_y)

    draw.text(name_position, name, font=font, fill=text_color)
    draw.text(team_position, team, font=font, fill=text_color)

    img_buffer = io.BytesIO()
    template.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    return img_buffer

st.subheader("Hack4Bengal S3 Certificate Generator")

user_type = st.selectbox("Choose whether you are a Participant, Core Team Member, Evangelist, or H4B Award Winner", 
                         ["Participant", "Core Team Member", "Evangelist", "H4B Award Winner"],
                         key="user_type_selector")

participants_df = pd.DataFrame()
core_df = pd.DataFrame()
evangelists_df = pd.DataFrame()
winners_df = pd.DataFrame()

if user_type == "Participant":
    try:
        participants_df = pd.read_csv("participants.csv")
    except FileNotFoundError:
        st.error("participants.csv file not found.")
    if not participants_df.empty:
        participants_df['team_clean'] = participants_df['team'].str.lower().str.replace(' ', '')
    name_input = st.selectbox("Enter Participant's Name", options=participants_df['name'], key="participant_name_selector")
    team_input = st.selectbox("Select Team Name", options=participants_df['team'].unique(), key="participant_team_selector")
    template_path = "certificate-participation.png"

elif user_type == "Core Team Member":
    try:
        core_df = pd.read_csv("core.csv")
    except FileNotFoundError:
        st.error("core.csv file not found.")
    name_input = st.selectbox("Select Core Team Member", options=core_df['name'], key="core_team_name_selector")
    team_input = core_df.loc[core_df['name'] == name_input, 'team'].values[0]
    gender = core_df.loc[core_df['name'] == name_input, 'gender'].values[0]
    template_path = "core-m.png" if gender == 'm' else "core-f.png"

elif user_type == "Evangelist":
    try:
        evangelists_df = pd.read_csv("evangelist.csv")
    except FileNotFoundError:
        st.error("evangelist.csv file not found.")
    name_input = st.selectbox("Select Evangelist", options=evangelists_df['name'], key="evangelist_name_selector")
    team_input = evangelists_df.loc[evangelists_df['name'] == name_input, 'team'].values[0]
    gender = evangelists_df.loc[evangelists_df['name'] == name_input, 'gender'].values[0]
    template_path = "ev-m.png" if gender == 'm' else "ev-f.png"

elif user_type == "H4B Award Winner":
    try:
        winners_df = pd.read_csv("winners.csv")
    except FileNotFoundError:
        st.error("winners.csv file not found.")
    name_input = st.selectbox("Enter Winner's Name", options=winners_df['name'], key="winner_name_selector")
    team_input = st.selectbox("Select Team Name", options=winners_df['team'].unique(), key="winner_team_selector")
    if not winners_df[(winners_df['name'] == name_input) & (winners_df['team'] == team_input)].empty:
        category = winners_df.loc[(winners_df['name'] == name_input) & (winners_df['team'] == team_input), 'category'].values[0]
        if category == 'Gold':
            template_path = "certificate-gold.png"
        elif category == 'Silver':
            template_path = "certificate-silver.png"
        elif category == 'Bronze':
            template_path = "certificate-bronze.png"
    else:
        st.warning("No matching record found for the selected name and team.")
        template_path = None

font_size = 93
font_family = "Montserrat"
font_weight = "SemiBold"
font_paths = {
    "Montserrat": {
        "Black": "./Montserrat/static/Montserrat-Black.ttf",
        "SemiBold": "./Montserrat/static/Montserrat-SemiBold.ttf",
        "Bold": "./Montserrat/static/Montserrat-Bold.ttf"
    },
    "Roboto": {
        "Black": "./Roboto/Roboto-Black.ttf",
        "SemiBold": "./Roboto/Roboto-SemiBold.ttf",
        "Bold": "./Roboto/Roboto-Bold.ttf"
    }
}
font_path = font_paths[font_family][font_weight]
text_color = "#ffffff"

if template_path:
    template = Image.open(template_path)

img_buffer = None
file_name = ""

if name_input and template_path:
    name_input = name_input.title()
    if user_type == "Participant":
        if not participants_df.empty and ((participants_df['name'].str.lower().str.replace(' ', '') == name_input.lower().replace(' ', '')) & 
                                          (participants_df['team_clean'] == team_input.lower().replace(' ', ''))).any():
            img_buffer = draw_text_on_image(name_input, team_input, 628, 974, font_path, font_size, text_color, template)
            file_name = f"Hack4Bengal_Season_3_Participation_{name_input}_{team_input}.png"
        else:
            st.warning("Details do not match any record in the CSV. Please check your details.")
    else:
        img_buffer = draw_text_on_image(name_input, team_input, 628, 974, font_path, font_size, text_color, template)
        file_name = f"Hack4Bengal_Season_3_{user_type.replace(' ', '_')}_{name_input}.png"
    
    if img_buffer:
        st.image(img_buffer, caption=f"Generated Certificate for {name_input}, {team_input}")
        st.download_button(
            label="Download Certificate",
            data=img_buffer,
            file_name=file_name,
            mime="image/png"
        )
else:
    if user_type != "H4B Award Winner" or (user_type == "H4B Award Winner" and template_path):
        st.error("Please select a name.")
