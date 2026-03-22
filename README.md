# uvda

Use uv like conda

## Why

I used to swear by conda, then later mamba, for maintaining different python envs for different projects. Then uv came along and all was fine and dandy as long as I was working strictly within a single project.

Having spent time with both conda and uv, I felt friction when (1) work to be done is not confined in a single project, and (2) when duplicating uv environments feel like a waste of disk space. Incredibly, I felt like wanting to use conda sometimes and then feeling the difference in dev ex reminded me why I dont use conda anymore. If you felt that way sometimes, this project is for you.

## Installation

`uv add git+https://github.com/tnwei/uvda`. Pure python without dependencies, planning to keep it that way.

## Usage

1. Configure an UVDA_ENVS dir. In this dir shall be envs/ themselves and also a toml config file to screen for all other uv / python kernels
2. `uvda activate ENV` will activate the python env made discoverable in UVDA_ENVS
3. `uvda deactivate` will deactivate the python env
3. `uvda uv xxx` will then pass through to call `uv xxx` in the same directory


