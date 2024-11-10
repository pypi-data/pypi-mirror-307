<p> Description: <b>autogit-cli</b> designed to guide users through common Git tasks interactively, which can be useful in projects requiring frequent updates, as it minimizes manual Git commands by offering a user-friendly CLI interface.</p>

<p><a href="#error-fix">Error `autogit` is not recognized. For help click me</a></p>

## INSTALLATION


<h1 align=center >pip install autopush</h1>


| Function    |  Auto Fetch     |
|-------------|----------------|
| `.gitignore` | node_modules/,dist/,.env,*.log,coverage/,.DS_Store,git_history.json and  more . . .
| `[+added, -removed]`     | **main.py [+56 ] [-6 ], index.js [+27 ] [-3 ],index.js [+10] [-3]** |
|`commit suggest`| *'Updated files', 'Refactor code', 'Fix bugs', 'Enhance performance', 'Add new feature', and more . . .*|
|`branch fetch`| origin/main *(default)*, master, custom branch|
|`git history`| Shows previous activity in json format in current project.|


## Usage

# Type `autopush` in your terminal with your active and remotely `Git` repo in project.

> Note: Current project has remote git repo exits, if not it will show error.

```js
// shows  Branch , SHA , Commit msg
{ Branch: "main", SHA: "p5m73l0", Commit: "Fix bugs" }
```
```js
//  create a githistory.json file where all GITHUB history is shown as json format

autopush -h 
```


<!-- This below block is for NPM -->

<!-- ### Error fix -->

<!-- ```cmd
setx PATH "%PATH%;%APPDATA%\npm"
```
The command `setx PATH "%PATH%;%APPDATA%\npm"` appends the npm global installation directory `(%APPDATA%\npm)` to the `PATH` environment variable on Windows. This allows you to run globally installed npm packages from any command prompt or terminal without needing to specify their full paths. The change is permanent and will affect new terminal sessions. --># autopush
