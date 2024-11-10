# Changelog

All notable changes between releases will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [1.0.0] - 2024-11-09

### Added
- Support for `ruff` linter output

### Changed
- Ciqar now requires Python 3.12 or newer

### Fixed
- Fixed the license classifier in project metadata (the license itself did not change!)

## [0.2.0] - 2023-06-03

### Added
- Single page HTML report (issue #11)
- `--template` parameter for choosing between multiple report templates (issue #7)
- `--version` parameter for displaying the program version

### Fixed
- Off-by-one line numbers in Pyright report

### Changed
- Improved README file
- Improved and extended template API

### Removed
- `attrs` dependency

## [0.1.0] - 2023-04-23

### Main features of first release
- Default HTML report based on the MyPy report style
- Support for MyPy logfiles Pyright JSON output
- This version doesn't yet support custom report templates
