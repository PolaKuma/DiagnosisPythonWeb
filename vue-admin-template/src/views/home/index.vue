<template>
  <div class="hello">
    <el-row :gutter="20">
      <el-col :span="8">
        <div class="grid-content bg-purple">
          <!-- 首页user信息 -->
          <el-card shadow='hover'>
            <div class="userCard">
              <el-avatar :size="150" :src="getAvatarUrl"></el-avatar>
              <div class="userInfo">
                <p class="important-font" style="font-size:20px !important;">{{ name }}</p>
                <p class="secondary-font">欢迎你！</p>
              </div>
            </div>
            <div class="login-info">
              <p v-if="usertype === 2">入职日期: 2023-12-10 07:29:48.294403</p>
              <p v-else>入职日期: 2023-11-29 14:52:54.909620</p>
            </div>
          </el-card>
          <!-- 首页表格 -->
          <el-card shadow='hover' class="tableInfo">
            <div slot="header">
              <span class="important-font">待诊断病患信息</span>
            </div>
            <div>
              <el-table
                :data="tableData"
                stripe
                border
                height="320px"
                style="width: 100%">
                <el-table-column
                  prop="date"
                  label="日期"
                  width="120">
                </el-table-column>
                <el-table-column
                  prop="name"
                  label="姓名"
                  width="80">
                </el-table-column>
                <el-table-column
                  prop="address"
                  label="地址">
                </el-table-column>
              </el-table>
            </div>
          </el-card>
        </div>
      </el-col>
      <el-col :span="16">
        <!-- 两个阴阳信息 -->
        <div class="num">
          <el-card shadow='hover' v-for="item in countData" :key="item.name" :body-style="{ display: 'flex',padding: 0 }" class="OrderCard">
            <i class="icon" :class="'el-icon-'+item.icon" :style="{ background: item.color}"></i>
            <div>
              <p class="important-font" style="margin-top: 2vmin !important;" id="numa">{{ item.value }}</p>
              <p class="secondary-font" style="margin-top: 2vmin !important;" id="numb">{{ item.name }}</p>
            </div>
          </el-card>
        </div>
        <!-- 柱状图 -->
        <el-card style="height: 280px">
          <div style="height:280px;" ref="barEcharts">{{ initBarEcharts() }}</div>
        </el-card>
        <div class="num graph">
          <el-card style="width:100%;">
            <div style="">
              <el-calendar v-model="value"></el-calendar>
            </div>
          </el-card>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters([
      'usertype',
      'name'
    ]),
    getAvatarUrl() {
      // Define the avatar URLs based on usertype
      const adminAvatar = require('@/assets/img/head_portrait1.jpg')
      const defaultAvatar = require('@/assets/img/head_portrait.jpg')
      switch (this.usertype) {
        case 1:
          return adminAvatar
        default:
          return defaultAvatar
      }
    }
  },
  name: 'Index',
  data() {
    return {
      value: new Date(),
      tableData: [{
        date: '2023-12-03',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1518 弄'
      }, {
        date: '2023-12-05',
        name: '李芳',
        address: '广州市天河区珠江新城华夏路 100 号'
      }, {
        date: '2023-12-11',
        name: '陈刚',
        address: '南京市鼓楼区中山路 789 号'
      }, {
        date: '2023-12-12',
        name: '刘美丽',
        address: '成都市武侯区人民南路 456 号'
      }, {
        date: '2023-12-15',
        name: '刘阳',
        address: '重庆市渝中区解放碑步行街 99 号'
      }, {
        date: '2023-12-19',
        name: '赵丽',
        address: '西安市雁塔区曲江南路 666 号'
      }, {
        date: '2023-12-21',
        name: '周明',
        address: '杭州市西湖区黄龙路 333 号'
      }],
      countData: [
        {
          name: '已完成报告数',
          value: 121,
          icon: 'success',
          color: '#2ec7c9'
        },
        {
          name: '未完成报告数',
          value: 3,
          icon: 'star-on',
          color: '#ffb980'
        }
      ]
    }
  }, methods: {
    // 柱状图
    initBarEcharts() {
      // 新建一个promise对象
      let p = new Promise((resolve) => {
        resolve()
      })
      // 然后异步执行echarts的初始化函数
      p.then(() => {
        //	此dom为echarts图标展示dom
        let myChart = echarts.init(this.$refs.barEcharts)
        let option = {
          title: {
            text: '诊断表'
          },
          tooltip: {},
          legend: {
            data: ['阳性', '阴性']
          },
          xAxis: {
            data: ['2023-12-10', '2023-12-11', '2023-12-12', '2023-12-13', '2023-12-14', '2023-12-15']
          },
          yAxis: {},
          series: [
            {
              name: '阳性',
              type: 'bar',
              data: [5, 20, 36, 10, 10, 20]
            },
            {
              name: '阴性',
              type: 'bar',
              data: [10, 18, 34, 8, 12, 21]
            }
          ]
        }
        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option)
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="less" scoped>
.el-card__body {
  padding: 10px;
}

.userCard {
  height: 180px;
  display: flex;
  border-bottom: 2px solid #DCDFE6;
  border-radius: 2px;
}

.userInfo {
  width: auto;
  padding: 6% 0 0 6%;
}

.important-font {
  font-weight: 900;
  font-size: 30px;
}

.secondary-font {
  color: #909399;
  margin-top: 30px;
}

.login-info {
  height: 40px;
  text-align: left;
  color: #909399;
  margin-top: 10px;
}

.tableInfo {
  margin: 20px 0 0 0;
}

.OrderCard {
  margin: 0;
  height: 100px !important;
  border: #DCDFE6 1px solid;
  border-radius: 10px;

  i {
    width: 30%;
    line-height: 120px;
    font-size: 50px;
    color: #fff;
  }

  div {
    width: 300px;
  }
}

.el-card {
  border: none;
  margin-bottom: 10px;
  margin-right: 30px;
}

.num {
  display: flex;
  flex-wrap: wrap;
}

#numa{
  margin-left: 10px;
  margin-top: 10px;
  font-size: 40px;
}

#numb{
  margin-left: 10px;
  margin-top: 0;
  font-size: 20px;
}

.graph {
  margin: 15px 0 0 0;
}

.el-calendar {
  height: 265px;
}

.hello {
  background-color: white !important;
}
</style>
