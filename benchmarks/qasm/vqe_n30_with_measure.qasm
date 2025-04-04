OPENQASM 2.0;
include "qelib1.inc";
qreg q[30];
creg meas[30];
sx q[0];
rz(4.31824513943531) q[0];
sx q[0];
rz(3*pi) q[0];
rz(1.90865844345986) q[0];
sx q[1];
rz(6.1283497342699) q[1];
sx q[1];
rz(3*pi) q[1];
rz(0.535717334235832) q[1];
cx q[0],q[1];
sx q[0];
rz(4.36265837149546) q[0];
sx q[0];
rz(3*pi) q[0];
rz(0.37571640445138) q[0];
sx q[2];
rz(5.44121944365674) q[2];
sx q[2];
rz(3*pi) q[2];
rz(0.204365606626867) q[2];
cx q[1],q[2];
sx q[1];
rz(3.99406077836937) q[1];
sx q[1];
rz(3*pi) q[1];
rz(2.24072458375098) q[1];
cx q[0],q[1];
sx q[0];
rz(5.67824071326661) q[0];
sx q[0];
rz(3*pi) q[0];
rz(2.85340143485906) q[0];
sx q[3];
rz(5.0223337495524) q[3];
sx q[3];
rz(3*pi) q[3];
rz(2.98101183293268) q[3];
cx q[2],q[3];
sx q[2];
rz(5.7451483240958) q[2];
sx q[2];
rz(3*pi) q[2];
rz(2.3900767196958) q[2];
cx q[1],q[2];
sx q[1];
rz(5.95674649837517) q[1];
sx q[1];
rz(3*pi) q[1];
rz(0.752605875799442) q[1];
cx q[0],q[1];
sx q[0];
rz(4.21308419643596) q[0];
sx q[0];
rz(3*pi) q[0];
rz(1.72389804145056) q[0];
sx q[4];
rz(3.63173966822682) q[4];
sx q[4];
rz(3*pi) q[4];
rz(3.03362250117801) q[4];
cx q[3],q[4];
sx q[3];
rz(4.26236628387409) q[3];
sx q[3];
rz(3*pi) q[3];
rz(1.7633043205118) q[3];
cx q[2],q[3];
sx q[2];
rz(4.14063003437743) q[2];
sx q[2];
rz(3*pi) q[2];
rz(0.455200665704619) q[2];
cx q[1],q[2];
sx q[1];
rz(3.49808023429619) q[1];
sx q[1];
rz(3*pi) q[1];
rz(2.17365287012542) q[1];
sx q[5];
rz(3.63166389267827) q[5];
sx q[5];
rz(3*pi) q[5];
rz(2.53965517002414) q[5];
cx q[4],q[5];
sx q[4];
rz(4.02417444536352) q[4];
sx q[4];
rz(3*pi) q[4];
rz(2.42206482870409) q[4];
cx q[3],q[4];
sx q[3];
rz(3.48733097119936) q[3];
sx q[3];
rz(3*pi) q[3];
rz(1.53766119596724) q[3];
cx q[2],q[3];
sx q[2];
rz(6.04660333159509) q[2];
sx q[2];
rz(3*pi) q[2];
rz(2.04819670327852) q[2];
sx q[6];
rz(3.32406770287137) q[6];
sx q[6];
rz(3*pi) q[6];
rz(0.956972379417358) q[6];
cx q[5],q[6];
sx q[5];
rz(4.8465226815717) q[5];
sx q[5];
rz(3*pi) q[5];
rz(1.55130461791336) q[5];
cx q[4],q[5];
sx q[4];
rz(3.85767208572635) q[4];
sx q[4];
rz(3*pi) q[4];
rz(3.09651222564131) q[4];
cx q[3],q[4];
sx q[3];
rz(5.8978355208767) q[3];
sx q[3];
rz(3*pi) q[3];
rz(0.704562815026951) q[3];
sx q[7];
rz(5.86276526987105) q[7];
sx q[7];
rz(3*pi) q[7];
rz(0.30684599582304) q[7];
cx q[6],q[7];
sx q[6];
rz(3.58431916348334) q[6];
sx q[6];
rz(3*pi) q[6];
rz(1.64221361657668) q[6];
cx q[5],q[6];
sx q[5];
rz(4.48339134462902) q[5];
sx q[5];
rz(3*pi) q[5];
rz(0.760439062743212) q[5];
cx q[4],q[5];
sx q[4];
rz(3.95194017627472) q[4];
sx q[4];
rz(3*pi) q[4];
rz(2.23737700982472) q[4];
sx q[8];
rz(5.0300511584448) q[8];
sx q[8];
rz(3*pi) q[8];
rz(2.1495814494341) q[8];
cx q[7],q[8];
sx q[7];
rz(5.6617687950586) q[7];
sx q[7];
rz(3*pi) q[7];
rz(1.34315972238352) q[7];
cx q[6],q[7];
sx q[6];
rz(5.71146183273987) q[6];
sx q[6];
rz(3*pi) q[6];
rz(2.11157609794686) q[6];
cx q[5],q[6];
sx q[5];
rz(5.21499368409724) q[5];
sx q[5];
rz(3*pi) q[5];
rz(0.745339990350829) q[5];
sx q[9];
rz(5.36606826220224) q[9];
sx q[9];
rz(3*pi) q[9];
rz(1.38277984079156) q[9];
cx q[8],q[9];
sx q[8];
rz(3.37580040809455) q[8];
sx q[8];
rz(3*pi) q[8];
rz(0.0798565418399173) q[8];
cx q[7],q[8];
sx q[7];
rz(5.84565753066798) q[7];
sx q[7];
rz(3*pi) q[7];
rz(2.39269858834658) q[7];
cx q[6],q[7];
sx q[6];
rz(5.70897191409242) q[6];
sx q[6];
rz(3*pi) q[6];
rz(1.02227330121749) q[6];
sx q[10];
rz(3.20626074964735) q[10];
sx q[10];
rz(3*pi) q[10];
rz(0.383394422045423) q[10];
cx q[9],q[10];
sx q[9];
rz(6.24198940353771) q[9];
sx q[9];
rz(3*pi) q[9];
rz(0.338950914427485) q[9];
cx q[8],q[9];
sx q[8];
rz(3.16343341579338) q[8];
sx q[8];
rz(3*pi) q[8];
rz(0.746560362423644) q[8];
cx q[7],q[8];
sx q[7];
rz(4.88580744457775) q[7];
sx q[7];
rz(3*pi) q[7];
rz(2.34517191428671) q[7];
sx q[11];
rz(6.18865431978628) q[11];
sx q[11];
rz(3*pi) q[11];
rz(1.55564414303286) q[11];
cx q[10],q[11];
sx q[10];
rz(5.56767114758532) q[10];
sx q[10];
rz(3*pi) q[10];
rz(0.0987376988617538) q[10];
cx q[9],q[10];
sx q[9];
rz(4.74615262720828) q[9];
sx q[9];
rz(3*pi) q[9];
rz(2.287759131023) q[9];
cx q[8],q[9];
sx q[8];
rz(4.80553901952261) q[8];
sx q[8];
rz(3*pi) q[8];
rz(2.04088194317697) q[8];
sx q[12];
rz(5.75678833846329) q[12];
sx q[12];
rz(3*pi) q[12];
rz(0.108034725303388) q[12];
cx q[11],q[12];
sx q[11];
rz(3.76587637885064) q[11];
sx q[11];
rz(3*pi) q[11];
rz(1.99934227269435) q[11];
cx q[10],q[11];
sx q[10];
rz(4.45292799460954) q[10];
sx q[10];
rz(3*pi) q[10];
rz(1.15542478786505) q[10];
cx q[9],q[10];
sx q[9];
rz(3.90139403393651) q[9];
sx q[9];
rz(3*pi) q[9];
rz(2.66791402766498) q[9];
sx q[13];
rz(3.80867564376646) q[13];
sx q[13];
rz(3*pi) q[13];
rz(2.85671429493002) q[13];
cx q[12],q[13];
sx q[12];
rz(3.15894089617756) q[12];
sx q[12];
rz(3*pi) q[12];
rz(0.9875784407614) q[12];
cx q[11],q[12];
sx q[11];
rz(3.83936491926955) q[11];
sx q[11];
rz(3*pi) q[11];
rz(1.98644735221478) q[11];
cx q[10],q[11];
sx q[10];
rz(3.43408362495768) q[10];
sx q[10];
rz(3*pi) q[10];
rz(2.06595183135669) q[10];
sx q[14];
rz(3.71281263480683) q[14];
sx q[14];
rz(3*pi) q[14];
rz(0.812981289090715) q[14];
cx q[13],q[14];
sx q[13];
rz(5.70344028650934) q[13];
sx q[13];
rz(3*pi) q[13];
rz(1.59772194719411) q[13];
cx q[12],q[13];
sx q[12];
rz(3.51816081102513) q[12];
sx q[12];
rz(3*pi) q[12];
rz(1.99029228515729) q[12];
cx q[11],q[12];
sx q[11];
rz(5.96027908746096) q[11];
sx q[11];
rz(3*pi) q[11];
rz(1.78539413321059) q[11];
sx q[15];
rz(3.71777491438058) q[15];
sx q[15];
rz(3*pi) q[15];
rz(2.081375141366) q[15];
cx q[14],q[15];
sx q[14];
rz(5.36225049215746) q[14];
sx q[14];
rz(3*pi) q[14];
rz(2.85120416713061) q[14];
cx q[13],q[14];
sx q[13];
rz(4.20224199581189) q[13];
sx q[13];
rz(3*pi) q[13];
rz(1.68318581146865) q[13];
cx q[12],q[13];
sx q[12];
rz(5.97033940713371) q[12];
sx q[12];
rz(3*pi) q[12];
rz(0.294287962435465) q[12];
sx q[16];
rz(4.09739784898316) q[16];
sx q[16];
rz(3*pi) q[16];
rz(0.979269226685062) q[16];
cx q[15],q[16];
sx q[15];
rz(5.43183621712166) q[15];
sx q[15];
rz(3*pi) q[15];
rz(0.783174635691129) q[15];
cx q[14],q[15];
sx q[14];
rz(6.10383085239989) q[14];
sx q[14];
rz(3*pi) q[14];
rz(0.283653678297241) q[14];
cx q[13],q[14];
sx q[13];
rz(5.13053954073648) q[13];
sx q[13];
rz(3*pi) q[13];
rz(1.15521326550039) q[13];
sx q[17];
rz(4.79016360412963) q[17];
sx q[17];
rz(3*pi) q[17];
rz(1.63384187469919) q[17];
cx q[16],q[17];
sx q[16];
rz(5.56460990867001) q[16];
sx q[16];
rz(3*pi) q[16];
rz(1.28925597616744) q[16];
cx q[15],q[16];
sx q[15];
rz(4.15696461044488) q[15];
sx q[15];
rz(3*pi) q[15];
rz(2.62418018366837) q[15];
cx q[14],q[15];
sx q[14];
rz(4.20668615449647) q[14];
sx q[14];
rz(3*pi) q[14];
rz(0.833157810023528) q[14];
sx q[18];
rz(4.49858795091057) q[18];
sx q[18];
rz(3*pi) q[18];
rz(1.71754099722687) q[18];
cx q[17],q[18];
sx q[17];
rz(3.37421078751523) q[17];
sx q[17];
rz(3*pi) q[17];
rz(2.37363390625825) q[17];
cx q[16],q[17];
sx q[16];
rz(4.77142145961003) q[16];
sx q[16];
rz(3*pi) q[16];
rz(1.00776029553326) q[16];
cx q[15],q[16];
sx q[15];
rz(4.23866688775615) q[15];
sx q[15];
rz(3*pi) q[15];
rz(0.766516071191722) q[15];
sx q[19];
rz(4.05651598094723) q[19];
sx q[19];
rz(3*pi) q[19];
rz(0.580737399462337) q[19];
cx q[18],q[19];
sx q[18];
rz(4.26774595294819) q[18];
sx q[18];
rz(3*pi) q[18];
rz(0.718790635863303) q[18];
cx q[17],q[18];
sx q[17];
rz(5.35019185018923) q[17];
sx q[17];
rz(3*pi) q[17];
rz(0.585965182030693) q[17];
cx q[16],q[17];
sx q[16];
rz(5.42224968116033) q[16];
sx q[16];
rz(3*pi) q[16];
rz(3.05680281067561) q[16];
sx q[20];
rz(5.06378521272727) q[20];
sx q[20];
rz(3*pi) q[20];
rz(3.04603994361873) q[20];
cx q[19],q[20];
sx q[19];
rz(3.5056060397723) q[19];
sx q[19];
rz(3*pi) q[19];
rz(0.241839519192141) q[19];
cx q[18],q[19];
sx q[18];
rz(4.28396874105236) q[18];
sx q[18];
rz(3*pi) q[18];
rz(0.12809888515753) q[18];
cx q[17],q[18];
sx q[17];
rz(5.95994765571684) q[17];
sx q[17];
rz(3*pi) q[17];
rz(1.23495292395596) q[17];
sx q[21];
rz(3.57982554143513) q[21];
sx q[21];
rz(3*pi) q[21];
rz(2.43515158342759) q[21];
cx q[20],q[21];
sx q[20];
rz(5.85311203560874) q[20];
sx q[20];
rz(3*pi) q[20];
rz(0.910281035840863) q[20];
cx q[19],q[20];
sx q[19];
rz(6.19453610555615) q[19];
sx q[19];
rz(3*pi) q[19];
rz(1.85634492937823) q[19];
cx q[18],q[19];
sx q[18];
rz(5.92845684716032) q[18];
sx q[18];
rz(3*pi) q[18];
rz(2.8024469044045) q[18];
sx q[22];
rz(4.05939213521361) q[22];
sx q[22];
rz(3*pi) q[22];
rz(2.95152297287344) q[22];
cx q[21],q[22];
sx q[21];
rz(5.09974146982753) q[21];
sx q[21];
rz(3*pi) q[21];
rz(0.50649161163947) q[21];
cx q[20],q[21];
sx q[20];
rz(6.1652100048473) q[20];
sx q[20];
rz(3*pi) q[20];
rz(2.12863122149797) q[20];
cx q[19],q[20];
sx q[19];
rz(5.59164393917043) q[19];
sx q[19];
rz(3*pi) q[19];
rz(1.98278047082976) q[19];
sx q[23];
rz(4.29255232903687) q[23];
sx q[23];
rz(3*pi) q[23];
rz(2.81118303033472) q[23];
cx q[22],q[23];
sx q[22];
rz(4.18113945755425) q[22];
sx q[22];
rz(3*pi) q[22];
rz(2.9207313146591) q[22];
cx q[21],q[22];
sx q[21];
rz(3.93259006445873) q[21];
sx q[21];
rz(3*pi) q[21];
rz(0.0521122014987571) q[21];
cx q[20],q[21];
sx q[20];
rz(5.15859455652027) q[20];
sx q[20];
rz(3*pi) q[20];
rz(2.49697335219657) q[20];
sx q[24];
rz(4.57437876552885) q[24];
sx q[24];
rz(3*pi) q[24];
rz(1.8783581810144) q[24];
cx q[23],q[24];
sx q[23];
rz(3.34126709992265) q[23];
sx q[23];
rz(3*pi) q[23];
rz(2.53878504765577) q[23];
cx q[22],q[23];
sx q[22];
rz(4.70374490670981) q[22];
sx q[22];
rz(3*pi) q[22];
rz(1.60878778990735) q[22];
cx q[21],q[22];
sx q[21];
rz(3.40592614949154) q[21];
sx q[21];
rz(3*pi) q[21];
rz(1.579080999121) q[21];
sx q[25];
rz(5.60829568567739) q[25];
sx q[25];
rz(3*pi) q[25];
rz(2.89615332428233) q[25];
cx q[24],q[25];
sx q[24];
rz(4.11857243088802) q[24];
sx q[24];
rz(3*pi) q[24];
rz(1.98989658820932) q[24];
cx q[23],q[24];
sx q[23];
rz(4.08682974133467) q[23];
sx q[23];
rz(3*pi) q[23];
rz(0.711557463430967) q[23];
cx q[22],q[23];
sx q[22];
rz(3.6493642343986) q[22];
sx q[22];
rz(3*pi) q[22];
rz(1.81239700576958) q[22];
sx q[26];
rz(3.76888634073298) q[26];
sx q[26];
rz(3*pi) q[26];
rz(0.27800739434409) q[26];
cx q[25],q[26];
sx q[25];
rz(4.16318618913895) q[25];
sx q[25];
rz(3*pi) q[25];
rz(2.73777418802676) q[25];
cx q[24],q[25];
sx q[24];
rz(4.03644545817093) q[24];
sx q[24];
rz(3*pi) q[24];
rz(2.02687009864635) q[24];
cx q[23],q[24];
sx q[23];
rz(5.9644838911188) q[23];
sx q[23];
rz(3*pi) q[23];
rz(1.54728996866433) q[23];
sx q[27];
rz(4.75710778753287) q[27];
sx q[27];
rz(3*pi) q[27];
rz(0.615698320805486) q[27];
cx q[26],q[27];
sx q[26];
rz(5.43371806347038) q[26];
sx q[26];
rz(3*pi) q[26];
rz(2.52481029268151) q[26];
cx q[25],q[26];
sx q[25];
rz(3.25747641641215) q[25];
sx q[25];
rz(3*pi) q[25];
rz(0.547788292394767) q[25];
cx q[24],q[25];
sx q[24];
rz(5.04674573233973) q[24];
sx q[24];
rz(3*pi) q[24];
rz(0.613373936131258) q[24];
sx q[28];
rz(5.00271791100635) q[28];
sx q[28];
rz(3*pi) q[28];
rz(0.14208571858313) q[28];
cx q[27],q[28];
sx q[27];
rz(5.14453852184062) q[27];
sx q[27];
rz(3*pi) q[27];
rz(0.586127126376185) q[27];
cx q[26],q[27];
sx q[26];
rz(5.05659548711139) q[26];
sx q[26];
rz(3*pi) q[26];
rz(2.17064492211066) q[26];
cx q[25],q[26];
sx q[25];
rz(3.17048604338328) q[25];
sx q[25];
rz(3*pi) q[25];
rz(2.26965025787595) q[25];
sx q[29];
rz(3.28752092894715) q[29];
sx q[29];
rz(3*pi) q[29];
rz(1.02205537711581) q[29];
cx q[28],q[29];
sx q[28];
rz(5.92885368783883) q[28];
sx q[28];
rz(3*pi) q[28];
rz(2.80405679255158) q[28];
cx q[27],q[28];
sx q[27];
rz(4.72080538007928) q[27];
sx q[27];
rz(3*pi) q[27];
rz(1.21496492282127) q[27];
cx q[26],q[27];
sx q[26];
rz(3.46037490720614) q[26];
sx q[26];
rz(3*pi) q[26];
rz(0.882072391175243) q[26];
sx q[29];
rz(4.62509959339403) q[29];
sx q[29];
rz(3*pi) q[29];
rz(1.69439362497286) q[29];
cx q[28],q[29];
sx q[28];
rz(3.30331792033274) q[28];
sx q[28];
rz(3*pi) q[28];
rz(2.94282405101257) q[28];
cx q[27],q[28];
sx q[27];
rz(5.22604493706349) q[27];
sx q[27];
rz(3*pi) q[27];
rz(0.0763908615059914) q[27];
sx q[29];
rz(4.0169863385843) q[29];
sx q[29];
rz(3*pi) q[29];
rz(0.432034787843785) q[29];
cx q[28],q[29];
sx q[28];
rz(3.1574940882166) q[28];
sx q[28];
rz(3*pi) q[28];
rz(2.0278110229177) q[28];
sx q[29];
rz(3.6467860465611) q[29];
sx q[29];
rz(3*pi) q[29];
rz(0.556409609297482) q[29];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
measure q[3] -> meas[3];
measure q[4] -> meas[4];
measure q[5] -> meas[5];
measure q[6] -> meas[6];
measure q[7] -> meas[7];
measure q[8] -> meas[8];
measure q[9] -> meas[9];
measure q[10] -> meas[10];
measure q[11] -> meas[11];
measure q[12] -> meas[12];
measure q[13] -> meas[13];
measure q[14] -> meas[14];
measure q[15] -> meas[15];
measure q[16] -> meas[16];
measure q[17] -> meas[17];
measure q[18] -> meas[18];
measure q[19] -> meas[19];
measure q[20] -> meas[20];
measure q[21] -> meas[21];
measure q[22] -> meas[22];
measure q[23] -> meas[23];
measure q[24] -> meas[24];
measure q[25] -> meas[25];
measure q[26] -> meas[26];
measure q[27] -> meas[27];
measure q[28] -> meas[28];
measure q[29] -> meas[29];
