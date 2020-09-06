(this.webpackJsonpwebapp=this.webpackJsonpwebapp||[]).push([[0],{114:function(e,t,n){},115:function(e,t,n){"use strict";n.r(t);var a=n(0),r=n.n(a),A=n(11),c=n.n(A),u=(n(91),n(55)),i=n(56),l=n(78),o=n(77),s=n(153),p=n(116),m=n(146),f=n(150),E=n(151),d=n(152),g=n(61),b=n.n(g),v=function(){return r.a.createElement(m.a,{position:"static",elevation:1},r.a.createElement(f.a,null,r.a.createElement(E.a,{edge:"start",color:"inherit","aria-label":"menu"},r.a.createElement(b.a,null)),r.a.createElement(d.a,{variant:"h6"},"OpenCast")))},h=n(19),C=n(159),w=n(154),x=n(117),y=n(7),B=n.n(y),k=n(16),j=n(62),O=n.n(j),Q=document.location.origin.replace("8081","2020")+"/api",M=O.a.create({baseURL:Q});function I(){return(I=Object(k.a)(B.a.mark((function e(){return B.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,M.get("/player/");case 2:return e.abrupt("return",e.sent);case 3:case"end":return e.stop()}}),e)})))).apply(this,arguments)}function D(){return(D=Object(k.a)(B.a.mark((function e(t){return B.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,M.post("/player/stream",null,{params:{url:t}});case 2:return e.abrupt("return",e.sent);case 3:case"end":return e.stop()}}),e)})))).apply(this,arguments)}function S(){return(S=Object(k.a)(B.a.mark((function e(t){return B.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,M.post("/player/queue",null,{params:{url:t}});case 2:return e.abrupt("return",e.sent);case 3:case"end":return e.stop()}}),e)})))).apply(this,arguments)}function N(){return(N=Object(k.a)(B.a.mark((function e(t){return B.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,M.post("/player/play",null,{params:{id:t}});case 2:return e.abrupt("return",e.sent);case 3:case"end":return e.stop()}}),e)})))).apply(this,arguments)}function q(){return(q=Object(k.a)(B.a.mark((function e(){return B.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,M.post("/player/stop");case 2:return e.abrupt("return",e.sent);case 3:case"end":return e.stop()}}),e)})))).apply(this,arguments)}function K(){return(K=Object(k.a)(B.a.mark((function e(){return B.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,M.post("/player/pause");case 2:return e.abrupt("return",e.sent);case 3:case"end":return e.stop()}}),e)})))).apply(this,arguments)}function H(){return(H=Object(k.a)(B.a.mark((function e(t,n){return B.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,M.post("/player/seek",null,{params:{forward:t,long:n}});case 2:return e.abrupt("return",e.sent);case 3:case"end":return e.stop()}}),e)})))).apply(this,arguments)}function R(){return(R=Object(k.a)(B.a.mark((function e(t){return B.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,M.post("/player/volume",null,{params:{value:t}});case 2:return e.abrupt("return",e.sent);case 3:case"end":return e.stop()}}),e)})))).apply(this,arguments)}function U(){return(U=Object(k.a)(B.a.mark((function e(){return B.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,M.post("/player/subtitle/toggle");case 2:return e.abrupt("return",e.sent);case 3:case"end":return e.stop()}}),e)})))).apply(this,arguments)}function F(){return(F=Object(k.a)(B.a.mark((function e(t){return B.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,M.post("/player/subtitle/seek",null,{params:{forward:t}});case 2:return e.abrupt("return",e.sent);case 3:case"end":return e.stop()}}),e)})))).apply(this,arguments)}var P={get:function(){return I.apply(this,arguments)},streamMedia:function(e){return D.apply(this,arguments)},queueMedia:function(e){return S.apply(this,arguments)},playMedia:function(e){return N.apply(this,arguments)},stopMedia:function(){return q.apply(this,arguments)},pauseMedia:function(){return K.apply(this,arguments)},seekMedia:function(e,t){return H.apply(this,arguments)},updateVolume:function(e){return R.apply(this,arguments)},toggleSubtitle:function(){return U.apply(this,arguments)},seekSubtitle:function(e){return F.apply(this,arguments)}};n(54);var X=function(){var e=Object(a.useState)(""),t=Object(h.a)(e,2),n=t[0],A=t[1],c=Object(a.useState)((function(){return P.streamMedia})),u=Object(h.a)(c,2),i=u[0],l=u[1],o=Object(a.useState)("contained"),p=Object(h.a)(o,2),m=p[0],f=p[1],E=Object(a.useState)("outlined"),d=Object(h.a)(E,2),g=d[0],b=d[1],v=function(e){e&&e.preventDefault(),""!==n&&(i(n).catch((function(e){return console.log(e)})),A(""))},y=function(e){!0===e?(f("contained"),b("outlined"),l((function(){return P.streamMedia}))):(f("outlined"),b("contained"),l((function(){return P.queueMedia}))),v(void 0)};return r.a.createElement("form",{onSubmit:function(e){return v(e)},noValidate:!0,autoComplete:"off"},r.a.createElement(s.a,{container:!0,spacing:1},r.a.createElement(s.a,{item:!0,xs:6,sm:7,md:8},r.a.createElement(C.a,{fullWidth:!0,id:"outlined-basic",label:"Media's URL",variant:"standard",value:n,onChange:function(e){return A(e.target.value)}})),r.a.createElement(s.a,{item:!0,xs:6,sm:5,md:4,className:"StreamButtons"},r.a.createElement(w.a,{size:"medium",color:"primary","aria-label":"vertical contained primary button group"},r.a.createElement(x.a,{variant:m,onClick:function(){return y(!0)}},"Cast"),r.a.createElement(x.a,{variant:g,onClick:function(){return y(!1)}},"Queue")))))},G=n(155),L=n(160),V=n(156),J=n(157),Y=n(158),z=n(64),T=n.n(z);function W(){return(W=Object(k.a)(B.a.mark((function e(){return B.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,M.get("/videos/");case 2:return e.abrupt("return",e.sent);case 3:case"end":return e.stop()}}),e)})))).apply(this,arguments)}function Z(){return(Z=Object(k.a)(B.a.mark((function e(t){return B.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,M.get("/videos/"+t);case 2:return e.abrupt("return",e.sent);case 3:case"end":return e.stop()}}),e)})))).apply(this,arguments)}function _(){return(_=Object(k.a)(B.a.mark((function e(t){return B.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,M.delete("/videos/"+t);case 2:return e.abrupt("return",e.sent);case 3:case"end":return e.stop()}}),e)})))).apply(this,arguments)}var $={list:function(){return W.apply(this,arguments)},get:function(e){return Z.apply(this,arguments)},delete_:function(e){return _.apply(this,arguments)}},ee=n(63),te=n.n(ee),ne=Object(G.a)((function(e){return Object(L.a)({root:{display:"flex",flexWrap:"wrap",justifyContent:"center",overflow:"hidden",backgroundColor:e.palette.background.paper},gridList:{flexWrap:"nowrap",transform:"translateZ(0)"},title:{color:e.palette.primary.light},titleBar:{background:"linear-gradient(to top, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.3) 70%, rgba(0,0,0,0) 100%)"}})}));var ae=function(){var e=ne(),t=Object(a.useState)([]),n=Object(h.a)(t,2),A=n[0],c=n[1],u=Object(a.useState)(0),i=Object(h.a)(u,2),l=i[0],o=i[1],s=Object(a.useState)(null),p=Object(h.a)(s,2),m=(p[0],p[1]),f=function(){$.list().then((function(e){c(e.data)})).catch((function(e){return console.log(e)}))};return Object(a.useEffect)((function(){var e;return e=setInterval((function(){return o(l+1)}),1e4),f(),function(){return clearInterval(e)}}),[l]),r.a.createElement("div",{className:e.root},r.a.createElement(V.a,{className:e.gridList,cols:4,spacing:2},A.map((function(t){return r.a.createElement(J.a,{key:t.thumbnail},r.a.createElement("img",{src:null===t.thumbnail?te.a:t.thumbnail,alt:t.title,onClick:function(){return e=t,void P.playMedia(e.id).then((function(t){m(e.id)})).catch((function(e){return console.log(e)}));var e}}),r.a.createElement(Y.a,{title:t.title,classes:{root:e.titleBar,title:e.title},actionIcon:r.a.createElement(E.a,{"aria-label":"delete ".concat(t.title),onClick:function(){return e=t,void $.delete_(e.id).then((function(e){f()})).catch((function(e){return console.log(e)}));var e}},r.a.createElement(T.a,{className:e.title}))}),")}")}))))},re=n(65),Ae=n.n(re),ce=n(66),ue=n.n(ce),ie=n(67),le=n.n(ie),oe=n(73),se=n.n(oe),pe=n(74),me=n.n(pe),fe=n(72),Ee=n.n(fe),de=n(68),ge=n.n(de),be=n(71),ve=n.n(be),he=n(69),Ce=n.n(he),we=n(70),xe=n.n(we);n(114);var ye=function(){var e=Object(a.useState)(!0),t=Object(h.a)(e,2),n=t[0],A=t[1],c=function(e){console.log("player: ",e),"PAUSED"===e.state?A(!1):A(!0)},u=function(e){for(var t=arguments.length,n=new Array(t>1?t-1:0),a=1;a<t;a++)n[a-1]=arguments[a];e.apply(void 0,n).then((function(e){c(e.data)})).catch((function(e){return console.log(e)}))};return Object(a.useEffect)((function(){u(P.get)}),[]),r.a.createElement(s.a,{container:!0,spacing:1},r.a.createElement(s.a,{item:!0,xs:6,md:4},r.a.createElement(w.a,{size:"small",variant:"text"},r.a.createElement(E.a,{onClick:function(){return u(P.pauseMedia)}},n?r.a.createElement(Ae.a,null):r.a.createElement(ue.a,null)),r.a.createElement(E.a,{onClick:function(){return u(P.stopMedia)}},r.a.createElement(le.a,null)))),r.a.createElement(s.a,{item:!0,xs:6,md:4,className:"SeekButtons"},r.a.createElement(w.a,{size:"small",variant:"text"},r.a.createElement(E.a,{onClick:function(){return u(P.seekMedia,!1,!0)}},r.a.createElement(ge.a,null)),r.a.createElement(E.a,{onClick:function(){return u(P.seekMedia,!1,!1)}},r.a.createElement(Ce.a,null)),r.a.createElement(E.a,{onClick:function(){return u(P.seekMedia,!0,!1)}},r.a.createElement(xe.a,null)),r.a.createElement(E.a,{onClick:function(){return u(P.seekMedia,!0,!0)}},r.a.createElement(ve.a,null)))),r.a.createElement(s.a,{item:!0,xs:12,md:4,className:"SubtitleButtons"},r.a.createElement(w.a,{size:"small",variant:"text"},r.a.createElement(E.a,{onClick:function(){return u(P.seekSubtitle,!1)}},r.a.createElement(Ee.a,null)),r.a.createElement(E.a,{onClick:function(){return u(P.toggleSubtitle)}},r.a.createElement(se.a,null)),r.a.createElement(E.a,{onClick:function(){return u(P.seekSubtitle,!0)}},r.a.createElement(me.a,null)))))},Be=n(161),ke=n(75),je=n.n(ke),Oe=n(76),Qe=n.n(Oe);var Me=function(){var e=r.a.useState(30),t=Object(h.a)(e,2),n=t[0],A=t[1];return Object(a.useEffect)((function(){P.get().then((function(e){!function(e){A(e.volume)}(e.data)})).catch((function(e){return console.log(e)}))}),[]),r.a.createElement("div",null,r.a.createElement(d.a,{id:"continuous-slider",gutterBottom:!0},"Volume ",n," %"),r.a.createElement(s.a,{container:!0,spacing:2},r.a.createElement(s.a,{item:!0},r.a.createElement(je.a,null)),r.a.createElement(s.a,{item:!0,xs:!0},r.a.createElement(Be.a,{value:n,onChange:function(e,t){A(t)},onChangeCommitted:function(e,t){P.updateVolume(t)},"aria-labelledby":"continuous-slider"})),r.a.createElement(s.a,{item:!0},r.a.createElement(Qe.a,null))))},Ie=function(e){Object(l.a)(n,e);var t=Object(o.a)(n);function n(){return Object(u.a)(this,n),t.apply(this,arguments)}return Object(i.a)(n,[{key:"render",value:function(){return r.a.createElement(s.a,{container:!0},r.a.createElement(s.a,{item:!0,sm:1,md:2}),r.a.createElement(s.a,{item:!0,container:!0,xs:12,sm:10,md:8},r.a.createElement(s.a,{item:!0,container:!0},r.a.createElement(v,null),r.a.createElement(p.a,{elevation:3,style:{flex:1,padding:24}},r.a.createElement(s.a,{item:!0,container:!0,direction:"column",spacing:4},r.a.createElement(s.a,{item:!0},r.a.createElement(X,null)),r.a.createElement(s.a,{item:!0},r.a.createElement(ae,null)),r.a.createElement(s.a,{item:!0},r.a.createElement(ye,null)),r.a.createElement(s.a,{item:!0},r.a.createElement(Me,null)))))),r.a.createElement(s.a,{item:!0,sm:1,md:2}))}}]),n}(a.Component);c.a.render(r.a.createElement(r.a.StrictMode,null,r.a.createElement(Ie,null)),document.getElementById("root"))},54:function(e,t,n){},63:function(e,t){e.exports="data:image/png;base64,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"},86:function(e,t,n){e.exports=n(115)},91:function(e,t,n){}},[[86,1,2]]]);
//# sourceMappingURL=main.03a23257.chunk.js.map