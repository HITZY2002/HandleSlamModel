# HandleSlamModel

[中文](README.md) · Units: millimetres

Previously delivered CAD and printable parts for three D435i research prototypes. This packaging revision preserves their geometry; it is not a mechanical redesign or a verified fix.

**Prototype status:** digital geometry checks do not establish physical fit, strength or tracking performance. A prior bracket was assembled, but its exact version is unknown. That observation cannot certify these files. The laptop B1 has not passed a physical installation review.

## Designs

- [Dual-hand Livox retrofit v1](mounts/dual_hand_livox_v1/README.md): six new part types, including optional shims and a fit coupon. It depends on five upstream Livox part types that are not bundled. This is not the full eleven-STL kit.
- [Single-hand spatial v2](mounts/single_hand_spatial_v2/README.md): five part types, nine printed pieces, and five removable adhesive marker pads. Joint M4×50 screw stack-up needs measurement. Do not mix v1 frame parts with v2.
- [Laptop B1](mounts/laptop_b1/README.md): one main part and two pressure shoes, plus an optional coupon. Designed around a MateBook EMF-16 use case, without a verified exact fit. Never lift the laptop by the bracket.

## Before printing

Read the design README, BOM and assembly guide, then [known issues](docs/KNOWN_ISSUES.md). Import STL in mm at 100%. STEP uses assembly coordinates; STL uses print orientation. Start with coupons and unloaded fitting. Confirm real fastener dimensions, support accessibility, contact surfaces and cable clearance before installing the camera.

Measure camera screw protrusion. The rear M3 hole limit must not be applied to the bottom 1/4-20 socket. Do not hammer nuts into place, substitute self-tapping screws, or use bolts to pull misaligned parts together. No rated load, fall-protection, suspension or human-support use is claimed.

Check actual RGB, infrared and depth images, cooling, cable strain relief and marker visibility. Establish marker ball centers from measurements and calibrate extrinsics after assembly changes.

## Editable source and checks

The original CAD scripts use CadQuery 2.7.0 and NumPy. See each design README for commands. Rebuild in a copy because scripts overwrite exports and reports. Python is unnecessary for slicing STL or opening STEP.

```sh
python -m pip install -r requirements.txt
python scripts/verify_release.py
```

[Validation status](docs/VALIDATION.md) separates historical records, release-time checks and unperformed physical tests.

## Attribution and licensing

Only custom printable parts and traceable source are included. Upstream Livox geometry, downloaded camera CAD/meshes, combined Blender scenes, historical renders containing third-party models, personal photographs and unrelated material are excluded.

The publisher approved GPL-2.0-only for the custom code, CAD and documentation in this repository. See [LICENSE](LICENSE) and [scope](LICENSING.md). External dependencies retain their own licenses.

[Dependencies and attribution](docs/ATTRIBUTION.md) · [Changelog](CHANGELOG.md) · [Checksums](SHA256SUMS.txt)
