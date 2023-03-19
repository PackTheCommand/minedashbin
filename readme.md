
# **<p align="center" style="font-size:50px">  mineDashBin</p>**





> # *Instruction Rules*:
> * every instruction ends with a `;` example: `i=12;`
> * line ends are **not important** for the end of a instrucktion example: `testvar=`_linebreak_`10;`

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
> * `inject "code"` is used to insert minecraft commands directly into the code ,these instruction skipp any compilers checks 

> ## Example Program:
>> `include pointer/pointer;`<br>
>    `cc minebase;`<br>
>    `func empty(){`<br>
>    `place 12 12 12 minecraft:grass;}`<br>
>    `func diskpart(name){`<br>
>    `shr Entity i"@e[type=bat]";`<br>
>    `p= 12;`<br>
>    `inject "tesl ais best";`<br>
>    `c=`<br>
>    `12;`<br>
>    `d= p;`<br>
>    `myfunc(1,1,1,1);`<br>
>    `tls(1,1,1,1);`<br>
>    `}`<br>
>    `func tls(new,parser,privat,nuller){`<br>
>    `printst "test";`<br>
>    `}`<br>
>    `func myfunc(new,parser,privat,nuller){`<br>
>    `}`<br>
