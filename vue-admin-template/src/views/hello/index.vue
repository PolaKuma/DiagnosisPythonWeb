<template>
  <div>
    <div class="nav">
      <div class="nav-item">
        <img src="./logo.png" alt="Logo" style="height: 40px;">
      </div>
      <div class="nav-item">
        <a href="index.html">首页</a>
      </div>
      <div class="nav-item">
        <a href="company.html">公司介绍</a>
      </div>
      <div class="nav-item">
        <a href="knowledge.html">科普天地</a>
      </div>
      <div class="nav-item">
        <a href="news.html">新闻资讯</a>
      </div>
    </div>

    <div class="banner"></div>

    <div class="robot">
      <div class="eye eyeleft"></div>
      <div class="eye eyeright"></div>
    </div>
    <div class="container">
      <div class="box">
        <router-link to="/dashboard">
          <h2>病患管理系统</h2>
          <p>描述页面1的内容</p>
        </router-link>
      </div>
      <div class="box">
        <router-link to="/chatHome">
          <h2>AI咨询助手</h2>
          <p>描述页面2的内容</p>
        </router-link>
      </div>
      <div class="box">
        <router-link to="/page3">
          <h2>页面3</h2>
          <p>描述页面3的内容</p>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  methods: {

  }
}
</script>

<style scoped>
/* 在这里可以添加组件的样式 */

* {
  margin: 0;
  padding: 0;
}

.nav {
  padding: 20px;
  text-align: right;
}

.nav-item {
  display: inline-block;
  margin-right: 20px;
  color: #fff;
  margin-left: 20px;
}

.nav-item:last-child {
  margin-right: 20px;
}

.nav-item a {
  color: #333;
  text-decoration: none;
}

.nav-item a:hover {
  background-color: #1482f0;
  color: #eee;
}

.nav-item img {
  vertical-align: middle;
  margin-right: 900px;
}

.banner {
  width: 100%;
  height: 400px;
  /* 设置高度，根据实际需要调整 */
  background-image: url('banner.png');
  background-size: cover;
  /* 使背景图片完全覆盖div */
  background-position: center;
  /* 居中显示背景图片 */
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
}

.container {
  display: flex;
  justify-content: space-around;
  padding: 170px;
}

.box {
  flex: 1;
  text-align: center;
  padding: 40px;
  border: 1px solid #ccc;
  margin: 30px;
  cursor: pointer;
}

/* 添加链接样式 */
.box a {
  text-decoration: none;
  color: #333;
}

.robot {
  position: absolute;
  top: 450px;
  left: 30%;
  height: 30%;
  width: 40%;
}

.robot .eyeleft {
  box-shadow: 18px 18px 30px rgba(0, 0, 0, 0.1),
  -18px -18px 30px rgba(255, 255, 255, 1);
  position: absolute;
  top: 30%;
  left: 25%;
  float: left;
  background-color: black;
  width: 2em;
  height: 40%;
  border-radius: 2em;
  animation: blink 5s;
  -moz-animation: blink 5s;
  /* Firefox */
  -webkit-animation: blink 5s;
  /* Safari and Chrome */
  -o-animation: blink 5s;
  /* Opera */
  -webkit-animation-iteration-count: infinite;
  animation-iteration-count: infinite;
}

.robot .eyeright {
  box-shadow: 18px 18px 30px rgba(0, 0, 0, 0.1),
  -18px -18px 30px rgba(255, 255, 255, 1);
  position: absolute;
  top: 30%;
  right: 25%;
  float: left;
  background-color: black;
  width: 2em;
  height: 40%;
  border-radius: 2em;
  animation: blink 5s;
  -moz-animation: blink 5s;
  /* Firefox */
  -webkit-animation: blink 5s;
  /* Safari and Chrome */
  -o-animation: blink 5s;
  /* Opera */
  -webkit-animation-iteration-count: infinite;
  animation-iteration-count: infinite;
}

@keyframes blink {
  47% {
    height: 40%;
    top: 30%;
    width: 2em;
  }

  50% {
    height: 1%;
    top: 50%;
    width: 4em;
  }

  53% {
    height: 40%;
    top: 30%;
    width: 2em;
  }
}
</style>
