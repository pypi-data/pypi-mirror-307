import pytest
import assimp_py
from pathlib import Path

ModelPath = Path(__file__).parent.joinpath("models/cyborg/cyborg.obj")


@pytest.fixture
def main_scene():
    post_flags = (
        assimp_py.Process_GenNormals | assimp_py.Process_CalcTangentSpace
    )
    scn = assimp_py.ImportFile(str(ModelPath.absolute()), post_flags)
    return scn


def test_scene(main_scene):
    assert main_scene, "Failed to Load Main Scene"


def test_meshes(main_scene):
    mesh = main_scene.meshes[-1]
    assert(mesh)
    assert(main_scene.num_meshes)


def test_mesh_members(main_scene):
    mesh = main_scene.meshes[-1]

    # -- ensure mesh properties
    assert(mesh.name == 'Cyborg')
    assert(mesh.material_index == 1)
    assert(mesh.num_uv_components)

    assert(mesh.indices is not None)

    assert(mesh.vertices is not None)
    assert(mesh.num_vertices > 0)

    # -- should not be None due to Process_GenNormals
    assert(mesh.normals is not None)

    # -- should not be None due to Process_CalcTangentSpace
    assert(mesh.tangents is not None)
    assert(mesh.bitangents is not None)
