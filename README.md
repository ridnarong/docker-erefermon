# E-Referral Monitor
--------
เป็น docker image สำหรับตรวจสอบสถานะการทำงานของ openvpn และ message queue server โดยภายในจะเริ่มขั้นตอนตรวจสอบดังนี้ 

* เชื่อมต่อ กับ vpn server 
* ping ทดสอบ ไปยังหมายเลข IP ภายในของเครื่อง message queue server
* ถ้า ping สำเร็จจะทดสอบส่งข้อความไปยัง message queue server ผ่าน หมายเลข IP ภายใน
* ถ้าไม่สำเร็จ จะทดสอบส่งข้อความไปยัง message queue server ผ่าน public IP

# Environment variable ที่รองรับ
---
* `AMQP_VPN_HOST` เป็น domain หรือ IP สำหรับ message queue ภายใน ค่า default เป็น 'localhost'
* `AMQP_PUBLIC_HOST` เป็น domain หรือ IP สำหรับ message queue public ค่า default เป็น 'localhost'
* `AMQP_PORT` เป็น port สำหรับ message queue server ค่า default เป็น 5672
* `AMQP_VHOST` เป็น virtual host สำหรับ message queue server ค่า default เป็น '/'
* `AMQP_SSL` เป็น การตั้งค่า ให้ใช้ SSL ในการเชื่อมต่อ message queue server ค่า default เป็น False ค่าที่รองรับคือ 0 สำหรับ False และ 1 สำหรับ True
* `AMQP_USERNAME` เป็น username สำหรับ message queue server ค่า default เป็น 'guest'
* `AMQP_PASSWORD` เป็น password สำหรับ message queue server ค่า default เป็น 'guest'
* `MAKER_ENDPOINT` เป็น endpoint สำหรับบริการ maker ifttt โดยจะส่งข้อความผิดพลาดโดยฟิลด์ `value1` ถ้าไม่ต้องการส่งผ่านไลน์ หรือไม่มีโปรแกรม curl ไม่ต้องใส่
* `VPN_EXE` path ของโปรแกรม openvpn ค่า default เป็น openvpn โดยใน windows อาจจะที่อยู่ของ openvpn.exe
* `OVPN_PATH` path ของไฟล์ ovpn ค่า default เป็น connect.ovpn

# Volume
---
* `/vpn` เป็นโฟลเดอร์ที่ใช้เก็บ ไฟล์ ovpn, key ต่างๆ โดยโปรแกรมจะมองหาไฟล์ connect.ovpn จากโฟลเดอร์นี้ (จำเป็นต้องระบุทุกครั้ง)
* `/app` เป็นโฟลเดอร์ที่ใช้เก็บ โปรแกรมทดสอบ test.py โดยโปรแกรมจะถูกเรียกเมื่อมีการ run docker image

# วิธีการ run
---
```sh
$ docker run -it --rm -e AMQP_VPN_HOST='mqv.e-referral.net' -e AMQP_PUBLIC_HOST='mq.e-referral.net' -e AMQP_USERNAME='tester' -e AMQP_PASSWORD='tester' -e AMQP_VHOST='test' --privileged --cap-add=ALL -v /dev:/dev -v /lib/modules:/lib/modules -v /path/to/vpn:/vpn -e MAKER_ENDPOINT='https://maker.ifttt.com/trigger/alert/with/key/XXXXX' ridnarong/erefermon
```
