// function* fib(max) {
//   var n = 0, a = 0, b = 1;
//   while (n < max) {
//     yield b;
//     ({ a, b } = { a: b, b: a + b });
//     n = n + 1;
//   }

//   return 'done'
// }

// //fib(6).next()
// for (item of fib(6)) {
//   console.log(item)
// }




var a = function (){
  console.log(arguments.callee);
  console.log(arguments.callee.name);
};
var a2=a;
a2();//指向匿名函数(a) a

var b = function fn(){
  console.log(arguments.callee);
  console.log(arguments.callee.name);
};
var b2=b;
b2();//指向fn fn

function c(){
  console.log(arguments.callee);
  console.log(arguments.callee.name);
};
var c2=c;
c2();//指向c c