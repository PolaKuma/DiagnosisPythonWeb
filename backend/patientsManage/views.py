import json
import time
import jwt
import xlrd2
from django.http import JsonResponse
from .models import Patient, diagnosisPatient, flow, complaint, duty


class PatientsManage:

    def handle(self, request):
        # 判断是否为GET请求
        if request.method == 'GET':
            pd = request.GET
        else:
            pd = json.loads(request.body)

        request.pd = pd
        action = pd.get('action')

        if action == 'listPatients':
            return self.listPatients(request)
        elif action == 'addPatients':
            return self.addPatients(request)
        elif action == 'updatePatients':
            return self.updatePatients(request)
        elif action == 'deletePatients':
            return self.deletePatients(request)
        elif action == 'addPic':
            return self.updatePic(request)
        elif action == 'saveReport':
            return self.saveReport(request)
        else:
            return JsonResponse({'code': 500, 'msg': 'action参数错误'})

    def saveReport(self, request):
        newdata = request.pd.get('data')
        newdata = newdata['id']
        res = Patient.saveReport(newdata)
        return JsonResponse(res)

    def updatePic(self, request):
        # 解析出newdata
        newdata = request.pd.get('data')
        # 解析出ID
        uid = newdata['patientid']
        # 去更新
        res = Patient.updatePic(uid, newdata)
        return JsonResponse(res)

    # 获取所有的患者信息
    def listPatients(self, request):
        # 当前第几页
        pagenum = int(request.pd.get('pageNum'))
        # 这一页一共要多少行
        pagesize = int(request.pd.get('pageSize'))
        # 模糊查询的键： bookname：书名、type：类型、author：作者、isbn：ISBN
        key = request.pd.get('key')
        # 模糊查询的值
        value = request.pd.get('value')
        res = Patient.listPatients(pagenum, pagesize, key, value)
        return JsonResponse(res)

    # 添加患者
    def addPatients(self, request):
        # 获取request请求体中的data
        data = request.pd.get('data')
        res = Patient.addPatients(data)

        return JsonResponse(res)

    # 修改患者
    def updatePatients(self, request):
        # 解析出newdata
        newdata = request.pd.get('newdata')
        # 解析出id
        uid = newdata['id']
        # 去更新
        res = Patient.updatePatients(uid, newdata)
        return JsonResponse(res)

    # 删除患者
    def deletePatients(self, request):
        data = request.pd.get('id')
        res = Patient.deletePatients(data)
        return JsonResponse(res)

    # 上传Excel文件
    def upload(self, request):
        # 获取request中的file文件
        file = request.FILES.get('file')
        # 拿到文件名 和 时间戳去拼接  (1655120584批量插入图书-模板.xlsx)
        filename = str(int(time.time())) + file.name
        # 写入文件
        dest = open("./excel模板/" + filename, 'wb+')
        for chunk in file.chunks():  # 分块写入文件
            dest.write(chunk)
        # 关闭
        dest.close()
        # 用xlrd2 打开这个文件
        workbook = xlrd2.open_workbook("./excel模板/" + filename)
        # 选中单元格的表
        sheet = workbook.sheet_by_name('批量插入')
        # 这个新建一个空的数组
        bookList = list()
        # sheet.nrows 当前表共有多少行
        for i in range(sheet.nrows):
            if i > 6:
                # 实例化对象 相当于new books()
                obj = Patient()
                obj.bookname = sheet.cell(i, 0).value
                obj.author = sheet.cell(i, 1).value
                obj.press = sheet.cell(i, 2).value
                # 日期 将时间戳转换成日期 年 月
                obj.time = sheet.cell(i, 3).value
                obj.type = sheet.cell(i, 4).value
                obj.isbn = sheet.cell(i, 5).value
                bookList.append(obj)
        # 批量添加
        Patient.objects.bulk_create(bookList)
        return JsonResponse({'code': 200, 'msg': "成功"})


# 诊断管理的类
class DiagnosisManage:
    def handle(self, request):

        # 判断是否为GET请求
        if request.method == 'GET':
            pd = request.GET
        else:
            pd = json.loads(request.body)

        request.pd = pd
        action = pd.get('action')

        if action == 'readlist':
            return self.readlist(request)
        elif action == 'reqDiagnosis':
            return self.reqDiagnosis(request)
        elif action == 'readPatient':
            return self.readPatient(request)
        elif action == 'returnPatient':
            return self.returnPatient(request)
        elif action == 'addPic':
            return self.update(request)
        elif action == 'Diagnosis':
            return self.diagnosis(request)
        elif action == 'chat':
            return self.chat(request)
        else:
            return JsonResponse({'code': 500, 'msg': 'action参数错误'})

    def chat(self, request):
        data = request.pd.get('data')
        inputmsg = data['input']
        dia = data['diares']
        print(inputmsg)
        res = diagnosisPatient.Chat(inputmsg, dia)
        return JsonResponse(res)

    def diagnosis(self, request):
        newdata = request.pd.get('data')
        diagnosisTime = newdata['diagnosisTime']
        picName = newdata['picName']
        res = diagnosisPatient.Diagnosis(diagnosisTime, picName)
        print("Server response:", res)
        return JsonResponse(res)

    def update(self, request):
        # 解析出newdata
        newdata = request.pd.get('data')
        # 解析出id
        uid = newdata['diagnosisTime']
        # 去更新
        res = diagnosisPatient.updateDPic(uid, newdata)
        return JsonResponse(res)

    # 获取自己所有的诊断信息
    def readlist(self, request):
        pagenum = int(request.pd.get('pageNum'))
        pagesize = int(request.pd.get('pageSize'))
        # 逻辑是 当前账号下的所有的诊断信息
        token = request.COOKIES.get('vue_admin_template_token')

        # 解密token
        if token:
            username = jwt.decode(token, "ukc8BDbRigUDaY6pZFfWus2jZWLPHO", algorithms=["HS256"])
            res = diagnosisPatient.diagnosispatient(pagenum, pagesize, username['username'])
            return JsonResponse(res)
        return JsonResponse({'code': 500, 'msg': '会话过期了'})

    def reqDiagnosis(self, request):
        # 当前第几页
        pagenum = int(request.pd.get('pageNum'))
        # 这一页一共要多少行
        pagesize = int(request.pd.get('pageSize'))
        patientID = str(request.pd.get('patientID'))
        res = diagnosisPatient.reqDiagnosis(patientID, pagenum, pagesize)
        return JsonResponse(res)

    # 诊断病人
    def readPatient(self, request):
        data = request.pd.get('data')
        token = request.COOKIES.get('vue_admin_template_token')
        if token:
            username = jwt.decode(token, "ukc8BDbRigUDaY6pZFfWus2jZWLPHO", algorithms=["HS256"])
            res = diagnosisPatient.addDiagnosisPatient(data, username['username'])
            return JsonResponse(res)

        return JsonResponse({'code': 500, 'msg': '会话过期了'})

    # 完成诊断
    def returnPatient(self, request):
        id = request.pd.get('data')
        res = diagnosisPatient.returndiagnosis(id)
        return JsonResponse(res)


# 人员流动的类
class flowManage:

    def handle(self, request):
        # 判断是否为GET请求
        if request.method == 'GET':
            pd = request.GET
        else:
            pd = json.loads(request.body)

        request.pd = pd
        action = pd.get('action')

        if action == 'doctorFlows':
            return self.listFlows(request)
        elif action == 'addFlows':
            return self.addFlow(request)
        elif action == 'deleteFlows':
            return self.deleteFlow(request)
        else:
            return JsonResponse({'code': 500, 'msg': 'action参数错误'})

    # 获取医生流动信息
    def listFlows(self, request):
        # 当前第几页
        pagenum = int(request.pd.get('pageNum'))
        # 这一页一共要多少行
        pagesize = int(request.pd.get('pageSize'))
        searchID = str(request.pd.get('searchID'))
        res = flow.doctorFlow(searchID, pagenum, pagesize)

        return JsonResponse(res)

    # 添加记录
    def addFlow(self, request):
        data = request.pd.get('data')
        res = flow.addFlow(data)
        return JsonResponse(res)

    # 删除记录
    def deleteFlow(self, request):
        data = request.pd.get('data')
        data = data['id']
        res = flow.deleteFlow(data)
        return JsonResponse(res)


# 投诉记录的类
class complaintManage:

    def handle(self, request):
        # 判断是否为GET请求
        if request.method == 'GET':
            pd = request.GET
        else:
            pd = json.loads(request.body)

        request.pd = pd
        action = pd.get('action')

        if action == 'addComplaints':
            return self.addComplaint(request)
        elif action == 'listComplaints':
            return self.listComplaints(request)
        elif action == 'deleteComplaints':
            return self.deleteComplaint(request)
        elif action == 'updateComplaints':
            return self.updateComplaint(request)
        else:
            return JsonResponse({'code': 500, 'msg': 'action参数错误'})

    def listComplaints(self, request):
        # 当前第几页
        pagenum = int(request.pd.get('pageNum'))
        # 这一页一共要多少行
        pagesize = int(request.pd.get('pageSize'))
        searchName = str(request.pd.get('searchName'))
        res = complaint.Complaint(searchName, pagenum, pagesize)
        return JsonResponse(res)

    # 添加
    def addComplaint(self, request):
        data = request.pd.get('data')
        res = complaint.addComplait(data)
        return JsonResponse(res)

    # 删除
    def deleteComplaint(self, request):
        data = request.pd.get('data')
        data = data['id']
        res = complaint.deleteComplait(data)
        return JsonResponse(res)

    # 更新
    def updateComplaint(self, request):
        # 获取newdata中的数据
        newdata = request.pd.get('newdata')
        # 从newdata中获取id
        complaintID = newdata['id']
        res = complaint.updateComplait(complaintID, newdata)
        return JsonResponse(res)


# 值班安排
class dutyManage:

    def handle(self, request):
        # 判断是否为GET请求
        if request.method == 'GET':
            pd = request.GET
        else:
            pd = json.loads(request.body)

        request.pd = pd
        action = pd.get('action')

        if action == 'listDuties':
            return self.listDuties(request)
        elif action == 'addDuty':
            return self.addDuty(request)
        elif action == 'deleteDuty':
            return self.deleteOneDuty(request)
        elif action == 'deleteAll':
            return self.deleteAll(request)
        elif action == 'updateDuty':
            return self.updateDuty(request)
        else:
            return JsonResponse({'code': 500, 'msg': 'action参数错误'})

    # 查询排班记录
    def listDuties(self, request):
        # 当前第几页
        pagenum = int(request.pd.get('pageNum'))
        # 这一页一共要多少行
        pagesize = int(request.pd.get('pageSize'))
        searchName = str(request.pd.get('searchName'))
        res = duty.doctorDuty(searchName, pagenum, pagesize)
        return JsonResponse(res)

    # 添加
    def addDuty(self, request):
        data = request.pd.get('data')
        res = duty.addDuty(data)
        return JsonResponse(res)

    # 删除一个
    def deleteOneDuty(self, request):
        data = request.pd.get('data')
        data = data['id']
        res = duty.deleteDuty(data)
        return JsonResponse(res)

    # 删除全部
    def deleteAll(self, request):
        res = duty.deleteAllDuties()
        return JsonResponse(res)

    # 更新
    def updateDuty(self, request):
        # 获取newdata中的数据
        newdata = request.pd.get('newdata')
        # 从newdata中获取id
        dutyID = newdata['id']
        res = duty.updateDuty(dutyID, newdata)
        return JsonResponse(res)
