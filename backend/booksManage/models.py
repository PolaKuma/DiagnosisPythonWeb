from django.db import models
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage

import traceback
import datetime


# 书的类
class Patient(models.Model):
    # 病例号
    id = models.BigAutoField(primary_key=True)

    # 患者姓名
    patientName = models.CharField(max_length=255, null=False)

    # 分类
    type = models.CharField(max_length=30)

    # 性别
    patientSex = models.CharField(max_length=30)

    # 年龄
    patientAge = models.CharField(max_length=30)

    # 体重
    patientWeight = models.CharField(max_length=30)

    # 书号
    report = models.CharField(max_length=255, null=False)

    # 诊治医生
    doctor = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "patients"

    # 分页模糊查询
    @staticmethod
    def listBooks(pagenum, pagesize, key, value):
        try:
            # .order_by('-id') 表示按照 id字段的值 倒序排列
            # 这样可以保证最新的记录显示在最前面
            if value:
                if key == 'author':
                    # icontains是模糊查询 相当于SQL中的like，value.strip()把value中的值的两边的空格都删掉，而且按照id倒叙排列
                    qs = Patient.objects.filter(doctor__icontains=value.strip()).values().order_by('-id')
                if key == 'bookname':
                    qs = Patient.objects.filter(patientName__icontains=value.strip()).values().order_by('-id')
                if key == 'type':
                    qs = Patient.objects.filter(type__icontains=value.strip()).values().order_by('-id')
                if key == 'isbn':
                    qs = Patient.objects.filter(report__icontains=value.strip()).values().order_by('-id')
            else:
                # value没有值的话，那么就把所有的都查出来
                qs = Patient.objects.values().order_by('-id')

            # 使用分页对象，设定每页多少条记录
            pgnt = Paginator(qs, pagesize)

            # 从数据库中读取数据，指定读取其中第几页
            page = pgnt.page(pagenum)
            # 将 QuerySet 对象 转化为 list 类型
            retlist = list(page)

            # total指定了 一共有多少数据
            return {'code': 200, 'msg': retlist, 'total': pgnt.count}
        except EmptyPage:
            return {'code': 200, 'msg': [], 'total': 0}
        except:
            return {'code': 500, 'msg': f'未知错误\n {traceback.format_exc()} '}

    @staticmethod
    def addBooks(data):
        if Patient.objects.filter(id=data['caseid']).exists():
            return {'code': 500, 'msg': f"病人 {data['caseid']} 已存在"}
        try:
            # 否则去新建
            patients = Patient.objects.create(
                id=data['caseid'],
                patientName=data['patientName'],
                doctor=data['doctor'],
                type=data['type'],
                patientWeight=data['patientWeight'],
                patientAge=data['patientAge'],
                report=data['report'],
            )
            return {'code': 200, 'msg': patients.id}
        except:
            err = traceback.format_exc()
            return {'code': 500, 'msg': err}

    # 更新book方法
    @staticmethod
    def updateBooks(uid, newdata):
        try:
            book = Patient.objects.get(id=uid)
            if Patient.objects.filter(~Q(id=uid),report=newdata['id']):
                return {'code': 500, 'msg': f'ISBN  {newdata["id"]}  已存在，不可重复'}

            # items是字典形式便利出来key 和 value
            # setattr是赋值
            for fileid, value in newdata.items():
                setattr(book, fileid, value)
            book.save()

            return {'code': 200, 'msg': book.id}
        except Patient.DoesNotExist:
            return {'code': 500, 'msg': f'id为 {uid} 的用户不存在'}
        except:
            err = traceback.format_exc()
            return {'code': 500, 'msg': err}

    @staticmethod
    def deleteBooks(data):
        try:
            user = Patient.objects.filter(id=data)
            user.delete()
            return {'code': 200, 'msg': "删除成功"}
        except Patient.DoesNotExist:
            return {'code': 500, 'msg': f'id为 {data} 的用户不存在'}
        except:
            err = traceback.format_exc()
            return {'code': 500, 'msg': err}


# 借书的类
class readBook(models.Model):
    id = models.BigAutoField(primary_key=True)

    # 借阅者用户名
    readname = models.CharField(max_length=255, null=True)

    # 书id
    bookid = models.CharField(max_length=30, null=True)

    # 书名称
    bookname = models.CharField(max_length=255, null=True)

    # 借阅时间
    readtime = models.CharField(max_length=100, null=True, blank=True)

    # 归还时间
    returntime = models.CharField(max_length=200)

    class Meta:
        db_table = "book_read"

    @staticmethod
    def readbook(pagenum, pagesize, username):
        try:
            # 要获取的第几页 rf 下所有的借阅信息读取出来 找到后按照时间正序排列
            qs = readBook.objects.filter(readname=username).values().order_by('returntime')
            # 使用分页对象，设定每页多少条记录
            pgnt = Paginator(qs, pagesize)

            # 从数据库中读取数据，指定读取其中第几页
            page = pgnt.page(pagenum)
            # 将 QuerySet 对象 转化为 list 类型
            retlist = list(page)

            # total指定了 一共有多少数据
            return {'code': 200, 'msg': retlist, 'total': pgnt.count}
        except EmptyPage:
            return {'code': 200, 'msg': [], 'total': 0}
        except:
            return {'code': 500, 'msg': f'未知错误\n {traceback.format_exc()} '}

    @staticmethod
    def addReadBook(data, username):

        try:
            # 生成时间 是以 2022年06月13日 19:49:32 生成的
            current_time = datetime.datetime.now().strftime('%Y{y}%m{m}%d{d} %H{h}%M{f}%S{s}').format(y='年', m='月', d='日', h='时', f='分', s='秒')
            # 创建
            user = readBook.objects.create(
                readname=username,
                bookid=data['bookid'],
                bookname=data['bookname'],
                readtime=current_time
            )
            return {'code': 200, 'msg': user.id}
        except:
            err = traceback.format_exc()
            return {'code': 500, 'msg': err}

    @staticmethod
    def returnbook(id):
        # 获取当前时间
        #current_time = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
        current_time = datetime.datetime.now().strftime('%Y{y}%m{m}%d{d} %H{h}%M{f}%S{s}').format(y='年', m='月', d='日', h='时', f='分', s='秒')
        try:
            book = readBook.objects.get(id=id)
            # 如果借阅信息不存在则报错500
        except readBook.DoesNotExist:
            return {
                'ret': 500,
                'msg': f'id 为 `{id}` 的借阅信息不存在'
            }
        book.returntime = current_time
        book.save()

        return {'code': 200}
