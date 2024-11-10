import os
import base64
import streamlit as st
import gzip
import json

from cognite.client import CogniteClient, ClientConfig
from cognite.client.credentials import OAuthInteractive, OAuthClientCredentials
from streamlit_mubadala_threedviewer import streamlit_mubadala_threedviewer

from models.viewer_data import ViewerData
from models.deck import Deck
from models.beacon import Beacon
from models.camera import Camera
from pandas import DataFrame

def assign_auth(project_name):
        
    if project_name == "slb-test":        
        tenant_id = os.environ.get("CDF_SLBTEST_TENANT_ID") 
        client_id = os.environ.get("CDF_SLBTEST_CLIENT_ID") 
        client_secret = os.environ.get("CDF_SLBTEST_CLIENT_SECRET")
        cluster = os.environ.get("CDF_SLBTEST_CLUSTER")     
    elif project_name == "petronas-pma-dev" or project_name == "petronas-pma-playground":
        tenant_id = os.environ.get("CDF_PETRONASPMA_TENANT_ID") 
        cluster = os.environ.get("CDF_PETRONASPMA_CLUSTER") 
        client_id = os.environ.get("CDF_PETRONASPMA_CLIENT_ID") 
        client_secret = ""
    elif project_name == "hess-malaysia-dev":
        tenant_id = os.environ.get("CDF_HESSDEV_TENANT_ID") 
        client_id = os.environ.get("CDF_HESSDEV_CLIENT_ID") 
        client_secret = os.environ.get("CDF_HESSDEV_CLIENT_SECRET") 
        cluster = os.environ.get("CDF_HESSDEV_CLUSTER") 
    elif project_name == "hess-malaysia-prod":
        tenant_id = os.environ.get("CDF_HESSPROD_TENANT_ID") 
        client_id = os.environ.get("CDF_HESSPROD_CLIENT_ID") 
        client_secret = os.environ.get("CDF_HESSPROD_CLIENT_SECRET") 
        cluster = os.environ.get("CDF_HESSPROD_CLUSTER")     
    elif project_name == "mubadala-dev":
        tenant_id = os.environ.get("CDF_MUBADALADEV_TENANT_ID") 
        cluster = os.environ.get("CDF_MUBADALADEV_CLUSTER")
        client_id = os.environ.get("CDF_MUBADALADEV_CLIENT_ID") 
        client_secret = os.environ.get("CDF_MUBADALADEV_CLIENT_SECRET") 
           
    base_url = f"https://{cluster}.cognitedata.com"
    scopes = [f"{base_url}/.default"]
    
    return {
        "tenant_id": tenant_id, 
        "client_id": client_id, 
        "client_secret": client_secret, 
        "cluster": cluster,
        "base_url": base_url,
        "project_name": project_name,
        "scopes": scopes
    }

def interactive_client(project_name):
    
    auth_data: any = assign_auth(project_name)
    
    """Function to instantiate the CogniteClient, using the interactive auth flow"""
    return CogniteClient(
        ClientConfig(
            client_name=auth_data['project_name'],
            project=auth_data['project_name'],
            base_url=auth_data['base_url'],
            credentials=OAuthInteractive(
                authority_url=f"https://login.microsoftonline.com/{auth_data['tenant_id']}",
                client_id=auth_data['client_id'],
                scopes=auth_data['scopes'],
            ),
        )
    )

def client_credentials(project_name):
    
    auth_data = assign_auth(project_name)

    credentials = OAuthClientCredentials(
        token_url=f"https://login.microsoftonline.com/{auth_data['tenant_id']}/oauth2/v2.0/token", 
        client_id=auth_data['client_id'], 
        client_secret= auth_data['client_secret'],
        scopes=auth_data['scopes']
    )

    config = ClientConfig(
        client_name=auth_data['project_name'],
        project=auth_data['project_name'],
        base_url=auth_data['base_url'],
        credentials=credentials,
    )
    client = CogniteClient(config)

    return client

def connect(project_name):
    auth = assign_auth(project_name=project_name)  
    if auth["client_secret"] == "":
        return interactive_client(project_name)
    else:
        return client_credentials(project_name)

st.set_page_config(layout='wide')
st.subheader("Streamlit Slb ThreeDViewer Examples")

client: CogniteClient = connect("mubadala-dev")

image_id: int = None
imagelist_df: DataFrame = None
viewer_data: ViewerData = None

def get_image_id_list():
    # get few image list for example test
    image_list = client.files.list(mime_type="image/jpeg", limit=10)
    image_list_df = image_list.to_pandas()
    # st.write(image_list_df)
    return image_list_df
        
def render_selectbox() -> int:
    options = imagelist_df["id"].tolist()
    image_id = st.selectbox(label="Image ID List", options=options)
    return image_id

def get_image_from_id(image_id) -> str:
    image_bytes = client.files.download_bytes(id=image_id)
    base64_str = base64.b64encode(image_bytes).decode("utf-8")
    return base64_str

def get_deck_info(viewer_data: ViewerData) -> ViewerData:    
    deck = Deck(id=12345, name="Heli Deck", image_id=1234567890)    
    deck.beacons = deck.add_beacon(beacon=Beacon(id=12345, name="Beacon 1", location=[0, 0, 0]))    
    viewer_data.add_deck(deck=deck)        
    return viewer_data

def get_deck_info_by_external_id(deck_external_id: str) -> dict[str, any]:    
    query = """
        query GetDeckInfoByDeckExternalID {
            listDeck(filter: {externalId: {eq: "%s"}}) {
                items {
                externalId
                name
                planeColor
                planeHeight
                planePosition {
                    items {
                    x
                    y
                    z
                    }
                }
                planeRotation
                planeThickness
                planeWidth
                imageId
                beacons {
                    items {
                    color
                    deviceLocation {
                        items {
                        coordinates {
                            items {
                            x
                            y
                            z
                            }
                        }
                        }
                    }
                    fadeSpeed
                    heightSegment
                    macAddress
                    maxScale
                    name
                    radius
                    signalRadius
                    widthSegment
                    zone
                    }
                }
                imageIdStr
                }
            }
        }
    """ % (deck_external_id)
    print(query)
    deck_info = client.data_modeling.graphql.query(
        id=("threed_viewer", "PlatformDeck", "8"),
        query=query
    )
    return deck_info

def render_viewer(image_id: int):      
    global viewer_data    
    viewer_data = ViewerData(name="3D Viewer", height=800, deck_image_id=image_id)
    deck_image_str = get_image_from_id(2798951298776205)
    events = streamlit_mubadala_threedviewer(height=800, deck_image=deck_image_str, data=viewer_data.to_json())
    return events

imagelist_df = get_image_id_list()
image_id = render_selectbox()
events = render_viewer(image_id=image_id)
# st.write(events)

# get decks, beacons and camera data
viewer_data = get_deck_info(viewer_data)
# print(viewer_data.to_json())
deck_info = get_deck_info_by_external_id("deck_main")
print(deck_info)
