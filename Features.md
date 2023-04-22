> # MineDashBin Features 


 <!-- TOC -->
## Contents
    1.Imports --------------------------- 0
    
    Shorts ---------------------------- 1

    Comments -------------------------- 1.5

    functions ------------------------- 2

    Command-Injection ----------------- 3

    CC-Syntax-refactoring ------------- 4

<!-- TOC -->

> ## Imports --------------------------------
> ### Import `.mcbd` files (normal Code)
> * **Keyword :** `include` 
> * Usage : `include folder/file;`
> * Examples : `include pointer/pointer;`
> ### Import `.mcfunctions` files (native minecraft-functions)
> * **Keyword :** `native` 
> * Usage : `native folder/file;`
> * Examples : `native pointer/pointer;`

> ## Shorts --------------------------------
> ### Use shorts like strings that get replaced on compile time,<br> => minimize redundanz in your code
> * **Keyword :** `shr` 
> * **Usage** : `shr Name "LongVersion"`
> * Than (to referent in your code): `<Name>`
> * Examples : `shr Armorstand3 "@e[type=armorstand,tag='specialArmorstand']"` <br> as reference than :`execute as <Armorstand3> at @s run setblock ~ ~ ~ dirt`<br> After compilation it looks like this : <br>`execute as @e[type=armorstand,tag='specialArmorstand'] at @s run setblock ~ ~ ~ dirt`


> ## Commands --------------------------------
> ### to make notes in your code tht get ignored when compiling
> * **Usage** : `// Your Commands here ...`



> ## Functions --------------------------------
> #### Functions later get compiled into alone-standing `.mcfunction` files but you can write them all in one file
> * **Keyword :** `func` 
> * **Usage** : `func funcname(parm1,parm2,...){mainbody}`
> * Call functions: `funcname(args1,args2,...)`
> * Examples : `func summonArmored(){summon minecraft:armor_stand ~ ~ ~}` <br> as reference than :`summonArmored();`
> 
> ## If statements --------------------------------
> #### Functions later get compiled into alone-standing `.mcfunction` files but you can write them all in one file
> * **Keyword :** `#req` or `#if`(coming soon)
> * **Usage** : `#req statement`
> * **What does it do ?** : #req sets the given condition as the prefix for the next line to execute (especially recommend for functionsCals)
> 
> ### Future
> * its work in progress to add the `#if` statement that lets you evaluate variables



## Hope you have Fun ; ) 


