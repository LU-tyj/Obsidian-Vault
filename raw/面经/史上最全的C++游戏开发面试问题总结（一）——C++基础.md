---
title: 史上最全的C++/游戏开发面试问题总结（一）——C++基础
source: https://zhuanlan.zhihu.com/p/47869981
author:
  - "[[Jerish]]"
published:
created: 2026-07-03
description: 笔者毕业两年多，前一阵通过猎头拿到了腾讯互娱以及网易游戏等多个客户端研发offer (UE4/C++）。在面试前夕，对C++进行了较为全面的复习和总结，乐观估计可以涵盖80%左右的面试基础问题。 这个系列的文章预计有《C…
tags:
  - clippings
  - 面试
  - Cpp
---
[收录于 · 游戏开发那些事](https://www.zhihu.com/column/c_185405805)

891 人赞同了该文章

笔者毕业两年多，前一阵通过猎头拿到了腾讯互娱以及网易游戏等多个客户端研发offer (UE4/C++）。在面试前夕，对C++进行了较为全面的复习和总结，乐观估计可以涵盖80%左右的面试基础问题。

这个系列的文章预计有《C++基础》、《内存、STL、虚函数相关》、《数据结构与算法》、《操作系统》、《计算机网络》、《面试准备与技巧》六篇（后续可能会调整），每篇都是以问答的形式分享并给出了参考资料的链接地址，这个系列的文章会先发布到我的微信公众号上，然后更新到知乎专栏。大部分问题回答的比较简洁，需要大家去仔细阅读参考资料的具体内容，当然也可以直接问我（人多的话会考虑建一个群）~

个人觉得如果这些问题你全部搞懂的话，大部分面试官在C++上就拿你没什么办法或者说不会再进一步为难你了。不过想彻底理解所有内容也并不容易，这里面涉及到操作系统、数据结构、计算机系统原理、汇编等基础内容，涉及到的书籍包括《C++ Primer》 [《Inside the C++ Object Model》](https://zhida.zhihu.com/search?content_id=9699948&content_type=Article&match_order=1&q=%E3%80%8AInside+the+C%2B%2B+Object+Model%E3%80%8B&zhida_source=entity) 《Effctive C++》《More Effctive C++》 [《C++ Template》](https://zhida.zhihu.com/search?content_id=9699948&content_type=Article&match_order=1&q=%E3%80%8AC%2B%2B+Template%E3%80%8B&zhida_source=entity) 《The Design and Evolution of C++》《STL源码剖析》 [《深入理解计算机系统》](https://zhida.zhihu.com/search?content_id=9699948&content_type=Article&match_order=1&q=%E3%80%8A%E6%B7%B1%E5%85%A5%E7%90%86%E8%A7%A3%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%B3%BB%E7%BB%9F%E3%80%8B&zhida_source=entity) 等。

---

**问：了解const么？哪些时候用到const？与宏定义有什么差异？（提问概率：★★★★）**

简单理解，const的目的就是定义一个“不会被修改的常量”，可以修饰变量、引用、指针，可以用于函数参数、成员函数修饰、成员变量， **修饰成员函数本质上就是修饰“this”指针，所以不能修改函数内部的成员变量** 。使用const可以减少代码出错的概率，我们通常要注意的是区分常量指针（指向常量的指针）和指针常量（地址是常量，指针指向的地址不变）以及合理的在函数参数里面使用。具体的情况可以参考下面的书籍与资料。

const修饰的如果是普通对象，那么非const对象不可以随便赋值给const对象，因为const对象只会初始化一次。const对象如果修饰的是常量指针（const int\* X），常量指针不可以赋值给非常量指针，因为赋值后，非常量指针就可以修改常量指针指向的那块内存。

相比宏定义，const在编译期也会起作用（宏定义只是预编译期），会做一些类型检查，方便调试。而且，const不需要在每个用到的地方都申请一块内存空间，要更节省内存。

**实际上，从const的实现原理上来讲，const只是一个编译期的语言功能，做一些简单的常量替换以及赋值限制等，他在运行时不会对内存有什么限制。** 不合理的使用 [const\_cast](https://zhida.zhihu.com/search?content_id=9699948&content_type=Article&match_order=1&q=const_cast&zhida_source=entity) 之所以会造成运行时崩溃，是由于const修饰的某些变量是位于常量区或者其他某些只读的内存页。

参考书籍与资料：《Effctive C++》

Const用法总结（快速区分指针常量与常量指针） [blog.csdn.net/u01299998](https://link.zhihu.com/?target=https%3A//blog.csdn.net/u012999985/article/details/49009531)

[C++ 中 const 的实现原理是什么？](https://www.zhihu.com/question/23006995)

[const修饰的成员函数](https://link.zhihu.com/?target=https%3A//blog.csdn.net/alidada_blog/article/details/86477750)

**问：reference和pointer的区别？哪些情况使用pointer？（提问概率：★★）**

1.指针可以为空，而引用强烈建议不要指向空值，否则可能会出现下面的情况。

```
int* iptr = NULL;
int &irptr = *iptr;
irptr = 'b';//运行时崩溃

char* cptr = NULL;
char* &crptr = cptr;
*crptr = 'b';//运行时崩溃
```

2.指针可以不初始化，引用必须初始化。这意味着引用不需要检测合法性（是否为空）  
3.指针可以随时更改指向的目标，而引用初始化后就不可以再指向任何其他对象  
根据上面的情况我们知道大概知道哪些时候需要使用指针了。不过还有一种情况，在重载如\[\]符号的时候，建议返回引用，这样便于我们书写习惯也方便理解。因为平时我们都是这样使用， a\[10\] = 10;而不是\*a\[10\] = 10;

参考书籍与资料：《More Effctive C++》

**问： [inline](https://zhida.zhihu.com/search?content_id=9699948&content_type=Article&match_order=1&q=inline&zhida_source=entity) 的优劣（提问概率：★★）**

**关于内联的总结可能有很多不恰当的地方，原文已经修改，具体可以参考我的新文章** [（被知乎大佬嘲讽后的一个月，我重新研究了一下内联函数）](https://zhuanlan.zhihu.com/p/50812510) **，另外也可以参考文章** [可别总结 C++ 开发面试问题了](https://zhuanlan.zhihu.com/p/48021301) **。**

优点：减少函数调用开销  
缺点：增加函数体积，exe太大，占用CPU资源，可导致cache装不下(减小了cache的命中) ，不方便调试。debug模式下编译器一般不内联（也可以手动调整参数）， 每次修改会重新编译头文件增加编译时间 （经过进一步学习后这一条也不准确）  
注意:inline只是一个请求，编译器有权利拒绝。有7种情况下都可能会拒绝，虚调用，体积过大，有递归，可变数目参数，通过函数指针调用，调用者异常类型不同，declspec宏等（这里描述不严谨，现代编译器会有更多的方式去采用inline去优化，比如虚调用也可能会被内联）

forceinline字面意思上是强制内联，一般可能只是对代码体积不做限制了，但是对于上面的那些情况仍然不会内联，如果没有内联他会返回一个警告。 构造函数析构函数不建议内联，里面可能会有编译器优化后添加的内容，比如说初始化列表里面的东西。

参考书籍与资料：

WiKi（ [zh.wikipedia.org/wiki/%](https://link.zhihu.com/?target=https%3A//zh.wikipedia.org/wiki/%25E5%2586%2585%25E8%2581%2594%25E5%2587%25BD%25E6%2595%25B0) ）

MSDN([msdn.microsoft.com/zh-c](https://link.zhihu.com/?target=https%3A//msdn.microsoft.com/zh-cn/magazine/z8y1yy88%28v%3Dvs.110%29).aspx)

**问：final和 [override](https://zhida.zhihu.com/search?content_id=9699948&content_type=Article&match_order=1&q=override&zhida_source=entity) 的作用，以及使用场合（提问概率：★★）**

final:禁止继承该类或者覆盖该虚函数  
override:必须覆盖基类的匹配的虚函数

使用场合（final）:

不希望这个类被继承，比如vector，编码者可能不够了解vector的实现，或者说编写者不希望别人去覆盖某个虚函数.顾名思义，final就是最终么

不希望这个函数再被其他子类覆写

使用场合（override）:

第一种情况是你想覆写一个基类的函数，但是不小心参数不匹配或者名字拼错，结果导致写了一个新的虚函数。这时候如果你加上override关键字，编译器会帮你发现与基类函数不匹配从而给出编译错误的提示。

第二种，在使用别人的函数库，或者继承了别人写的类时，你想写一个新函数，但是可能碰巧与原来基类的函数名称一样，这样就会被编译器（以及其他人）误认为要重写基类的函数。如果大家都养成习惯重写基类函数时都加上override，别人在看到你的代码时就知道你当前的函数是否想重写基类里面的函数，也就容易发现你这个无意中重载的Bug。

参考书籍与资料：《C++ Primer》

**问：The rule ofthree是什么？为什么这么做？（提问概率：★）**

If you need to explicitly declare either the destructor,copy constructor or copy assignment operator yourself, you probably need toexplicitly declare all three of them.（析构函数，拷贝构造函数，赋值运算符尽可能一起声明。如果你只定义一个，编译器会帮助你定义另外两个，而编译器定义的版本也许不是你想要的）

参考书籍与资料：WIKI [Rule of three](https://zhida.zhihu.com/search?content_id=9699948&content_type=Article&match_order=1&q=Rule+of+three&zhida_source=entity)

（ [en.wikipedia.org/wiki/R](https://link.zhihu.com/?target=https%3A//en.wikipedia.org/wiki/Rule_of_three_%28C%252B%252B_programming%29) ）

**问：C++03/98有什么你不习惯或不喜欢的用法？C++11有哪些你使用到的新特性？（提问概率：★★★★★）**

这个问题最简单的办法就是看下一个版本的C++有哪些特性，新的特性肯定是有意义的。

如：

auto，有一些迭代器或者map嵌套类型，遍历时比较麻烦，auto写起来很方便。

vector以及其他容器的列表初始化，原来想要像数组一样初始化的话，需要一个一个来，很麻烦。

类内初始值问题，总是需要放到构造函数里面初始化，初始化列表倒是不错，但是初始化数据太多就不行了。

[nullptr](https://zhida.zhihu.com/search?content_id=9699948&content_type=Article&match_order=1&q=nullptr&zhida_source=entity) ，C++11前的NULL一般是是这样定义的 #define NULL 0，这可能会导致一些函数参数匹配问题。而nullptr可以避免这个问题。

[thread](https://zhida.zhihu.com/search?content_id=9699948&content_type=Article&match_order=1&q=thread&zhida_source=entity) ，不需要再使用其他的库来写多线程了。

[智能指针shareptr](https://zhida.zhihu.com/search?content_id=9699948&content_type=Article&match_order=1&q=%E6%99%BA%E8%83%BD%E6%8C%87%E9%92%88shareptr&zhida_source=entity) ，一定程度上解决内存泄露问题。

[右值引用](https://zhida.zhihu.com/search?content_id=9699948&content_type=Article&match_order=1&q=%E5%8F%B3%E5%80%BC%E5%BC%95%E7%94%A8&zhida_source=entity) ，减少拷贝开销。

lambda function，简化那些结构简单的函数代码。  
当然，你要是能说出一些还没有改正或者有待考虑的问题就更好了，比如内存管理的困难（没有GC），没有反射以及一些C#，java里面有而C++没有的特性等，要能深入一点说那就更好了

参考书籍与资料：《C++ Primer》 nullptr，0与NULL （ [cnblogs.com/porter/p/36](https://link.zhihu.com/?target=https%3A//www.cnblogs.com/porter/p/3611718.html) ）

**问：Delete数组的一部分会发生什么？为什么出现异常？（提问概率：★★★★）**

VC下是异常，实际删除的时候整个数组的内存不仅仅是数据大小还包括CRTHeader，数组长度等信息。如果删除一部分会从数量的位置开始传入，是有问题的。VC下数组的内存布局参考下面公式，

公式1）\_CrtMemBlockHeader + \<Your Data>+gap\[nNoMansLandSize\];这类数据用delete和delete\[\]都一样！

公式2）\_CrtMemBlockHeader +数组元素个数+ \<Your Data>+gap\[nNoMansLandSize\];

如果其他编译器，有可能不会报错。但是只释放一个数组对象也是有问题的，其他的对象既没有释放也没有析构。

参考书籍与资料：为何new出的对象数组必须要用delete\[\]删除，而普通数组delete和delete\[\]都一样（ [cnblogs.com/sura/archiv](https://link.zhihu.com/?target=https%3A//www.cnblogs.com/sura/archive/2012/07/03/2575448.html) ）

**问：系统是如何知道指针越界的？（提问概率：★★）**

VC下有一个结构体\_CrtMemBlockHeader，里面有一个Gap属性，这个Gap数组放在你的指针数据的后面，默认为0xFD，当检测到你的数据后不是0xFD的时候就说明的你的数据越界了。

参考书籍与资料：为何new出的对象数组必须要用delete\[\]删除，而普通数组delete和delete\[\]都一样（ [cnblogs.com/sura/archiv](https://link.zhihu.com/?target=https%3A//www.cnblogs.com/sura/archive/2012/07/03/2575448.html) ）

**问：C++编译器有哪些常见的优化？听说过RVO（NRVO）么？（提问概率：★★★）**

1.常量替换如int a = 2; int b = a; return b;可能会优化为 int b=2; return b; 进一步会优化为return 2;

2.无用代码消除比如函数返回值以及参数与该表达式完全无关，直接会优化掉这段代码

3.表达式预计算和子表达式提取常量的乘法会在编译阶段就计算完毕，相同的子表达式也会被合并成一个变量来进行计算

4.某些返回值为了避免拷贝消耗，可能会被优化成一个引用并放到函数参数里面，如RVO，NRVO。

RVO：函数返回的对象如果是新构造的值类型就直接通过一个引用作为参数来构造，进而避免创建一个临时的“temp”对象。

NRVO：相比RVO进一步优化。对于RVO，如果函数在返回前创建了一个临时变量，这个临时变量还是会被构造的，参考下面代码

> Point3d Factory()  
> {  
> Point3d po(1,2, 3);  
> return po;  
> }  
> //RVO优化后  
> void Factory(Point3d &\_result)  
> {  
> Point3d po(1,2,3);  
> \_result.Point3d::Point3d(po);  
> return;  
> }  
> //NRVO优化后  
> void Factory(Point3d &\_result)  
> {  
> \_result.Point3d::Point3d(1, 2, 3);  
> return;  
> }

NRVO则直接跳过临时对象的构造。

（补充：上面的优化有的时候不同编译器可能有差别，想一探究竟建议查看反汇编代码。一般来说函数返回的临时值类型对象是右值，通过寄存器存储，所以获取不到地址）

当然，优化还有很多，这里不一一列举。由于这些优化，你在调试过程中可能无法设置断点，所以需要关闭优化。还有一个小的技巧，static变量不会被优化。

参考书籍与资料：

《Inside the C++ Object Model》（深度探索C++对象模型）

RVO和NRVO的区别是什么？

（ [zhihu.com/question/3223](https://www.zhihu.com/question/32237405/answer/55440484) ）

Copy elision

（ [en.wikipedia.org/wiki/C](https://link.zhihu.com/?target=https%3A//en.wikipedia.org/wiki/Copy_elision%23Return_value_optimization) ）

RVO V.S. std::move

（ [ibm.com/developerworks/](https://link.zhihu.com/?target=https%3A//www.ibm.com/developerworks/community/blogs/5894415f-be62-4bc0-81c5-3956e82276f3/entry/RVO_V_S_std_move%3Flang%3Den) ）

C++中的RVO和NRVO

（ [blog.csdn.net/yao\_zou/a](https://link.zhihu.com/?target=https%3A//blog.csdn.net/yao_zou/article/details/50759301) ）

详解RVO与NRVO

（ [blog.csdn.net/virtual\_f](https://link.zhihu.com/?target=https%3A//blog.csdn.net/virtual_func/article/details/48709617) ）

**问：听说过mangling么？（提问概率：★★）**

mangling 指编译器给函数变量等添加很多的描述信息到名称上用于传递更多信息。常用函数重载，编译时可以把返回值类型等与原函数名称进行组合达到区分的效果，具体规则看编译器。

参考书籍与资料：《Inside the C++ Object Model》（深度探索C++对象模型）

Name mangling

([en.wikipedia.org/wiki/N](https://link.zhihu.com/?target=https%3A//en.wikipedia.org/wiki/Name_mangling))

Why can't C functions be name-mangled?

（ [stackoverflow.com/quest](https://link.zhihu.com/?target=https%3A//stackoverflow.com/questions/36621845/why-cant-c-functions-be-name-mangled) ）

**问：成员函数指针了解么？可以转换为Void\*么？为什么？（提问概率：★★★）**

写法：函数指针 float (\*my\_func\_ptr)(int, char \*);

成员函数指针 float (SomeClass::\*my\_memfunc\_ptr)(int,char \*);

我们在实现delegate的时候通常要用到函数指针，函数指针可以让代码看起来简洁一些

成员函数指针不可以转换成Void **（void\*表示无类型指针通常可以与其他类型指针转换，在网络通信等方面经常使用** ），因为成员函数指针大小并不是4个字节（32位机器上），除了地址还需要this的delta，索引等信息。成员函数指针比较复杂，建议好好读一下下面给出的文章。

参考书籍与资料：

成员函数指针与高性能的C++委托（中文）（ [cnblogs.com/jans2002/ar](https://link.zhihu.com/?target=https%3A//www.cnblogs.com/jans2002/archive/2006/10/13/528160.html) ）

Member Function Pointers and the Fastest Possible C++Delegates（英文）

（ [codeproject.com/Article](https://link.zhihu.com/?target=https%3A//www.codeproject.com/Articles/7150/Member-Function-Pointers-and-the-Fastest-Possible) ）

[zhihu.com/question/4952](https://www.zhihu.com/question/49529308)

[cnblogs.com/wuyudong/p/](https://link.zhihu.com/?target=https%3A//www.cnblogs.com/wuyudong/p/c-void-point.html)

**问：描述一下C/C++代码的编译过程？（提问概率：★★★★）**

预处理——编译——汇编——链接。预处理器先处理各种宏定义，然后交给编译器；编译器编译成.s为后缀的汇编代码；汇编代码再通过汇编器形成.o为后缀的机器码（二进制）；最后通过链接器将一个个目标文件（库文件）链接成一个完整的可执行程序（或者静态库、动态库）。

参考书籍与资料：《深入理解计算机系统》

c++编译过程简介

（ [cnblogs.com/dongdongwei](https://link.zhihu.com/?target=http%3A//www.cnblogs.com/dongdongweiwu/p/4743709.html) ）

**问：了解静态库与动态库么？说说静态链接与动态链接的实现思路（提问概率：★★★）**

存在静态链接器和动态链接器，编译过程涉及到预编译器、编译器（词法分析、语法分析等）、汇编器、链接器，很多时候我们统一称为编译器。

**静态链接** ：编译器和汇编器将多个文件（模块）生成多个 **可重定位的目标文件** ， **静态链接器** 在链接时将多个可重定位目标文件链接成可执行的文件（exe，.out文件 ELF格式）

![](https://pic1.zhimg.com/v2-cfa13f874f3e9a2a43212ed57017277a_1440w.jpg)

**静态库文件** 可以在静态链接时和其他可重定位目标文件一同链接成可执行目标文件。

![](https://pic3.zhimg.com/v2-3e24157a6529aaeae7a0d4d85af3bae6_1440w.jpg)

**动态链接** ：动态链接器需要在链接时先通过静态连接器传入一些重定位和符号信息，后续在可执行文件加载或者运行的时候先加载动态链接器（.interp节中和包含动态连接器的路径，他本身就是一个共享库），随后根据重定位等信息将目标动态库文件加载到内存中。

![](https://pic3.zhimg.com/v2-e0a3804729d32b7b81f156cab6fc36b6_1440w.jpg)

静态库（.a/lib）、共享库(动态库.so/dll)都是由编译器生成

静态库：任意个.o文件的集合，程序link时，被复制到output文件。这个静态库文件是静态编译出来的，索引和实现都在其中，可以直接加到内存里面执行。

对于Windows上的静态库.lib有两种，一种和上面描述的一样，是任意个.o文件的集合。程序link时，随程序直接加载到内存里面。另一种是辅助动态链接的实现，包含函数的描述和在DLL中的位置。也就是说，它为存放函数实现的dll提供索引功能，为了找到dll中的函数实现的入口点，程序link时，根据函数的位置生成函数调用的jump指令。（Linux下.a为后缀）

动态库：包含一个或多个已被编译、链接并与使用它们的进程分开存储的函数。在程序编译时并不会被连接到目标代码中，而是在程序运行是才被载入。不同的应用程序如果调用相同的库，那么在内存里只需要有一份该共享库的实例，规避了空间浪费问题。（Linux下.so为后缀）

参考书籍与资料：《深入理解计算机系统》

Static library

（ [en.wikipedia.org/wiki/S](https://link.zhihu.com/?target=https%3A//en.wikipedia.org/wiki/Static_library) ）

Dynamic-link library

（ [en.wikipedia.org/wiki/D](https://link.zhihu.com/?target=https%3A//en.wikipedia.org/wiki/Dynamic-link_library) ）

lib与dll的关系

（ [blog.csdn.net/u01299998](https://link.zhihu.com/?target=https%3A//blog.csdn.net/u012999985/article/details/50429715) ）

程序的静态链接，动态链接和装载 （ [cnblogs.com/acSzz/p/574](https://link.zhihu.com/?target=https%3A//www.cnblogs.com/acSzz/p/5743789.html) ）

程序运行流程——链接、装载及执行 （ [xuebuyuan.com/1730287.h](https://link.zhihu.com/?target=https%3A//www.xuebuyuan.com/1730287.html) ）

**问：知道内部链接与外部链接么？（提问概率：★★）**

内部链接：如果一个名称对于他的编译单元是局部的，并且在链接时不会与其他的编译单元中同样的名字冲突，那么这个名称就拥有内部链接。

外部链接：一个多文件的程序中，一个实体可以在链接时与其他编译单元交互，那么这个实体就拥有外部链接。换个说法，那些编译单元（.cpp）中能想其他编译单元（.cpp）提供其定义，让其他编译单元(.cpp)使用的函数、变量就拥有外部链接

参考书籍与资料：What is external linkage and internallinkage?

（ [stackoverflow.com/quest](https://link.zhihu.com/?target=https%3A//stackoverflow.com/questions/1358400/what-is-external-linkage-and-internal-linkage) ）

C++编译与链接（2）-浅谈内部链接与外部链接（ [cnblogs.com/magicsoar/p](https://link.zhihu.com/?target=https%3A//www.cnblogs.com/magicsoar/p/3840682.html) ）

理解C++的链接：C++内链接与外链接的意义（ [blog.csdn.net/u01299998](https://link.zhihu.com/?target=https%3A//blog.csdn.net/u012999985/article/details/50429769) ）

**问：extern与static（提问概率：★★★）**

extern 声明一个变量定义在其他文件，这样当前文件就可以使用这个变量，否则会编译失败，如果两个全局变量名称一样会出现链接失败。extern c的作用更重要，因为c++的编译方式与c是不同的，比如函数重载利用mangling的优化。

static变量，很多编译器优化后的效果就是声明一个全局变量，然后判断是否初始化，是的话之后就不需要再初始化了，但是不绝对，win7的全局变量与static的位置就有差异。static成员函数其实在编译后与class完全没有关系。static成员其实也没关系，但是private的需要通过类去调用。static全局变量需要注意，他只能在当前编译单元也就是.cpp内使用(内链接)。全局函数变量是外链接，可以跨单元调用。

static相关注意与理解：静态内存是在main前分配，在main后释放。当存在多个复杂的static变量时，你就不知道哪个先分配了，也控制不了。另外，关于static具体的存储位置，一般是我们常说的静态存储区（bss，数据区等），更贴切的说他是一个可执行文件里面的区域，到操作系统层面可能是另一种叫法，对不同的编译器、C++版本、操作系统可能都有所差异。我们一个程序编译链接好后会把一些静态数据写到exe、dll里面，注意这时候exe并没有放入到内存，所以，其实所谓的编译后内存位置就确定了只不过是一种“理解方式”，真正的静态区（全局变量、静态变量、常量）也是在程序运行后操作系统将这些数据装入内存后的一个位置，这个位置相对exe来说可以理解为静态的，然后当我们运行exe动态申请内存时就是我们 常说的堆区（也可以叫动态区、C++叫自由存储区等）

参考书籍与资料：《C++ primer》

extern "C"

（ [baike.baidu.com/item/ex](https://link.zhihu.com/?target=https%3A//baike.baidu.com/item/extern%2520%2522C%2522) ）

**问：delegate是什么？实现思路？与event的区别？（提问概率：★★★）**

代理简单来说就是让对象B去代理A执行A本身的操作，本质上就是通过指向其他成员函数或者全局函数的函数指针去代理执行。而函数指针有两种，成员函数指针与普通的函数指针，我们一般就是通过对这两种指针的封装来实现代理的效果。常见的实现方式有两种，一种是通过多态接口，另一种是通过宏。代理也分为单播代理与多播代理，单播就是一个调用只代理执行一个函数功能，多播代理就是一个调用可以绑定多个代理函数，可以触发多个代理的函数操作。  
Event是一种特殊的多播delegate，只有声明事件的类可以调用事件的触发操作。最常见的也容易理解的就是MFC里面的按钮的鼠标点击事件了，他的调用只能在Button里面去执行。

参考书籍与资料：\[C++\]实现委托模型（ [cnblogs.com/zplutor/arc](https://link.zhihu.com/?target=https%3A//www.cnblogs.com/zplutor/archive/2011/09/17/2179756.html) ）

**问：使用过模板么？了解哪些特性？（提问概率：★★★★）**

模板分为函数模板与类模板，其根本目的是将类型“参数化”，实现编译时的“动态化”，避免重复代码的书写。另一种运行时的“动态化”就是多态。

模板使用常见的特性有“特化”，“偏特化”，“非类型模板参数”，“设置模板参数默认类型”，“模板中的typename的使用”，“双重模板参数Template Template Parameters”，“成员模板Member Template”，理解这些内容我们就基本上可以看STL标准库了。

另外，模板的实例化过程也是需要理解的。

参考书籍与资料：“STL源码”，《C++ Template》，《C++ Primer》

**问：模板代码如何组织？模板的编译（以及实例化）过程（提问概率：★★★）**

一般来说，模板类的声明与定义不像普通类那样拆分成.h和cpp，而是要全部放在头文件里面（或者定义放在使用到模板的.cpp里），否则会发生编译错误。为什么？因为模板函数所在的cpp不能直接编译成相应的二进制代码，他并不知道模板参数是什么，所以需要一个“实例化”的过程。简单来说，C++标准规定，如果一个cpp里面没有任何显示调用过模板函数（或者使用类模板）的语句，就不会生成真正的拥有确切类型的类的定义，进而就不会生成任何二进制代码，所以其他cpp也无法链接到只包含定义的.cpp文件。下面的例子就会编译报错，除了把template.cpp放到头文件里面，这里放到main.cpp也是可以的

```
//-------------template.h----------------// 
template<typename T> 
class TemTest 
{ 
  public: 
    void TestFun(); 
}; 
//------------template.cpp-------------// 
#include “template.h” 
template<class T> 
void TemTest <T>::TestFun() //定义，但是不会生成二进制文件
{ 
  .....
} 
//---------------main.cpp---------------// 
#include “template.h” 
int main() 
{ 
  TemTest<int> t; 
  t. TestFun(); 
}
```

**问：听说过转发构造么？（提问概率：★★）**

通过foward关键字可以同时考虑到参数为左值以及右值的情况，然后把函数的参数完美的转发到其他函数的参数里面。这个里面涉及到左值、右值、move、forward、引用折叠等技术点。

参考书籍与资料：《C++ Primer》《Effective Modern C++》

The Forwarding Problem: Arguments

（ [open-std.org/jtc1/sc22/](https://link.zhihu.com/?target=http%3A//www.open-std.org/jtc1/sc22/wg21/docs/papers/2002/n1385.htm) ）

A Brief Introduction to Rvalue References （ [artima.com/cppsource/rv](https://link.zhihu.com/?target=https%3A//www.artima.com/cppsource/rvalue.html) ）

C++11 forward完美转发

（ [blog.csdn.net/rankun1/a](https://link.zhihu.com/?target=https%3A//blog.csdn.net/rankun1/article/details/78354153) ）

Effective Modern C++ 条款28 理解引用折叠（ [blog.csdn.net/big\_yello](https://link.zhihu.com/?target=https%3A//blog.csdn.net/big_yellow_duck/article/details/52433305) ）

移动语义（move semantic）和完美转发（perfect forward）

（ [codinfox.github.io/dev/](https://link.zhihu.com/?target=https%3A//codinfox.github.io/dev/2014/06/03/move-semantic-perfect-forward/) ）

**问：描述一下函数调用过程中栈的变化（提问概率：★★★★）**

回答这个问题需要对栈的使用过程，函数调用，汇编都有一定的理解才行。首先，要清楚一个概念“栈帧”。

栈帧(stack frame)：机器用栈来传递过程参数，存储返回信息，保存寄存器用于以后恢复，以及本地存储。为单个过程(函数调用)分配的那部分栈称为栈帧。栈帧其实是两个指针寄存器，寄存器ebp为帧指针（指向该栈帧的最底部），而寄存器esp为栈指针（指向该栈帧的最顶部）。

然后我们再简单描述一下函数调用的机制，每个函数有自己的函数调用地址，里面会有各种指令操作（这端内存位于“代码段”部分），函数的参数与局部变量会被创建并压缩到“栈”的里面，并由两个指针分别指向当前帧栈顶和帧栈尾。当进入另一个子函数时候，当前函数的相关数据会被保存到栈里面，并压入当前的返回地址。子函数执行时也会有自己的“栈帧”，这个过程中会调用CPU的寄存机进行计算，计算后再弹出“栈帧”相关数据，通过“栈”里面之前保存的返回地址再回到原来的位置执行前面的函数。参考下图（改编自 [cnblogs.com/zlcxbb/p/57](https://link.zhihu.com/?target=https%3A//www.cnblogs.com/zlcxbb/p/5759776.html) 的图片）：

![](https://pic4.zhimg.com/v2-517e6c5f73ffdbfef54c2fc09be19eb7_1440w.jpg)

参考书籍与资料：《深入理解计算机系统》

函数调用栈帧过程带图详解

（ [blog.csdn.net/IT\_10/art](https://link.zhihu.com/?target=https%3A//blog.csdn.net/IT_10/article/details/52986350) ）

函数调用栈浅析

（ [cnblogs.com/coderland/p](https://link.zhihu.com/?target=https%3A//www.cnblogs.com/coderland/p/5902719.html) ）

函数调用过程栈帧变化详解

（ [cnblogs.com/zlcxbb/p/57](https://link.zhihu.com/?target=https%3A//www.cnblogs.com/zlcxbb/p/5759776.html) ）

**问：\_\_cdecl/\_\_stdcall是什么意思（提问概率：★★★）**

常见的函数调用有如下

\_\_cdecl/\_\_stdcall/\_\_thiscall/\_\_fastcall。

cdecl按照c语言标准，从右到左，可以实现可变参数，调用者弹出参数。

stdcall（pascal调用约定）按照c++标准，函数参数从右到左，不支持可变参数，函数返回自动清空。但是有的时候编译器会识别并优化成cdecl。

Pascal语言中参数就是从左到右入栈的不支持可变长度参数

（注：\_\_stdcall标记的函数结束后，ret 8表示清理8个字节的堆栈，函数自己恢复了堆栈）

参考书籍与资料：“建议查看反汇编代码”

x86 calling conventions

（ [en.wikipedia.org/wiki/X](https://link.zhihu.com/?target=https%3A//en.wikipedia.org/wiki/X86_calling_conventions) ）

What is \_\_stdcall?

（ [stackoverflow.com/quest](https://link.zhihu.com/?target=https%3A//stackoverflow.com/questions/297654/what-is-stdcall) ）

\_\_stdcall

（ [msdn.microsoft.com/zh-c](https://link.zhihu.com/?target=https%3A//msdn.microsoft.com/zh-cn/library/zxk0tw93.aspx) ）

**问：C++中四种Cast的使用场景是什么？（提问概率：★★★★★）**

constcast，去掉常量属性以及volatile，但是如果原来他就是常量去掉之后千万不要修改；比如你手里有一个常量指针引用，但是函数接口是非常量指针，可能需要转换一下；成员函数声明为const，你想用this去执行一个函数，也需要用constcast

staticcast，基本类型转换到void，转换父类指针到子类不安全

dynamiccast，判断基类指针或引用是不是我要的子类类型，不是强转结果就返回null，用于多态中的类型转换

reintercast，可以完成一些跨类型的转换，如int到void\*，用于序列化网络包数据

参考书籍与资料：《C++ Primer》《The Design and Evolution of C++》（C++语言的设计与演化）

**问：用过或很熟悉的设计模式有哪些？（提问概率：★★★★）**

这个问题看好书写写代码就可以自由发挥了，下面给几个例子。

工厂模式，通过简单工厂生成NPC对象，简单处理的话可通过“字符串匹配”动态创建对象。如果有“反射机制”就可以直接传class来实现。当然可以进一步使用抽象工厂，处理不同的生产对象。

单例，实现全局唯一的一个对象。构造函数、静态指针都是私有的，使用前提前初始化或者加锁来保证线程安全。

Adaptor适配器，代码适配原来的相机移动最后调用的是原来的移动，现在加了适配器继承里面放了当前引擎的摄像机，然后覆盖原来摄像机的移动逻辑。

Observer，一个对象绑定多个观察者，然后这个对象一旦有消息就立刻公布给所有的观察者，观察者可以动态添加或删除。在UE4里面，行为树任务节点请求任务后进入执行状态，然后会立刻注册一个观察者observer到行为树（行为树本身就相当于前面提到的那个对象）的observer数组里面同时绑定一个代理函数。行为树tick检测消息发送给所有观察者，观察者收到消息执行代理函数。

参考书籍与资料：《Head First设计模式》《设计模式：可复用面向对象软件的基础》

常见设计模式的解析和实现C++ （ [wenku.baidu.com/view/74](https://link.zhihu.com/?target=https%3A//wenku.baidu.com/view/7488c59f0508763231121295.html) ）

Design Patterns

([en.wikipedia.org/wiki/D](https://link.zhihu.com/?target=https%3A//en.wikipedia.org/wiki/Design_Patterns))

**问：为什么const修饰成员函数后不能修改成员变量**

每个成员函数在调用的时候，都会把this作为第一个参数传进去。我们在用const修饰成员函数的时候，就相当于修饰了this，也就是说我们的第一个参数应该是

```
const 类型* this
```

所以我们不能去修改this的成员变量，编译器不允许通过。

**问：编码了解么？unicode和utf-8的区别**

编码的本质就是将二进制与符号一一映射，然后通过二进制码解析出对应的符号。一开始计算机只存在于欧美，所以他们理所应当的把英文（以及常见的符号）与二进制做了一个映射表，这就是ASCII码。后来，其他国家也开始使用，需要用到的二进制也越来越多，不同的国家都有不同的编码方式，比如中国的GBK。但是问题是各个国家都不统一，解析起来非常麻烦，因此一个ISO的组织就重新搞了一个包含所有文字与符号的编码方式，即Unicode。unicode全称"Universal Multiple-Octet Coded Character Set"，是一个全球统一的符号集，规定了每个符号对应的二进制编码，这个编码的长度是不确定的，由字符来决定。虽然如此，但是他却没有表示这个符号该如何存储，比如一个英文字符只需要一个字节就可以处理，而一个汉字可能就需要两个字符存储。问题是我在编码的时候并不知道这N个字节的二进制编码到底表示的是一个还是N个符号。这样，UTF-8出现了，他提供了一种Unicode的存储方式，它是一种变长的编码方式。它可以使用1~4个字节表示一个符号，根据不同的符号而变化字节长度。

UTF-8的编码规则只有二条：

1）对于单字节的符号，字节的第一位设为0，后面7位为这个符号的unicode码。因此对于英语字母，UTF-8编码和ASCII码是相同的。

2）对于n字节的符号（n>1），第一个字节的前n位都设为1，第n+1位设为0，后面字节的前两位一律设为10。剩下的没有提及的二进制位，全部为这个符号的unicode码。

这样，通过判断每个字节前面的几位，就可以判断其表示的是某个符号还是符号的一部分了。

参考资料： [jerish.blog.csdn.net/ar](https://link.zhihu.com/?target=https%3A//jerish.blog.csdn.net/article/details/77619368)

> **更多内容欢迎关注微信公众号: 游戏开发那些事**  
> 之后还会陆续更新更多关于面试，游戏开发，虚幻引擎等相关的学习资料~

还没有人送礼物，鼓励一下作者吧

编辑于 2021-01-04 21:21[无需技术背景，分钟级生成个人作品集，求职快人一步，限时0元试用](https://click.aliyun.com/m/1000414442/?spu=biz%3D0%26ci%3D3760674%26si%3Dcd2f848a-c80d-44c3-96af-5a7c05c7f752%26ts%3D1783056193%26zid%3D1629)

[

如何从海量应届毕业生中脱颖而出，让面试官留下深刻印象？不用懂技术，不用懂设计，用秒悟说出你的需求，分钟级...

](https://click.aliyun.com/m/1000414442/?spu=biz%3D0%26ci%3D3760674%26si%3Dcd2f848a-c80d-44c3-96af-5a7c05c7f752%26ts%3D1783056193%26zid%3D1629)

赞同 891