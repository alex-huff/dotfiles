(function(Oe,M){typeof exports=="object"&&typeof module<"u"?module.exports=M():typeof define=="function"&&define.amd?define(M):(Oe=typeof globalThis<"u"?globalThis:Oe||self,Oe.WebGLFluid=M())})(this,function(){"use strict";(function(M,_){typeof exports=="object"&&typeof module<"u"?_(exports):typeof define=="function"&&define.amd?define(["exports"],_):_(M.dat={})})(globalThis,function(M){function _(e,t){var i=e.__state.conversionName.toString(),r=Math.round(e.r),u=Math.round(e.g),c=Math.round(e.b),h=e.a,g=Math.round(e.h),b=e.s.toFixed(1),v=e.v.toFixed(1);if(t||i==="THREE_CHAR_HEX"||i==="SIX_CHAR_HEX"){for(var S=e.hex.toString(16);S.length<6;)S="0"+S;return"#"+S}return i==="CSS_RGB"?"rgb("+r+","+u+","+c+")":i==="CSS_RGBA"?"rgba("+r+","+u+","+c+","+h+")":i==="HEX"?"0x"+e.hex.toString(16):i==="RGB_ARRAY"?"["+r+","+u+","+c+"]":i==="RGBA_ARRAY"?"["+r+","+u+","+c+","+h+"]":i==="RGB_OBJ"?"{r:"+r+",g:"+u+",b:"+c+"}":i==="RGBA_OBJ"?"{r:"+r+",g:"+u+",b:"+c+",a:"+h+"}":i==="HSV_OBJ"?"{h:"+g+",s:"+b+",v:"+v+"}":i==="HSVA_OBJ"?"{h:"+g+",s:"+b+",v:"+v+",a:"+h+"}":"unknown format"}function D(e,t,i){Object.defineProperty(e,t,{get:function(){return this.__state.space==="RGB"?this.__state[t]:(y.recalculateRGB(this,t,i),this.__state[t])},set:function(r){this.__state.space!=="RGB"&&(y.recalculateRGB(this,t,i),this.__state.space="RGB"),this.__state[t]=r}})}function he(e,t){Object.defineProperty(e,t,{get:function(){return this.__state.space==="HSV"?this.__state[t]:(y.recalculateHSV(this),this.__state[t])},set:function(i){this.__state.space!=="HSV"&&(y.recalculateHSV(this),this.__state.space="HSV"),this.__state[t]=i}})}function U(e){if(e==="0"||d.isUndefined(e))return 0;var t=e.match(J);return d.isNull(t)?0:parseFloat(t[1])}function me(e){var t=e.toString();return t.indexOf(".")>-1?t.length-t.indexOf(".")-1:0}function ee(e,t){var i=Math.pow(10,t);return Math.round(e*i)/i}function n(e,t,i,r,u){return r+(e-t)/(i-t)*(u-r)}function P(e,t,i,r){e.style.background="",d.each(Ae,function(u){e.style.cssText+="background: "+u+"linear-gradient("+t+", "+i+" 0%, "+r+" 100%); "})}function Qe(e){e.style.background="",e.style.cssText+="background: -moz-linear-gradient(top,  #ff0000 0%, #ff00ff 17%, #0000ff 34%, #00ffff 50%, #00ff00 67%, #ffff00 84%, #ff0000 100%);",e.style.cssText+="background: -webkit-linear-gradient(top,  #ff0000 0%,#ff00ff 17%,#0000ff 34%,#00ffff 50%,#00ff00 67%,#ffff00 84%,#ff0000 100%);",e.style.cssText+="background: -o-linear-gradient(top,  #ff0000 0%,#ff00ff 17%,#0000ff 34%,#00ffff 50%,#00ff00 67%,#ffff00 84%,#ff0000 100%);",e.style.cssText+="background: -ms-linear-gradient(top,  #ff0000 0%,#ff00ff 17%,#0000ff 34%,#00ffff 50%,#00ff00 67%,#ffff00 84%,#ff0000 100%);",e.style.cssText+="background: linear-gradient(top,  #ff0000 0%,#ff00ff 17%,#0000ff 34%,#00ffff 50%,#00ff00 67%,#ffff00 84%,#ff0000 100%);"}function X(e,t,i){var r=document.createElement("li");return t&&r.appendChild(t),i?e.__ul.insertBefore(r,i):e.__ul.appendChild(r),e.onResize(),r}function Pe(e){l.unbind(window,"resize",e.__resizeHandler),e.saveToLocalStorageIfPossible&&l.unbind(window,"unload",e.saveToLocalStorageIfPossible)}function Le(e,t){var i=e.__preset_select[e.__preset_select.selectedIndex];i.innerHTML=t?i.value+"*":i.value}function qe(e,t,i){if(i.__li=t,i.__gui=e,d.extend(i,{options:function(c){if(arguments.length>1){var h=i.__li.nextElementSibling;return i.remove(),ae(e,i.object,i.property,{before:h,factoryArgs:[d.toArray(arguments)]})}if(d.isArray(c)||d.isObject(c)){var g=i.__li.nextElementSibling;return i.remove(),ae(e,i.object,i.property,{before:g,factoryArgs:[c]})}},name:function(c){return i.__li.firstElementChild.firstElementChild.innerHTML=c,i},listen:function(){return i.__gui.listen(i),i},remove:function(){return i.__gui.remove(i),i}}),i instanceof ue){var r=new le(i.object,i.property,{min:i.__min,max:i.__max,step:i.__step});d.each(["updateDisplay","onChange","onFinishChange","step"],function(c){var h=i[c],g=r[c];i[c]=r[c]=function(){var b=Array.prototype.slice.call(arguments);return g.apply(r,b),h.apply(i,b)}}),l.addClass(t,"has-slider"),i.domElement.insertBefore(r.domElement,i.domElement.firstElementChild)}else if(i instanceof le){var u=function(c){if(d.isNumber(i.__min)&&d.isNumber(i.__max)){var h=i.__li.firstElementChild.firstElementChild.innerHTML,g=i.__gui.__listening.indexOf(i)>-1;i.remove();var b=ae(e,i.object,i.property,{before:i.__li.nextElementSibling,factoryArgs:[i.__min,i.__max,i.__step]});return b.name(h),g&&b.listen(),b}return c};i.min=d.compose(u,i.min),i.max=d.compose(u,i.max)}else i instanceof se?(l.bind(t,"click",function(){l.fakeEvent(i.__checkbox,"click")}),l.bind(i.__checkbox,"click",function(c){c.stopPropagation()})):i instanceof Se?(l.bind(t,"click",function(){l.fakeEvent(i.__button,"click")}),l.bind(t,"mouseover",function(){l.addClass(i.__button,"hover")}),l.bind(t,"mouseout",function(){l.removeClass(i.__button,"hover")})):i instanceof ge&&(l.addClass(t,"color"),i.updateDisplay=d.compose(function(c){return t.style.borderLeftColor=i.__color.toString(),c},i.updateDisplay),i.updateDisplay());i.setValue=d.compose(function(c){return e.getRoot().__preset_select&&i.isModified()&&Le(e.getRoot(),!0),c},i.setValue)}function B(e,t){var i=e.getRoot(),r=i.__rememberedObjects.indexOf(t.object);if(r!==-1){var u=i.__rememberedObjectIndecesToControllers[r];if(u===void 0&&(u={},i.__rememberedObjectIndecesToControllers[r]=u),u[t.property]=t,i.load&&i.load.remembered){var c=i.load.remembered,h=void 0;if(c[e.preset])h=c[e.preset];else{if(!c[I])return;h=c[I]}if(h[r]&&h[r][t.property]!==void 0){var g=h[r][t.property];t.initialValue=g,t.setValue(g)}}}}function ae(e,t,i,r){if(t[i]===void 0)throw new Error('Object "'+t+'" has no property "'+i+'"');var u=void 0;if(r.color)u=new ge(t,i);else{var c=[t,i].concat(r.factoryArgs);u=Re.apply(e,c)}r.before instanceof x&&(r.before=r.before.__li),B(e,u),l.addClass(u.domElement,"c");var h=document.createElement("span");l.addClass(h,"property-name"),h.innerHTML=u.property;var g=document.createElement("div");g.appendChild(h),g.appendChild(u.domElement);var b=X(e,g,r.before);return l.addClass(b,C.CLASS_CONTROLLER_ROW),u instanceof ge?l.addClass(b,"color"):l.addClass(b,tt(u.getValue())),qe(e,b,u),e.__controllers.push(u),u}function te(e,t){return document.location.href+"."+t}function F(e,t,i){var r=document.createElement("option");r.innerHTML=t,r.value=t,e.__preset_select.appendChild(r),i&&(e.__preset_select.selectedIndex=e.__preset_select.length-1)}function Ie(e,t){t.style.display=e.useLocalStorage?"block":"none"}function k(e){var t=e.__save_row=document.createElement("li");l.addClass(e.domElement,"has-save"),e.__ul.insertBefore(t,e.__ul.firstChild),l.addClass(t,"save-row");var i=document.createElement("span");i.innerHTML="&nbsp;",l.addClass(i,"button gears");var r=document.createElement("span");r.innerHTML="Save",l.addClass(r,"button"),l.addClass(r,"save");var u=document.createElement("span");u.innerHTML="New",l.addClass(u,"button"),l.addClass(u,"save-as");var c=document.createElement("span");c.innerHTML="Revert",l.addClass(c,"button"),l.addClass(c,"revert");var h=e.__preset_select=document.createElement("select");if(e.load&&e.load.remembered?d.each(e.load.remembered,function(S,T){F(e,T,T===e.preset)}):F(e,I,!1),l.bind(h,"change",function(){for(var S=0;S<e.__preset_select.length;S++)e.__preset_select[S].innerHTML=e.__preset_select[S].value;e.preset=this.value}),t.appendChild(h),t.appendChild(i),t.appendChild(r),t.appendChild(u),t.appendChild(c),oe){var g=document.getElementById("dg-local-explain"),b=document.getElementById("dg-local-storage");document.getElementById("dg-save-locally").style.display="block",localStorage.getItem(te(e,"isLocal"))==="true"&&b.setAttribute("checked","checked"),Ie(e,g),l.bind(b,"change",function(){e.useLocalStorage=!e.useLocalStorage,Ie(e,g)})}var v=document.getElementById("dg-new-constructor");l.bind(v,"keydown",function(S){!S.metaKey||S.which!==67&&S.keyCode!==67||ce.hide()}),l.bind(i,"click",function(){v.innerHTML=JSON.stringify(e.getSaveObject(),void 0,2),ce.show(),v.focus(),v.select()}),l.bind(r,"click",function(){e.save()}),l.bind(u,"click",function(){var S=prompt("Enter a new preset name.");S&&e.saveAs(S)}),l.bind(c,"click",function(){e.revert()})}function Ze(e){function t(c){return c.preventDefault(),e.width+=u-c.clientX,e.onResize(),u=c.clientX,!1}function i(){l.removeClass(e.__closeButton,C.CLASS_DRAG),l.unbind(window,"mousemove",t),l.unbind(window,"mouseup",i)}function r(c){return c.preventDefault(),u=c.clientX,l.addClass(e.__closeButton,C.CLASS_DRAG),l.bind(window,"mousemove",t),l.bind(window,"mouseup",i),!1}var u=void 0;e.__resize_handle=document.createElement("div"),d.extend(e.__resize_handle.style,{width:"6px",marginLeft:"-3px",height:"200px",cursor:"ew-resize",position:"absolute"}),l.bind(e.__resize_handle,"mousedown",r),l.bind(e.__closeButton,"mousedown",r),e.domElement.insertBefore(e.__resize_handle,e.domElement.firstElementChild)}function Ne(e,t){e.domElement.style.width=t+"px",e.__save_row&&e.autoPlace&&(e.__save_row.style.width=t+"px"),e.__closeButton&&(e.__closeButton.style.width=t+"px")}function ye(e,t){var i={};return d.each(e.__rememberedObjects,function(r,u){var c={},h=e.__rememberedObjectIndecesToControllers[u];d.each(h,function(g,b){c[b]=t?g.initialValue:g.getValue()}),i[u]=c}),i}function $e(e){for(var t=0;t<e.__preset_select.length;t++)e.__preset_select[t].value===e.preset&&(e.__preset_select.selectedIndex=t)}function Me(e){e.length!==0&&Ge.call(window,function(){Me(e)}),d.each(e,function(t){t.updateDisplay()})}var ze=Array.prototype.forEach,_e=Array.prototype.slice,d={BREAK:{},extend:function(e){return this.each(_e.call(arguments,1),function(t){(this.isObject(t)?Object.keys(t):[]).forEach((function(i){this.isUndefined(t[i])||(e[i]=t[i])}).bind(this))},this),e},defaults:function(e){return this.each(_e.call(arguments,1),function(t){(this.isObject(t)?Object.keys(t):[]).forEach((function(i){this.isUndefined(e[i])&&(e[i]=t[i])}).bind(this))},this),e},compose:function(){var e=_e.call(arguments);return function(){for(var t=_e.call(arguments),i=e.length-1;i>=0;i--)t=[e[i].apply(this,t)];return t[0]}},each:function(e,t,i){if(e){if(ze&&e.forEach&&e.forEach===ze)e.forEach(t,i);else if(e.length===e.length+0){var r=void 0,u=void 0;for(r=0,u=e.length;r<u;r++)if(r in e&&t.call(i,e[r],r)===this.BREAK)return}else for(var c in e)if(t.call(i,e[c],c)===this.BREAK)return}},defer:function(e){setTimeout(e,0)},debounce:function(e,t,i){var r=void 0;return function(){var u=this,c=arguments,h=i||!r;clearTimeout(r),r=setTimeout(function(){r=null,i||e.apply(u,c)},t),h&&e.apply(u,c)}},toArray:function(e){return e.toArray?e.toArray():_e.call(e)},isUndefined:function(e){return e===void 0},isNull:function(e){return e===null},isNaN:function(e){function t(i){return e.apply(this,arguments)}return t.toString=function(){return e.toString()},t}(function(e){return isNaN(e)}),isArray:Array.isArray||function(e){return e.constructor===Array},isObject:function(e){return e===Object(e)},isNumber:function(e){return e===e+0},isString:function(e){return e===e+""},isBoolean:function(e){return e===!1||e===!0},isFunction:function(e){return Object.prototype.toString.call(e)==="[object Function]"}},et=[{litmus:d.isString,conversions:{THREE_CHAR_HEX:{read:function(e){var t=e.match(/^#([A-F0-9])([A-F0-9])([A-F0-9])$/i);return t!==null&&{space:"HEX",hex:parseInt("0x"+t[1].toString()+t[1].toString()+t[2].toString()+t[2].toString()+t[3].toString()+t[3].toString(),0)}},write:_},SIX_CHAR_HEX:{read:function(e){var t=e.match(/^#([A-F0-9]{6})$/i);return t!==null&&{space:"HEX",hex:parseInt("0x"+t[1].toString(),0)}},write:_},CSS_RGB:{read:function(e){var t=e.match(/^rgb\(\s*(.+)\s*,\s*(.+)\s*,\s*(.+)\s*\)/);return t!==null&&{space:"RGB",r:parseFloat(t[1]),g:parseFloat(t[2]),b:parseFloat(t[3])}},write:_},CSS_RGBA:{read:function(e){var t=e.match(/^rgba\(\s*(.+)\s*,\s*(.+)\s*,\s*(.+)\s*,\s*(.+)\s*\)/);return t!==null&&{space:"RGB",r:parseFloat(t[1]),g:parseFloat(t[2]),b:parseFloat(t[3]),a:parseFloat(t[4])}},write:_}}},{litmus:d.isNumber,conversions:{HEX:{read:function(e){return{space:"HEX",hex:e,conversionName:"HEX"}},write:function(e){return e.hex}}}},{litmus:d.isArray,conversions:{RGB_ARRAY:{read:function(e){return e.length===3&&{space:"RGB",r:e[0],g:e[1],b:e[2]}},write:function(e){return[e.r,e.g,e.b]}},RGBA_ARRAY:{read:function(e){return e.length===4&&{space:"RGB",r:e[0],g:e[1],b:e[2],a:e[3]}},write:function(e){return[e.r,e.g,e.b,e.a]}}}},{litmus:d.isObject,conversions:{RGBA_OBJ:{read:function(e){return!!(d.isNumber(e.r)&&d.isNumber(e.g)&&d.isNumber(e.b)&&d.isNumber(e.a))&&{space:"RGB",r:e.r,g:e.g,b:e.b,a:e.a}},write:function(e){return{r:e.r,g:e.g,b:e.b,a:e.a}}},RGB_OBJ:{read:function(e){return!!(d.isNumber(e.r)&&d.isNumber(e.g)&&d.isNumber(e.b))&&{space:"RGB",r:e.r,g:e.g,b:e.b}},write:function(e){return{r:e.r,g:e.g,b:e.b}}},HSVA_OBJ:{read:function(e){return!!(d.isNumber(e.h)&&d.isNumber(e.s)&&d.isNumber(e.v)&&d.isNumber(e.a))&&{space:"HSV",h:e.h,s:e.s,v:e.v,a:e.a}},write:function(e){return{h:e.h,s:e.s,v:e.v,a:e.a}}},HSV_OBJ:{read:function(e){return!!(d.isNumber(e.h)&&d.isNumber(e.s)&&d.isNumber(e.v))&&{space:"HSV",h:e.h,s:e.s,v:e.v}},write:function(e){return{h:e.h,s:e.s,v:e.v}}}}}],pe=void 0,Ee=void 0,Te=function(){Ee=!1;var e=arguments.length>1?d.toArray(arguments):arguments[0];return d.each(et,function(t){if(t.litmus(e))return d.each(t.conversions,function(i,r){if(pe=i.read(e),Ee===!1&&pe!==!1)return Ee=pe,pe.conversionName=r,pe.conversion=i,d.BREAK}),d.BREAK}),Ee},He=void 0,ve={hsv_to_rgb:function(e,t,i){var r=Math.floor(e/60)%6,u=e/60-Math.floor(e/60),c=i*(1-t),h=i*(1-u*t),g=i*(1-(1-u)*t),b=[[i,g,c],[h,i,c],[c,i,g],[c,h,i],[g,c,i],[i,c,h]][r];return{r:255*b[0],g:255*b[1],b:255*b[2]}},rgb_to_hsv:function(e,t,i){var r=Math.min(e,t,i),u=Math.max(e,t,i),c=u-r,h=void 0,g=void 0;return u===0?{h:NaN,s:0,v:0}:(g=c/u,h=e===u?(t-i)/c:t===u?2+(i-e)/c:4+(e-t)/c,(h/=6)<0&&(h+=1),{h:360*h,s:g,v:u/255})},rgb_to_hex:function(e,t,i){var r=this.hex_with_component(0,2,e);return r=this.hex_with_component(r,1,t),r=this.hex_with_component(r,0,i)},component_from_hex:function(e,t){return e>>8*t&255},hex_with_component:function(e,t,i){return i<<(He=8*t)|e&~(255<<He)}},tt=typeof Symbol=="function"&&typeof Symbol.iterator=="symbol"?function(e){return typeof e}:function(e){return e&&typeof Symbol=="function"&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},z=function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")},H=function(){function e(t,i){for(var r=0;r<i.length;r++){var u=i[r];u.enumerable=u.enumerable||!1,u.configurable=!0,"value"in u&&(u.writable=!0),Object.defineProperty(t,u.key,u)}}return function(t,i,r){return i&&e(t.prototype,i),r&&e(t,r),t}}(),W=function e(t,i,r){t===null&&(t=Function.prototype);var u=Object.getOwnPropertyDescriptor(t,i);if(u===void 0){var c=Object.getPrototypeOf(t);return c===null?void 0:e(c,i,r)}if("value"in u)return u.value;var h=u.get;if(h!==void 0)return h.call(r)},K=function(e,t){if(typeof t!="function"&&t!==null)throw new TypeError("Super expression must either be null or a function, not "+typeof t);e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,enumerable:!1,writable:!0,configurable:!0}}),t&&(Object.setPrototypeOf?Object.setPrototypeOf(e,t):e.__proto__=t)},A=function(e,t){if(!e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return!t||typeof t!="object"&&typeof t!="function"?e:t},y=function(){function e(){if(z(this,e),this.__state=Te.apply(this,arguments),this.__state===!1)throw new Error("Failed to interpret color arguments");this.__state.a=this.__state.a||1}return H(e,[{key:"toString",value:function(){return _(this)}},{key:"toHexString",value:function(){return _(this,!0)}},{key:"toOriginal",value:function(){return this.__state.conversion.write(this)}}]),e}();y.recalculateRGB=function(e,t,i){if(e.__state.space==="HEX")e.__state[t]=ve.component_from_hex(e.__state.hex,i);else{if(e.__state.space!=="HSV")throw new Error("Corrupted color state");d.extend(e.__state,ve.hsv_to_rgb(e.__state.h,e.__state.s,e.__state.v))}},y.recalculateHSV=function(e){var t=ve.rgb_to_hsv(e.r,e.g,e.b);d.extend(e.__state,{s:t.s,v:t.v}),d.isNaN(t.h)?d.isUndefined(e.__state.h)&&(e.__state.h=0):e.__state.h=t.h},y.COMPONENTS=["r","g","b","h","s","v","hex","a"],D(y.prototype,"r",2),D(y.prototype,"g",1),D(y.prototype,"b",0),he(y.prototype,"h"),he(y.prototype,"s"),he(y.prototype,"v"),Object.defineProperty(y.prototype,"a",{get:function(){return this.__state.a},set:function(e){this.__state.a=e}}),Object.defineProperty(y.prototype,"hex",{get:function(){return!this.__state.space!=="HEX"&&(this.__state.hex=ve.rgb_to_hex(this.r,this.g,this.b)),this.__state.hex},set:function(e){this.__state.space="HEX",this.__state.hex=e}});var x=function(){function e(t,i){z(this,e),this.initialValue=t[i],this.domElement=document.createElement("div"),this.object=t,this.property=i,this.__onChange=void 0,this.__onFinishChange=void 0}return H(e,[{key:"onChange",value:function(t){return this.__onChange=t,this}},{key:"onFinishChange",value:function(t){return this.__onFinishChange=t,this}},{key:"setValue",value:function(t){return this.object[this.property]=t,this.__onChange&&this.__onChange.call(this,t),this.updateDisplay(),this}},{key:"getValue",value:function(){return this.object[this.property]}},{key:"updateDisplay",value:function(){return this}},{key:"isModified",value:function(){return this.initialValue!==this.getValue()}}]),e}(),Fe={HTMLEvents:["change"],MouseEvents:["click","mousemove","mousedown","mouseup","mouseover"],KeyboardEvents:["keydown"]},we={};d.each(Fe,function(e,t){d.each(e,function(i){we[i]=t})});var J=/(\d+(\.\d+)?)px/,l={makeSelectable:function(e,t){e!==void 0&&e.style!==void 0&&(e.onselectstart=t?function(){return!1}:function(){},e.style.MozUserSelect=t?"auto":"none",e.style.KhtmlUserSelect=t?"auto":"none",e.unselectable=t?"on":"off")},makeFullscreen:function(e,t,i){var r=i,u=t;d.isUndefined(u)&&(u=!0),d.isUndefined(r)&&(r=!0),e.style.position="absolute",u&&(e.style.left=0,e.style.right=0),r&&(e.style.top=0,e.style.bottom=0)},fakeEvent:function(e,t,i,r){var u=i||{},c=we[t];if(!c)throw new Error("Event type "+t+" not supported.");var h=document.createEvent(c);switch(c){case"MouseEvents":var g=u.x||u.clientX||0,b=u.y||u.clientY||0;h.initMouseEvent(t,u.bubbles||!1,u.cancelable||!0,window,u.clickCount||1,0,0,g,b,!1,!1,!1,!1,0,null);break;case"KeyboardEvents":var v=h.initKeyboardEvent||h.initKeyEvent;d.defaults(u,{cancelable:!0,ctrlKey:!1,altKey:!1,shiftKey:!1,metaKey:!1,keyCode:void 0,charCode:void 0}),v(t,u.bubbles||!1,u.cancelable,window,u.ctrlKey,u.altKey,u.shiftKey,u.metaKey,u.keyCode,u.charCode);break;default:h.initEvent(t,u.bubbles||!1,u.cancelable||!0)}d.defaults(h,r),e.dispatchEvent(h)},bind:function(e,t,i,r){var u=r||!1;return e.addEventListener?e.addEventListener(t,i,u):e.attachEvent&&e.attachEvent("on"+t,i),l},unbind:function(e,t,i,r){var u=r||!1;return e.removeEventListener?e.removeEventListener(t,i,u):e.detachEvent&&e.detachEvent("on"+t,i),l},addClass:function(e,t){if(e.className===void 0)e.className=t;else if(e.className!==t){var i=e.className.split(/ +/);i.indexOf(t)===-1&&(i.push(t),e.className=i.join(" ").replace(/^\s+/,"").replace(/\s+$/,""))}return l},removeClass:function(e,t){if(t)if(e.className===t)e.removeAttribute("class");else{var i=e.className.split(/ +/),r=i.indexOf(t);r!==-1&&(i.splice(r,1),e.className=i.join(" "))}else e.className=void 0;return l},hasClass:function(e,t){return new RegExp("(?:^|\\s+)"+t+"(?:\\s+|$)").test(e.className)||!1},getWidth:function(e){var t=getComputedStyle(e);return U(t["border-left-width"])+U(t["border-right-width"])+U(t["padding-left"])+U(t["padding-right"])+U(t.width)},getHeight:function(e){var t=getComputedStyle(e);return U(t["border-top-width"])+U(t["border-bottom-width"])+U(t["padding-top"])+U(t["padding-bottom"])+U(t.height)},getOffset:function(e){var t=e,i={left:0,top:0};if(t.offsetParent)do i.left+=t.offsetLeft,i.top+=t.offsetTop,t=t.offsetParent;while(t);return i},isActive:function(e){return e===document.activeElement&&(e.type||e.href)}},se=function(e){function t(i,r){z(this,t);var u=A(this,(t.__proto__||Object.getPrototypeOf(t)).call(this,i,r)),c=u;return u.__prev=u.getValue(),u.__checkbox=document.createElement("input"),u.__checkbox.setAttribute("type","checkbox"),l.bind(u.__checkbox,"change",function(){c.setValue(!c.__prev)},!1),u.domElement.appendChild(u.__checkbox),u.updateDisplay(),u}return K(t,x),H(t,[{key:"setValue",value:function(i){var r=W(t.prototype.__proto__||Object.getPrototypeOf(t.prototype),"setValue",this).call(this,i);return this.__onFinishChange&&this.__onFinishChange.call(this,this.getValue()),this.__prev=this.getValue(),r}},{key:"updateDisplay",value:function(){return this.getValue()===!0?(this.__checkbox.setAttribute("checked","checked"),this.__checkbox.checked=!0,this.__prev=!0):(this.__checkbox.checked=!1,this.__prev=!1),W(t.prototype.__proto__||Object.getPrototypeOf(t.prototype),"updateDisplay",this).call(this)}}]),t}(),Ue=function(e){function t(i,r,u){z(this,t);var c=A(this,(t.__proto__||Object.getPrototypeOf(t)).call(this,i,r)),h=u,g=c;if(c.__select=document.createElement("select"),d.isArray(h)){var b={};d.each(h,function(v){b[v]=v}),h=b}return d.each(h,function(v,S){var T=document.createElement("option");T.innerHTML=S,T.setAttribute("value",v),g.__select.appendChild(T)}),c.updateDisplay(),l.bind(c.__select,"change",function(){var v=this.options[this.selectedIndex].value;g.setValue(v)}),c.domElement.appendChild(c.__select),c}return K(t,x),H(t,[{key:"setValue",value:function(i){var r=W(t.prototype.__proto__||Object.getPrototypeOf(t.prototype),"setValue",this).call(this,i);return this.__onFinishChange&&this.__onFinishChange.call(this,this.getValue()),r}},{key:"updateDisplay",value:function(){return l.isActive(this.__select)?this:(this.__select.value=this.getValue(),W(t.prototype.__proto__||Object.getPrototypeOf(t.prototype),"updateDisplay",this).call(this))}}]),t}(),Be=function(e){function t(i,r){function u(){h.setValue(h.__input.value)}z(this,t);var c=A(this,(t.__proto__||Object.getPrototypeOf(t)).call(this,i,r)),h=c;return c.__input=document.createElement("input"),c.__input.setAttribute("type","text"),l.bind(c.__input,"keyup",u),l.bind(c.__input,"change",u),l.bind(c.__input,"blur",function(){h.__onFinishChange&&h.__onFinishChange.call(h,h.getValue())}),l.bind(c.__input,"keydown",function(g){g.keyCode===13&&this.blur()}),c.updateDisplay(),c.domElement.appendChild(c.__input),c}return K(t,x),H(t,[{key:"updateDisplay",value:function(){return l.isActive(this.__input)||(this.__input.value=this.getValue()),W(t.prototype.__proto__||Object.getPrototypeOf(t.prototype),"updateDisplay",this).call(this)}}]),t}(),ie=function(e){function t(i,r,u){z(this,t);var c=A(this,(t.__proto__||Object.getPrototypeOf(t)).call(this,i,r)),h=u||{};return c.__min=h.min,c.__max=h.max,c.__step=h.step,d.isUndefined(c.__step)?c.initialValue===0?c.__impliedStep=1:c.__impliedStep=Math.pow(10,Math.floor(Math.log(Math.abs(c.initialValue))/Math.LN10))/10:c.__impliedStep=c.__step,c.__precision=me(c.__impliedStep),c}return K(t,x),H(t,[{key:"setValue",value:function(i){var r=i;return this.__min!==void 0&&r<this.__min?r=this.__min:this.__max!==void 0&&r>this.__max&&(r=this.__max),this.__step!==void 0&&r%this.__step!=0&&(r=Math.round(r/this.__step)*this.__step),W(t.prototype.__proto__||Object.getPrototypeOf(t.prototype),"setValue",this).call(this,r)}},{key:"min",value:function(i){return this.__min=i,this}},{key:"max",value:function(i){return this.__max=i,this}},{key:"step",value:function(i){return this.__step=i,this.__impliedStep=i,this.__precision=me(i),this}}]),t}(),le=function(e){function t(i,r,u){function c(){v.__onFinishChange&&v.__onFinishChange.call(v,v.getValue())}function h(T){var m=S-T.clientY;v.setValue(v.getValue()+m*v.__impliedStep),S=T.clientY}function g(){l.unbind(window,"mousemove",h),l.unbind(window,"mouseup",g),c()}z(this,t);var b=A(this,(t.__proto__||Object.getPrototypeOf(t)).call(this,i,r,u));b.__truncationSuspended=!1;var v=b,S=void 0;return b.__input=document.createElement("input"),b.__input.setAttribute("type","text"),l.bind(b.__input,"change",function(){var T=parseFloat(v.__input.value);d.isNaN(T)||v.setValue(T)}),l.bind(b.__input,"blur",function(){c()}),l.bind(b.__input,"mousedown",function(T){l.bind(window,"mousemove",h),l.bind(window,"mouseup",g),S=T.clientY}),l.bind(b.__input,"keydown",function(T){T.keyCode===13&&(v.__truncationSuspended=!0,this.blur(),v.__truncationSuspended=!1,c())}),b.updateDisplay(),b.domElement.appendChild(b.__input),b}return K(t,ie),H(t,[{key:"updateDisplay",value:function(){return this.__input.value=this.__truncationSuspended?this.getValue():ee(this.getValue(),this.__precision),W(t.prototype.__proto__||Object.getPrototypeOf(t.prototype),"updateDisplay",this).call(this)}}]),t}(),ue=function(e){function t(i,r,u,c,h){function g(R){R.preventDefault();var q=m.__background.getBoundingClientRect();return m.setValue(n(R.clientX,q.left,q.right,m.__min,m.__max)),!1}function b(){l.unbind(window,"mousemove",g),l.unbind(window,"mouseup",b),m.__onFinishChange&&m.__onFinishChange.call(m,m.getValue())}function v(R){var q=R.touches[0].clientX,N=m.__background.getBoundingClientRect();m.setValue(n(q,N.left,N.right,m.__min,m.__max))}function S(){l.unbind(window,"touchmove",v),l.unbind(window,"touchend",S),m.__onFinishChange&&m.__onFinishChange.call(m,m.getValue())}z(this,t);var T=A(this,(t.__proto__||Object.getPrototypeOf(t)).call(this,i,r,{min:u,max:c,step:h})),m=T;return T.__background=document.createElement("div"),T.__foreground=document.createElement("div"),l.bind(T.__background,"mousedown",function(R){document.activeElement.blur(),l.bind(window,"mousemove",g),l.bind(window,"mouseup",b),g(R)}),l.bind(T.__background,"touchstart",function(R){R.touches.length===1&&(l.bind(window,"touchmove",v),l.bind(window,"touchend",S),v(R))}),l.addClass(T.__background,"slider"),l.addClass(T.__foreground,"slider-fg"),T.updateDisplay(),T.__background.appendChild(T.__foreground),T.domElement.appendChild(T.__background),T}return K(t,ie),H(t,[{key:"updateDisplay",value:function(){var i=(this.getValue()-this.__min)/(this.__max-this.__min);return this.__foreground.style.width=100*i+"%",W(t.prototype.__proto__||Object.getPrototypeOf(t.prototype),"updateDisplay",this).call(this)}}]),t}(),Se=function(e){function t(i,r,u){z(this,t);var c=A(this,(t.__proto__||Object.getPrototypeOf(t)).call(this,i,r)),h=c;return c.__button=document.createElement("div"),c.__button.innerHTML=u===void 0?"Fire":u,l.bind(c.__button,"click",function(g){return g.preventDefault(),h.fire(),!1}),l.addClass(c.__button,"button"),c.domElement.appendChild(c.__button),c}return K(t,x),H(t,[{key:"fire",value:function(){this.__onChange&&this.__onChange.call(this),this.getValue().call(this.object),this.__onFinishChange&&this.__onFinishChange.call(this,this.getValue())}}]),t}(),ge=function(e){function t(i,r){function u(N){S(N),l.bind(window,"mousemove",S),l.bind(window,"touchmove",S),l.bind(window,"mouseup",h),l.bind(window,"touchend",h)}function c(N){T(N),l.bind(window,"mousemove",T),l.bind(window,"touchmove",T),l.bind(window,"mouseup",g),l.bind(window,"touchend",g)}function h(){l.unbind(window,"mousemove",S),l.unbind(window,"touchmove",S),l.unbind(window,"mouseup",h),l.unbind(window,"touchend",h),v()}function g(){l.unbind(window,"mousemove",T),l.unbind(window,"touchmove",T),l.unbind(window,"mouseup",g),l.unbind(window,"touchend",g),v()}function b(){var N=Te(this.value);N!==!1?(R.__color.__state=N,R.setValue(R.__color.toOriginal())):this.value=R.__color.toString()}function v(){R.__onFinishChange&&R.__onFinishChange.call(R,R.__color.toOriginal())}function S(N){N.type.indexOf("touch")===-1&&N.preventDefault();var V=R.__saturation_field.getBoundingClientRect(),Z=N.touches&&N.touches[0]||N,We=Z.clientX,Ke=Z.clientY,fe=(We-V.left)/(V.right-V.left),xe=1-(Ke-V.top)/(V.bottom-V.top);return xe>1?xe=1:xe<0&&(xe=0),fe>1?fe=1:fe<0&&(fe=0),R.__color.v=xe,R.__color.s=fe,R.setValue(R.__color.toOriginal()),!1}function T(N){N.type.indexOf("touch")===-1&&N.preventDefault();var V=R.__hue_field.getBoundingClientRect(),Z=1-((N.touches&&N.touches[0]||N).clientY-V.top)/(V.bottom-V.top);return Z>1?Z=1:Z<0&&(Z=0),R.__color.h=360*Z,R.setValue(R.__color.toOriginal()),!1}z(this,t);var m=A(this,(t.__proto__||Object.getPrototypeOf(t)).call(this,i,r));m.__color=new y(m.getValue()),m.__temp=new y(0);var R=m;m.domElement=document.createElement("div"),l.makeSelectable(m.domElement,!1),m.__selector=document.createElement("div"),m.__selector.className="selector",m.__saturation_field=document.createElement("div"),m.__saturation_field.className="saturation-field",m.__field_knob=document.createElement("div"),m.__field_knob.className="field-knob",m.__field_knob_border="2px solid ",m.__hue_knob=document.createElement("div"),m.__hue_knob.className="hue-knob",m.__hue_field=document.createElement("div"),m.__hue_field.className="hue-field",m.__input=document.createElement("input"),m.__input.type="text",m.__input_textShadow="0 1px 1px ",l.bind(m.__input,"keydown",function(N){N.keyCode===13&&b.call(this)}),l.bind(m.__input,"blur",b),l.bind(m.__selector,"mousedown",function(){l.addClass(this,"drag").bind(window,"mouseup",function(){l.removeClass(R.__selector,"drag")})}),l.bind(m.__selector,"touchstart",function(){l.addClass(this,"drag").bind(window,"touchend",function(){l.removeClass(R.__selector,"drag")})});var q=document.createElement("div");return d.extend(m.__selector.style,{width:"122px",height:"102px",padding:"3px",backgroundColor:"#222",boxShadow:"0px 1px 3px rgba(0,0,0,0.3)"}),d.extend(m.__field_knob.style,{position:"absolute",width:"12px",height:"12px",border:m.__field_knob_border+(m.__color.v<.5?"#fff":"#000"),boxShadow:"0px 1px 3px rgba(0,0,0,0.5)",borderRadius:"12px",zIndex:1}),d.extend(m.__hue_knob.style,{position:"absolute",width:"15px",height:"2px",borderRight:"4px solid #fff",zIndex:1}),d.extend(m.__saturation_field.style,{width:"100px",height:"100px",border:"1px solid #555",marginRight:"3px",display:"inline-block",cursor:"pointer"}),d.extend(q.style,{width:"100%",height:"100%",background:"none"}),P(q,"top","rgba(0,0,0,0)","#000"),d.extend(m.__hue_field.style,{width:"15px",height:"100px",border:"1px solid #555",cursor:"ns-resize",position:"absolute",top:"3px",right:"3px"}),Qe(m.__hue_field),d.extend(m.__input.style,{outline:"none",textAlign:"center",color:"#fff",border:0,fontWeight:"bold",textShadow:m.__input_textShadow+"rgba(0,0,0,0.7)"}),l.bind(m.__saturation_field,"mousedown",u),l.bind(m.__saturation_field,"touchstart",u),l.bind(m.__field_knob,"mousedown",u),l.bind(m.__field_knob,"touchstart",u),l.bind(m.__hue_field,"mousedown",c),l.bind(m.__hue_field,"touchstart",c),m.__saturation_field.appendChild(q),m.__selector.appendChild(m.__field_knob),m.__selector.appendChild(m.__saturation_field),m.__selector.appendChild(m.__hue_field),m.__hue_field.appendChild(m.__hue_knob),m.domElement.appendChild(m.__input),m.domElement.appendChild(m.__selector),m.updateDisplay(),m}return K(t,x),H(t,[{key:"updateDisplay",value:function(){var i=Te(this.getValue());if(i!==!1){var r=!1;d.each(y.COMPONENTS,function(h){if(!d.isUndefined(i[h])&&!d.isUndefined(this.__color.__state[h])&&i[h]!==this.__color.__state[h])return r=!0,{}},this),r&&d.extend(this.__color.__state,i)}d.extend(this.__temp.__state,this.__color.__state),this.__temp.a=1;var u=this.__color.v<.5||this.__color.s>.5?255:0,c=255-u;d.extend(this.__field_knob.style,{marginLeft:100*this.__color.s-7+"px",marginTop:100*(1-this.__color.v)-7+"px",backgroundColor:this.__temp.toHexString(),border:this.__field_knob_border+"rgb("+u+","+u+","+u+")"}),this.__hue_knob.style.marginTop=100*(1-this.__color.h/360)+"px",this.__temp.s=1,this.__temp.v=1,P(this.__saturation_field,"left","#fff",this.__temp.toHexString()),this.__input.value=this.__color.toString(),d.extend(this.__input.style,{backgroundColor:this.__color.toHexString(),color:"rgb("+u+","+u+","+u+")",textShadow:this.__input_textShadow+"rgba("+c+","+c+","+c+",.7)"})}}]),t}(),Ae=["-moz-","-o-","-webkit-","-ms-",""],be={load:function(e,t){var i=t||document,r=i.createElement("link");r.type="text/css",r.rel="stylesheet",r.href=e,i.getElementsByTagName("head")[0].appendChild(r)},inject:function(e,t){var i=t||document,r=document.createElement("style");r.type="text/css",r.innerHTML=e;var u=i.getElementsByTagName("head")[0];try{u.appendChild(r)}catch{}}},Re=function(e,t){var i=e[t];return d.isArray(arguments[2])||d.isObject(arguments[2])?new Ue(e,t,arguments[2]):d.isNumber(i)?d.isNumber(arguments[2])&&d.isNumber(arguments[3])?d.isNumber(arguments[4])?new ue(e,t,arguments[2],arguments[3],arguments[4]):new ue(e,t,arguments[2],arguments[3]):d.isNumber(arguments[4])?new le(e,t,{min:arguments[2],max:arguments[3],step:arguments[4]}):new le(e,t,{min:arguments[2],max:arguments[3]}):d.isString(i)?new Be(e,t):d.isFunction(i)?new Se(e,t,""):d.isBoolean(i)?new se(e,t):null},Ge=window.requestAnimationFrame||window.webkitRequestAnimationFrame||window.mozRequestAnimationFrame||window.oRequestAnimationFrame||window.msRequestAnimationFrame||function(e){setTimeout(e,1e3/60)},ke=function(){function e(){z(this,e),this.backgroundElement=document.createElement("div"),d.extend(this.backgroundElement.style,{backgroundColor:"rgba(0,0,0,0.8)",top:0,left:0,display:"none",zIndex:"1000",opacity:0,WebkitTransition:"opacity 0.2s linear",transition:"opacity 0.2s linear"}),l.makeFullscreen(this.backgroundElement),this.backgroundElement.style.position="fixed",this.domElement=document.createElement("div"),d.extend(this.domElement.style,{position:"fixed",display:"none",zIndex:"1001",opacity:0,WebkitTransition:"-webkit-transform 0.2s ease-out, opacity 0.2s linear",transition:"transform 0.2s ease-out, opacity 0.2s linear"}),document.body.appendChild(this.backgroundElement),document.body.appendChild(this.domElement);var t=this;l.bind(this.backgroundElement,"click",function(){t.hide()})}return H(e,[{key:"show",value:function(){var t=this;this.backgroundElement.style.display="block",this.domElement.style.display="block",this.domElement.style.opacity=0,this.domElement.style.webkitTransform="scale(1.1)",this.layout(),d.defer(function(){t.backgroundElement.style.opacity=1,t.domElement.style.opacity=1,t.domElement.style.webkitTransform="scale(1)"})}},{key:"hide",value:function(){var t=this,i=function r(){t.domElement.style.display="none",t.backgroundElement.style.display="none",l.unbind(t.domElement,"webkitTransitionEnd",r),l.unbind(t.domElement,"transitionend",r),l.unbind(t.domElement,"oTransitionEnd",r)};l.bind(this.domElement,"webkitTransitionEnd",i),l.bind(this.domElement,"transitionend",i),l.bind(this.domElement,"oTransitionEnd",i),this.backgroundElement.style.opacity=0,this.domElement.style.opacity=0,this.domElement.style.webkitTransform="scale(1.1)"}},{key:"layout",value:function(){this.domElement.style.left=window.innerWidth/2-l.getWidth(this.domElement)/2+"px",this.domElement.style.top=window.innerHeight/2-l.getHeight(this.domElement)/2+"px"}}]),e}(),Q=function(e){if(e&&typeof window<"u"){var t=document.createElement("style");return t.setAttribute("type","text/css"),t.innerHTML=e,document.head.appendChild(t),e}}(`.dg ul{list-style:none;margin:0;padding:0;width:100%;clear:both}.dg.ac{position:fixed;top:0;left:0;right:0;height:0;z-index:0}.dg:not(.ac) .main{overflow:hidden}.dg.main{-webkit-transition:opacity .1s linear;-o-transition:opacity .1s linear;-moz-transition:opacity .1s linear;transition:opacity .1s linear}.dg.main.taller-than-window{overflow-y:auto}.dg.main.taller-than-window .close-button{opacity:1;margin-top:-1px;border-top:1px solid #2c2c2c}.dg.main ul.closed .close-button{opacity:1 !important}.dg.main:hover .close-button,.dg.main .close-button.drag{opacity:1}.dg.main .close-button{-webkit-transition:opacity .1s linear;-o-transition:opacity .1s linear;-moz-transition:opacity .1s linear;transition:opacity .1s linear;border:0;line-height:19px;height:20px;cursor:pointer;text-align:center;background-color:#000}.dg.main .close-button.close-top{position:relative}.dg.main .close-button.close-bottom{position:absolute}.dg.main .close-button:hover{background-color:#111}.dg.a{float:right;margin-right:15px;overflow-y:visible}.dg.a.has-save>ul.close-top{margin-top:0}.dg.a.has-save>ul.close-bottom{margin-top:27px}.dg.a.has-save>ul.closed{margin-top:0}.dg.a .save-row{top:0;z-index:1002}.dg.a .save-row.close-top{position:relative}.dg.a .save-row.close-bottom{position:fixed}.dg li{-webkit-transition:height .1s ease-out;-o-transition:height .1s ease-out;-moz-transition:height .1s ease-out;transition:height .1s ease-out;-webkit-transition:overflow .1s linear;-o-transition:overflow .1s linear;-moz-transition:overflow .1s linear;transition:overflow .1s linear}.dg li:not(.folder){cursor:auto;height:27px;line-height:27px;padding:0 4px 0 5px}.dg li.folder{padding:0;border-left:4px solid rgba(0,0,0,0)}.dg li.title{cursor:pointer;margin-left:-4px}.dg .closed li:not(.title),.dg .closed ul li,.dg .closed ul li>*{height:0;overflow:hidden;border:0}.dg .cr{clear:both;padding-left:3px;height:27px;overflow:hidden}.dg .property-name{cursor:default;float:left;clear:left;width:40%;overflow:hidden;text-overflow:ellipsis}.dg .c{float:left;width:60%;position:relative}.dg .c input[type=text]{border:0;margin-top:4px;padding:3px;width:100%;float:right}.dg .has-slider input[type=text]{width:30%;margin-left:0}.dg .slider{float:left;width:66%;margin-left:-5px;margin-right:0;height:19px;margin-top:4px}.dg .slider-fg{height:100%}.dg .c input[type=checkbox]{margin-top:7px}.dg .c select{margin-top:5px}.dg .cr.function,.dg .cr.function .property-name,.dg .cr.function *,.dg .cr.boolean,.dg .cr.boolean *{cursor:pointer}.dg .cr.color{overflow:visible}.dg .selector{display:none;position:absolute;margin-left:-9px;margin-top:23px;z-index:10}.dg .c:hover .selector,.dg .selector.drag{display:block}.dg li.save-row{padding:0}.dg li.save-row .button{display:inline-block;padding:0px 6px}.dg.dialogue{background-color:#222;width:460px;padding:15px;font-size:13px;line-height:15px}#dg-new-constructor{padding:10px;color:#222;font-family:Monaco, monospace;font-size:10px;border:0;resize:none;box-shadow:inset 1px 1px 1px #888;word-wrap:break-word;margin:12px 0;display:block;width:440px;overflow-y:scroll;height:100px;position:relative}#dg-local-explain{display:none;font-size:11px;line-height:17px;border-radius:3px;background-color:#333;padding:8px;margin-top:10px}#dg-local-explain code{font-size:10px}#dat-gui-save-locally{display:none}.dg{color:#eee;font:11px 'Lucida Grande', sans-serif;text-shadow:0 -1px 0 #111}.dg.main::-webkit-scrollbar{width:5px;background:#1a1a1a}.dg.main::-webkit-scrollbar-corner{height:0;display:none}.dg.main::-webkit-scrollbar-thumb{border-radius:5px;background:#676767}.dg li:not(.folder){background:#1a1a1a;border-bottom:1px solid #2c2c2c}.dg li.save-row{line-height:25px;background:#dad5cb;border:0}.dg li.save-row select{margin-left:5px;width:108px}.dg li.save-row .button{margin-left:5px;margin-top:1px;border-radius:2px;font-size:9px;line-height:7px;padding:4px 4px 5px 4px;background:#c5bdad;color:#fff;text-shadow:0 1px 0 #b0a58f;box-shadow:0 -1px 0 #b0a58f;cursor:pointer}.dg li.save-row .button.gears{background:#c5bdad url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAsAAAANCAYAAAB/9ZQ7AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAQJJREFUeNpiYKAU/P//PwGIC/ApCABiBSAW+I8AClAcgKxQ4T9hoMAEUrxx2QSGN6+egDX+/vWT4e7N82AMYoPAx/evwWoYoSYbACX2s7KxCxzcsezDh3evFoDEBYTEEqycggWAzA9AuUSQQgeYPa9fPv6/YWm/Acx5IPb7ty/fw+QZblw67vDs8R0YHyQhgObx+yAJkBqmG5dPPDh1aPOGR/eugW0G4vlIoTIfyFcA+QekhhHJhPdQxbiAIguMBTQZrPD7108M6roWYDFQiIAAv6Aow/1bFwXgis+f2LUAynwoIaNcz8XNx3Dl7MEJUDGQpx9gtQ8YCueB+D26OECAAQDadt7e46D42QAAAABJRU5ErkJggg==) 2px 1px no-repeat;height:7px;width:8px}.dg li.save-row .button:hover{background-color:#bab19e;box-shadow:0 -1px 0 #b0a58f}.dg li.folder{border-bottom:0}.dg li.title{padding-left:16px;background:#000 url(data:image/gif;base64,R0lGODlhBQAFAJEAAP////Pz8////////yH5BAEAAAIALAAAAAAFAAUAAAIIlI+hKgFxoCgAOw==) 6px 10px no-repeat;cursor:pointer;border-bottom:1px solid rgba(255,255,255,0.2)}.dg .closed li.title{background-image:url(data:image/gif;base64,R0lGODlhBQAFAJEAAP////Pz8////////yH5BAEAAAIALAAAAAAFAAUAAAIIlGIWqMCbWAEAOw==)}.dg .cr.boolean{border-left:3px solid #806787}.dg .cr.color{border-left:3px solid}.dg .cr.function{border-left:3px solid #e61d5f}.dg .cr.number{border-left:3px solid #2FA1D6}.dg .cr.number input[type=text]{color:#2FA1D6}.dg .cr.string{border-left:3px solid #1ed36f}.dg .cr.string input[type=text]{color:#1ed36f}.dg .cr.function:hover,.dg .cr.boolean:hover{background:#111}.dg .c input[type=text]{background:#303030;outline:none}.dg .c input[type=text]:hover{background:#3c3c3c}.dg .c input[type=text]:focus{background:#494949;color:#fff}.dg .c .slider{background:#303030;cursor:ew-resize}.dg .c .slider-fg{background:#2FA1D6;max-width:100%}.dg .c .slider:hover{background:#3c3c3c}.dg .c .slider:hover .slider-fg{background:#44abda}
`);be.inject(Q);var I="Default",oe=function(){try{return!!window.localStorage}catch{return!1}}(),ce=void 0,ne=!0,Y=void 0,de=!1,j=[],C=function e(t){var i=this,r=t||{};this.domElement=document.createElement("div"),this.__ul=document.createElement("ul"),this.domElement.appendChild(this.__ul),l.addClass(this.domElement,"dg"),this.__folders={},this.__controllers=[],this.__rememberedObjects=[],this.__rememberedObjectIndecesToControllers=[],this.__listening=[],r=d.defaults(r,{closeOnTop:!1,autoPlace:!0,width:e.DEFAULT_WIDTH}),r=d.defaults(r,{resizable:r.autoPlace,hideable:r.autoPlace}),d.isUndefined(r.load)?r.load={preset:I}:r.preset&&(r.load.preset=r.preset),d.isUndefined(r.parent)&&r.hideable&&j.push(this),r.resizable=d.isUndefined(r.parent)&&r.resizable,r.autoPlace&&d.isUndefined(r.scrollable)&&(r.scrollable=!0);var u=oe&&localStorage.getItem(te(this,"isLocal"))==="true",c=void 0,h=void 0;if(Object.defineProperties(this,{parent:{get:function(){return r.parent}},scrollable:{get:function(){return r.scrollable}},autoPlace:{get:function(){return r.autoPlace}},closeOnTop:{get:function(){return r.closeOnTop}},preset:{get:function(){return i.parent?i.getRoot().preset:r.load.preset},set:function(v){i.parent?i.getRoot().preset=v:r.load.preset=v,$e(this),i.revert()}},width:{get:function(){return r.width},set:function(v){r.width=v,Ne(i,v)}},name:{get:function(){return r.name},set:function(v){r.name=v,h&&(h.innerHTML=r.name)}},closed:{get:function(){return r.closed},set:function(v){r.closed=v,r.closed?l.addClass(i.__ul,e.CLASS_CLOSED):l.removeClass(i.__ul,e.CLASS_CLOSED),this.onResize(),i.__closeButton&&(i.__closeButton.innerHTML=v?e.TEXT_OPEN:e.TEXT_CLOSED)}},load:{get:function(){return r.load}},useLocalStorage:{get:function(){return u},set:function(v){oe&&(u=v,v?l.bind(window,"unload",c):l.unbind(window,"unload",c),localStorage.setItem(te(i,"isLocal"),v))}}}),d.isUndefined(r.parent)){if(r.closed=!1,l.addClass(this.domElement,e.CLASS_MAIN),l.makeSelectable(this.domElement,!1),oe&&u){i.useLocalStorage=!0;var g=localStorage.getItem(te(this,"gui"));g&&(r.load=JSON.parse(g))}this.__closeButton=document.createElement("div"),this.__closeButton.innerHTML=e.TEXT_CLOSED,l.addClass(this.__closeButton,e.CLASS_CLOSE_BUTTON),r.closeOnTop?(l.addClass(this.__closeButton,e.CLASS_CLOSE_TOP),this.domElement.insertBefore(this.__closeButton,this.domElement.childNodes[0])):(l.addClass(this.__closeButton,e.CLASS_CLOSE_BOTTOM),this.domElement.appendChild(this.__closeButton)),l.bind(this.__closeButton,"click",function(){i.closed=!i.closed})}else{r.closed===void 0&&(r.closed=!0);var b=document.createTextNode(r.name);l.addClass(b,"controller-name"),h=X(i,b),l.addClass(this.__ul,e.CLASS_CLOSED),l.addClass(h,"title"),l.bind(h,"click",function(v){return v.preventDefault(),i.closed=!i.closed,!1}),r.closed||(this.closed=!1)}r.autoPlace&&(d.isUndefined(r.parent)&&(ne&&(Y=document.createElement("div"),l.addClass(Y,"dg"),l.addClass(Y,e.CLASS_AUTO_PLACE_CONTAINER),document.body.appendChild(Y),ne=!1),Y.appendChild(this.domElement),l.addClass(this.domElement,e.CLASS_AUTO_PLACE)),this.parent||Ne(i,r.width)),this.__resizeHandler=function(){i.onResizeDebounced()},l.bind(window,"resize",this.__resizeHandler),l.bind(this.__ul,"webkitTransitionEnd",this.__resizeHandler),l.bind(this.__ul,"transitionend",this.__resizeHandler),l.bind(this.__ul,"oTransitionEnd",this.__resizeHandler),this.onResize(),r.resizable&&Ze(this),c=function(){oe&&localStorage.getItem(te(i,"isLocal"))==="true"&&localStorage.setItem(te(i,"gui"),JSON.stringify(i.getSaveObject()))},this.saveToLocalStorageIfPossible=c,r.parent||function(){var v=i.getRoot();v.width+=1,d.defer(function(){v.width-=1})}()};C.toggleHide=function(){de=!de,d.each(j,function(e){e.domElement.style.display=de?"none":""})},C.CLASS_AUTO_PLACE="a",C.CLASS_AUTO_PLACE_CONTAINER="ac",C.CLASS_MAIN="main",C.CLASS_CONTROLLER_ROW="cr",C.CLASS_TOO_TALL="taller-than-window",C.CLASS_CLOSED="closed",C.CLASS_CLOSE_BUTTON="close-button",C.CLASS_CLOSE_TOP="close-top",C.CLASS_CLOSE_BOTTOM="close-bottom",C.CLASS_DRAG="drag",C.DEFAULT_WIDTH=245,C.TEXT_CLOSED="Close Controls",C.TEXT_OPEN="Open Controls",C._keydownHandler=function(e){document.activeElement.type==="text"||e.which!==72&&e.keyCode!==72||C.toggleHide()},l.bind(window,"keydown",C._keydownHandler,!1),d.extend(C.prototype,{add:function(e,t){return ae(this,e,t,{factoryArgs:Array.prototype.slice.call(arguments,2)})},addColor:function(e,t){return ae(this,e,t,{color:!0})},remove:function(e){this.__ul.removeChild(e.__li),this.__controllers.splice(this.__controllers.indexOf(e),1);var t=this;d.defer(function(){t.onResize()})},destroy:function(){if(this.parent)throw new Error("Only the root GUI should be removed with .destroy(). For subfolders, use gui.removeFolder(folder) instead.");this.autoPlace&&Y.removeChild(this.domElement);var e=this;d.each(this.__folders,function(t){e.removeFolder(t)}),l.unbind(window,"keydown",C._keydownHandler,!1),Pe(this)},addFolder:function(e){if(this.__folders[e]!==void 0)throw new Error('You already have a folder in this GUI by the name "'+e+'"');var t={name:e,parent:this};t.autoPlace=this.autoPlace,this.load&&this.load.folders&&this.load.folders[e]&&(t.closed=this.load.folders[e].closed,t.load=this.load.folders[e]);var i=new C(t);this.__folders[e]=i;var r=X(this,i.domElement);return l.addClass(r,"folder"),i},removeFolder:function(e){this.__ul.removeChild(e.domElement.parentElement),delete this.__folders[e.name],this.load&&this.load.folders&&this.load.folders[e.name]&&delete this.load.folders[e.name],Pe(e);var t=this;d.each(e.__folders,function(i){e.removeFolder(i)}),d.defer(function(){t.onResize()})},open:function(){this.closed=!1},close:function(){this.closed=!0},onResize:function(){var e=this.getRoot();if(e.scrollable){var t=l.getOffset(e.__ul).top,i=0;d.each(e.__ul.childNodes,function(r){e.autoPlace&&r===e.__save_row||(i+=l.getHeight(r))}),window.innerHeight-t-20<i?(l.addClass(e.domElement,C.CLASS_TOO_TALL),e.__ul.style.height=window.innerHeight-t-20+"px"):(l.removeClass(e.domElement,C.CLASS_TOO_TALL),e.__ul.style.height="auto")}e.__resize_handle&&d.defer(function(){e.__resize_handle.style.height=e.__ul.offsetHeight+"px"}),e.__closeButton&&(e.__closeButton.style.width=e.width+"px")},onResizeDebounced:d.debounce(function(){this.onResize()},50),remember:function(){if(d.isUndefined(ce)&&((ce=new ke).domElement.innerHTML=`<div id="dg-save" class="dg dialogue">

  Here's the new load parameter for your <code>GUI</code>'s constructor:

  <textarea id="dg-new-constructor"></textarea>

  <div id="dg-save-locally">

    <input id="dg-local-storage" type="checkbox"/> Automatically save
    values to <code>localStorage</code> on exit.

    <div id="dg-local-explain">The values saved to <code>localStorage</code> will
      override those passed to <code>dat.GUI</code>'s constructor. This makes it
      easier to work incrementally, but <code>localStorage</code> is fragile,
      and your friends may not see the same values you do.

    </div>

  </div>

</div>`),this.parent)throw new Error("You can only call remember on a top level GUI.");var e=this;d.each(Array.prototype.slice.call(arguments),function(t){e.__rememberedObjects.length===0&&k(e),e.__rememberedObjects.indexOf(t)===-1&&e.__rememberedObjects.push(t)}),this.autoPlace&&Ne(this,this.width)},getRoot:function(){for(var e=this;e.parent;)e=e.parent;return e},getSaveObject:function(){var e=this.load;return e.closed=this.closed,this.__rememberedObjects.length>0&&(e.preset=this.preset,e.remembered||(e.remembered={}),e.remembered[this.preset]=ye(this)),e.folders={},d.each(this.__folders,function(t,i){e.folders[i]=t.getSaveObject()}),e},save:function(){this.load.remembered||(this.load.remembered={}),this.load.remembered[this.preset]=ye(this),Le(this,!1),this.saveToLocalStorageIfPossible()},saveAs:function(e){this.load.remembered||(this.load.remembered={},this.load.remembered[I]=ye(this,!0)),this.load.remembered[e]=ye(this),this.preset=e,F(this,e,!0),this.saveToLocalStorageIfPossible()},revert:function(e){d.each(this.__controllers,function(t){this.getRoot().load.remembered?B(e||this.getRoot(),t):t.setValue(t.initialValue),t.__onFinishChange&&t.__onFinishChange.call(t,t.getValue())},this),d.each(this.__folders,function(t){t.revert(t)}),e||Le(this.getRoot(),!1)},listen:function(e){var t=this.__listening.length===0;this.__listening.push(e),t&&Me(this.__listening)},updateDisplay:function(){d.each(this.__controllers,function(e){e.updateDisplay()}),d.each(this.__folders,function(e){e.updateDisplay()})}});var Xe={Color:y,math:ve,interpret:Te},Ve={Controller:x,BooleanController:se,OptionController:Ue,StringController:Be,NumberController:ie,NumberControllerBox:le,NumberControllerSlider:ue,FunctionController:Se,ColorController:ge},G={dom:l},Ce={GUI:C},Ye=C,je={color:Xe,controllers:Ve,dom:G,gui:Ce,GUI:Ye};M.color=Xe,M.controllers=Ve,M.dom=G,M.gui=Ce,M.GUI=Ye,M.default=je,Object.defineProperty(M,"__esModule",{value:!0})});function Oe(M,_){const D=M;g(),_={IMMEDIATE:!0,TRIGGER:"hover",AUTO:!1,INTERVAL:3e3,SIM_RESOLUTION:128,DYE_RESOLUTION:1024,CAPTURE_RESOLUTION:512,DENSITY_DISSIPATION:1,VELOCITY_DISSIPATION:.2,PRESSURE:.8,PRESSURE_ITERATIONS:20,CURL:30,SPLAT_RADIUS:.25,SPLAT_FORCE:6e3,SPLAT_COUNT:Number.parseInt(Math.random()*20)+5,SHADING:!0,COLORFUL:!0,COLOR_UPDATE_SPEED:10,PAUSED:!1,BACK_COLOR:{r:0,g:0,b:0},TRANSPARENT:!1,BLOOM:!0,BLOOM_ITERATIONS:8,BLOOM_RESOLUTION:256,BLOOM_INTENSITY:.8,BLOOM_THRESHOLD:.6,BLOOM_SOFT_KNEE:.7,SUNRAYS:!0,SUNRAYS_RESOLUTION:196,SUNRAYS_WEIGHT:1,..._};function he(){this.id=-1,this.texcoordX=0,this.texcoordY=0,this.prevTexcoordX=0,this.prevTexcoordY=0,this.deltaX=0,this.deltaY=0,this.down=!1,this.moved=!1,this.color=[30,0,300]}const U=[],me=[],ee=[];U.push(new he);const{gl:n,ext:P}=Qe(D);Le()&&(_.DYE_RESOLUTION=512),P.supportLinearFiltering||(_.DYE_RESOLUTION=512,_.SHADING=!1,_.BLOOM=!1,_.SUNRAYS=!1);function Qe(o){const s={alpha:!0,depth:!1,stencil:!1,antialias:!1,preserveDrawingBuffer:!1};let a=o.getContext("webgl2",s);const f=!!a;f||(a=o.getContext("webgl",s)||o.getContext("experimental-webgl",s));let p,w;f?(a.getExtension("EXT_color_buffer_float"),w=a.getExtension("OES_texture_float_linear")):(p=a.getExtension("OES_texture_half_float"),w=a.getExtension("OES_texture_half_float_linear")),a.clearColor(0,0,0,1);const E=f?a.HALF_FLOAT:p.HALF_FLOAT_OES;let L,O,re;return f?(L=X(a,a.RGBA16F,a.RGBA,E),O=X(a,a.RG16F,a.RG,E),re=X(a,a.R16F,a.RED,E)):(L=X(a,a.RGBA,a.RGBA,E),O=X(a,a.RGBA,a.RGBA,E),re=X(a,a.RGBA,a.RGBA,E)),{gl:a,ext:{formatRGBA:L,formatRG:O,formatR:re,halfFloatTexType:E,supportLinearFiltering:w}}}function X(o,s,a,f){if(!Pe(o,s,a,f))switch(s){case o.R16F:return X(o,o.RG16F,o.RG,f);case o.RG16F:return X(o,o.RGBA16F,o.RGBA,f);default:return null}return{internalFormat:s,format:a}}function Pe(o,s,a,f){const p=o.createTexture();o.bindTexture(o.TEXTURE_2D,p),o.texParameteri(o.TEXTURE_2D,o.TEXTURE_MIN_FILTER,o.NEAREST),o.texParameteri(o.TEXTURE_2D,o.TEXTURE_MAG_FILTER,o.NEAREST),o.texParameteri(o.TEXTURE_2D,o.TEXTURE_WRAP_S,o.CLAMP_TO_EDGE),o.texParameteri(o.TEXTURE_2D,o.TEXTURE_WRAP_T,o.CLAMP_TO_EDGE),o.texImage2D(o.TEXTURE_2D,0,s,4,4,0,a,f,null);const w=o.createFramebuffer();return o.bindFramebuffer(o.FRAMEBUFFER,w),o.framebufferTexture2D(o.FRAMEBUFFER,o.COLOR_ATTACHMENT0,o.TEXTURE_2D,p,0),o.checkFramebufferStatus(o.FRAMEBUFFER)===o.FRAMEBUFFER_COMPLETE}function Le(){return/Mobi|Android/i.test(navigator.userAgent)}class qe{constructor(s,a){this.vertexShader=s,this.fragmentShaderSource=a,this.programs=[],this.activeProgram=null,this.uniforms=[]}setKeywords(s){let a=0;for(let p=0;p<s.length;p++)a+=ft(s[p]);let f=this.programs[a];if(!f){const p=F(n.FRAGMENT_SHADER,this.fragmentShaderSource,s);f=ae(this.vertexShader,p),this.programs[a]=f}f!==this.activeProgram&&(this.uniforms=te(f),this.activeProgram=f)}bind(){n.useProgram(this.activeProgram)}}class B{constructor(s,a){this.uniforms={},this.program=ae(s,a),this.uniforms=te(this.program)}bind(){n.useProgram(this.program)}}function ae(o,s){const a=n.createProgram();if(n.attachShader(a,o),n.attachShader(a,s),n.linkProgram(a),!n.getProgramParameter(a,n.LINK_STATUS))throw n.getProgramInfoLog(a);return a}function te(o){const s=[],a=n.getProgramParameter(o,n.ACTIVE_UNIFORMS);for(let f=0;f<a;f++){const p=n.getActiveUniform(o,f).name;s[p]=n.getUniformLocation(o,p)}return s}function F(o,s,a){s=Ie(s,a);const f=n.createShader(o);if(n.shaderSource(f,s),n.compileShader(f),!n.getShaderParameter(f,n.COMPILE_STATUS))throw n.getShaderInfoLog(f);return f}function Ie(o,s){if(!s)return o;let a="";return s.forEach(f=>{a+=`#define ${f}
`}),a+o}const k=F(n.VERTEX_SHADER,`
    precision highp float;
    attribute vec2 aPosition;
    varying vec2 vUv;
    varying vec2 vL;
    varying vec2 vR;
    varying vec2 vT;
    varying vec2 vB;
    uniform vec2 texelSize;
    void main () {
        vUv = aPosition * 0.5 + 0.5;
        vL = vUv - vec2(texelSize.x, 0.0);
        vR = vUv + vec2(texelSize.x, 0.0);
        vT = vUv + vec2(0.0, texelSize.y);
        vB = vUv - vec2(0.0, texelSize.y);
        gl_Position = vec4(aPosition, 0.0, 1.0);
    }
`),Ze=F(n.VERTEX_SHADER,`
    precision highp float;
    attribute vec2 aPosition;
    varying vec2 vUv;
    varying vec2 vL;
    varying vec2 vR;
    uniform vec2 texelSize;
    void main () {
        vUv = aPosition * 0.5 + 0.5;
        float offset = 1.33333333;
        vL = vUv - texelSize * offset;
        vR = vUv + texelSize * offset;
        gl_Position = vec4(aPosition, 0.0, 1.0);
    }
`),Ne=F(n.FRAGMENT_SHADER,`
    precision mediump float;
    precision mediump sampler2D;
    varying vec2 vUv;
    varying vec2 vL;
    varying vec2 vR;
    uniform sampler2D uTexture;
    void main () {
        vec4 sum = texture2D(uTexture, vUv) * 0.29411764;
        sum += texture2D(uTexture, vL) * 0.35294117;
        sum += texture2D(uTexture, vR) * 0.35294117;
        gl_FragColor = sum;
    }
`),ye=F(n.FRAGMENT_SHADER,`
    precision mediump float;
    precision mediump sampler2D;
    varying highp vec2 vUv;
    uniform sampler2D uTexture;
    void main () {
        gl_FragColor = texture2D(uTexture, vUv);
    }
`),$e=F(n.FRAGMENT_SHADER,`
    precision mediump float;
    precision mediump sampler2D;
    varying highp vec2 vUv;
    uniform sampler2D uTexture;
    uniform float value;
    void main () {
        gl_FragColor = value * texture2D(uTexture, vUv);
    }
`),Me=F(n.FRAGMENT_SHADER,`
    precision mediump float;
    uniform vec4 color;
    void main () {
        gl_FragColor = color;
    }
`),ze=F(n.FRAGMENT_SHADER,_.TRANSPARENT?`
    precision highp float;
    precision highp sampler2D;
    varying vec2 vUv;
    uniform sampler2D uTexture;
    uniform float aspectRatio;
    #define SCALE 25.0
    void main () {
        vec2 uv = floor(vUv * SCALE * vec2(aspectRatio, 1.0));
        float v = mod(uv.x + uv.y, 2.0);
        v = v * 0.1 + 0.8;
        gl_FragColor = vec4(0.0, 0.0, 0.0, 0.0);
    }
`:`
    precision highp float;
    precision highp sampler2D;
    varying vec2 vUv;
    uniform sampler2D uTexture;
    uniform float aspectRatio;
    #define SCALE 25.0
    void main () {
        vec2 uv = floor(vUv * SCALE * vec2(aspectRatio, 1.0));
        float v = mod(uv.x + uv.y, 2.0);
        v = v * 0.1 + 0.8;
        gl_FragColor = vec4(vec3(v), 1.0);
    }
`),_e=`
    precision highp float;
    precision highp sampler2D;
    varying vec2 vUv;
    varying vec2 vL;
    varying vec2 vR;
    varying vec2 vT;
    varying vec2 vB;
    uniform sampler2D uTexture;
    uniform sampler2D uBloom;
    uniform sampler2D uSunrays;
    uniform sampler2D uDithering;
    uniform vec2 ditherScale;
    uniform vec2 texelSize;
    vec3 linearToGamma (vec3 color) {
        color = max(color, vec3(0));
        return max(1.055 * pow(color, vec3(0.416666667)) - 0.055, vec3(0));
    }
    void main () {
        vec3 c = texture2D(uTexture, vUv).rgb;
    #ifdef SHADING
        vec3 lc = texture2D(uTexture, vL).rgb;
        vec3 rc = texture2D(uTexture, vR).rgb;
        vec3 tc = texture2D(uTexture, vT).rgb;
        vec3 bc = texture2D(uTexture, vB).rgb;
        float dx = length(rc) - length(lc);
        float dy = length(tc) - length(bc);
        vec3 n = normalize(vec3(dx, dy, length(texelSize)));
        vec3 l = vec3(0.0, 0.0, 1.0);
        float diffuse = clamp(dot(n, l) + 0.7, 0.7, 1.0);
        c *= diffuse;
    #endif
    #ifdef BLOOM
        vec3 bloom = texture2D(uBloom, vUv).rgb;
    #endif
    #ifdef SUNRAYS
        float sunrays = texture2D(uSunrays, vUv).r;
        c *= sunrays;
    #ifdef BLOOM
        bloom *= sunrays;
    #endif
    #endif
    #ifdef BLOOM
        float noise = texture2D(uDithering, vUv * ditherScale).r;
        noise = noise * 2.0 - 1.0;
        bloom += noise / 255.0;
        bloom = linearToGamma(bloom);
        c += bloom;
    #endif
        float a = max(c.r, max(c.g, c.b));
        gl_FragColor = vec4(c, a);
    }
`,d=F(n.FRAGMENT_SHADER,`
    precision mediump float;
    precision mediump sampler2D;
    varying vec2 vUv;
    uniform sampler2D uTexture;
    uniform vec3 curve;
    uniform float threshold;
    void main () {
        vec3 c = texture2D(uTexture, vUv).rgb;
        float br = max(c.r, max(c.g, c.b));
        float rq = clamp(br - curve.x, 0.0, curve.y);
        rq = curve.z * rq * rq;
        c *= max(rq, br - threshold) / max(br, 0.0001);
        gl_FragColor = vec4(c, 0.0);
    }
`),et=F(n.FRAGMENT_SHADER,`
    precision mediump float;
    precision mediump sampler2D;
    varying vec2 vL;
    varying vec2 vR;
    varying vec2 vT;
    varying vec2 vB;
    uniform sampler2D uTexture;
    void main () {
        vec4 sum = vec4(0.0);
        sum += texture2D(uTexture, vL);
        sum += texture2D(uTexture, vR);
        sum += texture2D(uTexture, vT);
        sum += texture2D(uTexture, vB);
        sum *= 0.25;
        gl_FragColor = sum;
    }
`),pe=F(n.FRAGMENT_SHADER,`
    precision mediump float;
    precision mediump sampler2D;
    varying vec2 vL;
    varying vec2 vR;
    varying vec2 vT;
    varying vec2 vB;
    uniform sampler2D uTexture;
    uniform float intensity;
    void main () {
        vec4 sum = vec4(0.0);
        sum += texture2D(uTexture, vL);
        sum += texture2D(uTexture, vR);
        sum += texture2D(uTexture, vT);
        sum += texture2D(uTexture, vB);
        sum *= 0.25;
        gl_FragColor = sum * intensity;
    }
`),Ee=F(n.FRAGMENT_SHADER,`
    precision highp float;
    precision highp sampler2D;
    varying vec2 vUv;
    uniform sampler2D uTexture;
    void main () {
        vec4 c = texture2D(uTexture, vUv);
        float br = max(c.r, max(c.g, c.b));
        c.a = 1.0 - min(max(br * 20.0, 0.0), 0.8);
        gl_FragColor = c;
    }
`),Te=F(n.FRAGMENT_SHADER,`
    precision highp float;
    precision highp sampler2D;
    varying vec2 vUv;
    uniform sampler2D uTexture;
    uniform float weight;
    #define ITERATIONS 16
    void main () {
        float Density = 0.3;
        float Decay = 0.95;
        float Exposure = 0.7;
        vec2 coord = vUv;
        vec2 dir = vUv - 0.5;
        dir *= 1.0 / float(ITERATIONS) * Density;
        float illuminationDecay = 1.0;
        float color = texture2D(uTexture, vUv).a;
        for (int i = 0; i < ITERATIONS; i++)
        {
            coord -= dir;
            float col = texture2D(uTexture, coord).a;
            color += col * illuminationDecay * weight;
            illuminationDecay *= Decay;
        }
        gl_FragColor = vec4(color * Exposure, 0.0, 0.0, 1.0);
    }
`),He=F(n.FRAGMENT_SHADER,`
    precision highp float;
    precision highp sampler2D;
    varying vec2 vUv;
    uniform sampler2D uTarget;
    uniform float aspectRatio;
    uniform vec3 color;
    uniform vec2 point;
    uniform float radius;
    void main () {
        vec2 p = vUv - point.xy;
        p.x *= aspectRatio;
        vec3 splat = exp(-dot(p, p) / radius) * color;
        vec3 base = texture2D(uTarget, vUv).xyz;
        gl_FragColor = vec4(base + splat, 1.0);
    }
`),ve=F(n.FRAGMENT_SHADER,`
    precision highp float;
    precision highp sampler2D;
    varying vec2 vUv;
    uniform sampler2D uVelocity;
    uniform sampler2D uSource;
    uniform vec2 texelSize;
    uniform vec2 dyeTexelSize;
    uniform float dt;
    uniform float dissipation;
    vec4 bilerp (sampler2D sam, vec2 uv, vec2 tsize) {
        vec2 st = uv / tsize - 0.5;
        vec2 iuv = floor(st);
        vec2 fuv = fract(st);
        vec4 a = texture2D(sam, (iuv + vec2(0.5, 0.5)) * tsize);
        vec4 b = texture2D(sam, (iuv + vec2(1.5, 0.5)) * tsize);
        vec4 c = texture2D(sam, (iuv + vec2(0.5, 1.5)) * tsize);
        vec4 d = texture2D(sam, (iuv + vec2(1.5, 1.5)) * tsize);
        return mix(mix(a, b, fuv.x), mix(c, d, fuv.x), fuv.y);
    }
    void main () {
    #ifdef MANUAL_FILTERING
        vec2 coord = vUv - dt * bilerp(uVelocity, vUv, texelSize).xy * texelSize;
        vec4 result = bilerp(uSource, coord, dyeTexelSize);
    #else
        vec2 coord = vUv - dt * texture2D(uVelocity, vUv).xy * texelSize;
        vec4 result = texture2D(uSource, coord);
    #endif
        float decay = 1.0 + dissipation * dt;
        gl_FragColor = result / decay;
    }`,P.supportLinearFiltering?null:["MANUAL_FILTERING"]),tt=F(n.FRAGMENT_SHADER,`
    precision mediump float;
    precision mediump sampler2D;
    varying highp vec2 vUv;
    varying highp vec2 vL;
    varying highp vec2 vR;
    varying highp vec2 vT;
    varying highp vec2 vB;
    uniform sampler2D uVelocity;
    void main () {
        float L = texture2D(uVelocity, vL).x;
        float R = texture2D(uVelocity, vR).x;
        float T = texture2D(uVelocity, vT).y;
        float B = texture2D(uVelocity, vB).y;
        vec2 C = texture2D(uVelocity, vUv).xy;
        if (vL.x < 0.0) { L = -C.x; }
        if (vR.x > 1.0) { R = -C.x; }
        if (vT.y > 1.0) { T = -C.y; }
        if (vB.y < 0.0) { B = -C.y; }
        float div = 0.5 * (R - L + T - B);
        gl_FragColor = vec4(div, 0.0, 0.0, 1.0);
    }
`),z=F(n.FRAGMENT_SHADER,`
    precision mediump float;
    precision mediump sampler2D;
    varying highp vec2 vUv;
    varying highp vec2 vL;
    varying highp vec2 vR;
    varying highp vec2 vT;
    varying highp vec2 vB;
    uniform sampler2D uVelocity;
    void main () {
        float L = texture2D(uVelocity, vL).y;
        float R = texture2D(uVelocity, vR).y;
        float T = texture2D(uVelocity, vT).x;
        float B = texture2D(uVelocity, vB).x;
        float vorticity = R - L - T + B;
        gl_FragColor = vec4(0.5 * vorticity, 0.0, 0.0, 1.0);
    }
`),H=F(n.FRAGMENT_SHADER,`
    precision highp float;
    precision highp sampler2D;
    varying vec2 vUv;
    varying vec2 vL;
    varying vec2 vR;
    varying vec2 vT;
    varying vec2 vB;
    uniform sampler2D uVelocity;
    uniform sampler2D uCurl;
    uniform float curl;
    uniform float dt;
    void main () {
        float L = texture2D(uCurl, vL).x;
        float R = texture2D(uCurl, vR).x;
        float T = texture2D(uCurl, vT).x;
        float B = texture2D(uCurl, vB).x;
        float C = texture2D(uCurl, vUv).x;
        vec2 force = 0.5 * vec2(abs(T) - abs(B), abs(R) - abs(L));
        force /= length(force) + 0.0001;
        force *= curl * C;
        force.y *= -1.0;
        vec2 vel = texture2D(uVelocity, vUv).xy;
        gl_FragColor = vec4(vel + force * dt, 0.0, 1.0);
    }
`),W=F(n.FRAGMENT_SHADER,`
    precision mediump float;
    precision mediump sampler2D;
    varying highp vec2 vUv;
    varying highp vec2 vL;
    varying highp vec2 vR;
    varying highp vec2 vT;
    varying highp vec2 vB;
    uniform sampler2D uPressure;
    uniform sampler2D uDivergence;
    void main () {
        float L = texture2D(uPressure, vL).x;
        float R = texture2D(uPressure, vR).x;
        float T = texture2D(uPressure, vT).x;
        float B = texture2D(uPressure, vB).x;
        float C = texture2D(uPressure, vUv).x;
        float divergence = texture2D(uDivergence, vUv).x;
        float pressure = (L + R + B + T - divergence) * 0.25;
        gl_FragColor = vec4(pressure, 0.0, 0.0, 1.0);
    }
`),K=F(n.FRAGMENT_SHADER,`
    precision mediump float;
    precision mediump sampler2D;
    varying highp vec2 vUv;
    varying highp vec2 vL;
    varying highp vec2 vR;
    varying highp vec2 vT;
    varying highp vec2 vB;
    uniform sampler2D uPressure;
    uniform sampler2D uVelocity;
    void main () {
        float L = texture2D(uPressure, vL).x;
        float R = texture2D(uPressure, vR).x;
        float T = texture2D(uPressure, vT).x;
        float B = texture2D(uPressure, vB).x;
        vec2 velocity = texture2D(uVelocity, vUv).xy;
        velocity.xy -= vec2(R - L, T - B);
        gl_FragColor = vec4(velocity, 0.0, 1.0);
    }
`),A=(()=>(n.bindBuffer(n.ARRAY_BUFFER,n.createBuffer()),n.bufferData(n.ARRAY_BUFFER,new Float32Array([-1,-1,-1,1,1,1,1,-1]),n.STATIC_DRAW),n.bindBuffer(n.ELEMENT_ARRAY_BUFFER,n.createBuffer()),n.bufferData(n.ELEMENT_ARRAY_BUFFER,new Uint16Array([0,1,2,0,2,3]),n.STATIC_DRAW),n.vertexAttribPointer(0,2,n.FLOAT,!1,0,0),n.enableVertexAttribArray(0),o=>{n.bindFramebuffer(n.FRAMEBUFFER,o),n.drawElements(n.TRIANGLES,6,n.UNSIGNED_SHORT,0)}))();let y,x,Fe,we,J,l,se,Ue;const Be=e(),ie=new B(Ze,Ne),le=new B(k,ye),ue=new B(k,$e),Se=new B(k,Me),ge=new B(k,ze),Ae=new B(k,d),be=new B(k,et),Re=new B(k,pe),Ge=new B(k,Ee),ke=new B(k,Te),Q=new B(k,He),I=new B(k,ve),oe=new B(k,tt),ce=new B(k,z),ne=new B(k,H),Y=new B(k,W),de=new B(k,K),j=new qe(k,_e);function C(){const o=Je(_.SIM_RESOLUTION),s=Je(_.DYE_RESOLUTION),a=P.halfFloatTexType,f=P.formatRGBA,p=P.formatRG,w=P.formatR,E=P.supportLinearFiltering?n.LINEAR:n.NEAREST;y?y=je(y,s.width,s.height,f.internalFormat,f.format,a,E):y=Ce(s.width,s.height,f.internalFormat,f.format,a,E),x?x=je(x,o.width,o.height,p.internalFormat,p.format,a,E):x=Ce(o.width,o.height,p.internalFormat,p.format,a,E),Fe=G(o.width,o.height,w.internalFormat,w.format,a,n.NEAREST),we=G(o.width,o.height,w.internalFormat,w.format,a,n.NEAREST),J=Ce(o.width,o.height,w.internalFormat,w.format,a,n.NEAREST),Xe(),Ve()}function Xe(){const o=Je(_.BLOOM_RESOLUTION),s=P.halfFloatTexType,a=P.formatRGBA,f=P.supportLinearFiltering?n.LINEAR:n.NEAREST;l=G(o.width,o.height,a.internalFormat,a.format,s,f),ee.length=0;for(let p=0;p<_.BLOOM_ITERATIONS;p++){const w=o.width>>p+1,E=o.height>>p+1;if(w<2||E<2)break;const L=G(w,E,a.internalFormat,a.format,s,f);ee.push(L)}}function Ve(){const o=Je(_.SUNRAYS_RESOLUTION),s=P.halfFloatTexType,a=P.formatR,f=P.supportLinearFiltering?n.LINEAR:n.NEAREST;se=G(o.width,o.height,a.internalFormat,a.format,s,f),Ue=G(o.width,o.height,a.internalFormat,a.format,s,f)}function G(o,s,a,f,p,w){n.activeTexture(n.TEXTURE0);const E=n.createTexture();n.bindTexture(n.TEXTURE_2D,E),n.texParameteri(n.TEXTURE_2D,n.TEXTURE_MIN_FILTER,w),n.texParameteri(n.TEXTURE_2D,n.TEXTURE_MAG_FILTER,w),n.texParameteri(n.TEXTURE_2D,n.TEXTURE_WRAP_S,n.CLAMP_TO_EDGE),n.texParameteri(n.TEXTURE_2D,n.TEXTURE_WRAP_T,n.CLAMP_TO_EDGE),n.texImage2D(n.TEXTURE_2D,0,a,o,s,0,f,p,null);const L=n.createFramebuffer();n.bindFramebuffer(n.FRAMEBUFFER,L),n.framebufferTexture2D(n.FRAMEBUFFER,n.COLOR_ATTACHMENT0,n.TEXTURE_2D,E,0),n.viewport(0,0,o,s),n.clear(n.COLOR_BUFFER_BIT);const O=1/o,re=1/s;return{texture:E,fbo:L,width:o,height:s,texelSizeX:O,texelSizeY:re,attach(De){return n.activeTexture(n.TEXTURE0+De),n.bindTexture(n.TEXTURE_2D,E),De}}}function Ce(o,s,a,f,p,w){let E=G(o,s,a,f,p,w),L=G(o,s,a,f,p,w);return{width:o,height:s,texelSizeX:E.texelSizeX,texelSizeY:E.texelSizeY,get read(){return E},set read(O){E=O},get write(){return L},set write(O){L=O},swap(){const O=E;E=L,L=O}}}function Ye(o,s,a,f,p,w,E){const L=G(s,a,f,p,w,E);return le.bind(),n.uniform1i(le.uniforms.uTexture,o.attach(0)),A(L.fbo),L}function je(o,s,a,f,p,w,E){return o.width===s&&o.height===a||(o.read=Ye(o.read,s,a,f,p,w,E),o.write=G(s,a,f,p,w,E),o.width=s,o.height=a,o.texelSizeX=1/s,o.texelSizeY=1/a),o}function e(o){const s=n.createTexture();n.bindTexture(n.TEXTURE_2D,s),n.texParameteri(n.TEXTURE_2D,n.TEXTURE_MIN_FILTER,n.LINEAR),n.texParameteri(n.TEXTURE_2D,n.TEXTURE_MAG_FILTER,n.LINEAR),n.texParameteri(n.TEXTURE_2D,n.TEXTURE_WRAP_S,n.REPEAT),n.texParameteri(n.TEXTURE_2D,n.TEXTURE_WRAP_T,n.REPEAT),n.texImage2D(n.TEXTURE_2D,0,n.RGB,1,1,0,n.RGB,n.UNSIGNED_BYTE,new Uint8Array([255,255,255]));const a={texture:s,width:1,height:1,attach(p){return n.activeTexture(n.TEXTURE0+p),n.bindTexture(n.TEXTURE_2D,s),p}},f=new Image;return f.onload=()=>{a.width=f.width,a.height=f.height,n.bindTexture(n.TEXTURE_2D,s),n.texImage2D(n.TEXTURE_2D,0,n.RGB,n.RGB,n.UNSIGNED_BYTE,f)},o&&(f.src=o),a}function t(){const o=[];_.SHADING&&o.push("SHADING"),_.BLOOM&&o.push("BLOOM"),_.SUNRAYS&&o.push("SUNRAYS"),j.setKeywords(o)}t(),C(),_.IMMEDIATE&&Ke(_.SPLAT_COUNT);function i(){_.AUTO&&_.INTERVAL&&!_.PAUSED&&me.push(_.SPLAT_COUNT),setTimeout(i,_.INTERVAL)}setTimeout(i,_.INTERVAL);let r=Date.now(),u=0;c();function c(){const o=h();g()&&C(),b(o),v(),_.PAUSED||S(o),T(null),requestAnimationFrame(c)}function h(){const o=Date.now();let s=(o-r)/1e3;return s=Math.min(s,.016666),r=o,s}function g(){const o=$(D.clientWidth),s=$(D.clientHeight);return D.width!==o||D.height!==s?(D.width=o,D.height=s,!0):!1}function b(o){_.COLORFUL&&(u+=o*_.COLOR_UPDATE_SPEED,u>=1&&(u=ct(u,0,1),U.forEach(s=>{s.color=it()})))}function v(){me.length>0&&Ke(me.pop()),U.forEach(o=>{if(o.moved){if(o.moved=!1,o.deltaX===0&&o.deltaY===0)for(let s=0;s<4;s++)We(o);We(o)}})}function S(o){n.disable(n.BLEND),n.viewport(0,0,x.width,x.height),ce.bind(),n.uniform2f(ce.uniforms.texelSize,x.texelSizeX,x.texelSizeY),n.uniform1i(ce.uniforms.uVelocity,x.read.attach(0)),A(we.fbo),ne.bind(),n.uniform2f(ne.uniforms.texelSize,x.texelSizeX,x.texelSizeY),n.uniform1i(ne.uniforms.uVelocity,x.read.attach(0)),n.uniform1i(ne.uniforms.uCurl,we.attach(1)),n.uniform1f(ne.uniforms.curl,_.CURL),n.uniform1f(ne.uniforms.dt,o),A(x.write.fbo),x.swap(),oe.bind(),n.uniform2f(oe.uniforms.texelSize,x.texelSizeX,x.texelSizeY),n.uniform1i(oe.uniforms.uVelocity,x.read.attach(0)),A(Fe.fbo),ue.bind(),n.uniform1i(ue.uniforms.uTexture,J.read.attach(0)),n.uniform1f(ue.uniforms.value,_.PRESSURE),A(J.write.fbo),J.swap(),Y.bind(),n.uniform2f(Y.uniforms.texelSize,x.texelSizeX,x.texelSizeY),n.uniform1i(Y.uniforms.uDivergence,Fe.attach(0));for(let a=0;a<_.PRESSURE_ITERATIONS;a++)n.uniform1i(Y.uniforms.uPressure,J.read.attach(1)),A(J.write.fbo),J.swap();de.bind(),n.uniform2f(de.uniforms.texelSize,x.texelSizeX,x.texelSizeY),n.uniform1i(de.uniforms.uPressure,J.read.attach(0)),n.uniform1i(de.uniforms.uVelocity,x.read.attach(1)),A(x.write.fbo),x.swap(),I.bind(),n.uniform2f(I.uniforms.texelSize,x.texelSizeX,x.texelSizeY),P.supportLinearFiltering||n.uniform2f(I.uniforms.dyeTexelSize,x.texelSizeX,x.texelSizeY);const s=x.read.attach(0);n.uniform1i(I.uniforms.uVelocity,s),n.uniform1i(I.uniforms.uSource,s),n.uniform1f(I.uniforms.dt,o),n.uniform1f(I.uniforms.dissipation,_.VELOCITY_DISSIPATION),A(x.write.fbo),x.swap(),n.viewport(0,0,y.width,y.height),P.supportLinearFiltering||n.uniform2f(I.uniforms.dyeTexelSize,y.texelSizeX,y.texelSizeY),n.uniform1i(I.uniforms.uVelocity,x.read.attach(0)),n.uniform1i(I.uniforms.uSource,y.read.attach(1)),n.uniform1f(I.uniforms.dissipation,_.DENSITY_DISSIPATION),A(y.write.fbo),y.swap()}function T(o){_.BLOOM&&N(y.read,l),_.SUNRAYS&&(V(y.read,y.write,se),Z(se,Ue,1)),!o||!_.TRANSPARENT?(n.blendFunc(n.ONE,n.ONE_MINUS_SRC_ALPHA),n.enable(n.BLEND)):n.disable(n.BLEND);const s=o?o.width:n.drawingBufferWidth,a=o?o.height:n.drawingBufferHeight;n.viewport(0,0,s,a);const f=o?o.fbo:null;_.TRANSPARENT||m(f,ut(_.BACK_COLOR)),!o&&_.TRANSPARENT&&R(f),q(f,s,a)}function m(o,s){Se.bind(),n.uniform4f(Se.uniforms.color,s.r,s.g,s.b,1),A(o)}function R(o){ge.bind(),n.uniform1f(ge.uniforms.aspectRatio,D.width/D.height),A(o)}function q(o,s,a){if(j.bind(),_.SHADING&&n.uniform2f(j.uniforms.texelSize,1/s,1/a),n.uniform1i(j.uniforms.uTexture,y.read.attach(0)),_.BLOOM){n.uniform1i(j.uniforms.uBloom,l.attach(1)),n.uniform1i(j.uniforms.uDithering,Be.attach(2));const f=dt(Be,s,a);n.uniform2f(j.uniforms.ditherScale,f.x,f.y)}_.SUNRAYS&&n.uniform1i(j.uniforms.uSunrays,se.attach(3)),A(o)}function N(o,s){if(ee.length<2)return;let a=s;n.disable(n.BLEND),Ae.bind();const f=_.BLOOM_THRESHOLD*_.BLOOM_SOFT_KNEE+1e-4,p=_.BLOOM_THRESHOLD-f,w=f*2,E=.25/f;n.uniform3f(Ae.uniforms.curve,p,w,E),n.uniform1f(Ae.uniforms.threshold,_.BLOOM_THRESHOLD),n.uniform1i(Ae.uniforms.uTexture,o.attach(0)),n.viewport(0,0,a.width,a.height),A(a.fbo),be.bind();for(let L=0;L<ee.length;L++){const O=ee[L];n.uniform2f(be.uniforms.texelSize,a.texelSizeX,a.texelSizeY),n.uniform1i(be.uniforms.uTexture,a.attach(0)),n.viewport(0,0,O.width,O.height),A(O.fbo),a=O}n.blendFunc(n.ONE,n.ONE),n.enable(n.BLEND);for(let L=ee.length-2;L>=0;L--){const O=ee[L];n.uniform2f(be.uniforms.texelSize,a.texelSizeX,a.texelSizeY),n.uniform1i(be.uniforms.uTexture,a.attach(0)),n.viewport(0,0,O.width,O.height),A(O.fbo),a=O}n.disable(n.BLEND),Re.bind(),n.uniform2f(Re.uniforms.texelSize,a.texelSizeX,a.texelSizeY),n.uniform1i(Re.uniforms.uTexture,a.attach(0)),n.uniform1f(Re.uniforms.intensity,_.BLOOM_INTENSITY),n.viewport(0,0,s.width,s.height),A(s.fbo)}function V(o,s,a){n.disable(n.BLEND),Ge.bind(),n.uniform1i(Ge.uniforms.uTexture,o.attach(0)),n.viewport(0,0,s.width,s.height),A(s.fbo),ke.bind(),n.uniform1f(ke.uniforms.weight,_.SUNRAYS_WEIGHT),n.uniform1i(ke.uniforms.uTexture,s.attach(0)),n.viewport(0,0,a.width,a.height),A(a.fbo)}function Z(o,s,a){ie.bind();for(let f=0;f<a;f++)n.uniform2f(ie.uniforms.texelSize,o.texelSizeX,0),n.uniform1i(ie.uniforms.uTexture,o.attach(0)),A(s.fbo),n.uniform2f(ie.uniforms.texelSize,0,o.texelSizeY),n.uniform1i(ie.uniforms.uTexture,s.attach(0)),A(o.fbo)}function We(o){const s=o.deltaX*_.SPLAT_FORCE,a=o.deltaY*_.SPLAT_FORCE;fe(o.texcoordX,o.texcoordY,s,a,o.color)}function Ke(o){for(let s=0;s<o;s++){const a=it();a.r*=10,a.g*=10,a.b*=10;const f=Math.random(),p=Math.random(),w=1e3*(Math.random()-.5),E=1e3*(Math.random()-.5);fe(f,p,w,E,a)}}function fe(o,s,a,f,p){n.viewport(0,0,x.width,x.height),Q.bind(),n.uniform1i(Q.uniforms.uTarget,x.read.attach(0)),n.uniform1f(Q.uniforms.aspectRatio,D.width/D.height),n.uniform2f(Q.uniforms.point,o,s),n.uniform3f(Q.uniforms.color,a,f,0),n.uniform1f(Q.uniforms.radius,xe(_.SPLAT_RADIUS/100)),A(x.write.fbo),x.swap(),n.viewport(0,0,y.width,y.height),n.uniform1i(Q.uniforms.uTarget,y.read.attach(0)),n.uniform3f(Q.uniforms.color,p.r,p.g,p.b),A(y.write.fbo),y.swap()}function xe(o){const s=D.width/D.height;return s>1&&(o*=s),o}D.addEventListener("mousedown",o=>{const s=$(o.offsetX),a=$(o.offsetY);let f=U.find(p=>p.id===-1);f||(f=new he),ot(f,-1,s,a)}),setTimeout(()=>{D.addEventListener("mousemove",o=>{const s=$(o.offsetX),a=$(o.offsetY);nt(U[0],s,a)})},500),window.addEventListener("mouseup",()=>{rt(U[0])}),D.addEventListener("touchstart",o=>{o.preventDefault();const s=o.targetTouches;for(;s.length>=U.length;)U.push(new he);for(let a=0;a<s.length;a++){const f=$(s[a].pageX),p=$(s[a].pageY);ot(U[a+1],s[a].identifier,f,p)}}),D.addEventListener("touchmove",o=>{o.preventDefault();const s=o.targetTouches;for(let a=0;a<s.length;a++){const f=$(s[a].pageX),p=$(s[a].pageY);nt(U[a+1],f,p)}},!1),window.addEventListener("touchend",o=>{const s=o.changedTouches;for(let a=0;a<s.length;a++){const f=U.find(p=>p.id===s[a].identifier);rt(f)}}),window.addEventListener("keydown",o=>{o.code==="KeyP"&&(_.PAUSED=!_.PAUSED),o.key===" "&&me.push(Number.parseInt(Math.random()*20)+5)});function ot(o,s,a,f){o.id=s,o.down=!0,o.moved=!1,o.texcoordX=a/D.width,o.texcoordY=1-f/D.height,o.prevTexcoordX=o.texcoordX,o.prevTexcoordY=o.texcoordY,o.deltaX=0,o.deltaY=0,o.color=it()}function nt(o,s,a){_.TRIGGER==="click"?o.moved=o.down:_.TRIGGER==="hover"&&(o.moved=!0),o.prevTexcoordX=o.texcoordX,o.prevTexcoordY=o.texcoordY,o.texcoordX=s/D.width,o.texcoordY=1-a/D.height,o.deltaX=at(o.texcoordX-o.prevTexcoordX),o.deltaY=st(o.texcoordY-o.prevTexcoordY)}function rt(o){o.down=!1}function at(o){const s=D.width/D.height;return s<1&&(o*=s),o}function st(o){const s=D.width/D.height;return s>1&&(o/=s),o}function it(){const o=lt(Math.random(),1,1);return o.r*=.15,o.g*=.15,o.b*=.15,o}function lt(o,s,a){let f,p,w;const E=Math.floor(o*6),L=o*6-E,O=a*(1-s),re=a*(1-L*s),De=a*(1-(1-L)*s);switch(E%6){case 0:f=a,p=De,w=O;break;case 1:f=re,p=a,w=O;break;case 2:f=O,p=a,w=De;break;case 3:f=O,p=re,w=a;break;case 4:f=De,p=O,w=a;break;case 5:f=a,p=O,w=re;break}return{r:f,g:p,b:w}}function ut(o){return{r:o.r/255,g:o.g/255,b:o.b/255}}function ct(o,s,a){const f=a-s;return f===0?s:(o-s)%f+s}function Je(o){let s=n.drawingBufferWidth/n.drawingBufferHeight;s<1&&(s=1/s);const a=Math.round(o),f=Math.round(o*s);return n.drawingBufferWidth>n.drawingBufferHeight?{width:f,height:a}:{width:a,height:f}}function dt(o,s,a){return{x:s/o.width,y:a/o.height}}function $(o){const s=window.devicePixelRatio||1;return Math.floor(o*s)}function ft(o){if(o.length===0)return 0;let s=0;for(let a=0;a<o.length;a++)s=(s<<5)-s+o.charCodeAt(a),s|=0;return s}}return Oe});
//# sourceMappingURL=webgl-fluid.umd.js.map
