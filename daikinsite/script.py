s1 = "insert into "
s2 = "values("
s3 = "'sardar.ankan@grp.daikin.co.jp'"
s4 = "'patrawala.viraf@grp.daikin.co.jp'"
s5 = "'bhatia.vansh@grp.daikin.co.jp'"
s6 = "'senathi.anish@grp.daikin.co.jp'"
s7 = "'ankansardarth@gmail.com'"
s8 = ")"
s9 = "'japan'"
s10 = "'VRV'"

k = 100
l = 500
m = 800
n = 1000
o = 2000
lan = "34.5"
long = "135.6"

m = 800
for i in range(100):
    m += 1
    with open("insert.sql", "a") as myfile:
        myfile.write(s1 + "seinfo " + s2 + "'" + str(m) + "'" + ", " + "'ccc" + str(m) + "'" + ", " + s4 + ", " + "'novice'" + ", " +  lan + ", " + long + ", " + "'3.5'" + s8 + ';\n')
        myfile.close()

m = 800
for i in range(100):
    l += 1
    m += 1
    with open("insert.sql", "a") as myfile:
        myfile.write(s1 + "dealerinfo " + s2 + "'" + str(l) + "'" + ", " + "'bbb" + str(l) + "'" + ", " + s7 + ", " + "'" + str(m) + "'" + ", " +  lan + ", " + long + ", " + s9 + s8 + ';\n')
        myfile.close()
l = 500
for i in range(100):
    k += 1
    d = (l+1)+(i%50)
    with open("insert.sql", "a") as myfile:
        myfile.write(s1 + "customerinfo " + s2 + "'" + str(k) + "'" + ", " + "'aaa" + str(k) + "'" + ", " + s3 + ", " + s10 + ", " + "'04/20/2009', " + "'" + str(d) + "'"  + ", " +  lan + ", " + long + ", " + s9 + s8 + ';\n')
        myfile.close()


for i in range(50):
    n += 1
    with open("insert.sql", "a") as myfile:
        myfile.write(s1 + "analystinfo " + s2 + "'" + str(n) + "'" + ", " + "'ddd" + str(n)  + "'" + ", " + s5 + s8 + ';\n')
        myfile.close()

for i in range(20):
    o += 1
    with open("insert.sql", "a") as myfile:
        myfile.write(s1 + "expertinfo " + s2 + str(o) + ", " + "'eee" + str(o) + "'" + ", " + s6 + s8 + ';\n')
        myfile.close()
