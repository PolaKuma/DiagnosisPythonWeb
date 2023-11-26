<script setup>

</script>

<template>
  <div>
    <div class="head">
      <router-link to="/helloworld">
        <img src="@/image/home.png" style="height: 25px;position: absolute;top: 2vmin;left: 3vmax">
      </router-link>
    </div>
    <div id="new_box">

      <div class="title_cn">
        资讯中心
      </div>

      <div class="new_con">
        <div class="newtel">
          <ul class="new_telst">
            <li class="" style="color: #fff; opacity: 0.9">`</li>
            <li class="newon" style="text-align: center">院内通知</li>
            <li class="" style="color: #fff"></li>
            <p style="left: 166px;">

            </p>
          </ul>
          <div class="clear">
          </div>
        </div>
        <div class="new-wrap">
          <div class="new_lst" style="display: block;">
            <ul class="new_lst_cn">
              <li class="new_cnlf">
                <p class="newlf_img">
                  <img src="@/image/huaxi2.png" width="370" height="147">
                </p>
                <p class="newlf_tel">
                  <a href="#"> 关于开展第十五批四川省学术和技术带头人及后备人选推荐工作的通知</a>
                </p>
                <p class="newlf_tx">
                  根据《四川省人力资源和社会保障厅关于开展第十五批四川省学术和技术带头人及后备人选推荐工作的通知》,
                  启动我院第十五批四川省学术和技术带头人及后备人选推荐工作。
                </p>
              </li>
              <li class="new_cnrf">
                <div class="newrf_lst">
                  <dl>
                    <dd>
                      <p class="new_rq">
                        <span>26</span>2018-7
                      </p>
                      <p class="newrf_tx">
                        <router-link to="/news">
                          世界首例！耳鼻咽喉-头颈外科陈飞教授...
                        </router-link>
                        <span>继完成亚洲首例异体“喉-气管-甲状腺”联合移植手术后，近日，我院耳鼻咽喉-头颈外科陈飞...</span>
                      </p>
                    </dd>
                    <dd>
                      <p class="new_rq">
                        <span>25</span>2018-7
                      </p>
                      <p class="newrf_tx">
                        <a href="#"> 2024/2025年度瑞士互换奖学金项目</a>
                        <span>接学校国际合作与交流处通知，双方每年互换奖学金留学人员，前往对方国家学习或研修...</span>
                      </p>
                    </dd>
                    <dd>
                      <p class="new_rq">
                        <span>24</span>2018-7
                      </p>
                      <p class="newrf_tx">
                        <a href="#"> 2023年中秋国庆放假安排及有关事项</a>
                        <span>2023年中秋节、国庆节放假时间安排及有关事项通知如下...</span>
                      </p>
                    </dd>
                    <dd>
                      <p class="new_rq">
                        <span>23</span>2018-7
                      </p>
                      <p class="newrf_tx">
                        <a href="#"> 2023年西部地区人才培养特别项目选派</a>
                        <span>接四川省教育厅通知，2023年西部地区人才培养特别项目选派工作已开始...</span>
                      </p>
                    </dd>
                    <dd>
                      <p class="new_rq">
                        <span>19</span>2018-7
                      </p>
                      <p class="newrf_tx">
                        <a href="#"> 2023年清明节放假安排及有关事项</a>
                        <span>结合我院实际情况，现将2023年清明节放假时间安排及有关事项通知如下，请遵照执行...</span>
                      </p>
                    </dd>
                    <dd>
                      <p class="new_rq">
                        <span>18</span>2018-7
                      </p>
                      <p class="newrf_tx">
                        <a href="#"> 做好2023年医师资格考试报名工作</a>
                        <span>近日，国家卫健委已启动2023年医师资格考试报名工作，考试报名包括网上报名和现场...</span>
                      </p>
                    </dd>
                  </dl>
                </div>
              </li>
              <div class="clear">
              </div>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
/* 公共样式表css */
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

.head {
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
  margin-top: 10vmax;
  margin-left: 15vmax;
  margin-right: 15vmax;
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
