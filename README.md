# Submerged flexible structure simulator: designed for fish cage and trawl net. 

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/19931a0cd13143c29c7b26795031bc1f)](https://www.codacy.com/manual/hui-aqua/hydromodel?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=hui-aqua/hydromodel&amp;utm_campaign=Badge_Grade)

This is a project within the Ocean Technology Innovation Cluster Stavanger (OTICS) at the University of Stavanger. 
This program it is not ready for release now.

If you have any questions about this program, please email: hui.cheng@uis.no

* Requirements
    * Salome-Meca (Ver2019 or Ver2018)  
    https://www.code-aster.org/V2/spip.php?article303
    * Code_Aster   
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
 You can find a template and introduction of this input file [Here](https://github.com/hui-aqua/hydromodel/tree/master/benchMarkTests).
        
2. To use the applications, the user needs to source the environment:
   ```
   source [source folder]/hydromodel/etc/aliases.sh 
   ```
   
<details>
<summary>shortcut</summary>
<p> 
User configuration
In order to use the installed aquaSimulator, complete the following:

- 1. Open the $HOME/.bashrc file in the user's home directory in an editor, e.g., by typing in a terminal (note the dot)
    ```  vi ~/.bashrc ```
- 2. Add the following line at the bottom of that file and save the file
   ```    alias aqua='source [source folder]/hydromodel/etc/aliases.sh'```
- 3. type aqua in your terminal. 
</p>
</details>

3. Now there are few applications that can be used for simulations:
    - aquaMesh + input dict: To create mesh
    - aquaAster + input dict: To generate the input files for code_Aster
    - aquaSim + input dict: To run simulation
    - aquaClean : To clean working folder 
