OPENQASM 2.0;
include "qelib1.inc";
qreg q[30];
h q[0];
h q[1];
h q[2];
cp(-243*pi) q[1],q[2];
h q[3];
cp(802.67692) q[0],q[3];
cp(-413.11943) q[1],q[3];
h q[4];
cp(-1506.3937) q[0],q[4];
cp(1189.0928) q[3],q[4];
h q[5];
cp(579.62384) q[0],q[5];
cp(-13*pi/2) q[1],q[5];
cp(-1255.0663) q[2],q[5];
cp(-337.72121) q[3],q[5];
cp(-378.56191) q[4],q[5];
h q[6];
cp(281*pi) q[4],q[6];
cp(1465.553) q[5],q[6];
h q[7];
cp(9*pi) q[0],q[7];
cp(-859.22559) q[3],q[7];
cp(395*pi) q[4],q[7];
cp(-69*pi) q[5],q[7];
cp(708.42914) q[6],q[7];
h q[8];
cp(344.0044) q[0],q[8];
cp(488.51766) q[1],q[8];
cp(-526.21677) q[3],q[8];
cp(-193.20795) q[4],q[8];
cp(-702.14596) q[5],q[8];
cp(-421*pi) q[6],q[8];
cp(849.80081) q[7],q[8];
h q[9];
cp(724.13711) q[0],q[9];
cp(-239*pi) q[3],q[9];
cp(482.23447) q[6],q[9];
cp(-793.25215) q[8],q[9];
h q[10];
cp(749.26985) q[0],q[10];
cp(655.02207) q[1],q[10];
cp(-1185.9512) q[2],q[10];
cp(771.261) q[3],q[10];
cp(-620.46455) q[5],q[10];
cp(937.76541) q[6],q[10];
cp(-1399.5795) q[7],q[10];
cp(1324.1813) q[8],q[10];
cp(31*pi) q[9],q[10];
h q[11];
cp(-925.19904) q[0],q[11];
cp(576.48225) q[1],q[11];
cp(-677.01322) q[2],q[11];
cp(-447*pi) q[3],q[11];
cp(-1500.1105) q[4],q[11];
cp(111.52654) q[6],q[11];
cp(-179*pi) q[8],q[11];
cp(-179*pi) q[10],q[11];
h q[12];
cp(-1035.1548) q[2],q[12];
cp(427*pi) q[4],q[12];
cp(451*pi) q[6],q[12];
cp(-1094.845) q[7],q[12];
cp(1170.2433) q[8],q[12];
cp(1072.8539) q[9],q[12];
cp(-1471.8362) q[11],q[12];
h q[13];
cp(103*pi) q[0],q[13];
cp(-501.08403) q[1],q[13];
cp(-337.72121) q[2],q[13];
cp(146.08406) q[3],q[13];
cp(164.93361) q[4],q[13];
cp(-413*pi) q[5],q[13];
cp(-92.676983) q[6],q[13];
cp(1377.5884) q[7],q[13];
cp(199.49113) q[10],q[13];
cp(-217*pi) q[12],q[13];
h q[14];
cp(1267.6326) q[0],q[14];
cp(387*pi) q[1],q[14];
cp(1154.5353) q[2],q[14];
cp(1368.1636) q[6],q[14];
cp(-17*pi) q[7],q[14];
cp(389*pi) q[9],q[14];
cp(71*pi) q[10],q[14];
cp(-1119.9778) q[11],q[14];
cp(429*pi) q[12],q[14];
cp(-195*pi) q[13],q[14];
h q[15];
cp(135*pi) q[0],q[15];
cp(95.818576) q[1],q[15];
cp(-928.34063) q[2],q[15];
cp(896.9247) q[3],q[15];
cp(83*pi) q[4],q[15];
cp(127*pi) q[5],q[15];
cp(387.98669) q[6],q[15];
cp(1437.2786) q[7],q[15];
cp(493*pi) q[8],q[15];
cp(241*pi) q[9],q[15];
cp(560.77429) q[10],q[15];
cp(-1481.2609) q[11],q[15];
cp(915.77426) q[12],q[15];
cp(-501*pi) q[13],q[15];
cp(269*pi) q[14],q[15];
h q[16];
cp(136.65928) q[0],q[16];
cp(1088.5619) q[1],q[16];
cp(1292.7654) q[2],q[16];
cp(-1305.3317) q[3],q[16];
cp(-912.63267) q[5],q[16];
cp(-1302.1902) q[7],q[16];
cp(255*pi) q[8],q[16];
cp(441*pi) q[10],q[16];
cp(-758.69463) q[11],q[16];
cp(-293*pi) q[14],q[16];
cp(-3*pi) q[15],q[16];
h q[17];
cp(1063.4291) q[0],q[17];
cp(-405*pi) q[1],q[17];
cp(444.53536) q[2],q[17];
cp(-705.28755) q[4],q[17];
cp(1104.2698) q[5],q[17];
cp(-466.52651) q[6],q[17];
cp(225*pi) q[7],q[17];
cp(80.110613) q[9],q[17];
cp(812.1017) q[10],q[17];
cp(1490.6857) q[11],q[17];
cp(-337.72121) q[13],q[17];
cp(488.51766) q[14],q[17];
cp(114.66813) q[15],q[17];
cp(196.34954) q[16],q[17];
h q[18];
cp(35*pi) q[1],q[18];
cp(-614.18136) q[2],q[18];
cp(-65*pi) q[3],q[18];
cp(-265*pi) q[4],q[18];
cp(-13*pi/2) q[5],q[18];
cp(-560.77429) q[6],q[18];
cp(-1569.2255) q[7],q[18];
cp(483*pi) q[8],q[18];
cp(-343*pi) q[11],q[18];
cp(-1157.6769) q[12],q[18];
cp(180.64158) q[13],q[18];
cp(413.11943) q[14],q[18];
cp(-237*pi) q[15],q[18];
cp(1025.73) q[16],q[18];
h q[19];
cp(-247*pi) q[0],q[19];
cp(-1305.3317) q[1],q[19];
cp(-375.42032) q[2],q[19];
cp(227.76547) q[3],q[19];
cp(-29.84513) q[4],q[19];
cp(67.544242) q[6],q[19];
cp(978.60611) q[10],q[19];
cp(-7*pi/2) q[11],q[19];
cp(714.71233) q[12],q[19];
cp(-205.77432) q[13],q[19];
cp(1418.4291) q[14],q[19];
cp(918.91585) q[15],q[19];
cp(83.252205) q[16],q[19];
cp(903.20789) q[18],q[19];
h q[20];
cp(371*pi) q[0],q[20];
cp(171*pi) q[1],q[20];
cp(262.32299) q[2],q[20];
cp(-519.93358) q[5],q[20];
cp(-1396.4379) q[6],q[20];
cp(253*pi) q[7],q[20];
cp(849.80081) q[8],q[20];
cp(1603.783) q[10],q[20];
cp(488.51766) q[11],q[20];
cp(284.31414) q[12],q[20];
cp(-15*pi) q[13],q[20];
cp(-1273.9158) q[14],q[20];
cp(821.52648) q[15],q[20];
cp(1041.438) q[16],q[20];
h q[21];
cp(-1500.1105) q[1],q[21];
cp(1217.3672) q[3],q[21];
cp(-535.64155) q[4],q[21];
cp(-39.269908) q[5],q[21];
cp(-695.86277) q[6],q[21];
cp(-1217.3672) q[7],q[21];
cp(-77*pi) q[8],q[21];
cp(1584.9335) q[9],q[21];
cp(959.75656) q[10],q[21];
cp(-1258.2079) q[11],q[21];
cp(161.79202) q[12],q[21];
cp(-1041.438) q[13],q[21];
cp(196.34954) q[14],q[21];
cp(-11*pi) q[15],q[21];
cp(1481.2609) q[16],q[21];
cp(441*pi) q[18],q[21];
cp(27*pi) q[19],q[21];
cp(-387*pi) q[20],q[21];
h q[22];
cp(-805.81852) q[0],q[22];
cp(925.19904) q[2],q[22];
cp(761.83622) q[3],q[22];
cp(893.78311) q[5],q[22];
cp(-190.06636) q[7],q[22];
cp(17*pi) q[8],q[22];
cp(-796.39374) q[9],q[22];
cp(153*pi) q[10],q[22];
cp(-409*pi) q[11],q[22];
cp(-271.74776) q[12],q[22];
cp(299*pi) q[13],q[22];
cp(-306.30528) q[14],q[22];
cp(1214.2256) q[15],q[22];
cp(1493.8273) q[16],q[22];
cp(-950.33178) q[17],q[22];
cp(739.84507) q[18],q[22];
cp(363*pi) q[19],q[22];
cp(-283*pi) q[21],q[22];
h q[23];
cp(-129*pi) q[0],q[23];
cp(-63*pi) q[1],q[23];
cp(191*pi) q[3],q[23];
cp(323*pi) q[4],q[23];
cp(799.53533) q[5],q[23];
cp(-395*pi) q[6],q[23];
cp(900.0663) q[7],q[23];
cp(-742.98666) q[8],q[23];
cp(1553.5176) q[9],q[23];
cp(-437*pi) q[10],q[23];
cp(305*pi) q[12],q[23];
cp(-1449.845) q[13],q[23];
cp(-451*pi) q[15],q[23];
cp(761.83622) q[16],q[23];
cp(256.0398) q[18],q[23];
cp(1223.6503) q[20],q[23];
cp(29*pi) q[21],q[23];
cp(-86.393798) q[22],q[23];
h q[24];
cp(263*pi) q[0],q[24];
cp(843.51763) q[3],q[24];
cp(-120.95132) q[4],q[24];
cp(15*pi/2) q[5],q[24];
cp(-409.97784) q[7],q[24];
cp(-824.66807) q[8],q[24];
cp(-1239.3583) q[10],q[24];
cp(-357*pi) q[11],q[24];
cp(-1500.1105) q[12],q[24];
cp(221.48228) q[13],q[24];
cp(-307*pi) q[16],q[24];
cp(142.94247) q[17],q[24];
cp(786.96896) q[18],q[24];
cp(99*pi) q[20],q[24];
cp(1060.2875) q[22],q[24];
cp(1434.137) q[23],q[24];
h q[25];
cp(193*pi) q[0],q[25];
cp(165*pi) q[1],q[25];
cp(881.21674) q[2],q[25];
cp(152.36724) q[3],q[25];
cp(95*pi) q[4],q[25];
cp(-217*pi) q[5],q[25];
cp(-991.17248) q[6],q[25];
cp(764.97781) q[7],q[25];
cp(1154.5353) q[8],q[25];
cp(-1343.0309) q[9],q[25];
cp(-516.79199) q[10],q[25];
cp(313*pi) q[11],q[25];
cp(900.0663) q[12],q[25];
cp(-727.2787) q[13],q[25];
cp(-1022.5884) q[14],q[25];
cp(102.10176) q[15],q[25];
cp(-1085.4203) q[16],q[25];
cp(-92.676983) q[17],q[25];
cp(-1493.8273) q[18],q[25];
cp(80.110613) q[20],q[25];
cp(405*pi) q[22],q[25];
h q[26];
cp(447.67695) q[0],q[26];
cp(937.76541) q[1],q[26];
cp(1349.314) q[2],q[26];
cp(-359.71236) q[4],q[26];
cp(1368.1636) q[5],q[26];
cp(-473*pi) q[6],q[26];
cp(17*pi) q[7],q[26];
cp(-35*pi) q[8],q[26];
cp(357*pi) q[9],q[26];
cp(-611.03977) q[11],q[26];
cp(-472.80969) q[12],q[26];
cp(-335*pi) q[14],q[26];
cp(339*pi) q[15],q[26];
cp(-289*pi) q[17],q[26];
cp(-1575.5087) q[18],q[26];
cp(131*pi) q[19],q[26];
cp(274.88936) q[20],q[26];
cp(-215.1991) q[21],q[26];
cp(151*pi) q[22],q[26];
cp(80.110613) q[24],q[26];
cp(-117.80972) q[25],q[26];
p(-223.44578) q[9];
h q[9];
h q[27];
cp(278.03095) q[1],q[27];
p(336.54311) q[1];
h q[1];
cp(431.96899) q[2],q[27];
cp(-934.62381) q[3],q[27];
cp(469*pi) q[5],q[27];
cp(313*pi) q[6],q[27];
cp(1214.2256) q[8],q[27];
cp(-290.59732) q[10],q[27];
cp(419.40262) q[12],q[27];
cp(-494.80084) q[13],q[27];
cp(1358.7388) q[15],q[27];
cp(197*pi) q[17],q[27];
cp(-1126.261) q[18],q[27];
p(55.76327) q[18];
h q[18];
cp(290.59732) q[19],q[27];
cp(-36.128316) q[20],q[27];
cp(-755.55303) q[22],q[27];
cp(567.05747) q[25],q[27];
h q[28];
cp(733.56188) q[0],q[28];
cp(868.65037) q[2],q[28];
cp(76.96902) q[3],q[28];
cp(-443*pi) q[5],q[28];
cp(567.05747) q[6],q[28];
cp(-1352.4556) q[7],q[28];
cp(-171*pi) q[10],q[28];
cp(73*pi) q[11],q[28];
cp(-81*pi) q[12],q[28];
cp(109*pi) q[13],q[28];
cp(423*pi) q[14],q[28];
cp(-83*pi) q[15],q[28];
cp(pi/2) q[16],q[28];
p(135.87388) q[16];
h q[16];
cp(-1374.4468) q[19],q[28];
cp(-11*pi/2) q[20],q[28];
cp(1063.4291) q[21],q[28];
p(-25.918139) q[21];
h q[21];
cp(-868.65037) q[24],q[28];
cp(39*pi) q[25],q[28];
p(109.56304) q[25];
h q[25];
cp(-416.26103) q[26],q[28];
cp(318.87165) q[27],q[28];
p(115.45353) q[28];
h q[28];
h q[29];
cp(-11*pi/2) q[0],q[29];
p(-268.60617) q[0];
h q[0];
cp(981.7477) q[2],q[29];
p(291.38272) q[2];
h q[2];
cp(309.44688) q[3],q[29];
p(-158.25773) q[3];
h q[3];
cp(1355.5972) q[4],q[29];
p(-140.58627) q[4];
h q[4];
cp(373*pi) q[5],q[29];
h q[5];
cp(-224.62387) q[6],q[29];
p(177.10729) q[6];
h q[6];
cp(-1509.5353) q[7],q[29];
p(388.77209) q[7];
h q[7];
cp(-966.03974) q[8],q[29];
cp(1091.7034) q[10],q[29];
h q[10];
cp(-708.42914) q[11],q[29];
p(-36.913714) q[11];
h q[11];
cp(-824.66807) q[12],q[29];
p(-236.40485) q[12];
h q[12];
cp(300.0221) q[13],q[29];
p(84.430303) q[13];
h q[13];
cp(-409*pi) q[14],q[29];
p(-44.374996) q[14];
h q[14];
cp(541.92473) q[15],q[29];
p(-261.93029) q[15];
h q[15];
cp(1135.6857) q[17],q[29];
h q[17];
cp(-273*pi) q[19],q[29];
p(212.8429) q[19];
h q[19];
cp(516.79199) q[20],q[29];
p(221.08958) q[20];
h q[20];
cp(252.89821) q[22],q[29];
p(-35.735616) q[22];
h q[22];
cp(-488.51766) q[23],q[29];
h q[23];
cp(51.836279) q[24],q[29];
p(-338.50661) q[24];
h q[24];
cp(1044.5796) q[26],q[29];
p(396.62607) q[26];
h q[26];
cp(-699.00437) q[27],q[29];
h q[27];
p(114.66813) q[29];
h q[29];
h q[8];