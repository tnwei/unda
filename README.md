# unda

con**da** but **un**iversal for arbitrary Python envs

## Why

I used to swear by conda, then later mamba, for maintaining different python envs for different projects. Then uv came along and all was fine and dandy as long as I was working strictly within a single project.

Having spent time with both conda and uv, I felt friction when (1) work to be done is not confined in a single folder (hello fellow Jupyter notebook users), and (2) when duplicating uv environments feel like a waste of disk space. At some point I had 60+ python envs on my PC! 

Incredibly, I felt nostalgic for conda, but the feeling quickly went away when I felt the difference in DevEx switching from uv. If you felt that way sometimes, this project is for you.

## Installation

```bash
# 1. Run ONE of the below to install using your favourite package manager
uv tool install git+https://github.com/tnwei/unda
pipx install git+https://github.com/tnwei/unda

# 2. Append this line to your .bashrc
eval "$(unda init bash)"

# 3. Set an UNDAPATH variable to define the paths you want Unda to search for Python envs
# Example below, please modify!
export UNDAPATH=$HOME/projects:$HOME/gitclones:$HOME/work
```

No third party dependencies, will keep it that way.

Currently supports bash only.

## Usage

```bash
$ unda list
01: /home/user/work/project_a/etl/.venv
02: /home/user/projects/project_b/.venv
03: /home/user/gitclones/project_c/.venv

$ unda activate 3  # 'unda activate 03' works too
(project_c) $  # (env activated)

(project_c) $ unda deactivate # plain 'deactivate' works too
$ # (env deactivated)

```

## Misc

- I pronounce it in my head like how Sebastian sings "Under the sea" in The Little Mermaid
- No agentic coding involved. Im treating this project like knitting for the joy of creating by my own hands
