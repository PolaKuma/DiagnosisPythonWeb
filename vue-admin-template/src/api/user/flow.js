import request from '@/utils/request'

export const addFlow = (data) => request({
  url: `api/flows`,
  method: 'post',
  data: { 'action': 'addFlows', 'data': data }
})

export const findFlow = (pageNum, pageSize, searchID) => request({
  url: `api/flows`,
  method: 'post',
  data: { 'action': 'doctorFlows', 'pageNum': pageNum, 'pageSize': pageSize, 'searchID': searchID }
})

export const delFlow = (ID) => request({
  url: `api/flows`,
  method: 'post',
  data: { 'action': 'addFlows', 'data': { 'id': ID }}
})

export const addCompaints = (data) => request({
  url: `api/complaints`,
  method: 'post',
  data: { 'action': 'addComplaints', 'data': data }
})

export const updateCompaints = (data) => request({
  url: `api/complaints`,
  method: 'post',
  data: { 'action': 'updateComplaints', 'data': data }
})

export const delCompaints = (ID) => request({
  url: `api/flows`,
  method: 'post',
  data: { 'action': 'deleteComplaints', 'data': { 'id': ID }}
})

export const add_Duty = (data) => request({
  url: `api/duties`,
  method: 'post',
  data: { 'action': 'addDuty', 'data': data }
})

export const findDuty = (pageNum, pageSize, searchName) => request({
  url: `api/duties`,
  method: 'post',
  data: { 'action': 'listDuties', 'pageNum': pageNum, 'pageSize': pageSize, 'searchName': searchName }
})

export const update_Duty = (data) => request({
  url: `api/duties`,
  method: 'post',
  data: { 'action': 'updateDuty', 'newdata': data }
})

export const delDuty = (ID) => request({
  url: `api/duties`,
  method: 'post',
  data: { 'action': 'deleteDuty', 'data': { 'id': ID }}
})

export const delAllDuty = () => request({
  url: `api/duties`,
  method: 'post',
  data: { 'action': 'deleteAll' }
})
