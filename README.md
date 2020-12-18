# ml-autoCandidate

### รับพารามิเตอร์จาก console
```python
argumentList = sys.argv
    predictData(list(map(float, argumentList[1:12])))
```
# Clean Data 
1. Parsing คือ การแจกแจงข้อมูล หรือการใช้หัวข้อของชุดข้อมูล
2. Correcting คือ การแก้ไขข้อมูลที่ผิดพลาด
` หาค่าเฉลี่ย ค่าเบี่ยงเบียนมาตรฐาน หรือ standard deviation หรือ Clustering algorithm  `
3. Standardizing คือ การทำข้อมูลให้เป็นรูปแบบเดียวกัน
` Standard Normal Distribution เรียงข้อมูลให้อยู่ในรูป Normalization หรือ ระฆังคว่ำ` 
4. Duplicate Elimination คือ การลบชุดข้อความซ้ำซ้อนทิ้ง

## การเตรียมข้อมูลสำหรับ
### ข้อมูลต้องแยกความแตกต่างของแต่ละแถวได้ (กำจัดคอลัมน์ที่มีข้อมูลไม่ซ้ำกันเลยออก)
### ไม่ใช้ข้อมูลที่ไม่ซ้ำกันเลย  เพราะไม่มีความสัมพันธ์กันของข้อมูล
### ปรับข้อมูลให้สมดุล
       ` school = 0   # ม.6 `
       ` school = 1   # เทียบเข้า `
### ลดการกระจ่ายของข้อมูล (จัดกลุ่ม)
  ` {A, B+, B} เป็น High, เกรด{C+, C} เป็น Medium และ เกรด {D+, D, F, W, I} เป็น Low  `

![Artboard 1@2x](https://miro.medium.com/max/2400/1*-bqV4YyZtlz9EUxi8levjw.png)
