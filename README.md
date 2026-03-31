# unda

con**da** but **un**iversal for arbitrary Python envs

## Why

I used to swear by conda, then later mamba, for maintaining different python envs for different projects. Then uv came along and all was fine and dandy as long as I was working strictly within a single project.

Having spent time with both conda and uv, I felt friction when (1) work to be done is not confined in a single folder (hello fellow Jupyter notebook users), and (2) when duplicating uv environments feel like a waste of disk space. Incredibly, I felt like wanting to use conda sometimes and then feeling the difference in dev ex reminded me why I dont use conda anymore. If you felt that way sometimes, this project is for you.

## Installation

`uv add git+https://github.com/tnwei/unda`. No third party dependencies, will keep it that way.

## Usage

1. `unda list` to show all usable ENVs
2. `unda activate ENV` will activate the python env and keep it active for the rest of the shell
3. `unda deactivate` will deactivate the python env

## Misc

- I pronounce it in my head like how Sebastian sings "Under the sea" in The Little Mermaid
- No agentic coding involved. Im treating this project like knitting for the joy of creating by my own hands
