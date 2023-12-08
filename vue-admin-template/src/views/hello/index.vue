<template>
  <div>
    <div class="container">
      <div class="nav-item">
        <img src="@/image/logo.png">
      </div>
      <div class="robot">
        <div id="chatbot">
          <div class="dot"></div>
          <div class="dot"></div>
          <div class="dot"></div>
        </div>
        <div id="chatbot-corner"></div>
        <div id="antenna">
          <div id="beam"></div>
          <div id="beam-pulsar"></div>
        </div>
      </div>
      <ul id="nav">
        <li><a href="#">首页</a></li>
        <li><a href="#s1">医院介绍</a>
          <span id="s1"></span>
          <ul class="subs">
            <li>电话: 028-85422114</li>
            <li>传真: 028-85582944</li>
            <li>地址1: 四川省成都市武侯区国学巷37号（院本部）</li>
            <li>地址2: 温江区芙蓉大道三段363号（温江院区）</li>
            <li>地址3: 锦江区成龙路和锦江大道交汇处（锦江院区）</li>
            <li>网站备案号: 蜀ICP备16010396号-5-1</li>
          </ul>
        </li>
        <li class="active"><a href="#s2">科普天地</a>
          <span id="s2"></span>
          <ul class="subs">
            <li><B>新冠肺炎CT图特征</B></li>
            <li></li>
            <li>·磨玻璃影</li>
            <li>肺泡肿胀、肺泡间隔液体的渗出，肺泡间隔增厚等，这些会使的肺部的CT数增大。</li>
            <li>·烟花式扩散</li>
            <li>表现为一个中心向四周扩散，存在细小网格或者条状影。</li>
          </ul>
        </li>
        <li><a href="#s2">系统介绍</a>
          <span id="s3"></span>
          <ul class="subs">
            <li>呼吸与危重症医学科辅助诊断系统</li>
            <li>系统是一款综合性医疗辅助诊断系统，包括前台辅助医生诊断的部
              分，以及后台管理病患信息的系统。意图建立完善的信息管理体系，实现医疗资
              源的统一和高效利用，提高医疗诊断的准确性和效率，在减少医生工作量的同时
              改善患者信息管理。
            </li>
          </ul>
        </li>
      </ul>
    </div>

    <div class="banner">
      <div class="button-container">
        <div class="button">
          <router-link to='/homeIndex'>
            <img src="@/image/doctor.png" alt="Icon 1">
            <div class="button-text">
              <div class="title">患者管理系统</div>
              <div class="description"></div>
            </div>
          </router-link>
        </div>
        <div class="button">
          <router-link to='/chatHome'>
            <img src="@/image/diagnose.png" alt="Icon 2">
            <div class="button-text">
              <div class="title">智能辅助诊断</div>
              <div class="description"></div>
            </div>
          </router-link>
        </div>
        <div class="button">
          <router-link to="/newsindex">
            <img src="@/image/news.png" alt="Icon 3">
            <div class="button-text">
              <div class="title">医院新闻公告</div>
              <div class="description"></div>
            </div>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  methods: {}
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
}

html {
  background-color: #fff;
  height: 100%;
}

body {
  color: #fff;
  font: 0.75rem/1.5rem Arial, sans-serif;
}

#nav span {
  display: none;
}

#nav, #nav ul {
  list-style: none outside none;
  margin: 0;
  padding: 0;
}

#nav {
  background-color: #F5F5F5;
  border-bottom: 0.8vmin solid #333333;
  float: left;
  margin-left: 0;
  margin-right: 0;
  position: relative;
}

#nav ul.subs {
  background-color: #FFFFFF;
  box-shadow: 1vmin 1vmin 5vmin rgba(0, 0, 0, 0.2);
  color: #333333;
  display: none;
  left: 0;
  padding: 0%;
  position: absolute;
  top: 9.3vmin;
  width: 100%;
}

/*菜单*/
#nav > li {
  border-bottom: 5px solid transparent;
  float: left;
  color: #fff;
  margin-bottom: -1vmin;
  text-align: left;
  -moz-transition: all 300ms ease-in-out 0s;
  -ms-transition: all 300ms ease-in-out 0s;
  -o-transition: all 300ms ease-in-out 0s;
  -webkit-transition: all 300ms ease-in-out 0s;
  transition: all 300ms ease-in-out 0s;
}

#nav li a {
  display: block;
  background-color: #fff;
  text-decoration: none;
  -moz-transition: color 450ms ease-in-out 0s, background-color 450ms ease-in-out 0s;
  -ms-transition: color 450ms ease-in-out 0s, background-color 450ms ease-in-out 0s;
  -o-transition: color 450ms ease-in-out 0s, background-color 450ms ease-in-out 0s;
  -webkit-transition: color 450ms ease-in-out 0s, background-color 450ms ease-in-out 0s;
  transition: color 450ms ease-in-out 0s, background-color 450ms ease-in-out 0s;
  white-space: normal;
}

#nav > li > a {
  float: right;
  color: #333333;
  display: block;
  font-size: 1rem;
  line-height: 9vmin;
  padding: 0 10vmin;
  text-transform: uppercase;
}

#nav > li:hover > a, #nav > a:hover {
  background-color: #409EFF;
  color: #FFFFFF;
}

#nav li.active > a {
  background-color: #333333;
  color: #FFFFFF;
}

/* submenu */
#nav li:hover ul.subs {
  display: block;
}

#nav ul.subs > li {
  display: inline-block;
  float: none;
  padding: 10px 1%;
  vertical-align: top;
  width: 33%;
}

#nav ul.subs > li a {
  color: #777777;
  line-height: 20px;
}

#nav ul li a:hover {
  color: #F55856;
}

#nav ul.subs > li > a {
  font-size: 1.3em;
  margin-bottom: 10px;
  text-transform: uppercase;
}

#nav ul.subs > li li {
  float: none;
  padding-left: 8px;
  -moz-transition: padding 150ms ease-out 0s;
  -ms-transition: padding 150ms ease-out 0s;
  -o-transition: padding 150ms ease-out 0s;
  -webkit-transition: padding 150ms ease-out 0s;
  transition: padding 150ms ease-out 0s;
}

#nav ul.subs > li li:hover {
  padding-left: 15px;
}

/* responsive rules */
@media all and (max-width: 98vmin) {
  #nav > li {
    float: none;
    border-bottom: 0;
    margin-bottom: 0;

  }

  #nav ul.subs {
    position: relative;
    top: 0;
  }

  #nav li:hover ul.subs {
    display: none;
  }

  #nav li #s1:target + ul.subs,
  #nav li #s2:target + ul.subs {
    display: block;
  }

  #nav ul.subs > li {
    display: block;
    width: auto;
  }
}

.nav-item img {
  width: 23vmin;
  height: 8vmin;
  vertical-align: middle;
  margin-top: 0.7vmin;
  margin-right: 40vmin;
}

.banner {
  width: 100%;
  height: 75vmin;
  /* 设置高度，根据实际需要调整 */
  background-image: url("banner.png");
  background-size: cover;
  /* 使背景图片完全覆盖div */
  background-position: center;
  /* 居中显示背景图片 */
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
}

.button-container {
  position: absolute;
  bottom: 5vmin; /* 调整按钮距离底部的距离 */
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-around; /* 将按钮水平排列 */
}

.button a {
  background-color: #ffffff;
  border-radius: 8vmin;
  padding: 4vmin 2vmax;
  margin: 0 2vmax; /* 调整按钮之间的间距 */
  display: flex;
  align-items: center;
  box-shadow: 2vmin 2vmin 5vmin rgba(0, 0, 0, 0.1);
  text-decoration: none;
  color: #333;
}

.button a:hover {
  transform: scale(1.1); /* 鼠标悬停时按钮放大 */
  box-shadow: 4vmin 4vmin 10vmin rgba(0, 0, 0, 0.5); /* 添加灰色阴影 */
  color: #409EFF;
}

.button a:active {
  transform: translateY(2vmin); /* 点击时按钮缩小 */
  box-shadow: none; /* 移除阴影 */
}

.button img {
  width: 140px; /* 根据实际图标大小调整 */
  height: 100px; /* 根据实际图标大小调整 */
  margin-right: 10px;
}

.button-text a {
  display: flex;
  flex-direction: column;
  text-align: left;
}

.title {
  font-weight: bold;
  font-size: 1.5rem;
}

.description {
  margin-top: 8px;
  font-size: 1rem;
  color: #666;
}

.container {
  display: flex;
  justify-content: space-around;
}

@keyframes blink {
  47% {
    height: 40%;
    top: 30%;
    width: 2rem;
  }

  50% {
    height: 1%;
    top: 50%;
    width: 4rem;
  }

  53% {
    height: 40%;
    top: 30%;
    width: 2rem;
  }
}

.robot {
  position: absolute;
  margin: auto;
  bottom: 0;
  left: 0;
  top: 10vmin;
  right: 0;
  height: 200px;
  width: 200px;
  animation: up-down 7.5s infinite ease-in-out;
  transform-origin: top left; /* 设置变换的原点为左上角 */
  transform: scale(0.5); /* 缩小到原来的一半大小 */
}

.robot #chatbot {
  margin: auto;
  position: absolute;
  bottom: 0;
  left: 0;
  top: 0;
  right: 0;
  width: 150px;
  height: 85px;
  border: 12px solid #FFFFFF;
  border-radius: 5rem;
}

.robot #antenna {
  margin: auto;
  position: absolute;
  bottom: 0;
  left: 0;
  top: 0;
  right: 0;
  top: -125px;
  height: 20px;
  width: 10px;
  background-color: #FFFFFF;
  animation: antenna-appear 7.5s infinite ease-in-out;
}

.robot #antenna #beam {
  position: absolute;
  top: -12.5px;
  left: -5px;
  height: 20px;
  width: 20px;
  border-radius: 50%;
  background-color: #FFFFFF;
  animation: beam-appear 7.5s infinite ease-in-out;
}

.robot #antenna #beam-pulsar {
  position: absolute;
  top: -12.5px;
  left: -5px;
  height: 20px;
  width: 20px;
  border-radius: 50%;
  background-color: #FFFFFF;
  animation: beam-pulsar-appear 7.5s infinite ease-in-out;
}

.robot .dot {
  height: 17.5px;
  width: 17.5px;
  margin: auto;
  position: absolute;
  bottom: 0;
  left: 0;
  top: 0;
  right: 0;
  left: -65px;
  background-color: #FFFFFF;
  border-radius: 50%;
  animation: pulse-outer 7.5s infinite ease-in-out;
}

.robot .dot:nth-child(2) {
  left: 0;
  animation: pulse-inner 7.5s infinite ease-in-out;
  animation-delay: 0.2s;
}

.robot .dot:nth-child(3) {
  left: 65px;
  animation: pulse-outer 7.5s infinite ease-in-out;
  animation-delay: 0.4s;
}

@keyframes pulse-inner {
  0% {
    transform: scale(1);
  }
  7.5% {
    transform: scale(1.5);
  }
  15% {
    transform: scale(1);
  }
  22.5% {
    transform: scale(1.5);
  }
  30% {
    transform: scale(1);
  }
  37.5% {
    transform: scale(1.5);
  }
  45% {
    top: 0;
    transform: scale(1);
    height: 17.5px;
    border-bottom-left-radius: 50%;
    border-bottom-right-radius: 50%;
    transform: rotate(-370deg);
  }
  50% {
    top: 22.5px;
    height: 10px;
    border-top-left-radius: 50%;
    border-top-right-radius: 50%;
    border-bottom-left-radius: 3rem;
    border-bottom-right-radius: 3rem;
    transform: rotate(10deg);
  }
  55% {
    transform: rotate(-10deg);
  }
  60% {
    transform: rotate(10deg);
  }
  65% {
    transform: rotate(-10deg);
  }
  65% {
    transform: rotate(0deg);
  }
  85% {
    top: 22.5px;
    height: 10px;
    border-top-left-radius: 50%;
    border-top-right-radius: 50%;
    border-bottom-left-radius: 3rem;
    border-bottom-right-radius: 3rem;
    transform: rotate(0deg);
  }
  92.5% {
    top: 22.5px;
    height: 10px;
    border-top-left-radius: 50%;
    border-top-right-radius: 50%;
    border-bottom-left-radius: 2.5rem;
    border-bottom-right-radius: 2.5rem;
    transform: rotate(0deg);
  }
  100% {
    top: 0;
    height: 17.5px;
    border-radius: 50%;
    transform: rotate(-360deg);
  }
}

@keyframes pulse-outer {
  0% {
    transform: scale(1);
  }
  7.5% {
    transform: scale(1.5);
  }
  15% {
    transform: scale(1);
  }
  22.5% {
    transform: scale(1.5);
  }
  30% {
    transform: scale(1);
  }
  37.5% {
    transform: scale(1.5);
  }
  45% {
    transform: scale(1);
    height: 17.5px;
  }
  55% {
    tranform: scale(1);
    height: 5px;
  }
  60% {
    height: 17.5px;
  }
  75% {
    height: 17.5px;
  }
  80% {
    tranform: scale(1);
    height: 5px;
  }
  85% {
    height: 17.5px;
  }
  100% {
    height: 17.5px;
  }
}

@keyframes antenna-appear {
  0% {
    visibility: hidden;
    top: -100px;
    height: 0;
  }
  50% {
    visibility: hidden;
    top: -100px;
    height: 0;
  }
  55% {
    visibility: visible;
    top: -125px;
    height: 20px;
  }
  95% {
    visibility: visible;
    top: -125px;
    height: 20px;
  }
  100% {
    top: -100px;
    height: 0;
  }
}

@keyframes beam-appear {
  0% {
    visibility: hidden;
    top: -12.5px;
    height: 0;
  }
  50% {
    visibility: hidden;
    top: -12.5px;
    height: 0;
  }
  55% {
    visibility: visible;
    top: -12.5px;
    height: 20px;
    width: 20px;
  }
  100% {
    visibility: visible;
    top: -12.5px;
    height: 20px;
    width: 20px;
  }
}

@keyframes beam-pulsar-appear {
  0% {
    visibility: hidden;
    top: -12.5px;
    height: 0;
  }
  50% {
    visibility: hidden;
    top: -12.5px;
    height: 0;
  }
  55% {
    visibility: visible;
    top: -12.5px;
    left: -5px;
    height: 20px;
    width: 20px;
    opacity: 1;
  }
  65% {
    top: -25px;
    left: -15px;
    height: 40px;
    width: 40px;
    opacity: 0;
    visibility: visible;
  }
  74% {
    visibility: hidden;
    opacity: 0;
  }
  75% {
    visibility: visible;
    top: -12.5px;
    left: -5px;
    height: 20px;
    width: 20px;
    opacity: 1;
  }
  85% {
    top: -25px;
    left: -15px;
    height: 40px;
    width: 40px;
    opacity: 0;
    visibility: visible;
  }
  94% {
    visibility: hidden;
    opacity: 0;
  }
  100% {
    visibility: hidden;
    opacity: 0;
  }
}

@keyframes up-down {
  0% {
    transform: translate(0);
  }
  12.5% {
    transform: translate(0, 2%);
  }
  25% {
    transform: translate(0);
  }
  37.5% {
    transform: translate(0, 2%);
  }
  50% {
    transform: translate(0);
  }
  62.5% {
    transform: translate(0, 2%);
  }
  75% {
    transform: translate(0);
  }
  87.5% {
    transform: translate(0, 2%);
  }
  100% {
    transform: translate(0);
  }
}
</style>
