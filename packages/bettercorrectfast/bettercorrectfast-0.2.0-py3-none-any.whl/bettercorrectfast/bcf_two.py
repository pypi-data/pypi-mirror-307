# bettercorrectfast/bcf_two.py
# -*- coding: utf-8 -*-

# A fork for the undocumented IfcOpenShell wrapper
# https://github.com/IfcOpenShell/IfcOpenShell/blob/v0.8.0/src/bcf/bcf/v2/bcfxml.py

import uuid

from .bcf.v2 import bcfxml as BCF # TODO the ifcopenshell part is messing up, duplicate the libraries locally instead
from .bcf.v2 import topic as TOPIC  # TODO the ifcopenshell part is messing up, duplicate the libraries locally instead
from .bcf.v2 import visinfo as VIS  # TODO the ifcopenshell part is messing up, duplicate the libraries locally instead
from .bcf.v2 import model as MDL  # TODO the ifcopenshell part is messing up, duplicate the libraries locally instead
from .bcf.v2.model import visinfo as vi

from pathlib import Path

def create(title="BetterCorrectFast: Check this out!", description="Automatically generated topic by BetterCorrectFast", image_filepath=None, project_name="", ifc_guids = []): # TODO come up with a better alias # TODO come up with better placeholder values
    
    # Create the elements
    bcf = BCF.BcfXml().create_new(project_name)
    topic = _get_topic(title, description, image_filepath, ifc_guids)
    
    # Add the elements
    bcf.topics[topic.guid] = topic

    return bcf

def save(bcf, filepath):
    bcf.save(filepath)


def _get_topic(title, description, image_filepath, ifc_guids, author="BetterCorrectFast", topic_type="Issue", topic_status="Open"): # TODO come up with better placeholder values

    # Create the elements
    topic = TOPIC.TopicHandler().create_new(
        title=title,
        description=description,
        author=author,
        topic_type=topic_type,
        topic_status=topic_status
    )

    visualization_info_handler = _get_visualization_info_handler(image_filepath, ifc_guids) # TODO insert the image filepath here # TODO add user input for the picture
    
    # Add the elements
    topic.add_visinfo_handler(visualization_info_handler, snapshot_filename="snapshot.png")
 
    return topic

def _get_visualization_info_handler(image_filepath, ifc_guids):
    
    visualization_info = _get_visualization_info(ifc_guids)
    
    image_filepath = image_filepath if image_filepath is not None else _get_default_snapshot_path()
    image_bytes = _get_image_bytes_from_filepath(image_filepath)

    visualization_info_handler = VIS.VisualizationInfoHandler(visualization_info, snapshot=image_bytes )
    
    return visualization_info_handler

def _get_image_bytes_from_filepath(filepath):
    try:
        with open(filepath, "rb") as image_file:
            return image_file.read()
    except:
        return None # TODO check if return None is ok to begin with

def _get_visualization_info(ifc_guids):
    
    visualization_info = vi.VisualizationInfo(
        guid=str(uuid.uuid4()),  # Generate a random GUID
        components=VIS.build_components(*ifc_guids),
        perspective_camera=vi.PerspectiveCamera(
            camera_view_point=vi.Point(x=0, y=0, z=0),
            camera_direction=vi.Direction(x=0, y=1, z=0),
            camera_up_vector=vi.Direction(x=0, y=0, z=1),
            field_of_view=60.0,
        )
    )
    
    return visualization_info

def _get_default_snapshot_path(): # TODO might be unsafe if the filepath does not exits
    
    current_file = Path(__file__).resolve()
    snapshot_path = current_file.parent / 'assets' / 'icon.png'

    snapshot_path_exists = snapshot_path.exists()
    print(f"The default snapshot file is being used {'and is located' if snapshot_path_exists else ', but was not found'} at: {snapshot_path}") # User feedback
    
    if not snapshot_path_exists: return None
    return str(snapshot_path)

__all__ = ["create", "save"]  # Specify public API