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
          <el-table :data="complaintPatientList" height="250" border style="width: auto">
            <el-table-column prop="name" label="患者姓名" width="180"></el-table-column>
            <el-table-column prop="date" label="投诉日期" width="180"></el-table-column>
            <el-table-column prop="contents" label="投诉内容" width="300"></el-table-column>
            <el-table-column label="操作">
              <template scope="scope">
                <el-button size="small" @click.native.prevent="lookforPatient(scope.$index)">查看患者信息</el-button>
                <el-button size="small" type="danger"
                           @click.native.prevent="delectPatient(scope.$index, complaintPatientList)">删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          <!-- 表格 -->
        </template>
      </el-tab-pane>
    </el-tabs>
    <el-dialog title="患者详细信息" :visible.sync="dialogFormVisible" :before-close="handleClose">
      <ul class="patientMessage">
        <li><h3>患者姓名:</h3><span>{{ messages.name }}</span></li>
        <li><h3>挂号序:</h3><span>{{ messages.number }}</span></li>
        <li><h3>性别:</h3><span>{{ messages.sex }}</span></li>
        <li><h3>年龄:</h3><span>{{ messages.age }}</span></li>
        <li><h3>病科:</h3><span>{{ messages.disease }}</span></li>
        <li><h3>病情:</h3><span>{{ messages.symptoms }}</span></li>
        <li><h3>手机号码:</h3><span>{{ messages.phone }}</span></li>
        <li><h3>地址:</h3><span>{{ messages.position }}</span></li>
        <li><h3>日期:</h3><span>{{ messages.date }}</span></li>
      </ul>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="dialogFormVisible = false">确 定</el-button>
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
      title: '投诉处理指南',
      subheading: '欢迎您使用投诉处理系统，以下是相关指南。',
      ways: [
        '通过在线投诉系统提交',
        '通过电话拨打投诉热线提交'
      ],
      offices: [
        '医院总务办公室',
        '医院医务部门',
        '其他相关部门'
      ]
    };

    // Sample patient complaint list data for the first tab
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
</style>
