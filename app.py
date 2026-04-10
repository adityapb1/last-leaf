import streamlit as st
import os
import json
import random
from PIL import Image
import torch
import torch.nn as nn
from torchvision import models, transforms

# -------------------------------------------------------------
# Configuration & Setup
# -------------------------------------------------------------
st.set_page_config(
    page_title="PhytoScan AI",
    page_icon="🌿",
    layout="centered"
)

MODEL_PATH = 'plant_disease_model.pth'
CLASS_NAMES_PATH = 'class_names.txt'
MOCK_DATA_PATH = 'plant_data.json'

# Attempt to load PyTorch Model (st.cache_resource ensures it only happens once)
@st.cache_resource
def load_model():
    if os.path.exists(MODEL_PATH) and os.path.exists(CLASS_NAMES_PATH):
        try:
            with open(CLASS_NAMES_PATH, 'r') as f:
                class_names = [line.strip() for line in f.readlines()]
            
            model = models.resnet18(pretrained=False)
            num_ftrs = model.fc.in_features
            model.fc = nn.Linear(num_ftrs, len(class_names))
            
            model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
            model.eval()
            return model, class_names
        except Exception as e:
            st.warning(f"Error loading model weights: {e}")
            return None, None
    else:
        return None, None

model, class_names = load_model()
is_model_loaded = model is not None

# PyTorch Image Transforms
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

@st.cache_data
def load_mock_data():
    if os.path.exists(MOCK_DATA_PATH):
        with open(MOCK_DATA_PATH, 'r') as f:
            return json.load(f)
    return []

mock_data = load_mock_data()

def get_disease_metadata(class_name):
    # Mapping real PyTorch class names to the mock data JSON format
    plant_id = class_name.lower().replace('___', '_').replace(' ', '_')
    for item in mock_data:
        if item['id'] == plant_id:
            return item
    return None

def analyze_image(img):
    if is_model_loaded:
        with torch.no_grad():
            img_rgb = img.convert('RGB')
            input_tensor = transform(img_rgb).unsqueeze(0)
            outputs = model(input_tensor)
            _, preds = torch.max(outputs, 1)
            predicted_class = class_names[preds[0]]
            
        metadata = get_disease_metadata(predicted_class)
        if metadata:
            return metadata
        else:
            return {
                "plant_name": predicted_class.split('___')[0],
                "status": "Healthy" if "healthy" in predicted_class.lower() else "Diseased",
                "disease_name": predicted_class.split('___')[1] if "healthy" not in predicted_class.lower() else None,
                "plant_features": [],
                "symptoms": [f"AI detected: {predicted_class}"],
                "treatment": "Please refer to standard agricultural guidelines."
            }
    else:
        # Mock Simulation
        import time
        time.sleep(1.5) # Simulate processing time
        return random.choice(mock_data) if mock_data else None

# -------------------------------------------------------------
# Streamlit UI
# -------------------------------------------------------------

st.title("🌿 PhytoScan AI")
st.markdown("Snap a photo of a plant leaf and let our AI detect its health, species, and combat diseases.")

if not is_model_loaded:
    st.info("⚠️ **Simulation Mode Active:** The trained AI model (`plant_disease_model.pth`) was not found. Showing simulated mock data. Run `train.py` on your machine and place the `.pth` file here to enable real AI.")

# Tabs for input methods
tab1, tab2 = st.tabs(["📸 Use Camera", "📂 Upload File"])

captured_image = None

with tab1:
    camera_photo = st.camera_input("Take a picture of the leaf")
    if camera_photo:
        captured_image = Image.open(camera_photo)

with tab2:
    uploaded_file = st.file_uploader("Upload a leaf image", type=['png', 'jpg', 'jpeg'])
    if uploaded_file:
        captured_image = Image.open(uploaded_file)
        st.image(captured_image, caption="Uploaded Leaf", use_column_width=True)

# -------------------------------------------------------------
# Results Section
# -------------------------------------------------------------
if captured_image:
    st.markdown("---")
    st.header("🔬 AI Analysis Results")
    
    with st.spinner('Analyzing cellular structure...'):
        result = analyze_image(captured_image)
        
    if result:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader(f"Plant: {result['plant_name']}")
            if result['status'] == 'Healthy':
                st.success(f"Status: {result['status']}")
            else:
                st.error(f"Status: {result['status']}")
                
        with col2:
            if result['status'] == 'Diseased':
                st.warning(f"**Diagnosis:** {result['disease_name']}")
                
        # Features
        with st.expander("🌱 Plant Features", expanded=True):
            for feature in result.get('plant_features', []):
                st.markdown(f"- {feature}")
                
        # Symptoms & Treatment
        if result['status'] == 'Diseased':
            st.error("🩺 Detected Symptoms")
            for symptom in result.get('symptoms', []):
                st.markdown(f"- {symptom}")
                
            if result.get('treatment'):
                st.info(f"💊 **Treatment Recommendation:**\n\n{result['treatment']}")
    else:
        st.error("No data found or mock database empty.")
