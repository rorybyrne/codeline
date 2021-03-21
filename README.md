<p align="center">
  <img src="https://user-images.githubusercontent.com/9436784/111063516-ed8fe480-84a6-11eb-9a8d-c5235c3d9e3c.png">
</p>
<p align="center">
  <b>Codeline allows you to run code-aware commands from your source code comments.</b>
</p>
<br/>

![codeline](https://user-images.githubusercontent.com/9436784/111068981-d959e080-84c2-11eb-9b13-7b00d751fc10.gif)
<p>
  <img src="https://github.com/synek/codeline/workflows/Full%20Tests/badge.svg">
</p>
<p>
  Codeline runs as a service and monitors any projects where you have activated it. If it finds a comment beginning with <code><|</code> then it will run the corresponding plugin. The <code>codegen</code> plugin is just an example, and doesn't actually exist yet.
</p>
<h2>Installation</h2>
Codeline is in a pre-release state, so I recommend that you don't try to use it.
<p>
  If you really want to, then clone the repository and use <code>poetry</code> to install dependencies. To make Codeline watch the current directory for commands, run <code>CL_DEBUG=1 python -m codeline --watch .</code>, and to run Codeline on a single file run <code>CL_DEBUG=1 python -m codeline --file path/to/file.py</code>.
</p>
<h3>Requirements</h3>
<code>python3.8</code>
<code>systemd</code>
<h2>Commands</h2>
<p>
  Commands are implemented as Python plugins, built using a rich API for interacting with the
  source code around the command.
</p>
<p>
  The first available command is <code>commit</code>. It allows you to automatically commit a "hunk" of code by running this Codeline above it: </br> <code># <| commit -m "your message"</code>.
</p>
<h2>Contributing</h2>
<p>
  Codeline is still under heavy development. 
</p>
<p>
  The best way to contribute right now is to join the conversation in <a href="https://github.com/synek/codeline/discussions">discussions</a> and <a href="https://github.com/synek/codeline/issues">issues</a>. I will start accepting PRs in a couple of weeks once the development has stabilised a little.
</p>
