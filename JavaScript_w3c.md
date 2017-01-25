一些JavaScript实例
-------------
>1.输入内容
`document.write("<p>This is a paragraph.</p>");`

只能在html输出时加入内容。意义不明，不清楚与直接在html中加入`<p></p>`字段有什么不同

_______________________
>2.弹出提示
>`<button type="button" onclick="alert('Welcome!')">Submit</button>`

在操作后弹出提示，这里是在点击后弹出‘Welcome!’，在Javascript中并不常用。

_______________________
>3.改变HTML内容
```html
x=document.getElementById("demo")
x.innerHTML="Hello JavaScript";
```

这里需要注意改变不同内容时使用不同的方法：

>改变文字内容
```html
<!DOCTYPE html>
<html>
  <body>
    <h1>我的第一段 JavaScript</h1>
    <p id="demo">
      JavaScript 能改变 HTML 元素的内容。
    </p>
    <script>
      function myFunction()
      {
        x=document.getElementById("demo");  // 找到元素
        x.innerHTML="Hello JavaScript!";    // 改变内容
      }
    </script>
    <button type="button" onclick="myFunction()">点击这里</button>
  </body>
</html>
```
__x.innerHTML__

.
>改变图片内容:
```html
<script>
  function changeImage()
  {
    element=document.getElementById('myimage')
    if (element.src.match("bulbon"))
      {
        element.src="/i/eg_bulboff.gif";
      }
    else
      {
        element.src="/i/eg_bulbon.gif";
      }
  }
</script>
<img id="myimage" onclick="changeImage()" src="/i/eg_bulboff.gif">
<p>点击灯泡来点亮或熄灭这盏灯</p>
```
__element.src__

.
>改变样式内容
```html
<p id="demo">
  JavaScript 能改变 HTML 元素的样式。
</p>
<script>
  function myFunction()
  {
    x=document.getElementById("demo") // 找到元素
    x.style.color="#ff0000";          // 改变样式
  }
</script>
<button type="button" onclick="myFunction()">点击这里</button>
```
__x.style.color__

_______________________

>4.验证输入
`if isNaN(x) {alert("Not Numeric")};`

存在确认`<input>`内容的问题，有两种读取数据的方式：

`x=document.getElementById("demo")`

或

`var x=document.getElementById("demo").value`

相对应的函数方法定义也有不同，见下例：
>方式1：
```html
<input id="demo" type="text">
<script>
function myFunction()
{
x=document.getElementById("demo");
if(x.value==""||isNaN(x.value))
	{
	alert("Not Numeric");
	}
}
</script>
<button type="button" onclick="myFunction()">点击这里</button>
```
方式2：
```html
<input id="demo" type="text">
<script>
function myFunction()
{
var x=document.getElementById("demo").value;
if(x==""||isNaN(x))
	{
	alert("Not Numeric");
	}
}
</script>
<button type="button" onclick="myFunction()">点击这里</button>
```

JavaScript的使用规则
----------------------

脚本必须位于`<script></script>`标签之间，
可以放置在html文件的`<head>`或`<body>`部分或同时放在两者之中。

通常的做法是把函数放入 <head> 部分中，或者放在页面底部。这样就可以把它们安置到同一处位置，不会干扰页面的内容。

也可以引用外部脚本：
`<script src=""></script>`

提示：外部脚本不能包含 `<script>` 标签。

JavaScript的输出
--------------------------

**警告**
请使用 document.write() 仅仅向文档输出写内容。
如果在文档已完成加载后执行 document.write，整个 HTML 页面将被覆盖

JavaScript语句
------------------------

分号用于分隔 JavaScript 语句。
通常我们在每条可执行的语句结尾添加分号。
使用分号的另一用处是在一行中编写多条语句。
提示：您也可能看到不带有分号的案例。

在 JavaScript 中，用分号来结束语句是__可选__的。

JavaScript注释
-----------------------------
单行注释以`//`开头。

多行注释以`/*`开头、以`*/`结束。

可以用来阻止代码运行，也可以加在行尾。

JavaScript变量
-------------------------------
变量可以看作是存储数据的容器。

声明方式：`var x = `（等号意味着声明的同时赋值，可不加）。确定变量类型时用`var x = new Number`（变量未赋值），一次声明多个变量用`var x= , y= , z= ;`的方式。变量名必须以字母开头，区分大小写。重新声明变量不改变变量的值。（这种情况貌似会很少见）

**提示**：一个好的编程习惯是，在代码开始处，统一对需要的变量进行声明。

JavaScript只有一种数字类型（不区分整型和浮点型），。

JavaScript数据类型
----------------------
动态类型且不区分整型和浮点型。

数组：（类似Python里的列表）
`var cars=new Array("Audi","BMW","Volvo");`

对象：（类似Python里的字典）
`var person={firstname:"Bill", lastname="Gates", id:3324};`

下列方式更易读：

```
var person={
  firstname : "Bill",
  lastname  : "Gates"
  id        : 3324
};
```
对象的属性有两种寻址方式：
`name=person.lastname`;
`name=person["lastname"];`

`carname="Volvo";`
将声明一个全局变量 carname，即使它在函数内执行。


JavaScript 对象
----------------
对象具有属性与方法（与Python语法接近）
`object.propertyname``object.methodname()`

创建JavaScript对象时：
```
person=new Object();
person.firstname="Bill";
person.lastname="Gates";
person.age=56;
person.eyecolor="blue";
```

JavaScript 函数
-----------------
声明函数：
```
function functionname()
{
  scripts
}
```
**关键词 function 必须是小写的，并且必须以与函数名称相同的大小写来调用函数。**

定义带参数的函数时要在声明时说明：`function myFunction(var1,var2)`

实例：
```html
<p>请点击其中的一个按钮，来调用带参数的函数。</p>

<button onclick="myFunction('Harry Potter','Wizard')">点击这里</button>
<button onclick="myFunction('Bob','Builder')">点击这里</button>

<script>
function myFunction(name,job)
{
alert("Welcome " + name + ", the " + job);
}
</script>
```
函数可以返回值 return 返回值是可选的，返回值为空时退出函数。

JavaScript 运算符
----------------
与Python语法大体一致。**注意**：如果把数字与字符串相加，结果将成为字符串。

条件运算符中有一例：

`variablename=(condition)?value1:value2 `
`greeting=(visitor=="PRES")?"Dear President ":"Dear ";`

如果变量 visitor 中的值是 "PRES"，则向变量 greeting 赋值 "Dear President "，否则赋值 "Dear"。

JavaScript If...Else 语句
--------------------------

格式与Python不同：
```html
if ()
  {
    balabal;
  }
else if ()
  {
    balabala2;
  }
else
  {
    balabala3;
  }
```

实例：
```html
<p>点击这个按钮，获得基于时间的问候。</p>

<button onclick="myFunction()">点击这里</button>

<p id="demo"></p>

<script>
function myFunction()
{
var x="";
var time=new Date().getHours();
if (time<10)
  {
  x="Good morning";
  }
else if (time<20)
  {
  x="Good day";
  }
else
  {
  x="Good evening";
  }
document.getElementById("demo").innerHTML=x;
}
</script>
```

JavaScript Switch 语句
-----------------------
```
switch(n)
{
case 1:
  balabala;
  break;
case 2:
  balabala;
default:
  n 不符合以上时执行；
}
```
实例：
```html
var day=new Date().getDay();
switch (day)
{
case 6:
  x="Today it's Saturday";
  break;
case 0:
  x="Today it's Sunday";
  break;
default:
  x="Looking forward to the Weekend";
}
```

JavaScript For 循环
---------------------
JavaScript 支持不同类型的循环：
>for - 循环代码块一定的次数
>for/in - 循环遍历对象的属性
>while - 当指定的条件为 true 时循环指定的代码块
>do/while - 同样当指定的条件为 true 时循环指定的代码块

**for循环**
```
for (var i=0;i<cars.length;i++)
{
document.write(cars[i] + "<br>");
}
```
括号内分别称为第一、第二、第三语句。三者皆可省略，在循环之前声明变量就能省略第一语句。
第二语句省略的前提是循环内有break语句，否则陷入无限循环会导致浏览器崩溃。
省略第三语句是通过，把递增条件加入循环内部来实现的。

**for/in循环**
用来遍历对象的属性：
```
var person={fname:"John",lname:"Doe",age:25};

for (x in person)
  {
  txt=txt + person[x];
  }
```

**while循环**
递增条件在循环内部。
比较特别的是 for 循环与 while 循环的比较，以及 while 与 do/while 的比较。
后者的关键在于在 do/while 中循环内部会被首先执行一次。

for and while
```html
1.
cars=["BMW","Volvo","Saab","Ford"];
var i=0;
for (;cars[i];)
{
document.write(cars[i] + "<br>");
i++;
}
2.
cars=["BMW","Volvo","Saab","Ford"];
var i=0;
while (cars[i])
{
document.write(cars[i] + "<br>");
i++;
}
```

JavaScript Break 和 Continue 语句
--------------------------------
break 语句可用于**跳出**循环。
break 语句跳出循环后，会**继续**执行该循环之后的代码（如果有的话）：

**注意**
JavaScript 标签

continue 语句（带有或不带标签引用）只能用在循环中。

break 语句（不带标签引用），只能用在循环或 switch 中。

通过标签引用，break 语句可用于跳出任何 JavaScript 代码块：
```
cars=["BMW","Volvo","Saab","Ford"];
list:
{
document.write(cars[0] + "<br>");
document.write(cars[1] + "<br>");
document.write(cars[2] + "<br>");
break list;
document.write(cars[3] + "<br>");
document.write(cars[4] + "<br>");
document.write(cars[5] + "<br>");
}
```

JavaScript 错误 - Throw、Try 和 Catch
-----------------------------------------
JavaScript 语句 **try** 和 **catch** 是成对出现的。

**catch** 用以自定义错误发生后的反应与处理：
```html
<script>
var txt="";
function message()
{
try
  {
  adddlert("Welcome guest!");
  }
catch(err)
  {
  txt="There was an error on this page.\n\n";
  txt+="Error description: " + err.message + "\n\n";
  txt+="Click OK to continue.\n\n";
  alert(txt);
  }
}
</script>
```

**throw** 语句用以生成自定义错误消息

```html
<script>
function myFunction()
{
try
  {
  var x=document.getElementById("demo").value;
  if(x=="")    throw "empty";
  if(isNaN(x)) throw "not a number";
  if(x>10)     throw "too high";
  if(x<5)      throw "too low";
  }
catch(err)
  {
  var y=document.getElementById("mess");
  y.innerHTML="Error: " + err + ".";
  }
}
</script>
```

JavaScript 表单验证
---------------------------
**必填**
```html
<html>
<head>
<script type="text/javascript">

function validate_required(field,alerttxt)
{
with (field)
  {
  if (value==null||value=="")
    {alert(alerttxt);return false}
  else {return true}
  }
}

function validate_form(thisform)
{
with (thisform)
  {
  if (validate_required(email,"Email must be filled out!")==false)
    {email.focus();return false}
  }
}
</script>
</head>

<body>
<form action="submitpage.htm" onsubmit="return validate_form(this)" method="post">
Email: <input type="text" name="email" size="30">
<input type="submit" value="Submit">
</form>
</body>

</html>
```
**邮箱验证**
```html
<html>
<head>
  <script type="text/javascript">

  function validate_email(field, alerttxt)
  {
    with (field)
      {
        apos=value.indesOf("@")
        dotpos=value.lastIndexOf(".")
        if (apos<1||doptos-apos<2)
          {alert(alerttxt);return false}
        else {return true}
      }
  }

  function validate_form(thisform)
  {
    with (thisform)
    {
      if (validate_required(email, "Email must be filled out!")==false)
        {email.focus();return false}
    }
  }
  </script>
</head>

<body>
  <form action="submitpage.htm" onsubmit="return validate_form(this);" method="post">
    Email: <imput type="text" name="email" size="30">
      <input type="submit" value="Submit">
</body>
</html>
```
