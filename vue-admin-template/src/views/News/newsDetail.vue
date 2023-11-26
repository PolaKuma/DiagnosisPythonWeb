<script setup>

</script>

<template>
  <div>
    <div class="head">
      <router-link to="/newsindex">
        <img src="@/image/home.png" style="height: 25px;position: absolute;top: 2vmin;left: 3vmax">
      </router-link>>
    </div>
    <div id="new_box">
      <div class="title_cn">
        世界首例！耳鼻咽喉-头颈外科陈飞教授团队完成下咽食管癌多器官簇（5个）联合移植手术
      </div>
      <hr class="line">
    </div>
    <div class="content">
      <p>
        &nbsp;&nbsp;继完成亚洲首例异体“喉-气管-甲状腺”联合移植手术后，近日，我院耳鼻咽喉-头颈外科陈飞教授团队再次为一位52岁下咽癌化疗及免疫治疗效果不佳的男性患者实施异体“喉-气管-甲状腺-下咽-食管”多器官簇（5个器官）联合移植术。这在世界范围内尚属首次，目前，患者术后恢复良好，多器官均存活，已达到出院标准。</p>
    </div>
    <div class="content">
      <p>
        &nbsp;&nbsp;陈飞教授团队短期内连续完成两例高难度喉等多器官联合移植手术，标志着在喉移植领域取得了突破性进展，也为今后该领域的研究及技术开展提供了宝贵经验，更为全喉切除后需要移植喉部患者带来了新的希望。</p>
    </div>
    <div class="img">
      <img src="@/image/news1.png" alt="News Image">
    </div>
  </div>
</template>

<style scoped lang="scss">
.line {
  border-top: 0.5vmin solid #34495e; /* Style the horizontal line */
  margin-top: 4vmin; /* Add some margin above the line */
}

.content {

  font-size: 1rem;
  padding-top: 4vmin;
  padding-left: 13vmax; /* Add padding to the content area */
  padding-right: 13vmax;
}

.img {
  padding-top: 3vmin;
  text-align: center;
  max-width: 100%; /* Ensure images don't exceed the container width */
}

* {
	margin: 0;
	padding: 0;
}
body {
	color: #333;
	font-size: 14px;
	font: 14px/1.6 PingFangSC-Light, 'helvetica neue', 'hiragino sans gb', tahoma, 'microsoft yahei ui', 'microsoft yahei', simsun, sans-serif;
}
html {
	overflow: auto;
}
ul, li {
	list-style-type: none;
	cursor: auto;
}
img {
	vertical-align: middle;
	border: none;
}
a {
	text-decoration: none;
	outline: none;
}
a:hover {
	text-decoration: none;
	outline: none;
	color: #217af0
}
.clear {
	clear: both
}
input {
	border: none;
}

.head{
	position: fixed;
	z-index: 100;
	background-color: #34495e;
	width: 100%;
	height: 8vmin;
	box-shadow: 18px 18px 30px rgba(0, 0, 0, 0.1),
	-18px -18px 30px rgba(255, 255, 255, 1);
}
/* 必要布局样式css */
.title_cn {
	margin: auto;
  margin-top: 5vmax;
	margin-left: 15vmax;
	margin-right:15vmax;
	text-align: center;
	font-weight: bold;
	font-size: 2rem;
}
#new_box {
	width: 100%;
	padding: 50px 0px;
	margin: 0 auto;
	overflow: hidden;
	padding-bottom: 0px;
}
.new_con {
	max-width: 1200px;

	margin: 0 auto;
	margin-top: 50px;
}
.newtel {
	height: 30px;
	border-bottom: 1px solid #e7e7e7;
	padding-bottom: 10px;
	font-family: "微软雅黑";
	font-size: 18px;
	color: #666
}
.new_telst {
	width: 550px;
	margin: 0 auto;
	position: relative;
	top: 6px;
	text-align: center
}
.new_telst li {
	width: 166px;
	line-height: 30px;
	text-align: center;
	float: left;
	display: inline;
	font-family: "微软雅黑";
	cursor: pointer;
}
.new_telst li.newon {
	color: #217af0;
	font-weight: bold;
}
.new_telst p {
	position: absolute;
	top: 34px;
	left: 0px;
	width: 166px;
	height: 7px;
	border-top: 1px solid #217af0;
	overflow: hidden;
	text-align: center;
}
.new_telst b {
	display: inline-block;
	width: 0;
	height: 0;
	margin-top: -3px;
	border-style: solid dashed dashed dashed;
	border-width: 9px;
	border-color: #217af0 #fff #fff #fff;
	overflow: hidden;
	zoom: 1;
	font-size: 0;
}
.new_lst {
	height: 315px;
	position: relative;
	overflow: hidden;
	display: none;
	margin-top: 10px;
	padding-top: 20px;
}
.new_lst ul {
	position: absolute;
	left: 0px;
}
.new-wrap {
	margin-top: 30px;
}
.new-wrap .show {
	display: block;
}
li.new_cnlf {
	width: 370px;
	float: left;
}
li.new_cnlf p {
	width: 100%;
}
p.newlf_tel a {
	color: #217af0;
	font-size: 1.2rem;
	line-height: 7vmin;
	text-align: center;
	display: block;
}
p.newlf_tel a:hover {
	color: #C33
}
p.newlf_tx {
	font-size: 14px;
	line-height: 26px;
	color: #999;
	height: 105px;
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap; //文本不换行，这样超出一行的部分被截取，显示...
}
li.new_cnrf {
	float: right;
	width: 820px;
	margin-left: 10px;
}

.newrf_lst dd {
	width: 368px;
	height: 80px;
	border: 1px solid #e4e4e4;
	float: left;
	margin-left: 35px;
	margin-bottom: 20px;
}
p.new_rq {
	width: 65px;
	height: 65px;
	background: #969393;
	float: left;
	text-align: center;
	color: #FFF;
	margin-top: 10px;
	margin-left: 10px;
	margin-right: 15px;
	font-family: Arial, Helvetica, sans-serif;
}
p.new_rq span {
	display: block;
	font-size: 24px;
	text-align: center;
	font-weight: bold;
	line-height: 35px;
	padding-top: 5px;
}
p.newrf_tx {
	float: left;
	width: 270px;
	margin-top: 8px;
}
p.newrf_tx a {
	color: #333;
	font-size: 14px;
	display: block;
	line-height: 30px;
}
p.newrf_tx span {
	display: block;
	font-size: 12px;
	color: #999;
	height: 60px;
	overflow: hidden;
}
.newrf_lst dd:hover {
	width: 368px;
	height: 80px;
	border: 1px solid #217af0;
	box-shadow: 0px 0px 15px rgba(37, 125, 242, .27);
}
.newrf_lst dd:hover p.newrf_tx a {
	color: #217af0;
}
.newrf_lst dd:hover p.new_rq {
	background: #217af0;
	margin-top: 5px;
	margin-left: 5px;
}
.newrf_lst dd:hover p.newrf_tx {
	margin-top: 5px;
}
.mr0 {
	margin-right: 0px;
}
</style>
