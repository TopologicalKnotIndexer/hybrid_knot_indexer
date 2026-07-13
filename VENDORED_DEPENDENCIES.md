# Vendored dependencies

This repository is self-contained. Former Git submodules are tracked as regular files at the audited commits below. Their original directory layout is preserved so runtime imports and entry points remain compatible.

| Path | Source | Pinned commit |
| --- | --- | --- |
| `src/khovanov-indexer` | [khovanov-indexer](https://github.com/TopologicalKnotIndexer/khovanov-indexer) | `bee19b9fb363f0ac286eac072b6f13cd91a7847b` |
| `src/khovanov-indexer/src/khovanov-solver` | [khovanov-solver](https://github.com/TopologicalKnotIndexer/khovanov-solver) | `09aee50e389ed02046016dd555ac7fed8f965515` |
| `src/khovanov-indexer/src/khovanov-solver/src/pd_code_de_r1_k8` | [pd_code_de_r1_k8](https://github.com/TopologicalKnotIndexer/pd_code_de_r1_k8) | `395d0b272a06e90c28db90a38803412e8eb9edb5` |
| `src/khovanov-indexer/src/khovanov-solver/src/pd_code_input_sanity` | [pd_code_input_sanity](https://github.com/TopologicalKnotIndexer/pd_code_input_sanity) | `9f0233a3b48043a9e164d98ad6cee644cc792a28` |
| `src/khovanov-indexer/src/khovanov-homology-list` | [khovanov-homology-list](https://github.com/TopologicalKnotIndexer/khovanov-homology-list) | `d3ae43d297b8de7689afd6a925e991fa762420bb` |
| `src/khovanov-indexer/src/slow_dict_reader` | [slow_dict_reader](https://github.com/TopologicalKnotIndexer/slow_dict_reader) | `85e9af7681b8a9b569d3ffae2c68e8d861f89c54` |
| `src/khovanov-indexer/src/slow_dict_reader/src/knotname-reg` | [knotname-reg](https://github.com/TopologicalKnotIndexer/knotname-reg) | `fce68fc3d45a8f3d4e6da81efc07b069ed8179ad` |
| `src/HOMFLY-PT-indexer` | [HOMFLY-PT-indexer](https://github.com/TopologicalKnotIndexer/HOMFLY-PT-indexer) | `a6bf7847ee87444a3134939ceebb8f0e8d0c66da` |
| `src/HOMFLY-PT-indexer/src/HOMFLY-PT-solver` | [HOMFLY-PT-solver](https://github.com/TopologicalKnotIndexer/HOMFLY-PT-solver) | `c801d5dbed2edf57f1c08ed22976bd78cac2b900` |
| `src/HOMFLY-PT-indexer/src/HOMFLY-PT-solver/src/x86_64-sage-minimal` | [x86_64-sage-minimal](https://github.com/TopologicalKnotIndexer/x86_64-sage-minimal) | `ebc8eeaeda03e91425ef0d0cc11c3a7c977f0104` |
| `src/HOMFLY-PT-indexer/src/HOMFLY-PT-solver/src/pd_code_de_r1_k8` | [pd_code_de_r1_k8](https://github.com/TopologicalKnotIndexer/pd_code_de_r1_k8) | `395d0b272a06e90c28db90a38803412e8eb9edb5` |
| `src/HOMFLY-PT-indexer/src/HOMFLY-PT-solver/src/pd_code_input_sanity` | [pd_code_input_sanity](https://github.com/TopologicalKnotIndexer/pd_code_input_sanity) | `9f0233a3b48043a9e164d98ad6cee644cc792a28` |
| `src/HOMFLY-PT-indexer/src/HOMFLY-PT-polynomial-list` | [HOMFLY-PT-polynomial-list](https://github.com/TopologicalKnotIndexer/HOMFLY-PT-polynomial-list) | `cf8ca873e165169405565dd7b1b7b8577c49162f` |
| `src/HOMFLY-PT-indexer/src/slow_dict_reader` | [slow_dict_reader](https://github.com/TopologicalKnotIndexer/slow_dict_reader) | `85e9af7681b8a9b569d3ffae2c68e8d861f89c54` |
| `src/HOMFLY-PT-indexer/src/slow_dict_reader/src/knotname-reg` | [knotname-reg](https://github.com/TopologicalKnotIndexer/knotname-reg) | `fce68fc3d45a8f3d4e6da81efc07b069ed8179ad` |
| `src/spatial_coord_to_pd_code` | [spatial_coord_to_pd_code](https://github.com/TopologicalKnotIndexer/spatial_coord_to_pd_code) | `1215f22321b16e7484bff0573d7a80b8f45b2938` |
| `src/che_data_to_pd_code` | [che_data_to_pd_code](https://github.com/TopologicalKnotIndexer/che_data_to_pd_code) | `8e36a5de47dbb022fb727d24807103904313dcef` |
| `src/che_data_to_pd_code/src/che_data_to_spatial_coord` | [che_data_to_spatial_coord](https://github.com/TopologicalKnotIndexer/che_data_to_spatial_coord) | `9cf66fe76ff9af8cde26511b7f9b8cd62f2afb27` |
| `src/che_data_to_pd_code/src/spatial_coord_to_pd_code` | [spatial_coord_to_pd_code](https://github.com/TopologicalKnotIndexer/spatial_coord_to_pd_code) | `1215f22321b16e7484bff0573d7a80b8f45b2938` |

## Updating a vendored dependency

Replace the listed tree from a reviewed source commit, update this table, and run this repository's complete validation suite. Do not reintroduce Git submodules; every organization project must remain independently cloneable.
