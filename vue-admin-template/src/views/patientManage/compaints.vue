<template>
  <div class="officeComplaint">
    <!-- Tabs 标签页 -->
    <el-tabs v-model="activeName">
      <el-tab-pane label="投诉处理" name="second">
        <div class="importants">
          <h1>{{ complaintList.tittle }}</h1>
          <h3>{{ complaintList.subheading }}</h3>
          <h2>一、投诉途径与渠道</h2>
          <ol>
            <li v-for="item in complaintList.ways">{{ item }}</li>
          </ol>
          <h2>二、受理投诉的部门和范围</h2>
          <ol>
            <li v-for="item in complaintList.offices">{{ item }}</li>
          </ol>
        </div>
      </el-tab-pane>
      <el-tab-pane label="患者留言" name="first">
        <template>
          <el-button v-if="usertype===1" type="primary" @click="addComplaintFormVisible = true">新增投诉</el-button>
          <el-table :header-cell-style="{background:'#f5f7fa',color:'#606266'}" :data="complaintPatientList"
                    height="600" border style="width: auto">
            <el-table-column type="expand">
              <template scope="props">
                <el-form :model="props.row">
                  <el-row>
                    <el-col :span="24">
                      <el-form-item label="医生回复">
                        <span>{{ props.row.reply }}</span>
                      </el-form-item>
                    </el-col>
                  </el-row>
                  <el-row>
                    <el-col :span="24">
                      <el-form-item label="处理结果">
                        <span>{{ props.row.results }}</span>
                      </el-form-item>
                    </el-col>
                  </el-row>
                </el-form>
              </template>
            </el-table-column>
            <el-table-column prop="patient_id" label="病例号" width="180"></el-table-column>
            <el-table-column prop="patient_name" label="患者姓名" width="180"></el-table-column>
            <el-table-column prop="complaint_date" label="投诉日期" width="180"></el-table-column>
            <el-table-column prop="contents" label="投诉内容" width="300"></el-table-column>
            <el-table-column label="操作">
              <template v-slot="{row}">
                <el-button type="primary" size="mini" @click="showForm(row)">回复</el-button>
                <el-button type="info" size="mini" @click="showPatient(row)">查看</el-button>
                <el-button size="small" type="danger" @click="deletePatient(row)">删除
                </el-button>
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
            @current-change="getCompaintsList"
            @size-change="handleSizeChange"
          />
          <!-- 对话框部分 -->
          <el-dialog :title="'请书写回复内容'" :visible.sync="dialogFormVisible">
            <el-form model="form">
              <el-form-item v-if="usertype===2" label="回复" :label-width="formLabelWidth">
                <el-input v-model="form.reply" type="textarea" :rows="15" style="width: 300px;"/>
              </el-form-item>
              <el-form-item v-if="usertype===1" label="结果" :label-width="formLabelWidth">
                <el-input v-model="form.results" type="textarea" :rows="15" style="width: 300px;"/>
              </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button @click="dialogFormVisible = false">取消</el-button>
              <el-button type="primary" @click="handleReply">确定</el-button>
            </div>
          </el-dialog>
          <!-- Complaint Form Dialog -->
          <el-dialog :title="'新增投诉'" :visible.sync="addComplaintFormVisible">
            <el-form :model="newComplaintForm">
              <el-form-item label="病例号" :label-width="formLabelWidth">
                <el-input v-model="newComplaintForm.patient_id"/>
              </el-form-item>
              <el-form-item label="患者姓名" :label-width="formLabelWidth">
                <el-input v-model="newComplaintForm.patient_name"/>
              </el-form-item>
              <el-form-item label="投诉日期" :label-width="formLabelWidth">
                <el-date-picker v-model="newComplaintForm.complaint_date" type="date" placeholder="选择日期"/>
              </el-form-item>
              <el-form-item label="投诉内容" :label-width="formLabelWidth">
                <el-input v-model="newComplaintForm.contents" type="textarea" :rows="5"/>
              </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button @click="addComplaintFormVisible = false">取消</el-button>
              <el-button type="primary" @click="handleAddComplaint">确定</el-button>
            </div>
          </el-dialog>
          <el-dialog :title="'患者信息'" :visible.sync="showAttributesDialogVisible">
            <el-table :data="[patient_p_info]">
              <el-table-column prop="id" label="病例号"></el-table-column>
              <el-table-column prop="patientName" label="患者名字"></el-table-column>
              <el-table-column prop="doctorname" label="诊治医师"></el-table-column>
              <el-table-column prop="diagnosisTime" label="诊断时间"></el-table-column>
              <el-table-column prop="returntime" label="完成时间"></el-table-column>
            </el-table>
          </el-dialog>
        </template>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import {mapGetters} from 'vuex'

export default {
  computed: {
    ...mapGetters([
      'usertype'
    ])
  },
  data() {
    return {
      showAttributesDialogVisible: false,
      addComplaintFormVisible: false,
      pageNum: 1,
      pageSize: 10,
      dialogFormVisible: false,
      complaintList: [],
      complaintPatientList: [],
      messages: [],
      total: 10,
      loading: false,
      patientList: [],
      form: {},
      patient_p_info: {},
      patient_info: [],
      newComplaintForm: {
        patient_id: '',
        patient_name: '',
        complaint_date: '',
        contents: ''
      },
      activeName: 'second',
      searchName: '',
      Index: '',
      textarea: ''
    }
  },
  mounted() {
    this.complaintList = {
      'tittle': '医院患者投诉处理流程',
      'subheading': '为有效解决各类投诉问题，确保公民的合法权益得到妥善保障，推动医院服务水平不断提升，服务质量不断提高，维护医院良好形象。根据相关法律法规和医疗管理制度，结合医院的实际情况，制订了完善的投诉处理制度。',
      'ways': ['医院投诉监督电话(0511-88619092)、医院电子邮箱(zjzyydb@163.com)，医院公众场所的意见投诉箱，各系统、科室、班组意见薄(本)。', '建立院总值班制度，急诊期间接待来访、受理投诉，投诉电话(18906100399)。', '院办公室、党委办公室为综合接待受理、协调投诉科室，其它职能科室受理职权范围内的投诉。'],
      'offices': ['门诊部：受理并协调解决门诊患者对于医生服务态度、医疗质量、物价医保等方面的投诉。受理地点：总服务台、门诊部主任办公室。投诉电话(0511-88619015、88619016)', '院办公室：受理行政事务与管理方面的投诉。投诉电话(0511-88619092)', '党委办公室：受理医德医风、职工违规违纪方面的投诉。投诉电话 (0511-88619093)', '人事科：受理职工劳动纪律方面的投诉。投诉电话(0511-88619091)', '医教科：受理医疗质量、医疗纠纷方面的投诉。投诉电话(0511-88619085)', '护理部：受理护理质量、护理纠纷方面的投诉。投诉电话(0511-88619089)', '财务科：受理医疗收费记账,医疗物价方面的投诉。投诉电话(0511-88619087)', '保卫科：受理医院安全方面的投诉。投诉电话(0511-88619086)', '总务科：受理后勤保障方面的投诉。投诉电话(0511-88619090)', '器械科：受理设备管理方面的投诉。投诉电话(0511-88619077)', '疾控科：受理院内感染方面的投诉。投诉电话(0511-88619084)', '药剂科：受理药品质量、价格及药事管理方面的投诉。投诉电话(0511-88619078)', '各系统、各科室受理本系统和科室范围内的投诉。', '其它应该受理的投诉问题由相应的职能部门受理。']
    }
    this.getCompaintsList(1)
  },
  methods: {
    async getCompaintsList(pager = 1) {
      this.loading = true
      this.pageNum = pager
      const { pageNum, pageSize } = this
      var search = this.searchName
      if (search === '') {
        search = 'None'
      }
      console.log(search)
      const res = await this.$API.flow.findCompaints(pageNum, pageSize, search)
      if (res.code === 200) {
        this.complaintPatientList = res.msg
        this.total = res.total
        this.loading = false
      }
    },
    handleSizeChange(limit) {
      this.pageSize = limit
      this.getCompaintsList()
    },
    async handleReply() {
      console.log(this.form)
      const res = await this.$API.flow.updateCompaints(this.form)
      if (res.code === 200) {
        // 关闭表单
        this.dialogFormVisible = false
        // 消息提示
        this.$message({
          message: '修改成功!',
          type: 'success'
        }, await this.getCompaintsList(this.form.id ? this.pageNum : 1))
      }
    },
    async showPatient(row) {
      const res = await this.$API.patient.reqPDiagnosis(1, 10, row.patient_id)
      this.patient_info = res.msg
      this.patient_p_info = this.patient_info[0]
      console.log(this.patient_info)
      this.showAttributesDialogVisible = true
    },
    async handleAddComplaint() {
      const res = await this.$API.flow.addCompaints(this.newComplaintForm)
      if (res.code === 200) {
        // 关闭表单
        this.addComplaintFormVisible = false
        // 消息提示
        this.$message({
          message: '添加成功!',
          type: 'success'
        }, await this.getCompaintsList(this.form.id ? this.pageNum : 1))
      }
    },
    async deletePatient(row) {
      this.$confirm(`你确定删除 ${row.patient_name} 吗?`, '删除', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        const result = await this.$API.flow.delCompaints(row.id)
        console.log(result)
        if (result.code === 200) {
          this.$notify({ type: 'success', message: '删除成功!' }, await this.getCompaintsList(this.complaintPatientList.length > 1 ? this.pageNum : this.pageNum - 1)
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
    showForm(row) {
      this.dialogFormVisible = true
      this.form = {...row}
      console.log('this.form')
      console.log(this.form)
    }
  }
}
</script>

<style>
.importants h1 {
  padding-top: 10px;
  font-size: 22px;
  margin: 0 0 20px 0;
}

.importants h2 {
  font-size: 18px;
  margin: 10px 0 30px 0;
}

.importants h3 {
  color: red;
  font-size: 14px;
  padding: 0 0 10px 40px;
}

.importants li {
  margin-left: 30px;
  margin-bottom: 20px;
}

.el-table {
  box-shadow: 0 15px 30px rgba(0, 0, 0, .2);
  border-radius: 10px;
}
</style>
