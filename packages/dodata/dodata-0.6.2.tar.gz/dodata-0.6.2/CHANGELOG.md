# Changelog

<!-- towncrier release notes start -->

## [0.6.2](https://github.com/doplaydo/DoData_SDK/releases/v0.6.2) - 2024-11-10

No significant changes.


## [0.6.1](https://github.com/doplaydo/DoData_SDK/releases/v0.6.1) - 2024-11-08

No significant changes.


## 0.6.0

- Update gdsfactory 8.13.3
- fix label for plot #76

## 0.5.0

- improve docs 
    - less points in resistance generation
    - add wafer compare examples. Add plotly to dependencies.
    - add device variation factor on sheet resistance and spirals demos
- improve wafer_plot
    * add filter by percentile to wafer plots
    * support scientific notation with arbitrary number of decimals, and different die label font sizes

## 0.4.5

- update to gdsfactory 7.17.0

## 0.4.4

- disable multiprocessing #59
- fixing docs #54

## 0.4.3

- improve docs

## 0.4.2

- improve docs

## 0.4.1

- add analysis filter #52
- fix notebook header #51

## 0.4.0

- rename PROJECT_NAME to PROJECT_ID #47
- Bump gdsfactory from 7.10.5 to 7.10.6 #46
- Draft: rename id -> pkey, name -> *_id #45
- Improve docs #42
- Fix analysis join query #41
- Bump codecov/codecov-action from 3 to 4 #44
- rename is_bad to valid: update references in sdk docs #43
- better error messages #39

## 0.3.1

- define wafer level analysis for ring notebook #36
-  Bump dodata-core from 0.2.2 to 0.2.5 #38

## 0.3.0

No significant changes.


## 0.2.9

- Better wafermap colors #34
- Bump actions/upload-pages-artifact from 2 to 3 #13


## 0.2.8


- Removed requests with backoff as they were causing issues 

## 0.2.7

- generalize analysis functions and fix validate_and_upload #30


## 0.2.2

Added

- Added wafer/die db to get wafers/dies by query/name/id #18
- Added analysis queries for db 

Fixed

- Fixed wafer retrieval api #18

## 0.2.1

- Add cutback analysis, docs and wafermap #27

## 0.2.0

Added

- Added POST for Cell and Device API #20


Changed

- Changed models to use dodata_core models #21


## 0.1.5


Changed

- moved dodata_tutorials to notebook folder 

## 0.1.4


Added

- added tutorials to wheel build 

## 0.1.3

No significant changes.


## 0.1.2

- append username to project in examples

## 0.1.1

- update install instructions


## 0.1.0

- use new api
