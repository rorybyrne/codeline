<p align="center">
  <img src="https://user-images.githubusercontent.com/9436784/111063516-ed8fe480-84a6-11eb-9a8d-c5235c3d9e3c.png">
</p>
<p align="center">
  <b>Codeline allows you to run code-aware commands from your source code comments.</b>
</p>
<br/>

![codeline](https://user-images.githubusercontent.com/9436784/111068981-d959e080-84c2-11eb-9b13-7b00d751fc10.gif)
![tests](https://github.com/synek/codeline/workflows/Full%20Tests/badge.svg)


Codeline runs as a service and monitors any projects where you have activated it. If it finds a comment beginning with <code><|</code> then it will run the corresponding plugin. The <code>codegen</code> plugin is just an example, and doesn't actually exist yet.

## Installation

*Codeline is still pre-release, so expect bugs.*  

`git clone https://github.com/synek/codeline.git`  
`poetry install`

## Usage
Codeline can monitor the current directory for file-changes, and then run any commands it finds:  
`CL_DEBUG=1 poetry run codeline --watch .`

Alternatively, you can run Codeline on a single file. Codeline will execute any commands that it finds in the file and then exit.  
`CL_DEBUG=1 poetry run codeline --run path/to/python/file.py`

## Commands

Commands are implemented as Python plugins, built using a rich API for interacting with the
source code around the command.

### Commit
This allows you to automatically commit a "hunk" of code below a certain line. 

Example usage: 
```
# <| commit -m "Adds myfunc() to do something"
def myfunc(data):
    data.do_something()
    print("done")
```

## Contributing

Codeline is still under heavy development. I will start accepting PRs in a couple of weeks once the development has stabilised a little. However, if you'd like to make a new command for Codeline then please get in touch with me (rory@rory.bio) or open an issue and I'll help.

