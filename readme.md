
# **<p align="center" style="font-size:50px">  mineDashBin</p>**





> # *Instruction Rules*:
> * every instruction ends with a `;` example: `i=12;`
>
> ## *Imports*:
> * Imports are done with `include filepath/filename;` or `native filepath/filename;`
> * imports use for the file-extension native `.mcfunction` and for include `.mcdb`
> * imports-paths are used without the file-extension example : `include pointer/pointer` is loading file `pointer.mdblib`
> * the import module seach is first searching in the project directory,then in `<compilerdir>/templates/baselib`

> ## *Functions*:
> *   Syntax  `func functionName(argument1,argument2,...){functionBody;}`
> * they are called using `functionName(args1,ars2,...)`
> * Example define: `func test(abc){p=abc;}`
> > ### *Rules:*
> > * as of right now, function params can only **be integers**

> ## Other Keywords:
> * `cc filename` is used to import custom keywords
> * > `shr shortName "association";` is used to define shorts ,shorts get then user by using `<shortname>` inside of your functions .Shorts are normally strings,  there references get replaced with there association upon compile time


> ## Command injection:
> * **any minecraft command can be use inside the file they only need an ** 
> * `NOTE: Native minecraft command are not checked on syntax at this point`
> * Example


# Features 

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
> * **Keyword :** `if`
> * **Usage** : `if("execute if sting"){body}`
> * **What does it do ?** : wraps arount condition and provides 0-tick conditional execution to the if-body
> 

## Hope you have Fun ; ) 



