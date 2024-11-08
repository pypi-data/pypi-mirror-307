"""
All the constants and hardcoded stuff.
Update the content of the dictionnary accordingly with the dataset names from the
input configuration file '--config-path'.
"""

from kgforge.core import Resource

# ================== Commons constants ==================

# Allen annotation volume voxels resolution in microns
VOXELS_RESOLUTION = "25"
SPATIAL_UNIT = "um" # µm
entity_type = "Entity"
dataset_type = "Dataset"
subject = {
    "@type": "Subject",
    "species": {
        "@id": "http://purl.obolibrary.org/obo/NCBITaxon_10090",
        "label": "Mus musculus"},
}
atlas_spatial_reference_system_id = (
    "https://bbp.epfl.ch/neurosciencegraph/data/allen_ccfv3_spatial_reference_system") # no need for '_ccfv3', it's unique across all Allen versions

atlas_spatial_reference_system_type = [
    "BrainAtlasSpatialReferenceSystem",
    "AtlasSpatialReferenceSystem",
]
# Link to the spatial ref system
isRegisteredIn = {
    "@id": atlas_spatial_reference_system_id,
    "@type": atlas_spatial_reference_system_type,
}
# Allen annotations
allen_v2 = "ccfv2"
allen_v3 = "ccfv3"
allen_v2_split = allen_v2 + "_l23split"
allen_v3_split = allen_v3 + "_l23split"
# Descriptions
description_ccfv2 = (
    f"original Allen {allen_v2} annotation volume at {VOXELS_RESOLUTION} {SPATIAL_UNIT}"
)
description_ccfv3 = (
    f"original Allen {allen_v3} annotation volume at {VOXELS_RESOLUTION} {SPATIAL_UNIT}"
)
description_hybrid = (
    f"Hybrid annotation volume from {allen_v2} and {allen_v3} at {VOXELS_RESOLUTION} "
    f"{SPATIAL_UNIT}"
)
description_split = "with the isocortex layer 2 and 3 split"
description_barrel = " and barrel split"

description_ccfv2_split = f"{description_ccfv2} {description_split}"
description_ccfv3_split = f"{description_ccfv3} {description_split}"
description_ccfv3_split_barrel = f"{description_ccfv3} {description_split}{description_barrel}"
description_hybrid_split = f"{description_hybrid} {description_split}"

hem_split = f"Hemisphere labelling of the Allen annotation volume at {VOXELS_RESOLUTION} {SPATIAL_UNIT} {description_split}"
hem_v2_split = hem_split.replace("Allen annotation", f"Allen {allen_v2} annotation")
hem_v3_split = hem_split.replace("Allen annotation", f"Allen {allen_v3} annotation")

# Nexus schema
schema_ontology = "https://neuroshapes.org/dash/ontology"
schema_atlasrelease = "https://neuroshapes.org/dash/atlasrelease"
schema_activity = "https://neuroshapes.org/dash/activity"
schema_volumetricdatalayer = "https://neuroshapes.org/dash/volumetricdatalayer"
schema_mesh = "https://neuroshapes.org/dash/brainparcellationmesh"
schema_cellrecord = "https://neuroshapes.org/dash/cellrecordseries"
schema_regionsummary = ""  # https://neuroshapes.org/dash/entity
schema_spatialref = "https://neuroshapes.org/dash/atlasspatialreferencesystem"

# Isocortex layer Nexus UBERON @id_spatial_ref
isocortex_layers = {
    "1": "http://purl.obolibrary.org/obo/UBERON_0005390",
    "2": "http://purl.obolibrary.org/obo/UBERON_0005391",
    "3": "http://purl.obolibrary.org/obo/UBERON_0005392",
    "4": "http://purl.obolibrary.org/obo/UBERON_0005393",
    "5": "http://purl.obolibrary.org/obo/UBERON_0005394",
    "6": "http://purl.obolibrary.org/obo/UBERON_0005395",
}

atlasrelease_types = ["AtlasRelease", "BrainAtlasRelease", entity_type]

# atlasRelease already in Nexus bbp/atlas project
atlasrelease_ccfv2 = {
    "@id": (
        "https://bbp.epfl.ch/neurosciencegraph/data/dd114f81-ba1f-47b1-8900-e497597f06ac"),
    "@type": atlasrelease_types,
}
atlasrelease_ccfv3 = {
    "@id": (
        "https://bbp.epfl.ch/neurosciencegraph/data/831a626a-c0ae-4691-8ce8-cfb7491345d9"),
    "@type": atlasrelease_types,
}
atlasrelease_ccfv2v3 = [atlasrelease_ccfv2, atlasrelease_ccfv3]
atlasrelease_ccfv3_split = {
    "@id": (
        "https://bbp.epfl.ch/neurosciencegraph/data/brainatlasrelease/c96c71a8-4c0d-4bc1-8a1a-141d9ed6693d"
    ),
    "@type": atlasrelease_types,
}
atlasrelease_hybrid_l23split = {
    "@id": (
        "https://bbp.epfl.ch/neurosciencegraph/data/e2e500ec-fe7e-4888-88b9-b72425315dda"
    ),
    "@type": atlasrelease_types,
}

# ================== Ontology constants ==================

hierarchy_dict = {
    "hierarchy_mba": {"name": "hierarchy", "mba_jsonld": ""},
    "hierarchy_l23split": {
        "name": "hierarchy_l23split",
        "label": "AIBS Mouse CCF Atlas parcellation ontology L2L3 split",
        "description": "AIBS Mouse CCF Atlas regions hierarchy tree file including the "
        "split of layer 2 and layer 3",
        "derivation": "http://bbp.epfl.ch/neurosciencegraph/ontologies/mba",
        "mba_jsonld": "mba_hierarchy_l23split",
    },
}

# ================== atlasRelease constants ==================

# Parcellations used by atlasReleases
annot_hybrid = "annotation_hybrid"
annot_hybrid_l23split = "annotation_hybrid_l23split"
annot_v2_l23split = "annotation_"+allen_v2+"_l23split"
annot_v3_l23split = "annotation_"+allen_v3+"_l23split"
annot_v3_l23split_barrel = "annotation_"+allen_v3+"_l23split_barrelsplit"
hem_v2_l23split = "hemispheres_"+allen_v2+"_l23split"
hem_v3_l23split = "hemispheres_"+allen_v3+"_l23split"

# average brain model ccfv3
brainTemplateDataLayer = {
    "@id": "https://bbp.epfl.ch/neurosciencegraph/data/"
    "dca40f99-b494-4d2c-9a2f-c407180138b7",
    "@type": "BrainTemplateDataLayer",
}

atlasrelease_dict = {
    "hybrid_l23split": {
        "name": "Allen Mouse CCF v2-v3 hybrid l2-l3 split",
        "description": "This atlas release uses the brain parcellation resulting of "
        "the hybridation between CCFv2 and CCFv3 and integrating the splitting of "
        "layer 2 and layer 3. The average brain template and the ontology is "
        "common across CCFv2 and CCFv3.",
        "ontology": hierarchy_dict["hierarchy_l23split"],
        "parcellation": annot_hybrid_l23split,
    },
    allen_v3+"_l23split": {
        "name": "Blue Brain Mouse Atlas",  # "Allen Mouse CCF v3 l2-l3 split",
        "description": "This atlas release uses the brain parcellation of CCFv3 (2017) "
        "with the isocortex layer 2 and 3 split. The average brain template and the "
        "ontology is common across CCFv2 and CCFv3.",
        "ontology": hierarchy_dict["hierarchy_l23split"],
        "parcellation": annot_v3_l23split,
    },
}

# ================== VolumetricDataLayer constants ==================

volumetric_type = "VolumetricDataLayer"
ontology_type = "ParcellationOntology"
parcellation_type = "BrainParcellationDataLayer"
parcellationOntology_types = [entity_type, "Ontology", ontology_type]
parcellationVolume_types = [dataset_type, volumetric_type, parcellation_type]
default_sampling_period = 30
default_sampling_time_unit = "ms"
config = {
    "sampling_space_unit": SPATIAL_UNIT,
    "sampling_period": default_sampling_period,
    "sampling_time_unit": default_sampling_time_unit, }

cell_densiry_dsm = "quantity"
me_type = ["NeuronDensity", volumetric_type, "CellDensityDataLayer", "METypeDensity"]
voxel_vol = "intensity"

# ========================= Mesh constants =========================
mesh_type = "Mesh"
# ===================== RegionSummary constants =====================
regionsummary_type = "RegionSummary"
# ==================== CellRecordSeries constants ====================
cellrecord_type = "CellRecordSeries"


def return_spatial_reference(forge):

    spatialref_resource = forge.retrieve(atlas_spatial_reference_system_id + "?rev")
    if not spatialref_resource:
        boundingBox = {
            "@type": "BoundingBox",
            "lowerPoint": {"@type": "Vector3D", "valueX": 0, "valueY": 0, "valueZ": 0},
            "unitCode": SPATIAL_UNIT,
            "upperPoint": {
                "@type": "Vector3D",
                "valueX": 13200,
                "valueY": 8000,
                "valueZ": 11400,
            },
        }
        description = (
            "This spatial reference system describes the space used by Allen "
            "Institute for Brain Science, shared across CCFv1, CCFv2 and CCFv3 in "
            "world coordinates, using micrometer as a spatial unit."
        )
        orientation = (
            {
                "@type": "RotationalMatrix",
                "firstRow": {
                    "@type": "Vector3D",
                    "valueX": 1,
                    "valueY": 0,
                    "valueZ": 0,
                },
                "secondRow": {
                    "@type": "Vector3D",
                    "valueX": 0,
                    "valueY": 1,
                    "valueZ": 0,
                },
                "thirdRow": {
                    "@type": "Vector3D",
                    "valueX": 0,
                    "valueY": 0,
                    "valueZ": 1,
                },
            },
        )
        spatialAxesDirection = {
            "x": "anterior-to-posterior",
            "y": "superior-to-inferior",
            "z": "left-to-right",
        }
        spatialref_resource = Resource(
            type=atlas_spatial_reference_system_type,
            name="Allen Mouse CCF",
            description=description,
            boundingBox=boundingBox,
            orientation=orientation,
            origin={"@type": "Vector3D", "valueX": 0, "valueY": 0, "valueZ": 0},
            spatialAxesDirection=spatialAxesDirection,
            unitCode=SPATIAL_UNIT,
            citation="http://help.brain-map.org/display/mousebrain/API",
        )

    return spatialref_resource


def return_volumetric_dict(volumetric_datasets):
    """
    Parameters:
        volumetric_datasets : Dict containing all the volumetric datasets from the
                            input config file.

    Returns:
        volumetric_dict : Dict containing all the volumetric datasets with their
                        informations.
    """
    # Descriptions for VolumetricDataLayer datasets
    description_dirvectors_ccfv3 = (
        f"3D unit vectors defined over the Original Allen ccfv3 annotation volume "
        f"(spatial resolution of {VOXELS_RESOLUTION} {SPATIAL_UNIT}) and representing "
        "the neuron axone-to-dendrites orientation to voxels from the top regions of "
        "the Isocortex."
    )
    description_orientation = "Quaternions field (w,x,y,z) defined over the"
    description_orientation_end = (
        f"(spatial resolution of {VOXELS_RESOLUTION} {SPATIAL_UNIT}) and representing "
        "the neuron axone-to-dendrites orientation to voxels from the Isocortex region."
    )
    description_orientation_ccfv3 = (
        f"{description_orientation} Original Allen ccfv3 annotation volume "
        f"{description_orientation_end}"
    )
    description_orientation_hybrid = (
        f"{description_orientation} CCF v2-v3 Hybrid annotation volume "
        f"{description_orientation_end}"
    )
    description_PH = (
        "The layers are ordered with respect to depth, which means that the layer "
        "which is the closest from the skull is the first layer (upper layer) and the "
        "deepest one is the last (lower layer)."
    )
    description_PH_ccfv3_split = (
        "Placement hints (cortical distance of voxels to layer boundaries) of the "
        f"Isocortex Layer XX of the {description_ccfv3_split}. {description_PH}"
    )
    description_PH_hybrid_split = (
        "Placement hints (cortical distance of voxels to layer boundaries) of the "
        f"Isocortex Layer XX of the {description_hybrid_split}. {description_PH}"
    )

    derivation_correctednissl = {
        "@type": "Derivation",
        "entity": {
            "@id": "nissl_corrected_volume",
            "@type": "Dataset",
        },
    }

    # Dictionary containing the possible volumetric dataset to push
    linprog = "inhibitory_neuron_densities_linprog_"+allen_v2+"_correctednissl"
    linprog_trans = "inhibitory_neuron_densities_linprog_l23split_transplant_correctednissl"
    preserveprop = "inhibitory_neuron_densities_preserveprop_"+allen_v2+"_correctednissl"
    cell_density = "overall_cell_density_"+allen_v2+"_correctednissl"
    volumes = volumetric_datasets
    try:
        volumetric_dict = {
            "parcellations": {
                f"{volumes[annot_v2_l23split]}": {
                    "name": annot_v2_l23split,
                    "type": parcellationVolume_types,
                    "description": description_ccfv2_split,
                    "atlasrelease": "atlasrelease_"+allen_v3+"split",
                    "voxel_type": "label",
                    "datasamplemodality": "parcellationId",
                },
                f"{volumes[annot_hybrid]}": {
                    "name": annot_hybrid,
                    "type": parcellationVolume_types,
                    "description": f"{description_hybrid}. The version "
                    "replaces the leaf regions in ccfv3 with the leaf region of "
                    +allen_v2+", which have additional levels of hierarchy.",
                    "atlasrelease": atlasrelease_ccfv2v3,
                    "voxel_type": "label",
                    "datasamplemodality": "parcellationId",
                },
                f"{volumes[annot_hybrid_l23split]}": {
                    "name": annot_hybrid_l23split,
                    "type": parcellationVolume_types,
                    "description": description_hybrid_split,
                    "atlasrelease": atlasrelease_hybrid_l23split,
                    "voxel_type": "label",
                    "datasamplemodality": "parcellationId",
                },
                f"{volumes[annot_v3_l23split]}": {
                    "name": annot_v3_l23split,
                    "type": parcellationVolume_types,
                    "description": description_ccfv3_split,
                    "atlasrelease": "atlasrelease_"+allen_v3+"split",
                    "voxel_type": "label",
                    "datasamplemodality": "parcellationId",
                },
                f"{volumes[annot_v3_l23split_barrel]}": {
                    "name": annot_v3_l23split_barrel,
                    "type": parcellationVolume_types,
                    "description": description_ccfv3_split_barrel,
                    "atlasrelease": "atlasrelease_"+allen_v3+"split_barrelsplit",
                    "voxel_type": "label",
                    "datasamplemodality": "parcellationId",
                },
            },
            "hemispheres": {
                f"{volumes[hem_v2_l23split]}": {
                    "name": "hem_v2_l23split",
                    "type": [
                        dataset_type,
                        volumetric_type,
                        "HemisphereAnnotationDataLayer",
                    ],
                    "description": hem_v2_split,
                    "atlasrelease": "atlasrelease_"+allen_v2+"split",
                    "voxel_type": "label",
                    "datasamplemodality": "parcellationId",
                    "derivation": f"{volumes[annot_v2_l23split]}",
                },
                f"{volumes[hem_v3_l23split]}": {
                    "name": "hem_v3_l23split",
                    "type": [
                        dataset_type,
                        volumetric_type,
                        "HemisphereAnnotationDataLayer",
                    ],
                    "description": hem_v3_split,
                    "atlasrelease": "atlasrelease_"+allen_v3+"split",
                    "voxel_type": "label",
                    "datasamplemodality": "parcellationId",
                    "derivation": f"{volumes[annot_v3_l23split]}",
                },
            },
            "cell_orientations": {
                f"{volumes['direction_vectors_isocortex_ccfv3']}": {
                    "name": "direction_vectors_isocortex_ccfv3",
                    "type": [dataset_type, volumetric_type, "CellOrientationField"],
                    "description": description_dirvectors_ccfv3,
                    "atlasrelease": "atlasrelease_"+allen_v3+"split",
                    "voxel_type": "vector",
                    "datasamplemodality": "eulerAngle",
                },
                f"{volumes['cell_orientations_ccfv3']}": {
                    "name": "cell_orientations_ccfv3",
                    "type": [dataset_type, volumetric_type, "CellOrientationField"],
                    "description": description_orientation_ccfv3,
                    "atlasrelease": "atlasrelease_"+allen_v3+"split",
                    "voxel_type": "vector",
                    "datasamplemodality": "quaternion",
                },
                f"{volumes['cell_orientations_hybrid']}": {
                    "name": "cell_orientations_hybrid",
                    "type": [dataset_type, volumetric_type, "CellOrientationField"],
                    "description": description_orientation_hybrid,
                    "atlasrelease": atlasrelease_ccfv2v3,
                    "voxel_type": "vector",
                    "datasamplemodality": "quaternion",
                },
            },
            "placement_hints": {
                f"{volumes['placement_hints_hybrid_l23split']}": {
                    "name": "placement_hints_hybrid_l23split",
                    "type": [dataset_type, volumetric_type, "PlacementHintsDataLayer"],
                    "type_2": [
                        dataset_type,
                        volumetric_type,
                        "PlacementHintsDataReport",
                    ],
                    "description": description_PH_hybrid_split,
                    "atlasrelease": atlasrelease_hybrid_l23split,
                    "datasamplemodality": "distance",
                    "datasamplemodality_2": "mask",
                    "voxel_type": "vector",
                    "voxel_type_2": "label",
                    "suffixe": "CCF v2-v3 Hybrid L23 Split",
                },
                f"{volumes['placement_hints_ccfv3_l23split']}": {
                    "name": "placement_hints_"+allen_v3+"_l23split",
                    "type": [dataset_type, volumetric_type, "PlacementHintsDataLayer"],
                    "type_2": [
                        dataset_type,
                        volumetric_type,
                        "PlacementHintsDataReport",
                    ],
                    "description": description_PH_ccfv3_split,
                    "atlasrelease": "atlasrelease_"+allen_v3+"split",
                    "datasamplemodality": "distance",
                    "datasamplemodality_2": "mask",
                    "voxel_type": "vector",
                    "voxel_type_2": "label",
                    "suffixe": "CCFv3 L23 Split",
                },
            },
            "volume_mask": {
                f"{volumes['brain_region_mask_ccfv3_l23split']}": {
                    "name": "brain_region_mask_"+allen_v3+"_l23split",
                    "type": [dataset_type, volumetric_type, "BrainParcellationMask"],
                    "description": description_ccfv3_split,
                    "atlasrelease": "atlasrelease_"+allen_v3+"split",
                    "voxel_type": "label",
                    "datasamplemodality": "parcellationId",
                    "hierarchy_tag": "hierarchy_l23split",
                    "suffixe": "CCFv3 L23 Split",
                }
            },
            "brain_template": {
                f"{volumes['average_template_25']}": {
                    "name": "average_template_25",
                    "type": [dataset_type, volumetric_type, "BrainTemplateDataLayer"],
                    "description": (
                        "original Allen ccfv3 average template volume at "
                        f"{VOXELS_RESOLUTION} {SPATIAL_UNIT}"
                    ),
                    "atlasrelease": atlasrelease_ccfv3,
                    "voxel_type": voxel_vol,
                    "datasamplemodality": "luminance",
                }
            },
            "cell_densities": {
                f"{volumes['cell_densities_hybrid']}": {
                    "name": "cell_densities_hybrid",
                    "type": [
                        dataset_type,
                        volumetric_type,
                        "CellDensityDataLayer",
                        "GliaCellDensity",
                    ],
                    "description": description_hybrid,
                    "derivation": None,
                    "atlasrelease": atlasrelease_hybrid_l23split,
                    "voxel_type": voxel_vol,
                    "datasamplemodality": cell_densiry_dsm,
                },
                f"{volumes['neuron_densities_hybrid']}": {
                    "name": "neuron_densities_hybrid",
                    "type": [
                        dataset_type,
                        volumetric_type,
                        "CellDensityDataLayer",
                        "GliaCellDensity",
                    ],
                    "description": description_hybrid,
                    "derivation": None,
                    "atlasrelease": atlasrelease_hybrid_l23split,
                    "voxel_type": voxel_vol,
                    "datasamplemodality": cell_densiry_dsm,
                },
                f"{volumes[cell_density]}": {
                    "name": cell_density,
                    "type": [
                        dataset_type,
                        volumetric_type,
                        "CellDensityDataLayer",
                        "GliaCellDensity",
                    ],
                    "description": f"{description_ccfv2}. It has been generated using "
                    "the corrected nissl volume",
                    "derivation": derivation_correctednissl,
                    "atlasrelease": atlasrelease_ccfv2,
                    "voxel_type": voxel_vol,
                    "datasamplemodality": cell_densiry_dsm,
                },
                f"{volumes['cell_densities_ccfv2_correctednissl']}": {
                    "name": "cell_densities_"+allen_v2+"_correctednissl",
                    "type": [
                        dataset_type,
                        volumetric_type,
                        "CellDensityDataLayer",
                        "GliaCellDensity",
                    ],
                    "description": f"{description_ccfv2}. It has been generated using "
                    "the corrected nissl volume",
                    "derivation": f"{volumes[cell_density]}",
                    "atlasrelease": atlasrelease_ccfv2,
                    "voxel_type": voxel_vol,
                    "datasamplemodality": cell_densiry_dsm,
                },
                f"{volumes['neuron_densities_ccfv2_correctednissl']}": {
                    "name": "neuron_densities_"+allen_v2+"_correctednissl",
                    "type": [
                        dataset_type,
                        volumetric_type,
                        "CellDensityDataLayer",
                        "GliaCellDensity",
                    ],
                    "description": f"{description_ccfv2}. It has been generated using "
                    "the corrected nissl volume",
                    "derivation": (
                        f"{volumes['cell_densities_ccfv2_correctednissl']}",
                        "neuron_density.nrrd",
                    ),
                    "atlasrelease": atlasrelease_ccfv2,
                    "voxel_type": voxel_vol,
                    "datasamplemodality": cell_densiry_dsm,
                },
                f"{volumes['glia_cell_densities_l23split_transplant_correctednissl']}": {
                    "name": "glia_cell_densities_l23split_transplant_correctednissl",
                    "type": [
                        dataset_type,
                        volumetric_type,
                        "CellDensityDataLayer",
                        "GliaCellDensity",
                    ],
                    "description": f"{description_ccfv3_split}. It has been generated using "
                    "the corrected nissl volume",
                    "derivation": (
                        f"{volumes['cell_densities_ccfv2_correctednissl']}",
                        "neuron_density.nrrd",
                    ),
                    "atlasrelease": atlasrelease_ccfv3_split,
                    "voxel_type": voxel_vol,
                    "datasamplemodality": cell_densiry_dsm,
                },
                f"{volumes[linprog]}": {
                    "name": linprog,
                    "type": [
                        dataset_type,
                        volumetric_type,
                        "CellDensityDataLayer",
                        "GliaCellDensity",
                    ],
                    "description": f"{description_ccfv2}. It has been generated with "
                    "the corrected nissl volume and using the algorithm linprog",
                    "derivation": (
                        f"{volumes['cell_densities_ccfv2_correctednissl']}",
                        "neuron_density.nrrd",
                    ),
                    "atlasrelease": atlasrelease_ccfv2,
                    "voxel_type": voxel_vol,
                    "datasamplemodality": cell_densiry_dsm,
                },
                f"{volumes[linprog_trans]}": {
                    "name": linprog_trans,
                    "type": [
                        dataset_type,
                        volumetric_type,
                        "CellDensityDataLayer",
                        "GliaCellDensity",
                    ],
                    "description": f"{description_ccfv3_split}. It has been generated with "
                    "the corrected nissl volume and using the algorithm linprog",
                    "derivation": (
                        f"{volumes['cell_densities_ccfv3_correctednissl']}",
                        "neuron_density.nrrd",
                    ),
                    "atlasrelease": atlasrelease_ccfv3_split,
                    "voxel_type": voxel_vol,
                    "datasamplemodality": cell_densiry_dsm,
                },
                f"{volumes[preserveprop]}": {
                    "name": preserveprop,
                    "type": [
                        dataset_type,
                        volumetric_type,
                        "CellDensityDataLayer",
                        "GliaCellDensity",
                    ],
                    "description": f"{description_ccfv2}. It has been generated with "
                    "the corrected nissl volume and using the algorithm "
                    "keep-proportions",
                    "derivation": (
                        f"{volumes['cell_densities_ccfv2_correctednissl']}",
                        "neuron_density.nrrd",
                    ),
                    "atlasrelease": atlasrelease_ccfv2,
                    "voxel_type": voxel_vol,
                    "datasamplemodality": cell_densiry_dsm,
                },
                f"{volumes['mtypes_densities_profile_ccfv2_correctednissl']}": {
                    "name": "mtypes_densities_profile_"+allen_v2+"_correctednissl",
                    "type": me_type,
                    "description": f"{description_ccfv2}. It has been generated from "
                    "density profiles and using the corrected nissl volume",
                    "derivation": None,
                    "atlasrelease": atlasrelease_ccfv2,
                    "voxel_type": voxel_vol,
                    "datasamplemodality": cell_densiry_dsm,
                },
                f"{volumes['mtypes_densities_probability_map_ccfv2_correctednissl']}": {
                    "name": "mtypes_densities_probability_map_"+allen_v2+"_correctednissl",
                    "type": me_type,
                    "description": f"{description_ccfv2}. It has been generated from a "
                    "probability mapping and using the corrected nissl volume",
                    "derivation": None,
                    "atlasrelease": atlasrelease_ccfv2,
                    "voxel_type": voxel_vol,
                    "datasamplemodality": cell_densiry_dsm,
                },
                f"{volumes['mtypes_densities_probability_map_ccfv2_l23split_correctednissl']}": {
                    "name": "mtypes_densities_probability_map_"+allen_v2+"_l23split_correctednissl",
                    "type": me_type,
                    "description": f"{description_ccfv2_split}. It has been generated from a "
                    "probability mapping and using the corrected nissl volume",
                    "derivation": None,
                    "atlasrelease": atlasrelease_ccfv2,
                    "voxel_type": voxel_vol,
                    "datasamplemodality": cell_densiry_dsm,
                },
                f"{volumes['mtypes_densities_probability_map_transplant_correctednissl']}": {
                    "name": "mtypes_densities_probability_map_transplant_correctednissl",
                    "type": me_type,
                    "description": f"{description_ccfv3}. It has been generated from a "
                    "probability mapping, using the corrected nissl volume and transplanted",
                    "derivation": None,
                    "atlasrelease": atlasrelease_ccfv3,
                    "voxel_type": voxel_vol,
                    "datasamplemodality": cell_densiry_dsm,
                },
                f"{volumes['mtypes_densities_probability_map_l23split_transplant_correctednissl']}": {
                    "name": "mtypes_densities_probability_map_l23split_transplant_correctednissl",
                    "type": me_type,
                    "description": f"{description_ccfv3_split}. It has been generated from a "
                    "probability mapping, using the corrected nissl volume and transplanted",
                    "derivation": None,
                    "atlasrelease": atlasrelease_ccfv3_split,
                    "voxel_type": voxel_vol,
                    "datasamplemodality": cell_densiry_dsm,
                },
                f"{volumes['mtypes_densities_probability_map_transplant']}": {
                    "name": "mtypes_densities_probability_map_transplant",
                    "type": me_type,
                    "description": f"{description_ccfv3_split}. It has been generated from a "
                    "probability mapping, using the corrected nissl volume and transplanted",
                    "derivation": None,
                    "atlasrelease": atlasrelease_ccfv3_split,
                    "voxel_type": voxel_vol,
                    "datasamplemodality": cell_densiry_dsm,
                },
            }
        }
    except KeyError as error:
        raise KeyError(
            f"KeyError: {error} does not correspond to one of the datasets defined in "
            "the VolumetricFile section of the 'generated dataset' configuration file."
        )
        exit(1)

    return volumetric_dict


def return_mesh_dict(mesh_datasets):
    """
    Parameters:
        mesh_datasets : Dict containing all the mesh datasets from the input config
                        file.

    Returns:
        mesh_dict : Dict containing all the mesh datasets with their informations.
    """
    mesh = mesh_datasets
    brainmesh_type = [dataset_type, mesh_type, "BrainParcellationMesh"]
    try:
        mesh_dict = {
            f"{mesh['brain_region_meshes_hybrid']}": {
                "name": "brain_region_meshes_hybrid",
                "type": brainmesh_type,
                "description": description_hybrid,
                "atlasrelease": atlasrelease_ccfv2v3,
                "hierarchy_tag": hierarchy_dict["hierarchy_mba"]["name"],
                "annotation_name": "Hybrid",
                "derivation_type": [
                    "VolumetricDataLayer",
                    "BrainParcellationMask",
                    "Dataset",
                ],
            },
            f"{mesh['brain_region_meshes_hybrid_l23split']}": {
                "name": "brain_region_meshes_hybrid",
                "type": brainmesh_type,
                "description": description_hybrid_split,
                "atlasrelease": atlasrelease_hybrid_l23split,
                "hierarchy_tag": hierarchy_dict["hierarchy_l23split"]["name"],
                "annotation_name": "Hybrid L23split",
                "derivation_type": [
                    "VolumetricDataLayer",
                    "BrainParcellationMask",
                    "Dataset",
                ],
            },
            f"{mesh['brain_region_meshes_ccfv2_l23split']}": {
                "name": "brain_region_meshes_ccfv2_l23split",
                "type": brainmesh_type,
                "description": description_ccfv2_split,
                "atlasrelease": allen_v2_split,
                "hierarchy_tag": hierarchy_dict["hierarchy_l23split"]["name"],
                "annotation_name": "CCFv2 L23split",
                "derivation_type": [
                    "VolumetricDataLayer",
                    "BrainParcellationMask",
                    "Dataset",
                ],
            },
            f"{mesh['brain_region_meshes_ccfv3_l23split']}": {
                "name": "brain_region_meshes_ccfv3_l23split",
                "type": brainmesh_type,
                "description": description_ccfv3_split,
                "atlasrelease": allen_v3_split,
                "hierarchy_tag": hierarchy_dict["hierarchy_l23split"]["name"],
                "annotation_name": "CCFv3 L23split",
                "derivation_type": [
                    "VolumetricDataLayer",
                    "BrainParcellationMask",
                    "Dataset",
                ],
            },
        }
    except KeyError as error:
        raise KeyError(
            f"KeyError: {error} does not correspond to one of the datasets defined in "
            "the MeshFile section of the 'generated dataset' configuration file."
        )
        exit(1)

    return mesh_dict


def return_metadata_dict(metadata_datasets):
    """
    Parameters:
        metadata_datasets : Dict containing all the metadata json datasets from the
                           input config file.

    Returns:
        metadata_dict : Dict containing all the metadata json datasets with their
                        informations.
    """
    metadata = metadata_datasets
    allen_v = allen_v2 if (allen_v2 in list(metadata.keys())[0]) else allen_v3
    Allen_v = allen_v.capitalize()
    description_split = description_ccfv2_split if (allen_v == allen_v2) else description_ccfv3_split
    metadata_type = ["BrainRegionSummary", entity_type, regionsummary_type]
    try:
        metadata_dict = {
            f"{metadata['metadata_parcellations_'+allen_v+'_l23split']}": {
                "name": f"metadata_parcellations_{allen_v}_l23split",
                "type": metadata_type,
                "description": description_split,
                "atlasrelease": f"atlasrelease_{allen_v}split",
                "hierarchy_tag": "hierarchy_l23split",
                "annotation_name": f"{Allen_v} L23split",
            }
        }
    except KeyError as error:
        raise KeyError(
            f"KeyError: {error} does not correspond to one of the datasets defined in "
            "the MetadataFile section of the 'generated dataset' configuration file."
        )
        exit(1)

    return metadata_dict


def return_cellrecords_dict(cellrecords_datasets):
    """
    Parameters:
        cellrecords_datasets : Dict containing all the cellrecord datasets from the
                               input config file.

    Returns:
        cellrecord_dict : Dict containing all the cellrecord datasets with their
                          informations.
    """
    cellrecords = cellrecords_datasets
    cellrecords_type = [dataset_type, cellrecord_type]
    try:
        cellrecord_dict = {
            f"{cellrecords['cell_records_sonata']}": {
                "name": "cell_records_sonata",
                "type": cellrecords_type,
                "description": f"Sonata .h5 file storing the 3D cell positions and "
                f"orientations of the {description_hybrid}.",
                "atlasrelease": atlasrelease_hybrid_l23split,
            }
        }
    except KeyError as error:
        raise KeyError(
            f"KeyError: {error} does not correspond to one of the datasets defined in "
            "the CellRecordsFile section of the 'generated dataset' configuration file."
        )
        exit(1)

    return cellrecord_dict
