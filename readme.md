
# **<p align="center" style="font-size:50px">  mineDashBin</p>**





> # *Instruction Rules*:
> * every instruction ends with a `;` example: `i=12;`
>
> ## *Imports*:
> * Imports are done with `include filepath/filename;` or `native filepath/filename;`
> * imports use for the file-extension native `.mcfunction` and for include `.mdblib`
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


