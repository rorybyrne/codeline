<p align="center">
  <img src="https://github.com/synek/codeline/workflows/Full%20Tests/badge.svg">
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/9436784/111063516-ed8fe480-84a6-11eb-9a8d-c5235c3d9e3c.png">
</p>
<p align="center">
    Codeline allows you to run code-aware commands from your source code comments.
</p>

![codeline](https://user-images.githubusercontent.com/9436784/111068579-410f2c00-84c1-11eb-839d-60302e2b84a3.gif)

<p>
  Codeline runs as a service and monitors any projects where you have activated it. Any comment beginning with <code><|</code> will be processed, and Codeline will run the corresponding plugin. The `codegen` plugin is just an example, and doesn't actually exist (yet!).
</p>
<h2>Installation</h2>
<h3>Requirements</h3>
<code>python3.8</code>
<code>systemd</code>
<h3>Instructions</h3>
<ol>
    <li><code>git clone https://github.com/synek/codeline</code></li>
    <li><code>cd codeline</code></li>
    <li><code>make install</code></li>
</ol>
<p>
    If you have trouble with the install, check what the <code>Makefile</code> is doing. Get in touch with me if you need help.
</p>
<p>
    To uninstall, run <code>make uninstall</code>
</p>
<h2>Commands</h2>
<p>
  Commands are implemented as Python plugins, built using a rich API for interacting with the
  source code around the command.
</p>
<p>
  Currently, there is only one plugin: <code>git</code>. This plugin allows you to automatically commit a single-line change by running a command like <code># <| git commit --now -m "your message"</code>.
</p>
<h2>Contributing</h2>
<p>
  Codeline is still under heavy development. 
</p>
<p>
  The best way to contribute right now is to join the conversation in <a href="https://github.com/synek/codeline/discussions">discussions</a> and <a href="https://github.com/synek/codeline/issues">issues</a>. I will start accepting PRs in a couple of weeks once the development has stabilised a little.
</p>
