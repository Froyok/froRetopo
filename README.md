```
//////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////

  ####                  #####            ##                           
 ##                     ##  ##           ##                           
 ##     ##  ##   ####   ##  ##   ####   ######   ####   #####    #### 
 ##     ## ###  ##  ##  ##  ##  ##  ##   ##     ##  ##  ##  ##  ##  ##
######  ###     ##  ##  #####   ##  ##   ##     ##  ##  ##  ##  ##  ##
 ##     ##      ##  ##  ## ##   ######   ##     ##  ##  ##  ##  ##  ##
 ##     ##      ##  ##  ##  ##  ##       ##     ##  ##  ##  ##  ##  ##
 ##     ##      ##  ##  ##  ##  ##       ##     ##  ##  ##  ##  ##  ##
 ##     ##       ####   ##  ##   ####     ####   ####   #####    #### 
                                                        ##            
                                                        ##            
                                                        ##  
//////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////
```

The froRetopo a python plugin and a script for Autodesk Maya that allows to perform mesh retopology much more easily and faster than with the native tools.

---

## How to install ?

Put the content of the folder "froRetopo" inside your "Documents/Maya" folder. Example : "My Documents\\maya\\2011-x64\\"

This script has been tested on the following Maya versions:

* Maya 2011
* Maya 2012
* Maya 2013 
* Maya 2014

> Make sure to extract the python plug-in "__froCmds.py__" and to enable it in Maya, otherwise the "Quad Tool" will be unable to work properly. If you don’t have a "plug-ins" folder inside your "My documents/Maya/201x-xxx/" folder, simply create it and extract the python file inside it.

The edge extrude function may behave improperly on newer version of Maya. To avoid the problem use the following command in Maya (in the script editor or in the mel command) :

```
selectPref -selectTypeChangeAffectsActive 0;
```

[![](resources/th_instal_script.jpg)](resources/instal_script.jpg) [![](resources/th_enable_plugin.jpg)](resources/enable_plugin.jpg)

---

## How to launch the script ?

Call the command following command in the mel command line for the first time: 

```
source froRetopo3.mel; froRetopo3();
```

You can use the “Make Shelf Button” to make a shelf button in your current shelf.

You can also add the froTools to launch when Maya start, to do so, open the 
userSetup.mel file (create it if it doesn’t exist) inside your script folder 
(where froTools3.mel is) and put the following line inside it :

```
eval(“froRetopo3?);
```

---

## Release Notes

__3.5__

* Added a function to count the number of nGons in the currently selected mesh
* Added a function to count the number of edge borders in the currently selected mesh
* Added insert and delete edge loop in the Quad tool
* Added an option to automatically soften the edges of the low-poly when using the Quad Tool
* Updated the viewport UI of the Quad Tool to display all the mouse shortcuts
* Updated the Quad tool to give an error if the user don't have a scene in centimeters
* Updated the UI to make it easier to use (+ removing unnecessary tools)
* Updated the Python plugin, now gives better performances on vertices operations
* Updated the edge extrude, now with better performances when projecting on the high poly
* Updated the sculpt tools to improve performances when selecting all the vertices
* Fixed an error about the Edge Loop tool not finding a froTools command
* Fixed an error about the "edgeToVertex" option (when releasing the mouse in the Quad Tool)
* Fixed an error when an object was too big for the Quad Tool (distance limited by 1000 units, now raised to 10000)
* Fixed soft selection problem (now soft selection is disabled when launching the quad tool)
* Fixed a conflict that was affecting the edge extrude under Maya 2014 ("selectTypeChangeAffectsActive" option)
* Fixed the C++ crash of the viewport (use "currentTime" command instead of "refresh")

__3.4__

* Updated the quad-extrude, now available as a tool with new features
* \[Quad Tool\] Click and drag Quad face extrude
* \[Quad Tool\] Click and drag edge extrude (with snap and welding)
* \[Quad Tool\] Edge fill hole
* \[Quad Tool\] Face deletion
* \[Quad Tool\] Axis Snap and Weld tolerance
* Fixed the sculpt geometry tool not launching when you were not in hilite mode
* Fixed the switch of the live mesh (keep your selection)

__3.3__

* Added a new button to quickly switch between vertex and edge selection
* Added full compatibility to call the script as a floating window

__3.2__

* Changed the "Magnetism" function to a manual "Project geometry"

__3.1__

* Added draggercontext tools : edge extrude and vertex quad extrude

__3.0__

* Initial release
