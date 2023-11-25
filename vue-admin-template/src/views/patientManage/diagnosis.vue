<template>
  <div>
    <el-table :data="tableData" v-loading="loading" style="width: 100%">
      <el-table-column type="index" label="序号" align="center" width="70"/>
      <el-table-column prop="patientName" label="患者姓名" align="center" width="300"/>
      <el-table-column prop="doctorname" label="诊治医师" align="center" width="300"/>
      <el-table-column prop="diagnosisTime" label="处理时间" align="center" width="300"/>
      <el-table-column label="完成状态" align="center" width="300">
        <template v-slot="{row}">
          <a v-if="row.returntime">{{ row.returntime }}</a>
          <el-tag size="mini" v-else type="danger">
            处理中
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="300px">
        <template v-slot="{row}">
          <el-button type="success" v-if="!row.returntime" @click="returnbook(row)" size='mini'>完成</el-button>
          <el-button type="primary" v-if="!row.returntime" @click="generateReport(row)" size="mini">报告生成</el-button>
          <el-button type="info" v-if="!row.returntime" @click="showForm(row)" size="mini">编辑报告</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      background
      style="margin-top: 20px;text-align: center"
      :current-page="pageNum"
      :page-size="pageSize"
      :total="total"
      :pager-count="5"
      :page-sizes="[5,15,30]"
      layout="prev,pager,next,jumper,->,sizes,total"
      @current-change="getPatientList"
      @size-change="handleSizeChange"
    />

    <el-dialog :title="'请书写报告内容'" :visible.sync="dialogFormVisible">
      <el-form model="form">
        <el-form-item label="报告" :label-width="formLabelWidth">
          <el-input v-model="form.report" type="textarea" :rows="15" style="width: 300px;"/>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取消</el-button>
        <el-button type="primary" @click="onForm">确定</el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script>

export default {
  name: "diagnosis",

  data() {
    return {
      form: {
        id: '',
        report: ''
      },
      dialogFormVisible: false,
      tableData: [],
      loading: false,
      pageNum: 1,
      pageSize: 5,
      total: 0
    }
  },
  mounted() {
    this.getPatientList(1)
  },
  methods: {
    async getPatientList(pager = 1) {
      this.loading = true
      this.pageNum = pager
      const {pageNum, pageSize} = this // 发送请求时候需要带参数
      const res = await this.$API.patient.reqDiagnosis(pageNum, pageSize)
      if (res.code === 200) {
        console.log(res.msg)
        this.tableData = res.msg
        this.total = res.total
        this.loading = false
      }
    },
    handleSizeChange(limit) {
      this.pageSize = limit
      this.getPatientList(1)
    },
    async generateReport(row) {
      const patientid = row.patientid
      const diagnosisTime = row.diagnosisTime
      const targetPath = `http://localhost:1024/chatHome#/chatHome?patientid=${patientid}&diagnosisTime=${diagnosisTime}`
      window.open(targetPath, '_blank')
    },
    showForm(row) {
      this.dialogFormVisible = true
      this.form = {
        id: row.patientid,
        report: ''
      }
    },
    async onForm() {
      const res = await this.$API.patient.reqSaveAndUpdatePatients(this.form)
      if (res.code === 200) {
        // 关闭表单
        this.dialogFormVisible = false
        // 消息提示
        this.$message({
          message: '修改成功!',
          type: 'success'
        })
      }
    },
    async returnbook(row) {
      this.$confirm(`你确定诊断 ${row.patientName} 吗?`, '删除', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        const result = await this.$API.patient.returnPatient(row.diagnosisTime)
        if (result.code === 200) {
          this.$notify({
              type: 'success',
              message: row.patientName + ' 诊断完成'
            },
          )
          await this.getPatientList(this.pageNum)
        }
      }).catch(() => {
        this.$notify({
          type: 'info',
          message: '已取消'
        })
      })
    }
  }
}
</script>

<style scoped>

</style>
