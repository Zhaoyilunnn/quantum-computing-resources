OPENQASM 2.0;
include "qelib1.inc";
qreg q[30];
h q[0];
h q[1];
cp(167*pi) q[0],q[1];
h q[2];
cp(189*pi) q[0],q[2];
h q[3];
cp(-1474.9778) q[0],q[3];
h q[4];
cp(-15*pi/2) q[0],q[4];
cp(-1481.2609) q[1],q[4];
cp(181*pi) q[2],q[4];
h q[5];
cp(337*pi) q[2],q[5];
cp(-1145.1105) q[3],q[5];
h q[6];
cp(461*pi) q[0],q[6];
cp(-240.33184) q[2],q[6];
cp(257*pi) q[4],q[6];
cp(174.35839) q[5],q[6];
h q[7];
cp(-103*pi) q[0],q[7];
cp(-400.55306) q[1],q[7];
cp(362.85395) q[3],q[7];
cp(133.51769) q[4],q[7];
cp(-351*pi) q[6],q[7];
h q[8];
cp(-1292.7654) q[0],q[8];
cp(-253*pi) q[2],q[8];
cp(1588.0751) q[5],q[8];
cp(-101*pi) q[6],q[8];
h q[9];
cp(-45.553093) q[1],q[9];
cp(-171.2168) q[2],q[9];
cp(1264.491) q[4],q[9];
cp(501.08403) q[6],q[9];
cp(239*pi) q[7],q[9];
cp(-479*pi) q[8],q[9];
h q[10];
cp(1236.2167) q[0],q[10];
cp(-347*pi) q[3],q[10];
cp(397*pi) q[4],q[10];
cp(-504.22562) q[5],q[10];
cp(1415.2875) q[6],q[10];
cp(-1361.8804) q[7],q[10];
cp(771.261) q[8],q[10];
cp(-893.78311) q[9],q[10];
h q[11];
cp(234.04865) q[0],q[11];
cp(-1506.3937) q[1],q[11];
cp(-306.30528) q[2],q[11];
cp(1409.0043) q[4],q[11];
cp(865.50878) q[5],q[11];
cp(557.6327) q[8],q[11];
cp(83*pi) q[9],q[11];
h q[12];
cp(1054.0043) q[1],q[12];
cp(-177*pi) q[2],q[12];
cp(-824.66807) q[3],q[12];
cp(-271.74776) q[5],q[12];
cp(473*pi) q[6],q[12];
cp(-1176.5264) q[7],q[12];
cp(-477*pi) q[9],q[12];
cp(466.52651) q[10],q[12];
h q[13];
cp(-1220.5087) q[0],q[13];
cp(-1496.9689) q[1],q[13];
cp(-365*pi) q[2],q[13];
cp(21*pi) q[4],q[13];
cp(1474.9778) q[5],q[13];
cp(-1424.7123) q[6],q[13];
cp(443*pi) q[7],q[13];
cp(-620.46455) q[8],q[13];
cp(-55*pi) q[9],q[13];
cp(-1449.845) q[12],q[13];
h q[14];
cp(394.26988) q[0],q[14];
cp(-411*pi) q[1],q[14];
cp(57*pi) q[2],q[14];
cp(1261.3495) q[3],q[14];
cp(431.96899) q[5],q[14];
cp(385*pi) q[6],q[14];
cp(-457*pi) q[7],q[14];
cp(-463*pi) q[9],q[14];
cp(174.35839) q[10],q[14];
cp(-328.29643) q[12],q[14];
h q[15];
cp(451*pi) q[0],q[15];
cp(636.17251) q[1],q[15];
cp(155*pi) q[2],q[15];
cp(333*pi) q[5],q[15];
cp(-227*pi) q[6],q[15];
cp(-279*pi) q[8],q[15];
cp(-1512.6769) q[9],q[15];
cp(541.92473) q[11],q[15];
cp(1185.9512) q[12],q[15];
cp(680.15481) q[13],q[15];
cp(273*pi) q[14],q[15];
h q[16];
cp(1305.3317) q[2],q[16];
cp(-1041.438) q[3],q[16];
cp(-124.09291) q[5],q[16];
cp(129*pi) q[7],q[16];
cp(152.36724) q[8],q[16];
cp(-629.88933) q[9],q[16];
cp(-349*pi) q[10],q[16];
cp(161.79202) q[11],q[16];
cp(1242.4999) q[12],q[16];
cp(683.2964) q[13],q[16];
cp(155.50884) q[14],q[16];
cp(63*pi) q[15],q[16];
h q[17];
cp(39.269908) q[2],q[17];
cp(-479*pi) q[3],q[17];
cp(488.51766) q[4],q[17];
cp(1242.4999) q[7],q[17];
cp(77*pi) q[8],q[17];
cp(-325*pi) q[9],q[17];
cp(489*pi) q[10],q[17];
cp(36.128316) q[11],q[17];
cp(400.55306) q[13],q[17];
cp(1185.9512) q[14],q[17];
h q[18];
cp(-57*pi) q[0],q[18];
cp(95*pi) q[1],q[18];
cp(-377*pi) q[2],q[18];
cp(900.0663) q[3],q[18];
cp(922.05744) q[4],q[18];
cp(65*pi) q[5],q[18];
cp(113*pi) q[6],q[18];
cp(-1035.1548) q[9],q[18];
cp(-333*pi) q[10],q[18];
cp(-285*pi) q[11],q[18];
cp(-275*pi) q[12],q[18];
cp(-443*pi) q[13],q[18];
cp(-151*pi) q[14],q[18];
cp(-1107.4114) q[15],q[18];
cp(-639.31411) q[16],q[18];
cp(1242.4999) q[17],q[18];
h q[19];
cp(972.32293) q[0],q[19];
cp(-852.94241) q[2],q[19];
cp(-1223.6503) q[3],q[19];
cp(-234.04865) q[4],q[19];
cp(-256.0398) q[5],q[19];
cp(-1185.9512) q[6],q[19];
cp(423*pi) q[7],q[19];
cp(-234.04865) q[9],q[19];
cp(-1355.5972) q[14],q[19];
cp(429*pi) q[15],q[19];
cp(1025.73) q[16],q[19];
cp(-131*pi) q[17],q[19];
cp(339*pi) q[18],q[19];
h q[20];
cp(-677.01322) q[0],q[20];
cp(-331.43802) q[1],q[20];
cp(-115*pi) q[2],q[20];
cp(-1396.4379) q[3],q[20];
cp(431*pi) q[4],q[20];
cp(-67*pi) q[5],q[20];
cp(699.00437) q[6],q[20];
cp(-1283.3406) q[7],q[20];
cp(-925.19904) q[9],q[20];
cp(340.8628) q[11],q[20];
cp(-92.676983) q[12],q[20];
cp(-758.69463) q[13],q[20];
cp(1399.5795) q[14],q[20];
cp(-11*pi) q[15],q[20];
cp(1233.0751) q[16],q[20];
cp(1465.553) q[17],q[20];
cp(441.39377) q[18],q[20];
cp(-475*pi) q[19],q[20];
h q[21];
cp(-1559.8008) q[0],q[21];
cp(683.2964) q[1],q[21];
cp(507*pi) q[2],q[21];
cp(1321.0397) q[4],q[21];
cp(-195*pi) q[5],q[21];
cp(-535.64155) q[6],q[21];
cp(-243.47343) q[7],q[21];
cp(-1189.0928) q[8],q[21];
cp(1588.0751) q[9],q[21];
cp(1427.8539) q[10],q[21];
cp(193*pi) q[11],q[21];
cp(-821.52648) q[13],q[21];
cp(-142.94247) q[14],q[21];
cp(-400.55306) q[15],q[21];
cp(783.82737) q[16],q[21];
cp(351*pi) q[18],q[21];
cp(-645.59729) q[19],q[21];
cp(830.95126) q[20],q[21];
h q[22];
cp(1581.7919) q[1],q[22];
cp(153*pi) q[2],q[22];
cp(-171*pi) q[3],q[22];
cp(868.65037) q[4],q[22];
cp(1559.8008) q[5],q[22];
cp(328.29643) q[6],q[22];
cp(-93*pi) q[7],q[22];
cp(-774.40259) q[8],q[22];
cp(856.084) q[10],q[22];
cp(1097.9866) q[12],q[22];
cp(-724.13711) q[14],q[22];
cp(821.52648) q[16],q[22];
cp(83.252205) q[17],q[22];
cp(253*pi) q[18],q[22];
cp(-1462.4114) q[19],q[22];
cp(-25*pi) q[20],q[22];
cp(567.05747) q[21],q[22];
h q[23];
cp(164.93361) q[0],q[23];
cp(27*pi) q[4],q[23];
cp(501.08403) q[5],q[23];
cp(-1484.4025) q[6],q[23];
cp(-1138.8273) q[7],q[23];
cp(-818.38489) q[8],q[23];
cp(1132.5442) q[10],q[23];
cp(-830.95126) q[11],q[23];
cp(1220.5087) q[13],q[23];
cp(1487.5441) q[14],q[23];
cp(-796.39374) q[15],q[23];
cp(11*pi/2) q[16],q[23];
cp(1028.8716) q[18],q[23];
cp(164.93361) q[19],q[23];
cp(29.84513) q[20],q[23];
cp(-337*pi) q[22],q[23];
h q[24];
cp(1522.1016) q[0],q[24];
cp(-1251.9247) q[1],q[24];
cp(-475.95129) q[2],q[24];
cp(-218.34069) q[3],q[24];
cp(317*pi) q[4],q[24];
cp(-796.39374) q[5],q[24];
cp(133*pi) q[6],q[24];
cp(604.75659) q[7],q[24];
cp(322.01325) q[8],q[24];
cp(-389*pi) q[9],q[24];
cp(211*pi) q[10],q[24];
cp(39.269908) q[11],q[24];
cp(1214.2256) q[12],q[24];
cp(171.2168) q[13],q[24];
cp(790.11055) q[15],q[24];
cp(-365*pi) q[17],q[24];
cp(-466.52651) q[18],q[24];
cp(-1179.668) q[19],q[24];
cp(-49*pi) q[21],q[24];
cp(1233.0751) q[22],q[24];
cp(1358.7388) q[23],q[24];
h q[25];
cp(-617.32296) q[0],q[25];
cp(-1409.0043) q[2],q[25];
cp(752.41144) q[3],q[25];
cp(227.76547) q[5],q[25];
cp(-69*pi) q[6],q[25];
cp(493*pi) q[8],q[25];
cp(-1349.314) q[10],q[25];
cp(296.88051) q[11],q[25];
cp(117*pi) q[12],q[25];
cp(-7*pi/2) q[14],q[25];
cp(-202.63273) q[15],q[25];
cp(1437.2786) q[16],q[25];
cp(-9*pi) q[17],q[25];
cp(1471.8362) q[19],q[25];
cp(724.13711) q[20],q[25];
cp(387*pi) q[24],q[25];
h q[26];
cp(563.91588) q[0],q[26];
cp(65*pi) q[1],q[26];
cp(329*pi) q[4],q[26];
cp(-856.084) q[5],q[26];
cp(680.15481) q[7],q[26];
cp(629.88933) q[8],q[26];
cp(51.836279) q[9],q[26];
cp(1245.6415) q[10],q[26];
cp(362.85395) q[11],q[26];
cp(-485.37606) q[12],q[26];
cp(-523.07518) q[14],q[26];
cp(369.13714) q[17],q[26];
cp(-127*pi) q[18],q[26];
cp(-145*pi) q[21],q[26];
cp(-59*pi) q[22],q[26];
h q[22];
cp(620.46455) q[23],q[26];
cp(61.261057) q[24],q[26];
cp(1016.3052) q[25],q[26];
h q[27];
cp(-507*pi) q[1],q[27];
cp(-1459.2698) q[3],q[27];
p(-280.38714) q[3];
h q[3];
cp(-127.2345) q[4],q[27];
cp(661.30525) q[6],q[27];
cp(375.42032) q[7],q[27];
cp(-1550.376) q[8],q[27];
cp(-403*pi) q[10],q[27];
h q[10];
cp(375*pi) q[11],q[27];
cp(35*pi) q[12],q[27];
p(-124.48561) q[12];
h q[12];
cp(-177.49998) q[13],q[27];
cp(-1135.6857) q[15],q[27];
cp(177*pi) q[16],q[27];
cp(1459.2698) q[18],q[27];
cp(1094.845) q[19],q[27];
cp(-427*pi) q[20],q[27];
cp(461*pi) q[21],q[27];
cp(-51*pi) q[24],q[27];
h q[28];
cp(-1299.0486) q[0],q[28];
cp(-742.98666) q[1],q[28];
cp(425*pi) q[2],q[28];
p(-pi/4) q[2];
h q[2];
cp(-331.43802) q[5],q[28];
cp(369.13714) q[6],q[28];
cp(-297*pi) q[7],q[28];
cp(-179*pi) q[8],q[28];
cp(235*pi) q[11],q[28];
cp(-384.8451) q[14],q[28];
p(78.932515) q[14];
h q[14];
cp(1220.5087) q[15],q[28];
cp(411*pi) q[16],q[28];
cp(419*pi) q[17],q[28];
h q[17];
cp(181*pi) q[19],q[28];
cp(-1182.8096) q[20],q[28];
cp(-469*pi) q[21],q[28];
p(117.41703) q[21];
h q[21];
cp(-345*pi) q[23],q[28];
cp(1531.5264) q[24],q[28];
p(-30.237829) q[24];
h q[24];
cp(818.38489) q[26],q[28];
cp(-714.71233) q[27],q[28];
h q[29];
cp(-567.05747) q[0],q[29];
p(356.17807) q[0];
h q[0];
cp(-692.72118) q[1],q[29];
p(200.27653) q[1];
h q[1];
cp(755.55303) q[4],q[29];
h q[4];
cp(-846.65922) q[5],q[29];
p(-323.19134) q[5];
h q[5];
cp(1430.9955) q[6],q[29];
p(-381.31081) q[6];
h q[6];
cp(415*pi) q[7],q[29];
p(-249.36392) q[7];
h q[7];
cp(290.59732) q[8],q[29];
p(-368.35174) q[8];
h q[8];
cp(-488.51766) q[9],q[29];
cp(427*pi) q[11],q[29];
p(-207.73781) q[11];
h q[11];
cp(1606.9246) q[13],q[29];
p(379.74001) q[13];
h q[13];
cp(-1518.96) q[15],q[29];
p(126.8418) q[15];
h q[15];
cp(343*pi) q[16],q[29];
h q[16];
cp(-730.42029) q[18],q[29];
p(-33.379422) q[18];
h q[18];
cp(667.58844) q[19],q[29];
p(-324.36944) q[19];
h q[19];
cp(1229.9335) q[20],q[29];
p(237.19025) q[20];
h q[20];
cp(365*pi) q[23],q[29];
p(237.58294) q[23];
h q[23];
cp(177*pi) q[25],q[29];
p(184.17587) q[25];
h q[25];
cp(-592.19022) q[26],q[29];
p(245.82963) q[26];
h q[26];
cp(-438.25218) q[27],q[29];
p(105.24335) q[27];
h q[27];
cp(189*pi) q[28],q[29];
h q[28];
p(-330.25993) q[29];
h q[29];
p(77.361719) q[9];
h q[9];