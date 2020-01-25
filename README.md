# Submerged flexible structure simulator: designed for fish cage and trawl net. 

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/19931a0cd13143c29c7b26795031bc1f)](https://www.codacy.com/manual/hui-aqua/hydromodel?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=hui-aqua/hydromodel&amp;utm_campaign=Badge_Grade)

This is a project within the Ocean Technology Innovation Cluster Stavanger (OTICS) at the University of Stavanger. 
This program it is not ready for release now.
If you have any questions about this program, please email: hui.cheng@uis.no
* Requirements
    * Salome-Meca (Ver2019, Ver2018)  
    https://www.code-aster.org/V2/spip.php?article303
    * Code_Aster (stable version)  
    https://www.code-aster.org/V2/spip.php?article272
    * Python3
     
* How to install this program
    1. Clone this repository to your local folder. 
    2. If you cloned folder, the user should:
        ```
        python3 install.py
        ```
 * How to use this program   
1. The users has to prepare the the 'cageDict' in your working path. 
 You can find a template and introduction of this input file in the examples folder.
        
2. To use the applications, the user needs to source the environment:
   ```
   source $HOME/aqua/etc/aliases.sh 
   ```
3. User configuration
In order to use the installed aquaSimulator, complete the following:
    1. Open the $HOME/.bashrc file in the user's home directory in an editor, e.g., by typing in a terminal (note the dot)
    ```
   vi ~/.bashrc 
   ```
   2. Add the following line at the bottom of that file and save the file
   ```
    alias aqua='source [source folder]/hydromodel/etc/aliases.sh'
   ```

4. Now there are three applications that can be used for simulations:
    - amesh : To creat mesh
    - arun : To auto run simulation
    - aclean : To clean working folder 
