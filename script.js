//let colors=["#EF4836","#446CB3","#03C9A9","#19B5FE","#F9BF3B","#6C7A89","#1F3A93","#2C3E50","#F62459"];
//let i;
//for(i=0;i < colors.length;i++)
	//$('.img-box:nth-child('+(i+1)+')').css("background-color",colors[i]);

$('.img-box').each(function(i){
	$(this).css("background-color","hsl("+(Math.floor(Math.abs(Math.random()*360)%360))+",100%,65%)");
	//console.log($(this).css("background-color"));
});