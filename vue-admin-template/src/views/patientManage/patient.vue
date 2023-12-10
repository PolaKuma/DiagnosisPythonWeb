<template>
  <div class="all">
    <div>
      <div style="text-align: center">
        <el-select v-model="key" style="width: 120px" placeholder="请选择">
          <el-option label="患者名字" value="patientName"/>
          <el-option label="诊治医师" value="doctor"/>
          <el-option label="性别" value="patientSex"/>
          <el-option label="年龄" value="patientAge"/>
        </el-select>
        <el-input v-model="value" autocomplete="off" style="width: 500px; margin: 20px"/>
        <el-button type="primary" @click="onState">搜素</el-button>
      </div>
      <el-button class="add" type="primary" icon="el-icon-edit" @click="showForm">添加患者</el-button>

    </div>
    <el-table :header-cell-style="{background:'#f5f7fa',color:'#606266'}" v-loading="loading" :data="tableData" style="width: 100%">
      <el-table-column type="index" label="序号" align="center" width="70"/>
      <el-table-column prop="id" label="病例号" align="center" width="300"/>
      <el-table-column prop="patientName" label="名字" align="center" width="300"/>
      <el-table-column prop="patientAge" label="年龄" align="center" width="180"/>
      <el-table-column prop="patientSex" label="性别" align="center" width="180"/>
      <el-table-column prop="date" label="生日" align="center" width="180"/>
      <el-table-column prop="doctor" label="主治医师" align="center"/>
      <el-table-column label="操作" align="center" width="330" fixed="right">
        <template v-slot="{row}">
          <el-button type="success" size="mini" @click="diagnosisPatient(row)">诊断</el-button>
          <el-button type="primary" size="mini" @click="showForm(row)">编辑</el-button>
          <el-button type="danger" size="mini" @click="deleted(row)">删除</el-button>
          <el-button type="info" size="mini" @click="showAttributesDialog(row)">显示</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      background
      style="margin-top: 20px;text-align: center"
      :current-page="pageNum"
      :page-size="pageSize"
      :total="total"
      :pager-count="10"
      :page-sizes="[10,15,30]"
      layout="prev,pager,next,jumper,->,sizes,total"
      @current-change="getPatientList"
      @size-change="handleSizeChange"
    />

    <el-dialog :title="form.id ? '修改患者信息':'新增患者信息'" :visible.sync="dialogFormVisible">
      <el-form :model="form">
        <el-form-item v-if="!form.id" label="病例号" :label-width="formLabelWidth">
          <el-input v-model="form.caseid" autocomplete="off" style="width: 300px;"/>
        </el-form-item>
        <el-form-item label="名字" :label-width="formLabelWidth">
          <el-input v-model="form.patientName" autocomplete="off" style="width: 300px;"/>
        </el-form-item>
        <el-form-item label="年龄" :label-width="formLabelWidth">
          <el-input v-model="form.patientAge" autocomplete="off" style="width: 300px;"/>
        </el-form-item>
        <el-form-item label="性别" :label-width="formLabelWidth">
          <el-input v-model="form.patientSex" autocomplete="off" style="width: 300px;"/>
        </el-form-item>
        <el-form-item label="体重" :label-width="formLabelWidth">
          <el-input v-model="form.patientWeight" autocomplete="off" style="width: 300px;"/>
        </el-form-item>
        <el-form-item label="生日" :label-width="formLabelWidth">
          <el-date-picker v-model="form.date" value-format="yyyy年MM月" format="" type="month" placeholder="选择日期"/>
        </el-form-item>
        <el-form-item label="主治医师" :label-width="formLabelWidth">
          <el-input v-model="form.doctor" autocomplete="off" style="width: 300px;"/>
        </el-form-item>
        <el-form-item label="报告" :label-width="formLabelWidth">
          <el-input v-model="form.report" autocomplete="off" style="width: 300px;"/>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="onForm">确 定</el-button>
      </div>
    </el-dialog>

    <el-dialog :title="'患者信息'" :visible.sync="showAttributesDialogVisible">
      <el-table :data="[form]">
        <el-table-column prop="id" label="病例号"></el-table-column>
        <el-table-column prop="patientName" label="名字"></el-table-column>
        <el-table-column prop="patientAge" label="年龄"></el-table-column>
        <el-table-column prop="patientSex" label="性别"></el-table-column>
        <el-table-column prop="patientWeight" label="体重"></el-table-column>
        <el-table-column prop="date" label="生日"></el-table-column>
        <el-table-column prop="doctor" label="主治医师"></el-table-column>
      </el-table>
      <el-table :data="[form]">
        <el-table-column prop="report" label="报告"></el-table-column>
      </el-table>
      <el-table :data="[form]">
        <el-table-column label="图片">
          <template slot-scope="scope">
            <img :src="scope.row.patientPic" alt="病例图片" style="max-width: 400px; max-height: 400px;">
          </template>
        </el-table-column>
      </el-table>

      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="saveReport(form)">导出报告</el-button>
        <el-button @click="showAttributesDialogVisible = false">关闭</el-button>
      </div>
    </el-dialog>
  </div>

</template>

<script>

import {mapGetters} from 'vuex'

export default {
  name: 'Patient',
  computed: {
    ...mapGetters([
      'usertype'
    ])
  },
  data() {
    return {
      tableData: [],
      showAttributesDialogVisible: false,
      dialogFormVisible: false,
      form: {
        doctor: '',
        caseid: '',
        patientAge: '',
        patientName: '',
        patientSex: '',
        patientWeight: '',
        report: 'none',
        date: '',
        patientPic: ''
      },
      formLabelWidth: '120px',
      pageSize: 5,
      pageNum: 1,
      total: 0,
      key: 'patientName',
      value: '',
      loading: false
    }
  },
  mounted() {
    this.getPatientList(1)
  },
  methods: {
    async getPatientList(pager = 1) {
      this.loading = true
      this.pageNum = pager
      const { pageNum, pageSize } = this // 发送请求时候需要带参数
      const res = await this.$API.patient.reqPatients(pageNum, pageSize, this.key, this.value)
      if (res.code === 200) {
        this.tableData = res.msg
        this.total = res.total
        this.loading = false
        console.log('Response Message:', res.msg)
      }
    },
    async saveReport(form) {
      const res = await this.$API.patient.saveReport(form)
      if (res.code === 200) {
        this.$message({
          message: '导出成功!',
          type: 'success'
        })
      }
    },
    showForm(row) {
      this.dialogFormVisible = true
      this.form = {...row}
    },
    showAttributesDialog(row) {
      this.showAttributesDialogVisible = true
      this.form = {...row}
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
        await this.getPatientList(1)
      }
    },
    deleted(row) {
      this.$confirm(`你确定删除 ${row.patientName} 吗?`, '删除', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        const result = await this.$API.patient.delPatients(row.id)
        if (result.code === 200) {
          this.$notify({
              type: 'success',
              message: '删除成功!'
            },
            await this.getPatientList(1)
          )
        } else {
          this.$notify({
            type: 'warning',
            message: '删除失败,请联系系统运维!'
          })
        }
      }).catch(() => {
        this.$notify({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    onState() {
      this.getPatientList(1)
    },
    handleSizeChange(limit) {
      this.pageSize = limit
      this.getUserList()
    },
    async diagnosisPatient(row) {
      const data = {
        'patientid': row.id,
        'patientName': row.patientName
      }
      this.$confirm(`你确定诊断 ${row.patientName} 吗?`, '删除', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        const result = await this.$API.patient.diagnosisPatient(data)
        if (result.code === 200) {
          this.$notify({
              type: 'success',
              message: '' + row.patientName + ' 待诊断！请到诊断记录中查看'
            }
          )
        }
      }).catch(() => {
        this.$notify({
          type: 'info',
          message: '已取消'
        })
      })
    },
  }
}
</script>

<style scoped>
.flex-container {
  display: flex;
  flex-wrap: wrap;
}

.flex-item {
  flex: 0 0 33.33%;
  box-sizing: border-box;
  padding: 5px; /* 调整列之间的间距 */
}

.all{
  height: 700px;
  width: 1160px;
  background-color: white;
  box-shadow: 0 15px 30px rgba(0,0,0,.3);
}

.add{
  margin-left: 30px;
  margin-bottom: 30px;
}
</style>
