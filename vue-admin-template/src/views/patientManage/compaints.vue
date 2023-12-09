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
          <!-- 表格 -->
          <el-table :header-cell-style="{background:'#f5f7fa',color:'#606266'}" :data="complaintPatientList" height="600" border style="width: auto">
            <el-table-column type="expand">
              <template scope="props">
                <el-form label-position="left" inline class="demo-table-expand">
                  <el-form-item label="患者姓名">
                    <span>{{ props.row.name }}</span>
                  </el-form-item>
                  <el-form-item label="投诉日期">
                    <span>{{ props.row.sex }}</span>
                  </el-form-item>
                  <el-form-item label="投诉内容">
                    <span>{{ props.row.degree }}</span>
                  </el-form-item>
                  <el-form-item label="医生回复">
                    <span>{{ props.row.major }}</span>
                  </el-form-item>
                  <el-form-item label="处理结果">
                    <span>{{ props.row.profession }}</span>
                  </el-form-item>
                </el-form>
              </template>
            </el-table-column>
            <el-table-column prop="name" label="患者姓名" width="180"></el-table-column>
            <el-table-column prop="date" label="投诉日期" width="180"></el-table-column>
            <el-table-column prop="contents" label="投诉内容" width="300"></el-table-column>
            <el-table-column label="操作">
              <template scope="scope">
                <el-button type="primary" size="mini" @click="showForm(row)">回复</el-button>
                <el-button size="small" @click.native.prevent="lookforPatient(scope.$index)">查看患者信息</el-button>
                <el-button size="small" type="danger"
                           @click.native.prevent="delectPatient(scope.$index, complaintPatientList)">删除
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
            @current-change="getUserList"
            @size-change="handleSizeChange"
          />
          <!-- 表格 -->
        </template>
      </el-tab-pane>
    </el-tabs>
    <el-dialog :title="'患者信息'" :visible.sync="dialogFormVisible">
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
        <el-button @click="dialogFormVisible = false">关闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      dialogFormVisible: false,
      complaintList: [],
      complaintPatientList: [],
      messages: [],
      patientList: [],
      activeName: 'second',
      Index: '',
      textarea: ''
    };
  },
  methods: {
    handleClose(done) {
      this.$confirm('确认关闭？')
        .then(_ => {
          done();
        })
        .catch(_ => {
        });
    },
    lookforPatient(index) {
      // console.log(index, row);
      this.dialogFormVisible = true;
      this.Index = compaints;
      // console.log('患者姓名', this.complaintPatientList[this.Index].name);
      for (let i = 0; i < this.patientList.length; i++) {
        if (this.complaintPatientList[this.Index].name === this.patientList[i].name) {
          this.messages = this.patientList[i];
        }
        ;
      }
      ;
    },
    delectPatient(index, rows) {
      rows.splice(compaints, 1);
    },
    getEmpty() {
      this.textarea = '';
    },
    save() {
      if (this.textarea === '') {
        this.$message({
          showClose: true,
          message: '保存失败！',
          type: 'error'
        });
      } else {
        this.$message({
          showClose: true,
          message: '保存成功！',
          type: 'success'
        });
      }
    }
  },
  created() {
    // Sample complaint list data for the second tab
    this.complaintList = {
      "tittle": "医院患者投诉处理流程",
      "subheading": "为及时处理各种投诉，保障公民的合法权益，促进医院改进服务，提高服务质量，维护医院形象。根据有关法律法规和医疗规章制度，结合医院的实际情况，制定投诉处理制度。",
      "ways": ["医院投诉监督电话(0511-88619092)、医院电子邮箱(zjzyydb@163.com)，医院公众场所的意见投诉箱，各系统、科室、班组意见薄(本)。", "建立院总值班制度，急诊期间接待来访、受理投诉，投诉电话(18906100399)。", "院办公室、党委办公室为综合接待受理、协调投诉科室，其它职能科室受理职权范围内的投诉。"],
      "offices": ["门诊部：受理并协调解决门诊患者对于医生服务态度、医疗质量、物价医保等方面的投诉。受理地点：总服务台、门诊部主任办公室。投诉电话(0511-88619015、88619016)", "院办公室：受理行政事务与管理方面的投诉。投诉电话(0511-88619092)", "党委办公室：受理医德医风、职工违规违纪方面的投诉。投诉电话 (0511-88619093)", "人事科：受理职工劳动纪律方面的投诉。投诉电话(0511-88619091)", "医教科：受理医疗质量、医疗纠纷方面的投诉。投诉电话(0511-88619085)", "护理部：受理护理质量、护理纠纷方面的投诉。投诉电话(0511-88619089)", "财务科：受理医疗收费记账,医疗物价方面的投诉。投诉电话(0511-88619087)", "保卫科：受理医院安全方面的投诉。投诉电话(0511-88619086)", "总务科：受理后勤保障方面的投诉。投诉电话(0511-88619090)", "器械科：受理设备管理方面的投诉。投诉电话(0511-88619077)", "疾控科：受理院内感染方面的投诉。投诉电话(0511-88619084)", "药剂科：受理药品质量、价格及药事管理方面的投诉。投诉电话(0511-88619078)", "各系统、各科室受理本系统和科室范围内的投诉。", "其它应该受理的投诉问题由相应的职能部门受理。"]
    },
      this.complaintPatientList = [
        {
          name: 'Patient 1',
          date: '2023-01-01',
          contents: 'Complaint about service quality.'
        },
        {
          name: 'Patient 2',
          date: '2023-02-01',
          contents: 'Complaint about waiting times.'
        },
        // Add more complaint entries as needed
      ];

    // Sample patient details data for the dialog
    this.patientList = [
      {
        name: 'Patient 1',
        number: '12345',
        sex: 'Male',
        age: 30,
        disease: 'Internal Medicine',
        symptoms: 'Fever and cough',
        phone: '123-456-7890',
        position: '123 Main St, City',
        date: '2023-01-01'
      },
      {
        name: 'Patient 2',
        number: '67890',
        sex: 'Female',
        age: 25,
        disease: 'Surgery',
        symptoms: 'Pain in the abdomen',
        phone: '987-654-3210',
        position: '456 Oak St, Town',
        date: '2023-02-01'
      },
      // Add more patient entries as needed
    ];
  },
};
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

.el-table{
  box-shadow: 0 15px 30px rgba(0,0,0,.2);
  border-radius: 10px;
}
</style>
