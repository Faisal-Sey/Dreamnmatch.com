"""
import subprocess

# traverse the info
Id = subprocess.check_output(['systeminfo']).decode('utf-8').split('\n')
new = []

# arrange the string into clear info
for item in Id:
    new.append(str(item.split("\r")[:-1]))

string = str(new)
print(string.replace("[]", ""))



class Statics:
    def mode(self):
        inpts = input("Enter numbers eg: 2,3,4:\n").split(',')
        list1 = list(inpts)
        list_mod = []
        dict = {}
        for val in list1:
            count = list1.count(val)
            dict[val] = count

        vals = list(dict.values())
        sorts = (max(vals))
        for num in dict.keys():
            if dict[num] == sorts:
                list_mod.append(num)

        print(list_mod)

r = Statics()
r.mode()


{'resp': '{"id":383524539,"txRef":"HP2212","orderRef":"URF_MMGH_1615580079663_736835","flwRef":"51907364505595681","redirectUrl":"http://127.0.0","device_fingerprint":"N/A","settlement_to
ken":null,"cycle":"one-time","amount":30,"charged_amount":30.75,"appfee":0.75,"merchantfee":0,"merchantbearsfee":0,"chargeResponseCode":"02","raveRef":null,"chargeResponseMessage":"Transa
ction Pending","authModelUsed":"MOBILEMONEY","currency":"GHS","IP":"::ffff:10.65.248.108","narration":"FashionAlley","status":"failed","modalauditid":"385ac68c6b8613d264976f6afa239bf6","v
bvrespmessage":"N/A","authurl":"NO-URL","vbvrespcode":"N/A","acctvalrespmsg":"Transaction Pending","acctvalrespcode":"02","paymentType":"mobilemoneygh","paymentPlan":null,"paymentPage":nu
ll,"paymentId":"N/A","fraud_status":"ok","charge_type":"normal","is_live":0,"retry_attempt":null,"getpaidBatchId":null,"createdAt":"2021-03-12T20:14:39.000Z","updatedAt":"2021-03-12T20:14
:46.000Z","deletedAt":null,"customerId":231926675,"AccountId":152431,"customer.id":231926675,"customer.phone":"0249141809","customer.fullName":"Anonymous Customer","customer.customertoken
":null,"customer.email":"phaisalsey6@gmail.com","customer.createdAt":"2020-11-10T06:52:47.000Z","customer.updatedAt":"2020-11-10T06:52:47.000Z","customer.deletedAt":null,"customer.Account
Id":152431,"meta":[],"flwMeta":{}}'}

resp[tx_ref]
resp[amount]
resp[customer.phone]
resp[customer.email]
resp["status"]

"""
