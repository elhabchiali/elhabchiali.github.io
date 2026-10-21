'use strict';
(() => {
  const N = 128;
  const kernels = {
    sobel: { values: [-1,0,1,-2,0,2,-1,0,1], divisor: 1, description: 'Sobel X measures intensity change along X. Vertical edges produce strong signed responses.' },
    blur: { values: [1,1,1,1,1,1,1,1,1], divisor: 9, description: 'Box blur takes the average of the nine neighbouring pixels. The coefficient sum is divided by 9.' },
    sharpen: { values: [0,-1,0,-1,5,-1,0,-1,0], divisor: 1, description: 'Sharpen emphasizes the centre pixel relative to its immediate neighbours.' },
    identity: { values: [0,0,0,0,1,0,0,0,0], divisor: 1, description: 'Identity keeps only the centre pixel. Input and output should match exactly.' }
  };
  const $ = id => document.getElementById(id);
  const sourceCanvas = document.createElement('canvas'); sourceCanvas.width=N; sourceCanvas.height=N;
  const source = sourceCanvas.getContext('2d', {willReadFrequently:true});
  const inputContext = $('input').getContext('2d');
  const outputContext = $('output').getContext('2d');
  let pixels = new Uint8ClampedArray(N*N), filtered = new Float32Array(N*N), stepIndex = -1;
  let currentSample = 'scene';
  const clamp = (v,min=0,max=255) => Math.min(max,Math.max(min,v));
  function synthetic(kind) {
    source.fillStyle='#364b40'; source.fillRect(0,0,N,N);
    if(kind==='scene') {
      for(let y=0;y<N;y+=8) {source.strokeStyle=y%16?'#71826b':'#61755e';source.lineWidth=3;source.beginPath();source.moveTo(0,y);source.lineTo(N,y+20);source.stroke();}
      source.fillStyle='#b6b4a1';source.save();source.translate(64,64);source.rotate(-.45);source.fillRect(-12,-110,24,220);source.restore();
      [[20,25,23,15],[85,35,20,21],[72,88,29,16]].forEach(([x,y,w,h])=>{source.fillStyle='#ded8bc';source.fillRect(x,y,w,h);source.fillStyle='#6e7066';source.fillRect(x+2,y+2,w-4,h-4);});
    } else if(kind==='shapes') {
      source.fillStyle='#e9e5d4';source.fillRect(14,14,40,46);source.beginPath();source.arc(90,38,23,0,Math.PI*2);source.fill();source.fillStyle='#9d9e89';source.beginPath();source.moveTo(20,111);source.lineTo(63,64);source.lineTo(108,111);source.closePath();source.fill();
    } else {
      const gradient=source.createLinearGradient(0,0,N,0);gradient.addColorStop(0,'black');gradient.addColorStop(1,'white');source.fillStyle=gradient;source.fillRect(0,0,N,N);source.fillStyle='#ddd';source.fillRect(31,25,25,78);source.fillStyle='#222';source.fillRect(81,25,18,78);
    }
    readPixels();
  }
  function readPixels() {
    const rgba = source.getImageData(0,0,N,N).data;
    for(let i=0;i<N*N;i++) pixels[i]=Math.round(.299*rgba[i*4]+.587*rgba[i*4+1]+.114*rgba[i*4+2]);
    apply();
  }
  function at(x,y) { return pixels[clamp(y,0,N-1)*N+clamp(x,0,N-1)]; }
  function apply() {
    const k=kernels[$('filter').value];
    filtered=window.VisionFilters.applyKernel(pixels,N,N,k.values,k.divisor);
    $('kernel').replaceChildren(...k.values.map(v=>{const el=document.createElement('span');el.textContent=v;return el;}));
    $('filter-description').textContent=k.description;
    stepIndex=-1; inspect();
  }
  function paint(context,values) {
    const frame=context.createImageData(N,N);
    for(let i=0;i<N*N;i++) {const value=clamp(Math.round(values[i]));frame.data[i*4]=value;frame.data[i*4+1]=value;frame.data[i*4+2]=value;frame.data[i*4+3]=255;}
    context.putImageData(frame,0,0);
  }
  function inspect() {
    const x=Number($('pixel-x').value), y=Number($('pixel-y').value), k=kernels[$('filter').value];
    $('x-value').value=x; $('y-value').value=y;
    paint(inputContext,pixels);paint(outputContext,filtered);
    inputContext.strokeStyle='#ed7441';inputContext.lineWidth=.7;inputContext.strokeRect(x-1.5,y-1.5,3,3);
    outputContext.strokeStyle='#ed7441';outputContext.lineWidth=.7;outputContext.strokeRect(x-.5,y-.5,1,1);
    const neighbours=[];for(let j=-1;j<=1;j++)for(let i=-1;i<=1;i++)neighbours.push(at(x+i,y+j));
    $('neighbours').replaceChildren(...neighbours.map((v,i)=>{const el=document.createElement('span');el.textContent=v;if(i===stepIndex)el.classList.add('current');return el;}));
    [...$('kernel').children].forEach((el,i)=>el.classList.toggle('current',i===stepIndex));
    const sum=neighbours.reduce((a,v,i)=>a+v*k.values[i],0),raw=sum/k.divisor;
    $('calculation').textContent=`Pixel (${x}, ${y}): sum = ${sum}${k.divisor!==1?' ÷ '+k.divisor:''} → raw ${Number(raw.toFixed(2))} → displayed ${clamp(Math.round(raw))}`;
    if(stepIndex>=0) {
      const partial=neighbours.slice(0,stepIndex+1).reduce((a,v,i)=>a+v*k.values[i],0);
      $('step-detail').textContent=`Term ${stepIndex+1}/9: ${neighbours[stepIndex]} × ${k.values[stepIndex]} = ${neighbours[stepIndex]*k.values[stepIndex]}. Running sum: ${partial}.`;
    } else $('step-detail').textContent='Each neighbourhood value is multiplied by the matching kernel coefficient, then all nine products are added.';
  }
  $('sample').addEventListener('change',()=>{currentSample=$('sample').value;$('upload').value='';$('image-note').textContent='Synthetic input, not drone footage. Uploaded images stay in this browser and are resized to 128 × 128 pixels.';synthetic(currentSample);});
  $('filter').addEventListener('change',apply);
  ['pixel-x','pixel-y'].forEach(id=>$(id).addEventListener('input',()=>{stepIndex=-1;inspect();}));
  $('step').addEventListener('click',()=>{stepIndex=(stepIndex+1)%9;inspect();});
  $('next').addEventListener('click',()=>{let x=Number($('pixel-x').value)+1,y=Number($('pixel-y').value);if(x>126){x=1;y=y>=126?1:y+1;}$('pixel-x').value=x;$('pixel-y').value=y;stepIndex=-1;inspect();});
  $('reset').addEventListener('click',()=>{$('sample').value='scene';$('filter').value='sobel';$('upload').value='';$('pixel-x').value=64;$('pixel-y').value=64;currentSample='scene';$('image-note').textContent='Synthetic input, not drone footage. Uploaded images stay in this browser and are resized to 128 × 128 pixels.';synthetic('scene');});
  $('upload').addEventListener('change',async()=>{
    const file=$('upload').files[0];if(!file)return;
    if(!file.type.startsWith('image/')){$('image-note').textContent='Please choose an image file.';return;}
    const url=URL.createObjectURL(file),image=new Image();
    try {await new Promise((resolve,reject)=>{image.onload=resolve;image.onerror=reject;image.src=url;});source.fillStyle='white';source.fillRect(0,0,N,N);const scale=Math.min(N/image.width,N/image.height);const w=image.width*scale,h=image.height*scale;source.drawImage(image,(N-w)/2,(N-h)/2,w,h);$('image-note').textContent='Your image is processed locally, fitted within 128 × 128 pixels with white padding, and converted to grayscale.';readPixels();}
    catch {$('image-note').textContent='This image could not be read. Try another image or one of the samples.';}
    finally {URL.revokeObjectURL(url);}
  });
  synthetic('scene');
})();
