<template>
  <div>
    <div class="dashboard-container">
      <div class="dashboard-text">欢迎您！ {{ name }}</div>
    </div>
    <!--块类统计-->
    <el-row :gutter="20" style="margin-top: 2%">
      <el-col :span="8">
        <el-card class="box-card">
          <h3>累计诊断数</h3>
          <div>
            <i class="el-icon-user-solid" style="color: green"></i>
            <span>328</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="box-card">
          <h3>待处理报告数</h3>
          <div>
            <i class="el-icon-s-flag" style="color: red"></i>
            <span>3</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="box-card">
          <h3>阳性患者比例</h3>
          <div>
            <i class="el-icon-star-on" style="color: blue"></i>
            <span>34%</span>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <!--acharts统计图-->
    <el-row :gutter="0">
      <el-col :span="24">
        <el-card class="box-card">
          <echarts1/>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import echarts1 from '@/components/ECharts/echarts1'
import {mapGetters} from 'vuex'

export default {
  name: 'Dashboard',
  components: {
    echarts1
  },
  computed: {
    ...mapGetters([
      'name',
      'usertype'
    ])
  }
}
</script>

<style scoped>
.el-card {
  margin-bottom: 20px;
  text-align: center;
}

.dashboard-text {
  font-weight: bold;
  font-size: 3em;
  text-align: center;
}
</style>
