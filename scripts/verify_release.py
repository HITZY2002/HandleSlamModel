"""Verify the curated printable meshes and editable solids. No physical-test claims.

Run from any working directory with the versions in requirements.txt.
Writes validation/release_geometry.json. SPDX-License-Identifier: GPL-2.0-only; see LICENSE.
"""
from pathlib import Path
import hashlib
import json
import struct
from datetime import datetime, timezone
import numpy as np
import cadquery as cq

ROOT = Path(__file__).resolve().parents[1]
DESIGNS = {
    'dual_hand_livox_v1': ('stl', 'source', 6),
    'single_hand_spatial_v2': ('STL', 'STEP', 5),
    'laptop_b1': ('STL_PROTOTYPE', 'STEP', 3),
}


def read_stl(path):
    data = path.read_bytes()
    n = struct.unpack_from('<I', data, 80)[0] if len(data) >= 84 else -1
    if len(data) == 84 + 50 * n:
        dtype = np.dtype([('normal', '<f4', (3,)), ('v', '<f4', (3, 3)), ('attr', '<u2')])
        triangles = np.frombuffer(data, dtype=dtype, offset=84)['v'].astype(float)
    else:
        rows = [list(map(float, line.split()[1:])) for line in data.decode().splitlines()
                if line.strip().startswith('vertex ')]
        triangles = np.asarray(rows).reshape(-1, 3, 3)
    assert triangles.size and np.isfinite(triangles).all(), str(path)
    return triangles, hashlib.sha256(data).hexdigest()


def check_mesh(path):
    t, digest = read_stl(path)
    vertices, ids = np.unique(np.round(t.reshape(-1, 3), 5), axis=0, return_inverse=True)
    faces = ids.reshape(-1, 3)
    edges = np.concatenate([faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]])
    unordered = np.sort(edges, axis=1)
    _, inverse, counts = np.unique(unordered, axis=0, return_inverse=True, return_counts=True)
    directions = np.where(edges[:, 0] < edges[:, 1], 1, -1)
    winding = np.bincount(inverse, weights=directions)
    double_area = np.linalg.norm(np.cross(t[:, 1] - t[:, 0], t[:, 2] - t[:, 0]), axis=1)
    volume = float(np.einsum('ij,ij->i', t[:, 0], np.cross(t[:, 1], t[:, 2])).sum() / 6)
    report = {
        'sha256': digest, 'triangles': len(t),
        'boundary_edges': int(np.sum(counts == 1)),
        'nonmanifold_edges': int(np.sum(counts > 2)),
        'degenerate_triangles': int(np.sum(double_area <= 1e-9)),
        'inconsistent_edge_directions': int(np.sum(winding != 0)),
        'signed_volume_mm3': volume,
        'print_dimensions_mm': (t.max((0, 1)) - t.min((0, 1))).tolist(),
        'print_min_z_mm': float(t[:, :, 2].min()),
    }
    assert all(report[k] == 0 for k in ('boundary_edges', 'nonmanifold_edges',
                                       'degenerate_triangles', 'inconsistent_edge_directions')), report
    assert volume > 0 and abs(report['print_min_z_mm']) < .01, report
    return report


def main():
    report = {
        'checked_at_utc': datetime.now(timezone.utc).isoformat(),
        'cadquery_version': cq.__version__, 'numpy_version': np.__version__,
        'scope': '14 curated STL files and 14 matching STEP part files only',
        'physical_test_performed': False,
        'limitations': ['No complete triangle self-intersection proof',
                       'No complete assembly collision or screw stack-up proof',
                       'No physical fit, strength, thermal or tracking validation'],
        'designs': {},
    }
    for design, (mesh_dir, cad_dir, expected_count) in DESIGNS.items():
        root = ROOT / 'mounts' / design
        files = sorted((root / mesh_dir).glob('*.stl'))
        assert len(files) == expected_count, (design, len(files), expected_count)
        parts = {}
        for mesh in files:
            item = check_mesh(mesh)
            step = root / cad_dir / (mesh.stem + '.step')
            shape = cq.importers.importStep(str(step)).val()
            bb = shape.BoundingBox()
            assert shape.isValid() and len(shape.Solids()) == 1, str(step)
            item['step_sha256'] = hashlib.sha256(step.read_bytes()).hexdigest()
            item['step_valid'] = True
            item['step_solid_count'] = len(shape.Solids())
            item['step_volume_mm3'] = shape.Volume()
            item['step_dimensions_mm'] = [bb.xlen, bb.ylen, bb.zlen]
            relative_error = abs(item['signed_volume_mm3'] / shape.Volume() - 1)
            item['mesh_vs_step_relative_volume_error'] = relative_error
            assert relative_error < .005, (str(mesh), relative_error)
            assert np.allclose(sorted(item['print_dimensions_mm']),
                               sorted(item['step_dimensions_mm']), atol=.1), str(mesh)
            parts[mesh.name] = item
        report['designs'][design] = parts
    (ROOT / 'validation').mkdir(exist_ok=True)
    (ROOT / 'validation' / 'release_geometry.json').write_text(json.dumps(report, indent=2) + '\n')
    print('PASS: 14 STL meshes and 14 matching STEP single solids. Physical tests: NOT RUN.')


if __name__ == '__main__':
    main()
