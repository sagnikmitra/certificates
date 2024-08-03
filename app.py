import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import pandas as pd

st.set_page_config(
    page_title="H4B S3 Certificates",
    page_icon=":trophy:"
)

def draw_text_on_image(name, team, cert_id, name_y, team_y, id_y, font_path, font_size, text_color, template):
    draw = ImageDraw.Draw(template)
    font = ImageFont.truetype(font_path, font_size)
    small_font = ImageFont.truetype(font_path, int(font_size / 3))
    verify_link = f"Certificate Id: {cert_id} Verify at sagnikmitra.com/s3-verify"

    name_bbox = draw.textbbox((0, 0), name, font=font)
    team_bbox = draw.textbbox((0, 0), team, font=font)
    verify_bbox = draw.textbbox((0, 0), verify_link, font=small_font)

    name_width = name_bbox[2] - name_bbox[0]
    team_width = team_bbox[2] - team_bbox[0]
    verify_width = verify_bbox[2] - verify_bbox[0]

    image_width = template.width

    name_position = ((image_width - name_width) / 2, name_y)
    team_position = ((image_width - team_width) / 2, team_y)
    verify_position = ((image_width - verify_width) / 2, id_y)

    draw.text(name_position, name, font=font, fill=text_color)
    draw.text(team_position, team, font=font, fill=text_color)
    draw.text(verify_position, verify_link, font=small_font, fill=text_color)

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
        if not participants_df.empty:
            participants_df['team_clean'] = participants_df['team'].str.lower().str.replace(' ', '')
            name_input = st.selectbox("Enter Participant's Name", options=participants_df['name'].tolist(), key="participant_name_selector")
            team_input = st.selectbox("Select Team Name", options=participants_df['team'].unique(), key="participant_team_selector")
            template_path = "certificate-participation.png"
        else:
            st.error("The participants CSV file is empty.")
    except FileNotFoundError:
        st.error("participants.csv file not found.")

elif user_type == "Core Team Member":
    try:
        core_df = pd.read_csv("core.csv")
        if not core_df.empty:
            name_input = st.selectbox("Select Core Team Member", options=core_df['name'].tolist(), key="core_team_name_selector")
            team_input = st.selectbox("Select Team Name", options=core_df['team'].unique(), key="core_team_team_selector")
            gender = core_df.loc[core_df['name'] == name_input, 'gender'].values[0]
            template_path = "core-m.png" if gender == 'm' else "core-f.png"
        else:
            st.error("The core team CSV file is empty.")
    except FileNotFoundError:
        st.error("core.csv file not found.")

elif user_type == "Evangelist":
    try:
        evangelists_df = pd.read_csv("evangelist.csv")
        if not evangelists_df.empty:
            name_input = st.selectbox("Select Evangelist", options=evangelists_df['name'].tolist(), key="evangelist_name_selector")
            team_input = st.selectbox("Select Team Name", options=evangelists_df['team'].unique(), key="evangelist_team_selector")
            gender = evangelists_df.loc[evangelists_df['name'] == name_input, 'gender'].values[0]
            template_path = "ev-m.png" if gender == 'm' else "ev-f.png"
        else:
            st.error("The evangelist CSV file is empty.")
    except FileNotFoundError:
        st.error("evangelist.csv file not found.")

elif user_type == "H4B Award Winner":
    try:
        winners_df = pd.read_csv("winners.csv")
        if not winners_df.empty:
            name_input = st.selectbox("Enter Winner's Name", options=winners_df['name'].tolist(), key="winner_name_selector")
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
                st.warning("Details do not match any record in the winners CSV. Please check your details.")
        else:
            st.error("The winners CSV file is empty.")
    except FileNotFoundError:
        st.error("winners.csv file not found.")

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

img_buffer = None
cert_location = 1570
if user_type in ["Participant", "Core Team Member", "Evangelist", "H4B Award Winner"]:
    if not participants_df.empty or not core_df.empty or not evangelists_df.empty or not winners_df.empty:
        template = Image.open(template_path)
        cert_id = ""

        if name_input and team_input:
            if user_type == "Participant":
                if not participants_df.empty and ((participants_df['name'].str.lower().str.replace(' ', '') == name_input.lower().replace(' ', '')) & 
                                                  (participants_df['team_clean'] == team_input.lower().replace(' ', ''))).any():
                    cert_id = participants_df.loc[(participants_df['name'].str.lower() == name_input.lower()) & 
                                                  (participants_df['team_clean'] == team_input.lower().replace(' ', '')), 'cert_id'].values[0]
                    if not pd.isna(cert_id):
                        img_buffer = draw_text_on_image(name_input.title(), team_input, cert_id, 628, 974, cert_location, font_path, font_size, text_color, template)
                        file_name = f"Hack4Bengal_Season_3_Participation_{name_input}_{team_input}.png"
                    else:
                        st.error("Certificate ID not found for the participant.")
                else:
                    st.warning("Details do not match any record in the CSV. Please check your details.")
            elif user_type == "Core Team Member":
                if not core_df.empty and ((core_df['name'] == name_input) & (core_df['team'] == team_input)).any():
                    cert_id = core_df.loc[(core_df['name'] == name_input) & (core_df['team'] == team_input), 'cert_id'].values[0]
                    if not pd.isna(cert_id):
                        img_buffer = draw_text_on_image(name_input.title(), team_input, cert_id, 628, 974, cert_location, font_path, font_size, text_color, template)
                        file_name = f"Hack4Bengal_Season_3_Core_Team_Member_{name_input}.png"
                    else:
                        st.error("Certificate ID not found for the core team member.")
                else:
                    st.warning("Details do not match any record in the CSV. Please check your details.")
            elif user_type == "Evangelist":
                if not evangelists_df.empty and ((evangelists_df['name'] == name_input) & (evangelists_df['team'] == team_input)).any():
                    cert_id = evangelists_df.loc[(evangelists_df['name'] == name_input) & (evangelists_df['team'] == team_input), 'cert_id'].values[0]
                    if not pd.isna(cert_id):
                        img_buffer = draw_text_on_image(name_input.title(), team_input, cert_id, 628, 974, cert_location, font_path, font_size, text_color, template)
                        file_name = f"Hack4Bengal_Season_3_Evangelist_{name_input}.png"
                    else:
                        st.error("Certificate ID not found for the evangelist.")
                else:
                    st.warning("Details do not match any record in the CSV. Please check your details.")
            elif user_type == "H4B Award Winner":
                if not winners_df.empty and ((winners_df['name'] == name_input) & (winners_df['team'] == team_input)).any():
                    cert_id = winners_df.loc[(winners_df['name'] == name_input) & (winners_df['team'] == team_input), 'cert_id'].values[0]
                    if not pd.isna(cert_id):
                        img_buffer = draw_text_on_image(name_input.title(), team_input, cert_id, 628, 974, cert_location, font_path, font_size, text_color, template)
                        file_name = f"Hack4Bengal_Season_3_Award_Winner_{name_input}.png"
                    else:
                        st.error("Certificate ID not found for the award winner.")
                else:
                    st.warning("Details do not match any record in the CSV. Please check your details.")
            else:
                st.error("Please select a name and team.")
        else:
            st.error("Please select a name and team.")
        
        if img_buffer:
            st.image(img_buffer, caption=f"Generated Certificate for {name_input}, {team_input}")
            st.download_button(
                label="Download Certificate",
                data=img_buffer,
                file_name=file_name,
                mime="image/png"
            )
    else:
        st.error("Data is not available.")
