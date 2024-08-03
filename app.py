import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import pandas as pd

st.set_page_config(
    page_title="H4B S3 Certificates",
    page_icon=":trophy:"
)

# Function to draw text on the image
def draw_text_on_image(name, team, name_y, team_y, font_path, font_size, text_color, template):
    # Load the certificate template
    draw = ImageDraw.Draw(template)

    # Set the font and size
    font = ImageFont.truetype(font_path, font_size)

    # Calculate the width and height of the text to center it
    name_bbox = draw.textbbox((0, 0), name, font=font)
    team_bbox = draw.textbbox((0, 0), team, font=font)
    
    name_width = name_bbox[2] - name_bbox[0]
    name_height = name_bbox[3] - name_bbox[1]
    team_width = team_bbox[2] - team_bbox[0]
    team_height = team_bbox[3] - team_bbox[1]
    
    # Get the image width
    image_width = template.width

    # Define text position to center it
    name_position = ((image_width - name_width) / 2, name_y)
    team_position = ((image_width - team_width) / 2, team_y)

    # Draw the text
    draw.text(name_position, name, font=font, fill=text_color)
    draw.text(team_position, team, font=font, fill=text_color)

    # Save the edited image to a bytes buffer
    img_buffer = io.BytesIO()
    template.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    return img_buffer


# Streamlit UI
st.subheader("Hack4Bengal S3 Participation Certificate Generator")

# Load participants data from CSV
try:
    participants_df = pd.read_csv("participants.csv")
except FileNotFoundError:
    st.error("participants.csv file not found.")
    participants_df = pd.DataFrame()

# Clean and get unique Team Names
if not participants_df.empty:
    participants_df['team_clean'] = participants_df['team'].str.lower().str.replace(' ', '')
    unique_teams = participants_df['team_clean'].unique()

# Input fields
name_input = st.selectbox("Enter Participant's Name", options=participants_df['name'])
team_input = st.selectbox("Select Team Name", options=participants_df['team'].unique())

# Position and font adjustments
name_y = 628
team_y = 974
font_size = 93

# Font selection
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

# Load the certificate template
template = Image.open("certificate-participation.png")

# Normalize and clean input
name_clean = name_input.lower().replace(' ', '')
team_clean = team_input.lower().replace(' ', '')

# Verify if the entered name and team are in the same row of the CSV
if name_input and team_input:
    if not participants_df.empty and ((participants_df['name'].str.lower().str.replace(' ', '') == name_clean) & (participants_df['team_clean'] == team_clean)).any():
        img_buffer = draw_text_on_image(name_input, team_input, name_y, team_y, font_path, font_size, text_color, template)
        
        st.image(img_buffer, caption="Generated Certificate")

        # Create file name with participant's name and Team Name
        file_name = f"Hack4Bengal_Season_3_Participation_{name_input}_{team_input}.png"
        
        st.download_button(
            label="Download Certificate",
            data=img_buffer,
            file_name=file_name,
            mime="image/png"
        )
    else:
        st.warning("Details do not match any record in the CSV. Please check your details.")
else:
    st.error("Please provide both Name and Team Name.")
