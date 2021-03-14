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
  Codeline runs as a service and monitors any projects where you have activated it. Any comment beginning with <code><|</code> will be processed, and Codeline will run the corresponding plugin. The <code>codegen</code> plugin is just an example, and doesn't actually exist (yet).
</p>
<h2>Installation</h2>
Codeline is in a pre-release state, so the only way to run it is to invoke python directly.
<h3>Requirements</h3>
<code>python3.8</code>
<code>systemd</code>
<h2>Commands</h2>
<p>
  Commands are implemented as Python plugins, built using a rich API for interacting with the
  source code around the command.
</p>
<p>
  The first planned plugin is <code>git</code>. It will allow you to automatically commit a single-line change by running a command like <code># <| git commit --now -m "your message"</code>.
</p>
<h2>Contributing</h2>
<p>
  Codeline is still under heavy development. 
</p>
<p>
  The best way to contribute right now is to join the conversation in <a href="https://github.com/synek/codeline/discussions">discussions</a> and <a href="https://github.com/synek/codeline/issues">issues</a>. I will start accepting PRs in a couple of weeks once the development has stabilised a little.
</p>
