const start = Date.now();
let number = 0
for (i=0;i<100000000;i++){
	number += i
}
console.log(number)
const millis = Date.now() - start;
console.log(`milliseconds elapsed = `, millis);