<p align="center">
  <img src="https://user-images.githubusercontent.com/9436784/111063516-ed8fe480-84a6-11eb-9a8d-c5235c3d9e3c.png">
</p>
<p align="center">
  <b>Run context-aware commands from your source code comments.</b>
</p>
<br/>

![codeline](https://user-images.githubusercontent.com/9436784/111068981-d959e080-84c2-11eb-9b13-7b00d751fc10.gif)
![tests](https://github.com/synek/codeline/workflows/Full%20Tests/badge.svg)

Codeline allows you to run custom commands directly from source-code comments, combining the expressiveness of the command-line with the power of an extensions API like VS Code. 

Codeline allows you to pipe commands together, and automatically updates the comment in-place with command results, allowing for a semi-interactive experience.

## Current State

*Codeline is functional, but is still in the very-early stages of development.*  

Please join the [discussions](https://github.com/synek/codeline/discussions), add issues, and get involved.

## Installation

`git clone https://github.com/synek/codeline.git`  
`poetry install`

## Usage
Codeline can monitor the current directory for file-changes, and then run any commands it finds:  
`CL_DEBUG=1 poetry run python -m codeline --watch .`

Alternatively you can run Codeline on a single file, executing any commands the file and then exiting.  
`CL_DEBUG=1 poetry run python -m codeline --run path/to/python/file.py`

## Commands

Currently, commands are implemented as Python plugins. The SDK for building commands is found in `codeline/sdk`.

### Commit
This command allows you to automatically commit a "hunk" of code. 

Example usage: 
```
# <| commit -m "Adds myfunc() to do something"
def myfunc(data):
    data.do_something()
    print("done")
```

## Future Work

* Add support for shell scripts
* Make it possible to pipe commands together
* Publish documentation for the SDK

## Contributing

Codeline is still under heavy development. I will start accepting PRs in a couple of weeks once the development has stabilised a little. However, if you'd like to make a new command for Codeline then please get in touch with me (rory@rory.bio) or open an issue and I'll help.

