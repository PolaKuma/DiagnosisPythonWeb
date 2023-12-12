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
            <li style='list-style-type:None' v-for="item in complaintList.ways">{{ item }}</li>
          </ol>
          <h2>二、受理投诉的部门和范围</h2>
          <ol>
            <li style='list-style-type:None' v-for="item in complaintList.offices">{{ item }}</li>
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
      ways : [
        "1. 投诉途径与渠道",
        "   1.1 口头投诉",
        "      - 医院前台服务台： 在医院前台服务台，患者可以直接表达投诉意见，工作人员将及时记录并引导患者填写投诉表格。",
        "      - 医疗团队沟通： 患者可以通过与医生、护士或其他医疗团队成员的交流中提出投诉，以便立即解决问题。",
        "   1.2 书面投诉",
        "      - 投诉信函： 可以通过邮寄或亲自递交投诉信函至医院行政办公室。信函中需包含患者基本信息、投诉细节、联系方式等。",
        "      - 电子邮件： 患者可以通过医院提供的投诉专用电子邮件地址发送投诉邮件，确保在邮件中提供详细信息以便快速处理。",
        "   1.3 在线投诉",
        "      - 官方网站投诉页面： 在医院官方网站上设有专门的投诉页面，患者可在此填写在线投诉表格，并附上相关证明材料。",
        "      - 医院APP投诉模块： 医院移动应用程序中设置了投诉模块，用户可在应用内直接提交投诉，方便快捷。",
        "   1.4 电话投诉",
        "      - 投诉热线： 医院设有专门的投诉热线电话，患者可通过拨打该电话表达投诉意见，确保电话中提供详细信息以便记录。",
        "2. 投诉处理流程",
        "   2.1 投诉接收与记录",
        "      无论投诉途径如何，医院将在接收到投诉后立即进行记录，并确保所有相关信息完整。",
        "   2.2 投诉初步调查",
        "      医院将启动初步调查程序，核实投诉事实，了解相关情况，并尽快采取必要的应对措施。",
        "   2.3 投诉跟踪与反馈",
        "      医院将定期跟踪投诉处理进展，确保在合理的时间内提供反馈给患者，解释已采取的措施以及问题的解决情况。",
        "   2.4 投诉解决与改进",
        "      医院将根据投诉情况采取相应的解决方案，并通过改进医疗服务流程、提高沟通效果等手段，防范类似问题再次发生。",
        "   2.5 终结与总结",
        "      一旦投诉得到妥善解决，医院将对整个投诉处理流程进行总结，以进一步改进患者服务质量。",
        "通过上述投诉途径与渠道，Pola医院致力于提供一个开放、透明、快捷的患者投诉处理机制，确保患者的合法权益得到充分尊重和保障。"
      ],
      'offices': ["受理投诉的部门和范围",

    "受理投诉的部门：",
    "   - 医院行政办公室：负责协调和处理所有患者投诉事宜，确保投诉能够得到妥善解决。",
    "   - 医疗质量管理部：主要处理涉及医疗服务质量的投诉，包括医疗错误、护理不当、手术事故等方面。",
    "   - 客户服务部：负责处理服务态度、患者体验等与医护人员服务相关的投诉。",
    "   - 环境卫生部：主要处理医院环境卫生、设施维护等方面的投诉。",
    "   - 财务部：处理与收费相关的投诉，包括医疗费用不明、计费错误等。",
    "   - 信息安全与隐私保护办公室：负责处理涉及隐私泄露、信息安全等方面的投诉。",
    "   - 人力资源部：处理医护人员的不当行为、歧视行为等投诉。",
    "   - 其他相关部门：根据具体投诉内容，可能会牵涉到其他专业部门的处理。",

    "受理投诉的范围：",
    "   - 医疗服务质量、服务态度、环境卫生、收费问题、隐私保护、人员行为等与患者服务相关的投诉，以及其他问题。"]
    }
    this.getCompaintsList(1)
  },
  methods: {
    async getCompaintsList(pager = 1) {
      this.loading = true
      this.pageNum = pager
      const {pageNum, pageSize} = this
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
          this.$notify({
              type: 'success',
              message: '删除成功!'
            }, await this.getCompaintsList(this.complaintPatientList.length > 1 ? this.pageNum : this.pageNum - 1)
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
