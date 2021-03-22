<p align="center">
  <img src="https://user-images.githubusercontent.com/9436784/111063516-ed8fe480-84a6-11eb-9a8d-c5235c3d9e3c.png">
</p>
<p align="center">
  <b>Run context-aware commands from your source code comments.</b>
</p>
<br/>

![codeline](https://user-images.githubusercontent.com/9436784/111068981-d959e080-84c2-11eb-9b13-7b00d751fc10.gif)
![tests](https://github.com/synek/codeline/workflows/Full%20Tests/badge.svg)

<p align="center">
  Codeline allows you to run custom commands directly from source-code comments, combining the power of IDE extensions with the expressiveness of the command-line.
</p>


## Current State

*Codeline is functional, but is still in the very-early stages of development.*  

Please join the [discussions](https://github.com/synek/codeline/discussions), add issues, and get involved.

## Installation

* `git clone https://github.com/synek/codeline.git`
* `poetry install`

## Development
Codeline can monitor the current directory for file-changes, and then run any commands it finds:  
`poetry run codeline --watch .`

Alternatively you can run Codeline on a single file, executing any commands the file and then exiting.  
`poetry run codeline --run path/to/python/file.py`

To build a command, copy the `plugins/test_plugin` as a starting point.

## Commands

Currently, commands are implemented as Python plugins. The SDK for building commands is found in `codeline/sdk`.

### Test
The test command doesn't do anything, but shows how commands work.

Example usage:
```
def some_function():
    # <| test run
    do_something()
    more_stuff()
```

If Codeline is monitoring the directory, then it will run the command when you save the file.

### Commit
This command allows you to automatically commit a "hunk" of code. 

Example usage: 
```
# <| commit -m "Adds myfunc() to do something"
def myfunc(data):
    data.do_something()
    print("done")
```

If Codeline is monitoring the directory, then it will run the command when you save the file.

## Future Work

* Add support for shell scripts
* Make it possible to pipe commands together
* Publish documentation for the SDK

## Contributing

Codeline is still under heavy development. I will start accepting PRs in a couple of weeks once the development has stabilised a little. However, if you'd like to make a new command for Codeline then please get in touch with me (rory@rory.bio) or open an issue and I'll help.

