*One Task To Go (1T2G)* is a focused to do tracker for the Mac Menubar.

The application is built using the rumps package and is in a very early stage. Please feel free to make PR against the  application.

Current known limitations of the application are:
- It does not save state in any way; ideally it should save state between reloads
- It does not automatically run on startup
- It has no debug information
- The icon is horrendous
- Limited hotkey/keyboard navigation support (even though they are listed)

Use at your own risk :)

Some _intentional_ limitations (i.e. features) include:
- Tracking only three tasks at once
- Displaying only one task at a time
- Zero task depth, nesting, or tagging

One task to go is based on the task management principle of, "Think of one task, write it down, do it, cross it out." I believe that at the time of pushing the initial commit, this concept had reached The Organge Site Zeitgeist via https://www.oliverburkeman.com/onething.

## Inside the repo
Inside the repo are some python scripts to run the application. There are also some shell scripts to build the iconset for packaging via py2app. I am an expert neither in python, nor in py2app, so any constructive feedback is more than welcome.