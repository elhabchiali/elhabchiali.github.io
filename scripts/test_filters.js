'use strict';
const assert = require('node:assert/strict');
const {applyKernel} = require('../filter-core.js');
const identity=[0,0,0,0,1,0,0,0,0], box=Array(9).fill(1), sobel=[-1,0,1,-2,0,2,-1,0,1];
const data=Uint8Array.from([0,20,40,60,80,100,120,140,255]);
assert.deepEqual([...applyKernel(data,3,3,identity)],[...data]);
assert.ok([...applyKernel(new Uint8Array(25).fill(90),5,5,box,9)].every(v=>v===90));
assert.ok([...applyKernel(new Uint8Array(25).fill(90),5,5,sobel)].every(v=>v===0));
// A linear X ramp has a Sobel response of 8 in the interior, 4 at replicated borders.
const ramp=Uint8Array.from([0,1,2,0,1,2,0,1,2]);
assert.deepEqual([...applyKernel(ramp,3,3,sobel)],[4,8,4,4,8,4,4,8,4]);
// Reversing the ramp preserves the negative signed response before display clipping.
assert.deepEqual([...applyKernel(Uint8Array.from(ramp,v=>2-v),3,3,sobel)],[-4,-8,-4,-4,-8,-4,-4,-8,-4]);
const impulse=Uint8Array.from([0,0,0,0,90,0,0,0,0]);
assert.ok([...applyKernel(impulse,3,3,box,9)].every(v=>v===10));
assert.throws(()=>applyKernel(data,3,3,box,0));
console.log('PASS: identity, normalized blur, constant-edge response, signed Sobel, replicated borders and invalid input.');
