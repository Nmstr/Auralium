# Auralium

Auralium is a free and open source music player for Linux!
```
    // | |                                                         
   //__| |              __      ___     // ( )           _   __    
  / ___  |   //   / / //  ) ) //   ) ) // / / //   / / // ) )  ) ) 
 //    | |  //   / / //      //   / / // / / //   / / // / /  / /  
//     | | ((___( ( //      ((___( ( // / / ((___( ( // / /  / /   
```
## Features
- Fast and native
- Listen to local audio files
- Search your library
- Create playlists

# Installation Instructions

## Run from Source

This section describes how to run the Auralium program directly from the source code.

Prerequisites: Make sure you have Python, pip, and git installed on your system.

1. Clone the repo
`git clone https://github.com/Nmstr/Auralium.git`

2. Go into the installation dir
`cd Auralium/src/`

3. Install the dependencies
`pip install -r requirements.txt`

4. Run the program
`python3 main.py`

## Build flatpak from Source

This section describes how to build and run the Auralium program as a flatpak from the source code.

Prerequisites: Make sure you have flatpak and git installed on your system.

1. Clone the repo
`git clone https://github.com/Nmstr/Auralium.git`

2. Go into the installation dir
`cd Auralium/`

3. Install the application
`flatpak-builder --install --user --force-clean build-dir flatpak/io.github.nmstr.auralium.yaml`

4. Run the application
`flatpak run io.github.nmstr.auralium`

# Authors

Namester (Nmstr)

## License

This project is licensed under the GNU General Public License v3.0 (GPLv3)

See LICENSE.md for more information

