# Changelog

## [2.4.0](https://github.com/BLSQ/openhexa-sdk-python/compare/v2.3.1...v2.4.0) (2025-06-16)


### Features

* include R files in the pipeline zip file ([#271](https://github.com/BLSQ/openhexa-sdk-python/issues/271)) ([66c99be](https://github.com/BLSQ/openhexa-sdk-python/commit/66c99beef16f825b685eedbfe01f28746491b3f1))

## [2.3.1](https://github.com/BLSQ/openhexa-sdk-python/compare/v2.3.0...v2.3.1) (2025-06-06)


### Bug Fixes

* **conda:** fixes recipe dependencies ([de137b0](https://github.com/BLSQ/openhexa-sdk-python/commit/de137b0115dda70268bf36acff30bbd9e2ff8359))

## [2.3.0](https://github.com/BLSQ/openhexa-sdk-python/compare/v2.2.0...v2.3.0) (2025-05-26)


### Features

* add the new GitHub action for pushing into the SDK init command (HEXA-1269) ([#266](https://github.com/BLSQ/openhexa-sdk-python/issues/266)) ([575f604](https://github.com/BLSQ/openhexa-sdk-python/commit/575f604872d39049131a9b460b3571882002edb6))
* breaking changes detection against the backend server (HEXA-1238) ([#260](https://github.com/BLSQ/openhexa-sdk-python/issues/260)) ([316feef](https://github.com/BLSQ/openhexa-sdk-python/commit/316feef5ed62b981d855c379278f670df544fbdb))


### Bug Fixes

* prefix iaso widget with IASO_ ([#267](https://github.com/BLSQ/openhexa-sdk-python/issues/267)) ([8a7dd70](https://github.com/BLSQ/openhexa-sdk-python/commit/8a7dd70b32b4c99deee8c458b1804842ca7b06b7))
* SDK dataset add_file filename is not optional ([#262](https://github.com/BLSQ/openhexa-sdk-python/issues/262)) ([825f209](https://github.com/BLSQ/openhexa-sdk-python/commit/825f209e076a0059fa5b44145820ca333565f4f9))
* type of arg `type` should be of type `type` ([#265](https://github.com/BLSQ/openhexa-sdk-python/issues/265)) ([d9e7421](https://github.com/BLSQ/openhexa-sdk-python/commit/d9e742197b47f5fe387a3f8b008b3dd08cbaf184))

## [2.2.0](https://github.com/BLSQ/openhexa-sdk-python/compare/v2.1.2...v2.2.0) (2025-05-14)


### Features

* **pipeline:** add IASO widget implementation ([#255](https://github.com/BLSQ/openhexa-sdk-python/issues/255)) ([1d51228](https://github.com/BLSQ/openhexa-sdk-python/commit/1d512289df7a2b704d720fd3b6dff006913a0ec6))


### Bug Fixes

* dhis org_units and iaso org_units overlap ([#261](https://github.com/BLSQ/openhexa-sdk-python/issues/261)) ([5b256f1](https://github.com/BLSQ/openhexa-sdk-python/commit/5b256f1259440a16971091f381000242a59a2c7e))

## [2.1.2](https://github.com/BLSQ/openhexa-sdk-python/compare/v2.1.1...v2.1.2) (2025-04-07)


### Bug Fixes

* adds connection field to decorator ([#251](https://github.com/BLSQ/openhexa-sdk-python/issues/251)) ([2be9bd3](https://github.com/BLSQ/openhexa-sdk-python/commit/2be9bd38a1230467e56eb103bb425242f6809d1f))

## [2.1.1](https://github.com/BLSQ/openhexa-sdk-python/compare/v2.1.0...v2.1.1) (2025-04-02)


### Bug Fixes

* getting permissions of create template version (HEXA-1228)([#249](https://github.com/BLSQ/openhexa-sdk-python/issues/249)) ([ce36728](https://github.com/BLSQ/openhexa-sdk-python/commit/ce3672821e9bea53251be0ffe90c0d7ee90c24cb))

## [2.1.0](https://github.com/BLSQ/openhexa-sdk-python/compare/v2.0.5...v2.1.0) (2025-03-28)


### Features

* cli users should have a way to give a pipeline code in the command to upload a pipeline (HEXA-1216) ([#242](https://github.com/BLSQ/openhexa-sdk-python/issues/242)) ([69d1cb9](https://github.com/BLSQ/openhexa-sdk-python/commit/69d1cb963b38385d39d088beacdd876a1c1be2c3))


### Bug Fixes

* dictionary lapping for widget ([#248](https://github.com/BLSQ/openhexa-sdk-python/issues/248)) ([9b5224c](https://github.com/BLSQ/openhexa-sdk-python/commit/9b5224ce61acc732a1124fc347a9cfc0f0e49e9f))

## [2.0.5](https://github.com/BLSQ/openhexa-sdk-python/compare/v2.0.4...v2.0.5) (2025-03-11)


### Bug Fixes

* Adapt the github actions to reflect the change of python version ([1312d64](https://github.com/BLSQ/openhexa-sdk-python/commit/1312d6498a236ff9c7154c31cbddfbc986a30b1d))

## [2.0.4](https://github.com/BLSQ/openhexa-sdk-python/compare/v2.0.3...v2.0.4) (2025-03-11)


### Bug Fixes

* We need to provide the version to anaconda to not have the v in front of the version ([74e240a](https://github.com/BLSQ/openhexa-sdk-python/commit/74e240ac695f32679aa899bc1274975e5f7c8049))

## [2.0.3](https://github.com/BLSQ/openhexa-sdk-python/compare/v2.0.2...v2.0.3) (2025-03-11)


### Miscellaneous Chores

* Release 2.0.3 ([2cd0d5a](https://github.com/BLSQ/openhexa-sdk-python/commit/2cd0d5a2aaa6a74859a9c85ec0a5f1414d82b27f))

## [2.0.2](https://github.com/BLSQ/openhexa-sdk-python/compare/v2.0.1...v2.0.2) (2025-03-11)


### ⚠ BREAKING CHANGES

* Deprecate pipeline code and allow to select the target pipeline when pushing(HEXA-1170) ([#227](https://github.com/BLSQ/openhexa-sdk-python/issues/227))
* Set a default version number for each pipeline version, make version name optional ([#221](https://github.com/BLSQ/openhexa-sdk-python/issues/221))

### Features

* add a retry mechanism for API call ([#166](https://github.com/BLSQ/openhexa-sdk-python/issues/166)) ([3d89da3](https://github.com/BLSQ/openhexa-sdk-python/commit/3d89da3f5efd690b1505b0130ec23b70ac3f455d))
* Add jinja2 templates, add github workflow ([7f53c6a](https://github.com/BLSQ/openhexa-sdk-python/commit/7f53c6a281eab59d3e559c50f57f283844300252))
* Add support for Python 3.11 ([#87](https://github.com/BLSQ/openhexa-sdk-python/issues/87)) ([03aa815](https://github.com/BLSQ/openhexa-sdk-python/commit/03aa8157896f92afdd5eadf7eeae3ad73741b633))
* Add tmp_path property on workspace ([#83](https://github.com/BLSQ/openhexa-sdk-python/issues/83)) ([c944b6d](https://github.com/BLSQ/openhexa-sdk-python/commit/c944b6d8d6cea6bfcb1e1e1974ec06c8f47609c2))
* Check that docker exists and is running ([#136](https://github.com/BLSQ/openhexa-sdk-python/issues/136)) ([3d4d75f](https://github.com/BLSQ/openhexa-sdk-python/commit/3d4d75f5b79d0fd7b5288b5447c4e538a5a7844a))
* **CI/CD:** adds github action v4 config ([59cdde2](https://github.com/BLSQ/openhexa-sdk-python/commit/59cdde223b873ec1cd1ff4f95978631e51a2ac83))
* **CI/CD:** adds github action v4 config ([ce8f848](https://github.com/BLSQ/openhexa-sdk-python/commit/ce8f8487dee48c2df32c2eab81723fa2cc514529))
* **CLI:** check if permission_denied is thrown ([#129](https://github.com/BLSQ/openhexa-sdk-python/issues/129)) ([2f856fe](https://github.com/BLSQ/openhexa-sdk-python/commit/2f856fe5927e7fe30456b9ff7fee57a12491c827))
* **CLI:** Integrate CLI in the openhexa-sdk repo + accepts json ([efdd0a4](https://github.com/BLSQ/openhexa-sdk-python/commit/efdd0a45f42ba4aa32e51f66e4a921c5461fc8c7))
* **cli:** Run pipeline using 'openhexa pipelines run -c {}' ([ab29c06](https://github.com/BLSQ/openhexa-sdk-python/commit/ab29c06e8743000ede860a3fc72b01d3886b0991))
* **CLI:** Use blsq/openhexa-blsq-environment as the image to run the pipeline ([#115](https://github.com/BLSQ/openhexa-sdk-python/issues/115)) ([c813e3a](https://github.com/BLSQ/openhexa-sdk-python/commit/c813e3a1bc44a3ad8524326bfc3cdf4abca92cde))
* **CLI:** User can add --yes to the  command to not have to confirm the creation of the pipeline ([85a9098](https://github.com/BLSQ/openhexa-sdk-python/commit/85a9098e72a3889879ad4723ffea94c773a6178b))
* **CLI:** User can provide a name, description and link of the pipel… ([#142](https://github.com/BLSQ/openhexa-sdk-python/issues/142)) ([45fd2e7](https://github.com/BLSQ/openhexa-sdk-python/commit/45fd2e7cd70ebc1000509ab50eb4d31a5c567200))
* conditionally run pipelines in debug mode ([#223](https://github.com/BLSQ/openhexa-sdk-python/issues/223)) ([6f495f7](https://github.com/BLSQ/openhexa-sdk-python/commit/6f495f79d90c64bf1b7729b4b570af1fa5bdb925))
* **Connections:** add custom connection ([7ea7739](https://github.com/BLSQ/openhexa-sdk-python/commit/7ea7739e04657d7b04bee2ff4b4ef4ae3837a1f8))
* **Connections:** add gcs connection ([b8715ea](https://github.com/BLSQ/openhexa-sdk-python/commit/b8715eabc124f1f04c83bd4da345bd962a9deeab))
* **Connections:** add S3 connection function ([e6664fa](https://github.com/BLSQ/openhexa-sdk-python/commit/e6664fa06b0d7adf561f605357ca12808d2d7e2b))
* **Connections:** add support for IASO connection ([#82](https://github.com/BLSQ/openhexa-sdk-python/issues/82)) ([707b798](https://github.com/BLSQ/openhexa-sdk-python/commit/707b798ac6e8fc7846a241f3d05ef760b224ce45))
* **Connections:** add tests and small improvement ([5499897](https://github.com/BLSQ/openhexa-sdk-python/commit/5499897537a1a1acf884d9c71bf563adcd7976cb))
* **Connections:** import and re-export connection classes in openhexa.sdk ([#93](https://github.com/BLSQ/openhexa-sdk-python/issues/93)) ([2e3db63](https://github.com/BLSQ/openhexa-sdk-python/commit/2e3db639d2a2ef0b6b27e15eca0970457e6822bb))
* **Credentials:** Use the new endpoint to get the env vars from the backend ([#47](https://github.com/BLSQ/openhexa-sdk-python/issues/47)) ([6277926](https://github.com/BLSQ/openhexa-sdk-python/commit/62779262d632146020697156cf410ae5deee60fc))
* **Dataset:** Create dataset with the SDK ([#110](https://github.com/BLSQ/openhexa-sdk-python/issues/110)) ([cba3e7e](https://github.com/BLSQ/openhexa-sdk-python/commit/cba3e7e861487204a534295492ee93e3c118387c))
* **DatasetFiles:** add helper to check if file exists ([c76d890](https://github.com/BLSQ/openhexa-sdk-python/commit/c76d8905a5e21785107257361c843a2be60da895))
* **Datasets:** Add datasets support to SDK ([#77](https://github.com/BLSQ/openhexa-sdk-python/issues/77)) ([d8eb50e](https://github.com/BLSQ/openhexa-sdk-python/commit/d8eb50e9210f7f610fd4e210dc17daf5331b8e97))
* delete pipeline ([#91](https://github.com/BLSQ/openhexa-sdk-python/issues/91)) ([549f73d](https://github.com/BLSQ/openhexa-sdk-python/commit/549f73d55cf3ddab6e1788ec78d484c4078ea85f))
* **dependencies:** Install extra dependencies if provided in pipeline ([#23](https://github.com/BLSQ/openhexa-sdk-python/issues/23)) ([426bae4](https://github.com/BLSQ/openhexa-sdk-python/commit/426bae438f5aac566e613285f4a9449ec46a4b40))
* Deprecate pipeline code and allow to select the target pipeline when pushing(HEXA-1170) ([#227](https://github.com/BLSQ/openhexa-sdk-python/issues/227)) ([fd5ccac](https://github.com/BLSQ/openhexa-sdk-python/commit/fd5ccace020fc00116d886b975a3fd70e972d03d))
* **Environment:** Add a Environment env variable to be able to differientate the different running environments ([#20](https://github.com/BLSQ/openhexa-sdk-python/issues/20)) ([0e5c878](https://github.com/BLSQ/openhexa-sdk-python/commit/0e5c8781ffa62775f025883e0721d1bbde23c958))
* Integrate CLI into openhexa-sdk ([7ff5001](https://github.com/BLSQ/openhexa-sdk-python/commit/7ff5001a565fc8220e8967716ccf5066c51fb36c))
* **Parameter:** add float to supported types ([#43](https://github.com/BLSQ/openhexa-sdk-python/issues/43)) ([3b6f709](https://github.com/BLSQ/openhexa-sdk-python/commit/3b6f7098bff9f37b8a790a50c90216c9b79b618c))
* **Parameter:** add support for Dataset parameter type ([#120](https://github.com/BLSQ/openhexa-sdk-python/issues/120)) ([783b672](https://github.com/BLSQ/openhexa-sdk-python/commit/783b67208d21f5a226ebb6f65d1f35dfe6da6d3d))
* **Parameter:** HEXA-1134 adds dhis2 parameters widget and connection fields plus validation ([#225](https://github.com/BLSQ/openhexa-sdk-python/issues/225)) ([c1b703c](https://github.com/BLSQ/openhexa-sdk-python/commit/c1b703cc0a942da000093eccd18edf26936afd6b))
* **Pipelines:** allow user to define a timeout for pipelines ([0eeab40](https://github.com/BLSQ/openhexa-sdk-python/commit/0eeab4064d38422b38f31a4cf70d3d8b823d2702))
* **Pipelines:** Allow user to download the latest version of a pipeline ([#128](https://github.com/BLSQ/openhexa-sdk-python/issues/128)) ([2dae69d](https://github.com/BLSQ/openhexa-sdk-python/commit/2dae69da69d4742b844f4b8e0c0e5b4e999da41d))
* **Pipelines:** prevent push of version  with params for scheduled pipeline. ([#55](https://github.com/BLSQ/openhexa-sdk-python/issues/55)) ([b9de756](https://github.com/BLSQ/openhexa-sdk-python/commit/b9de756f4dc94296bc427b2dd3337740909399ed))
* **Pipeline:** Use the AST to get the specs of the pipeline and its parameters ([#130](https://github.com/BLSQ/openhexa-sdk-python/issues/130)) ([9515499](https://github.com/BLSQ/openhexa-sdk-python/commit/951549925fae7ace4bf26a1922dea7f7738c6982))
* revamp IO (workspace & current_run helpers) ([5f2193f](https://github.com/BLSQ/openhexa-sdk-python/commit/5f2193f4a6508f42a13432ccb4b3140fd328e0ec))
* **Run:** Run pipelines with the debugger ready to be used ([a67d0fe](https://github.com/BLSQ/openhexa-sdk-python/commit/a67d0fe6eeba0c97cb2513b5c9d6fb9a2b5d8690))
* **Run:** Run pipelines with the debugger ready to be used ([#157](https://github.com/BLSQ/openhexa-sdk-python/issues/157)) ([754c21b](https://github.com/BLSQ/openhexa-sdk-python/commit/754c21b4888b69ee7feb6f80beaf672520539f52))
* **Run:** Run pipelines with the debugger ready to be used ([#157](https://github.com/BLSQ/openhexa-sdk-python/issues/157)) ([6863173](https://github.com/BLSQ/openhexa-sdk-python/commit/686317301b7ec9e1c83ec8ce7bb2c58a0f9b4021))
* Set a default version number for each pipeline version, make version name optional ([#221](https://github.com/BLSQ/openhexa-sdk-python/issues/221)) ([488b290](https://github.com/BLSQ/openhexa-sdk-python/commit/488b2906a3d9948d6c86de8cdf4d998ec8e8bc47))
* Support template version creation on push (HEXA-1182) ([#226](https://github.com/BLSQ/openhexa-sdk-python/issues/226)) ([45a61be](https://github.com/BLSQ/openhexa-sdk-python/commit/45a61be06ca1e8333383b612eb384cd2d70203ad))
* Update SDK version in Dockerfile ([#57](https://github.com/BLSQ/openhexa-sdk-python/issues/57)) ([208d7ea](https://github.com/BLSQ/openhexa-sdk-python/commit/208d7ea561417bf9dc106d3b545254ecbde863db))
* Use a new way to load settings ([#131](https://github.com/BLSQ/openhexa-sdk-python/issues/131)) ([9619673](https://github.com/BLSQ/openhexa-sdk-python/commit/9619673f226149915afb73387ed8e0f8891ed520))
* **Workspaces:** allow user to specify workspace docker image ([#95](https://github.com/BLSQ/openhexa-sdk-python/issues/95)) ([2455a3e](https://github.com/BLSQ/openhexa-sdk-python/commit/2455a3e2eb136e94e543e8b1c8a44fa329bf9769))
* **Workspaces:** get connections from graphql API ([#158](https://github.com/BLSQ/openhexa-sdk-python/issues/158)) ([bba409b](https://github.com/BLSQ/openhexa-sdk-python/commit/bba409b7d241993c124100f34b7b64b899fa423b))
* **Workspaces:** list datasets in a workspace ([#112](https://github.com/BLSQ/openhexa-sdk-python/issues/112)) ([916832a](https://github.com/BLSQ/openhexa-sdk-python/commit/916832a44bae906cfe0a2706bf90c8057ab1b43f))


### Bug Fixes

* Adapt type parameter typing to accept floats in [@parameter](https://github.com/parameter) decorator ([#45](https://github.com/BLSQ/openhexa-sdk-python/issues/45)) ([4c51414](https://github.com/BLSQ/openhexa-sdk-python/commit/4c5141473d66f5fa0f0c4d4823ed242ad820d151))
* add missing MANIFEST.in for assets ([#11](https://github.com/BLSQ/openhexa-sdk-python/issues/11)) ([5b280bd](https://github.com/BLSQ/openhexa-sdk-python/commit/5b280bd76cbf418ac42cac0d8d447c72d4939a5f))
* add requests dep ([#9](https://github.com/BLSQ/openhexa-sdk-python/issues/9)) ([209bee1](https://github.com/BLSQ/openhexa-sdk-python/commit/209bee187ea07561e931da76fcd2b52a539b2c71))
* **API:** uploading a version now returns a pipelineVersion instead of a version ([5f89738](https://github.com/BLSQ/openhexa-sdk-python/commit/5f89738f803a391dd39f3a88a4e3ae7bb19f2860))
* apply lower() to pipeline name to avoid weird snakecase strings ([#15](https://github.com/BLSQ/openhexa-sdk-python/issues/15)) ([6dd7333](https://github.com/BLSQ/openhexa-sdk-python/commit/6dd73337478e8f77d21ad299d3184ab94312fe04))
* **bootstrap:** Wrong path to check if there is a requirements.txt file ([#33](https://github.com/BLSQ/openhexa-sdk-python/issues/33)) ([9791133](https://github.com/BLSQ/openhexa-sdk-python/commit/9791133917e4cb717c9960012958d412d2938b55))
* **Build:** Manifest.in was missing the .github folder ([8afa0eb](https://github.com/BLSQ/openhexa-sdk-python/commit/8afa0eb4560f3ca4663850b4fb7860fa995dbe5f))
* **ci:** Fix python3.9 tests ([3d9aa95](https://github.com/BLSQ/openhexa-sdk-python/commit/3d9aa955262e19ba549d160d2f650a7ac7403ddb))
* **CLI:** Ask the user to create the workspace.yaml if not found ([#109](https://github.com/BLSQ/openhexa-sdk-python/issues/109)) ([1da1a04](https://github.com/BLSQ/openhexa-sdk-python/commit/1da1a049f1c91fa8ff0e8389528b0a904f31c661))
* **CLI:** Check if args of decorators are of a primitive type ([#146](https://github.com/BLSQ/openhexa-sdk-python/issues/146)) ([3ca0f51](https://github.com/BLSQ/openhexa-sdk-python/commit/3ca0f51af415680da7c31188c9340e09fcfefc2b))
* **CLI:** current_workspace does not exist the first time ([54c779e](https://github.com/BLSQ/openhexa-sdk-python/commit/54c779ee5ac12f6161a6da60bc6c3d38273a4c16))
* **CLI:** Do not add a workspace that cannot be found online ([#27](https://github.com/BLSQ/openhexa-sdk-python/issues/27)) ([8190a34](https://github.com/BLSQ/openhexa-sdk-python/commit/8190a34b332080cd3ac54e6b9446a4c09ce5a1a9))
* **CLI:** Do not ask to create the pipeline if the user has said yes as param ([6597876](https://github.com/BLSQ/openhexa-sdk-python/commit/6597876ded1e900599d33fbe17083e307805d39f))
* **CLI:** Do not require a config even if it's empty ([#50](https://github.com/BLSQ/openhexa-sdk-python/issues/50)) ([8e1098f](https://github.com/BLSQ/openhexa-sdk-python/commit/8e1098fc544918aaf78e1eb821e2b5540ba6c42e))
* **CLI:** Exclude venv/.venv from the zip file ([#31](https://github.com/BLSQ/openhexa-sdk-python/issues/31)) ([088ea01](https://github.com/BLSQ/openhexa-sdk-python/commit/088ea01e46411c6114097b80e7b83fadf57564d7))
* **CLI:** Include python notebooks in pipelines ([#36](https://github.com/BLSQ/openhexa-sdk-python/issues/36)) ([a2ac723](https://github.com/BLSQ/openhexa-sdk-python/commit/a2ac7234099c18526b7fc0869e73d9d117a67338))
* **Cli:** no error is thrown when workspace doesn't exist ([#153](https://github.com/BLSQ/openhexa-sdk-python/issues/153)) ([fbbec07](https://github.com/BLSQ/openhexa-sdk-python/commit/fbbec07bc27ad6e53cd8f15bd68c701f4b702c76))
* **Cli:** no error is thrown when workspace doesn't exist ([#153](https://github.com/BLSQ/openhexa-sdk-python/issues/153)) ([cefc69c](https://github.com/BLSQ/openhexa-sdk-python/commit/cefc69c15f8abd2b27e3e4d9ba3b88507537f296))
* **CLI:** Notebook pipelines make the pipelines list to crash ([374c8fb](https://github.com/BLSQ/openhexa-sdk-python/commit/374c8fbfe332cb4c1876d1497b8b6f098ced9573))
* **CLI:** Running a pipeline should not require an active workspace ([#126](https://github.com/BLSQ/openhexa-sdk-python/issues/126)) ([7618d91](https://github.com/BLSQ/openhexa-sdk-python/commit/7618d918ebe701de41191dfe58196c3118f0bd9f))
* **CLI:** Set the minimum version of Python to 3.9 (is_relative_to requirement) ([b0bb113](https://github.com/BLSQ/openhexa-sdk-python/commit/b0bb11397bc33673467cb198d28a9b8e3542bf35))
* **code:** Inform users when they try to push a pipeline with a 'code' ([5b2f991](https://github.com/BLSQ/openhexa-sdk-python/commit/5b2f9910919ca310d0832eae3ba828ffff7f4884))
* **Conda:** Copy stringcase package into our repo ([e6345b2](https://github.com/BLSQ/openhexa-sdk-python/commit/e6345b23b60260c5db957faa70caf606ea623476))
* **Conda:** Update requirements conditions ([7d01ad3](https://github.com/BLSQ/openhexa-sdk-python/commit/7d01ad36988862dda64b5e9913cd0c87e53a42b9))
* **connection:** Create a dataclass on the fly for custom connection ([d10b689](https://github.com/BLSQ/openhexa-sdk-python/commit/d10b689e8779a52e7a352ede5c3c32ab535a7b71))
* **Connections:** constcase needs to have a lowercase slug to avoid _ ([#30](https://github.com/BLSQ/openhexa-sdk-python/issues/30)) ([ac809c1](https://github.com/BLSQ/openhexa-sdk-python/commit/ac809c14a9e4766b3c9f3ee2887b7802f706432c))
* **Connections:** fix shallow matching when retrieving connection fields ([#209](https://github.com/BLSQ/openhexa-sdk-python/issues/209)) ([0bfd5f7](https://github.com/BLSQ/openhexa-sdk-python/commit/0bfd5f7d6f56f9e061551d85343e9389d827cf79))
* **Connections:** hide sensitive informations when printing  connection ([#79](https://github.com/BLSQ/openhexa-sdk-python/issues/79)) ([db749a3](https://github.com/BLSQ/openhexa-sdk-python/commit/db749a3d1d9119c95013030d390d8ecf568d5b26))
* **Connections:** Rename 'slug' to 'identifier' ([7f52ce4](https://github.com/BLSQ/openhexa-sdk-python/commit/7f52ce43309546a614bb71041146d42aa3c0e92a))
* **Connections:** Set the slug to lowercase before building the env var ([7f52ce4](https://github.com/BLSQ/openhexa-sdk-python/commit/7f52ce43309546a614bb71041146d42aa3c0e92a))
* **Connections:** specify connection workspace ([#170](https://github.com/BLSQ/openhexa-sdk-python/issues/170)) ([f8b2dda](https://github.com/BLSQ/openhexa-sdk-python/commit/f8b2ddabf17022661418ca3ec7d22dab51b3aa51))
* **Connections:** use lowercase for identifier ([#184](https://github.com/BLSQ/openhexa-sdk-python/issues/184)) ([a864629](https://github.com/BLSQ/openhexa-sdk-python/commit/a864629fd21cabb1ea0918cee974ae71e36a42b7))
* copies files correctly to workspace directory ([f6a19b2](https://github.com/BLSQ/openhexa-sdk-python/commit/f6a19b2f61b2a997822110f473846520495a3943))
* copy workspace folder to correct path ([d316597](https://github.com/BLSQ/openhexa-sdk-python/commit/d3165971750131d4b0bc001ece35f72554ce9163))
* copy workspace folder to correct path ([6a1a6a4](https://github.com/BLSQ/openhexa-sdk-python/commit/6a1a6a4b456d320709f0e4c491171f01489a82b6))
* **CurrentRun:** check if file exist when adding output ([#114](https://github.com/BLSQ/openhexa-sdk-python/issues/114)) ([4dfe8d1](https://github.com/BLSQ/openhexa-sdk-python/commit/4dfe8d12d56ed2d66007a90b48372adb0b5ac3d3))
* **dataset:** Support bytes directly in read_content ([#111](https://github.com/BLSQ/openhexa-sdk-python/issues/111)) ([e83eefb](https://github.com/BLSQ/openhexa-sdk-python/commit/e83eefba04713db3c38749395a043e6dfb58a977))
* **Datasets:** Use the correct mutation to upload files in datasets : generateDatasetUploadUrl ([d4d56d6](https://github.com/BLSQ/openhexa-sdk-python/commit/d4d56d6600912653eddbcce5b230d9c81f7ab3a3))
* default args & pipeline URL ([#13](https://github.com/BLSQ/openhexa-sdk-python/issues/13)) ([8c99c85](https://github.com/BLSQ/openhexa-sdk-python/commit/8c99c85c59d501ff55db9591dd28564195ace996))
* **deps:** update dependency pytest-cov to v6 ([#218](https://github.com/BLSQ/openhexa-sdk-python/issues/218)) ([47a78e5](https://github.com/BLSQ/openhexa-sdk-python/commit/47a78e5917ecab473c19f5b792bec94e1665f0c9))
* **deps:** update dependency urllib3 to v2 ([#217](https://github.com/BLSQ/openhexa-sdk-python/issues/217)) ([8d93d99](https://github.com/BLSQ/openhexa-sdk-python/commit/8d93d993a3fb2a6260bb1e5154fff9de12428749))
* Do not crash the CLI when some pipelines do not have a current version ([3b8cd5c](https://github.com/BLSQ/openhexa-sdk-python/commit/3b8cd5ce0d9bc03fbbc308db21394eb48a061eb9))
* Do not make two requests to the server to check if the pipeline exists ([#94](https://github.com/BLSQ/openhexa-sdk-python/issues/94)) ([4501bda](https://github.com/BLSQ/openhexa-sdk-python/commit/4501bdadf2ba6627f9c718a15c7036df5783044b))
* **Docker:** Always force pull the image ([#103](https://github.com/BLSQ/openhexa-sdk-python/issues/103)) ([c538e10](https://github.com/BLSQ/openhexa-sdk-python/commit/c538e109e05b541d0e70dec8196e564338afd6db))
* **Docker:** Disable healthchecks when running the pipeline locally ([c1b8535](https://github.com/BLSQ/openhexa-sdk-python/commit/c1b853598c8086200166edc63cb93b78860dab40))
* Fix local workspace.yaml path ([#46](https://github.com/BLSQ/openhexa-sdk-python/issues/46)) ([b625d69](https://github.com/BLSQ/openhexa-sdk-python/commit/b625d6994c97b2ae464f565ba4a6c5926ba715fc))
* fixes the default value to be of type list ([#211](https://github.com/BLSQ/openhexa-sdk-python/issues/211)) ([151e3af](https://github.com/BLSQ/openhexa-sdk-python/commit/151e3af419d5ea142781ce306c6c5bad3dc36239))
* **Logs:** convert log message to str ([#40](https://github.com/BLSQ/openhexa-sdk-python/issues/40)) ([bc31dfb](https://github.com/BLSQ/openhexa-sdk-python/commit/bc31dfbfcbc474bfcd0af51007e121ffece2b2a2))
* more robust task status check when stepping DAG  ([#38](https://github.com/BLSQ/openhexa-sdk-python/issues/38)) ([63cfeaf](https://github.com/BLSQ/openhexa-sdk-python/commit/63cfeaf5e3d4db2167894ef6f6d8f48f4142967e))
* Only add debugging ports when it's enabled ([4a9f17d](https://github.com/BLSQ/openhexa-sdk-python/commit/4a9f17d862225f8c66742bf39c1ee8c3442ac140))
* **Parameter:** check if default value is in choices ([#123](https://github.com/BLSQ/openhexa-sdk-python/issues/123)) ([726df4e](https://github.com/BLSQ/openhexa-sdk-python/commit/726df4ef94a556552778baa09262aad0537e4f49))
* **Parameters:** add support for custom connection ([#116](https://github.com/BLSQ/openhexa-sdk-python/issues/116)) ([65db931](https://github.com/BLSQ/openhexa-sdk-python/commit/65db93107d1c6a46d4f5af46171490b39722521f))
* **Parameter:** Validate parameter's code ([ce699b4](https://github.com/BLSQ/openhexa-sdk-python/commit/ce699b4bd77a6d09a048c5e4a57567fa6b3a6fec))
* **Parameter:** Validate parameter's code ([4d7d666](https://github.com/BLSQ/openhexa-sdk-python/commit/4d7d66674ad78d93cc67386e15097d118ddb9950))
* **Pipelines:** prevent upload of workspace folder content ([#68](https://github.com/BLSQ/openhexa-sdk-python/issues/68)) ([957c277](https://github.com/BLSQ/openhexa-sdk-python/commit/957c277b5348ac07dd7594879703ce0b0b3b09c0))
* **Pipelines:** set timeout when uploading a version ([#72](https://github.com/BLSQ/openhexa-sdk-python/issues/72)) ([7703794](https://github.com/BLSQ/openhexa-sdk-python/commit/77037943405406673ab5e2612fb1287fa3e19742))
* **Pipeline:** Store the pipeline name ([f8738d1](https://github.com/BLSQ/openhexa-sdk-python/commit/f8738d12e519177f322ee9448cfa0371635b3244))
* Prevent saving pipeline versions with the same name ([#220](https://github.com/BLSQ/openhexa-sdk-python/issues/220)) ([93e597e](https://github.com/BLSQ/openhexa-sdk-python/commit/93e597e2962b1901b01794a21c051127e02cf525))
* print something understandable when using add_file_output locally ([fddbbbd](https://github.com/BLSQ/openhexa-sdk-python/commit/fddbbbdb1f3aa2676d4f0ee25c142efb15cec27f))
* print something understandable when using add_file_output locally ([ce77c1c](https://github.com/BLSQ/openhexa-sdk-python/commit/ce77c1c79e1a558bf3d352c32d5603ee559a0f91))
* Proper error messages for arguments and missing config file ([#51](https://github.com/BLSQ/openhexa-sdk-python/issues/51)) ([07a5027](https://github.com/BLSQ/openhexa-sdk-python/commit/07a5027fb6be317d6f3e666dd6b0d145b8573358))
* **read_content:** bineary files do not take an encoding ([5448287](https://github.com/BLSQ/openhexa-sdk-python/commit/5448287a0e373ffa422028c6288d475c029faa29))
* remove duplicated instruction ([137a90d](https://github.com/BLSQ/openhexa-sdk-python/commit/137a90df0e9d2bd6db01161d285414e1eaa67d2d))
* Remove slash from api_url ([#219](https://github.com/BLSQ/openhexa-sdk-python/issues/219)) ([965ba0b](https://github.com/BLSQ/openhexa-sdk-python/commit/965ba0bfe970db30e3908e52ac3bb76f3aee7c9d))
* **Run:** In local runs using docker, the configuration from the workspace.yaml should not be parsed and loaded ([e4bb7a3](https://github.com/BLSQ/openhexa-sdk-python/commit/e4bb7a37cae0df31c9978d5d2c3b1b78f0fdeb69))
* **Skeleton:** Add '--yes' to the push action to create the pipeline by default ([0013039](https://github.com/BLSQ/openhexa-sdk-python/commit/0013039bcb61288e567f13aba8a3b42659f9721f))
* **Templates:** Do not abort when the user do not want to create a template version ([#229](https://github.com/BLSQ/openhexa-sdk-python/issues/229)) ([71d40b2](https://github.com/BLSQ/openhexa-sdk-python/commit/71d40b2c55e062accc8ea3bc6f8efe0ee2ac6806))
* **typing:** Add all accepted types ([96d4170](https://github.com/BLSQ/openhexa-sdk-python/commit/96d4170fe7301e6931bf98826fe49e90fe4bfc2b))
* Update readme.md to upgrade the lib on install ([51a7fb7](https://github.com/BLSQ/openhexa-sdk-python/commit/51a7fb7860d434f897e84652aeffa86e1c2a8c79))
* **urllib:** Use urllib &lt; 2 to avoid problemw with openssl being not uptodate ([#160](https://github.com/BLSQ/openhexa-sdk-python/issues/160)) ([bb0c98a](https://github.com/BLSQ/openhexa-sdk-python/commit/bb0c98a51a36671019611f1f9d92a3f428a83525))
* use proper namespace package setup ([#53](https://github.com/BLSQ/openhexa-sdk-python/issues/53)) ([81fc51e](https://github.com/BLSQ/openhexa-sdk-python/commit/81fc51e9256d55ac68274c204432582490c37a3a))
* Users are warned when pushing a pipeline with a code and a name or 'code=' ([1bd0039](https://github.com/BLSQ/openhexa-sdk-python/commit/1bd0039ca79a9896f5c2a3cd932b22ad3882292f))
* **Utils:** run pipeline config with right path ([99cd6f2](https://github.com/BLSQ/openhexa-sdk-python/commit/99cd6f2e8825609b77f8d03ad9b579379aa3cdb6))


### Documentation

* Add docstrings for [@pipeline](https://github.com/pipeline) and [@parameter](https://github.com/parameter) ([#70](https://github.com/BLSQ/openhexa-sdk-python/issues/70)) ([6282a50](https://github.com/BLSQ/openhexa-sdk-python/commit/6282a50328e2cb2f47c1c85c4105d5451f7e6477))
* update parameter supported types ([#90](https://github.com/BLSQ/openhexa-sdk-python/issues/90)) ([b3b6740](https://github.com/BLSQ/openhexa-sdk-python/commit/b3b6740678833efe0959ff1bef94ae1d70be5b58))


### Miscellaneous Chores

* Release v2.0.1 ([087d3cd](https://github.com/BLSQ/openhexa-sdk-python/commit/087d3cd9b50fd38c0e6b6246de90398bb6378c4c))
* Release v2.0.1 ([#235](https://github.com/BLSQ/openhexa-sdk-python/issues/235)) ([329493a](https://github.com/BLSQ/openhexa-sdk-python/commit/329493a3049d01128a8d6b9980c33e3e5431de79))
* Release v2.0.2 ([cb5a14d](https://github.com/BLSQ/openhexa-sdk-python/commit/cb5a14d34c9b6a269c50a7e07b67acff0f51ff4a))

## [2.0.1](https://github.com/BLSQ/openhexa-sdk-python/compare/v2.0.0...v2.0.1) (2025-03-11)


### Miscellaneous Chores

* Release v2.0.1 ([#235](https://github.com/BLSQ/openhexa-sdk-python/issues/235)) ([329493a](https://github.com/BLSQ/openhexa-sdk-python/commit/329493a3049d01128a8d6b9980c33e3e5431de79))

## [2.0.0](https://github.com/BLSQ/openhexa-sdk-python/compare/v1.1.0...v2.0.0) (2025-03-07)


### ⚠ BREAKING CHANGES

* Deprecate pipeline code and allow to select the target pipeline when pushing(HEXA-1170) ([#227](https://github.com/BLSQ/openhexa-sdk-python/issues/227))

### Features

* Deprecate pipeline code and allow to select the target pipeline when pushing(HEXA-1170) ([#227](https://github.com/BLSQ/openhexa-sdk-python/issues/227)) ([fd5ccac](https://github.com/BLSQ/openhexa-sdk-python/commit/fd5ccace020fc00116d886b975a3fd70e972d03d))


### Bug Fixes

* **code:** Inform users when they try to push a pipeline with a 'code' ([5b2f991](https://github.com/BLSQ/openhexa-sdk-python/commit/5b2f9910919ca310d0832eae3ba828ffff7f4884))
* **Templates:** Do not abort when the user do not want to create a template version ([#229](https://github.com/BLSQ/openhexa-sdk-python/issues/229)) ([71d40b2](https://github.com/BLSQ/openhexa-sdk-python/commit/71d40b2c55e062accc8ea3bc6f8efe0ee2ac6806))
* Users are warned when pushing a pipeline with a code and a name or 'code=' ([1bd0039](https://github.com/BLSQ/openhexa-sdk-python/commit/1bd0039ca79a9896f5c2a3cd932b22ad3882292f))

## [1.1.0](https://github.com/BLSQ/openhexa-sdk-python/compare/v1.0.0...v1.1.0) (2025-02-18)


### Features

* **Parameter:** HEXA-1134 adds dhis2 parameters widget and connection fields plus validation ([#225](https://github.com/BLSQ/openhexa-sdk-python/issues/225)) ([c1b703c](https://github.com/BLSQ/openhexa-sdk-python/commit/c1b703cc0a942da000093eccd18edf26936afd6b))
* Support template version creation on push (HEXA-1182) ([#226](https://github.com/BLSQ/openhexa-sdk-python/issues/226)) ([45a61be](https://github.com/BLSQ/openhexa-sdk-python/commit/45a61be06ca1e8333383b612eb384cd2d70203ad))


### Bug Fixes

* **deps:** update dependency urllib3 to v2 ([#217](https://github.com/BLSQ/openhexa-sdk-python/issues/217)) ([8d93d99](https://github.com/BLSQ/openhexa-sdk-python/commit/8d93d993a3fb2a6260bb1e5154fff9de12428749))

## [1.0.0](https://github.com/BLSQ/openhexa-sdk-python/compare/v0.3.1...v1.0.0) (2024-12-09)


### ⚠ BREAKING CHANGES

* Set a default version number for each pipeline version, make version name optional ([#221](https://github.com/BLSQ/openhexa-sdk-python/issues/221))

### Features

* conditionally run pipelines in debug mode ([#223](https://github.com/BLSQ/openhexa-sdk-python/issues/223)) ([6f495f7](https://github.com/BLSQ/openhexa-sdk-python/commit/6f495f79d90c64bf1b7729b4b570af1fa5bdb925))
* Set a default version number for each pipeline version, make version name optional ([#221](https://github.com/BLSQ/openhexa-sdk-python/issues/221)) ([488b290](https://github.com/BLSQ/openhexa-sdk-python/commit/488b2906a3d9948d6c86de8cdf4d998ec8e8bc47))


### Bug Fixes

* **Connections:** fix shallow matching when retrieving connection fields ([#209](https://github.com/BLSQ/openhexa-sdk-python/issues/209)) ([0bfd5f7](https://github.com/BLSQ/openhexa-sdk-python/commit/0bfd5f7d6f56f9e061551d85343e9389d827cf79))
* **deps:** update dependency pytest-cov to v6 ([#218](https://github.com/BLSQ/openhexa-sdk-python/issues/218)) ([47a78e5](https://github.com/BLSQ/openhexa-sdk-python/commit/47a78e5917ecab473c19f5b792bec94e1665f0c9))
* fixes the default value to be of type list ([#211](https://github.com/BLSQ/openhexa-sdk-python/issues/211)) ([151e3af](https://github.com/BLSQ/openhexa-sdk-python/commit/151e3af419d5ea142781ce306c6c5bad3dc36239))
* Prevent saving pipeline versions with the same name ([#220](https://github.com/BLSQ/openhexa-sdk-python/issues/220)) ([93e597e](https://github.com/BLSQ/openhexa-sdk-python/commit/93e597e2962b1901b01794a21c051127e02cf525))
* Remove slash from api_url ([#219](https://github.com/BLSQ/openhexa-sdk-python/issues/219)) ([965ba0b](https://github.com/BLSQ/openhexa-sdk-python/commit/965ba0bfe970db30e3908e52ac3bb76f3aee7c9d))

## [0.3.1](https://github.com/BLSQ/openhexa-sdk-python/compare/v0.3.0...v0.3.1) (2024-09-05)


### Bug Fixes

* **Datasets:** Use the correct mutation to upload files in datasets : generateDatasetUploadUrl ([d4d56d6](https://github.com/BLSQ/openhexa-sdk-python/commit/d4d56d6600912653eddbcce5b230d9c81f7ab3a3))

## [0.3.0](https://github.com/BLSQ/openhexa-sdk-python/compare/0.2.0...v0.3.0) (2024-08-28)


### Features

* add a retry mechanism for API call ([#166](https://github.com/BLSQ/openhexa-sdk-python/issues/166)) ([3d89da3](https://github.com/BLSQ/openhexa-sdk-python/commit/3d89da3f5efd690b1505b0130ec23b70ac3f455d))
* Add jinja2 templates, add github workflow ([7f53c6a](https://github.com/BLSQ/openhexa-sdk-python/commit/7f53c6a281eab59d3e559c50f57f283844300252))
* Add support for Python 3.11 ([#87](https://github.com/BLSQ/openhexa-sdk-python/issues/87)) ([03aa815](https://github.com/BLSQ/openhexa-sdk-python/commit/03aa8157896f92afdd5eadf7eeae3ad73741b633))
* Add tmp_path property on workspace ([#83](https://github.com/BLSQ/openhexa-sdk-python/issues/83)) ([c944b6d](https://github.com/BLSQ/openhexa-sdk-python/commit/c944b6d8d6cea6bfcb1e1e1974ec06c8f47609c2))
* Check that docker exists and is running ([#136](https://github.com/BLSQ/openhexa-sdk-python/issues/136)) ([3d4d75f](https://github.com/BLSQ/openhexa-sdk-python/commit/3d4d75f5b79d0fd7b5288b5447c4e538a5a7844a))
* **CI/CD:** adds github action v4 config ([ce8f848](https://github.com/BLSQ/openhexa-sdk-python/commit/ce8f8487dee48c2df32c2eab81723fa2cc514529))
* **CLI:** check if permission_denied is thrown ([#129](https://github.com/BLSQ/openhexa-sdk-python/issues/129)) ([2f856fe](https://github.com/BLSQ/openhexa-sdk-python/commit/2f856fe5927e7fe30456b9ff7fee57a12491c827))
* **CLI:** Use blsq/openhexa-blsq-environment as the image to run the pipeline ([#115](https://github.com/BLSQ/openhexa-sdk-python/issues/115)) ([c813e3a](https://github.com/BLSQ/openhexa-sdk-python/commit/c813e3a1bc44a3ad8524326bfc3cdf4abca92cde))
* **CLI:** User can add --yes to the  command to not have to confirm the creation of the pipeline ([85a9098](https://github.com/BLSQ/openhexa-sdk-python/commit/85a9098e72a3889879ad4723ffea94c773a6178b))
* **CLI:** User can provide a name, description and link of the pipel… ([#142](https://github.com/BLSQ/openhexa-sdk-python/issues/142)) ([45fd2e7](https://github.com/BLSQ/openhexa-sdk-python/commit/45fd2e7cd70ebc1000509ab50eb4d31a5c567200))
* **Connections:** add support for IASO connection ([#82](https://github.com/BLSQ/openhexa-sdk-python/issues/82)) ([707b798](https://github.com/BLSQ/openhexa-sdk-python/commit/707b798ac6e8fc7846a241f3d05ef760b224ce45))
* **Connections:** import and re-export connection classes in openhexa.sdk ([#93](https://github.com/BLSQ/openhexa-sdk-python/issues/93)) ([2e3db63](https://github.com/BLSQ/openhexa-sdk-python/commit/2e3db639d2a2ef0b6b27e15eca0970457e6822bb))
* **Dataset:** Create dataset with the SDK ([#110](https://github.com/BLSQ/openhexa-sdk-python/issues/110)) ([cba3e7e](https://github.com/BLSQ/openhexa-sdk-python/commit/cba3e7e861487204a534295492ee93e3c118387c))
* **DatasetFiles:** add helper to check if file exists ([c76d890](https://github.com/BLSQ/openhexa-sdk-python/commit/c76d8905a5e21785107257361c843a2be60da895))
* **Datasets:** Add datasets support to SDK ([#77](https://github.com/BLSQ/openhexa-sdk-python/issues/77)) ([d8eb50e](https://github.com/BLSQ/openhexa-sdk-python/commit/d8eb50e9210f7f610fd4e210dc17daf5331b8e97))
* delete pipeline ([#91](https://github.com/BLSQ/openhexa-sdk-python/issues/91)) ([549f73d](https://github.com/BLSQ/openhexa-sdk-python/commit/549f73d55cf3ddab6e1788ec78d484c4078ea85f))
* **Parameter:** add support for Dataset parameter type ([#120](https://github.com/BLSQ/openhexa-sdk-python/issues/120)) ([783b672](https://github.com/BLSQ/openhexa-sdk-python/commit/783b67208d21f5a226ebb6f65d1f35dfe6da6d3d))
* **Pipelines:** allow user to define a timeout for pipelines ([0eeab40](https://github.com/BLSQ/openhexa-sdk-python/commit/0eeab4064d38422b38f31a4cf70d3d8b823d2702))
* **Pipelines:** Allow user to download the latest version of a pipeline ([#128](https://github.com/BLSQ/openhexa-sdk-python/issues/128)) ([2dae69d](https://github.com/BLSQ/openhexa-sdk-python/commit/2dae69da69d4742b844f4b8e0c0e5b4e999da41d))
* **Pipelines:** prevent push of version  with params for scheduled pipeline. ([#55](https://github.com/BLSQ/openhexa-sdk-python/issues/55)) ([b9de756](https://github.com/BLSQ/openhexa-sdk-python/commit/b9de756f4dc94296bc427b2dd3337740909399ed))
* **Pipeline:** Use the AST to get the specs of the pipeline and its parameters ([#130](https://github.com/BLSQ/openhexa-sdk-python/issues/130)) ([9515499](https://github.com/BLSQ/openhexa-sdk-python/commit/951549925fae7ace4bf26a1922dea7f7738c6982))
* **Run:** Run pipelines with the debugger ready to be used ([a67d0fe](https://github.com/BLSQ/openhexa-sdk-python/commit/a67d0fe6eeba0c97cb2513b5c9d6fb9a2b5d8690))
* **Run:** Run pipelines with the debugger ready to be used ([#157](https://github.com/BLSQ/openhexa-sdk-python/issues/157)) ([754c21b](https://github.com/BLSQ/openhexa-sdk-python/commit/754c21b4888b69ee7feb6f80beaf672520539f52))
* **Run:** Run pipelines with the debugger ready to be used ([#157](https://github.com/BLSQ/openhexa-sdk-python/issues/157)) ([6863173](https://github.com/BLSQ/openhexa-sdk-python/commit/686317301b7ec9e1c83ec8ce7bb2c58a0f9b4021))
* Update SDK version in Dockerfile ([#57](https://github.com/BLSQ/openhexa-sdk-python/issues/57)) ([208d7ea](https://github.com/BLSQ/openhexa-sdk-python/commit/208d7ea561417bf9dc106d3b545254ecbde863db))
* Use a new way to load settings ([#131](https://github.com/BLSQ/openhexa-sdk-python/issues/131)) ([9619673](https://github.com/BLSQ/openhexa-sdk-python/commit/9619673f226149915afb73387ed8e0f8891ed520))
* **Workspaces:** allow user to specify workspace docker image ([#95](https://github.com/BLSQ/openhexa-sdk-python/issues/95)) ([2455a3e](https://github.com/BLSQ/openhexa-sdk-python/commit/2455a3e2eb136e94e543e8b1c8a44fa329bf9769))
* **Workspaces:** get connections from graphql API ([#158](https://github.com/BLSQ/openhexa-sdk-python/issues/158)) ([bba409b](https://github.com/BLSQ/openhexa-sdk-python/commit/bba409b7d241993c124100f34b7b64b899fa423b))
* **Workspaces:** list datasets in a workspace ([#112](https://github.com/BLSQ/openhexa-sdk-python/issues/112)) ([916832a](https://github.com/BLSQ/openhexa-sdk-python/commit/916832a44bae906cfe0a2706bf90c8057ab1b43f))


### Bug Fixes

* **API:** uploading a version now returns a pipelineVersion instead of a version ([5f89738](https://github.com/BLSQ/openhexa-sdk-python/commit/5f89738f803a391dd39f3a88a4e3ae7bb19f2860))
* **Build:** Manifest.in was missing the .github folder ([8afa0eb](https://github.com/BLSQ/openhexa-sdk-python/commit/8afa0eb4560f3ca4663850b4fb7860fa995dbe5f))
* **ci:** Fix python3.9 tests ([3d9aa95](https://github.com/BLSQ/openhexa-sdk-python/commit/3d9aa955262e19ba549d160d2f650a7ac7403ddb))
* **CLI:** Ask the user to create the workspace.yaml if not found ([#109](https://github.com/BLSQ/openhexa-sdk-python/issues/109)) ([1da1a04](https://github.com/BLSQ/openhexa-sdk-python/commit/1da1a049f1c91fa8ff0e8389528b0a904f31c661))
* **CLI:** Check if args of decorators are of a primitive type ([#146](https://github.com/BLSQ/openhexa-sdk-python/issues/146)) ([3ca0f51](https://github.com/BLSQ/openhexa-sdk-python/commit/3ca0f51af415680da7c31188c9340e09fcfefc2b))
* **CLI:** Do not ask to create the pipeline if the user has said yes as param ([6597876](https://github.com/BLSQ/openhexa-sdk-python/commit/6597876ded1e900599d33fbe17083e307805d39f))
* **CLI:** Do not require a config even if it's empty ([#50](https://github.com/BLSQ/openhexa-sdk-python/issues/50)) ([8e1098f](https://github.com/BLSQ/openhexa-sdk-python/commit/8e1098fc544918aaf78e1eb821e2b5540ba6c42e))
* **Cli:** no error is thrown when workspace doesn't exist ([#153](https://github.com/BLSQ/openhexa-sdk-python/issues/153)) ([fbbec07](https://github.com/BLSQ/openhexa-sdk-python/commit/fbbec07bc27ad6e53cd8f15bd68c701f4b702c76))
* **Cli:** no error is thrown when workspace doesn't exist ([#153](https://github.com/BLSQ/openhexa-sdk-python/issues/153)) ([cefc69c](https://github.com/BLSQ/openhexa-sdk-python/commit/cefc69c15f8abd2b27e3e4d9ba3b88507537f296))
* **CLI:** Notebook pipelines make the pipelines list to crash ([374c8fb](https://github.com/BLSQ/openhexa-sdk-python/commit/374c8fbfe332cb4c1876d1497b8b6f098ced9573))
* **CLI:** Running a pipeline should not require an active workspace ([#126](https://github.com/BLSQ/openhexa-sdk-python/issues/126)) ([7618d91](https://github.com/BLSQ/openhexa-sdk-python/commit/7618d918ebe701de41191dfe58196c3118f0bd9f))
* **Conda:** Copy stringcase package into our repo ([e6345b2](https://github.com/BLSQ/openhexa-sdk-python/commit/e6345b23b60260c5db957faa70caf606ea623476))
* **Conda:** Update requirements conditions ([7d01ad3](https://github.com/BLSQ/openhexa-sdk-python/commit/7d01ad36988862dda64b5e9913cd0c87e53a42b9))
* **Connections:** hide sensitive informations when printing  connection ([#79](https://github.com/BLSQ/openhexa-sdk-python/issues/79)) ([db749a3](https://github.com/BLSQ/openhexa-sdk-python/commit/db749a3d1d9119c95013030d390d8ecf568d5b26))
* **Connections:** Rename 'slug' to 'identifier' ([7f52ce4](https://github.com/BLSQ/openhexa-sdk-python/commit/7f52ce43309546a614bb71041146d42aa3c0e92a))
* **Connections:** Set the slug to lowercase before building the env var ([7f52ce4](https://github.com/BLSQ/openhexa-sdk-python/commit/7f52ce43309546a614bb71041146d42aa3c0e92a))
* **Connections:** specify connection workspace ([#170](https://github.com/BLSQ/openhexa-sdk-python/issues/170)) ([f8b2dda](https://github.com/BLSQ/openhexa-sdk-python/commit/f8b2ddabf17022661418ca3ec7d22dab51b3aa51))
* **Connections:** use lowercase for identifier ([#184](https://github.com/BLSQ/openhexa-sdk-python/issues/184)) ([a864629](https://github.com/BLSQ/openhexa-sdk-python/commit/a864629fd21cabb1ea0918cee974ae71e36a42b7))
* copies files correctly to workspace directory ([f6a19b2](https://github.com/BLSQ/openhexa-sdk-python/commit/f6a19b2f61b2a997822110f473846520495a3943))
* copy workspace folder to correct path ([6a1a6a4](https://github.com/BLSQ/openhexa-sdk-python/commit/6a1a6a4b456d320709f0e4c491171f01489a82b6))
* **CurrentRun:** check if file exist when adding output ([#114](https://github.com/BLSQ/openhexa-sdk-python/issues/114)) ([4dfe8d1](https://github.com/BLSQ/openhexa-sdk-python/commit/4dfe8d12d56ed2d66007a90b48372adb0b5ac3d3))
* **dataset:** Support bytes directly in read_content ([#111](https://github.com/BLSQ/openhexa-sdk-python/issues/111)) ([e83eefb](https://github.com/BLSQ/openhexa-sdk-python/commit/e83eefba04713db3c38749395a043e6dfb58a977))
* Do not crash the CLI when some pipelines do not have a current version ([3b8cd5c](https://github.com/BLSQ/openhexa-sdk-python/commit/3b8cd5ce0d9bc03fbbc308db21394eb48a061eb9))
* Do not make two requests to the server to check if the pipeline exists ([#94](https://github.com/BLSQ/openhexa-sdk-python/issues/94)) ([4501bda](https://github.com/BLSQ/openhexa-sdk-python/commit/4501bdadf2ba6627f9c718a15c7036df5783044b))
* **Docker:** Always force pull the image ([#103](https://github.com/BLSQ/openhexa-sdk-python/issues/103)) ([c538e10](https://github.com/BLSQ/openhexa-sdk-python/commit/c538e109e05b541d0e70dec8196e564338afd6db))
* **Docker:** Disable healthchecks when running the pipeline locally ([c1b8535](https://github.com/BLSQ/openhexa-sdk-python/commit/c1b853598c8086200166edc63cb93b78860dab40))
* Only add debugging ports when it's enabled ([4a9f17d](https://github.com/BLSQ/openhexa-sdk-python/commit/4a9f17d862225f8c66742bf39c1ee8c3442ac140))
* **Parameter:** check if default value is in choices ([#123](https://github.com/BLSQ/openhexa-sdk-python/issues/123)) ([726df4e](https://github.com/BLSQ/openhexa-sdk-python/commit/726df4ef94a556552778baa09262aad0537e4f49))
* **Parameters:** add support for custom connection ([#116](https://github.com/BLSQ/openhexa-sdk-python/issues/116)) ([65db931](https://github.com/BLSQ/openhexa-sdk-python/commit/65db93107d1c6a46d4f5af46171490b39722521f))
* **Pipelines:** prevent upload of workspace folder content ([#68](https://github.com/BLSQ/openhexa-sdk-python/issues/68)) ([957c277](https://github.com/BLSQ/openhexa-sdk-python/commit/957c277b5348ac07dd7594879703ce0b0b3b09c0))
* **Pipelines:** set timeout when uploading a version ([#72](https://github.com/BLSQ/openhexa-sdk-python/issues/72)) ([7703794](https://github.com/BLSQ/openhexa-sdk-python/commit/77037943405406673ab5e2612fb1287fa3e19742))
* Proper error messages for arguments and missing config file ([#51](https://github.com/BLSQ/openhexa-sdk-python/issues/51)) ([07a5027](https://github.com/BLSQ/openhexa-sdk-python/commit/07a5027fb6be317d6f3e666dd6b0d145b8573358))
* **read_content:** bineary files do not take an encoding ([5448287](https://github.com/BLSQ/openhexa-sdk-python/commit/5448287a0e373ffa422028c6288d475c029faa29))
* remove duplicated instruction ([137a90d](https://github.com/BLSQ/openhexa-sdk-python/commit/137a90df0e9d2bd6db01161d285414e1eaa67d2d))
* **Run:** In local runs using docker, the configuration from the workspace.yaml should not be parsed and loaded ([e4bb7a3](https://github.com/BLSQ/openhexa-sdk-python/commit/e4bb7a37cae0df31c9978d5d2c3b1b78f0fdeb69))
* **Skeleton:** Add '--yes' to the push action to create the pipeline by default ([0013039](https://github.com/BLSQ/openhexa-sdk-python/commit/0013039bcb61288e567f13aba8a3b42659f9721f))
* **typing:** Add all accepted types ([96d4170](https://github.com/BLSQ/openhexa-sdk-python/commit/96d4170fe7301e6931bf98826fe49e90fe4bfc2b))
* **urllib:** Use urllib &lt; 2 to avoid problemw with openssl being not uptodate ([#160](https://github.com/BLSQ/openhexa-sdk-python/issues/160)) ([bb0c98a](https://github.com/BLSQ/openhexa-sdk-python/commit/bb0c98a51a36671019611f1f9d92a3f428a83525))
* use proper namespace package setup ([#53](https://github.com/BLSQ/openhexa-sdk-python/issues/53)) ([81fc51e](https://github.com/BLSQ/openhexa-sdk-python/commit/81fc51e9256d55ac68274c204432582490c37a3a))
* **Utils:** run pipeline config with right path ([99cd6f2](https://github.com/BLSQ/openhexa-sdk-python/commit/99cd6f2e8825609b77f8d03ad9b579379aa3cdb6))


### Documentation

* Add docstrings for [@pipeline](https://github.com/pipeline) and [@parameter](https://github.com/parameter) ([#70](https://github.com/BLSQ/openhexa-sdk-python/issues/70)) ([6282a50](https://github.com/BLSQ/openhexa-sdk-python/commit/6282a50328e2cb2f47c1c85c4105d5451f7e6477))
* update parameter supported types ([#90](https://github.com/BLSQ/openhexa-sdk-python/issues/90)) ([b3b6740](https://github.com/BLSQ/openhexa-sdk-python/commit/b3b6740678833efe0959ff1bef94ae1d70be5b58))

## [0.1.52](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.51...0.1.52) (2024-07-19)


### Miscellaneous

* **deps:** update setuptools requirement ([4547d32](https://github.com/BLSQ/openhexa-sdk-python/commit/4547d32ffac371fa8f2fed67031e30dd2db7582a))

## [0.1.51](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.50...0.1.51) (2024-06-28)


### Features

* add a retry mechanism for API call ([#166](https://github.com/BLSQ/openhexa-sdk-python/issues/166)) ([3d89da3](https://github.com/BLSQ/openhexa-sdk-python/commit/3d89da3f5efd690b1505b0130ec23b70ac3f455d))


### Bug Fixes

* **Connections:** use lowercase for identifier ([#184](https://github.com/BLSQ/openhexa-sdk-python/issues/184)) ([a864629](https://github.com/BLSQ/openhexa-sdk-python/commit/a864629fd21cabb1ea0918cee974ae71e36a42b7))


### Miscellaneous

* **deps:** update actions/setup-python action to v5 ([#177](https://github.com/BLSQ/openhexa-sdk-python/issues/177)) ([efc4253](https://github.com/BLSQ/openhexa-sdk-python/commit/efc42534aba155f08bcb3dd9c41d7c5925352e67))
* **deps:** update dependency dev/ruff to &gt;=0.5.0,&lt;0.6.0 ([#185](https://github.com/BLSQ/openhexa-sdk-python/issues/185)) ([a7d0657](https://github.com/BLSQ/openhexa-sdk-python/commit/a7d0657d2df7bd3b211cd0e310225bc422c53588))
* **deps:** update dependency examples/geopandas to v1 ([#178](https://github.com/BLSQ/openhexa-sdk-python/issues/178)) ([a580ba8](https://github.com/BLSQ/openhexa-sdk-python/commit/a580ba89a1394b344aae8c0b3b320dfd01a067d5))
* **deps:** update pre-commit/action action to v3 ([#183](https://github.com/BLSQ/openhexa-sdk-python/issues/183)) ([b48cb83](https://github.com/BLSQ/openhexa-sdk-python/commit/b48cb8398f38b26823902d02b8e3b4ff91354fcf))

## [0.1.50](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.49...0.1.50) (2024-06-25)


### Bug Fixes

* **CLI:** Notebook pipelines make the pipelines list to crash ([374c8fb](https://github.com/BLSQ/openhexa-sdk-python/commit/374c8fbfe332cb4c1876d1497b8b6f098ced9573))
* Do not crash the CLI when some pipelines do not have a current version ([3b8cd5c](https://github.com/BLSQ/openhexa-sdk-python/commit/3b8cd5ce0d9bc03fbbc308db21394eb48a061eb9))


### Miscellaneous

* Add renovate.json ([#172](https://github.com/BLSQ/openhexa-sdk-python/issues/172)) ([3571a43](https://github.com/BLSQ/openhexa-sdk-python/commit/3571a434ab094fcff6860e8cbc0e5dccdef446c5))
* **deps:** update actions/checkout action to v4 ([#175](https://github.com/BLSQ/openhexa-sdk-python/issues/175)) ([d1e3e9d](https://github.com/BLSQ/openhexa-sdk-python/commit/d1e3e9d38e9b428d573599ed3a605a0b18f9fe19))
* **deps:** update dependency dev/ruff to &gt;=0.4.10,&lt;0.5.0 ([#174](https://github.com/BLSQ/openhexa-sdk-python/issues/174)) ([f11a4bb](https://github.com/BLSQ/openhexa-sdk-python/commit/f11a4bb888863c21130d143d7550e03446b85120))
* **release-please:** Stop release-please workflows when a new one is created ([2e87701](https://github.com/BLSQ/openhexa-sdk-python/commit/2e87701d1b12a1cf437ea3ce1859527b1fbe1fe4))

## [0.1.49](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.48...0.1.49) (2024-06-25)


### Bug Fixes

* **Connections:** specify connection workspace ([#170](https://github.com/BLSQ/openhexa-sdk-python/issues/170)) ([f8b2dda](https://github.com/BLSQ/openhexa-sdk-python/commit/f8b2ddabf17022661418ca3ec7d22dab51b3aa51))

## [0.1.48](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.47...0.1.48) (2024-06-19)


### Bug Fixes

* **Conda:** Update requirements conditions ([7d01ad3](https://github.com/BLSQ/openhexa-sdk-python/commit/7d01ad36988862dda64b5e9913cd0c87e53a42b9))

## [0.1.47](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.46...0.1.47) (2024-06-18)


### Features

* **Workspaces:** get connections from graphql API ([#158](https://github.com/BLSQ/openhexa-sdk-python/issues/158)) ([bba409b](https://github.com/BLSQ/openhexa-sdk-python/commit/bba409b7d241993c124100f34b7b64b899fa423b))


### Bug Fixes

* **Conda:** Copy stringcase package into our repo ([e6345b2](https://github.com/BLSQ/openhexa-sdk-python/commit/e6345b23b60260c5db957faa70caf606ea623476))
* Only add debugging ports when it's enabled ([4a9f17d](https://github.com/BLSQ/openhexa-sdk-python/commit/4a9f17d862225f8c66742bf39c1ee8c3442ac140))

## [0.1.46](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.45...0.1.46) (2024-06-11)


### Bug Fixes

* **CLI:** Do not ask to create the pipeline if the user has said yes as param ([6597876](https://github.com/BLSQ/openhexa-sdk-python/commit/6597876ded1e900599d33fbe17083e307805d39f))
* **urllib:** Use urllib &lt; 2 to avoid problemw with openssl being not uptodate ([#160](https://github.com/BLSQ/openhexa-sdk-python/issues/160)) ([bb0c98a](https://github.com/BLSQ/openhexa-sdk-python/commit/bb0c98a51a36671019611f1f9d92a3f428a83525))

## [0.1.45](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.44...0.1.45) (2024-05-30)


### Features

* **Run:** Run pipelines with the debugger ready to be used ([a67d0fe](https://github.com/BLSQ/openhexa-sdk-python/commit/a67d0fe6eeba0c97cb2513b5c9d6fb9a2b5d8690))
* **Run:** Run pipelines with the debugger ready to be used ([#157](https://github.com/BLSQ/openhexa-sdk-python/issues/157)) ([754c21b](https://github.com/BLSQ/openhexa-sdk-python/commit/754c21b4888b69ee7feb6f80beaf672520539f52))
* **Run:** Run pipelines with the debugger ready to be used ([#157](https://github.com/BLSQ/openhexa-sdk-python/issues/157)) ([6863173](https://github.com/BLSQ/openhexa-sdk-python/commit/686317301b7ec9e1c83ec8ce7bb2c58a0f9b4021))


### Bug Fixes

* **Cli:** no error is thrown when workspace doesn't exist ([#153](https://github.com/BLSQ/openhexa-sdk-python/issues/153)) ([fbbec07](https://github.com/BLSQ/openhexa-sdk-python/commit/fbbec07bc27ad6e53cd8f15bd68c701f4b702c76))
* **Cli:** no error is thrown when workspace doesn't exist ([#153](https://github.com/BLSQ/openhexa-sdk-python/issues/153)) ([cefc69c](https://github.com/BLSQ/openhexa-sdk-python/commit/cefc69c15f8abd2b27e3e4d9ba3b88507537f296))


### Miscellaneous

* **deps:** bump docker from 7.0.0 to 7.1.0 ([#156](https://github.com/BLSQ/openhexa-sdk-python/issues/156)) ([e6cc226](https://github.com/BLSQ/openhexa-sdk-python/commit/e6cc226bae490bc1bb85453b6bed988464093c51))
* **deps:** bump docker from 7.0.0 to 7.1.0 ([#156](https://github.com/BLSQ/openhexa-sdk-python/issues/156)) ([377fca6](https://github.com/BLSQ/openhexa-sdk-python/commit/377fca606d6c51665cf4e60e1a9cae3d491421d3))

## [0.1.44](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.43...0.1.44) (2024-05-27)


### Bug Fixes

* **Docker:** Disable healthchecks when running the pipeline locally ([c1b8535](https://github.com/BLSQ/openhexa-sdk-python/commit/c1b853598c8086200166edc63cb93b78860dab40))


### Miscellaneous

* **deps:** bump jinja2 from 3.1.3 to 3.1.4 ([#151](https://github.com/BLSQ/openhexa-sdk-python/issues/151)) ([bee0be0](https://github.com/BLSQ/openhexa-sdk-python/commit/bee0be04536b35d5f7f43d9be6838a3e1ddd3c04))
* **deps:** update pytest requirement from &lt;8.2,&gt;=7.3 to >=7.3,<8.3 ([#150](https://github.com/BLSQ/openhexa-sdk-python/issues/150)) ([2536198](https://github.com/BLSQ/openhexa-sdk-python/commit/253619825113c2607bb683a9f59857f5b5ff3aa5))
* **deps:** update requests requirement from ~=2.31.0 to &gt;=2.31,&lt;2.33 ([#152](https://github.com/BLSQ/openhexa-sdk-python/issues/152)) ([0500b97](https://github.com/BLSQ/openhexa-sdk-python/commit/0500b97257aa150548ca4f6d79bee0f8b62a61de))
* **deps:** update setuptools requirement ([#148](https://github.com/BLSQ/openhexa-sdk-python/issues/148)) ([2c97d6f](https://github.com/BLSQ/openhexa-sdk-python/commit/2c97d6fcfb7f49765fd5ef4821e7c205e1741ee2))

## [0.1.43](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.42...0.1.43) (2024-04-10)


### Bug Fixes

* **API:** uploading a version now returns a pipelineVersion instead of a version ([5f89738](https://github.com/BLSQ/openhexa-sdk-python/commit/5f89738f803a391dd39f3a88a4e3ae7bb19f2860))
* **typing:** Add all accepted types ([96d4170](https://github.com/BLSQ/openhexa-sdk-python/commit/96d4170fe7301e6931bf98826fe49e90fe4bfc2b))


### Miscellaneous

* Check if a new version of the library is available and inform the user. ([495cda8](https://github.com/BLSQ/openhexa-sdk-python/commit/495cda8d6fb853f2bfad4265d1d10f868ec5bcca))

## [0.1.42](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.41...0.1.42) (2024-04-09)


### Features

* **CLI:** check if permission_denied is thrown ([#129](https://github.com/BLSQ/openhexa-sdk-python/issues/129)) ([2f856fe](https://github.com/BLSQ/openhexa-sdk-python/commit/2f856fe5927e7fe30456b9ff7fee57a12491c827))
* **CLI:** User can provide a name, description and link of the pipel… ([#142](https://github.com/BLSQ/openhexa-sdk-python/issues/142)) ([45fd2e7](https://github.com/BLSQ/openhexa-sdk-python/commit/45fd2e7cd70ebc1000509ab50eb4d31a5c567200))


### Bug Fixes

* **CLI:** Check if args of decorators are of a primitive type ([#146](https://github.com/BLSQ/openhexa-sdk-python/issues/146)) ([3ca0f51](https://github.com/BLSQ/openhexa-sdk-python/commit/3ca0f51af415680da7c31188c9340e09fcfefc2b))


### Miscellaneous

* **deps-dev:** update build requirement ([#144](https://github.com/BLSQ/openhexa-sdk-python/issues/144)) ([38ce2c3](https://github.com/BLSQ/openhexa-sdk-python/commit/38ce2c355b4ac8b5002976a549b22805cb836fd6))
* **deps-dev:** update pytest requirement from &lt;8.1,&gt;=7.3 to >=7.3,<8.2 ([#139](https://github.com/BLSQ/openhexa-sdk-python/issues/139)) ([51938c8](https://github.com/BLSQ/openhexa-sdk-python/commit/51938c80c83a72a1bc5cd6473271fcacc0df9696))
* **deps-dev:** update pytest-cov requirement ([#143](https://github.com/BLSQ/openhexa-sdk-python/issues/143)) ([c4ea0ef](https://github.com/BLSQ/openhexa-sdk-python/commit/c4ea0ef377b786f462ec6344085d999b405672fd))

## [0.1.41](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.40...0.1.41) (2024-04-02)


### Bug Fixes

* **Build:** Manifest.in was missing the .github folder ([8afa0eb](https://github.com/BLSQ/openhexa-sdk-python/commit/8afa0eb4560f3ca4663850b4fb7860fa995dbe5f))
* remove duplicated instruction ([137a90d](https://github.com/BLSQ/openhexa-sdk-python/commit/137a90df0e9d2bd6db01161d285414e1eaa67d2d))


### Miscellaneous

* **deps-dev:** bump jinja2 from 3.0.3 to 3.1.3 ([#138](https://github.com/BLSQ/openhexa-sdk-python/issues/138)) ([50d7843](https://github.com/BLSQ/openhexa-sdk-python/commit/50d7843614100b44090b65117afebbbbbbcc1c13))
* **deps-dev:** update build requirement ([#133](https://github.com/BLSQ/openhexa-sdk-python/issues/133)) ([182c3dd](https://github.com/BLSQ/openhexa-sdk-python/commit/182c3dd52cb39a3752631b9f38564d6bb748ece2))
* **deps-dev:** update ruff requirement ([#132](https://github.com/BLSQ/openhexa-sdk-python/issues/132)) ([bc96de1](https://github.com/BLSQ/openhexa-sdk-python/commit/bc96de11d5acb22698109fb6ec0d1ef00c22480a))
* **deps-dev:** update setuptools requirement ([#140](https://github.com/BLSQ/openhexa-sdk-python/issues/140)) ([96ae76e](https://github.com/BLSQ/openhexa-sdk-python/commit/96ae76ef65f047283be9bfef9585596cf2d74160))

## [0.1.40](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.39...0.1.40) (2024-03-11)


### Features

* Check that docker exists and is running ([#136](https://github.com/BLSQ/openhexa-sdk-python/issues/136)) ([3d4d75f](https://github.com/BLSQ/openhexa-sdk-python/commit/3d4d75f5b79d0fd7b5288b5447c4e538a5a7844a))


### Bug Fixes

* **Skeleton:** Add '--yes' to the push action to create the pipeline by default ([0013039](https://github.com/BLSQ/openhexa-sdk-python/commit/0013039bcb61288e567f13aba8a3b42659f9721f))

## [0.1.39](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.38...0.1.39) (2024-03-06)


### Features

* Add jinja2 templates, add github workflow ([7f53c6a](https://github.com/BLSQ/openhexa-sdk-python/commit/7f53c6a281eab59d3e559c50f57f283844300252))


### Bug Fixes

* **ci:** Fix python3.9 tests ([3d9aa95](https://github.com/BLSQ/openhexa-sdk-python/commit/3d9aa955262e19ba549d160d2f650a7ac7403ddb))

## [0.1.38](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.37...0.1.38) (2024-03-05)


### Features

* **Pipeline:** Use the AST to get the specs of the pipeline and its parameters ([#130](https://github.com/BLSQ/openhexa-sdk-python/issues/130)) ([9515499](https://github.com/BLSQ/openhexa-sdk-python/commit/951549925fae7ace4bf26a1922dea7f7738c6982))
* Use a new way to load settings ([#131](https://github.com/BLSQ/openhexa-sdk-python/issues/131)) ([9619673](https://github.com/BLSQ/openhexa-sdk-python/commit/9619673f226149915afb73387ed8e0f8891ed520))

## [0.1.37](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.36...0.1.37) (2024-02-20)


### Features

* **Parameter:** add support for Dataset parameter type ([#120](https://github.com/BLSQ/openhexa-sdk-python/issues/120)) ([783b672](https://github.com/BLSQ/openhexa-sdk-python/commit/783b67208d21f5a226ebb6f65d1f35dfe6da6d3d))
* **Pipelines:** Allow user to download the latest version of a pipeline ([#128](https://github.com/BLSQ/openhexa-sdk-python/issues/128)) ([2dae69d](https://github.com/BLSQ/openhexa-sdk-python/commit/2dae69da69d4742b844f4b8e0c0e5b4e999da41d))


### Bug Fixes

* **CLI:** Running a pipeline should not require an active workspace ([#126](https://github.com/BLSQ/openhexa-sdk-python/issues/126)) ([7618d91](https://github.com/BLSQ/openhexa-sdk-python/commit/7618d918ebe701de41191dfe58196c3118f0bd9f))
* **Parameter:** check if default value is in choices ([#123](https://github.com/BLSQ/openhexa-sdk-python/issues/123)) ([726df4e](https://github.com/BLSQ/openhexa-sdk-python/commit/726df4ef94a556552778baa09262aad0537e4f49))

## [0.1.36](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.35...0.1.36) (2024-01-30)


### Features

* **CLI:** User can add --yes to the  command to not have to confirm the creation of the pipeline ([85a9098](https://github.com/BLSQ/openhexa-sdk-python/commit/85a9098e72a3889879ad4723ffea94c773a6178b))


### Bug Fixes

* **CurrentRun:** check if file exist when adding output ([#114](https://github.com/BLSQ/openhexa-sdk-python/issues/114)) ([4dfe8d1](https://github.com/BLSQ/openhexa-sdk-python/commit/4dfe8d12d56ed2d66007a90b48372adb0b5ac3d3))


### Miscellaneous

* **deps-dev:** update geopandas requirement ([#121](https://github.com/BLSQ/openhexa-sdk-python/issues/121)) ([80f21cb](https://github.com/BLSQ/openhexa-sdk-python/commit/80f21cb5435b9626671f6bceec3ef8a16a40fbd3))
* **deps-dev:** update pandas requirement ([#117](https://github.com/BLSQ/openhexa-sdk-python/issues/117)) ([2270bef](https://github.com/BLSQ/openhexa-sdk-python/commit/2270befb55d29a2b95bd4310d58ee4e4fc3d191c))
* **deps-dev:** update pytest requirement from ~=7.3.0 to &gt;=7.3,&lt;8.1 ([#122](https://github.com/BLSQ/openhexa-sdk-python/issues/122)) ([94d867f](https://github.com/BLSQ/openhexa-sdk-python/commit/94d867fdb4a29163d9f69e6c549203d23dabe143))
* **deps:** update requests ([75301e9](https://github.com/BLSQ/openhexa-sdk-python/commit/75301e92e63d5c33b4be29798a6bf54e79d13fbc))

## [0.1.35](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.34...0.1.35) (2024-01-23)


### Features

* **CLI:** Use blsq/openhexa-blsq-environment as the image to run the pipeline ([#115](https://github.com/BLSQ/openhexa-sdk-python/issues/115)) ([c813e3a](https://github.com/BLSQ/openhexa-sdk-python/commit/c813e3a1bc44a3ad8524326bfc3cdf4abca92cde))


### Bug Fixes

* **Parameters:** add support for custom connection ([#116](https://github.com/BLSQ/openhexa-sdk-python/issues/116)) ([65db931](https://github.com/BLSQ/openhexa-sdk-python/commit/65db93107d1c6a46d4f5af46171490b39722521f))

## [0.1.34](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.33...0.1.34) (2024-01-16)


### Features

* **Dataset:** Create dataset with the SDK ([#110](https://github.com/BLSQ/openhexa-sdk-python/issues/110)) ([cba3e7e](https://github.com/BLSQ/openhexa-sdk-python/commit/cba3e7e861487204a534295492ee93e3c118387c))
* **Workspaces:** list datasets in a workspace ([#112](https://github.com/BLSQ/openhexa-sdk-python/issues/112)) ([916832a](https://github.com/BLSQ/openhexa-sdk-python/commit/916832a44bae906cfe0a2706bf90c8057ab1b43f))


### Bug Fixes

* **CLI:** Ask the user to create the workspace.yaml if not found ([#109](https://github.com/BLSQ/openhexa-sdk-python/issues/109)) ([1da1a04](https://github.com/BLSQ/openhexa-sdk-python/commit/1da1a049f1c91fa8ff0e8389528b0a904f31c661))
* **dataset:** Support bytes directly in read_content ([#111](https://github.com/BLSQ/openhexa-sdk-python/issues/111)) ([e83eefb](https://github.com/BLSQ/openhexa-sdk-python/commit/e83eefba04713db3c38749395a043e6dfb58a977))
* **Docker:** Always force pull the image ([#103](https://github.com/BLSQ/openhexa-sdk-python/issues/103)) ([c538e10](https://github.com/BLSQ/openhexa-sdk-python/commit/c538e109e05b541d0e70dec8196e564338afd6db))


### Miscellaneous

* **deps-dev:** update build requirement from ~=0.10.0 to &gt;=0.10,&lt;1.1 ([#99](https://github.com/BLSQ/openhexa-sdk-python/issues/99)) ([a15457e](https://github.com/BLSQ/openhexa-sdk-python/commit/a15457ef3436d708b173a6c21cd90ff558f30b20))
* **deps-dev:** update geopandas requirement from ~=0.12.2 to ~=0.14.2 ([#107](https://github.com/BLSQ/openhexa-sdk-python/issues/107)) ([a843015](https://github.com/BLSQ/openhexa-sdk-python/commit/a84301538d1d606e40a198eeafcbfd0f82c34d7e))
* **deps-dev:** update pandas requirement from ~=2.0.0 to ~=2.1.4 ([#105](https://github.com/BLSQ/openhexa-sdk-python/issues/105)) ([b8691d1](https://github.com/BLSQ/openhexa-sdk-python/commit/b8691d1d9db9b66b1f6bd7130c0bd3d28c3d384f))
* **deps-dev:** update pytest requirement from ~=7.3.0 to ~=7.4.4 ([#108](https://github.com/BLSQ/openhexa-sdk-python/issues/108)) ([f972373](https://github.com/BLSQ/openhexa-sdk-python/commit/f9723731bf3b98fb3f9155b09ef55548698a8c70))
* **deps-dev:** update pytest-cov requirement ([#97](https://github.com/BLSQ/openhexa-sdk-python/issues/97)) ([65568b9](https://github.com/BLSQ/openhexa-sdk-python/commit/65568b99e628ade197c833037efeccf74b73ae08))
* **deps-dev:** update rasterstats requirement ([#98](https://github.com/BLSQ/openhexa-sdk-python/issues/98)) ([e361c42](https://github.com/BLSQ/openhexa-sdk-python/commit/e361c426403316826a4fd6433a135a85f2d10886))
* **deps-dev:** update requests requirement ([#100](https://github.com/BLSQ/openhexa-sdk-python/issues/100)) ([e5d9f3d](https://github.com/BLSQ/openhexa-sdk-python/commit/e5d9f3da1eba7ecda0b204138288d1283c8e7c6a))
* **deps-dev:** update setuptools requirement ([#101](https://github.com/BLSQ/openhexa-sdk-python/issues/101)) ([6582ada](https://github.com/BLSQ/openhexa-sdk-python/commit/6582adab38dded7b2a4104459de541af3d3f3468))

## [0.1.33](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.32...0.1.33) (2023-12-12)


### Features

* **Workspaces:** allow user to specify workspace docker image ([#95](https://github.com/BLSQ/openhexa-sdk-python/issues/95)) ([2455a3e](https://github.com/BLSQ/openhexa-sdk-python/commit/2455a3e2eb136e94e543e8b1c8a44fa329bf9769))


### Bug Fixes

* Do not make two requests to the server to check if the pipeline exists ([#94](https://github.com/BLSQ/openhexa-sdk-python/issues/94)) ([4501bda](https://github.com/BLSQ/openhexa-sdk-python/commit/4501bdadf2ba6627f9c718a15c7036df5783044b))

## [0.1.32](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.31...0.1.32) (2023-12-04)


### Features

* **Connections:** import and re-export connection classes in openhexa.sdk ([#93](https://github.com/BLSQ/openhexa-sdk-python/issues/93)) ([2e3db63](https://github.com/BLSQ/openhexa-sdk-python/commit/2e3db639d2a2ef0b6b27e15eca0970457e6822bb))
* delete pipeline ([#91](https://github.com/BLSQ/openhexa-sdk-python/issues/91)) ([549f73d](https://github.com/BLSQ/openhexa-sdk-python/commit/549f73d55cf3ddab6e1788ec78d484c4078ea85f))

## [0.1.31](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.30...0.1.31) (2023-11-17)


### Features

* Add support for Python 3.11 ([#87](https://github.com/BLSQ/openhexa-sdk-python/issues/87)) ([03aa815](https://github.com/BLSQ/openhexa-sdk-python/commit/03aa8157896f92afdd5eadf7eeae3ad73741b633))

## [0.1.30](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.29...0.1.30) (2023-10-17)


### Features

* Add tmp_path property on workspace ([#83](https://github.com/BLSQ/openhexa-sdk-python/issues/83)) ([c944b6d](https://github.com/BLSQ/openhexa-sdk-python/commit/c944b6d8d6cea6bfcb1e1e1974ec06c8f47609c2))

## [0.1.29](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.28...0.1.29) (2023-09-30)


### Features

* **Connections:** add support for IASO connection ([#82](https://github.com/BLSQ/openhexa-sdk-python/issues/82)) ([707b798](https://github.com/BLSQ/openhexa-sdk-python/commit/707b798ac6e8fc7846a241f3d05ef760b224ce45))
* **Datasets:** Add datasets support to SDK ([#77](https://github.com/BLSQ/openhexa-sdk-python/issues/77)) ([d8eb50e](https://github.com/BLSQ/openhexa-sdk-python/commit/d8eb50e9210f7f610fd4e210dc17daf5331b8e97))


### Bug Fixes

* **Connections:** hide sensitive informations when printing  connection ([#79](https://github.com/BLSQ/openhexa-sdk-python/issues/79)) ([db749a3](https://github.com/BLSQ/openhexa-sdk-python/commit/db749a3d1d9119c95013030d390d8ecf568d5b26))
* **read_content:** bineary files do not take an encoding ([5448287](https://github.com/BLSQ/openhexa-sdk-python/commit/5448287a0e373ffa422028c6288d475c029faa29))


### Miscellaneous

* Reame dataset methods ([5c087fc](https://github.com/BLSQ/openhexa-sdk-python/commit/5c087fcb6c5e2b8b8b561bf108f5396079bb15c3))

## [0.1.28](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.27...0.1.28) (2023-08-14)


### Bug Fixes

* **Pipelines:** set timeout when uploading a version ([#72](https://github.com/BLSQ/openhexa-sdk-python/issues/72)) ([7703794](https://github.com/BLSQ/openhexa-sdk-python/commit/77037943405406673ab5e2612fb1287fa3e19742))

## [0.1.27](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.26...0.1.27) (2023-08-10)


### Bug Fixes

* **Pipelines:** prevent upload of workspace folder content ([#68](https://github.com/BLSQ/openhexa-sdk-python/issues/68)) ([957c277](https://github.com/BLSQ/openhexa-sdk-python/commit/957c277b5348ac07dd7594879703ce0b0b3b09c0))


### Miscellaneous

* Remove pipelines image doc in readme.md ([62725a7](https://github.com/BLSQ/openhexa-sdk-python/commit/62725a7807615859230e15f3b7d318c77c3fcd88))

## [0.1.26](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.25...0.1.26) (2023-08-08)


### Features

* **Pipelines:** allow user to define a timeout for pipelines ([0eeab40](https://github.com/BLSQ/openhexa-sdk-python/commit/0eeab4064d38422b38f31a4cf70d3d8b823d2702))


### Bug Fixes

* **Connections:** Rename 'slug' to 'identifier' ([7f52ce4](https://github.com/BLSQ/openhexa-sdk-python/commit/7f52ce43309546a614bb71041146d42aa3c0e92a))
* **Connections:** Set the slug to lowercase before building the env var ([7f52ce4](https://github.com/BLSQ/openhexa-sdk-python/commit/7f52ce43309546a614bb71041146d42aa3c0e92a))


### Miscellaneous

* add tests on how to get connections ([7f52ce4](https://github.com/BLSQ/openhexa-sdk-python/commit/7f52ce43309546a614bb71041146d42aa3c0e92a))
* do not keep the container once finished ([6a079b3](https://github.com/BLSQ/openhexa-sdk-python/commit/6a079b369db7ede98f2e86c5464e2662037ae05d))
* Expose "current_run" only in pipeline environments ([6a079b3](https://github.com/BLSQ/openhexa-sdk-python/commit/6a079b369db7ede98f2e86c5464e2662037ae05d))
* Move the openhexa-pipelines dockerfile to openhexa-notebooks ([6a079b3](https://github.com/BLSQ/openhexa-sdk-python/commit/6a079b369db7ede98f2e86c5464e2662037ae05d))

## [0.1.25](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.24...0.1.25) (2023-07-28)


### Miscellaneous

* Simplify messages displayed in CLI for new pipelines ([#61](https://github.com/BLSQ/openhexa-sdk-python/issues/61)) ([16e0cbd](https://github.com/BLSQ/openhexa-sdk-python/commit/16e0cbd94b9b8d5a1420698e897d6a48546f7c4f))
* Update SDK to match project configuration of openhexa-toolbox ([#59](https://github.com/BLSQ/openhexa-sdk-python/issues/59)) ([83a2700](https://github.com/BLSQ/openhexa-sdk-python/commit/83a27004ecfbbe259514bf81ab73123f95f3cfb1))

## [0.1.24](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.23...0.1.24) (2023-07-20)


### Features

* Update SDK version in Dockerfile ([#57](https://github.com/BLSQ/openhexa-sdk-python/issues/57)) ([208d7ea](https://github.com/BLSQ/openhexa-sdk-python/commit/208d7ea561417bf9dc106d3b545254ecbde863db))

## [0.1.23](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.22...0.1.23) (2023-07-20)


### Features

* **Pipelines:** prevent push of version  with params for scheduled pipeline. ([#55](https://github.com/BLSQ/openhexa-sdk-python/issues/55)) ([b9de756](https://github.com/BLSQ/openhexa-sdk-python/commit/b9de756f4dc94296bc427b2dd3337740909399ed))

## [0.1.22](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.21...0.1.22) (2023-07-14)


### Bug Fixes

* Proper error messages for arguments and missing config file ([#51](https://github.com/BLSQ/openhexa-sdk-python/issues/51)) ([07a5027](https://github.com/BLSQ/openhexa-sdk-python/commit/07a5027fb6be317d6f3e666dd6b0d145b8573358))
* use proper namespace package setup ([#53](https://github.com/BLSQ/openhexa-sdk-python/issues/53)) ([81fc51e](https://github.com/BLSQ/openhexa-sdk-python/commit/81fc51e9256d55ac68274c204432582490c37a3a))


### Miscellaneous

* Update SDK version in Dockerfile ([#54](https://github.com/BLSQ/openhexa-sdk-python/issues/54)) ([c6125c0](https://github.com/BLSQ/openhexa-sdk-python/commit/c6125c0ac29a82b19c55bffae435e798113e94db))

## [0.1.21](https://github.com/BLSQ/openhexa-sdk-python/compare/0.1.20...0.1.21) (2023-06-21)


### Bug Fixes

* **CLI:** Do not require a config even if it's empty ([#50](https://github.com/BLSQ/openhexa-sdk-python/issues/50)) ([8e1098f](https://github.com/BLSQ/openhexa-sdk-python/commit/8e1098fc544918aaf78e1eb821e2b5540ba6c42e))


### Miscellaneous

* **docker:** Use openhexa-base-notebook 0.14.0 ([81fca98](https://github.com/BLSQ/openhexa-sdk-python/commit/81fca98c1693dd56b2c7e8c5443e1a1fbe5ee37d))
* **image:** Upgrade openehxa.sdk in pipelines image to 0.1.20 ([8f9a33a](https://github.com/BLSQ/openhexa-sdk-python/commit/8f9a33ac3436e415a8d334c456096a89c05a0dab))

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
