# Changelog

## [0.1.20](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.19...0.1.20) (2023-06-19)


### Features

* **Credentials:** Use the new endpoint to get the env vars from the backend ([#47](https://github.com/BLSQ/openhexa-sdk-python/issues/47)) ([6277926](https://github.com/BLSQ/openhexa-sdk-python/commit/62779262d632146020697156cf410ae5deee60fc))

## [0.1.19](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.18...0.1.19) (2023-06-07)


### Bug Fixes

* Adapt type parameter typing to accept floats in [@parameter](https://github.com/parameter) decorator ([#45](https://github.com/BLSQ/openhexa-sdk-python/issues/45)) ([4c51414](https://github.com/BLSQ/openhexa-sdk-python/commit/4c5141473d66f5fa0f0c4d4823ed242ad820d151))
* Fix local workspace.yaml path ([#46](https://github.com/BLSQ/openhexa-sdk-python/issues/46)) ([b625d69](https://github.com/BLSQ/openhexa-sdk-python/commit/b625d6994c97b2ae464f565ba4a6c5926ba715fc))


### Miscellaneous

* Update Docker image and adapted docs ([8c42c8f](https://github.com/BLSQ/openhexa-sdk-python/commit/8c42c8fa86765c9c8399f175e0c154966084f87b))
* Update Dockerfile ([41e21d1](https://github.com/BLSQ/openhexa-sdk-python/commit/41e21d134493ea644594488638f704fccc9b0b87))

## [0.1.18](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.17...0.1.18) (2023-06-05)


### Features

* **cli:** Run pipeline using 'openhexa pipelines run -c {}' ([ab29c06](https://github.com/BLSQ/openhexa-sdk-python/commit/ab29c06e8743000ede860a3fc72b01d3886b0991))
* **Parameter:** add float to supported types ([#43](https://github.com/BLSQ/openhexa-sdk-python/issues/43)) ([3b6f709](https://github.com/BLSQ/openhexa-sdk-python/commit/3b6f7098bff9f37b8a790a50c90216c9b79b618c))

## [0.1.17](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.16...0.1.17) (2023-06-01)


### Bug Fixes

* **Logs:** convert log message to str ([#40](https://github.com/BLSQ/openhexa-sdk-python/issues/40)) ([bc31dfb](https://github.com/BLSQ/openhexa-sdk-python/commit/bc31dfbfcbc474bfcd0af51007e121ffece2b2a2))


### Miscellaneous

* **Envs:** Add DOCKER environment ([1f2f19e](https://github.com/BLSQ/openhexa-sdk-python/commit/1f2f19e339337b123162351850f12556571e64ae))
* **Release:** Add chore commits to the changelog ([993efda](https://github.com/BLSQ/openhexa-sdk-python/commit/993efda0d1630eadeeda82e94cf3169422737217))
* Update Docker image ([492b6b4](https://github.com/BLSQ/openhexa-sdk-python/commit/492b6b4a5649c993cffd5625014967778d55285c))

## [0.1.16](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.15...0.1.16) (2023-05-23)


### Bug Fixes

* more robust task status check when stepping DAG  ([#38](https://github.com/BLSQ/openhexa-sdk-python/issues/38)) ([63cfeaf](https://github.com/BLSQ/openhexa-sdk-python/commit/63cfeaf5e3d4db2167894ef6f6d8f48f4142967e))

## [0.1.15](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.14...0.1.15) (2023-05-11)


### Bug Fixes

* **CLI:** Include python notebooks in pipelines ([#36](https://github.com/BLSQ/openhexa-sdk-python/issues/36)) ([a2ac723](https://github.com/BLSQ/openhexa-sdk-python/commit/a2ac7234099c18526b7fc0869e73d9d117a67338))

## [0.1.14](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.13...0.1.14) (2023-05-10)


### Bug Fixes

* **connection:** Create a dataclass on the fly for custom connection ([d10b689](https://github.com/BLSQ/openhexa-sdk-python/commit/d10b689e8779a52e7a352ede5c3c32ab535a7b71))

## [0.1.13](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.12...0.1.13) (2023-05-10)


### Bug Fixes

* **CLI:** current_workspace does not exist the first time ([54c779e](https://github.com/BLSQ/openhexa-sdk-python/commit/54c779ee5ac12f6161a6da60bc6c3d38273a4c16))
* **CLI:** Set the minimum version of Python to 3.9 (is_relative_to requirement) ([b0bb113](https://github.com/BLSQ/openhexa-sdk-python/commit/b0bb11397bc33673467cb198d28a9b8e3542bf35))

## [0.1.12](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.11...0.1.12) (2023-05-10)


### Bug Fixes

* **bootstrap:** Wrong path to check if there is a requirements.txt file ([#33](https://github.com/BLSQ/openhexa-sdk-python/issues/33)) ([9791133](https://github.com/BLSQ/openhexa-sdk-python/commit/9791133917e4cb717c9960012958d412d2938b55))
* **CLI:** Exclude venv/.venv from the zip file ([#31](https://github.com/BLSQ/openhexa-sdk-python/issues/31)) ([088ea01](https://github.com/BLSQ/openhexa-sdk-python/commit/088ea01e46411c6114097b80e7b83fadf57564d7))

## [0.1.11](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.10...0.1.11) (2023-05-09)


### Features

* **Environment:** Add a Environment env variable to be able to differientate the different running environments ([#20](https://github.com/BLSQ/openhexa-sdk-python/issues/20)) ([0e5c878](https://github.com/BLSQ/openhexa-sdk-python/commit/0e5c8781ffa62775f025883e0721d1bbde23c958))


### Bug Fixes

* **Connections:** constcase needs to have a lowercase slug to avoid _ ([#30](https://github.com/BLSQ/openhexa-sdk-python/issues/30)) ([ac809c1](https://github.com/BLSQ/openhexa-sdk-python/commit/ac809c14a9e4766b3c9f3ee2887b7802f706432c))

## [0.1.10](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.9...0.1.10) (2023-05-08)


### Features

* **dependencies:** Install extra dependencies if provided in pipeline ([#23](https://github.com/BLSQ/openhexa-sdk-python/issues/23)) ([426bae4](https://github.com/BLSQ/openhexa-sdk-python/commit/426bae438f5aac566e613285f4a9449ec46a4b40))


### Bug Fixes

* **CLI:** Do not add a workspace that cannot be found online ([#27](https://github.com/BLSQ/openhexa-sdk-python/issues/27)) ([8190a34](https://github.com/BLSQ/openhexa-sdk-python/commit/8190a34b332080cd3ac54e6b9446a4c09ce5a1a9))

## [0.1.9](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.8...0.1.9) (2023-05-05)


### Features

* **Connections:** add custom connection ([7ea7739](https://github.com/BLSQ/openhexa-sdk-python/commit/7ea7739e04657d7b04bee2ff4b4ef4ae3837a1f8))
* **Connections:** add gcs connection ([b8715ea](https://github.com/BLSQ/openhexa-sdk-python/commit/b8715eabc124f1f04c83bd4da345bd962a9deeab))
* **Connections:** add S3 connection function ([e6664fa](https://github.com/BLSQ/openhexa-sdk-python/commit/e6664fa06b0d7adf561f605357ca12808d2d7e2b))
* **Connections:** add tests and small improvement ([5499897](https://github.com/BLSQ/openhexa-sdk-python/commit/5499897537a1a1acf884d9c71bf563adcd7976cb))


### Bug Fixes

* **Parameter:** Validate parameter's code ([4d7d666](https://github.com/BLSQ/openhexa-sdk-python/commit/4d7d66674ad78d93cc67386e15097d118ddb9950))

## [0.1.8](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.7...0.1.8) (2023-05-02)


### Bug Fixes

* Update readme.md to upgrade the lib on install ([51a7fb7](https://github.com/BLSQ/openhexa-sdk-python/commit/51a7fb7860d434f897e84652aeffa86e1c2a8c79))

## [0.1.7](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.6...0.1.7) (2023-05-02)


### Bug Fixes

* print something understandable when using add_file_output locally ([fddbbbd](https://github.com/BLSQ/openhexa-sdk-python/commit/fddbbbdb1f3aa2676d4f0ee25c142efb15cec27f))
* print something understandable when using add_file_output locally ([ce77c1c](https://github.com/BLSQ/openhexa-sdk-python/commit/ce77c1c79e1a558bf3d352c32d5603ee559a0f91))

## [0.1.6](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.5...0.1.6) (2023-04-27)


### Bug Fixes

* apply lower() to pipeline name to avoid weird snakecase strings ([#15](https://github.com/BLSQ/openhexa-sdk-python/issues/15)) ([6dd7333](https://github.com/BLSQ/openhexa-sdk-python/commit/6dd73337478e8f77d21ad299d3184ab94312fe04))

## [0.1.5](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.4...0.1.5) (2023-04-26)


### Bug Fixes

* default args & pipeline URL ([#13](https://github.com/BLSQ/openhexa-sdk-python/issues/13)) ([8c99c85](https://github.com/BLSQ/openhexa-sdk-python/commit/8c99c85c59d501ff55db9591dd28564195ace996))

## [0.1.4](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.3...0.1.4) (2023-04-26)


### Bug Fixes

* add missing MANIFEST.in for assets ([#11](https://github.com/BLSQ/openhexa-sdk-python/issues/11)) ([5b280bd](https://github.com/BLSQ/openhexa-sdk-python/commit/5b280bd76cbf418ac42cac0d8d447c72d4939a5f))

## [0.1.3](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.2...0.1.3) (2023-04-26)


### Bug Fixes

* add requests dep ([#9](https://github.com/BLSQ/openhexa-sdk-python/issues/9)) ([209bee1](https://github.com/BLSQ/openhexa-sdk-python/commit/209bee187ea07561e931da76fcd2b52a539b2c71))

## [0.1.2](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.1...0.1.2) (2023-04-26)


### Features

* **CLI:** Integrate CLI in the openhexa-sdk repo + accepts json ([efdd0a4](https://github.com/BLSQ/openhexa-sdk-python/commit/efdd0a45f42ba4aa32e51f66e4a921c5461fc8c7))
* Integrate CLI into openhexa-sdk ([7ff5001](https://github.com/BLSQ/openhexa-sdk-python/commit/7ff5001a565fc8220e8967716ccf5066c51fb36c))
* revamp IO (workspace & current_run helpers) ([5f2193f](https://github.com/BLSQ/openhexa-sdk-python/commit/5f2193f4a6508f42a13432ccb4b3140fd328e0ec))

## [0.1.1](https://github.com/BLSQ/openhexa-sdk-python/compare/v0.1.0...0.1.1) (2023-04-17)


### Bug Fixes

* **Pipeline:** Store the pipeline name ([f8738d1](https://github.com/BLSQ/openhexa-sdk-python/commit/f8738d12e519177f322ee9448cfa0371635b3244))

## 0.1.0 (2023-04-17)


### Bug Fixes

* **Pipeline:** Store the pipeline name ([f8738d1](https://github.com/BLSQ/openhexa-sdk-python/commit/f8738d12e519177f322ee9448cfa0371635b3244))
