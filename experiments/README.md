# Experiments

This directory is reserved for exploratory material that is useful while learning but should not
be treated as stable package code.

Good candidates for `experiments/` include:

- generated plots
- benchmark outputs
- temporary notebooks
- exported spreadsheets
- sample carrier files for steganography
- image outputs from block-cipher visualizations
- one-off scripts used to compare approaches

## Rule Of Thumb

If a file is needed by tests or imported by a lab, it probably belongs under `src/kryptografia` or
`labs`. If it is produced by running an experiment, it probably belongs here or should be ignored
by Git.

Generated artifacts are intentionally separated from source code so the repository stays readable
and reviewable.

