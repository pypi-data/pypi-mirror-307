function murmurHash64(str) {
    let h1 = 0xdeadbeef;
    let h2 = 0x41c6ce57;

    for (let i = 0; i < str.length; i++) {
        let k = str.charCodeAt(i);
        h1 = Math.imul(h1 ^ k, 0x85ebca6b);
        h2 = Math.imul(h2 ^ k, 0xc2b2ae35);
    }

    h1 = Math.imul(h1 ^ (h1 >>> 16), 0x85ebca6b) ^ Math.imul(h2 ^ (h2 >>> 13), 0xc2b2ae35);
    h2 = Math.imul(h2 ^ (h2 >>> 16), 0x85ebca6b) ^ Math.imul(h1 ^ (h1 >>> 13), 0xc2b2ae35);

    return (h1 >>> 0).toString(16).padStart(8, '0') + (h2 >>> 0).toString(16).padStart(8, '0');
}

function fillN(url){
    const urlObj = new URL(url);

    const params = new URLSearchParams(urlObj.search);

    const n = params.get("n");
    const enc_n = nfunc(n)
    params.set("n", enc_n);
    urlObj.search = params.toString();
    return urlObj.toString();
}

// function nfunc(a)  {var b=a.split(a.slice(0,0)),c=[function(d,e){e=(e%d.length+d.length)%d.length;d.splice(-e).reverse().forEach(function(f){d.unshift(f)})},
//     -2081002339,2051943908,function(){for(var d=64,e=[];++d-e.length-32;)switch(d){case 46:d=95;default:e.push(String.fromCharCode(d));case 94:case 95:case 96:break;case 123:d-=76;case 92:case 93:continue;case 58:d=44;case 91:}return e},
//     77431391,function(){for(var d=64,e=[];++d-e.length-32;)switch(d){case 46:d=95;default:e.push(String.fromCharCode(d));case 94:case 95:case 96:break;case 123:d-=76;case 92:case 93:continue;case 58:d=44;case 91:}return e},
//     -1665076476,-905069865,function(){for(var d=64,e=[];++d-e.length-32;){switch(d){case 91:d=44;continue;case 123:d=65;break;case 65:d-=18;continue;case 58:d=96;continue;case 46:d=95}e.push(String.fromCharCode(d))}return e},
//     -77584436,null,function(d){d.reverse()},
//     -373870752,567199967,-1732348182,function(d,e,f,h,l,m,n,p){return e(f,h,l,m,n,p)},
//     -433355706,-438114930,b,b,function(d,e,f,h,l,m,n,p,q){return f(h,l,m,n,p,q)},
//     2070868492,b,null,function(d,e){e=(e%d.length+d.length)%d.length;d.splice(e,1)},
//     1966193249,2117333066,-226486515,"dcF1p",function(d,e){e.length!=0&&(d=(d%e.length+e.length)%e.length,e.splice(0,1,e.splice(d,1,e[0])[0]))},
//     1351334442,-346598915,1255477581,1753795232,function(d,e){for(e=(e%d.length+d.length)%d.length;e--;)d.unshift(d.pop())},
//     -1341655039,"const",312387913,2122508990,"(,,][}/",function(d){for(var e=d.length;e;)d.push(d.splice(--e,1)[0])},
//     -77584436,"forEach",function(d,e,f,h,l,m){return e(h,l,m)},
//     1118402060,-1980068027,function(d,e,f,h,l){return e(f,h,l)},
//     450471574,294481238,1559755110,2001154336,-186015268,-1919163602,245503339,-1353234439,-1394755194,-1877591835,574500037,1847613880,function(d,e,f){var h=e.length;d.forEach(function(l,m,n){this.push(n[m]=e[(e.indexOf(l)-e.indexOf(this[m])+m+h--)%e.length])},f.split(""))},
//     1334376232,"CZnyab",null,-56166698,-1065761336,840504684,-239880899,function(){for(var d=64,e=[];++d-e.length-32;)switch(d){case 58:d=96;continue;case 91:d=44;break;case 65:d=47;continue;case 46:d=153;case 123:d-=58;default:e.push(String.fromCharCode(d))}return e},
//     -1341529479,82293166,628541612,function(d,e){if(d.length!=0){e=(e%d.length+d.length)%d.length;var f=d[0];d[0]=d[e];d[e]=f}},
//     -423372772,-40128020];c[10]=c;c[23]=c;c[62]=c;try{try{c[31]<-3&&(c[16]<3&&((0,c[20])(((((0,c[11])(c[23]),c[14])(c[51],(0,c[65])(),c[45]),c[39])(c[63],c[61]),c[39])(c[20],c[69]),(0,c[10])(c[18],c[16]),c[67],(0,c[42])(c[new Date("1969-12-31T19:30:21.000-04:30")/1E3],c[13]),c[28],c[51]),1)||(0,c[49])((0,c[49])((0,c[63])(c[24],c[57])>>((0,c[0])(c[22]),(0,c[0])(c[44])),c[6],(0,c[19])(c[52],(0,c[42])(),c[70]),c[19],c[56],(0,c[27])(),c[62]),c[6],(0,c[58])(c[53],c[41]),c[58],c[56],c[13])),c[38]!=new Date("1970-01-01T06:45:00.000+06:45")/
//     1E3&&(0,c[68])(c[22],c[35]),c[56]<3?((((0,c[63])(((((0,c[41])(c[39],c[33]),c[28])(c[39]),c[57])(c[36]),c[2])(c[39],(0,c[22])(),c[53]),c[46],c[50],c[27]),(((0,c[2])(c[39],(0,c[20])(),c[4]),c[46])(c[42],c[39]),c[41])(c[39],c[44]),c[2])(c[36],(0,c[25])(),c[53]),c[2])(c[35],(0,c[10])(),c[4]),c[41])(c[36],c[48]):(((((((0,c[60])((0,c[14])(c[5],c[15]),c[41],(0,c[63])((0,c[46])(c[19],c[36]),c[14],c[35],c[1]),c[35],c[64]),c[63])((0,c[46])(c[9],c[27]),c[57],c[27]),c[45])(c[38]),c[59])(c[46],c[18]),c[73])(c[38],
//     c[49]),c[16])(c[0]),c[41])(c[39],c[49]),c[70]==8?(((((0,c[51])(c[40],c[21]),c[41])(c[35],c[72]),c[14])(c[73],c[5]),(0,c[28])(c[35]),c[46])(c[23],c[39]),c[41])(c[27],c[65]):((((((0,c[0])(c[new Date("1969-12-31T19:00:27.000-05:00")/1E3],c[12]),c[32])(c[71],c[59]),c[37])(c[59],c[20]),c[60])(c[19],(0,c[68])(),c[62]),c[17])(c[20],c[53]),c[58])(c[57],c[55])}catch(d){(0,c[50])(c[29])<=(0,c[34])(c[29],c[1]),(0,c[56])((0,c[39])(c[59],c[20]),c[69],c[32],(0,c[3])(),c[52])}finally{c[24]<=new Date("1970-01-01T06:00:01.000+06:00")/
//     1E3&&(c[16]===-7||((0,c[50])(c[20]),0))&&(0,c[23])(c[53]),c[67]>1&&(0,c[47])(c[53],c[18]),c[15]!=-8?(((0,c[34])(c[28],c[53]),c[34])(c[12],c[53]),(0,c[29])(c[44],c[24]))&(0,c[17])((0,c[17])((0,c[17])((0,c[17])((0,c[52])(c[41]),c[6],c[53],c[3]),c[52],c[15],c[62]),c[22],c[62],(0,c[73])(),c[39]),c[22],c[63],(0,c[73])(),c[8+new Date("1969-12-31T18:30:17.000-05:30")/1E3%13+33]):(0,c[38])((((0,c[47])(c[71],c[31]),c[57])(c[63],c[8]),c[47])(c[59],c[44]),c[70],(0,c[57])(c[59],c[51]),c[58])!==(0,c[38])((0,c[22])(c[59],
//     (0,c[2])(),c[45]),c[70],(0,c[22])(c[59],(0,c[4])(),c[53]),c[25]),c[55]!=-2&&(0,c[38])((0,c[35])((0,c[70])(c[59]),c[47],c[63],c[40]),c[24],(0,c[57])(c[62],c[11]),c[59],c[67])}}catch(d){return"enhanced_except_upwBxeP-_w8_"+a}return b.join("")};;


    function nfunc(a)  {var b=a.split(a.slice(0,0)),c=[function(d,e){e=(e%d.length+d.length)%d.length;d.splice(e,1)},
        function(){for(var d=64,e=[];++d-e.length-32;)switch(d){case 46:d=95;default:e.push(String.fromCharCode(d));case 94:case 95:case 96:break;case 123:d-=76;case 92:case 93:continue;case 58:d=44;case 91:}return e},
        -1646750266,205095617,null,-552000204,"oA-8Fu",-1138238467,-1375213103,1603012011,-1041695649,function(d,e){for(e=(e%d.length+d.length)%d.length;e--;)d.unshift(d.pop())},
        function(d,e){e.length!=0&&(d=(d%e.length+e.length)%e.length,e.splice(0,1,e.splice(d,1,e[0])[0]))},
        -1860254261,-280201868,-1110826877,-796205464,function(d,e){d=(d%e.length+e.length)%e.length;e.splice(-d).reverse().forEach(function(f){e.unshift(f)})},
        1876720395,function(d){d.reverse()},
        -2049381711,function(d,e,f){var h=d.length;e.forEach(function(l,m,n){this.push(n[m]=d[(d.indexOf(l)-d.indexOf(this[m])+m+h--)%d.length])},f.split(""))},
        -959247782,function(){for(var d=64,e=[];++d-e.length-32;){switch(d){case 91:d=44;continue;case 123:d=65;break;case 65:d-=18;continue;case 58:d=96;continue;case 46:d=95}e.push(String.fromCharCode(d))}return e},
        473574103,212707435,function(d,e){if(d.length!=0){e=(e%d.length+d.length)%d.length;var f=d[0];d[0]=d[e];d[e]=f}},    
        179537969,1595141961,337335874,-374895331,1785443463,1323806337,-290264246,"var",function(d,e,f,h,l){return e(f,h,l)},
        288838435,1955448682,-117256602,1193841137,b,function(){for(var d=64,e=[];++d-e.length-32;)switch(d){case 58:d=96;continue;case 91:d=44;break;case 65:d=47;continue;case 46:d=153;case 123:d-=58;default:e.push(String.fromCharCode(d))}return e},
        -1455376874,null,/[)'\(,,]'/,308918831,b,-2136053295,-406946196,-689980940,1085207950,-1157308046,128662844,-1450743562,-73468562,b,-957032142,null,-221371012,1131492157,/\/,,{\/[[\\][[""/]\//,-59686438,1317073930,-71265744,202785280,-2069206094,',}\\}[,"',1260534801,-1041695649,454095680,326036423,221633703,1357226582,-1187982265,function(d,e){d.splice(d.length,0,e)},
        1676096769,-1907539902,-267137802,function(d){for(var e=d.length;e;)d.push(d.splice(--e,1)[0])},
        -620912280,function(d,e,f,h,l,m){return e(h,l,m)}];
        c[4]=c;c[43]=c;c[57]=c;try{try{c[18]>-9&&(c[5]==1?(0,c[35])((0,c[12])(c[37],c[43]),c[11],c[55],c[50]):(0,c[35])((0,c[0])(c[55],c[61]),c[12],c[31],c[43])),c[73]<=-1&&((((0,c[35])((0,c[12])(c[15],c[new Date("1970-01-01T11:15:43.000+11:15")/1E3]),c[26],c[new Date("1969-12-31T14:15:43.000-09:45")/1E3],c[51]),(0,c[11])(c[46],c[49]),(((0,c[35])((0,c[21])((0,c[41])(),c[40],c[34]),c[26],c[40],c[new Date("1969-12-31T12:45:56.000-11:15")/1E3]),c[19])(c[43]),c[new Date("1969-12-31T17:00:45.000-07:00")/1E3])((0,c[61])(c[40]),
        c[61],c[76]),c[11])(c[46],c[20]),c[17])(c[76],c[57]),1)||(0,c[58])(((((0,c[13])((0,c[78])(c[18]),c[71],c[66],c[63]),(0,c[80])((0,c[19])(),c[33],c[12]),c[71])(c[2],c[21]),c[4])(c[35],c[48]),(0,c[13])((0,c[50])(c[24],c[36]),c[80],(0,c[1])(),c[33],c[12])),c[new Date("1970-01-01T10:31:10.000+10:30")/1E3],(0,c[13])((0,c[56])(c[18]),c[50],c[new Date("1969-12-31T18:30:33.000-05:30")/1E3],c[32]),c[21],c[17]),c[74]===9&&(((0,c[80])((0,c[19])(),c[24],c[65]),c[70])(c[24],c[47]),[])||(0,c[13])((0,c[52])(c[21],
        c[26]),c[71],c[77],c[35]),c[new Date("1969-12-31T20:46:15.000-03:15")/1E3]!=10&&(c[39]<new Date("1969-12-31T17:44:56.000-06:15")/1E3||(((0,c[13])((0,c[70])(c[35],c[new Date("1969-12-31T14:00:08.000-10:00")/1E3]),c[new Date("1969-12-31T17:15:50.000-06:45")/1E3],c[24],c[61]),c[70])(c[33],c[30]),void 0))&&(0,c[13])((0,c[13])((0,c[76])(c[68],c[33]),c[71],c[40],c[21]),c[4],c[21],c[41]),c[59]===8?(((0,c[50])(c[new Date("1970-01-01T08:30:18.000+08:30")/1E3],c[59]),c[80])((0,c[60])(),c[18],c[12]),c[50])(c[24],
        c[new Date("1969-12-31T15:30:43.000-08:30")/1E3]):(((0,c[4])(c[18],c[51]),c[4])(c[63],c[5]),c[52])(c[63],c[72])}catch(d){(0,c[58])((0,c[50])(c[33],c[14]),c[71],(0,c[50])(c[24],c[23]),c[72],c[18]),(0,c[13])((0,c[71])(c[62],c[24]),c[50],c[0],c[25])}finally{c[81]!==-6&&((0,c[13])((0,c[70])(c[0],c[42]),c[68],c[36]),(0,c[16])(c[30],c[79]),1)||(0,c[25])((0,c[25])((0,c[62])(c[75],c[18]),c[9],(0,c[72])(),c[30],c[24]),c[82],c[12],c[65]),c[78]<3&&(c[60]!==-3||((0,c[62])(c[75],c[69]),0))&&(0,c[7])(c[45]),c[67]!=
        -7&&((0,c[25])((0,c[82])(c[30],c[28]),c[16],c[45],c[57]),3)||(0,c[25])((0,c[5])(c[15],c[45]),c[7],c[12]),c[41]<=-5&&(((((0,c[25])((0,c[16])(c[33],c[10]),c[82],c[33],c[19]),c[9])((0,c[72])(c[31],c[14]),c[72],c[27],c[59]),(0,c[66])(c[9]),c[7])(c[new Date("1969-12-31T21:57:27.000-02:00")/1E3*13+27- -1973],c[19]),c[36])((0,c[41])(c[1],c[73]),c[78],(0,c[18])(c[48],c[new Date("1969-12-31T14:46:13.000-09:15")/1E3]),c[19],c[62]),c[32])(c[49],c[27]),c[43]!==-1&&(c[55]!=0?(0,c[69])((0,c[29])(c[45],c[49])*(0,c[4])(c[64]),
        c[2],(0,c[22])(),c[64],c[17]):(0,c[69])((0,c[69])((0,c[4])(c[58]),c[2],(0,c[63])(),c[58],c[70]),c[26],c[19])),c[36]<8&&(((0,c[29])(c[9],c[64]),c[12])(c[64],c[78]),[])||(0,c[12])(c[19],c[18])%(0,c[32])(c[64],c[33])}}catch(d){return"enhanced_except_v5wBwOP-_w8_"+a}return b.join("")};;