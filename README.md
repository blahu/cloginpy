## Welcome to CloginPy Page

Here's a short description of the cloginpy project. The idea is to replace expect-based clogin script with a _refined_ version powered by [netmiko](https://github.com/ktbyers/netmiko).

### WIP

#### 2016-12-21 21:22 GMT

fixed enable mode. also made changes to `read_cloginrc()` to support spaces in passwords, user prompts and password prompts
todo: use protocol according to method with fallback if ``len(method)>2``

#### 2016-12-20 22:23 GMT

cloginrc.py has been incorporated into clogin.py. Now we can connect to devices that allow priv==15. Enable doesn't work yet.

#### 2016-12-19 20:13 GMT
cloginrc.py completed reading of .cloginrc file for most of the interesting options. Works starts on merging both scripts to provide single utility.

### Components (outdated)

At the moment there are 2 scripts. First `clogin.py` is the main script and is still work in progress. Second `cloginrc.py` reads `.cloginrc` configuration/credentials file using `fnmatch` glob matching function this is still work in progress.

### Contact

Find me.
