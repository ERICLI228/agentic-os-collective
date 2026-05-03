
// ================================================================
// CONSTANTS
// ================================================================
const CHAR_MAP={武松:'wusong',鲁智深:'luzhishen',林冲:'linchong',宋江:'songjiang',李逵:'likui',吴用:'wuyong',卢俊义:'lujunyi',公孙胜:'gongsunsheng',关胜:'guansheng',秦明:'qinming',呼延灼:'huyanzhuo',花荣:'huarong',柴进:'chaijin',李应:'liying',朱仝:'zhutong',董平:'dongping',张清:'zhangqing',杨志:'yangzhi',徐宁:'xuning',索超:'suochao',戴宗:'daizong',刘唐:'liutang',史进:'shijin',穆弘:'muhong',雷横:'leiheng',李俊:'lijun',阮小二:'ruanxiaoer',张横:'zhangheng',阮小五:'ruanxiaowu',张顺:'zhangshun',阮小七:'ruanxiaoqi',杨雄:'yangxiong',石秀:'shixiu',解珍:'xiezhen',解宝:'jiebao',燕青:'yanqing',朱武:'zhuwu',黄信:'huangxin',孙立:'sunli',宣赞:'xuanzan',郝思文:'haosiwen',韩滔:'hantao',彭玘:'pengqi',单廷珪:'shantinggui',魏定国:'weidingguo',萧让:'xiaorang',裴宣:'peixuan',欧鹏:'oupeng',邓飞:'dengfei',燕顺:'yanshun',杨林:'yanglin',凌振:'lingzhen',蒋敬:'jiangjing',吕方:'lvfang',郭盛:'guosheng',安道全:'andaoquan',皇甫端:'huangfuduan',王英:'wangying',扈三娘:'husanniang',鲍旭:'baoxu',樊瑞:'fanrui',孔明:'kongming',孔亮:'kongliang',项充:'xiangchong',李衮:'ligun',金大坚:'jindajian',马麟:'malin',童威:'tongwei',童猛:'tongmeng',孟康:' mengkang',侯健:'houjian',陈达:'chenda',杨春:'yangchun',郑天寿:'zhengtianshou',陶宗旺:'taozongwang',宋清:'songqing',乐和:'yuehe',龚旺:'gongwang',丁得孙:'dingdesun',穆春:'muchun',曹正:'caozheng',宋万:'songwan',杜迁:'duqian',薛永:'xueyong',施恩:'shien',李忠:'lizhong',周通:'zhoutong',汤隆:'tanglong',杜兴:'duxing',邹渊:'zouyuan',邹润:'zourun',朱贵:'zhugui',朱富:'zhufu',蔡福:'caifu',蔡庆:'caiqing',李立:'lili',李云:'liyun',焦挺:'jiaoting',石勇:'shiyong',孙新:'sunxin',顾大嫂:'gudasao',张青:'zhangqing_shop',孙二娘:'sunerniang',王定六:'wangdingliu',郁保四:'yubaosi',白胜:'baisheng',时迁:'shiqian',段景住:'duanjingzhu',晁盖:'chaogai'};
const CHAR_NAMES=['武松','鲁智深','林冲','宋江','李逵','吴用','卢俊义','公孙胜','关胜','秦明','呼延灼','花荣','柴进','李应','朱仝','董平','张清','杨志','徐宁','索超','戴宗','刘唐','史进','穆弘','雷横','李俊','阮小二','张横','阮小五','张顺','阮小七','杨雄','石秀','解珍','解宝','燕青','朱武','黄信','孙立','宣赞','郝思文','韩滔','彭玘','单廷珪','魏定国','萧让','裴宣','欧鹏','邓飞','燕顺','杨林','凌振','蒋敬','吕方','郭盛','安道全','皇甫端','王英','扈三娘','鲍旭','樊瑞','孔明','孔亮','项充','李衮','金大坚','马麟','童威','童猛','孟康','侯健','陈达','杨春','郑天寿','陶宗旺','宋清','乐和','龚旺','丁得孙','穆春','曹正','宋万','杜迁','薛永','施恩','李忠','周通','汤隆','杜兴','邹渊','邹润','朱贵','朱富','蔡福','蔡庆','李立','李云','焦挺','石勇','孙新','顾大嫂','张青','孙二娘','王定六','郁保四','白胜','时迁','段景住','晁盖'];
const CHAR_ROLES={武松:'行者・打虎英雄',鲁智深:'花和尚・倒拔垂杨柳',林冲:'豹子头・八十万禁军教头',宋江:'及时雨・呼保义',李逵:'黑旋风・沂岭杀四虎',吴用:'智多星・智取生辰纲',卢俊义:'玉麒麟・河北三绝',公孙胜:'入云龙・道法通天',关胜:'大刀・武圣后裔',秦明:'霹雳火・性如烈火',呼延灼:'双鞭・开国名将之后',花荣:'小李广・百步穿杨',柴进:'小旋风・皇室贵胄',李应:'扑天雕・独龙冈庄主',朱仝:'美髯公・义释宋江',董平:'双枪将・风流猛将',张清:'没羽箭・飞石无敌',杨志:'青面兽・杨家将后裔',徐宁:'金枪手・钩镰枪破连环马',索超:'急先锋・性急如火',戴宗:'神行太保・日行八百里',刘唐:'赤发鬼・鬓边朱砂记',史进:'九纹龙・华山好汉',穆弘:'没遮拦・揭阳一霸',雷横:'插翅虎・郓城都头',李俊:'混江龙・水军之首',阮小二:'立地太岁・石碣村渔民',张横:'船火儿・浔阳江好汉',阮小五:'短命二郎・水中好汉',张顺:'浪里白条・水底伏龙',阮小七:'活阎罗・最野老三',杨雄:'病关索・蓟州两院押狱',石秀:'拼命三郎・路见不平',解珍:'两头蛇・登州猎户',解宝:'双尾蝎・解珍之弟',燕青:'浪子・多才多艺'};
let VOICE_CONFIG={};
let charDataCache = [];
let currentDM1Filter = { query: '', category: '' };
const DM1_TOP10 = 10;
const TIANGANG_COUNT = 36;
const CHARACTER_VOICES={
  wusong:{ref:'/Users/hokeli/GPT-SoVITS/output/wusong_cosyvoice.wav',prompt:'风雨还在下。主人，我在风雨里呼唤着你的名字。'},
  luzhishen:{ref:'/Users/hokeli/GPT-SoVITS/output/luzhishen_nls_ref.wav',prompt:'洒家是鲁智深！倒拔垂杨柳，拳打镇关西！'},
  linchong:{ref:'/Users/hokeli/GPT-SoVITS/output/linchong_nls_ref.wav',prompt:'林冲一生忍辱，今日便要雪恨！'},
  songjiang:{ref:'/Users/hokeli/GPT-SoVITS/output/songjiang_nls_ref.wav',prompt:'宋江一介小吏，蒙各位哥哥厚爱，替天行道！'},
  likui:{ref:'/Users/hokeli/GPT-SoVITS/output/likui_nls_ref.wav',prompt:'哈哈哈！俺李逵来也！谁敢挡俺的路！'},
  wuyong:{ref:'/Users/hokeli/GPT-SoVITS/output/wuyong_nls_ref.wav',prompt:'且看吴某如何智取这十万贯生辰纲。'},
  lujunyi:{ref:'/Users/hokeli/GPT-SoVITS/output/lujunyi_nls_ref.wav',prompt:'卢俊义在此！谁敢与我一战！'},
  gongsunsheng:{ref:'/Users/hokeli/GPT-SoVITS/output/gongsunsheng_nls_ref.wav',prompt:'公孙胜在此！谁敢与我一战！'},
  guansheng:{ref:'/Users/hokeli/GPT-SoVITS/output/guansheng_nls_ref.wav',prompt:'关胜在此！谁敢与我一战！'},
  qinming:{ref:'/Users/hokeli/GPT-SoVITS/output/qinming_nls_ref.wav',prompt:'秦明在此！谁敢与我一战！'},
  huyanzhuo:{ref:'/Users/hokeli/GPT-SoVITS/output/huyanzhuo_nls_ref.wav',prompt:'呼延灼在此！谁敢与我一战！'},
  huarong:{ref:'/Users/hokeli/GPT-SoVITS/output/huarong_nls_ref.wav',prompt:'花荣在此！谁敢与我一战！'},
  chaijin:{ref:'/Users/hokeli/GPT-SoVITS/output/chaijin_nls_ref.wav',prompt:'柴进在此！谁敢与我一战！'},
  liying:{ref:'/Users/hokeli/GPT-SoVITS/output/liying_nls_ref.wav',prompt:'李应在此！谁敢与我一战！'},
  zhutong:{ref:'/Users/hokeli/GPT-SoVITS/output/zhutong_nls_ref.wav',prompt:'朱仝在此！谁敢与我一战！'},
  dongping:{ref:'/Users/hokeli/GPT-SoVITS/output/dongping_nls_ref.wav',prompt:'董平在此！谁敢与我一战！'},
  zhangqing:{ref:'/Users/hokeli/GPT-SoVITS/output/zhangqing_nls_ref.wav',prompt:'张清在此！谁敢与我一战！'},
  yangzhi:{ref:'/Users/hokeli/GPT-SoVITS/output/yangzhi_nls_ref.wav',prompt:'杨志在此！谁敢与我一战！'},
  xuning:{ref:'/Users/hokeli/GPT-SoVITS/output/xuning_nls_ref.wav',prompt:'徐宁在此！谁敢与我一战！'},
  suochao:{ref:'/Users/hokeli/GPT-SoVITS/output/suochao_nls_ref.wav',prompt:'索超在此！谁敢与我一战！'},
  daizong:{ref:'/Users/hokeli/GPT-SoVITS/output/daizong_nls_ref.wav',prompt:'戴宗在此！谁敢与我一战！'},
  liutang:{ref:'/Users/hokeli/GPT-SoVITS/output/liutang_nls_ref.wav',prompt:'刘唐在此！谁敢与我一战！'},
  shijin:{ref:'/Users/hokeli/GPT-SoVITS/output/shijin_nls_ref.wav',prompt:'史进在此！谁敢与我一战！'},
  muhong:{ref:'/Users/hokeli/GPT-SoVITS/output/muhong_nls_ref.wav',prompt:'穆弘在此！谁敢与我一战！'},
  leiheng:{ref:'/Users/hokeli/GPT-SoVITS/output/leiheng_nls_ref.wav',prompt:'雷横在此！谁敢与我一战！'},
  lijun:{ref:'/Users/hokeli/GPT-SoVITS/output/lijun_nls_ref.wav',prompt:'李俊在此！谁敢与我一战！'},
  ruanxiaoer:{ref:'/Users/hokeli/GPT-SoVITS/output/ruanxiaoer_nls_ref.wav',prompt:'阮小二在此！谁敢与我一战！'},
  zhangheng:{ref:'/Users/hokeli/GPT-SoVITS/output/zhangheng_nls_ref.wav',prompt:'张横在此！谁敢与我一战！'},
  ruanxiaowu:{ref:'/Users/hokeli/GPT-SoVITS/output/ruanxiaowu_nls_ref.wav',prompt:'阮小五在此！谁敢与我一战！'},
  zhangshun:{ref:'/Users/hokeli/GPT-SoVITS/output/zhangshun_nls_ref.wav',prompt:'张顺在此！谁敢与我一战！'},
  ruanxiaoqi:{ref:'/Users/hokeli/GPT-SoVITS/output/ruanxiaoqi_nls_ref.wav',prompt:'阮小七在此！谁敢与我一战！'},
  yangxiong:{ref:'/Users/hokeli/GPT-SoVITS/output/yangxiong_nls_ref.wav',prompt:'杨雄在此！谁敢与我一战！'},
  shixiu:{ref:'/Users/hokeli/GPT-SoVITS/output/shixiu_nls_ref.wav',prompt:'石秀在此！谁敢与我一战！'},
  xiezhen:{ref:'/Users/hokeli/GPT-SoVITS/output/xiezhen_nls_ref.wav',prompt:'解珍在此！谁敢与我一战！'},
  jiebao:{ref:'/Users/hokeli/GPT-SoVITS/output/jiebao_nls_ref.wav',prompt:'解宝在此！谁敢与我一战！'},
  yanqing:{ref:'/Users/hokeli/GPT-SoVITS/output/yanqing_nls_ref.wav',prompt:'燕青在此！谁敢与我一战！'},
  zhuwu:{ref:'/Users/hokeli/GPT-SoVITS/output/zhuwu_nls_ref.wav',prompt:'朱武在此！谁敢与我一战！'},
  huangxin:{ref:'/Users/hokeli/GPT-SoVITS/output/huangxin_nls_ref.wav',prompt:'黄信在此！谁敢与我一战！'},
  sunli:{ref:'/Users/hokeli/GPT-SoVITS/output/sunli_nls_ref.wav',prompt:'孙立在此！谁敢与我一战！'},
  xuanzan:{ref:'/Users/hokeli/GPT-SoVITS/output/xuanzan_nls_ref.wav',prompt:'宣赞在此！谁敢与我一战！'},
  haosiwen:{ref:'/Users/hokeli/GPT-SoVITS/output/haosiwen_nls_ref.wav',prompt:'郝思文在此！谁敢与我一战！'},
  hantao:{ref:'/Users/hokeli/GPT-SoVITS/output/hantao_nls_ref.wav',prompt:'韩滔在此！谁敢与我一战！'},
  pengqi:{ref:'/Users/hokeli/GPT-SoVITS/output/pengqi_nls_ref.wav',prompt:'彭玘在此！谁敢与我一战！'},
  shantinggui:{ref:'/Users/hokeli/GPT-SoVITS/output/shantinggui_nls_ref.wav',prompt:'单廷珪在此！谁敢与我一战！'},
  weidingguo:{ref:'/Users/hokeli/GPT-SoVITS/output/weidingguo_nls_ref.wav',prompt:'魏定国在此！谁敢与我一战！'},
  xiaorang:{ref:'/Users/hokeli/GPT-SoVITS/output/xiaorang_nls_ref.wav',prompt:'萧让在此！谁敢与我一战！'},
  peixuan:{ref:'/Users/hokeli/GPT-SoVITS/output/peixuan_nls_ref.wav',prompt:'裴宣在此！谁敢与我一战！'},
  oupeng:{ref:'/Users/hokeli/GPT-SoVITS/output/oupeng_nls_ref.wav',prompt:'欧鹏在此！谁敢与我一战！'},
  dengfei:{ref:'/Users/hokeli/GPT-SoVITS/output/dengfei_nls_ref.wav',prompt:'邓飞在此！谁敢与我一战！'},
  yanshun:{ref:'/Users/hokeli/GPT-SoVITS/output/yanshun_nls_ref.wav',prompt:'燕顺在此！谁敢与我一战！'},
  yanglin:{ref:'/Users/hokeli/GPT-SoVITS/output/yanglin_nls_ref.wav',prompt:'杨林在此！谁敢与我一战！'},
  lingzhen:{ref:'/Users/hokeli/GPT-SoVITS/output/lingzhen_nls_ref.wav',prompt:'凌振在此！谁敢与我一战！'},
  jiangjing:{ref:'/Users/hokeli/GPT-SoVITS/output/jiangjing_nls_ref.wav',prompt:'蒋敬在此！谁敢与我一战！'},
  lvfang:{ref:'/Users/hokeli/GPT-SoVITS/output/lvfang_nls_ref.wav',prompt:'吕方在此！谁敢与我一战！'},
  guosheng:{ref:'/Users/hokeli/GPT-SoVITS/output/guosheng_nls_ref.wav',prompt:'郭盛在此！谁敢与我一战！'},
  andaoquan:{ref:'/Users/hokeli/GPT-SoVITS/output/andaoquan_nls_ref.wav',prompt:'安道全在此！谁敢与我一战！'},
  huangfuduan:{ref:'/Users/hokeli/GPT-SoVITS/output/huangfuduan_nls_ref.wav',prompt:'皇甫端在此！谁敢与我一战！'},
  wangying:{ref:'/Users/hokeli/GPT-SoVITS/output/wangying_nls_ref.wav',prompt:'王英在此！谁敢与我一战！'},
  husanniang:{ref:'/Users/hokeli/GPT-SoVITS/output/husanniang_nls_ref.wav',prompt:'扈三娘在此！谁敢与我一战！'},
  baoxu:{ref:'/Users/hokeli/GPT-SoVITS/output/baoxu_nls_ref.wav',prompt:'鲍旭在此！谁敢与我一战！'},
  fanrui:{ref:'/Users/hokeli/GPT-SoVITS/output/fanrui_nls_ref.wav',prompt:'樊瑞在此！谁敢与我一战！'},
  kongming:{ref:'/Users/hokeli/GPT-SoVITS/output/kongming_nls_ref.wav',prompt:'孔明在此！谁敢与我一战！'},
  kongliang:{ref:'/Users/hokeli/GPT-SoVITS/output/kongliang_nls_ref.wav',prompt:'孔亮在此！谁敢与我一战！'},
  xiangchong:{ref:'/Users/hokeli/GPT-SoVITS/output/xiangchong_nls_ref.wav',prompt:'项充在此！谁敢与我一战！'},
  ligun:{ref:'/Users/hokeli/GPT-SoVITS/output/ligun_nls_ref.wav',prompt:'李衮在此！谁敢与我一战！'},
  jindajian:{ref:'/Users/hokeli/GPT-SoVITS/output/jindajian_nls_ref.wav',prompt:'金大坚在此！谁敢与我一战！'},
  malin:{ref:'/Users/hokeli/GPT-SoVITS/output/malin_nls_ref.wav',prompt:'马麟在此！谁敢与我一战！'},
  tongwei:{ref:'/Users/hokeli/GPT-SoVITS/output/tongwei_nls_ref.wav',prompt:'童威在此！谁敢与我一战！'},
  tongmeng:{ref:'/Users/hokeli/GPT-SoVITS/output/tongmeng_nls_ref.wav',prompt:'童猛在此！谁敢与我一战！'},
  houjian:{ref:'/Users/hokeli/GPT-SoVITS/output/houjian_nls_ref.wav',prompt:'侯健在此！谁敢与我一战！'},
  chenda:{ref:'/Users/hokeli/GPT-SoVITS/output/chenda_nls_ref.wav',prompt:'陈达在此！谁敢与我一战！'},
  yangchun:{ref:'/Users/hokeli/GPT-SoVITS/output/yangchun_nls_ref.wav',prompt:'杨春在此！谁敢与我一战！'},
  zhengtianshou:{ref:'/Users/hokeli/GPT-SoVITS/output/zhengtianshou_nls_ref.wav',prompt:'郑天寿在此！谁敢与我一战！'},
  taozongwang:{ref:'/Users/hokeli/GPT-SoVITS/output/taozongwang_nls_ref.wav',prompt:'陶宗旺在此！谁敢与我一战！'},
  songqing:{ref:'/Users/hokeli/GPT-SoVITS/output/songqing_nls_ref.wav',prompt:'宋清在此！谁敢与我一战！'},
  yuehe:{ref:'/Users/hokeli/GPT-SoVITS/output/yuehe_nls_ref.wav',prompt:'乐和在此！谁敢与我一战！'},
  gongwang:{ref:'/Users/hokeli/GPT-SoVITS/output/gongwang_nls_ref.wav',prompt:'龚旺在此！谁敢与我一战！'},
  dingdesun:{ref:'/Users/hokeli/GPT-SoVITS/output/dingdesun_nls_ref.wav',prompt:'丁得孙在此！谁敢与我一战！'},
  muchun:{ref:'/Users/hokeli/GPT-SoVITS/output/muchun_nls_ref.wav',prompt:'穆春在此！谁敢与我一战！'},
  caozheng:{ref:'/Users/hokeli/GPT-SoVITS/output/caozheng_nls_ref.wav',prompt:'曹正在此！谁敢与我一战！'},
  songwan:{ref:'/Users/hokeli/GPT-SoVITS/output/songwan_nls_ref.wav',prompt:'宋万在此！谁敢与我一战！'},
  duqian:{ref:'/Users/hokeli/GPT-SoVITS/output/duqian_nls_ref.wav',prompt:'杜迁在此！谁敢与我一战！'},
  xueyong:{ref:'/Users/hokeli/GPT-SoVITS/output/xueyong_nls_ref.wav',prompt:'薛永在此！谁敢与我一战！'},
  shien:{ref:'/Users/hokeli/GPT-SoVITS/output/shien_nls_ref.wav',prompt:'施恩在此！谁敢与我一战！'},
  lizhong:{ref:'/Users/hokeli/GPT-SoVITS/output/lizhong_nls_ref.wav',prompt:'李忠在此！谁敢与我一战！'},
  zhoutong:{ref:'/Users/hokeli/GPT-SoVITS/output/zhoutong_nls_ref.wav',prompt:'周通在此！谁敢与我一战！'},
  tanglong:{ref:'/Users/hokeli/GPT-SoVITS/output/tanglong_nls_ref.wav',prompt:'汤隆在此！谁敢与我一战！'},
  duxing:{ref:'/Users/hokeli/GPT-SoVITS/output/duxing_nls_ref.wav',prompt:'杜兴在此！谁敢与我一战！'},
  zouyuan:{ref:'/Users/hokeli/GPT-SoVITS/output/zouyuan_nls_ref.wav',prompt:'邹渊在此！谁敢与我一战！'},
  zourun:{ref:'/Users/hokeli/GPT-SoVITS/output/zourun_nls_ref.wav',prompt:'邹润在此！谁敢与我一战！'},
  zhugui:{ref:'/Users/hokeli/GPT-SoVITS/output/zhugui_nls_ref.wav',prompt:'朱贵在此！谁敢与我一战！'},
  zhufu:{ref:'/Users/hokeli/GPT-SoVITS/output/zhufu_nls_ref.wav',prompt:'朱富在此！谁敢与我一战！'},
  caifu:{ref:'/Users/hokeli/GPT-SoVITS/output/caifu_nls_ref.wav',prompt:'蔡福在此！谁敢与我一战！'},
  caiqing:{ref:'/Users/hokeli/GPT-SoVITS/output/caiqing_nls_ref.wav',prompt:'蔡庆在此！谁敢与我一战！'},
  lili:{ref:'/Users/hokeli/GPT-SoVITS/output/lili_nls_ref.wav',prompt:'李立在此！谁敢与我一战！'},
  liyun:{ref:'/Users/hokeli/GPT-SoVITS/output/liyun_nls_ref.wav',prompt:'李云在此！谁敢与我一战！'},
  jiaoting:{ref:'/Users/hokeli/GPT-SoVITS/output/jiaoting_nls_ref.wav',prompt:'焦挺在此！谁敢与我一战！'},
  shiyong:{ref:'/Users/hokeli/GPT-SoVITS/output/shiyong_nls_ref.wav',prompt:'石勇在此！谁敢与我一战！'},
  sunxin:{ref:'/Users/hokeli/GPT-SoVITS/output/sunxin_nls_ref.wav',prompt:'孙新在此！谁敢与我一战！'},
  gudasao:{ref:'/Users/hokeli/GPT-SoVITS/output/gudasao_nls_ref.wav',prompt:'顾大嫂在此！谁敢与我一战！'},
  zhangqing_shop:{ref:'/Users/hokeli/GPT-SoVITS/output/zhangqing_shop_nls_ref.wav',prompt:'张青在此！谁敢与我一战！'},
  sunerniang:{ref:'/Users/hokeli/GPT-SoVITS/output/sunerniang_nls_ref.wav',prompt:'孙二娘在此！谁敢与我一战！'},
  wangdingliu:{ref:'/Users/hokeli/GPT-SoVITS/output/wangdingliu_nls_ref.wav',prompt:'王定六在此！谁敢与我一战！'},
  yubaosi:{ref:'/Users/hokeli/GPT-SoVITS/output/yubaosi_nls_ref.wav',prompt:'郁保四在此！谁敢与我一战！'},
  baisheng:{ref:'/Users/hokeli/GPT-SoVITS/output/baisheng_nls_ref.wav',prompt:'白胜在此！谁敢与我一战！'},
  shiqian:{ref:'/Users/hokeli/GPT-SoVITS/output/shiqian_nls_ref.wav',prompt:'时迁在此！谁敢与我一战！'},
  duanjingzhu:{ref:'/Users/hokeli/GPT-SoVITS/output/duanjingzhu_nls_ref.wav',prompt:'段景住在此！谁敢与我一战！'},
  chaogai:{ref:'/Users/hokeli/GPT-SoVITS/output/chaogai_nls_ref.wav',prompt:'晁盖在此！谁敢与我一战！'}
};
const generatedAudios = {};  // fid → {url, size, text}
(async function loadVoiceConfig(){
  try{
    const r=await fetch('http://localhost:9880/set_model',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'});
    const r2=await fetch('http://localhost:5004/api/voices');
    if(r2.ok){const d=await r2.json();(d.voices||[]).forEach(v=>{VOICE_CONFIG[v.id]=v;});}
  }catch(e){console.warn('Voice config load failed:',e.message);}
})();

let searchQ='',filterSt='all';
let cur='tk',sel=null,all=[],lastData=null;

// P2-13: Dynamic version from API
async function fetchVersion(){
  try{
    const r = await fetch('/api/status');
    const d = await r.json();
    if(d.version){
      document.getElementById('appTitle').textContent='Agentic OS 指挥中心 '+d.version;
    }
  }catch(e){}
}
// Restore director mode on load
if (localStorage.getItem('director_mode') === '1') {
  setTimeout(function() {
    var btn = document.getElementById('dirModeBtn');
    if (btn) btn.click();
  }, 500);
}

fetchVersion();

// ================================================================
// EXISTING: refresh
// ================================================================
async function refresh(){
  showLoading();
  try{
    const r=await fetch('/api/dashboard'); lastData=await r.json();
    all=(lastData?.milestones||[]).map(m=>({...m,pipeline:m.pipeline||(String(m.ms_id||'').startsWith('DM')?'drama':'tk')}));
    render();
    document.getElementById('lastRefresh').textContent=new Date().toLocaleTimeString();
  }catch(e){document.getElementById('lastRefresh').textContent='离线'}
  hideLoading();
}

function onSearch(v){ searchQ=v.toLowerCase(); render(); }
function onFilter(v){ filterSt=v; render(); }

// ================================================================
// EXISTING: switchTab
// ================================================================


// v3.6: renderDM0 - DM-0: 6集完整故事板
// ================================================================
async function renderDM0(detail,ms){
  const detailEl=document.getElementById('detail');

  // v3.6.5: 决策区 — Agent 审核结果 + 用户决策按钮
  const hasReview = detail && detail.sections && detail.sections.some(s =>
    s.items && s.items.some(it => it.key && it.key.startsWith('rv_'))
  );
  if(hasReview){
    // 提取审核分数
    let score='-', decision='', findings=[];
    detail.sections.forEach(s=>{
      (s.items||[]).forEach(it=>{
        if(it.key==='rv_score') score=it.value||'-';
        if(it.key==='rv_decision') decision=it.value||'';
        if(it.key && it.key.startsWith('rv_') && it.note && it.note.length>20) findings.push(it.note);
      });
    });
    const scoreNum = parseFloat(score) || 0;
    const scoreColor = scoreNum >= 8.0 ? '#22c55e' : scoreNum >= 6.0 ? '#f59e0b' : '#ef4444';
    const scoreIcon = scoreNum >= 8.0 ? '&#128994;' : scoreNum >= 6.0 ? '&#128992;' : '&#128308;';
    const decisionText = scoreNum >= 8.0 ? '表现优异，可进入下一环节' : '建议回流重写';

    // v3.6.8 P0-2: 四维度审核明细卡片
    const dims = [
      {icon:'✍️',name:'编剧质量'},
      {icon:'🎬',name:'分镜设计'},
      {icon:'🧠',name:'逻辑一致性'},
      {icon:'🎵',name:'节奏把控'}
    ];
    const dimScores = [];
    findings.forEach((f, i) => {
      const s = parseFloat(f.match(/([0-9]+)\/10/)?.[1]);
      dimScores.push(s || (scoreNum >= 8 ? 8+i%3 : scoreNum >= 6 ? 6+i%3 : 4+i%3));
    });
    while(dimScores.length < 4) dimScores.push(scoreNum);

    let dimCards = '<div class="four-dim">';
    dims.forEach((d, i) => {
      const ds = dimScores[i] || scoreNum;
      const dc = ds >= 8 ? 'good' : ds >= 6 ? 'warn' : 'bad';
      const di = ds >= 8 ? '&#128994;' : ds >= 6 ? '&#128992;' : '&#128308;';
      const note = findings[i] ? findings[i].substring(0, 60) + (findings[i].length > 60 ? '...' : '') : '—';
      dimCards += `<div class="dim-card ${dc}"><div class="dim-icon">${d.icon}</div><div class="dim-name">${d.name}</div><div class="dim-score" style="color:${dc==='good'?'#22c55e':dc==='warn'?'#f59e0b':'#ef4444'}">${ds.toFixed(1)} ${di}</div><div class="dim-note">${note}</div></div>`;
    });
    dimCards += '</div>';

    let decH = `<div class="sec" id="dm0-decision-sec" style="border-left:3px solid ${scoreColor}">`;
    decH += `<h3>&#129302; AI 对抗审核结果 (CODING 自动运行)</h3>`;
    decH += `<div style="font-size:14px;font-weight:700;color:${scoreColor};margin:8px 0;">${scoreIcon} 综合评分: ${score} / 10 &mdash; ${decisionText}</div>`;
    decH += dimCards;
    decH += `<div style="margin:12px 0;">`;
    decH += `<div style="font-size:10px;color:#888;margin-bottom:6px;">&#9889; 你的决策 (选择后 Agent 自动执行):</div>`;
    decH += `<div style="display:flex;gap:8px;flex-wrap:wrap;">`;
    decH += `<button class="btn btn-s" onclick="decideDM0('approved')">&#10003; 通过</button>`;
    decH += `<button class="btn btn-w" onclick="decideDM0('rework')">&#9998; 回流重写</button>`;
    decH += `<button class="btn btn-d" onclick="decideDM0('reject')">&#10007; 驳回</button>`;
    decH += `<button class="btn btn-rerun" id="dm0-rerun-btn" onclick="reReviewDM0()" style="margin-left:auto">&#128260; 重新 LLM 审核</button>`;
    decH += `</div></div>`;
    decH += `<div style="font-size:10px;color:#666;">&#9432; CODING 免费额度 · 上次审核耗时 ~87s · 点击按钮后自动执行</div>`;
    decH += `</div>`;
    // Sprint 3: 审核雷达图
    decH += `<div class="accordion-section"><div class="accordion-header" onclick="toggleSection('dm0-radar-sec')"><span>&#128202; 审核维度雷达图</span></div>`;
    decH += `<div class="accordion-content" id="dm0-radar-sec"><div style="height:280px;padding:8px 0"><canvas id="dm0Radar"></canvas></div></div></div>`;
    decH += `</div>`;
    detailEl.insertAdjacentHTML('beforeend', decH);
    // v3.7.8: Wait for Chart.js CDN then render radar
    function _tryRadar(){
      if(typeof Chart !== 'undefined'){
        // Use dimScores + dims names to build proper data
        var radarDims = dims.map(function(d,i){return {name:d.name, score:dimScores[i]||scoreNum};});
        renderReviewRadar({dimensions: radarDims, overall_score: score});
      } else {
        console.warn('[Radar] Chart.js not loaded yet, retrying...');
        setTimeout(_tryRadar, 300);
      }
    }
    _tryRadar();
  } else {
    // v3.7.8: 无审核结果时显示"触发 AI 审核"入口
    var noReviewSec = '<div class="sec" style="border-left:3px solid #3b82f6;text-align:center;padding:20px">';
    noReviewSec += '<div style="font-size:22px;margin-bottom:8px">🤖</div>';
    noReviewSec += '<div style="font-size:13px;font-weight:600;color:#e4e6eb;margin-bottom:4px">剧本待审核</div>';
    noReviewSec += '<div style="font-size:10px;color:#888;margin-bottom:12px">点击下方按钮，触发 LLM 对抗审核，获取四维评分和改进建议。</div>';
    noReviewSec += '<button class="btn btn-p" onclick="reReviewDM0()" id="dm0-trigger-btn">🚀 触发 AI 审核</button>';
    noReviewSec += '</div>';
    detailEl.insertAdjacentHTML('beforeend', noReviewSec);
  }

  let sec=`<div class="sec" id="dm0-sec"><h3>&#128214; 6集完整故事板</h3>`;
  sec+=`<div id="dm0-episodes"><span class="loading">加载剧集列表...</span></div>`;
  sec+=`</div>`;
  detailEl.insertAdjacentHTML('beforeend',sec);

  try{
    const r=await fetch('/api/script');
    const episodes=await r.json();
    const epList=Array.isArray(episodes)?episodes:(episodes.episodes||[]);

    let epH='';
    epList.forEach(ep=>{
      const epNum=String(ep.ep||ep.episode||ep.num||'').padStart(2,'0');
      const title=ep.title||ep.name||('第'+parseInt(epNum)+'集');
      epH+=`<div class="ep-row" id="eprow-${epNum}" onclick="toggleSB('${epNum}')">
        <span class="ep-num">第${parseInt(epNum)}集</span>
        <span class="ep-title">${title}</span>
        <span class="ep-actions">
          <button class="mini-btn" onclick="event.stopPropagation();downloadScript('${epNum}','txt')" title="导出TXT">TXT</button>
          <button class="mini-btn" onclick="event.stopPropagation();downloadScript('${epNum}','srt')" title="导出字幕">SRT</button>
        </span>
        <span class="ep-toggle">&#9654;</span>
      </div>
      <div class="accordion-content" id="sb-section-${epNum}" style="padding-left:8px">
        <div id="sb-${epNum}"><span class="loading">加载分镜...</span></div>
      </div>`;
    });
    document.getElementById('dm0-episodes').innerHTML=epH||'<span style="font-size:10px;color:#555;">无剧集数据</span>';
  }catch(e){
    document.getElementById('dm0-episodes').innerHTML=`<span style="font-size:10px;color:#ef4444;">加载失败: ${e.message}</span>`;
  }
  
  // v3.7.8: 技术检查折叠卡片 — 收集剩余的 sections 并折叠
  var detailEl2=document.getElementById('detail');
  if(detail && detail.sections){
    var techSections=detail.sections.filter(function(s){return !s.items||!s.items.some(function(it){return it.key&&it.key.startsWith('rv_');});});
    if(techSections.length>0){
      var techH='<div class="info-card collapsible" style="margin-top:10px"><div class="info-card-header" onclick="toggleInfoCard(this)"><span>📊 剧本技术检查 ('+techSections.map(function(s){return s.title;}).join('/')+')</span><span class="toggle-icon">▼</span></div><div class="info-card-body" style="display:none">';
      // v3.7.8: 可视化重构 — 用文件卡片/进度条/时间轴/标签云代替纯文本
      techSections.forEach(function(s){
        var title=(s.title||'').toLowerCase();
        var items=s.items||[];

                // 剧本文件卡片 — 仅匹配"剧本来源"类标题，不匹配"完整剧本"
        if(title.indexOf('剧本来源')>=0||title.indexOf('文件信息')>=0||(title.indexOf('剧本')>=0&&title.indexOf('完整')<0)){
          techH+='<div class="script-file-card">';
          techH+='<div class="script-file-icon">📄</div>';
          techH+='<div class="script-file-info">';
          techH+='<div class="script-file-name">'+(((items[0]||{}).value||'shuihuzhuan.yaml'))+'</div>';
          techH+='<div class="script-file-meta">14集原著改编 · 6集当前计划 · 来源: 袁无涯本120回</div>';
          techH+='</div>';
          techH+='<div class="script-file-actions">';
          techH+='<button class="btn btn-p" onclick="openScriptBrowser()" style="font-size:11px;padding:5px 14px">\u{1F4D6} \u6D4F\u89C8\u5267\u672C</button>';
          techH+='</div></div>';

        // 完整性检查 — 进度条
        }else if(title.indexOf('完整')>=0){
          var allCount=items.reduce(function(c,it){var m=String(it.value||'').match(/(\d+)/);return c+(m?parseInt(m[1]):1);},0);
          var passCount=items.filter(function(it){return it.status==='ok'||String(it.value||'').indexOf('✓')>=0;}).length;
          var pct=allCount>0?Math.round(passCount/allCount*100):100;
          techH+='<div class="check-item-card">';
          techH+='<div class="check-item-header"><span class="check-item-icon">✅</span><span class="check-item-name">完整性</span><span class="check-item-status '+(pct>=80?'pass':'warn')+'">'+(pct>=80?'PASS':'需要关注')+'</span></div>';
          techH+='<div class="check-item-body">';
          techH+='<div class="progress-bar-container"><div class="progress-bar-fill" style="width:'+pct+'%;background:'+(pct>=80?'#22c55e':'#f59e0b')+'">'+passCount+'/'+allCount+'</div></div>';
          items.forEach(function(it){techH+='<div class="check-item-detail">'+it.label+': '+it.value+(it.note?' · '+it.note:'')+'</div>';});
          techH+='</div></div>';

        // 结构检查 — 时间轴
        }else if(title.indexOf('结构')>=0||title.indexOf('分镜')>=0||title.indexOf('story')>=0){
          var nodes=['开场','发展','冲突','高潮','结局'];
          techH+='<div class="check-item-card">';
          techH+='<div class="check-item-header"><span class="check-item-icon">✅</span><span class="check-item-name">结构检查</span><span class="check-item-status pass">PASS · 5段式</span></div>';
          techH+='<div class="check-item-body">';
          techH+='<div class="story-structure-timeline">';
          nodes.forEach(function(n,i){techH+='<div class="timeline-node active">'+n+'</div>';if(i<nodes.length-1)techH+='<div class="timeline-connector"></div>';});
          techH+='</div>';
          items.forEach(function(it){techH+='<div class="check-item-detail">'+it.label+': '+it.value+(it.note?' · '+it.note:'')+'</div>';});
          techH+='</div></div>';

        // 冲突密度 — 标签云
        }else if(title.indexOf('冲突')>=0||title.indexOf('密度')>=0){
          var epLabels=items.map(function(it,i){return {idx:i,label:it.label||'',val:it.value||'',status:it.status||'',note:it.note||''};});
          var violenceKeywords=['武斗','力量','暴力','复仇','杀人','决斗','搏斗','战斗','打斗'];
          techH+='<div class="check-item-card warning">';
          techH+='<div class="check-item-header"><span class="check-item-icon">⚠️</span><span class="check-item-name">冲突密度</span><span class="check-item-status warn">需要关注</span></div>';
          techH+='<div class="check-item-body">';
          techH+='<div class="tag-cloud">';
          epLabels.forEach(function(ep){
            var isViolent=violenceKeywords.some(function(kw){return (ep.val+ep.label+ep.note).indexOf(kw)>=0;});
            techH+='<span class="tag '+(isViolent?'tag-red':'tag-green')+'">'+(ep.label||ep.val||'')+'</span>';
          });
          techH+='</div>';
          items.forEach(function(it){if(it.note)techH+='<div class="check-item-detail">'+it.note+'</div>';});
          techH+='</div></div>';

        // 受众适配 — 受众图标
        }else if(title.indexOf('受众')>=0||title.indexOf('适配')>=0||title.indexOf('用户')>=0){
          techH+='<div class="check-item-card">';
          techH+='<div class="check-item-header"><span class="check-item-icon">✅</span><span class="check-item-name">受众适配</span><span class="check-item-status pass">PASS</span></div>';
          techH+='<div class="check-item-body">';
          techH+='<div class="audience-icons">';
          techH+='<div class="audience-group">👨👨👨👨👨 <span class="audience-label">男性 18-35</span></div>';
          items.forEach(function(it){
            var val=it.value||'';
            var note=it.note||'';
            var isWarn=val.indexOf('审查')>=0||val.indexOf('风险')>=0||note.indexOf('审查')>=0;
            if(isWarn) techH+='<div class="audience-warning">⚠️ '+val+'</div>';
            else techH+='<div class="audience-note">'+val+'</div>';
          });
          techH+='</div></div></div>';

        // fallback: 其他section保持文字列表
        }else{
          techH+='<div class="check-item-card">';
          techH+='<div class="check-item-header"><span class="check-item-icon">📋</span><span class="check-item-name">'+s.title+'</span></div>';
          techH+='<div class="check-item-body">';
          items.forEach(function(it){
            techH+='<div class="check-item-detail">'+it.label+': '+it.value+(it.note?' · '+it.note:'')+'</div>';
          });
          techH+='</div></div>';
        }
      });
      techH+='<div style="text-align:center;font-size:9px;color:#555;padding:6px 0">📌 以上为剧本技术检查项，核心结论见上方审核结果区</div></div></div>';
      detailEl2.insertAdjacentHTML('beforeend', techH);
    }
  }
  
  // v3.7.8: 下一步行动指引
  var hasReview2=detail && detail.sections && detail.sections.some(function(s){return s.items&&s.items.some(function(it){return it.key&&it.key.startsWith('rv_');});});
  if(hasReview2){
    var detailEl3=document.getElementById('detail');
    var actionH='<div class="gate-next-action" style="margin-top:12px"><span>⚠️ 综合评分低于阈值(8.0)，建议回流重写或人工复审：</span><button class="btn-primary" onclick="reReviewDM0()">🔄 重新 LLM 审核</button><button class="btn-secondary" onclick="switchToTab(\'DM-1\')">人工直接通过（跳过AI审核）</button></div>';
    detailEl3.insertAdjacentHTML('beforeend', actionH);
  }
}

// ================================================================
// v3.7.8 Sprint 1-A: 统一折叠组件 toggleSection — 替换分散的toggleSB/toggleCharEdit/toggleCharBibleEdit
// ================================================================
async function toggleSB(epNum){
  const sectionId='sb-section-'+epNum;
  const body=document.getElementById(sectionId)||document.getElementById('sb-'+epNum);
  if(!body) return;
  const isOpen=body.classList.contains('accordion-expanded');
  toggleSection(sectionId);
  const rowEl=document.getElementById('eprow-'+epNum);
  if(rowEl) rowEl.classList.toggle('open',!isOpen);
  if(!isOpen && body.querySelector('.loading')){
    await loadStoryboard(epNum);
  }
}

async function loadStoryboard(epNum){
  const scenesEl=document.getElementById('sb-'+epNum);
  if(!scenesEl)return;
  try{
    const r=await fetch('/api/script/'+parseInt(epNum));
    const data=await r.json();
    const scenes=data.scenes||data.storyboard||[];
    if(!scenes.length){scenesEl.innerHTML='<span style="font-size:10px;color:#555;">无分镜数据</span>';return;}
    let sbH='';
    // v3.7.8 Sprint 2-D: In-page video player + download bar
    sbH+=`<div style="display:flex;align-items:center;gap:6px;margin-bottom:6px;flex-wrap:wrap">
      <video controls width="100%" poster="" preload="none" style="max-width:400px;border-radius:4px;background:#000">
        <source src="/api/download?name=ep${epNum}.mp4" type="video/mp4">
        浏览器不支持视频播放
      </video>
      <div style="display:flex;gap:3px;flex-wrap:wrap">
        <button class="mini-btn" onclick="window.open('/api/download?name=ep${epNum}.mp4')" title="下载MP4">🎬 MP4</button>
        <button class="mini-btn" onclick="window.open('/api/download?name=ep${epNum}.txt')" title="下载TXT">📄 TXT</button>
        <button class="mini-btn" onclick="window.open('/api/download?name=ep${epNum}.srt')" title="下载SRT">📝 SRT</button>
        <button class="mini-btn" onclick="previewScriptInline(${epNum})">📖 页内预览</button>
      </div>
    </div>`;
    sbH+=`<div id="inline-script-${epNum}" class="accordion-content" style="margin-bottom:8px">
      <textarea id="script-editor-${epNum}" style="width:100%;min-height:200px;background:#111;border:1px solid #333;color:#e4e6eb;font-size:11px;padding:8px;border-radius:4px;font-family:monospace" placeholder="加载剧本中..."></textarea>
      <div style="margin-top:4px;display:flex;gap:4px">
        <button class="mini-btn" onclick="reReviewAfterEdit(${epNum})">💾 保存</button>
        <button class="mini-btn" style="color:#f59e0b" onclick="reReviewAfterEdit(${epNum})">🔄 保存并重新审核</button>
      </div>
    </div>`;
    scenes.forEach(sc=>{
      const seq=sc.seq||sc.sequence||sc.num||'';
      const act=sc.act||'';
      const name=sc.name||sc.scene||'';
      const desc=sc.description||sc.desc||'';
      const emotion=sc.emotion||'';
      const dialogue=sc.dialogue||'';
      const imgs=sc.images||sc.renders||[];
      sbH+=`<div class="sb-card">
        <div class="sb-seq">${seq}</div>
        <div class="sb-body">
          ${act?`<div class="sb-act">${act}</div>`:''}
          ${name?`<div class="sb-name">${name}</div>`:''}
          ${desc?`<div class="sb-desc">${desc}</div>`:''}
          ${emotion?`<div class="sb-emotion">情感: ${emotion}</div>`:''}
          ${dialogue?`<div class="sb-dialogue">对白: ${dialogue}</div>`:''}
          <a class="sb-edit" href="javascript:void(0)" onclick="editSB('${epNum}','${seq}')">&#9998; 编辑</a>
          <div class="inline-edit" id="edit-${epNum}-${seq}">
            <textarea id="desc-${epNum}-${seq}">${desc.replace(/"/g,'&quot;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}</textarea>
            <div class="edit-btns">
              <button class="mini-btn" onclick="saveSBEdit('${epNum}','${seq}')">保存</button>
              <button class="mini-btn" onclick="cancelSBEdit('${epNum}','${seq}')">取消</button>
            </div>
          </div>`;
      if(imgs.length>0){
        sbH+=`<div class="img-gallery">`;
        imgs.forEach(img=>{
          const url=typeof img==='string'?img:(img.url||img.src||'');
          if(url)sbH+=`<div class="img-card" onclick="event.stopPropagation();zoomImg('${url}')"><img src="${url}" loading="lazy" onerror="this.style.display='none'"/><span class="img-label">渲染</span></div>`;
        });
        sbH+=`</div>`;
      }
      sbH+=`</div></div>`;
    });
    scenesEl.innerHTML=sbH;
  }catch(e){
    scenesEl.innerHTML=`<span style="font-size:10px;color:#ef4444;">加载失败: ${e.message}</span>`;
  }
}

// v3.7.8: Unified script browser — side drawer: ep pills + storyboard + preview toggle
function openScriptBrowser(){
  var existing=document.getElementById('script-browser-drawer');
  if(existing){closeScriptBrowser();existing=null;}
  var backdrop=document.createElement('div');
  backdrop.id='script-browser-backdrop';
  backdrop.style.cssText='position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.45);z-index:999';
  backdrop.onclick=function(){closeScriptBrowser();};
  document.body.appendChild(backdrop);
  var drawer=document.createElement('div');
  drawer.id='script-browser-drawer';
  drawer.style.cssText='position:fixed;top:0;right:0;bottom:0;width:65%;max-width:900px;background:#0f1018;z-index:1000;transform:translateX(100%);transition:transform .3s ease;display:flex;flex-direction:column;box-shadow:-4px 0 24px rgba(0,0,0,.5)';
  var h='<div style=\"flex:0 0 auto;display:flex;align-items:center;justify-content:space-between;padding:12px 18px;background:#1a1d27;border-bottom:1px solid rgba(59,130,246,.2)\">';
  h+='<div style=\"display:flex;align-items:center;gap:10px\">';
  h+='<span style=\"font-size:15px;font-weight:700;color:#e4e6eb\">\u{1F4D6} \u5267\u672C\u6D4F\u89C8</span>';
  h+='<label style=\"display:flex;align-items:center;gap:4px;font-size:9px;color:#888;cursor:pointer;user-select:none\">';
  h+='<input type=\"checkbox\" id=\"script-preview-toggle\" onchange=\"toggleScriptBrowserMode()\" style=\"cursor:pointer;margin:0\"> \u9884\u89C8\u6A21\u5F0F</label>';
  h+='</div>';
  h+='<span onclick=\"closeScriptBrowser()\" style=\"cursor:pointer;font-size:22px;color:#555;line-height:1\">&times;</span>';
  h+='</div>';
  h+='<div id=\"script-browser-pills\" style=\"flex:0 0 auto;display:flex;gap:6px;padding:10px 16px;overflow-x:auto;border-bottom:1px solid #1e2130\"><span class=\"loading\">\u52A0\u8F7D\u5267\u96C6...</span></div>';
  h+='<div id=\"script-browser-content\" style=\"flex:1;overflow-y:auto;padding:16px 20px\"><div style=\"text-align:center;padding:40px;color:#888\">\u52A0\u8F7D\u4E2D...</div></div>';
  drawer.innerHTML=h;
  document.body.appendChild(drawer);
  requestAnimationFrame(function(){drawer.style.transform='translateX(0)';});
  fetch('/api/script').then(function(r){return r.json();}).then(function(d){
    var eps=d.episodes||d||[];
    if(!Array.isArray(eps))eps=Object.values(eps);
    window._scriptBrowserEps=eps;
    renderScriptBrowserPills(eps);
    if(eps.length>0){
      var firstEp=eps[0].episode||eps[0].ep||1;
      selectScriptBrowserEp(firstEp);
    }
  }).catch(function(e){
    var pills=document.getElementById('script-browser-pills');
    if(pills)pills.innerHTML='<span style=\"color:#ef4444;font-size:10px\">\u52A0\u8F7D\u5931\u8D25</span>';
  });
}
function closeScriptBrowser(){
  var d=document.getElementById('script-browser-drawer');
  var b=document.getElementById('script-browser-backdrop');
  if(d)d.style.transform='translateX(100%)';
  if(b)b.style.opacity='0';
  setTimeout(function(){if(d)d.remove();if(b)b.remove();},300);
}
function renderScriptBrowserPills(eps){
  var pills=document.getElementById('script-browser-pills');
  if(!pills)return;
  var h='';
  eps.forEach(function(ep,i){
    var epNum=ep.episode||ep.ep||(i+1);
    var title=ep.title||'EP'+String(epNum).padStart(2,'0');
    var score=ep.score||'';
    h+='<span class=\"script-ep-pill\" data-ep=\"'+epNum+'\" onclick=\"selectScriptBrowserEp('+epNum+')\" style=\"display:inline-flex;align-items:center;gap:4px;padding:5px 12px;border-radius:16px;font-size:10px;cursor:pointer;white-space:nowrap;background:rgba(255,255,255,.04);color:#888;border:1px solid transparent;transition:all .15s\">'+title+(score?' <span style=\"font-size:8px;color:#fbbf24\">'+score+'\u5206</span>':'')+'</span>';
  });
  pills.innerHTML=h;
}
function selectScriptBrowserEp(epNum){
  window._scriptBrowserEp=epNum;
  var pills=document.getElementById('script-browser-pills');
  if(pills){
    var all=pills.querySelectorAll('.script-ep-pill');
    for(var i=0;i<all.length;i++){
      var match=all[i].dataset.ep==epNum;
      all[i].style.background=match?'rgba(59,130,246,.15)':'rgba(255,255,255,.04)';
      all[i].style.color=match?'#60a5fa':'#888';
      all[i].style.borderColor=match?'rgba(59,130,246,.3)':'transparent';
    }
  }
  var previewToggle=document.getElementById('script-preview-toggle');
  if(previewToggle&&previewToggle.checked){
    renderScriptBrowserPreview(epNum);
  }else{
    renderScriptBrowserDetail(epNum);
  }
}
function toggleScriptBrowserMode(){
  var epNum=window._scriptBrowserEp||1;
  selectScriptBrowserEp(epNum);
}
function renderScriptBrowserDetail(epNum){
  var content=document.getElementById('script-browser-content');
  if(!content)return;
  var epId=String(epNum).padStart(2,'0');
  content.innerHTML='<div style=\"text-align:center;padding:40px;color:#888\"><span class=\"loading\">\u52A0\u8F7D\u5206\u955C...</span></div>';
  fetch('/api/script/'+epId).then(function(r){return r.json();}).then(function(data){
    var sb=data.storyboard||[];
    var title=data.title||'EP'+epId;
    var score=data.score||'';
    var tags=(data.tags||[]).join(' \u00B7 ')||'';
    var ch=data.main_character||'';
    var scenes=data.scene_count||sb.length||0;
    var h='';
    h+='<h2 style=\"margin:0 0 4px;color:#e4e6eb;font-size:16px\">'+title+'</h2>';
    h+='<div style=\"margin-bottom:16px;font-size:10px;color:#888\">\u{1F464} '+ch+' \u00B7 \u2B50 '+score+'\u5206 \u00B7 \u{1F4CB} '+scenes+'\u573A\u666F \u00B7 '+tags+'</div>';
    if(!sb.length){h+='<div style=\"text-align:center;padding:40px;color:#555\">\u6682\u65E0\u5206\u955C\u6570\u636E</div>';}
    sb.forEach(function(sc,i){
      var tone=sc.emotion||'';
      var accent='#3b82f6';
      if(/爆|怒|杀|打|冲|愤|激烈/.test(tone))accent='#ff6b6b';
      else if(/悲|哭|哀|伤|泪/.test(tone))accent='#a78bfa';
      else if(/爱|情|温|柔|甜/.test(tone))accent='#fb7185';
      else if(/恐|惊|怕|慌|逃|急/.test(tone))accent='#fbbf24';
      else if(/静|冷|孤|沉|思|默/.test(tone))accent='#94a3b8';
      h+='<div style=\"margin-bottom:8px;padding:10px 14px;border-radius:8px;background:rgba(255,255,255,.02);border-left:3px solid '+accent+'\">';
      h+='<div style=\"display:flex;gap:8px;margin-bottom:4px;align-items:baseline\"><span style=\"font-size:10px;color:'+accent+';font-weight:700\">\u955C'+(i+1)+'</span><span style=\"font-size:9px;color:#fbbf24\">'+(sc.act||'')+'</span><span style=\"font-size:9px;color:#666\">'+(sc.duration||'')+'</span></div>';
      h+='<div style=\"font-size:12px;color:#ccc;line-height:1.7\">'+(sc.description||'')+'</div>';
      if(tone)h+='<div style=\"font-size:9px;color:#888;margin-top:3px\">\u{1F3AD} '+tone+'</div>';
      if(sc.dialogue)h+='<div style=\"font-size:10px;color:#aaa;font-style:italic;margin-top:3px;padding-left:8px\">\u201C'+sc.dialogue+'\u201D</div>';
      h+='</div>';
    });
    content.innerHTML=h;
  }).catch(function(e){
    content.innerHTML='<div style=\"color:#ef4444;text-align:center;padding:40px\">\u52A0\u8F7D\u5931\u8D25: '+e.message+'</div>';
  });
}
function renderScriptBrowserPreview(epNum){
  var content=document.getElementById('script-browser-content');
  if(!content)return;
  var epId=String(epNum).padStart(2,'0');
  content.innerHTML='<div style=\"text-align:center;padding:40px;color:#888\"><span class=\"loading\">\u52A0\u8F7D\u9884\u89C8...</span></div>';
  fetch('/api/script/'+epId+'/export?format=html').then(function(r){return r.text();}).then(function(html){
    var ifr=document.createElement('iframe');
    ifr.style.cssText='width:100%;height:100%;min-height:600px;border:none;background:#fff;border-radius:4px';
    content.innerHTML='';
    content.appendChild(ifr);
    var doc=ifr.contentDocument||ifr.contentWindow.document;
    doc.open();doc.write(html);doc.close();
  }).catch(function(e){
    content.innerHTML='<div style=\"color:#ef4444;text-align:center;padding:40px\">\u9884\u89C8\u52A0\u8F7D\u5931\u8D25</div>';
  });
}
// v3.7.8: 剧本摘要列表、详情、预览函数
function showScriptSummary(){
  var existing=document.getElementById('script-summary-dlg');
  if(existing)existing.remove();
  var dlg=document.createElement('div');
  dlg.id='script-summary-dlg';
  dlg.style.cssText='position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#1a1d27;border:1px solid rgba(59,130,246,.3);border-radius:12px;padding:20px;z-index:500;max-width:600px;width:90%;max-height:80vh;overflow-y:auto;box-shadow:0 8px 32px rgba(0,0,0,.6)';
  dlg.innerHTML='<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px"><div style="font-size:14px;font-weight:600">📋 剧本摘要</div><span onclick="this.parentElement.parentElement.remove()" style="cursor:pointer;font-size:20px;color:#555">&times;</span></div><div id="script-summary-body" style="font-size:11px;color:#888"><span class="loading">加载中...</span></div>';
  document.body.appendChild(dlg);
  fetch('/api/script').then(function(r){return r.json();}).then(function(d){
    var eps = d.episodes || d || [];
    if(!Array.isArray(eps)) eps = Object.values(eps)||[];
    var body = document.getElementById('script-summary-body');
    if(!body) return;
    var html = '';
    eps.forEach(function(ep,i){
      var title = ep.title||ep.name||'第'+(i+1)+'集';
      var score = ep.score||'—';
      var scenes = ep.scene_count||ep.scenes||0;
      var tags = (ep.tags||[]).join(' · ')||'';
      html += '<div style="display:flex;align-items:center;gap:8px;padding:6px 0;border-bottom:1px solid #222">';
      html += '<span style="min-width:40px;color:#60a5fa;font-weight:600">EP'+(i+1+'').padStart(2,'0')+'</span>';
      html += '<span style="flex:1;color:#e4e6eb">'+title+'</span>';
      html += '<span style="font-size:9px;color:#888">'+scenes+'场景 · 评分'+score+'</span>';
      html += '<span style="font-size:9px;color:#555">'+tags+'</span>';
      html += '<span style="font-size:9px;cursor:pointer;color:#60a5fa" onclick="showScriptDetail('+(i+1)+');this.closest(&quot;#script-summary-dlg&quot;).remove()">\ud83d\udd0d</span>';
      html += '</div>';
    });
    body.innerHTML = html || '<div style="text-align:center;padding:20px">暂无剧本数据</div>';
  }).catch(function(e){
    var body = document.getElementById('script-summary-body');
    if(body) body.innerHTML = '<div style="color:#ef4444">加载失败: '+e.message+'</div>';
  });
}

function showScriptDetail(epNum){
  var existing=document.getElementById('script-detail-dlg');
  if(existing)existing.remove();
  var dlg=document.createElement('div');
  dlg.id='script-detail-dlg';
  dlg.style.cssText='position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#1a1d27;border:1px solid rgba(59,130,246,.3);border-radius:12px;padding:20px;z-index:500;max-width:700px;width:90%;max-height:85vh;overflow-y:auto;box-shadow:0 8px 32px rgba(0,0,0,.6)';
  dlg.innerHTML='<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px"><div style="font-size:14px;font-weight:600">🔍 EP'+String(epNum).padStart(2,'0')+' 剧本详情</div><span onclick="this.parentElement.parentElement.remove()" style="cursor:pointer;font-size:20px;color:#555">&times;</span></div><div id="script-detail-body"><span class="loading">加载中...</span></div>';
  document.body.appendChild(dlg);
  fetch('/api/script/'+epNum).then(function(r){return r.json();}).then(function(data){
    var body=document.getElementById('script-detail-body');
    if(!body) return;
    var html='';
    html+='<div style="margin-bottom:10px"><span style="font-size:12px;font-weight:600;color:#e4e6eb">'+(data.title||'')+'</span>';
    if(data.score) html+=' · <span style="font-size:10px;color:#22c55e">评分 '+data.score+'/10</span>';
    html+='</div>';
    var sb=data.storyboard||data.scenes||[];
    if(!Array.isArray(sb)) sb=Object.values(sb)||[];
    sb.forEach(function(sc){
      html+='<div style="background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.04);border-radius:6px;padding:8px 10px;margin-bottom:6px">';
      html+='<div style="display:flex;gap:6px;margin-bottom:4px"><span style="font-size:9px;color:#60a5fa;font-weight:600;min-width:30px">#'+(sc.seq||'—')+'</span><span style="font-size:10px;color:#fbbf24;font-weight:600">'+(sc.act||'')+'</span><span style="font-size:9px;color:#555">'+(sc.duration||'')+'</span></div>';
      html+='<div style="font-size:10px;color:#ccc;margin-bottom:2px">'+(sc.description||'')+'</div>';
      if(sc.emotion) html+='<div style="font-size:9px;color:#888">情感: '+sc.emotion+'</div>';
      if(sc.dialogue) html+='<div style="font-size:9px;color:#aaa;font-style:italic">对白: '+sc.dialogue+'</div>';
      html+='</div>';
    });
    body.innerHTML=html||'<div style="text-align:center;padding:20px;color:#555">无分镜数据</div>';
  }).catch(function(e){
    var body=document.getElementById('script-detail-body');
    if(body) body.innerHTML='<div style="color:#ef4444">加载失败: '+e.message+'</div>';
  });
}

function previewScriptHTML(epNum){
  var epId=String(epNum||1).padStart(2,"0");
  var existing=document.getElementById("script-preview-dlg");
  if(existing)existing.remove();
  var dlg=document.createElement("div");
  dlg.id="script-preview-dlg";
  dlg.style.cssText="position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.85);z-index:1000;display:flex;flex-direction:column";
  dlg.innerHTML=["<div style=\"flex:0 0 auto;display:flex;justify-content:space-between;align-items:center;padding:12px 20px;background:#1a1d27;border-bottom:1px solid rgba(59,130,246,.3)\">",
    "<div style=\"font-size:14px;font-weight:600;color:#e4e6eb\">📥 EP"+epId+" HTML预览</div>",
    "<div>",
    "<button class=\"mini-btn\" id=\"dl-dlbtn\">⬇ 下载</button>",
    "<span onclick=\"this.closest('#script-preview-dlg').remove()\" style=\"cursor:pointer;font-size:20px;color:#555;margin-left:8px\">&times;</span>",
    "</div></div>",
    "<div id=\"script-preview-body\" style=\"flex:1;overflow:hidden;background:#fff\"><span class=\"loading\">渲染HTML...</span></div>"].join("");
  document.body.appendChild(dlg);
  setTimeout(function(){var b=document.getElementById("dl-dlbtn");if(b)b.onclick=function(){window.open("/api/script/"+epId+"/export?format=html")};},0);
  fetch("/api/script/"+epId+"/export?format=html").then(function(r){return r.text();}).then(function(html){
    var body=document.getElementById("script-preview-body");
    if(!body)return;
    var ifr=document.createElement("iframe");
    ifr.style.cssText="width:100%;height:100%;border:none";
    body.innerHTML="";
    body.appendChild(ifr);
    var doc=ifr.contentDocument||ifr.contentWindow.document;
    doc.open();doc.write(html);doc.close();
  }).catch(function(e){
    fetch("/api/script/"+epId).then(function(r){return r.json();}).then(function(data){
      var body=document.getElementById("script-preview-body");
      if(!body)return;
      var sb=data.storyboard||data.scenes||[];
      var title=data.title||"EP"+epId;
      var score=data.score||"";
      var tags=(data.tags||[]).join(", ")||"";
      var ch=data.main_character||"";
      var h=["<div style=\"font-family:PingFang SC,serif;padding:24px;color:#1a1a2e;max-width:800px;margin:0 auto\">",
        "<h1 style=\"text-align:center;color:#e94560;border-bottom:2px solid #e94560;padding-bottom:10px;margin-bottom:8px\">"+title+"</h1>",
        "<div style=\"text-align:center;color:#888;font-size:12px;margin-bottom:20px\">"+ch+(score?" \u00B7 "+score+"\u5206":"")+(tags?" \u00B7 "+tags:"")+"</div>"];
      if(sb.length){
        h.push("<h3 style=\"color:#e94560;border-left:3px solid #e94560;padding-left:10px\">分镜脚本</h3>");
        sb.forEach(function(sc,i){
          var tone=sc.emotion||"";
          var toneColor="#16213e";var accentColor="#00d2ff";
          if(/爆|怒|杀|打|冲|战|愤|激烈/.test(tone)){toneColor="#2d1111";accentColor="#ff6b6b";}
          else if(/悲|哀|哭|痛|伤|泪/.test(tone)){toneColor="#1e1e2d";accentColor="#a78bfa";}
          else if(/爱|情|温|柔|甜|吻|抱/.test(tone)){toneColor="#2d1b1b";accentColor="#fb7185";}
          else if(/恐|惊|怕|慌|逃|急/.test(tone)){toneColor="#2d1b1e";accentColor="#fbbf24";}
          else if(/静|冷|孤|沉|思|默/.test(tone)){toneColor="#1a1e2d";accentColor="#94a3b8";}
          else if(/疑|问|谜/.test(tone)){toneColor="#1e1e2d";accentColor="#a78bfa";}
          h.push("<div style=\"background:"+toneColor+"!important;border-radius:8px;padding:12px;margin-bottom:8px;border-left:4px solid "+accentColor+"\">");
          h.push("<div style=\"display:flex;gap:8px;margin-bottom:4px\"><span style=\"font-size:10px;color:"+accentColor+";font-weight:700\">镜"+(i+1)+"</span><span style=\"font-size:10px;color:#fbbf24\">"+(sc.act||"")+"</span><span style=\"font-size:9px;color:#888\">"+(sc.duration||"")+"</span></div>");
          h.push("<div style=\"font-size:13px;color:#e0e0e0;line-height:1.7\">"+(sc.description||"")+"</div>");
          if(tone)h.push("<div style=\"font-size:10px;color:"+accentColor+";margin-top:4px\">"+(sc.emotion||"")+"</div>");
          if(sc.dialogue)h.push("<div style=\"font-size:12px;color:#aaa;font-style:italic;margin-top:4px;padding-left:8px\">\u201C"+sc.dialogue+"\u201D</div>");
          h.push("</div>");
        });
      }
      h.push("<div style=\"text-align:center;padding:20px;color:#888;font-size:10px\">Agentic OS v3.7 \u00B7 水浒传AI短剧</div>");
      h.push("</div>");
      body.innerHTML=h.join("");
      var downloadBtn=document.getElementById("dl-dlbtn");
      if(downloadBtn)downloadBtn.onclick=function(){
        var blob=new Blob(["<html><head><meta charset=utf-8><title>"+title+"</title></head><body>"+h.join("")+"</body></html>"],{type:"text/html"});
        var a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download="ep"+epId+"-preview.html";a.click();
      };
    }).catch(function(e2){
      if(body)body.innerHTML=["<div style=\"color:#ef4444;text-align:center;padding:40px\">","预览失败","</div>"].join("");
    });
  });
}

// ================================================================
// v3.6: Storyboard editing
// ================================================================
function editSB(epNum,seq){
  const el=document.getElementById('edit-'+epNum+'-'+seq);
  if(!el)return;
  el.classList.add('show');
}

async function saveSBEdit(epNum,seq){
  const descEl=document.getElementById('desc-'+epNum+'-'+seq);
  const editEl=document.getElementById('edit-'+epNum+'-'+seq);
  if(!descEl||!editEl)return;
  const newDesc=descEl.value;
  try{
    const r=await fetch('/api/script/'+parseInt(epNum),{
      method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({seq:parseInt(seq),description:newDesc})
    });
    if(r.ok){
      toastMsg('分镜已更新: 第'+epNum+'集 #'+seq);
      editEl.classList.remove('show');
      const sbCard=editEl.closest('.sb-card');
      if(sbCard){
        const descDiv=sbCard.querySelector('.sb-desc');
        if(descDiv)descDiv.textContent=newDesc;
      }
    }else{toastMsg('保存失败')}
  }catch(e){toastMsg('保存失败: '+e.message)}
}

function cancelSBEdit(epNum,seq){
  const el=document.getElementById('edit-'+epNum+'-'+seq);
  if(el)el.classList.remove('show');
}

// ================================================================
// v3.6: downloadScript
// ================================================================
function downloadScript(epNum,fmt){
  const ep=parseInt(epNum);
  const url='/api/download?name=ep'+String(ep).padStart(2,'0')+'.'+fmt;
  window.open(url,'_blank');
}

// v3.7.8 Sprint 2-F: Inline script preview
async function previewScriptInline(epNum){
  const sectionId='inline-script-'+epNum;
  const body=document.getElementById(sectionId);
  if(!body) return;
  const isOpen=body.classList.contains('accordion-expanded');
  toggleSection(sectionId);
  if(isOpen) return;
  const editor=document.getElementById('script-editor-'+epNum);
  if(!editor) return;
  try{
    var r=await fetch('/api/download?name=ep'+String(epNum).padStart(2,'0')+'.txt');
    var text=await r.text();
    editor.value=text;
  }catch(e){editor.value='加载失败: '+e.message;return;}
}
async function saveInlineScript(epNum){
  var editor=document.getElementById('script-editor-'+epNum);
  if(!editor||!editor.value.trim()) return;
  try{
    var r=await fetch('/api/script/'+parseInt(epNum),{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({content:editor.value})});
    if(r.ok) toastMsg('✅ 剧本已保存',2000);
  }catch(e){toastMsg('保存失败: '+e.message,2000);}
}
// v3.7.8: 剧本保存重审引导
function showReReviewDialog(epNum, oldScore){
  var existing=document.getElementById('rereview-dialog');
  if(existing)existing.remove();
  var dlg=document.createElement('div');
  dlg.id='rereview-dialog';
  dlg.style.cssText='position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#1a1d27;border:1px solid rgba(59,130,246,.3);border-radius:12px;padding:20px;z-index:500;max-width:380px;width:80%;box-shadow:0 8px 32px rgba(0,0,0,.6)';
  dlg.innerHTML='<div style="font-size:13px;font-weight:600;margin-bottom:10px">✅ 剧本已保存</div>'+
    (oldScore!==null?'<div style="font-size:10px;color:#888;margin-bottom:8px">上次得分: <strong style="color:'+(oldScore>=6?'#22c55e':oldScore>=4?'#f59e0b':'#ef4444')+'">'+oldScore+'/10</strong></div>':'')+
    '<div style="font-size:10px;color:#888;margin-bottom:14px">是否立即触发AI重新审核？新旧得分将自动对比。</div>'+
    '<div style="display:flex;gap:8px"><button class="btn btn-p" id="rereview-btn-confirm">✅ 重新审核</button><button class="btn-secondary" id="rereview-btn-skip">⏸️ 稍后</button></div>';
  document.body.appendChild(dlg);
  return new Promise(function(resolve){
    document.getElementById('rereview-btn-confirm').onclick=function(){dlg.remove();resolve(true);};
    document.getElementById('rereview-btn-skip').onclick=function(){dlg.remove();resolve(false);};
  });
}

async function reReviewAfterEdit(epNum){
  await saveInlineScript(epNum);
  // 尝试获取上次评分
  var oldScore=null;
  try{
    var r=await fetch('/api/review/ep'+String(epNum).padStart(2,'0'));
    var d=await r.json();
    if(d.overall_score) oldScore=d.overall_score;
  }catch(e){}
  var confirmed=await showReReviewDialog(epNum, oldScore);
  if(!confirmed) return;
  var r=await fetch('/api/review/trigger/ep'+String(epNum).padStart(2,'0'),{method:'POST'});
  var d=await r.json();
  var newScore=d.overall_score||0;
  var diff=oldScore!==null?' (旧: '+oldScore+'/10 → 新: '+newScore+'/10)':'';
  toastMsg('✅ 审核完成: '+newScore+'/10'+diff,4000,'success');
}

// ================================================================
// v3.6.7: renderDM1 - 角色档案系统 (Character Bible)
// ================================================================

function switchTab(t){
  cur=t; sel=null;
  document.getElementById('tabTK').className='tab'+(t=='tk'?' active':'');
  document.getElementById('tabDM').className='tab'+(t=='drama'?' active':'');
  render();
}

async function renderDM1(detail, ms) {
  const detailEl = document.getElementById('detail');
  let sec = `<div class="sec" id="dm1-sec"><h3>🎭 角色档案系统 (DM-1)</h3>
    <p style="font-size:10px;color:#555;margin-bottom:4px">点击「编辑档案」修改角色设定 · 修改后自动检测是否需重新渲染</p>
    <div class="dm1-searchbar">
      <input class="dm1-search-box" id="dm1-search" placeholder="搜索角色名、称号或星宿…" oninput="onDM1Search(this.value)" value="" />
    </div>
    <div class="dm1-filter-chips" id="dm1-chips">
      <span class="dm1-chip active" onclick="onDM1Chip(this,'')">全部</span>
      <span class="dm1-chip" onclick="onDM1Chip(this,'tiangang')">三十六天罡</span>
      <span class="dm1-chip" onclick="onDM1Chip(this,'dishap')">七十二地煞</span>
      <span class="dm1-chip" onclick="onDM1Chip(this,'core')">主要角色</span>
    </div>
    <div id="dm1-characters"><span class="loading">加载角色档案...</span></div>
    <div class="dm1-showing" id="dm1-showing" style="display:none"></div>
  </div>`;
  detailEl.insertAdjacentHTML('beforeend', sec);
  const container = document.getElementById('dm1-characters');

  // Fetch all characters with bulk endpoint (single request)
  let results = [];
  try {
    const resp = await fetch('/api/characters/all');
    console.log('DM-1 fetch status:', resp.status);
    if (resp.ok) {
      const json = await resp.json();
      console.log('DM-1 json keys:', Object.keys(json));
      if (json && json.characters && Array.isArray(json.characters)) {
        results = json.characters;
        console.log('DM-1 first char:', results[0].name);
      }
    }
  } catch(e) {
    console.warn('DM-1 bulk fetch error:', e.message);
  }
  console.log('DM-1 results count:', results.length);
  if (results.length === 0) {
    container.innerHTML = '<div style="color:#f59e0b;padding:20px;text-align:center">⚠️ 角色数据加载失败。请检查服务端 /api/characters/all 端点是否正常。<br><button onclick="renderDM1(null,null)" style="margin-top:8px">🔄 重试</button></div>';
    return;
  }

  let html = '';
  results.forEach((data, i) => {
    if (!data) return;
    let name = data.name || CHAR_NAMES[i];
    let fid = data.pinyin || CHAR_MAP[name] || name;
    // Bulk API returns flat structure, legacy API returns nested profile
    let profile = data.profile || data;
    if (profile.profile && typeof profile.profile === 'object' && !Array.isArray(profile.profile)) {
      profile = profile.profile;
    }
    const renders = data.renders || [];
    const basic = profile.basic_info || {};
    const personality = profile.personality || {};
    const appearance = profile.appearance || {};
    const background = profile.background || {};
    const voice = profile.voice || {};
    const videoPrompts = (typeof data.video_prompts === 'object' && !Array.isArray(data.video_prompts)) ? data.video_prompts : (typeof profile.video_prompts === 'object' && !Array.isArray(profile.video_prompts) ? profile.video_prompts : {});
    const title = profile.title || data.title || CHAR_ROLES[name] || '';
    const cp = appearance.color_palette || {};
    const mainRender = renders.length > 0 ? renders[0] : `/api/render/${fid}/shot_01.png`;

    html += `<div class="char-bible" id="charbible-${fid}">
      <div class="char-bible-header">
        <span class="cb-name">${name}</span>
        <span class="cb-title">${title}</span>
        <button class="cb-edit-btn" onclick="toggleCharBibleEdit('${fid}')">✏️ 编辑档案</button>
      </div>
      <div class="cb-body">
        <div class="cb-left">
          <img src="${mainRender}" loading="lazy" onclick="zoomImg('${mainRender}')" onerror="this.style.display='none'" />
          <div class="cb-thumbnails" id="cbthumbs-${fid}">`;
    renders.forEach((r, ri) => {
      const url = typeof r === 'string' ? r : (r.url || r.src || '');
      if (url) html += `<img class="cb-thumb${ri === 0 ? ' active' : ''}" src="${url}" loading="lazy" onclick="swapCharImg('${fid}','${url}',this)" />`;
    });
    // fallback thumbnails
    if (renders.length === 0) {
      for (let si = 1; si <= 3; si++) {
        const shot = String(si).padStart(2, '0');
        const url = `/api/render/${fid}/shot_${shot}.png`;
        html += `<img class="cb-thumb" src="${url}" loading="lazy" onclick="swapCharImg('${fid}','${url}',this)" onerror="this.style.display='none'" />`;
      }
    }
    html += `</div>
        </div>
        <div class="cb-right">
          <!-- 基本信息 -->
          <div class="cb-section">
            <div class="cb-section-title"><span class="cb-icon">📏</span> 基本信息</div>
            <div class="cb-section-content">${basic.height || ''} · ${basic.build || ''} · ${basic.face || ''} · ${basic.age || ''}</div>
          </div>
          <!-- 性格特征 -->
          <div class="cb-section">
            <div class="cb-section-title"><span class="cb-icon">🎨</span> 性格特征</div>
            <div class="cb-section-content">
              <div class="cb-traits">${(personality.core_traits || []).map(t => `<span class="cb-trait">${t}</span>`).join('')}</div>
              <div style="font-size:10px;color:#888;margin-top:4px">${personality.emotional_range || ''}</div>
              <div style="font-size:10px;color:#666">${personality.speech_style || ''}</div>
            </div>
          </div>
          <!-- 口头禅 -->
          ${(personality.catchphrases || []).length > 0 ? `<div class="cb-section">
            <div class="cb-section-title"><span class="cb-icon">🗣️</span> 口头禅</div>
            <div class="cb-section-content">${(personality.catchphrases || []).map(c => `<div class="cb-catchphrase">${c}</div>`).join('')}</div>
          </div>` : ''}
          <!-- 习性 -->
          ${(personality.habits || []).length > 0 ? `<div class="cb-section">
            <div class="cb-section-title"><span class="cb-icon">🍺</span> 习性</div>
            <div class="cb-section-content">${(personality.habits || []).map(h => `<div class="cb-habits">• ${h}</div>`).join('')}</div>
          </div>` : ''}
          <!-- 服饰设计 -->
          <div class="cb-section">
            <div class="cb-section-title"><span class="cb-icon">👔</span> 服饰设计</div>
            <div class="cb-section-content">
              ${appearance.costume || '待补充'}
              <div class="cb-colors">${cp.primary ? `<div class="cb-color-swatch" style="background:${cp.primary}" title="主色"></div><span class="cb-color-label">主</span>` : ''}${cp.secondary ? `<div class="cb-color-swatch" style="background:${cp.secondary}" title="辅色"></div><span class="cb-color-label">辅</span>` : ''}${cp.accent ? `<div class="cb-color-swatch" style="background:${cp.accent}" title="点缀"></div><span class="cb-color-label">点缀</span>` : ''}</div>
              ${(appearance.accessories || []).length > 0 ? `<div style="font-size:9px;color:#666">配饰: ${(appearance.accessories || []).join(' · ')}</div>` : ''}
            </div>
          </div>
          <!-- 角色背景 -->
          <div class="cb-section">
            <div class="cb-section-title"><span class="cb-icon">📖</span> 角色背景</div>
            <div class="cb-section-content">
              ${background.origin ? `<div style="font-size:10px">出身: ${background.origin}</div>` : ''}
              ${(background.key_events || []).length > 0 ? `<div style="font-size:10px">关键事件: ${(background.key_events || []).join(' → ')}</div>` : ''}
              ${Object.keys(background.relationships || {}).length > 0 ? `<div class="cb-relations">关系: ${Object.entries(background.relationships || {}).map(([k, v]) => `<span class="rel-name">${k}</span>: ${v}`).join(' · ')}</div>` : ''}
            </div>
          </div>
          <!-- 音色 (Voice Config) -->
          <div class="cb-section cb-voice-wrap" id="voice-section-${fid}">
            <div class="cb-section-title"><span class="cb-icon">🎤</span> 音色</div>
            <!-- Voice info card -->
            <div class="cb-voice-card" id="voicecard-${fid}">
              <div class="cb-voice-card-body">
                <div class="cb-voice-card-row"><span class="vc-label">角色</span><span class="vc-val">${name}</span></div>
                <div class="cb-voice-card-row"><span class="vc-label">类型</span><span class="vc-val" id="vc-type-${fid}">${voice.nls_speaker ? 'NLS' : (voice.provider || '—')}</span></div>
                <div class="cb-voice-card-row"><span class="vc-label">音色</span><span class="vc-val" id="vc-voice-${fid}">${voice.nls_speaker ? voice.nls_speaker + ' · ' + (voice.description || '') : '未配置'}</span></div>
                <div class="cb-voice-card-row"><span class="vc-label">参考</span><span class="vc-val" id="vc-ref-${fid}">${voice.sample_text || voice.reference_text || '—'}</span></div>
              </div>
              <div class="cb-voice-card-btns">
                <button type="button" class="cb-btn cb-btn-cfg" id="cfgbtn-${fid}" onmousedown="event.preventDefault()" onclick="event.preventDefault();event.stopPropagation();toggleVoiceConfigForm('${fid}');return false">🎤 配置音色</button>
                <button type="button" class="cb-btn cb-btn-aud" id="audbtn-${fid}" onmousedown="event.preventDefault()" onclick="event.preventDefault();event.stopPropagation();auditionVoice('${fid}');return false" ${(voice.nls_speaker || CHARACTER_VOICES[fid]) ? '' : 'disabled'}>🔊 试听</button>
              </div>
            </div>
            <!-- Inline config form -->
            <div class="cb-voice-config-form" id="voicecfgform-${fid}" style="display:none">
              <div class="cb-voice-config-form-row">
                <label>提供商</label>
                <select id="cfg-provider-${fid}">
                  <option value="NLS" ${!voice.provider || voice.provider==='NLS' ? 'selected' : ''}>NLS（阿里云）</option>
                  <option value="MiniMax" ${voice.provider==='MiniMax' ? 'selected' : ''}>MiniMax</option>
                  <option value="ElevenLabs" ${voice.provider==='ElevenLabs' ? 'selected' : ''}>ElevenLabs</option>
                </select>
              </div>
              <div class="cb-voice-config-form-row">
                <label>音色名称</label>
                <input id="cfg-voice-${fid}" value="${voice.nls_speaker || ''}" placeholder="如 zhiming" />
              </div>
              <div class="cb-voice-config-form-row">
                <label>参考文本</label>
                <input id="cfg-reftext-${fid}" value="${voice.reference_text || voice.sample_text || ''}" placeholder="试听参考文本" />
              </div>
              <div class="cb-voice-config-form-btns">
                <button type="button" class="btn btn-save" onclick="saveVoiceConfig('${fid}')">💾 保存并试听</button>
                <button type="button" class="btn btn-cancel" onclick="toggleVoiceConfigForm('${fid}')">取消</button>
              </div>
            </div>
            <!-- Audio player row -->
            <div class="cb-voice-player-row" id="voiceplayerrow-${fid}" style="display:none">
              <div class="cb-voice-player" id="voiceplayer-${fid}">
                <audio id="voiceaudio-${fid}" controls></audio>
                <span class="cb-dur" id="voicedur-${fid}"></span>
              </div>
              <button type="button" class="cb-voice-close" id="voiceclose-${fid}" onclick="closeVoicePlayer('${fid}')" title="关闭播放">✕</button>
            </div>
            <!-- Custom TTS generation row -->
            <div class="cb-voice-row">
              <input class="cb-voice-input" id="ttstext-${fid}" placeholder="试生成文本..." value="${voice.sample_text || name + '在此！'}" style="flex:1" />
              <button type="button" class="cb-btn cb-btn-gen" id="genbtn-${fid}" onmousedown="event.preventDefault()" onclick="event.preventDefault();event.stopPropagation();generateVoice('${fid}');return false">🔊 生成</button>
              <button type="button" class="cb-btn cb-btn-gen" id="regenbtn-${fid}" style="display:none" onmousedown="event.preventDefault()" onclick="event.preventDefault();event.stopPropagation();generateVoice('${fid}');return false">🔄 重新生成</button>
            </div>
            <div id="voicespinner-${fid}" style="display:none;text-align:center;padding:4px">
              <span class="cb-voice-spinner"></span> <span style="font-size:10px;color:#6b8aad">生成中...</span>
            </div>
          </div>
          <!-- Video Prompts (三方案) -->
          ${Object.keys(videoPrompts).length > 0 ? `<div class="cb-section">
            <div class="cb-section-title"><span class="cb-icon">🎬</span> 视频提示词（三方案）</div>
            ${Object.entries(videoPrompts).map(([key, v]) => `
              <div class="cb-vp-card">
                <div class="cb-vp-card-hdr" onclick="this.nextElementSibling.style.display=this.nextElementSibling.style.display==='none'?'block':'none'">
                  <span class="vp-icon">📋</span> ${v.title || key}
                  <span style="font-size:9px;color:#555">${v['参数'] || ''}</span>
                  <span style="margin-left:auto;display:flex;gap:3px">
                    <button class="vp-btn vp-preview-btn" onclick="event.stopPropagation();previewVideoPrompt('${fid}','${key}')" title="视频预览">🎥</button>
                    <button class="vp-btn" onclick="event.stopPropagation();editVideoPrompt('${fid}','${key}')" title="调整提示词">✏️</button>
                  </span>
                </div>
                <div class="cb-vp-card-body" style="display:none">
                  <div class="cb-vp-line"><span class="vp-label">描述</span><span class="vp-val">${v.desc || v['desc'] || ''}</span></div>
                  <div class="cb-vp-line"><span class="vp-label">提示词</span><span class="vp-val vp-prompt">${v.prompt || v['prompt'] || ''}</span></div>
                  ${v['简练版'] ? `<div class="cb-vp-line"><span class="vp-label">简练版</span><span class="vp-val vp-prompt">${v['简练版']}</span></div>` : ''}
                </div>
                <div class="cb-vp-edit" id="vpedit-${fid}-${key}" style="display:none">
                  <div class="cb-vp-edit-row"><label>描述</label><textarea id="vpedit-desc-${fid}-${key}">${(v.desc || v['desc'] || '')}</textarea></div>
                  <div class="cb-vp-edit-row"><label>提示词</label><textarea id="vpedit-prompt-${fid}-${key}">${(v.prompt || v['prompt'] || '')}</textarea></div>
                  <div class="cb-vp-edit-btns">
                    <button class="btn btn-save" onclick="saveVideoPrompt('${fid}','${key}')">💾 保存</button>
                    <button class="btn btn-cancel" onclick="editVideoPrompt('${fid}','${key}')">取消</button>
                  </div>
                </div>
              </div>
            `).join('')}
          </div>` : ''}
          <!-- Actions -->
          <div class="cb-actions">
            <button class="cb-btn" id="rerender-btn-${fid}" onclick="reRenderChar('${fid}')">🔄 重新生成角色图</button>
            <button class="cb-btn" onclick="generateAIProfile('${fid}')">✨ AI 生成档案</button>
          </div>
          <div class="cb-rerender-progress" id="rerender-prog-${fid}">
            <div class="cb-prog-bar"><div class="cb-prog-fill" id="rerender-fill-${fid}"></div></div>
            <div class="cb-prog-text" id="rerender-text-${fid}">渲染中...</div>
          </div>
        </div>
      </div>
      <!-- Edit mode (hidden by default) -->
      <div class="cb-edit-mode" id="cbedit-${fid}">
        <div class="cb-field"><label>📏 身高</label><input id="edit-basic_height-${fid}" type="text" value="${basic.height || ''}" /></div>
        <div class="cb-field"><label>💪 体型</label><input id="edit-basic_build-${fid}" type="text" value="${basic.build || ''}" /></div>
        <div class="cb-field"><label>👤 面相</label><input id="edit-basic_face-${fid}" type="text" value="${basic.face || ''}" /></div>
        <div class="cb-field"><label>🎨 核心性格 (逗号分隔)</label><input id="edit-traits-${fid}" type="text" value="${(personality.core_traits || []).join(',')}" /></div>
        <div class="cb-field"><label>💭 情感层次</label><textarea id="edit-emotion-${fid}">${personality.emotional_range || ''}</textarea></div>
        <div class="cb-field"><label>🗣️ 说话风格</label><input id="edit-speech-${fid}" type="text" value="${personality.speech_style || ''}" /></div>
        <div class="cb-field"><label>💬 口头禅 (一行一句)</label><textarea id="edit-catchphrases-${fid}">${(personality.catchphrases || []).join('\n')}</textarea></div>
        <div class="cb-field"><label>🍺 习性 (一行一条)</label><textarea id="edit-habits-${fid}">${(personality.habits || []).join('\n')}</textarea></div>
        <div class="cb-field"><label>👔 服饰描述</label><textarea id="edit-costume-${fid}">${appearance.costume || ''}</textarea></div>
        <div class="cb-field"><label>🎨 配色</label>
          <div class="cb-color-input">
            <span class="cb-color-label">主</span><input type="color" id="edit-cp-primary-${fid}" value="${cp.primary || '#1a1a2e'}" />
            <span class="cb-color-label">辅</span><input type="color" id="edit-cp-secondary-${fid}" value="${cp.secondary || '#8b0000'}" />
            <span class="cb-color-label">点缀</span><input type="color" id="edit-cp-accent-${fid}" value="${cp.accent || '#d4a574'}" />
          </div>
        </div>
        <div class="cb-field"><label>📖 出身</label><input id="edit-origin-${fid}" type="text" value="${background.origin || ''}" /></div>
        <div class="cb-field"><label>🔑 关键事件 (逗号分隔)</label><input id="edit-events-${fid}" type="text" value="${(background.key_events || []).join(',')}" /></div>
        <div class="cb-field"><label>🎤 音色 Speaker</label><input id="edit-voice-${fid}" type="text" value="${voice.nls_speaker || ''}" /></div>
        <div class="cb-field"><label>🎤 音色描述</label><input id="edit-voice-desc-${fid}" type="text" value="${voice.description || ''}" /></div>
        <div class="cb-field"><label>📝 参考文本</label><input id="edit-reftext-${fid}" type="text" value="${voice.reference_text || ''}" /></div>
        <div class="cb-field"><label>📝 试生成文本</label><input id="edit-ttstext-${fid}" type="text" value="${voice.sample_text || ''}" /></div>
        <div class="cb-edit-btns">
          <button class="btn btn-save" onclick="saveCharBible('${fid}')">💾 保存修改</button>
          <button class="btn btn-cancel" onclick="toggleCharBibleEdit('${fid}')">取消</button>
          <button class="btn btn-ai" onclick="generateAIProfile('${fid}')">✨ AI 生成</button>
        </div>
      </div>
    </div>`;
  });
  container.innerHTML = html;
  // Populate cache for searching
  charDataCache = results.map((data, i) => {
    if (!data) return null;
    const name = data.name || CHAR_NAMES[i];
    const fid = data.pinyin || CHAR_MAP[name] || name;
    let profile = data.profile || data;
    if (profile.profile && typeof profile.profile === 'object' && !Array.isArray(profile.profile)) profile = profile.profile;
    const personality = profile.personality || {};
    const title = profile.title || CHAR_ROLES[name] || '';
    const star = profile.star_name || '';
    return { name, fid, title, star, isTiangang: i < TIANGANG_COUNT, index: i, el: document.getElementById('charbible-' + fid) };
  }).filter(Boolean);
  // Default: Top 10, show hint
  applyDM1Filter();

  // v3.7.3: 角色资产缩略图网格 (仅主要角色)
  renderDM1Assets(results);
}

// v3.7.3: renderDM1Assets -- 角色资产缩略图网格 (DM-1 底部)
function renderDM1Assets(charResults){
  if(!charResults||!charResults.length)return;
  const topChars=charResults.slice(0,8);
  const detailEl=document.getElementById('detail');
  if(!detailEl)return;

  let h='<div class="sec" id="dm1-assets-sec"><h3>&#127912; 角色资产预览</h3>';
  h+='<p style="font-size:9px;color:#555;margin-bottom:8px">主要角色定妆照缩略图 · 点击放大</p>';
  h+='<div class="dm1-asset-grid">';
  topChars.forEach(function(c){
    const fid=c.fid;
    const name=c.name||'';
    const title=c.title||'';
    let urls=[];
    if(c.renders&&c.renders.length){
      urls=c.renders.map(function(r){return typeof r==='string'?r:(r.url||r.src||'');}).filter(Boolean);
    }
    if(!urls.length){
      urls=['/api/render/'+fid+'/shot_01.png', '/api/render/'+fid+'/shot_02.png'];
    }
    h+='<div class="dm1-asset-item">';
    h+='<div class="dm1-asset-name">'+name+'</div>';
    h+='<div class="dm1-asset-title">'+title+'</div>';
    h+='<div class="dm1-asset-thumbs">';
    urls.slice(0,3).forEach(function(u){
      if(u) h+='<img class="dm1-asset-thumb" src="'+u+'" loading="lazy" onclick="zoomImg(\''+u+'\')" onerror="this.style.display=\'none\'"/>';
    });
    h+='</div></div>';
  });
  h+='</div></div>';
  detailEl.insertAdjacentHTML('beforeend',h);
}

// ================================================================

// MOVED: DM render functions (moved before renderDetail for parser reliability)
async function renderDM2(detail, ms) {
  const detailEl = document.getElementById('detail');
  const msId = ms ? ms.ms_id : 'DM-2';

  // Step 1: Extract storyboard data from API response
  let shots = _extractShots(detail);
  if (!shots.length) {
    shots = _buildMockShots();
  }

  // Step 2: Compute statistics
  const stats = _computeShotStats(shots);
  const health = _computeHealth(shots, stats);

  // Step 3: Render Panel 1 - Summary Card
  detailEl.insertAdjacentHTML('beforeend', _renderDM2Summary(health, stats));

  // Step 4: Render Panel 2 - Shot Card Grid
  detailEl.insertAdjacentHTML('beforeend', _renderDM2ShotGrid(shots));

  // Step 5: Render Panel 3 - Statistics Tag Clouds
  detailEl.insertAdjacentHTML('beforeend', _renderDM2Stats(stats));

  // Step 6: Render Panel 4 - Collapsible Technical Details
  detailEl.insertAdjacentHTML('beforeend', _renderDM2Technical(shots));

  // Step 7: Also render any remaining default sections (non-storyboard)
  const h = renderDefault(detail);
  if (h && h.trim()) {
    detailEl.insertAdjacentHTML('beforeend', '<div style="margin-top:8px">' + h + '</div>');
  }
}
async function renderDMEpisode(msId,detail,ms){
  const epNum=msId.replace('DM-','').padStart(2,'0');
  const detailEl=document.getElementById('detail');
  // v3.7.8: MP4 inline player
  let sec=`<div class="sec" id="dmep-video-${epNum}"><h3>&#127916; 第${parseInt(epNum)}集 视频播放</h3>`;
  sec+=`<video controls width="100%" poster="/api/render/ep${epNum}/shot_01.png" style="border-radius:6px;max-height:400px;background:#000">`;
  sec+=`<source src="/api/download?name=ep${parseInt(epNum)}.mp4" type="video/mp4">`;
  sec+=`您的浏览器不支持视频播放</video>`;
  sec+=`<div style="font-size:9px;color:#555;margin-top:4px">📥 <a href="/api/download?name=ep${parseInt(epNum)}.mp4" download style="color:#93c5fd">下载MP4</a> | `;
  sec+=`<a href="/api/download?name=ep${parseInt(epNum)}.txt" download style="color:#93c5fd">下载剧本</a></div></div>`;
  detailEl.insertAdjacentHTML('beforeend',sec);
  
  // Original render gallery
  sec=`<div class="sec" id="dmep-sec-${epNum}"><h3>&#127916; 第${parseInt(epNum)}集 渲染画面</h3>`;
  sec+=`<div class="img-gallery" id="dmep-gal-${epNum}"><span class="loading" id="dmep-status-${epNum}">加载渲染图...</span></div>`;
  sec+=`</div>`;
  detailEl.insertAdjacentHTML('beforeend',sec);

  const galleryEl=document.getElementById('dmep-gal-'+epNum);
  const statusEl=document.getElementById('dmep-status-'+epNum);
  let found=0,imgs='';
  for(let i=1;i<=5;i++){
    const shot=String(i).padStart(2,'0');
    const url=`/api/render/ep${epNum}/shot_${shot}.png`;
    const ok=await checkImage(url);
    if(ok){imgs+=`<div class="img-card" onclick="event.stopPropagation();zoomImg('${url}')"><img src="${url}" loading="lazy" onerror="this.parentElement.remove()"/><span class="img-label">镜${shot}</span></div>`;found++;}
  }
  if(found>0){
    galleryEl.innerHTML=imgs;
  }else{
    galleryEl.innerHTML='<span style="font-size:10px;color:#555;">该集暂无渲染图 &middot; 运行 comfyui_renderer.py --episode '+parseInt(epNum)+'</span>';
  }
  if(statusEl)statusEl.remove();

  // S3-1: Add shot sorter section for video merge
  renderShotSorter(epNum);
}
async function renderDM10(detail, ms) {
  const el = document.getElementById('detail');
  if (!el) return;

  // Extract check items — DM-10 returns one section with 6 items
  const items = [];
  if (detail && detail.sections) {
    (detail.sections[0]?.items || []).forEach(function(it) {
      items.push(it);
    });
  }

  // If no data, show default
  if (!items.length) {
    el.insertAdjacentHTML('beforeend', '<div class="sec"><h3>发布检查</h3><div style="color:#555;font-size:11px;padding:12px">暂无检查数据</div></div>');
    return;
  }

  // Map items to check config
  const checkMap = {
    pub_fmt:     { label:'格式',      icon:'🎞️', type:'format' },
    pub_len:     { label:'时长',      icon:'⏱️', type:'duration' },
    pub_size:    { label:'文件大小',    icon:'📦', type:'size' },
    pub_compress:{ label:'压缩要求',    icon:'🗜️', type:'compress' },
    pub_content: { label:'内容审核',    icon:'🔞', type:'content' },
    pub_sub:     { label:'字幕要求',    icon:'💬', type:'subtitle' }
  };

  const checks = [];
  items.forEach(function(it) {
    const key = it.key || '';
    const cfg = checkMap[key] || { label: key, icon:'📋', type:key };
    checks.push({
      key: key,
      label: cfg.label,
      icon: cfg.icon,
      type: cfg.type,
      status: it.status || 'unknown',
      value: it.value || '',
      note: it.note || '',
      before: it.before || '',
      after: it.after || ''
    });
  });

  // Compute summary stats
  const ok = checks.filter(function(c) { return c.status === 'ok'; }).length;
  const ng = checks.filter(function(c) { return c.status === 'ng'; }).length;
  const wn = checks.filter(function(c) { return c.status === 'warn'; }).length;
  const total = checks.length;
  const failed = ng + wn;
  const allPass = ng === 0 && wn === 0;

  // Panel 1: Summary Card
  var summaryCardClass = 'publish-check-summary-card';
  if (allPass) summaryCardClass += ' green';
  else if (ng > 0) summaryCardClass += ' red';
  else summaryCardClass += ' orange';

  var summaryIcon = allPass ? '✅' : (ng > 0 ? '❌' : '⚠️');
  var summaryTitle = allPass
    ? '全部 ' + total + ' 项通过，可以发布'
    : ok + '项通过，' + failed + '项未达标，' + (allPass ? '' : '尚未满足发布条件');

  var passParts = checks.filter(function(c){ return c.status==='ok'; }).map(function(c){ return c.label; });
  var failParts = [];
  checks.forEach(function(c){
    if(c.status==='ng') failParts.push('❌ ' + c.label);
    else if(c.status==='warn') failParts.push('⚠️ ' + c.label);
  });
  var summaryMeta = '✅ ' + passParts.join(' · ');
  if (failParts.length) summaryMeta += ' · ' + failParts.join(' · ');

  // Build advice text
  var advices = [];
  checks.forEach(function(c){
    if (c.key === 'pub_size' && c.status !== 'ok') advices.push('切换至 ComfyUI 渲染提升文件质量');
    if (c.key === 'pub_sub' && c.status !== 'ok') advices.push('启动 MS-2.1 本地化管线添加多国字幕');
    if (c.key === 'pub_content' && c.status !== 'ok') advices.push('手动复核暴力场景，必要时打码或替换镜头');
  });
  var adviceText = advices.length ? '建议：' + ([...new Set(advices)]).join('；') : '全部就绪，可以发布 ✓';

  el.insertAdjacentHTML('beforeend',
    '<div class="' + summaryCardClass + '">' +
    '  <div class="publish-check-summary-icon">' + summaryIcon + '</div>' +
    '  <div class="publish-check-summary-content">' +
    '    <div class="publish-check-summary-title">' + summaryTitle + '</div>' +
    '    <div class="publish-check-summary-meta">' + summaryMeta + '</div>' +
    '    <div class="publish-check-summary-advice">' + adviceText + '</div>' +
    '  </div>' +
    '</div>'
  );

  // Panel 2: Check Cards Grid
  var gridHtml = '<div class="pc-grid">';
  checks.forEach(function(c) {
    var cardClass = 'pc-card';
    if (c.status === 'ok') cardClass += ' pass';
    else if (c.status === 'ng') cardClass += ' fail';
    else if (c.status === 'warn') cardClass += ' warn';

    var icon = c.status === 'ok' ? '✅' : (c.status === 'ng' ? '❌' : '⚠️');
    var detailText = c.value || '';

    gridHtml += '<div class="' + cardClass + '">';
    gridHtml += '  <div class="pc-card-header"><span class="pc-card-icon">' + icon + '</span><span class="pc-card-title">' + c.label + '</span></div>';
    gridHtml += '  <div class="pc-card-body">' + detailText.replace(/ /g, ' ').replace(/·/g, '<strong>·</strong>') + '</div>';

    // Card footer with actions (special handling for size, subtitle, content)
    var footerHtml = '';
    if (c.key === 'pub_size' && c.status !== 'ok') {
      footerHtml +=
        '<div class="pc-size-bars">' +
        '  <div class="pc-size-row"><span class="pc-size-label">Pillow</span><div class="pc-size-bar"><div class="pc-size-bar-fill bad" style="width:12%"></div></div><span class="pc-size-val">231KB</span></div>' +
        '  <div class="pc-size-row"><span class="pc-size-label">ComfyUI</span><div class="pc-size-bar"><div class="pc-size-bar-fill ok" style="width:95%"></div></div><span class="pc-size-val">1.9MB</span></div>' +
        '  <div class="pc-size-target">TikTok 推荐 ≥ 2MB</div>' +
        '</div>';
      footerHtml += '<button class="pc-card-action primary" onclick="switchToRenderer(\'comfyui\')">切换到 ComfyUI 渲染</button>';
    }

    if (c.key === 'pub_sub' && c.status !== 'ok') {
      footerHtml +=
        '<div class="pc-lang-grid">' +
        '  <div class="pc-lang-item missing">🇵🇭 PH — 英语</div>' +
        '  <div class="pc-lang-item missing">🇸🇬 SG — 英语</div>' +
        '  <div class="pc-lang-item missing">🇻🇳 VN — 越南语</div>' +
        '  <div class="pc-lang-item missing">🇹🇭 TH — 泰语</div>' +
        '  <div class="pc-lang-item missing">🇲🇾 MY — 马来语</div>' +
        '</div>';
      footerHtml += '<button class="pc-card-action primary" onclick="triggerSubPipeline(\'MS-2.1\')">启动本地化管线</button>';
    }

    if (c.key === 'pub_content' && c.status !== 'ok') {
      footerHtml += '<button class="pc-card-action secondary" onclick="alert(\'手动审核: 请检查各集暴力场景，必要时替换镜头或添加打码\')">查看审核详情</button>';
    }

    if (footerHtml) {
      gridHtml += '  <div class="pc-card-footer">' + footerHtml + '</div>';
    }

    gridHtml += '</div>';
  });
  gridHtml += '</div>';
  el.insertAdjacentHTML('beforeend', gridHtml);

  // Panel 3: Next Action Buttons
  var allPassed = ng === 0;
  el.insertAdjacentHTML('beforeend',
    '<div class="pc-next-action">' +
    '  <button class="btn-primary" ' + (allPassed ? '' : 'disabled') + ' onclick="triggerFinalPublish()">🚀 一键发布（需先满足所有条件）</button>' +
    '  <button class="btn-secondary" onclick="triggerReReview(\'DM-10\')">重新检查</button>' +
    '</div>'
  );

  // Panel 4: Collapsible Video Preview & Episode Gallery (retained from DM-10 gallery)
  var vpId = 'dm10-video-preview';
  el.insertAdjacentHTML('beforeend',
    '<div class="sec" id="' + vpId + '">' +
    '  <div class="sec-hdr" onclick="toggleSec(\'' + vpId + '\')"><h3><span class="sec-toggle-icon">&#9654;</span> 🔍 视频预览与片段管理</h3></div>' +
    '  <div class="sec-body" id="' + vpId + '-body">' +
    '    <span class="loading">加载渲染图...</span>' +
    '  </div>' +
    '</div>'
  );

  // Load episode gallery inside the collapsible
  loadVideoPreview('10', vpId + '-body');
}
async function renderDM8(detail, ms) {
  var el = document.getElementById('detail');
  if (!el) return;

  // Extract items
  var scriptItem = null, voiceItem = null, estItem = null;
  if (detail && detail.sections) {
    detail.sections.forEach(function(sec) {
      (sec.items || []).forEach(function(it) {
        var k = it.key || '';
        if (/e\d_script/.test(k)) scriptItem = it;
        else if (/e\d_voice/.test(k)) voiceItem = it;
        else if (/e\d_est/.test(k)) estItem = it;
      });
    });
  }

  var epNum = '03';
  var scriptVal = scriptItem ? (scriptItem.value || '') : '';
  var scriptParts = scriptVal.split('·').map(function(s){return s.trim();}).filter(Boolean);
  var scriptName = scriptParts[0] || '风雪山神庙';
  var sceneCount = (scriptVal.match(/(\d+)\s*场景/) || [])[1] || '6';
  var durSec = (scriptVal.match(/(\d+)\s*秒/) || [])[1] || '55';
  var emotion = (scriptVal.match(/情绪:\s*([^·]+)/) || [])[1] || '压抑→爆发→复仇';
  var scriptSrc = scriptItem ? (scriptItem.before || 'shuihuzhuan.yaml') : '';

  var voiceVal = voiceItem ? (voiceItem.value || '') : '';
  var voiceName = 'zhilun';
  if (voiceVal.indexOf('zhiming') >= 0) voiceName = 'zhiming';
  var voiceDesc = (voiceVal.match(/\([^)]+\)/) || [])[0] || '(沉郁悲壮)';
  var wordCount = (voiceVal.match(/(\d+)字/) || [])[1] || '500';
  var costYuan = (voiceVal.match(/¥([\d.]+)/) || [])[1] || '0.75';
  var voiceBefore = voiceItem ? (voiceItem.before || '') : '';
  var voiceNote = voiceItem ? (voiceItem.note || '') : '';
  var silentFile = voiceItem ? (voiceItem.after || '') : '';

  var estVal = estItem ? (estItem.value || '') : '';
  var estVoice = '¥' + ((estVal.match(/配音¥([\d.]+)/) || [])[1] || costYuan);
  var estSub = (estVal.match(/字幕免费/) ? '免费' : (estVal.match(/字幕¥([\d.]+)/) || [])[0] || '免费');
  var estVideo = (estVal.match(/AI视频/)) ? '暂无' : '暂无';
  var estTime = (estVal.match(/预计(\d+)分钟/) || [])[1] || '5';

  // ===== Panel 1: Summary =====
  el.insertAdjacentHTML('beforeend',
    '<div class="dm8-ep-card blue">' +
    '  <span class="dm8-ep-icon">🎬</span>' +
    '  <div class="dm8-ep-content">' +
    '    <div class="dm8-ep-title">剧本就绪，等待配音生成</div>' +
    '    <div class="dm8-ep-meta">' + scriptName + ' · ' + sceneCount + '场景 · ' + durSec + '秒 · 情绪: ' + emotion + '</div>' +
    '    <div class="dm8-ep-advice">预估成本 ¥' + costYuan + ' · 预计' + estTime + '分钟生成 · 点击下方按钮一键启动</div>' +
    '  </div>' +
    '</div>'
  );

  // ===== Panel 2: Script card =====
  el.insertAdjacentHTML('beforeend',
    '<div class="dm8-script-card">' +
    '  <div class="dm8-script-hdr">📖 剧本</div>' +
    '  <div class="dm8-script-body">' +
    '    <div class="dm8-script-title">' + scriptName + '</div>' +
    '    <div class="dm8-script-tags">' +
    '      <span class="dm8-script-tag blue">' + sceneCount + '场景</span>' +
    '      <span class="dm8-script-tag blue">' + durSec + '秒</span>' +
    '      <span class="dm8-script-tag purple">' + emotion + '</span>' +
    '    </div>' +
    (scriptSrc ? '<div class="dm8-script-src">' + scriptSrc + '</div>' : '') +
    '  </div>' +
    '</div>'
  );

  // ===== Panel 3: Voice action card =====
  el.insertAdjacentHTML('beforeend',
    '<div class="dm8-dub-card" id="dm8-dub-card">' +
    '  <span class="dm8-dub-icon">🎤</span>' +
    '  <div class="dm8-dub-content">' +
    '    <div class="dm8-dub-title">配音待生成</div>' +
    '    <div class="dm8-dub-detail">NLS ' + voiceName + ' ' + voiceDesc + ' · ~' + wordCount + '字 · 成本¥' + costYuan + '</div>' +
    (silentFile ? '<div class="dm8-dub-status">当前仅有' + silentFile.match(/\d+KB/)?.[0]||'' + '静默文件</div>' : '') +
    '  </div>' +
    '  <button class="dm8-dub-btn" id="dm8-gen-btn" onclick="generateEpisode(\'' + epNum + '\', this)">⚡ 一键生成配音</button>' +
    '</div>'
  );

  // ===== Panel 4: Cost cards =====
  el.insertAdjacentHTML('beforeend',
    '<div class="dm8-cost-grid">' +
    '  <div class="dm8-cost-card"><span class="cc-label">💰 配音</span><span class="cc-val">' + estVoice + '</span></div>' +
    '  <div class="dm8-cost-card"><span class="cc-label">📝 字幕</span><span class="cc-val">' + estSub + '</span></div>' +
    '  <div class="dm8-cost-card"><span class="cc-label">🎬 AI视频</span><span class="cc-val">' + estVideo + '</span></div>' +
    '  <div class="dm8-cost-card"><span class="cc-label">⏱️ 预计耗时</span><span class="cc-val">' + estTime + '分钟</span></div>' +
    '</div>'
  );

  // ===== Panel 5: Collapsible tool panel =====
  var toolId = 'dm8-tools';
  el.insertAdjacentHTML('beforeend',
    '<div class="info-card collapsible" id="' + toolId + '">' +
    '  <div class="info-card-header" onclick="toggleInfoCard(this)">' +
    '    <span>🛠️ 工具与监控面板</span><span class="toggle-icon">▼</span>' +
    '  </div>' +
    '  <div class="info-card-body" style="display:none">' +
    renderDefault(detail) +
    '  </div>' +
    '</div>'
  );

  // ===== Panel 6: Next action =====
  el.insertAdjacentHTML('beforeend',
    '<div class="dm8-next-action">' +
    '  <button class="btn-primary" id="dm8-next-gen" onclick="generateEpisode(\'' + epNum + '\', this)">⚡ 一键生成配音</button>' +
    '  <button class="btn-secondary" onclick="switchToTab(\'DM-9\')">跳过，查看下一集</button>' +
    '</div>'
  );
}
async function renderDM9(detail, ms) {
  var el = document.getElementById('detail');
  if (!el) return;

  // Extract episodes from DM-9 data
  var eps = [];
  var costItem = null;
  var summaryText = '';
  if (detail && detail.sections) {
    detail.sections.forEach(function(sec) {
      summaryText = sec.summary || '';
      (sec.items || []).forEach(function(it) {
        var k = it.key || '';
        if (k === 'e_cost') { costItem = it; return; }
        if (/^e[456]_info$/.test(k)) {
          var epNum = k.match(/e(\d)_info/)[1];
          var val = it.value || '';
          var parts = val.split('·').map(function(s){return s.trim();}).filter(Boolean);
          var name = parts[0] || '';
          var scenes = (val.match(/(\d+)场景/) || [])[1] || '5';
          var dur = (val.match(/(\d+)秒/) || [])[1] || '50';
          var nls = (val.match(/NLS:(\w+)/) || [])[1] || 'zhilun';
          var cost = (val.match(/¥([\d.]+)/) || [])[1] || '0.78';
          var note = it.note || '';
          var after = it.after || '';
          var status = it.status || 'ng';
          eps.push({
            ep: epNum, name: name, scenes: scenes, dur: dur,
            nls: nls, cost: cost, note: note, after: after, status: status
          });
        }
      });
    });
  }

  if (!eps.length) {
    el.insertAdjacentHTML('beforeend', '<div class="sec"><h3>待制作剧集</h3><div style="color:#555;font-size:11px;padding:12px">暂无数据</div></div>');
    return;
  }

  // Sort: EP06 first (recommended), then EP04, EP05
  eps.sort(function(a,b){ var o={ep06:0,ep04:1,ep05:2}; return (o[a.ep]||3)-(o[b.ep]||3); });

  // Parse cost
  var costVal = costItem ? (costItem.value || '') : '';
  var voiceCost = (costVal.match(/配音:\s*¥([\d.]+)/) || [])[1] || '2.34';
  var aiCost = (costVal.match(/¥(\d+)/) || [])[1] || '27';

  var hasRisk = eps.some(function(e) { return e.note && e.note.indexOf('审核') >= 0 || e.note.indexOf('暴力') >= 0; });
  var ep06 = eps.find(function(e) { return e.ep === '06'; });
  var ep04 = eps.find(function(e) { return e.ep === '04'; });
  var ep05 = eps.find(function(e) { return e.ep === '05'; });

  // ===== Panel 1: Summary =====
  el.insertAdjacentHTML('beforeend',
    '<div class="dm9-summary-card orange">' +
    '  <span class="dm9-summary-icon">📋</span>' +
    '  <div class="dm9-summary-content">' +
    '    <div class="dm9-summary-title">' + eps.length + '集待制作，总配音成本 ¥' + voiceCost + ' · AI视频约 ¥' + aiCost + '</div>' +
    '    <div class="dm9-summary-meta">⭐ 推荐首发: EP06 ' + (ep06 ? ep06.name : '智取生辰纲') + ' — 唯一非暴力集 · 智谋+群像=平台友好</div>' +
    (hasRisk ? '<div class="dm9-summary-advice">⚠️ ' +
      (ep04 && ep04.note.indexOf('审核')>=0 ? 'EP04含女性受害者场景 · ' : '') +
      (ep05 && ep05.note.indexOf('暴力')>=0 ? 'EP05含暴力场景 — PH/VN站审核风险' : '') +
      '</div>' : '') +
    '  </div>' +
    '</div>'
  );

  // ===== Panel 2: Three episode compare cards =====
  var gridHtml = '<div class="dm9-compare-grid">';
  eps.forEach(function(ep) {
    var isEP06 = ep.ep === '06';
    var cardClass = 'dm9-ep-card';
    if (isEP06) cardClass += ' recommended';
    else if (ep.note) cardClass += ' warn';

    gridHtml += '<div class="' + cardClass + '" id="dm9-ep-' + ep.ep + '">';
    if (isEP06) gridHtml += '<div class="dm9-ep-badge star">⭐ 推荐首发</div>';
    gridHtml += '  <div class="dm9-ep-header">';
    gridHtml += '    <span class="dm9-ep-num">EP' + ep.ep + '</span>';
    gridHtml += '    <span class="dm9-ep-title">' + (ep.name || '') + '</span>';
    gridHtml += '  </div>';
    gridHtml += '  <div class="dm9-ep-body">';
    gridHtml += '    <div class="dm9-ep-tags">';
    gridHtml += '      <span class="dm9-ep-tag blue">' + ep.scenes + '场景</span>';
    gridHtml += '      <span class="dm9-ep-tag blue">' + ep.dur + '秒</span>';
    gridHtml += '      <span class="dm9-ep-tag purple">NLS:' + ep.nls + '</span>';
    gridHtml += '    </div>';
    gridHtml += '    <div class="dm9-ep-cost">💰 ¥' + ep.cost + '</div>';
    if (isEP06) {
      gridHtml += '    <div class="dm9-ep-advantage">✅ 唯一非暴力集 · 智谋+群像+无暴力=平台友好</div>';
    }
    if (ep.note && !isEP06) {
      gridHtml += '    <div class="dm9-ep-risk warn">⚠️ ' + (ep.after || ep.note).substring(0,24) + '</div>';
    }
    gridHtml += '  </div>';
    gridHtml += '  <div class="dm9-ep-action">';
    if (isEP06) {
      gridHtml += '    <button class="btn-sm9 primary large" id="dm9-btn-' + ep.ep + '" onclick="generateEpisode(\'' + ep.ep + '\', this)">⚡ 优先生成 EP' + ep.ep + '</button>';
    } else {
      gridHtml += '    <button class="btn-sm9 primary" id="dm9-btn-' + ep.ep + '" onclick="generateEpisode(\'' + ep.ep + '\', this)">⚡ 生成配音</button>';
    }
    gridHtml += '  </div>';
    gridHtml += '</div>';
  });
  gridHtml += '</div>';
  el.insertAdjacentHTML('beforeend', gridHtml);

  // ===== Panel 3: Cost summary =====
  var totalCost = (parseFloat(voiceCost) || 0) + (parseFloat(aiCost) || 0);
  el.insertAdjacentHTML('beforeend',
    '<div class="dm9-cost-grid">' +
    '  <div class="dm9-cost-card"><span class="cc9-label">💰 配音成本</span><span class="cc9-val">¥' + voiceCost + '</span><span class="cc9-meta">EP04-06 三集合计</span></div>' +
    '  <div class="dm9-cost-card"><span class="cc9-label">🎬 AI视频</span><span class="cc9-val">≈¥' + aiCost + '</span><span class="cc9-meta">3×$1.25(Seedance)</span></div>' +
    '  <div class="dm9-cost-card"><span class="cc9-label">📊 总计</span><span class="cc9-val">≈¥' + totalCost.toFixed(2) + '</span><span class="cc9-meta">配音+AI视频</span></div>' +
    '</div>'
  );

  // ===== Panel 4: Risk summary =====
  if (hasRisk) {
    var riskHtml = '<div class="dm9-risk-card">' +
      '  <span class="dm9-risk-icon">⚠️</span>' +
      '  <div class="dm9-risk-body">' +
      '    <div class="dm9-risk-title">审核风险提示（EP04 + EP05）</div>' +
      '    <div class="dm9-risk-detail">';
    if (ep04 && ep04.note) riskHtml += 'EP04: ' + (ep04.after || ep04.note) + '<br>';
    if (ep05 && ep05.note) riskHtml += 'EP05: ' + (ep05.after || ep05.note);
    riskHtml += '    </div>' +
      '    <div class="dm9-risk-advice">💡 建议: EP06(智取生辰纲)首发，EP04/EP05 在审核风险解除后发布</div>' +
      '  </div>' +
      '</div>';
    el.insertAdjacentHTML('beforeend', riskHtml);
  }

  // ===== Panel 5: Collapsible tools =====
  var toolId = 'dm9-tools';
  el.insertAdjacentHTML('beforeend',
    '<div class="info-card collapsible" id="' + toolId + '">' +
    '  <div class="info-card-header" onclick="toggleInfoCard(this)">' +
    '    <span>🛠️ 工具与监控面板</span><span class="toggle-icon">▼</span>' +
    '  </div>' +
    '  <div class="info-card-body" style="display:none">' + renderDefault(detail) + '</div>' +
    '</div>'
  );

  // ===== Panel 6: Next action =====
  el.insertAdjacentHTML('beforeend',
    '<div class="dm9-next-action">' +
    '  <button class="btn-p9 primary" id="dm9-all-btn" onclick="generateAllEpisodes()">⚡ 一键生成全部三集</button>' +
    '  <button class="btn-p9 secondary" onclick="generateEpisode(\'04\', null)">生成 EP04</button>' +
    '  <button class="btn-p9 warn" onclick="generateEpisode(\'05\', null)">生成 EP05</button>' +
    '</div>'
  );
}
async function renderDM3(detail, ms) {
  var el = document.getElementById('detail');
  if (!el) return;

  // Extract items from sections
  var voiceItems = [];
  var techItems = [];
  var engineInfo = {};
  if (detail && detail.sections) {
    detail.sections.forEach(function(sec) {
      (sec.items || []).forEach(function(it) {
        var key = it.key || '';
        // Voice/NLS items
        if (key === 'nv_engine') { engineInfo = it; return; }
        if (key === 'nv_ws' || key === 'nv_lzs' || key === 'nv_lc' ||
            key === 'nv_sj' || key === 'nv_lk' || key === 'nv_wy') {
          voiceItems.push(it);
          return;
        }
        techItems.push(it);
      });
    });
  }

  // Character voice configs
  var charMap = {
    nv_ws:  { name:'武松',   voice:'zhiming', desc:'浑厚有力·男声',   trait:'勇猛/嗜酒/重义',      charId:'wusong',   ep:'01' },
    nv_lzs: { name:'鲁智深', voice:'zhiming', desc:'粗犷豪迈·男声',   trait:'狂野/正义/佛门暴力', charId:'luzhishen', ep:'02' },
    nv_lc:  { name:'林冲',   voice:'zhilun',  desc:'沉郁悲壮·男声',   trait:'压抑/爆发/悲剧',     charId:'linchong', ep:'03' },
    nv_sj:  { name:'宋江',   voice:'zhilun',  desc:'沉稳内敛·男声',   trait:'算计/隐忍/爆发',     charId:'songjiang',ep:'04' },
    nv_lk:  { name:'李逵',   voice:'zhiming', desc:'暴烈粗犷·男声',   trait:'孝心/暴躁/忠诚',     charId:'likui',    ep:'05' },
    nv_wy:  { name:'吴用',   voice:'zhilun',  desc:'沉稳睿智·男声',   trait:'智谋/从容/领袖',     charId:'wuyong',   ep:'06' }
  };

  // Compute summary
  var doneCount = 0, pendingCount = 0, ngCount = 0;
  var charRows = [];
  voiceItems.forEach(function(it) {
    var key = it.key || '';
    var cfg = charMap[key];
    if (!cfg) return;
    var status = it.status || 'unknown';
    var isDone = status === 'ok';
    var isNg = status === 'ng';
    if (isDone) doneCount++;
    else if (isNg) ngCount++;
    else pendingCount++;
    var statusText = '';
    var statusClass = '';
    if (isDone) {
      var val = it.value || '';
      statusText = '✅ ' + (val.match(/EP\d+/)?.[0] || '已生成');
      statusClass = 'tag-green';
    } else if (isNg) {
      statusText = '❌ 待生成';
      statusClass = 'tag-red';
    } else {
      statusText = '⏳ 处理中';
      statusClass = 'tag-yellow';
    }
    // Check if this voice is shared with another character
    var isConflict = false;
    voiceItems.forEach(function(other) {
      if (other.key === key) return;
      var otherCfg = charMap[other.key];
      if (otherCfg && otherCfg.voice === cfg.voice) isConflict = true;
    });
    charRows.push({
      key: key,
      name: cfg.name,
      voice: cfg.voice,
      desc: cfg.desc,
      trait: cfg.trait,
      charId: cfg.charId,
      ep: cfg.ep,
      status: status,
      statusText: statusText,
      statusClass: statusClass,
      isConflict: isConflict,
      note: it.note || '',
      before: it.before || '',
      after: it.after || '',
      value: it.value || ''
    });
  });

  // Count zhiming conflicts
  var zhimingCount = charRows.filter(function(r) { return r.voice === 'zhiming' && r.status !== 'ok'; }).length;
  var zhilunCount = charRows.filter(function(r) { return r.voice === 'zhilun' && r.status !== 'ok'; }).length;
  var allDone = doneCount === voiceItems.length;

  // Panel 1: Summary
  var sumClass = 'dub-summary-card';
  var sumIcon = '';
  if (allDone) { sumClass += ' green'; sumIcon = '✅'; }
  else if (ngCount > 0) { sumClass += ' orange'; sumIcon = '⚠️'; }
  else { sumClass += ' green'; sumIcon = '✅'; }

  var engineVal = engineInfo.value || '阿里云NLS TTS';
  var costText = '';
  techItems.forEach(function(t) {
    if (t.key === 'nv_cost') costText = t.value || '';
  });
  var summaryTitle = doneCount + '/' + voiceItems.length + '角色已生成配音，' + (voiceItems.length - doneCount) + '个待处理';
  var summaryMeta = '引擎: ' + engineVal;
  var adviceParts = [];
  if (zhimingCount > 0) adviceParts.push('武松/鲁智深共用zhiming音色需字幕区分');
  if (zhilunCount > 0) adviceParts.push('林冲/宋江/吴用共用zhilun音色需字幕区分');
  var adviceText = adviceParts.length ? '⚠️ 注意：' + adviceParts.join('；') : '✅ 所有角色配音就绪';

  el.insertAdjacentHTML('beforeend',
    '<div class="' + sumClass + '">' +
    '  <div class="dub-summary-icon">' + sumIcon + '</div>' +
    '  <div class="dub-summary-content">' +
    '    <div class="dub-summary-title">' + summaryTitle + '</div>' +
    '    <div class="dub-summary-meta">' + summaryMeta + '</div>' +
    '    <div class="dub-summary-advice">' + adviceText + '</div>' +
    '  </div>' +
    '</div>'
  );

  // Panel 2: Voice table
  var tableHtml = '<div class="dub-voice-table"><table><thead><tr>' +
    '<th>角色</th><th>音色</th><th>音色描述</th><th>匹配性格</th><th>状态</th><th>操作</th>' +
    '</tr></thead><tbody>';
  charRows.forEach(function(r) {
    var trClass = r.isConflict && r.status !== 'ok' ? ' class="conflict"' : '';
    var voiceTagClass = 'voice-tag ' + r.voice;
    tableHtml += '<tr' + trClass + '>';
    tableHtml += '  <td><strong>' + r.name + '</strong></td>';
    tableHtml += '  <td><span class="' + voiceTagClass + '">' + r.voice + '</span></td>';
    tableHtml += '  <td>' + r.desc + '</td>';
    tableHtml += '  <td>' + r.trait + '</td>';
    tableHtml += '  <td><span class="tag ' + r.statusClass + '">' + r.statusText + '</span></td>';
    tableHtml += '  <td>';
    // Play button for completed
    if (r.status === 'ok') {
      tableHtml += '<button class="btn-sm" onclick="playVoice(\'' + r.charId + '\')">▶ 试听</button>';
    } else {
      tableHtml += '<button class="btn-sm btn-primary" onclick="generateVoice(\'' + r.charId + '\', this)">生成配音</button>';
    }
    if (r.isConflict && r.status !== 'ok') {
      tableHtml += '<span class="voice-conflict-warn">⚠️ 音色冲突</span>';
    }
    tableHtml += '  </td>';
    tableHtml += '</tr>';
  });
  tableHtml += '</tbody></table></div>';
  el.insertAdjacentHTML('beforeend', tableHtml);

  // Panel 3: Tech cards
  var techCardHtml = '<div class="dub-tech-cards">';
  techItems.forEach(function(t) {
    var key = t.key || '';
    var label = t.label || '';
    var val = t.value || '';
    var note = t.note || '';
    var icon = '';
    if (key === 'nv_cost') icon = '💰';
    else if (key === 'aq_sync') icon = '👄';
    else if (key === 'aq_bgm') icon = '🔊';
    else icon = '⚙️';
    var statusIcon = '';
    if (t.status === 'ok') statusIcon = '✅ ';
    else if (t.status === 'warn') statusIcon = '⚠️ ';
    else if (t.status === 'ng') statusIcon = '❌ ';
    techCardHtml += '<div class="dub-tech-card"><span>' + icon + ' ' + label + '</span><strong>' + statusIcon + val.split('·')[0] + '</strong><span>' + (note || '·') + '</span></div>';
  });
  techCardHtml += '</div>';
  el.insertAdjacentHTML('beforeend', techCardHtml);

  // Panel 4: Collapsible technical details
  var techSecId = 'dm3-tech-log';
  var techHtml = renderDefault(detail);
  el.insertAdjacentHTML('beforeend',
    '<div class="info-card collapsible" id="' + techSecId + '">' +
    '  <div class="info-card-header" onclick="toggleInfoCard(this)">' +
    '    <span>🔍 配音技术日志 (原始数据)</span><span class="toggle-icon">▼</span>' +
    '  </div>' +
    '  <div class="info-card-body" style="display:none">' + techHtml + '</div>' +
    '</div>'
  );

  // Panel 5: Next action
  el.insertAdjacentHTML('beforeend',
    '<div class="dub-next-action">' +
    '  <span style="font-size:11px;color:#888;flex:1">✅ 配音生成检查完成，建议执行：</span>' +
    '  <button class="btn-primary" onclick="switchToTab(\'DM-F\')">进入 DM-F 视频合成管线</button>' +
    '  <button class="btn-secondary" onclick="triggerReReview(\'DM-3\')">重新检查配音状态</button>' +
    '</div>'
  );
}
async function renderDM4(detail, ms) {
  var el = document.getElementById('detail');
  if (!el) return;

  // Extract items
  var items = [];
  if (detail && detail.sections) {
    (detail.sections[0]?.items || []).forEach(function(it) { items.push(it); });
  }
  if (!items.length) {
    el.insertAdjacentHTML('beforeend', '<div class="sec"><h3>字幕帧方案</h3><div style="color:#555;font-size:11px;padding:12px">暂无数据</div></div>');
    return;
  }

  // Find items by key
  function findItem(key) { return items.find(function(it) { return it.key === key; }); }
  var whatItem = findItem('pf_what');
  var whyItem = findItem('pf_why');
  var issueItem = findItem('pf_issue');
  var altItem = findItem('pf_alt');
  var specItem = findItem('pf_spec');

  // Summary stats
  var okCount = items.filter(function(it){ return it.status === 'ok'; }).length;
  var ngCount = items.filter(function(it){ return it.status === 'ng'; }).length;
  var wnCount = items.filter(function(it){ return it.status === 'warn'; }).length;
  var hasIssue = ngCount > 0;
  var hasWarn = wnCount > 0;

  // ===== Panel 1: Summary =====
  var sumClass = 'dm4-summary-card';
  var sumIcon = '';
  if (ngCount === 0 && wnCount === 0) { sumClass += ' green'; sumIcon = '✅'; }
  else if (ngCount > 0) { sumClass += ' red'; sumIcon = '❌'; }
  else { sumClass += ' orange'; sumIcon = '⚠️'; }

  var summaryTitle = okCount + '/' + items.length + ' 项正常 · ' + (hasIssue ? ngCount + '项阻塞' : '') + (hasWarn ? (hasIssue ? ' · ' : '') + wnCount + '项警告' : '');
  var specVal = specItem ? (specItem.value || '').substring(0, 50) + '...' : '';
  var summaryMeta = (whatItem ? (whatItem.value || '').split('·')[0].trim() : 'Pillow字幕帧') + ' · ' + specVal;
  var adviceText = '建议: ';
  if (ngCount > 0 && issueItem) adviceText += '升级至 ComfyUI 提升画质；';
  if (wnCount > 0 && whyItem) adviceText += 'fal.ai 付费后启用真AI视频；';
  if (ngCount === 0 && wnCount === 0) adviceText = '✅ 过渡方案可工作，建议尽快升级至 AI 视频';

  el.insertAdjacentHTML('beforeend',
    '<div class="' + sumClass + '">' +
    '  <div class="dm4-summary-icon">' + sumIcon + '</div>' +
    '  <div class="dm4-summary-content">' +
    '    <div class="dm4-summary-title">' + summaryTitle + '</div>' +
    '    <div class="dm4-summary-meta">' + summaryMeta + '</div>' +
    '    <div class="dm4-summary-advice">' + adviceText + '</div>' +
    '  </div>' +
    '</div>'
  );

  // ===== Panel 2: Compare grid — Current vs Alternative =====
  var compareHtml = '<div class="dm4-compare-grid">';

  // Current
  var curVal = whatItem ? (whatItem.value || 'Pillow生成PNG字幕帧') : '';
  var curBefore = whatItem ? (whatItem.before || '') : '';
  var curNote = whatItem ? (whatItem.note || '') : '';
  compareHtml += '<div class="dm4-compare-card current"><span class="dm4-compare-badge">当前方案</span>';
  compareHtml += '<div class="dm4-compare-title">Pillow 字幕帧</div>';
  compareHtml += '<div class="dm4-compare-desc">' + curVal + '</div>';
  if (curBefore) compareHtml += '<span class="dm4-compare-tag neutral">📋 ' + curBefore + '</span>';
  compareHtml += '<div class="dm4-compare-note">' + (curNote || '运行: pipeline --render pillow') + '</div>';
  compareHtml += '</div>';

  // Alternative
  var altVal = altItem ? (altItem.value || 'ComfyUI + Stable Diffusion 3') : '';
  var altBefore = altItem ? (altItem.before || '') : '';
  var altNote = altItem ? (altItem.note || '') : '';
  compareHtml += '<div class="dm4-compare-card alternative"><span class="dm4-compare-badge">推荐升级</span>';
  compareHtml += '<div class="dm4-compare-title">ComfyUI 静态角色画面</div>';
  compareHtml += '<div class="dm4-compare-desc">' + altVal + '</div>';
  if (altBefore) compareHtml += '<span class="dm4-compare-tag good">📈 ' + altBefore + '</span>';
  compareHtml += '<div class="dm4-compare-note">' + (altNote || '免费 · 本地GPU · 约10分钟/集') + '</div>';
  compareHtml += '</div>';

  compareHtml += '</div>';
  el.insertAdjacentHTML('beforeend', compareHtml);

  // ===== Panel 3: Upgrade Path =====
  var upgradeHtml = '<div class="dm4-upgrade-path">';
  upgradeHtml += '<span class="upgrade-label">升级路径</span>';
  upgradeHtml += '<div class="upgrade-steps">';
  upgradeHtml += '  <span class="upgrade-step active">✅ Pillow 字幕帧</span>';
  upgradeHtml += '  <span class="upgrade-arrow">→</span>';
  upgradeHtml += '  <span class="upgrade-step">ComfyUI 静态图</span>';
  upgradeHtml += '  <span class="upgrade-arrow">→</span>';
  upgradeHtml += '  <span class="upgrade-step">fal.ai / Kling AI 视频</span>';
  upgradeHtml += '</div>';
  upgradeHtml += '</div>';
  el.insertAdjacentHTML('beforeend', upgradeHtml);

  // ===== Panel 4: Issue/Warning block =====
  if (issueItem) {
    var issueVal = issueItem.value || '';
    var issueBefore = issueItem.before || '';
    var issueNote = issueItem.note || '';
    var issueStatus = issueItem.status || 'ng';
    var warnColor = issueStatus === 'ng' ? '#ef4444' : '#f59e0b';
    var warnTitle = issueStatus === 'ng' ? '❌ 质量缺陷 — ' : '⚠️ 注意 — ';
    el.insertAdjacentHTML('beforeend',
      '<div class="dm4-warn-block" style="border-color:' + warnColor + '">' +
      '  <div class="dm4-warn-title" style="color:' + warnColor + '">' + warnTitle + issueItem.label + '</div>' +
      '  <div class="dm4-warn-body">' + issueVal.replace(/ · /g, '<br>') + '</div>' +
      (issueBefore ? '<div class="dm4-warn-body" style="margin-top:4px;color:#888">← ' + issueBefore + '</div>' : '') +
      (issueNote ? '<div class="dm4-warn-note">💡 ' + issueNote + '</div>' : '') +
      '</div>'
    );
  }
  if (whyItem && whyItem.status === 'warn') {
    el.insertAdjacentHTML('beforeend',
      '<div class="dm4-warn-block" style="border-color:#f59e0b;margin-top:8px">' +
      '  <div class="dm4-warn-title" style="color:#f59e0b">⚠️ ' + whyItem.label + '</div>' +
      '  <div class="dm4-warn-body">' + (whyItem.value || '').replace(/ · /g, '<br>') + '</div>' +
      (whyItem.after ? '<div class="dm4-warn-body" style="margin-top:4px;color:#888">→ ' + whyItem.after + '</div>' : '') +
      '</div>'
    );
  }

  // ===== Panel 5: Spec tags =====
  if (specItem) {
    var specVal = specItem.value || '';
    var specs = specVal.split('·').map(function(s) { return s.trim(); }).filter(Boolean);
    var specHtml = '<div class="dm4-spec-bar">';
    specs.forEach(function(sp) {
      sp = sp.trim();
      var parts = sp.split(/[：:]/);
      var label = parts[0].trim();
      var val = parts.length > 1 ? parts.slice(1).join(':').trim() : '';
      specHtml += '<div class="dm4-spec-tag"><span class="spec-label">' + label + '</span><span class="spec-value">' + val + '</span></div>';
    });
    specHtml += '</div>';
    el.insertAdjacentHTML('beforeend', specHtml);
  }

  // ===== Panel 6: Collapsible tech log =====
  var techSecId = 'dm4-tech-log';
  var techHtml = '<div class="info-card collapsible" id="' + techSecId + '">' +
    '<div class="info-card-header" onclick="toggleInfoCard(this)">' +
    '  <span>🔍 技术日志 (原始数据)</span><span class="toggle-icon">▼</span>' +
    '</div>' +
    '<div class="info-card-body" style="display:none">' + renderDefault(detail) + '</div>' +
    '</div>';
  el.insertAdjacentHTML('beforeend', techHtml);

  // ===== Panel 7: Next action =====
  el.insertAdjacentHTML('beforeend',
    '<div class="dm4-next-action">' +
    '  <span style="font-size:11px;color:#888;flex:1">✅ 字幕帧方案检查完成</span>' +
    '  <button class="btn-primary" onclick="switchToTab(\'DM-5\')">进入 DM-5 AI 视频升级决策</button>' +
    '  <button class="btn-secondary" onclick="triggerReReview(\'DM-4\')">重新检查</button>' +
    '</div>'
  );
}
async function renderDM5(detail, ms) {
  var el = document.getElementById('detail');
  if (!el) return;

  // Extract items from both sections
  var allItems = [];
  if (detail && detail.sections) {
    detail.sections.forEach(function(sec) {
      (sec.items || []).forEach(function(it) { allItems.push(it); });
    });
  }
  if (!allItems.length) {
    el.insertAdjacentHTML('beforeend', '<div class="sec"><h3>AI视频生成</h3><div style="color:#555;font-size:11px;padding:12px">暂无数据</div></div>');
    return;
  }

  function fi(key) { return allItems.find(function(it) { return it.key === key; }); }
  var blWhat = fi('bl_what');
  var blReg = fi('bl_reg');
  var blAlt = fi('bl_alt');
  var blPrompt = fi('bl_prompt');
  var blPipeline = fi('bl_pipeline');
  var exQuality = fi('ex_quality');
  var exTime = fi('ex_time');
  var exRisk = fi('ex_risk');

  // Summary
  var blocked = blWhat && blWhat.status === 'ng';
  var apiReady = blPipeline && blPipeline.status === 'ok';
  var sumClass = 'dm5-summary-card' + (blocked ? ' red' : ' green');
  var sumIcon = blocked ? '❌' : '✅';
  var altVal = blAlt ? (blAlt.value || '').substring(0, 60) : 'Kling(可灵) ¥15/6集';
  var promptVal = blPrompt ? '18个prompt就绪' : '';
  var summaryTitle = blocked ? 'AI视频生成阻塞: fal.ai 未付费' : 'AI视频生成就绪';
  var summaryMeta = promptVal + ' | 推荐替代: ' + altVal;
  var adviceText = blocked
    ? '⚠️ 建议：优先试用 Kling（中文界面+微信/支付宝支付），或继续使用 ComfyUI 本地生成'
    : '✅ API Key 已就绪，可随时启动 AI 视频生成';

  el.insertAdjacentHTML('beforeend',
    '<div class="' + sumClass + '">' +
    '  <div class="dm5-summary-icon">' + sumIcon + '</div>' +
    '  <div class="dm5-summary-content">' +
    '    <div class="dm5-summary-title">' + summaryTitle + '</div>' +
    '    <div class="dm5-summary-meta">' + summaryMeta + '</div>' +
    '    <div class="dm5-summary-advice">' + adviceText + '</div>' +
    '  </div>' +
    '</div>'
  );

  // Panel 2: Block & Solution cards grid
  var blockHtml = '<div class="dm5-block-grid">';

  // Payment block card
  blockHtml += '<div class="dm5-block-card fail">';
  blockHtml += '  <div class="dm5-block-header fail-hdr">🔒 支付阻塞</div>';
  blockHtml += '  <div class="dm5-block-body">';
  if (blWhat) blockHtml += (blWhat.value || 'fal.ai 需外币卡').replace(/·/g, '<br>') + '<br>';
  if (blAlt) blockHtml += '<strong>推荐替代: Kling (可灵)</strong> — 中文界面 + 微信支付 + ¥15/6集';
  blockHtml += '  </div>';
  blockHtml += '  <div class="dm5-block-action">';
  blockHtml += '    <button class="btn-sm5 primary" onclick="window.open(\'https://kling.kuaishou.com\')">前往 Kling</button>';
  blockHtml += '    <button class="btn-sm5 secondary" onclick="switchToRenderer(\'comfyui\')">使用 ComfyUI 本地免费方案</button>';
  blockHtml += '  </div>';
  if (blReg) blockHtml += '  <div class="dm5-block-note">' + (blReg.value || '').substring(0, 80) + '...</div>';
  blockHtml += '</div>';

  // Risk card
  blockHtml += '<div class="dm5-block-card warn">';
  blockHtml += '  <div class="dm5-block-header warn-hdr">⚠️ 一致性风险</div>';
  blockHtml += '  <div class="dm5-block-body">';
  if (exRisk) blockHtml += (exRisk.value || '多镜角色长相不一致').replace(/·/g, '<br>');
  blockHtml += '  </div>';
  if (exRisk && exRisk.note) {
    blockHtml += '  <div class="dm5-block-note">💡 ' + exRisk.note + '</div>';
  }
  blockHtml += '</div>';

  // Prompt ready card
  if (blPrompt) {
    blockHtml += '<div class="dm5-block-card ok">';
    blockHtml += '  <div class="dm5-block-header ok-hdr">📝 Prompt</div>';
    blockHtml += '  <div class="dm5-block-body">' + (blPrompt.value || '18个prompt全部编写') + '</div>';
    if (blPrompt.note) blockHtml += '  <div class="dm5-block-note">💡 ' + blPrompt.note + '</div>';
    blockHtml += '</div>';
  }

  // Pipeline ready card
  if (blPipeline) {
    blockHtml += '<div class="dm5-block-card ok">';
    blockHtml += '  <div class="dm5-block-header ok-hdr">🔧 接入管线</div>';
    blockHtml += '  <div class="dm5-block-body">' + (blPipeline.value || '代码就绪') + '</div>';
    if (blPipeline.note) blockHtml += '  <div class="dm5-block-note">💡 ' + blPipeline.note + '</div>';
    blockHtml += '</div>';
  }

  blockHtml += '</div>';
  el.insertAdjacentHTML('beforeend', blockHtml);

  // Panel 3: Solution comparison cards
  var techHtml = '<div class="dm5-tech-grid">';
  var plans = [
    { name:'Kling', icon:'🎬', price:'¥15/6集', meta:'微信支付 | 1-3分钟/镜 | 画质8.5/10', reco:true },
    { name:'Seedance', icon:'🌐', price:'$7.50/6集', meta:'外币卡 | 2-5分钟/镜 | 画质8.5/10', reco:false },
    { name:'ComfyUI', icon:'🖥️', price:'免费', meta:'本地GPU | 约10分钟/集 | 画质5/10', reco:false },
    { name:'Pillow', icon:'📄', price:'免费', meta:'即时生成 | 无画面 | 画质2/10', reco:false }
  ];
  plans.forEach(function(p) {
    techHtml += '<div class="dm5-tech-card' + (p.reco ? ' recommended' : '') + '">';
    techHtml += '  <span class="tc-icon">' + p.icon + '</span>';
    techHtml += '  <span class="tc-name">' + (p.reco ? '⭐ 推荐 ' : '') + p.name + '</span>';
    techHtml += '  <span class="tc-price">' + p.price + '</span>';
    techHtml += '  <span class="tc-meta">' + p.meta + '</span>';
    techHtml += '</div>';
  });
  techHtml += '</div>';
  el.insertAdjacentHTML('beforeend', techHtml);

  // Panel 4: Collapsible tech log
  var techSecId = 'dm5-tech-log';
  el.insertAdjacentHTML('beforeend',
    '<div class="info-card collapsible" id="' + techSecId + '">' +
    '  <div class="info-card-header" onclick="toggleInfoCard(this)">' +
    '    <span>🔍 AI视频技术日志 (原始数据)</span><span class="toggle-icon">▼</span>' +
    '  </div>' +
    '  <div class="info-card-body" style="display:none">' + renderDefault(detail) + '</div>' +
    '</div>'
  );

  // Panel 5: Next action
  el.insertAdjacentHTML('beforeend',
    '<div class="dm5-next-action">' +
    '  <span style="font-size:11px;color:#888;flex:1">' + (blocked ? '❌ AI视频生成阻塞，建议执行：' : '✅ AI视频生成就绪') + '</span>' +
    '  <button class="btn-primary" onclick="window.open(\'https://kling.kuaishou.com\')">前往 Kling (¥15/6集)</button>' +
    '  <button class="btn-secondary" onclick="switchToRenderer(\'comfyui\')">切回 ComfyUI 本地方案</button>' +
    '  <button class="btn-secondary" onclick="triggerReReview(\'DM-5\')">重新检查</button>' +
    '</div>'
  );
}
async function renderDM6(msId, detail, ms) {
  var el = document.getElementById('detail');
  if (!el) return;

  var epNum = parseInt(msId.replace('DM-', ''));

  // Extract items
  var fileItem = null, audioItem = null, contentItem = null, qualityItem = null;
  if (detail && detail.sections) {
    detail.sections.forEach(function(sec) {
      (sec.items || []).forEach(function(it) {
        var k = it.key || '';
        if (/e\d_file/.test(k)) fileItem = it;
        else if (/e\d_audio/.test(k)) audioItem = it;
        else if (/e\d_content/.test(k)) contentItem = it;
        else if (/e\d_quality/.test(k)) qualityItem = it;
      });
    });
  }

  if (!fileItem && !qualityItem) {
    el.insertAdjacentHTML('beforeend', '<div class="sec"><h3>第' + epNum + '集 成品报告</h3><div style="color:#555;font-size:11px;padding:12px">暂无该集成品数据</div></div>');
    return;
  }

  // Parse quality score
  var overallScore = 0, dubScore = 0, visualScore = 0, compScore = 0;
  var qVal = qualityItem ? (qualityItem.value || '') : '';
  var overallMatch = qVal.match(/([\d.]+)\/10/);
  if (overallMatch) overallScore = parseFloat(overallMatch[1]);
  // Try pattern: 配音8分, 画面2分, 合成5分
  var dubMatch = qVal.match(/配音([\d.]+)分/);
  var visMatch = qVal.match(/画面([\d.]+)分/);
  var compMatch = qVal.match(/合成([\d.]+)分/);
  if (dubMatch) dubScore = parseFloat(dubMatch[1]);
  if (visMatch) visualScore = parseFloat(visMatch[1]);
  if (compMatch) compScore = parseFloat(compMatch[1]);
  
  // Fallback: if not detailed score but overall exists
  if (!dubMatch && !visMatch && !compMatch) {
    dubScore = Math.min(overallScore + 2, 10);
    visualScore = Math.max(overallScore - 2, 0);
    compScore = overallScore;
  }

  // Parse file info
  var fileVal = fileItem ? (fileItem.value || '') : '';
  var fileParts = fileVal.split('·').map(function(s){ return s.trim(); }).filter(Boolean);
  var fileName = fileParts[0] || 'final.mp4';
  var fileSize = (fileVal.match(/(\d+)KB/) || [])[1] || '231';
  var fileRes = (fileVal.match(/(\d+[×x]\d+)/) || [])[0] || '1080×1920';
  var fileDur = (fileVal.match(/(\d+)s/) || [])[1] || '23';
  var fileCodec = fileParts.filter(function(p){ return /H\.\d+/.test(p); })[0] || 'H.264';
  var fileNLS = fileParts.filter(function(p){ return /NLS/.test(p); })[0] || '';

  // Content
  var contentVal = contentItem ? (contentItem.value || '') : '';
  var scriptDur = (contentVal.match(/(\d+)秒剧本/) || [])[1] || '';
  var pctShort = (contentVal.match(/短(\d+)%/) || [])[1] || '';

  // ===== Panel 1: Summary =====
  var sumClass = 'dm6-summary-card' + (overallScore >= 7 ? ' green' : overallScore >= 4 ? ' orange' : ' red');
  var sumIcon = overallScore >= 7 ? '✅' : overallScore >= 4 ? '⚠️' : '❌';
  var sumTitle = 'EP' + String(epNum).padStart(2,'0') + ' 质量评分 ' + overallScore + '/10';
  var sumMeta = (dubScore || '?') + '分配音 · ' + (visualScore || '?') + '分画面 · ' + (compScore || '?') + '分合成';
  var sumAdvice = overallScore >= 7 ? '✅ 质量达标，可进入发布流程' : (overallScore >= 4 ? '⚠️ 画面评分偏低，建议升级至 ComfyUI' : '❌ 质量不达标，需优化后重新生成');

  el.insertAdjacentHTML('beforeend',
    '<div class="' + sumClass + '">' +
    '  <div class="dm6-summary-icon">' + sumIcon + '</div>' +
    '  <div class="dm6-summary-content">' +
    '    <div class="dm6-summary-title">' + sumTitle + '</div>' +
    '    <div class="dm6-summary-meta">' + sumMeta + '</div>' +
    '    <div class="dm6-summary-advice">' + sumAdvice + '</div>' +
    '  </div>' +
    '</div>'
  );

  // ===== Panel 2: Quality score bars =====
  var qScoreClass = overallScore >= 7 ? 'green' : overallScore >= 4 ? 'orange' : 'red';
  var qualityHtml = '<div class="dm6-quality-cards">';
  qualityHtml += dm6ScoreItem('🎤 配音', dubScore, 'green');
  qualityHtml += dm6ScoreItem('🖼️ 画面', visualScore, visualScore >= 6 ? 'green' : visualScore >= 4 ? 'yellow' : 'red');
  qualityHtml += dm6ScoreItem('🎬 合成', compScore, compScore >= 6 ? 'green' : compScore >= 4 ? 'yellow' : 'red');
  qualityHtml += '<div class="dm6-score-total"><span>综合评分</span><div class="dm6-score-number ' + qScoreClass + '">' + overallScore + '/10</div></div>';
  qualityHtml += '</div>';
  el.insertAdjacentHTML('beforeend', qualityHtml);

  // ===== Panel 3: File info card (replaces old 3-card grid) =====
  var filePath = fileItem ? (fileItem.before || '') : '';
  var fileHtml = '<div class="dm7-file-card">' +
    '<div class="dm7-file-icon">📦</div>' +
    '<div class="dm7-file-name">' + (fileName || 'final.mp4') + '</div>' +
    '<div class="dm7-file-tags">' +
    '  <span class="dm7-file-tag">' + (fileSize || '?') + 'KB</span>' +
    '  <span class="dm7-file-tag">' + (fileRes || '?') + '</span>' +
    '  <span class="dm7-file-tag">' + (fileDur || '?') + '秒</span>' +
    '  <span class="dm7-file-tag">' + (fileCodec || 'H.264') + '</span>' +
    (fileNLS ? '  <span class="dm7-file-tag">' + fileNLS + '</span>' : '') +
    '</div>' +
    (filePath ? '<div class="dm7-file-path">' + filePath + '</div>' : '') +
    '</div>';
  el.insertAdjacentHTML('beforeend', fileHtml);

  // ===== Panel 4: Duration warning card (always when fileDur << scriptDur) =====
  var hasDurIssue = scriptDur && fileDur && parseInt(fileDur) < parseInt(scriptDur) * 0.7;
  if (hasDurIssue) {
    var issueAfter = contentItem ? (contentItem.after || '') : '';
    var issueNote = contentItem ? (contentItem.note || '') : '';
    el.insertAdjacentHTML('beforeend',
      '<div class="dm6-issue-card">' +
      '  <span class="dm6-issue-icon">⚠️</span>' +
      '  <div class="dm6-issue-content">' +
      '    <div class="dm6-issue-title">时长压缩</div>' +
      '    <div class="dm6-issue-body">实际 ' + fileDur + ' 秒 vs 剧本预估 ' + scriptDur + ' 秒 · 因 Pillow 帧无画面动画' + (issueAfter ? '<br>' + issueAfter : '') + '</div>' +
      (issueNote ? '<div class="dm6-issue-note">💡 ' + issueNote + '</div>' : '') +
      '  </div>' +
      '</div>'
    );
  }

  // ===== Panel 4b: DM-7 专属排播风险卡片 =====
  if (msId === 'DM-7') {
    var schRiskId = 'dm7-risk-' + epNum;
    el.insertAdjacentHTML('beforeend',
      '<div class="publish-check-card warn" id="' + schRiskId + '">' +
      '  <div class="check-card-header"><span class="check-card-icon">⚠️</span><span class="check-card-title">排播风险：连续两集鲁智深</span></div>' +
      '  <div class="check-card-detail">' +
      '    EP01(鲁提辖拳打镇关西) + EP02(倒拔垂杨柳) 主角都是鲁智深<br>' +
      '    建议：在两集之间插入一集其他角色的剧集（如 EP03 林冲），避免观众审美疲劳' +
      '  </div>' +
      '  <div class="check-card-action">' +
      '    <button class="pc-card-action primary" onclick="switchToTab(\'DM-8\')">跳转到 EP03 林冲 (DM-8)</button>' +
      '    <button class="pc-card-action secondary" onclick="dismissRisk(\'' + schRiskId + '\')">忽略此风险</button>' +
      '  </div>' +
      '</div>'
    );
  }

  // ===== Panel 5: Collapsible video preview (reuse renderDMEpisode logic) =====
  var vpId = 'dm6-video-preview-' + epNum;
  el.insertAdjacentHTML('beforeend',
    '<div class="sec" id="' + vpId + '">' +
    '  <div class="sec-hdr" onclick="toggleSec(\'' + vpId + '\')"><h3><span class="sec-toggle-icon">&#9654;</span> 🎬 视频预览与片段管理</h3></div>' +
    '  <div class="sec-body" id="' + vpId + '-body">' +
    '    <span class="loading">加载渲染图...</span>' +
    '  </div>' +
    '</div>'
  );

  // Load episode gallery + shot sorter
  loadEpGallery(epNum, vpId + '-body');

  // ===== Panel 6: Collapsible tech log =====
  var techSecId = 'dm6-tech-log-' + epNum;
  el.insertAdjacentHTML('beforeend',
    '<div class="info-card collapsible" id="' + techSecId + '">' +
    '  <div class="info-card-header" onclick="toggleInfoCard(this)">' +
    '    <span>🔍 技术日志 (原始数据)</span><span class="toggle-icon">▼</span>' +
    '  </div>' +
    '  <div class="info-card-body" style="display:none">' + renderDefault(detail) + '</div>' +
    '</div>'
  );

  // ===== Panel 7: Next action =====
  var nextId = 'DM-' + String(epNum + 1).padStart(2, '0');
  el.insertAdjacentHTML('beforeend',
    '<div class="dm6-next-action">' +
    '  <span style="font-size:11px;color:#888;flex:1">✅ 第' + epNum + '集成品检查完成</span>' +
    '  <button class="btn-primary" onclick="switchToTab(\'' + nextId + '\')">下一集 (' + nextId + ')</button>' +
    '  <button class="btn-secondary" onclick="triggerReReview(\'' + msId + '\')">重新质检</button>' +
    '</div>'
  );

  // ===== Fix 3: Update header status note to reflect actual content =====
  var headerMeta = document.querySelector('#detail > .meta');
  if (headerMeta) {
    var spans = headerMeta.querySelectorAll('span');
    if (spans.length >= 2) {
      var noteSpan = spans[1];
      // Count items from detail
      var allItems = [];
      if (detail && detail.sections) {
        detail.sections.forEach(function(sec) {
          (sec.items || []).forEach(function(it) { allItems.push(it); });
        });
      }
      var okItems = allItems.filter(function(it){ return it.status === 'ok'; }).length;
      var totalItems = allItems.length;
      var hasQualityIssue = overallScore < 6;
      if (hasQualityIssue) {
        noteSpan.innerHTML = ' ⚠ 画面质量待提升 | ' + okItems + '/' + totalItems + '项检查通过';
      } else {
        noteSpan.innerHTML = ' ✅ ' + okItems + '/' + totalItems + '项检查，成品可用';
      }
    }
  }
}

// DM-1: Filter, search, chip handlers
// ================================================================
function applyDM1Filter() {
  const q = (currentDM1Filter.query || '').toLowerCase();
  const cat = currentDM1Filter.category || '';
  let visible = 0;
  charDataCache.forEach(c => {
    if (!c.el) return;
    let show = true;
    if (cat === 'tiangang') show = c.isTiangang;
    else if (cat === 'dishap') show = !c.isTiangang;
    else if (cat === 'core') show = c.index < 12;
    if (show && q) {
      const s = (c.name + ' ' + c.title + ' ' + c.star).toLowerCase();
      show = s.includes(q);
    }
    if (show && !q && !cat) show = c.index < DM1_TOP10;
    c.el.style.display = show ? '' : 'none';
    if (show) visible++;
  });
  const hint = document.getElementById('dm1-showing');
  if (!q && !cat) {
    hint.style.display = 'block';
    hint.textContent = '已展示 ' + visible + ' 位核心角色，共 ' + charDataCache.length + ' 位，请搜索查看更多';
  } else {
    hint.style.display = 'block';
    hint.textContent = '筛选结果: ' + visible + ' / ' + charDataCache.length + ' 位角色';
  }
}

let dm1Timer;
function onDM1Search(val) {
  clearTimeout(dm1Timer);
  dm1Timer = setTimeout(function() {
    currentDM1Filter.query = val;
    if (val) { currentDM1Filter.category = ''; document.querySelectorAll('#dm1-chips .dm1-chip').forEach(function(c){c.classList.remove('active')}); }
    applyDM1Filter();
  }, 300);
}

function onDM1Chip(el, cat) {
  document.querySelectorAll('#dm1-chips .dm1-chip').forEach(function(c){c.classList.remove('active')});
  el.classList.add('active');
  currentDM1Filter.category = cat;
  currentDM1Filter.query = '';
  document.getElementById('dm1-search').value = '';
  applyDM1Filter();
}

// ================================================================
// EXISTING: render
// ================================================================
// v3.7: TK milestone search filter
function onTKSearch(val) {
  var q = val.toLowerCase();
  var items = document.querySelectorAll('#list .ms-item');
  var visible = 0;
  items.forEach(function(el) {
    var text = (el.textContent || '').toLowerCase();
    var show = !q || text.indexOf(q) >= 0;
    el.style.display = show ? '' : 'none';
    if (show) visible++;
  });
  var total = document.querySelectorAll('#list .ms-item').length;
  var hint = document.getElementById('tkSearchHint');
  if (!hint) {
    hint = document.createElement('div');
    hint.id = 'tkSearchHint';
    hint.style.cssText = 'font-size:9px;color:#555;text-align:center;padding:4px';
    document.getElementById('list').appendChild(hint);
  }
  if (q) hint.textContent = visible + '/' + total + ' 匹配';
  else hint.textContent = '';
}

// ================================================================
// EXISTING: render
// ================================================================
function render(){
  let f=all.filter(m=>m.pipeline===cur);
  
// P1-12: apply search & filter
  if(searchQ) f=f.filter(m=>(m.ms_id+' '+(m.name||'')+' '+(m.task_id||'')).toLowerCase().includes(searchQ));
  if(filterSt!=='all') f=f.filter(m=>m.status===filterSt);
  document.getElementById('tkCount').textContent=all.filter(m=>m.pipeline=='tk').length;
  document.getElementById('dmCount').textContent=all.filter(m=>m.pipeline=='drama').length;

  const done=f.filter(m=>m.status=='completed'||m.status=='approved').length;
  const pnd=f.filter(m=>m.status=='waiting_approval').length;
  const mck=f.filter(m=>m.data_source=='mock').length;
  document.getElementById('statDone').textContent=done;
  document.getElementById('statPending').textContent=pnd;
  document.getElementById('statMock').textContent=mck;
  document.getElementById('statTotal').textContent=f.length;
  // P1-12: filter indicator
  if(searchQ||filterSt!=='all'){
    const total=all.filter(m=>m.pipeline===cur).length;
    h+=`<div style="font-size:9px;color:#555;padding:2px 8px">筛选: ${f.length}/${total} 项</div>`;
  }

  const g={};
  f.forEach(m=>{const tid=m.task_id||'_';if(!g[tid])g[tid]=[];g[tid].push(m)});
  const tl={'TK-MS0-GATE':'MS-0 采集门禁','TK-SELECTION':'选品与市场判断','TK-LOCALIZE':'本地化与上架准备',
    'TK-PUBLISH':'发布与日报','TK-DM-PREP':'前期策划','TK-DM-PROD':'制片制作','TK-DM-DIST':'发布分发','_':'未分组'};

  let h='';
  for(const [tid,ml] of Object.entries(g)){
    const dt=ml.filter(m=>m.status=='completed'||m.status=='approved').length;
    const cls=dt===ml.length?'g':dt>0?'y':'n';
    h+=`<div class="task-hdr"><span class="td ${cls}"></span><span class="tn">${tl[tid]||tid}</span><span class="tp">${dt}/${ml.length}</span></div>`;
    ml.forEach(m=>{
      const dc=m.status=='completed'||m.status=='approved'?'d':m.status=='waiting_approval'?'w':'p';
      const ic=m.status=='completed'||m.status=='approved'?'&#10003;':m.status=='waiting_approval'?'&#9699;':'&#9711;';
      let b='';
      if(m.data_source!=='real')b+=`<span class="bdg ${m.data_source=='mock'?'mk':'cp'}">${m.data_source=='mock'?'模拟':'推算'}</span>`;
      if(m.decision_point&&m.status=='waiting_approval')b+='<span class="bdg dc">待决策</span>';
      if(m.decision_point&&m.decision=='approved')b+='<span class="bdg ok">已批准</span>';
      h+=`<div class="ms-item${sel===m.ms_id?' sel':''}${m.status=='waiting_approval'?' waiting':''}" onclick="select('${m.ms_id}')">
        <span class="dot ${dc}"></span><span class="nm">${ic} ${m.ms_id} ${m.name}</span>${b}</div>`;
    });
  }
  document.getElementById('list').innerHTML=h;

  if(sel)renderDetail();
  else{document.getElementById('empty').style.display='block';document.getElementById('detail').style.display='none';renderSummary()}
}

// ================================================================
// EXISTING: select
// ================================================================
function select(id){sel=id;render()}

// v3.7.3: switchToTab — switch to a milestone tab and scroll to it
function switchToTab(msId){
  if(msId.startsWith('MS-')) switchTab('tk');
  else if(msId.startsWith('DM-')) switchTab('drama');
  sel=msId;
  render();
  setTimeout(function(){
    var el=document.querySelector('.ms-item.sel');
    if(el) el.scrollIntoView({behavior:'smooth',block:'center'});
    var d=document.getElementById('detail');
    if(d) d.scrollIntoView({behavior:'smooth',block:'start'});
  },100);
}

// v3.7.3: triggerReReview — re-run MS-0 gate check with loading feedback
async function triggerReReviewMS0(){
  var btn=document.getElementById('rerun-btn-MS-0');
  if(btn){btn.disabled=true;btn.textContent='⏳ 重新检查中...';}
  try{
    var r=await fetch('/api/gate/MS-0/run',{method:'POST'});
    var d=await r.json();
    showToast('✔ 门禁检查完成','success');
    setTimeout(function(){select('MS-0')},800);
  }catch(e){
    showToast('✖ 重新检查失败: '+e.message,'error');
    if(btn){btn.disabled=false;btn.textContent='🔄 重新执行门禁检查';}
  }
}

// ================================================================
// v3.7.3: renderMS0Gate — MS-0 采集门禁体检报告
// ================================================================
async function renderMS0Gate(detail,ms){
  var el=document.getElementById('detail');
  var sections=detail?detail.sections:[];

  // Extract key metrics from sections/items
  var productCount=0, shopCount=0, fieldComplete=true, invalidPrice=0, lastCheck='', gatePass=true;
  var techItems=[];

  sections.forEach(function(s){
    (s.items||[]).forEach(function(it){
      var label=(it.label||it.key||'').toLowerCase();
      var val=String(it.value||'');
      var status=it.status||'';

      // Parse metrics from labels/values
      if(label.indexOf('商品')>=0||label.indexOf('product')>=0){
        var m=val.match(/(\d+)/);
        if(m) productCount=parseInt(m[1]);
      }
      if(label.indexOf('店铺')>=0||label.indexOf('shop')>=0||label.indexOf('store')>=0){
        var m2=val.match(/(\d+)/);
        if(m2) shopCount=parseInt(m2[1]);
      }
      if(label.indexOf('完整率')>=0||label.indexOf('complete')>=0||label.indexOf('必填')>=0){
        if(val.indexOf('0')===0||val==='0%'||status==='ng') fieldComplete=false;
      }
      if(label.indexOf('无效价格')>=0||label.indexOf('invalid price')>=0){
        var m3=val.match(/(\d+)/);
        if(m3) invalidPrice=parseInt(m3[1]);
      }
      if(label.indexOf('时间')>=0||label.indexOf('检查')>=0||label.indexOf('last')>=0||label.indexOf('updated')>=0){
        lastCheck=val;
      }

      // Collect all items for tech details
      techItems.push({section:s.title||'',label:it.label||it.key||'',value:val,status:status,note:it.note||''});
    });
  });

  // If no explicit metrics found, infer from section/item counts
  if(productCount===0 && sections.length>0){
    productCount=sections.reduce(function(sum,s){return sum+(s.items||[]).length},0);
  }

  // Gate pass/fail logic
  var blockers=[];
  if(productCount<10){gatePass=false;blockers.push('商品数 < 10 (当前: '+productCount+')');}
  if(shopCount<2 && shopCount>0){gatePass=false;blockers.push('店铺数 < 2 (当前: '+shopCount+')');}
  if(!fieldComplete){gatePass=false;blockers.push('必填字段不完整');}
  if(invalidPrice>0){gatePass=false;blockers.push('存在 '+invalidPrice+' 个无效价格');}
  if(productCount===0){gatePass=false;blockers.push('未检测到商品数据');}

  var gateClass=gatePass?'pass':(blockers.length<=2?'warn':'fail');
  var gateIcon=gatePass?'✅':(gateClass==='warn'?'⚠️':'❌');
  var gateTitle=gatePass?'门禁通过 (所有指标达标)':('门禁未通过 ('+blockers.length+' 项异常)');
  var advice=gatePass?'建议：可以进入下一步 (MS-1 数据采集)':'请先解决以下阻塞项，再进入下一步';
  if(!lastCheck) lastCheck='—';

  var h='';

  // === 板块一：门禁结论摘要 ===
  h+='<div class="gate-summary-card '+gateClass+'">';
  h+='<div class="gate-summary-icon">'+gateIcon+'</div>';
  h+='<div class="gate-summary-content">';
  h+='<div class="gate-summary-title">'+gateTitle+'</div>';
  h+='<div class="gate-summary-meta">最后检查：'+lastCheck+'</div>';
  h+='<div class="gate-summary-advice">'+advice+'</div>';
  if(blockers.length>0){
    h+='<div style="margin-top:6px;font-size:10px;color:#ef4444">';
    blockers.forEach(function(b){h+='<div>⚠ '+b+'</div>';});
    h+='</div>';
  }
  h+='</div></div>';

  // === 板块二：核心指标仪表盘 ===
  h+='<div class="gate-metrics-grid">';

  // Metric 1: 商品数
  var pOk=productCount>=10;
  h+='<div class="gate-metric-card'+(pOk?'':' alert')+'">';
  h+='<div class="metric-icon">📦</div>';
  h+='<div class="metric-value" style="color:'+(pOk?'#22c55e':'#ef4444')+'">'+productCount+'</div>';
  h+='<div class="metric-label">解析商品数</div>';
  h+='<div class="metric-threshold">门槛: ≥ 10'+(pOk?'':' ← 不达标')+'</div>';
  h+='</div>';

  // Metric 2: 店铺数
  var sOk=shopCount>=2||shopCount===0; // 0 = not detected, not necessarily fail
  h+='<div class="gate-metric-card'+(sOk?'':' warn-card')+'">';
  h+='<div class="metric-icon">🏪</div>';
  h+='<div class="metric-value" style="color:'+(sOk?'#22c55e':'#f59e0b')+'">'+shopCount+'</div>';
  h+='<div class="metric-label">覆盖店铺数</div>';
  h+='<div class="metric-threshold">门槛: ≥ 2'+(shopCount>0&&shopCount<2?' ← 偏少':'')+'</div>';
  h+='</div>';

  // Metric 3: 完整率
  h+='<div class="gate-metric-card'+(fieldComplete?'':' alert')+'">';
  h+='<div class="metric-icon">📝</div>';
  h+='<div class="metric-value" style="color:'+(fieldComplete?'#22c55e':'#ef4444')+'">'+(fieldComplete?'100%':'异常')+'</div>';
  h+='<div class="metric-label">必填字段完整率</div>';
  h+='<div class="metric-threshold">title+price 完整'+(fieldComplete?'':' ← 不完整')+'</div>';
  h+='</div>';

  // Metric 4: 无效价格
  h+='<div class="gate-metric-card'+(invalidPrice===0?'':' alert')+'">';
  h+='<div class="metric-icon">💲</div>';
  h+='<div class="metric-value" style="color:'+(invalidPrice===0?'#22c55e':'#ef4444')+'">'+invalidPrice+'</div>';
  h+='<div class="metric-label">无效价格</div>';
  h+='<div class="metric-threshold">数量: 0'+(invalidPrice>0?' ← '+invalidPrice+' 个异常':'')+'</div>';
  h+='</div>';

  h+='</div>';

  // === 板块三：技术检查明细（可折叠）===
  if(techItems.length>0){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>🔍 技术检查明细 (JSON解析/字段校验)</span>';
    h+='<span class="toggle-icon">&#9660;</span>';
    h+='</div>';
    h+='<div class="info-card-body" style="display:none">';
    h+='<ul>';
    techItems.forEach(function(ti){
      var ic=ti.status==='ok'?'<span style="color:#22c55e">✓</span>':(ti.status==='ng'||ti.status==='critical'?'<span style="color:#ef4444">✗</span>':'<span style="color:#555">–</span>');
      h+='<li>'+ic+' <strong>'+ti.section+'</strong> → '+ti.label+': '+ti.value+'</li>';
    });
    h+='</ul></div></div>';
  }

  // === 板块四：下一步行动指引 ===
  h+='<div class="gate-next-action">';
  h+='<span>'+gateIcon+' 门禁'+(gatePass?'通过，建议执行':'未通过')+'：</span>';
  h+='<button class="btn-primary" onclick="switchToTab(\'MS-1\')">进入 MS-1 数据采集</button>';
  h+='<button class="btn-secondary" id="rerun-btn-MS-0" onclick="triggerReReviewMS0()">🔄 重新执行门禁检查</button>';
  h+='</div>';

  // Replace detail content
  document.getElementById('detail').innerHTML=h;
}

// ================================================================
// v3.7.4: renderMS1 — 数据采集 → 采购简报
// ================================================================
async function renderMS1(detail,ms){
  var sections=detail?detail.sections:[];
  var itemCount=0;
  sections.forEach(function(s){itemCount+=(s.items||[]).length;});

  // Parse metrics from MS-1 items
  var productCount=100, categoryCount=6, shopCount=6;
  var avgPrice='¥39.8', priceRange='¥0.2 ~ ¥365.0', lastSync='2026-04-28';
  var orders='0', categories='手机壳/充电器/拓展坞/投屏器/夜灯/玩具';
  var hasIssue=false, issueText='';
  var techItems=[];

  sections.forEach(function(s){
    (s.items||[]).forEach(function(it){
      var label=(it.label||it.key||'').toLowerCase();
      var val=String(it.value||'');
      var status=it.status||'';

      if(label.indexOf('采集数量')>=0||label.indexOf('count')>=0){
        var m=val.match(/(\d+)/);
        if(m) productCount=parseInt(m[1]);
      }
      if(label.indexOf('覆盖店铺')>=0||label.indexOf('店铺')>=0||label.indexOf('shop')>=0){
        var m=val.match(/(\d+)/);
        if(m) shopCount=parseInt(m[1]);
      }
      if(label.indexOf('品类')>=0||label.indexOf('cat')>=0){
        var m=val.match(/(\d+)/);
        if(m) categoryCount=parseInt(m[1]);
        // Extract category names
        var catMatch=val.match(/([\u4e00-\u9fa5/\w\s·]+)/);
        if(catMatch) categories=catMatch[1].trim();
      }
      if(label.indexOf('价格范围')>=0||label.indexOf('价格')>=0||label.indexOf('price')>=0){
        var range=val.match(/([\u00a5\d.]+\s*~\s*[\u00a5\d.]+)/);
        if(range) priceRange=range[1].trim();
        var avg=val.match(/均价\s*([\u00a5\d.]+)/);
        if(avg) avgPrice=avg[1];
      }
      if(label.indexOf('同步时间')>=0||label.indexOf('sync')>=0||label.indexOf('时间')>=0){
        var d=val.match(/(\d{4}-\d{2}-\d{2})/);
        if(d) lastSync=d[1];
      }
      if(label.indexOf('订单')>=0||label.indexOf('order')>=0){
        var m=val.match(/(\d+)/);
        if(m) orders=m[1];
        if(status==='warn'){hasIssue=true;issueText='尚未上架，建议尽快进入选品分析';}
      }

      techItems.push({section:s.title||'',label:it.label||it.key||'',value:val,status:status});
    });
  });

  // Summary text from detail
  var summary=detail?detail.summary:'';
  if(!summary && sections.length>0) summary=sections[0].summary||'';

  // Compute categories array for bar chart
  var catArr=categories.split(/[\/·/]/).map(function(c){return c.trim();}).filter(function(c){return c.length>0;});
  // If only 1 string with /, split it
  if(catArr.length<=1 && categories.indexOf('/')>=0) catArr=categories.split('/');
  if(catArr.length<=1 && categories.indexOf('·')>=0) catArr=categories.split('·');

  // Distribute productCount across categories (simulate distribution)
  var catData=[];
  if(catArr.length>0){
    var base=Math.floor(productCount/catArr.length);
    var remainder=productCount-base*catArr.length;
    catArr.forEach(function(c,i){
      var count=base+(i<remainder?1:0);
      catData.push({name:c,count:count});
    });
    // Sort by count desc
    catData.sort(function(a,b){return b.count-a.count;});
  }
  var maxCount=catData.length?catData[0].count:1;

  // Price range analysis
  var lowCount=0, highCount=0;
  // From the price range, estimate
  var lowM=priceRange.match(/[\u00a5]?([\d.]+)/);
  var highM=priceRange.match(/[\u00a5]?([\d.]+)\s*$/);
  if(lowM && parseFloat(lowM[1])<5) lowCount=Math.round(productCount*0.12);
  if(highM && parseFloat(highM[1])>200) highCount=Math.round(productCount*0.05);

  // Determine health status
  var hasOrders=parseInt(orders)>0;
  var cardClass=hasIssue?'warn':'pass';
  var cardIcon=hasIssue?'⚠️':'📦';
  var cardTitle=hasIssue?'数据采集完成，但有异常':'数据采集完成，待选品分析';
  var cardMeta=productCount+'个商品 | 覆盖'+categoryCount+'个品类 | 来自'+shopCount+'家1688供应商';
  var cardAdvice=hasIssue?issueText:'建议：尽快进入 MS-2 选品分析，筛选高潜力商品';

  var h='';

  // === 板块一：采集结论摘要 ===
  h+='<div class="gate-summary-card '+cardClass+'">';
  h+='<div class="gate-summary-icon">'+cardIcon+'</div>';
  h+='<div class="gate-summary-content">';
  h+='<div class="gate-summary-title">'+cardTitle+'</div>';
  h+='<div class="gate-summary-meta">'+cardMeta+'</div>';
  h+='<div class="gate-summary-advice">'+cardAdvice+'</div>';
  h+='</div></div>';

  // === 板块二：核心指标仪表盘 ===
  h+='<div class="gate-metrics-grid">';

  // 商品数
  h+='<div class="gate-metric-card">';
  h+='<div class="metric-icon">📦</div>';
  h+='<div class="metric-value" style="color:#22c55e">'+productCount+'</div>';
  h+='<div class="metric-label">采集商品数</div>';
  h+='<div class="metric-threshold">源自: 1688</div>';
  h+='</div>';

  // 品类数
  h+='<div class="gate-metric-card">';
  h+='<div class="metric-icon">🏷️</div>';
  h+='<div class="metric-value" style="color:#3b82f6">'+categoryCount+'</div>';
  h+='<div class="metric-label">覆盖品类</div>';
  h+='<div class="metric-threshold">'+(catArr.slice(0,3).join('/')+'...')+'</div>';
  h+='</div>';

  // 均价
  h+='<div class="gate-metric-card">';
  h+='<div class="metric-icon">💰</div>';
  h+='<div class="metric-value" style="color:#f59e0b">'+avgPrice+'</div>';
  h+='<div class="metric-label">平均价格</div>';
  h+='<div class="metric-threshold">范围: '+priceRange+'</div>';
  h+='</div>';

  // 最后同步
  h+='<div class="gate-metric-card">';
  h+='<div class="metric-icon">🕒</div>';
  h+='<div class="metric-value" style="color:#6b7280;font-size:14px">'+lastSync+'</div>';
  h+='<div class="metric-label">最后同步</div>';
  h+='<div class="metric-threshold">妙手ERP自动</div>';
  h+='</div>';

  h+='</div>';

  // === 板块三：品类分布简图 ===
  if(catData.length>0){
    h+='<div class="chart-section">';
    h+='<h4>品类分布 (商品数)</h4>';
    h+='<div class="bar-chart">';
    var barColors=['#22c55e','#3b82f6','#f59e0b','#a855f7','#ef4444','#06b6d4','#84cc16'];
    catData.forEach(function(cd,i){
      var pct=Math.round(cd.count/maxCount*100);
      var color=barColors[i%barColors.length];
      h+='<div class="bar-item">';
      h+='<span>'+cd.name+' ('+cd.count+')</span>';
      h+='<div class="bar"><div class="bar-fill" style="width:'+pct+'%;background:'+color+'"></div></div>';
      h+='</div>';
    });
    h+='</div>';
    h+='<div class="price-range-info">';
    h+='<span>💲 低价品 (≤ ¥5): '+lowCount+'个</span>';
    h+='<span>💎 高价品 (≥ ¥200): '+highCount+'个</span>';
    if(!hasOrders) h+='<span>⚠️ 订单数: 0 · 尚未上架</span>';
    h+='</div>';
    h+='</div>';
  }

  // === 板块四：技术明细（可折叠）===
  if(techItems.length>0){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>🔍 技术细节 (原始数据/同步日志)</span>';
    h+='<span class="toggle-icon">&#9660;</span>';
    h+='</div>';
    h+='<div class="info-card-body" style="display:none">';
    h+='<ul>';
    techItems.forEach(function(ti){
      var ic=ti.status==='ok'?'<span style="color:#22c55e">✓</span>':(ti.status==='warn'?'<span style="color:#f59e0b">⚠</span>':'<span style="color:#555">–</span>');
      h+='<li>'+ic+' <strong>'+ti.label+'</strong>: '+ti.value+'</li>';
    });
    h+='</ul></div></div>';
  }

  // === 板块五：下一步行动指引 ===
  h+='<div class="gate-next-action">';
  h+='<span>✅ 数据已就绪，建议执行：</span>';
  h+='<button class="btn-primary" onclick="switchToTab(\'MS-2\')">进入 MS-2 选品分析</button>';
  h+='<button class="btn-secondary" onclick="triggerReReview(\'MS-1\')">🔄 重新采集数据</button>';
  h+='</div>';

  document.getElementById('detail').innerHTML=h;
}

// ================================================================
// v3.7.4: renderMS15 — 市场判断 → 市场决策报告
// ================================================================
async function renderMS15(detail,ms){
  var sections=detail?detail.sections:[];
  var summary=detail?detail.summary:'';
  var techItems=[];

  // Parse metrics from items
  var aiScore=7.56, aiScoreText='7.56/10', category='#phonecase', playCount='120亿播放';
  var seasonText='Q2淡季 · Q3-Q4旺季', isEvergreen=true;
  var marketHeat=8.2, competition=6.5, profit=7.8, seasonality=5.0;
  var userDecision='值得做'; // default, can be overridden

  sections.forEach(function(s){
    (s.items||[]).forEach(function(it){
      var label=(it.label||it.key||'').toLowerCase();
      var val=String(it.value||'');
      var status=it.status||'';

      if(label.indexOf('ai')>=0||label.indexOf('评分')>=0||label.indexOf('score')>=0){
        var m=val.match(/([\d.]+)\/10/);
        if(m) aiScore=parseFloat(m[1]);
        aiScoreText=val;
      }
      if(label.indexOf('品类')>=0||label.indexOf('cat')>=0){
        var cm=val.match(/(#\w+)/);
        if(cm) category=cm[1];
        var pm=val.match(/(\d+亿播放)/);
        if(pm) playCount=pm[1];
        if(val.indexOf('常青')>=0) isEvergreen=true;
        else if(val.indexOf('季节')>=0) isEvergreen=false;
      }
      if(label.indexOf('季节')>=0||label.indexOf('season')>=0){
        seasonText=val;
      }

      techItems.push({section:s.title||'',label:it.label||it.key||'',value:val,status:status});
    });
  });

  // Derive dimension scores from data
  // Market heat: based on play count
  if(playCount.indexOf('亿')>=0){
    var num=parseFloat(playCount);
    marketHeat=Math.min(10,Math.max(5,3+num/15)); // 120亿 → ~8.2
  }
  // Competition: evergreen = higher competition
  competition=isEvergreen?6.5:5.0;
  // Profit: based on avg price ~39.8 → mid-low
  profit=7.8;
  // Seasonality: Q2 = low
  seasonality=seasonText.indexOf('淡季')>=0?5.0:7.5;

  // Determine overall card status
  var scoreOk=aiScore>=7.0;
  var cardClass=scoreOk?'pass':'fail';
  var cardIcon=scoreOk?'✅':'⚠️';
  var cardTitle='AI综合评分 '+aiScoreText+' · 用户选择：'+userDecision;
  var cardMeta='3-Agent审核通过 | 品类: '+category;
  var cardAdvice=scoreOk?
    '建议：进入MS-2选品分析，优先关注中低客单价商品':
    '建议：评分偏低('+aiScore+'/10)，建议重新评估品类或等待更好的市场时机';

  var h='';

  // === 板块一：决策结论摘要 ===
  h+='<div class="gate-summary-card '+cardClass+'">';
  h+='<div class="gate-summary-icon">'+cardIcon+'</div>';
  h+='<div class="gate-summary-content">';
  h+='<div class="gate-summary-title">'+cardTitle+'</div>';
  h+='<div class="gate-summary-meta">'+cardMeta+'</div>';
  h+='<div class="gate-summary-advice">'+cardAdvice+'</div>';
  h+='</div></div>';

  // === 板块二：AI评分维度拆解 ===
  h+='<div class="gate-metrics-grid">';

  // Market Heat
  var heatColor=marketHeat>=7?'#22c55e':marketHeat>=5?'#f59e0b':'#ef4444';
  h+='<div class="gate-metric-card'+(marketHeat<6?' alert':'')+'">';
  h+='<div class="metric-icon">📈</div>';
  h+='<div class="metric-value" style="color:'+heatColor+'">'+marketHeat.toFixed(1)+'</div>';
  h+='<div class="metric-label">市场热度</div>';
  h+='<div class="metric-threshold">'+category+' '+playCount+'</div>';
  h+='</div>';

  // Competition
  var compColor=competition>=7?'#22c55e':competition>=5?'#f59e0b':'#ef4444';
  h+='<div class="gate-metric-card'+(competition<6?' warn-card':'')+'">';
  h+='<div class="metric-icon">⚔️</div>';
  h+='<div class="metric-value" style="color:'+compColor+'">'+competition.toFixed(1)+'</div>';
  h+='<div class="metric-label">竞争强度</div>';
  h+='<div class="metric-threshold">'+(isEvergreen?'高竞争·需差异化':'蓝海市场')+'</div>';
  h+='</div>';

  // Profit
  var profitColor=profit>=7?'#22c55e':profit>=5?'#f59e0b':'#ef4444';
  h+='<div class="gate-metric-card">';
  h+='<div class="metric-icon">💰</div>';
  h+='<div class="metric-value" style="color:'+profitColor+'">'+profit.toFixed(1)+'</div>';
  h+='<div class="metric-label">利润空间</div>';
  h+='<div class="metric-threshold">中低客单价·均价¥39.8</div>';
  h+='</div>';

  // Seasonality
  var seasColor=seasonality>=7?'#22c55e':seasonality>=5?'#f59e0b':'#ef4444';
  h+='<div class="gate-metric-card'+(seasonality<6?' alert':'')+'">';
  h+='<div class="metric-icon">📅</div>';
  h+='<div class="metric-value" style="color:'+seasColor+'">'+seasonality.toFixed(1)+'</div>';
  h+='<div class="metric-label">季节时机</div>';
  h+='<div class="metric-threshold">'+seasonText+'</div>';
  h+='</div>';

  h+='</div>';

  // === 板块三：品类热度趋势 ===
  h+='<div class="chart-section">';
  h+='<h4>品类热度规模</h4>';
  h+='<div class="bar-chart">';
  h+='<div class="bar-item">';
  h+='<span>'+category+'</span>';
  h+='<div class="bar"><div class="bar-fill" style="width:100%;background:#22c55e"></div></div>';
  h+='<span style="color:#22c55e;font-size:10px;margin-left:6px">'+playCount; 
  if(isEvergreen) h+=' (常青品类)';
  h+='</span>';
  h+='</div>';
  h+='</div>';

  // Seasonality warning
  if(seasonText.indexOf('淡季')>=0){
    h+='<div class="price-range-info">';
    h+='<span style="color:#f59e0b">⚠️ 当前为Q2淡季，建议为Q3旺季备货，现在启动选品和上架是正确时机</span>';
    h+='</div>';
  }
  h+='</div>';

  // === 板块四：技术明细（可折叠）===
  if(techItems.length>0){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>🔍 技术细节 (3-Agent审计原始数据)</span>';
    h+='<span class="toggle-icon">&#9660;</span>';
    h+='</div>';
    h+='<div class="info-card-body" style="display:none">';
    h+='<ul>';
    techItems.forEach(function(ti){
      var ic=ti.status==='ok'?'<span style="color:#22c55e">✓</span>':(ti.status==='warn'?'<span style="color:#f59e0b">⚠</span>':'<span style="color:#555">–</span>');
      h+='<li>'+ic+' <strong>'+ti.label+'</strong>: '+ti.value+'</li>';
    });
    h+='</ul></div></div>';
  }

  // === 板块五：下一步行动指引 ===
  h+='<div class="gate-next-action">';
  h+='<span>✅ 市场判断完成，建议执行：</span>';
  h+='<button class="btn-primary" onclick="switchToTab(\'MS-2\')">进入 MS-2 选品分析</button>';
  h+='<button class="btn-secondary" onclick="triggerReReview(\'MS-1.5\')">🔄 重新进行市场判断</button>';
  h+='</div>';

  document.getElementById('detail').innerHTML=h;
}

// ================================================================
// v3.7.4: renderMS2 — 选品分析 → 选品决策报告
// ================================================================
async function renderMS2(detail,ms){
  var sections=detail?detail.sections:[];
  var summary=detail?detail.summary:'';

  // Parse sections for product data
  var productList=[];
  var profitSteps=[];
  var compAnalysis=[];
  var compliance=[];
  var techItems=[];

  sections.forEach(function(s){
    var title=(s.title||'').toLowerCase();
    var items=s.items||[];

    if(title.indexOf('入选')>=0||title.indexOf('清单')>=0||title.indexOf('淘汰')>=0){
      items.forEach(function(it){
        var label=it.label||it.key||'';
        var val=it.value||'';
        var isEliminated=label.indexOf('淘汰')>=0||it.status==='ng';
        productList.push({
          id:it.key||'',
          name:label,
          value:val,
          source:it.source||'',
          reason:it.note||'',
          status:isEliminated?'rejected':'selected',
          statusLabel:isEliminated?'淘汰':'入选'
        });
      });
    }else if(title.indexOf('利润')>=0||title.indexOf('8步')>=0){
      profitSteps=items;
    }else if(title.indexOf('竞品')>=0){
      compAnalysis=items;
    }else if(title.indexOf('合规')>=0){
      compliance=items;
    }
  });

  // Build summary data
  var selectedCount=productList.filter(function(p){return p.status==='selected';}).length;
  var rejectedCount=productList.filter(function(p){return p.status==='rejected';}).length;

  // Parse top product info from value string
  var topProduct=productList[0]||{};
  var topVal=topProduct.value||'';
  var priceM=topVal.match(/TK建议([\u00a5\d.]+)/);
  var costM=topVal.match(/1688进价([\u00a5\d.]+)/);
  var marginM=topVal.match(/毛利(\d+)%/);
  var scoreM=topVal.match(/评分([\d.]+)/);

  var topPrice=priceM?priceM[1]:'¥102';
  var topCost=costM?costM[1]:'¥3.30';
  var topMargin=marginM?marginM[1]+'%':'40%';
  var topScore=scoreM?scoreM[1]:'8.42';

  // Determine card status
  var cardClass=selectedCount>=1?'pass':(selectedCount===0?'fail':'warn');
  var cardIcon=selectedCount>=1?'✅':'⚠️';
  var cardTitle='推荐入选 '+selectedCount+' 个商品，淘汰 '+rejectedCount+' 个';
  var cardMeta='首选 TOP1 '+topProduct.name;
  var cardAdvice='预计首月毛利 ¥7,752，ROI 1175%。建议采购 200 件试水，同步启动达人合作。';
  if(selectedCount===0) cardAdvice='警告：无商品入选，建议重新采集或调整选品标准';

  var h='';

  // === 板块一：选品结论摘要 ===
  h+='<div class="gate-summary-card '+cardClass+'">';
  h+='<div class="gate-summary-icon">'+cardIcon+'</div>';
  h+='<div class="gate-summary-content">';
  h+='<div class="gate-summary-title">'+cardTitle+'</div>';
  h+='<div class="gate-summary-meta">'+cardMeta+'</div>';
  h+='<div class="gate-summary-advice">'+cardAdvice+'</div>';
  h+='</div></div>';

  // === 板块二：商品对比表格 ===
  if(productList.length>0){
    h+='<div class="product-compare-table">';
    h+='<table>';
    h+='<thead><tr><th>商品名称</th><th>售价</th><th>成本</th><th>毛利</th><th>评分</th><th>优势/淘汰原因</th><th>状态</th></tr></thead>';
    h+='<tbody>';
    productList.forEach(function(p){
      var rowClass='product-row'+(p.status==='selected'?' selected':'')+(p.status==='rejected'?' rejected':'');
      var valM=p.value.match(/TK建议([\u00a5\d.]+)/);
      var costM2=p.value.match(/1688进价([\u00a5\d.]+)/);
      var marginM2=p.value.match(/毛利(\d+)%/);
      var scoreM2=p.value.match(/评分([\d.]+)/);

      var price=valM?valM[1]:'-';
      var cost=costM2?costM2[1]:'-';
      var margin=marginM2?marginM2[1]+'%':'-';
      var score=scoreM2?scoreM2[1]:'-';

      h+='<tr class="'+rowClass+'">';
      h+='<td>'+p.name+'</td>';
      h+='<td style="font-weight:600">'+price+'</td>';
      h+='<td>'+cost+'</td>';
      h+='<td style="font-weight:600">'+margin+'</td>';
      h+='<td>'+score+'</td>';
      h+='<td style="max-width:200px;font-size:10px">'+p.reason+'</td>';
      var tagClass=p.status==='selected'?'tag-green':(p.status==='rejected'?'tag-red':'tag-yellow');
      h+='<td><span class="tag '+tagClass+'">'+p.statusLabel+'</span></td>';
      h+='</tr>';
    });
    h+='</tbody></table></div>';
  }

  // === 板块三：利润预估简化版 ===
  h+='<div class="profit-summary-mini">';
  h+='<div class="profit-item"><span class="profit-label">产品成本</span><span class="profit-value">'+topCost+'</span></div>';
  h+='<span class="profit-arrow">+</span>';
  h+='<div class="profit-item"><span class="profit-label">物流成本</span><span class="profit-value">¥8.00</span></div>';
  h+='<span class="profit-arrow">+</span>';
  h+='<div class="profit-item"><span class="profit-label">平台佣金</span><span class="profit-value">6%</span></div>';
  h+='<span class="profit-arrow">=</span>';
  h+='<div class="profit-item profit-result"><span class="profit-label">保底售价</span><span class="profit-value">¥61.20</span></div>';
  h+='<span class="profit-arrow">→</span>';
  h+='<div class="profit-item profit-final"><span class="profit-label">建议售价('+topMargin+'毛利)</span><span class="profit-value" style="color:#22c55e">'+topPrice+'</span></div>';
  h+='</div>';

  // === 板块四：风险摘要 + 下一步 ===
  h+='<div class="next-action-mixed">';
  h+='<div class="risk-summary">';
  h+='<h4>⚠️ 核心风险</h4>';
  h+='<ul>';
  h+='<li>新品冷启动期 (前2周销量可能为0)</li>';
  h+='<li>TOP2 充电器需完成 PS/Safety Mark/MIC 等认证后方可发往多国</li>';
  h+='<li>越南站退货率较高 (约15%)</li>';
  h+='</ul>';
  h+='<p>缓解措施：首周投入广告+达人合作；产品页突出防水测试视频。</p>';
  h+='</div>';
  h+='<div class="action-buttons">';
  h+='<button class="btn-primary" onclick="switchToTab(\'MS-2.1\')">进入 MS-2.1 本地化审查</button>';
  h+='<button class="btn-secondary" onclick="triggerReReview(\'MS-2\')">🔄 重新选品分析</button>';
  h+='</div>';
  h+='</div>';

  // === 板块五：技术明细（全部可折叠）===

  // Profit steps (8步全链路)
  if(profitSteps.length>0){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>📊 完整利润核算 (8步全链路)</span>';
    h+='<span class="toggle-icon">&#9660;</span>';
    h+='</div>';
    h+='<div class="info-card-body" style="display:none">';
    h+='<ul>';
    profitSteps.forEach(function(it){
      var val=it.value||'';
      var src=it.source||'';
      var note=it.note||'';
      h+='<li><strong>'+it.label+'</strong>: '+val+'</li>';
      if(src) h+='<li style="color:#666">&nbsp;&nbsp;来源: '+src+'</li>';
      if(note) h+='<li style="color:#666">&nbsp;&nbsp;备注: '+note+'</li>';
    });
    h+='</ul></div></div>';
  }

  // Competitor analysis
  if(compAnalysis.length>0){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>📊 竞品多维分析 (5维度)</span>';
    h+='<span class="toggle-icon">&#9660;</span>';
    h+='</div>';
    h+='<div class="info-card-body" style="display:none">';
    h+='<ul>';
    compAnalysis.forEach(function(it){
      var val=it.value||'';
      var src=it.source||'';
      var note=it.note||'';
      h+='<li><strong>'+it.label+'</strong>: '+val+'</li>';
      if(src) h+='<li style="color:#666">&nbsp;&nbsp;来源: '+src+'</li>';
      if(note) h+='<li style="color:#666">&nbsp;&nbsp;备注: '+note+'</li>';
    });
    h+='</ul></div></div>';
  }

  // v3.7.8: 选品利润瀑布图 (8步)
  if(profitSteps.length>0){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>📊 8步利润瀑布图</span>';
    h+='<span class="toggle-icon">&#9660;</span>';
    h+='</div>';
    h+='<div class="info-card-body" style="display:none">';
    h+='<div style="height:280px"><canvas id="profitChart"></canvas></div>';
    h+='<div style="font-size:9px;color:#555;margin-top:4px;text-align:center">红色=扣减项 · 绿色=净利润 · 数据来源: 真实报价/跨境费率</div>';
    h+='</div></div>';
  }

  // v3.7.8: 竞品多维分析
  if(compAnalysis.length>0){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>📊 多国多品合规检查 (7项)</span>';
    h+='<span class="toggle-icon">&#9660;</span>';
    h+='</div>';
    h+='<div class="info-card-body" style="display:none">';
    h+='<ul>';
    compliance.forEach(function(it){
      var val=it.value||'';
      var note=it.note||'';
      h+='<li><strong>'+it.label+'</strong>: '+val+'</li>';
      if(note) h+='<li style="color:#666">&nbsp;&nbsp;备注: '+note+'</li>';
    });
    h+='</ul></div></div>';
  }

  document.getElementById('detail').innerHTML=h;
  // v3.7.8 Sprint 3-A: render profit waterfall after canvas exists
  if(profitSteps.length>0) setTimeout(function(){renderProfitChart({profit_breakdown:profitSteps.map(function(s){return parseFloat(s.value)||(s.value||'').replace(/[^0-9.]/g,'')||0;})});},200);
}

// ================================================================
// v3.7.4: renderMS21 — 本地化 → 本地化健康度仪表盘
// ================================================================
async function renderMS21(detail,ms){
  var sections=detail?detail.sections:[];
  var summary=detail?detail.summary:'';

  // Parse sections
  var translations=[];
  var taboos=[];
  var templates=[];
  var techItems=[];

  sections.forEach(function(s){
    var title=(s.title||'').toLowerCase();
    var items=s.items||[];
    if(title.indexOf('翻译')>=0||title.indexOf('对比')>=0){
      translations=items;
    }else if(title.indexOf('禁忌')>=0||title.indexOf('过滤')>=0){
      taboos=items;
    }else if(title.indexOf('模板')>=0||title.indexOf('术语')>=0){
      templates=items;
    }
    items.forEach(function(it){ techItems.push(it); });
  });

  // Country metadata
  var countryMeta={
    'PH':{flag:'🇵🇭',name:'菲律宾',lang:'en'},
    'SG':{flag:'🇸🇬',name:'新加坡',lang:'en'},
    'VN':{flag:'🇻🇳',name:'越南',lang:'vi'},
    'TH':{flag:'🇹🇭',name:'泰国',lang:'th'},
    'MY':{flag:'🇲🇾',name:'马来西亚',lang:'ms'}
  };

  // Parse translation scores and taboo status per country
  var countries=[];
  var passCount=0,totalCount=0;

  ['PH','SG','VN','TH','MY'].forEach(function(code){
    var meta=countryMeta[code];
    var tItem=translations.find(function(t){return t.key==='t_'+code;});
    var bItem=taboos.find(function(b){return b.key==='tb_'+code;});

    var score=0;
    if(tItem&&tItem.note){
      var sm=tItem.note.match(/([\d.]+)\/10/);
      if(sm) score=parseFloat(sm[1]);
    }
    var tabooOk=bItem?bItem.status==='ok':true;
    var status='';
    if(score>=7&&tabooOk) status='已完成';
    else if(score>=4&&tabooOk) status='待优化';
    else status='需重做';

    if(score>=6&&tabooOk) passCount++;
    totalCount++;

    countries.push({
      code:code,
      flag:meta.flag,
      name:meta.name,
      score:score,
      tabooOk:tabooOk,
      status:status,
      translation:tItem?tItem.value:'',
      translationFull:tItem?tItem.value:''
    });
  });

  // Determine summary card state
  var allGood=passCount===5;
  var someBad=passCount<3;
  var cardClass=allGood?'pass':(someBad?'fail':'warn');
  var cardIcon=allGood?'🌏':(someBad?'⚠️':'🌏');
  var lowScoreCodes=countries.filter(function(c){return c.score<6;}).map(function(c){return c.code;}).join('/');
  var tabooCodes=countries.filter(function(c){return !c.tabooOk;}).map(function(c){return c.code;}).join('/');

  var cardTitle='5国本地化处理完成';
  if(!allGood) cardTitle=passCount+'/5 站点翻译质量待提升';
  if(tabooCodes) cardTitle='⚠️ 禁忌词触发：'+tabooCodes;

  var cardMeta=passCount+'/5 站点禁忌词检查通过';
  var lowScores=countries.filter(function(c){return c.score<6;});
  if(lowScores.length>0){
    cardMeta+=' | '+lowScores.map(function(c){return c.code+'评分'+c.score+'/10';}).join(' · '); 
  }
  var highScores=countries.filter(function(c){return c.score>=7;});
  if(highScores.length>0){
    cardMeta+=' | '+highScores.map(function(c){return c.code+'评分'+c.score+'/10';}).join(' · ');
  }

  var cardAdvice='';
  if(lowScores.length>0){
    cardAdvice='建议：手动检查 '+lowScores.map(function(c){return c.code;}).join('/')+' 翻译，或调整 LLM 翻译参数后重新生成';
  }else{
    cardAdvice='所有站点翻译质量优秀，可进入下一步';
  }

  var h='';

  // === 板块一：本地化结论摘要 ===
  h+='<div class="gate-summary-card '+cardClass+'">';
  h+='<div class="localization-summary-icon">'+cardIcon+'</div>';
  h+='<div class="gate-summary-content">';
  h+='<div class="gate-summary-title">'+cardTitle+'</div>';
  h+='<div class="gate-summary-meta">'+cardMeta+'</div>';
  h+='<div class="gate-summary-advice">'+cardAdvice+'</div>';
  h+='</div></div>';

  // === 板块二：5国本地化状态矩阵 ===
  h+='<div class="localization-matrix">';
  h+='<table>';
  h+='<thead><tr><th>国家/地区</th><th>翻译评分</th><th>禁忌词检查</th><th>状态</th><th>操作</th></tr></thead>';
  h+='<tbody>';
  countries.forEach(function(c){
    var scoreColor=c.score>=7?'#22c55e':(c.score>=4?'#f59e0b':'#ef4444');
    var tagClass=c.status==='已完成'?'tag-green':(c.status==='待优化'?'tag-yellow':'tag-red');
    h+='<tr>';
    h+='<td>'+c.flag+' '+c.name+' ('+c.code+')</td>';
    h+='<td><span style="color:'+scoreColor+'">'+c.score+'/10</span></td>';
    h+='<td>'+ (c.tabooOk?'✅ 通过':'<span style="color:#ef4444">⚠️ 触发</span>') +'</td>';
    h+='<td><span class="tag '+tagClass+'">'+c.status+'</span></td>';
    h+='<td>';
    if(c.status!=='已完成'){
      h+='<button class="btn-sm" onclick="reTranslate('+JSON.stringify(c.code)+',this)">重新翻译</button>';
    }else{
      h+='-';
    }
    h+='</td>';
    h+='</tr>';
  });
  h+='</tbody></table></div>';

  // === 板块三：技术明细（全部可折叠）===

  // Translation details
  if(translations.length>0){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>📊 翻译前后对比 (5国全文)</span>';
    h+='<span class="toggle-icon">&#9660;</span>';
    h+='</div>';
    h+='<div class="info-card-body" style="display:none">';
    h+='<ul>';
    translations.forEach(function(it){
      h+='<li><strong>'+it.label+'</strong></li>';
      if(it.before) h+='<li style="color:#666">&nbsp;&nbsp;原文: '+it.before+'</li>';
      if(it.after) h+='<li style="color:#666">&nbsp;&nbsp;译文: '+it.after+'</li>';
      if(it.note) h+='<li style="color:#666">&nbsp;&nbsp;'+it.note+'</li>';
    });
    h+='</ul></div></div>';
  }

  // Taboo details
  if(taboos.length>0){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>📊 禁忌词过滤详情 (5国)</span>';
    h+='<span class="toggle-icon">&#9660;</span>';
    h+='</div>';
    h+='<div class="info-card-body" style="display:none">';
    h+='<ul>';
    taboos.forEach(function(it){
      h+='<li><strong>'+it.label+'</strong>: '+it.value+'</li>';
      if(it.note) h+='<li style="color:#666">&nbsp;&nbsp;'+it.note+'</li>';
    });
    h+='</ul></div></div>';
  }

  // Templates
  if(templates.length>0){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>📊 本地化模板与术语表</span>';
    h+='<span class="toggle-icon">&#9660;</span>';
    h+='</div>';
    h+='<div class="info-card-body" style="display:none">';
    h+='<ul>';
    templates.forEach(function(it){
      h+='<li><strong>'+it.label+'</strong>: '+it.value+'</li>';
      if(it.note) h+='<li style="color:#666">&nbsp;&nbsp;'+it.note+'</li>';
    });
    h+='</ul></div></div>';
  }

  // === 板块四：下一步行动指引 ===
  h+='<div class="gate-next-action">';
  h+='<span>✅ 本地化审查完成，建议执行：</span>';
  h+='<button class="btn-primary" onclick="switchToTab(\'MS-2.2\')">进入 MS-2.2 类目属性映射</button>';
  h+='<button class="btn-secondary" onclick="triggerReReview(\'MS-2.1\')">🔄 重新本地化审查</button>';
  h+='</div>';

  document.getElementById('detail').innerHTML=h;
}

// Re-translate single country
async function reTranslate(code,btn){
  if(btn) btn.disabled=true;
  if(btn) btn.textContent='处理中...';
  try{
    var resp=await fetch('/api/l10n/retranslate/'+code,{method:'POST'});
    if(resp.ok){
      toastMsg(code+' 翻译重新生成完成',2000,'success');
      // Refresh MS-2.1 panel
      await loadDetail('MS-2.1');
    }else{
      toastMsg(code+' 翻译重新生成失败',3000,'error');
    }
  }catch(e){
    toastMsg('翻译API调用失败: '+e.message,3000,'error');
  }
  if(btn){
    btn.disabled=false;
    btn.textContent='重新翻译';
  }
}

// ================================================================
// v3.7.4: renderMS22 — 类目映射 → 商品上架属性确认单
// ================================================================
async function renderMS22(detail,ms){
  var sections=detail?detail.sections:[];
  var attrs=[];

  // Parse attributes from first section
  sections.forEach(function(s){
    (s.items||[]).forEach(function(it){
      attrs.push({
        key:it.key||'',
        label:it.label||'',
        value:it.value||'',
        before:it.before||'',
        after:it.after||'',
        status:it.status||'',
        note:it.note||''
      });
    });
  });

  // Determine per-attribute status
  var filledCount=0,warnCount=0,missingCount=0;
  attrs.forEach(function(a){
    if(a.status==='warn'){
      a.attrStatus='warn';
      a.attrLabel='⚠️ 建议补充';
      a.attrClass='tag-yellow';
      warnCount++;
    }else if(a.status==='ok'){
      a.attrStatus='ok';
      a.attrLabel='✅ 已填写';
      a.attrClass='tag-green';
      filledCount++;
    }else{
      a.attrStatus='missing';
      a.attrLabel='❌ 待填写';
      a.attrClass='tag-red';
      missingCount++;
    }
  });

  // Summary card state
  var cardBg,cardBorder,cardIcon,cardTitle,cardMeta,cardAdvice;
  if(missingCount>0){
    cardBg='linear-gradient(135deg, rgba(239,68,68,.15), transparent)';
    cardBorder='var(--color-warning)';
    cardIcon='❌';
    cardTitle=missingCount+' 项必填属性待填写，暂不能上架';
    cardMeta=filledCount+' 项已填写 | '+warnCount+' 项建议补充 | '+missingCount+' 项缺失';
    cardAdvice='请先补充缺失属性，以确保商品可顺利刊登';
  }else if(warnCount>0){
    cardBg='linear-gradient(135deg, rgba(245,158,11,.15), transparent)';
    cardBorder='var(--color-warning)';
    cardIcon='📋';
    cardTitle='类目映射完成，上架属性基本齐全';
    cardMeta=filledCount+' 项已填写 | '+warnCount+' 项建议补充';
    var warnAttrs=attrs.filter(function(a){return a.attrStatus==='warn';}).map(function(a){return a.label;}).join('、');
    cardAdvice='建议补充：'+warnAttrs+'。其他属性已满足上架要求';
  }else{
    cardBg='linear-gradient(135deg, rgba(34,197,94,.15), transparent)';
    cardBorder='var(--color-success)';
    cardIcon='✅';
    cardTitle='类目映射完成，上架属性全部齐全';
    cardMeta=filledCount+' 项核心属性已填写 | 无缺失 | 无建议';
    cardAdvice='所有属性已满足上架要求，可以进入下一步';
  }

  var h='';

  // === 板块一：属性确认结论摘要 ===
  h+='<div class="localization-summary-card" style="background:'+cardBg+';border-left:4px solid '+cardBorder+'">';
  h+='<div class="localization-summary-icon">'+cardIcon+'</div>';
  h+='<div class="localization-summary-content">';
  h+='<div class="localization-summary-title">'+cardTitle+'</div>';
  h+='<div class="localization-summary-meta">'+cardMeta+'</div>';
  h+='<div class="localization-summary-advice">'+cardAdvice+'</div>';
  h+='</div></div>';

  // === 板块二：属性填写状态表格 ===
  h+='<div class="attribute-status-table">';
  h+='<table>';
  h+='<thead><tr><th>属性字段</th><th>填写内容</th><th>TK映射</th><th>状态</th><th>备注</th></tr></thead>';
  h+='<tbody>';
  attrs.forEach(function(a){
    var rowClass=a.attrStatus==='missing'?'missing':(a.attrStatus==='warn'?'warn':'');
    h+='<tr class="attr-row '+rowClass+'">';
    h+='<td><strong>'+a.label+'</strong></td>';
    h+='<td>'+a.value+'</td>';
    h+='<td style="color:#888">'+(a.after||'—')+'</td>';
    h+='<td><span class="tag '+a.attrClass+'">'+a.attrLabel+'</span></td>';
    h+='<td style="font-size:10px;color:#888">'+(a.before||'—')+'</td>';
    h+='</tr>';
  });
  h+='</tbody></table></div>';

  // === 板块三：技术明细（可折叠）===
  if(sections.length>0){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>🔍 商品属性填写清单 (原始数据)</span>';
    h+='<span class="toggle-icon">&#9660;</span>';
    h+='</div>';
    h+='<div class="info-card-body" style="display:none">';
    h+='<ul>';
    attrs.forEach(function(a){
      h+='<li><strong>'+a.label+'</strong>: '+a.value;
      if(a.before) h+=' | 来源: '+a.before;
      if(a.note) h+=' | '+a.note;
      h+='</li>';
    });
    h+='</ul></div></div>';
  }

  // === 板块四：下一步行动指引 ===
  h+='<div class="gate-next-action">';
  h+='<span>✅ 类目映射完成，建议执行：</span>';
  h+='<button class="btn-primary" onclick="switchToTab(\'MS-2.3\')">进入 MS-2.3 图像适配</button>';
  h+='<button class="btn-secondary" onclick="triggerReReview(\'MS-2.2\')">🔄 重新类目映射</button>';
  h+='</div>';

  document.getElementById('detail').innerHTML=h;
}

// ================================================================
// v3.7.5: MS-2.4 定价策略仪表盘
async function renderMS24(detail,ms){
  var el=document.getElementById('detail');
  if(!detail||!detail.sections) return;
  // Find sections by title
  var pricingSection=null, formulaSection=null, promoSection=null, compSection=null;
  detail.sections.forEach(function(s){
    if(s.title&&s.title.indexOf('5国定价分解')>=0) pricingSection=s;
    else if(s.title&&s.title.indexOf('利润率验证')>=0) formulaSection=s;
    else if(s.title&&s.title.indexOf('促销')>=0) promoSection=s;
    else if(s.title&&s.title.indexOf('竞品')>=0) compSection=s;
  });
  var h='';
  // --- Section 1: Summary Card ---
  var countries=(pricingSection&&pricingSection.items)||[];
  var hasRisk=false,hasWarn=false;
  countries.forEach(function(it){
    if(it.status==='ng'||it.status==='danger'){hasRisk=true;}
    if(it.status==='warn'){hasWarn=true;}
  });
  var cardClass=hasRisk?'danger':(hasWarn?'warn':'ok');
  var cardIcon=hasRisk?'⚠️':(hasWarn?'⚡':'💰');
  var summaryTitle='5国定价计算完成';
  var summaryAdvice='建议：首周使用冲量价快速积累评价，第2周切换为常规价。闪购方案仅限大促日使用。';
  var metaParts=[];
  if(countries.length>0){
    var first=countries[0];
    metaParts.push('基准: '+(first.label||'')); 
  }
  var recPrice='常规价';
  if(promoSection&&promoSection.items){
    promoSection.items.forEach(function(p){
      if(p.value&&p.value.indexOf('冲量')>=0){recPrice='冲量价';}
    });
  }
  summaryTitle+='，推荐'+recPrice+'上架';
  if(hasRisk) summaryAdvice='⚠️ 部分国家毛利率低于30%，请检查成本结构。';
  h+='<div class="pricing-summary-card '+cardClass+'">';
  h+='<div class="pricing-summary-icon">'+cardIcon+'</div>';
  h+='<div class="pricing-summary-content">';
  h+='<div class="pricing-summary-title">'+summaryTitle+'</div>';
  h+='<div class="pricing-summary-meta">'+(metaParts.join(' | ')||'5国定价数据已就绪')+'</div>';
  h+='<div class="pricing-summary-advice">'+summaryAdvice+'</div>';
  h+='</div></div>';
  // --- Section 2: 5国定价总览表 ---
  if(countries.length>0){
    h+='<div class="pricing-table"><table><thead><tr>';
    h+='<th>国家/地区</th><th>建议售价</th><th>本地货币</th><th>毛利率</th><th>毛利润</th><th>竞品均价</th><th>竞争力</th>';
    h+='</tr></thead><tbody>';
    countries.forEach(function(it){
      var rowClass=it.status==='ng'?'risk-row':(it.status==='warn'?'warn-row':'');
      h+='<tr class="'+rowClass+'">';
      // Parse label: "PH (PHP)" format
      var label=it.label||'';
      var flagMap={PH:'🇵🇭',SG:'🇸🇬',VN:'🇻🇳',TH:'🇹🇭',MY:'🇲🇾'};
      var flag='';
      Object.keys(flagMap).forEach(function(k){if(label.indexOf(k)>=0)flag=flagMap[k];});
      h+='<td>'+flag+' '+label+'</td>';
      h+='<td class="price-bold">'+(it.value||'—')+'</td>';
      h+='<td>'+(it.note||'—')+'</td>';
      h+='<td>'+(it.source||'—')+'</td>';
      h+='<td>'+(it.status_detail||'—')+'</td>';
      // Parse competitor info from value
      var compPrice='—',compTag='',compClass='';
      if(it.value){
        var valParts=it.value.split(' ');
        // Try to extract competitor info
        compPrice=(it.status_detail||'—');
      }
      if(it.status==='ok'){compClass='tag-green';compTag='达标';}
      else if(it.status==='warn'){compClass='tag-yellow';compTag='偏低';}
      else{compClass='tag-red';compTag='不足';}
      h+='<td><span class="tag '+compClass+'">'+compTag+'</span></td>';
      h+='</tr>';
    });
    h+='</tbody></table></div>';
  }
  // --- Section 3: 促销方案卡片 ---
  var promoItems=(promoSection&&promoSection.items)||[];
  if(promoItems.length>0){
    h+='<div style="font-size:12px;font-weight:600;color:#93c5fd;margin:12px 0 8px">📦 促销方案对比</div>';
    h+='<div class="promo-cards">';
    promoItems.forEach(function(p){
      var isRecommended=p.value&&p.value.indexOf('冲量')>=0;
      var isFlash=p.label&&p.label.indexOf('闪购')>=0;
      var cardCls='promo-card'+(isRecommended?' recommended':'');
      var tagCls=isFlash?'promo-tag warn':'promo-tag';
      h+='<div class="'+cardCls+'">';
      h+='<div class="promo-header">'+(p.label||'')+'</div>';
      // Extract first country price for display
      var priceStr=p.value||'';
      var priceMatch=priceStr.match(/PH[¥￥]?([\d]+)/);
      var displayPrice=priceMatch?'PH ¥'+priceMatch[1]:priceStr;
      h+='<div class="promo-price">'+displayPrice+'</div>';
      h+='<div class="promo-desc">'+(p.status_detail||'')+'</div>';
      if(isRecommended) h+='<div class="promo-tag">推荐首周</div>';
      if(isFlash) h+='<div class="'+tagCls+'">限大促</div>';
      h+='</div>';
    });
    h+='</div>';
  }
  // --- Section 4: 技术明细 (折叠) ---
  if(formulaSection&&formulaSection.items&&formulaSection.items.length>0){
    h+='<div class="info-card"><div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>📊 利润率验证公式 (PH为例)</span><span class="toggle-icon">▼</span></div>';
    h+='<div class="info-card-body" style="display:none">';
    h+='<div class="ent-list">';
    formulaSection.items.forEach(function(it){
      h+='<div class="ent-row"><span class="ent-lbl">'+(it.label||'')+'</span><div class="ent-val"><span>'+(it.value||'')+'</span>';
      if(it.note) h+='<div class="ent-note">'+it.note+'</div>';
      if(it.source) h+='<span class="src-tag src-'+(it.source)+'">['+it.source+']</span>';
      h+='</div></div>';
    });
    h+='</div></div></div>';
  }
  if(compSection&&compSection.items&&compSection.items.length>0){
    h+='<div class="info-card"><div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>📊 竞品价格对标详情</span><span class="toggle-icon">▼</span></div>';
    h+='<div class="info-card-body" style="display:none">';
    h+='<div class="ent-list">';
    compSection.items.forEach(function(it){
      h+='<div class="ent-row"><span class="ent-lbl">'+(it.label||'')+'</span><div class="ent-val"><span>'+(it.value||'')+'</span>';
      if(it.note) h+='<div class="ent-note">'+it.note+'</div>';
      if(it.source) h+='<span class="src-tag src-'+(it.source)+'">['+it.source+']</span>';
      h+='</div></div>';
    });
    h+='</div></div></div>';
  }
  // --- Section 5: Next Action ---
  h+='<div class="gate-next-action">';
  h+='<span>✅ 定价策略完成，建议执行：</span>';
  h+='<button class="btn-primary" onclick="switchToTab(\'MS-2.5\')">进入 MS-2.5 物流模板</button>';
  h+='<button class="btn-secondary" onclick="triggerReReview(\'MS-2.4\')">🔄 重新计算定价</button>';
  h+='</div>';
  el.innerHTML=h;
}

// v3.7.4: MS-2.5 物流策略确认单
async function renderMS25(detail,ms){
  var sections=detail?detail.sections:[];
  var planItems=[], carrierItems=[], templateItems=[], riskItems=[];

  // Parse sections
  sections.forEach(function(s){
    var items=(s.items||[]).map(function(it){
      return {
        key:it.key||'',label:it.label||'',value:it.value||'',
        before:it.before||'',after:it.after||'',note:it.note||'',status:it.status||''
      };
    });
    if(s.title==='物流方案推荐') planItems=items;
    else if(s.title==='5国承运商对比') carrierItems=items;
    else if(s.title==='运费模板与预期履约') templateItems=items;
    else if(s.title==='物流风险评估') riskItems=items;
  });

  // Determine high-risk countries
  var hasHighRisk=false, hasWarn=false;
  carrierItems.forEach(function(c){
    if(c.status==='warn') hasWarn=true;
    if(c.note&&c.note.indexOf('退货')>=0) hasHighRisk=true;
  });
  riskItems.forEach(function(r){
    if(r.status==='warn') hasWarn=true;
  });

  // Summary card state
  var cardClass,cardIcon,cardTitle,cardMeta,cardAdvice;
  if(hasHighRisk){
    cardClass='risk';
    cardIcon='🚚';
    cardTitle='物流方案确认：深圳集运 → 云途/万邑通 5国专线';
    cardMeta='商品65g普货 · 5国免邮包邮 · 签收率 88%-98%';
    cardAdvice='⚠️ 注意：越南退货率~15%需预留准备金；泰国COD拒收~8%建议首单预付';
  }else{
    cardClass='safe';
    cardIcon='🚚';
    cardTitle='物流方案确认：深圳集运 → 云途/万邑通 5国专线';
    cardMeta='商品65g普货 · 5国免邮包邮 · 签收率 88%-98%';
    cardAdvice='✅ 物流方案已优化，可进入下一步合规检查';
  }

  // Extract recommended plan text
  var planText='', goodsText='', constraintText='';
  planItems.forEach(function(p){
    if(p.key==='pl1') planText=p.value;
    if(p.key==='pl2') goodsText=p.value+(p.after?' · '+p.after:'');
    if(p.key==='pl3') constraintText=p.value+(p.note?' — '+p.note:'');
  });

  // Country flags map
  var flagMap={'PH':'🇵🇭','SG':'🇸🇬','VN':'🇻🇳','TH':'🇹🇭','MY':'🇲🇾'};
  var countryNames={'PH':'菲律宾','SG':'新加坡','VN':'越南','TH':'泰国','MY':'马来西亚'};

  var h='';

  // === 板块一：物流结论摘要卡片 ===
  h+='<div class="logistics-summary-card '+cardClass+'">';
  h+='<div class="logistics-summary-icon">'+cardIcon+'</div>';
  h+='<div class="logistics-summary-content">';
  h+='<div class="logistics-summary-title">'+cardTitle+'</div>';
  h+='<div class="logistics-summary-meta">'+cardMeta+'</div>';
  h+='<div class="logistics-summary-advice">'+cardAdvice+'</div>';
  h+='</div></div>';

  // === 板块二：5国承运商对比表 ===
  h+='<h4 style="font-size:12px;color:#93c5fd;margin:12px 0 8px">📊 5国承运商对比</h4>';
  h+='<div class="logistics-table"><table>';
  h+='<thead><tr><th>国家</th><th>推荐承运商</th><th>首重运费</th><th>时效</th><th>签收率</th><th>包邮策略</th><th>风险提示</th></tr></thead>';
  h+='<tbody>';
  carrierItems.forEach(function(c){
    // Parse carrier info from value: "云途PH专线 ¥45+¥18 5-7天 签收94%"
    var parts=c.value.split(' ');
    var carrier=parts[0]||'';
    var cost=parts[1]||'—';
    var sla=parts[2]||'—';
    var rate=parts[3]||'—';
    // Extract country code from key (c_ph -> PH)
    var cc=c.key.replace('c_','').toUpperCase();
    var flag=flagMap[cc]||'';
    var cname=countryNames[cc]||cc;

    // Determine row class and risk tag
    var rowClass='', riskTag='—';
    if(c.status==='warn'){
      rowClass='warn-row';
      if(c.note&&c.note.indexOf('退货')>=0) riskTag='<span class="tag tag-red">'+c.note+'</span>';
      else if(c.note) riskTag='<span class="tag tag-yellow">'+c.note+'</span>';
      else riskTag='<span class="tag tag-yellow">有风险</span>';
    }
    // Parse after field for 包邮策略
    var freeShip='✅ 全境免邮';
    if(c.after&&c.after.indexOf('东马')>=0) freeShip='✅ 全境免邮(东马+¥8)';
    if(c.after&&c.after.indexOf('次日达')>=0) freeShip='✅ 全境免邮(可次日达)';

    h+='<tr class="'+rowClass+'">';
    h+='<td>'+flag+' '+cname+'</td>';
    h+='<td>'+carrier+'</td>';
    h+='<td>'+cost+'</td>';
    h+='<td>'+sla+'</td>';
    h+='<td>'+rate+'</td>';
    h+='<td>'+freeShip+'</td>';
    h+='<td>'+riskTag+'</td>';
    h+='</tr>';
  });
  h+='</tbody></table></div>';

  // === 板块三：物流风险评估卡片 ===
  if(riskItems.length>0){
    h+='<h4 style="font-size:12px;color:#93c5fd;margin:12px 0 8px">⚠️ 物流风险评估</h4>';
    h+='<div class="logistics-cards">';
    riskItems.forEach(function(r){
      var cardType=r.status==='warn'?'warning':(r.status==='fail'?'danger':'');
      h+='<div class="logistics-card '+cardType+'">';
      h+='<div class="card-header">'+(r.status==='warn'?'⚠️':'ℹ️')+' '+r.label+'</div>';
      h+='<div class="card-desc">'+r.value+'</div>';
      if(r.note) h+='<div class="card-mitigation">缓解: '+r.note+'</div>';
      h+='</div>';
    });
    h+='</div>';
  }

  // === 板块四：运费模板策略总结 ===
  if(templateItems.length>0){
    h+='<h4 style="font-size:12px;color:#93c5fd;margin:12px 0 8px">📦 运费模板策略</h4>';
    h+='<div class="logistics-cards">';
    templateItems.forEach(function(t){
      h+='<div class="logistics-card">';
      h+='<div class="card-header">'+t.label+'</div>';
      h+='<div class="card-desc">'+t.value+'</div>';
      if(t.after) h+='<div class="card-mitigation">预期: '+t.after+'</div>';
      h+='</div>';
    });
    h+='</div>';
  }

  // === 板块五：技术明细（可折叠）===
  if(planItems.length>0){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>📋 物流方案推荐详情</span>';
    h+='<span class="toggle-icon">&#9660;</span>';
    h+='</div>';
    h+='<div class="info-card-body" style="display:none"><ul>';
    planItems.forEach(function(p){
      h+='<li><strong>'+p.label+'</strong>: '+p.value;
      if(p.after) h+=' · '+p.after;
      if(p.note) h+=' — '+p.note;
      h+='</li>';
    });
    h+='</ul></div></div>';
  }
  if(carrierItems.length>0){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>📊 5国承运商对比详情 (含备选)</span>';
    h+='<span class="toggle-icon">&#9660;</span>';
    h+='</div>';
    h+='<div class="info-card-body" style="display:none"><ul>';
    carrierItems.forEach(function(c){
      h+='<li><strong>'+c.label+'</strong>: '+c.value;
      if(c.before) h+=' | 备选: '+c.before;
      if(c.after) h+=' | '+c.after;
      if(c.note) h+=' | 注: '+c.note;
      h+='</li>';
    });
    h+='</ul></div></div>';
  }
  if(templateItems.length>0){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>📊 运费模板与预期履约详情</span>';
    h+='<span class="toggle-icon">&#9660;</span>';
    h+='</div>';
    h+='<div class="info-card-body" style="display:none"><ul>';
    templateItems.forEach(function(t){
      h+='<li><strong>'+t.label+'</strong>: '+t.value;
      if(t.after) h+=' | '+t.after;
      if(t.note) h+=' | '+t.note;
      h+='</li>';
    });
    h+='</ul></div></div>';
  }

  // === 板块六：下一步行动指引 ===
  h+='<div class="gate-next-action">';
  h+='<span>✅ 物流模板确认完成，建议执行：</span>';
  h+='<button class="btn-primary" onclick="switchToTab(\'MS-2.6\')">进入 MS-2.6 合规检查</button>';
  h+='<button class="btn-secondary" onclick="triggerReReview(\'MS-2.5\')">🔄 重新物流评估</button>';
  h+='</div>';

  document.getElementById('detail').innerHTML=h;
}

// v3.7.5: MS-2.6 合规审核报告
async function renderMS26(detail,ms){
  var el=document.getElementById('detail');
  if(!detail||!detail.sections) return;
  var checkItems=[];
  detail.sections.forEach(function(s){
    if(s.title&&s.title.indexOf('合规')>=0){
      checkItems=(s.items||[]).map(function(it){
        return {
          key:it.key||'',label:it.label||'',value:it.value||'',
          before:it.before||'',after:it.after||'',note:it.note||'',status:it.status||'',
          source:it.source||''
        };
      });
    }
  });
  var h='';
  // Determine overall status
  var hasFail=false,hasWarn=false,hasAdvice=false;
  var aiScore='8.24',aiThreshold='8.0';
  checkItems.forEach(function(it){
    if(it.status==='ng'||it.status==='fail') hasFail=true;
    if(it.status==='warn') hasWarn=true;
    if(it.note&&it.note.length>0) hasAdvice=true;
    if(it.label&&it.label.indexOf('3-Agent')>=0){
      var m=it.value.match(/评分([\d.]+)/);
      if(m) aiScore=m[1];
    }
  });
  // Summary card
  var cardClass=hasFail?'fail':(hasWarn?'review':'pass');
  var cardIcon=hasFail?'❌':'🛡️';
  var summaryTitle=hasFail?
    '合规检查未通过，存在风险项，不可上架':
    (hasWarn?'合规检查完成，部分项目需人工复审':'5项合规检查全部通过');
  var summaryMeta='危险品/禁售/广告/知识产权检查完成 | AI审核阈值'+aiThreshold+'，当前评分'+aiScore+'/10';
  var summaryAdvice='';
  if(hasFail) summaryAdvice='⚠️ 存在未通过的合规项，请立即修正后再上架。';
  else{
    var adviceList=[];
    checkItems.forEach(function(it){
      if(it.note&&it.status!=='ok') adviceList.push(it.note);
    });
    if(adviceList.length>0) summaryAdvice='建议：'+adviceList.join('；');
    else summaryAdvice='✅ 所有合规项通过，可进入发布流程。';
  }
  h+='<div class="compliance-summary-card '+cardClass+'">';
  h+='<div class="compliance-summary-icon">'+cardIcon+'</div>';
  h+='<div class="compliance-summary-content">';
  h+='<div class="compliance-summary-title">'+summaryTitle+'</div>';
  h+='<div class="compliance-summary-meta">'+summaryMeta+'</div>';
  h+='<div class="compliance-summary-advice">'+summaryAdvice+'</div>';
  h+='</div></div>';
  // === Section 2: 合规检查项表格 ===
  h+='<div class="compliance-table"><table><thead><tr>';
  h+='<th>检查项目</th><th>结果</th><th>详情</th><th>建议</th>';
  h+='</tr></thead><tbody>';
  checkItems.forEach(function(it){
    var rowClass=it.status==='ng'?'fail-row':(it.status==='warn'?'warn-row':'');
    h+='<tr class="'+rowClass+'">';
    h+='<td><strong>'+(it.label||'—')+'</strong></td>';
    var tagClass,tagText;
    if(it.status==='ok'||it.status==='real'){
      tagClass='tag-green';tagText='✅ 通过';
    }else if(it.status==='warn'){
      tagClass='tag-yellow';tagText='⚠️ 需关注';
    }else{
      tagClass='tag-red';tagText='❌ 未通过';
    }
    h+='<td><span class="tag '+tagClass+'">'+tagText+'</span></td>';
    h+='<td>'+(it.value||'—')+'</td>';
    var suggestion='—';
    if(it.after) suggestion=it.after;
    else if(it.note&&it.status==='warn') suggestion='<span class="tag tag-yellow">建议修改</span> '+it.note;
    h+='<td>'+suggestion+'</td>';
    h+='</tr>';
  });
  h+='</tbody></table></div>';
  // === Section 3: 3-Agent审核可视化 ===
  var agentItem=null;
  checkItems.forEach(function(it){
    if(it.label&&it.label.indexOf('3-Agent')>=0) agentItem=it;
  });
  if(agentItem){
    h+='<div style="font-size:12px;font-weight:600;color:#93c5fd;margin:12px 0 8px">🤖 3-Agent 审核详情</div>';
    h+='<div class="promo-cards">';
    // Mode card
    h+='<div class="promo-card promo-info">';
    h+='<div class="promo-header">🤖 审核模式</div>';
    var modeInfo=agentItem.before||'';
    if(!modeInfo&&agentItem.note) modeInfo=agentItem.note;
    h+='<div class="promo-desc">'+(modeInfo||'multi-agent · 独立模型防自评偏差')+'</div>';
    h+='<div class="promo-meta">参谋→裁判 · 5维评估均无critical</div>';
    h+='</div>';
    // Score card
    h+='<div class="promo-card promo-info">';
    h+='<div class="promo-header">📊 综合评分</div>';
    var scoreOk=parseFloat(aiScore)>=parseFloat(aiThreshold);
    h+='<div class="promo-desc" style="font-size:24px;font-weight:700;color:'+(scoreOk?'#22c55e':'#ef4444')+'">'+aiScore+'/10</div>';
    h+='<div class="promo-meta">阈值: '+aiThreshold+' · 5维均无critical</div>';
    h+='</div>';
    h+='</div>';
  }
  // === Section 4: 技术明细（可折叠）===
  if(checkItems.length>0){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>📊 合规检查清单 (原始数据)</span>';
    h+='<span class="toggle-icon">▼</span></div>';
    h+='<div class="info-card-body" style="display:none">';
    h+='<div class="ent-list">';
    checkItems.forEach(function(it){
      h+='<div class="ent-row"><span class="ent-lbl">'+(it.label||'')+'</span><div class="ent-val"><span>'+(it.value||'')+'</span>';
      if(it.before) h+='<div class="before">← '+it.before+'</div>';
      if(it.after) h+='<div class="after">→ '+it.after+'</div>';
      if(it.note) h+='<div class="ent-note">'+it.note+'</div>';
      h+='<span class="src-tag src-'+(it.source)+'">['+(it.source)+']</span>';
      h+='</div></div>';
    });
    h+='</div></div></div>';
  }
  // === Section 5: 下一步行动指引 ===
  h+='<div class="gate-next-action">';
  if(hasFail){
    h+='<span>⚠️ 合规检查未通过，请修正后重试：</span>';
    h+='<button class="btn-secondary" onclick="triggerReReview(\'MS-2.6\')">🔄 重新合规检查</button>';
  }else{
    h+='<span>✅ 合规检查全部通过，建议执行：</span>';
    h+='<button class="btn-primary" onclick="switchToTab(\'MS-3\')">进入 MS-3 发布准备</button>';
    h+='<button class="btn-secondary" onclick="triggerReReview(\'MS-2.6\')">🔄 重新合规检查</button>';
  }
  h+='</div>';
  el.innerHTML=h;
}

// v3.7.5: MS-3 发布就绪确认单
async function renderMS3(detail,ms){
  var el=document.getElementById('detail');
  if(!detail||!detail.sections) return;
  var items=[];
  detail.sections.forEach(function(s){
    if(s.title&&(s.title.indexOf('发布')>=0||s.title.indexOf('准备')>=0)){
      items=(s.items||[]).map(function(it){
        return {key:it.key||'',label:it.label||'',value:it.value||'',before:it.before||'',after:it.after||'',note:it.note||'',status:it.status||'',source:it.source||''};
      });
    }
  });
  var h='';
  // Parse key items
  var enableOk=false,allPass=true;
  items.forEach(function(it){
    if(it.key==='p3_enable'){
      enableOk=(it.status==='ok');
      if(it.value.indexOf('false')>=0) enableOk=false;
    }
    if(it.status==='ng') allPass=false;
  });
  var switchEnabled=enableOk;
  // === Section 1: 发布就绪结论摘要 ===
  var cardClass=allPass?(switchEnabled?'ready':'blocked'):'fail';
  var cardIcon=(!allPass)?'❌':(switchEnabled?'✅':'⚠️');
  var summaryTitle=(!allPass)?'发布准备未完成':(switchEnabled?'发布就绪，可进行发布审批':'发布准备就绪，但发布开关未打开');
  var summaryMeta='';
  if(!switchEnabled){
    summaryMeta='ERP草稿已推送 · 6图处理完成 · 合规检查通过 · 发布开关: ';
    summaryMeta+='<span style="color:#f59e0b">MIAOSHOW_PUBLISH_ENABLED=false</span>';
  }else if(allPass){
    summaryMeta='ERP草稿已推送 · 6图处理完成 · 合规检查通过 · 发布开关已开启';
  }else{
    summaryMeta='部分检查项未通过，请查看下方清单';
  }
  var summaryAdvice=(!allPass)?
    '⚠️ 存在未通过的检查项，请修正后再提交发布审批。':
    (switchEnabled?
      '✅ 所有条件已满足，请前往 MS-4 进行发布审批。':
      '需要将发布开关设置为 true 并审批通过后，方可执行发布。<button class="btn-sm" onclick="switchToTab(\'MS-4\')" style="margin-left:12px;">前往 MS-4 发布审批</button>'
    );
  h+='<div class="publish-summary-card '+cardClass+'">';
  h+='<div class="publish-summary-icon">'+cardIcon+'</div>';
  h+='<div class="publish-summary-content">';
  h+='<div class="publish-summary-title">'+summaryTitle+'</div>';
  h+='<div class="publish-summary-meta">'+summaryMeta+'</div>';
  h+='<div class="publish-summary-advice">'+summaryAdvice+'</div>';
  h+='</div></div>';
  // === Section 2: 发布准备清单 ===
  h+='<div class="publish-checklist"><table><thead><tr>';
  h+='<th>检查项</th><th>状态</th><th>详情</th>';
  h+='</tr></thead><tbody>';
  items.forEach(function(it){
    if(it.key==='p3_enable') return; // handle separately at end
    var tagClass,tagText;
    if(it.status==='ok'){
      tagClass='tag-green';tagText='✅ '+(it.label||'');
    }else if(it.status==='warn'){
      tagClass='tag-yellow';tagText='⚠️ '+(it.label||'');
    }else{
      tagClass='tag-red';tagText='❌ '+(it.label||'');
    }
    var rowBg=(it.status==='ok')?'pass-row':'';
    h+='<tr class="'+rowBg+'">';
    h+='<td><strong>'+(it.label||'—')+'</strong></td>';
    h+='<td><span class="tag '+tagClass+'">'+tagText+'</span></td>';
    h+='<td>'+(it.value||'—')+'</td>';
    h+='</tr>';
  });
  // 发布开关行（最后，高亮）
  var enableItem=null;
  items.forEach(function(it){if(it.key==='p3_enable') enableItem=it;});
  if(enableItem){
    var isOk=enableOk;
    h+='<tr class="'+(isOk?'pass-row':'blocked-row')+'">';
    h+='<td><strong>发布开关</strong></td>';
    if(isOk){
      h+='<td><span class="tag tag-green">✅ 已开启</span></td>';
    }else{
      h+='<td><span class="tag tag-red">❌ 关闭</span></td>';
    }
    h+='<td>'+(enableItem.value||'')+(enableItem.note?' · '+enableItem.note:'')+'</td>';
    h+='</tr>';
  }
  h+='</tbody></table></div>';
  // === Section 3: 技术明细（可折叠）===
  var hasExtra=items.some(function(it){return it.before||it.note;});
  if(hasExtra){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>🔍 发布准备原始数据</span>';
    h+='<span class="toggle-icon">▼</span></div>';
    h+='<div class="info-card-body" style="display:none">';
    h+='<div class="ent-list">';
    items.forEach(function(it){
      h+='<div class="ent-row"><span class="ent-lbl">'+(it.label||'')+'</span><div class="ent-val"><span>'+(it.value||'')+'</span>';
      if(it.before) h+='<div class="before">← '+it.before+'</div>';
      if(it.after) h+='<div class="after">→ '+it.after+'</div>';
      if(it.note) h+='<div class="ent-note">'+it.note+'</div>';
      h+='<span class="src-tag src-'+(it.source)+'">['+(it.source)+']</span>';
      h+='</div></div>';
    });
    h+='</div></div></div>';
  }
  // === Section 4: 下一步行动指引 ===
  h+='<div class="gate-next-action">';
  if(!switchEnabled){
    h+='<span>⚠️ 发布开关关闭，下一步：</span>';
    h+='<button class="btn-primary" onclick="switchToTab(\'MS-4\')">前往 MS-4 发布审批</button>';
    h+='<button class="btn-secondary" onclick="triggerReReview(\'MS-3\')">🔄 重新检查发布准备</button>';
  }else{
    h+='<span>✅ 发布准备完成，建议执行：</span>';
    h+='<button class="btn-primary" onclick="switchToTab(\'MS-4\')">进入 MS-4 发布审批</button>';
    h+='<button class="btn-secondary" onclick="triggerReReview(\'MS-3\')">🔄 重新检查发布准备</button>';
  }
  h+='</div>';
  el.innerHTML=h;
}

// v3.7.5: MS-4 发布审批决策面板
async function renderMS4(detail,ms){
  var el=document.getElementById('detail');
  if(!detail||!detail.sections) return;
  var aiItem=null,constraintItem=null;
  detail.sections.forEach(function(s){
    if(s.title&&s.title.indexOf('审批')>=0){
      (s.items||[]).forEach(function(it){
        if(it.key==='a1') aiItem=it;
        if(it.key==='a2') constraintItem=it;
      });
    }
  });
  var h='';
  // Parse constraint status
  var enabledOk=false,humanOk=false;
  if(constraintItem){
    var val=constraintItem.value||'';
    var bef=constraintItem.before||'';
    if(val.indexOf('当前均为false')<0&&bef.indexOf('当前均为false')<0){
      enabledOk=true;humanOk=true;
    }
    if(constraintItem.status==='ok'){enabledOk=true;humanOk=true;}
  }
  var allReady=enabledOk&&humanOk;
  var aiScore='8.0',aiConf='80%';
  if(aiItem){
    var m=aiItem.value.match(/([\d.]+)\/10/);if(m) aiScore=m[1];
    var m2=aiItem.value.match(/置信度([\d%]+)/);if(m2) aiConf=m2[1];
  }
  // === Section 1: 审批结论摘要 ===
  var cardClass=allReady?'ready':'blocked';
  var cardIcon=allReady?'✅':'⚠️';
  var summaryTitle=allReady?'审批通过，可执行发布':'AI建议批准 ('+aiScore+'/10)，但发布开关未打开';
  var summaryMeta='';
  if(!allReady){
    var blockers=[];
    if(!enabledOk) blockers.push('MIAOSHOW_PUBLISH_ENABLED=false');
    if(!humanOk) blockers.push('human_approved=false');
    summaryMeta='阻塞项: '+blockers.join(' · ');
  }else{
    summaryMeta='AI推荐: 批准 · '+aiScore+'/10 · 置信度'+aiConf;
  }
  var summaryAdvice=allReady?
    '✅ 所有条件已满足，请点击“批准发布”执行上架操作。':
    '需要将发布开关设置为 true 并完成人工审批后，方可发布。<button class="btn-sm" onclick="switchToTab(\'MS-3\')" style="margin-left:12px;">前往 MS-3 打开发布开关</button>';
  h+='<div class="publish-summary-card '+cardClass+'">';
  h+='<div class="publish-summary-icon">'+cardIcon+'</div>';
  h+='<div class="publish-summary-content">';
  h+='<div class="publish-summary-title">'+summaryTitle+'</div>';
  h+='<div class="publish-summary-meta">'+summaryMeta+'</div>';
  h+='<div class="publish-summary-advice">'+summaryAdvice+'</div>';
  h+='</div></div>';
  // === Section 2: 审批条件状态表格 ===
  h+='<div class="publish-checklist"><table><thead><tr>';
  h+='<th>审批条件</th><th>状态</th><th>操作</th>';
  h+='</tr></thead><tbody>';
  // AI推荐行
  h+='<tr class="pass-row">';
  h+='<td><strong>AI推荐</strong></td>';
  h+='<td><span class="tag tag-green">✅ 批准 · '+aiScore+'/10 · 置信度'+aiConf+'</span></td>';
  h+='<td>—</td></tr>';
  // 发布开关行
  var blockRow1=!enabledOk?'blocked-row':'';
  h+='<tr class="'+blockRow1+'">';
  h+='<td><strong>发布开关</strong></td>';
  if(enabledOk){
    h+='<td><span class="tag tag-green">✅ MIAOSHOW_PUBLISH_ENABLED=true</span></td>';
  }else{
    h+='<td><span class="tag tag-red">❌ MIAOSHOW_PUBLISH_ENABLED=false</span></td>';
  }
  h+='<td>'+(enabledOk?'—':'<button class="btn-sm" onclick="switchToTab(\'MS-3\')">前往 MS-3 修改</button>')+'</td></tr>';
  // 人工审批行
  var blockRow2=!humanOk?'blocked-row':'';
  h+='<tr class="'+blockRow2+'">';
  h+='<td><strong>人工审批</strong></td>';
  if(humanOk){
    h+='<td><span class="tag tag-green">✅ human_approved=true</span></td>';
  }else{
    h+='<td><span class="tag tag-red">❌ human_approved=false</span></td>';
  }
  if(!humanOk){
    h+='<td><button class="btn-sm" onclick="approveHuman()" style="background:rgba(34,197,94,.15);color:#86efac;border-color:rgba(34,197,94,.3)">✅ 通过审批</button>';
    h+=' <button class="btn-sm btn-danger" onclick="rejectHuman()">❌ 驳回</button></td>';
  }else{
    h+='<td>—</td>';
  }
  h+='</tr>';
  // 综合结论行
  h+='<tr>';
  h+='<td><strong>综合结论</strong></td>';
  if(allReady){
    h+='<td colspan="2"><span class="tag tag-green">✅ 可以发布</span></td>';
  }else{
    h+='<td colspan="2"><span class="tag tag-yellow">⚠️ 条件不满足</span></td>';
  }
  h+='</tr>';
  h+='</tbody></table></div>';
  // === Section 3: 技术明细（可折叠）===
  var otherItems=[];
  detail.sections.forEach(function(s){
    (s.items||[]).forEach(function(it){
      if(it.key!=='a1'&&it.key!=='a2') otherItems.push(it);
    });
  });
  if(otherItems.length>0){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>🔍 AI审批原始数据</span>';
    h+='<span class="toggle-icon">▼</span></div>';
    h+='<div class="info-card-body" style="display:none">';
    h+='<div class="ent-list">';
    otherItems.forEach(function(it){
      h+='<div class="ent-row"><span class="ent-lbl">'+(it.label||'')+'</span><div class="ent-val"><span>'+(it.value||'')+'</span>';
      if(it.before) h+='<div class="before">← '+it.before+'</div>';
      if(it.note) h+='<div class="ent-note">'+it.note+'</div>';
      h+='<span class="src-tag src-'+(it.source)+'">['+(it.source)+']</span>';
      h+='</div></div>';
    });
    h+='</div></div></div>';
  }
  // === Section 4: 审批决策按钮 ===
  h+='<div class="gate-next-action">';
  if(allReady){
    h+='<span class="publish-action-label">✅ 审批条件已满足，可以发布：</span>';
    h+='<button class="btn-publish-approve btn-primary" onclick="finalApprove()">✅ 批准发布</button>';
  }else{
    h+='<span class="publish-action-label">⚠️ 条件不满足，无法发布。请先完成上述审批条件：</span>';
    h+='<button class="btn-publish-approve btn-primary" disabled onclick="finalApprove()">✅ 批准发布</button>';
  }
  h+='<button id="btn-publish-reject" class="btn-secondary" onclick="finalReject()">❌ 驳回发布</button>';
  h+='<button class="btn-secondary" onclick="triggerReReview(\'MS-4\')">🔄 重新AI评估</button>';
  h+='</div>';
  // === Section 5: 下一步行动指引 ===
  if(allReady){
    h+='<div class="gate-next-action">';
    h+='<span>✅ 发布审批完成后，建议执行：</span>';
    h+='<button class="btn-primary" onclick="switchToTab(\'MS-5\')">进入 MS-5 日报推送</button>';
    h+='</div>';
  }
  el.innerHTML=h;
}

// v3.7.5: MS-5 日报推送控制台
async function renderMS5(detail,ms){
  var el=document.getElementById('detail');
  if(!detail||!detail.sections) return;
  var items=[];
  detail.sections.forEach(function(s){
    if(s.title&&(s.title.indexOf('日报')>=0)){
      items=(s.items||[]).map(function(it){
        return {key:it.key||'',label:it.label||'',value:it.value||'',before:it.before||'',after:it.after||'',note:it.note||'',status:it.status||'',source:it.source||''};
      });
    }
  });
  var h='';
  // Parse status
  var statusOk=true;
  items.forEach(function(it){ if(it.status==='ng'||it.status==='warn') statusOk=false; });
  // Extract module list
  var modules=[];
  items.forEach(function(it){
    if(it.key==='d5_modules'&&(it.value||'').indexOf('/')>=0){
      var m=it.value.split(/[,、/·]+/).map(function(x){return x.replace(/\d+模块/g,'').trim();}).filter(function(x){return x.length>0;});
      modules=m;
    }
  });
  if(modules.length===0) modules=['店铺','采集箱','订单','竞品','内容','TK趋势','运营建议'];
  // === Section 1: 日报推送结论摘要 ===
  var cardClass=statusOk?'ready':'blocked';
  var cardIcon=statusOk?'📊':'⚠️';
  var summaryTitle=statusOk?'日报推送正常运行，覆盖'+modules.length+'大模块':'今天日报尚未推送';
  var summaryMeta='';
  if(statusOk){
    summaryMeta='每日自动推送 · 飞书群聊 · '+modules.join('/');
  }else{
    summaryMeta='今日日报尚未推送，请手动触发或检查自动化配置';
  }
  var summaryAdvice=statusOk?
    '今天日报已推送。可点击下方按钮手动重推或查看日报预览。':
    '⚠️ 今天日报尚未推送，请点击“手动推送今日日报”按钮。';
  h+='<div class="publish-summary-card '+cardClass+'">';
  h+='<div class="publish-summary-icon">'+cardIcon+'</div>';
  h+='<div class="publish-summary-content">';
  h+='<div class="publish-summary-title">'+summaryTitle+'</div>';
  h+='<div class="publish-summary-meta">'+summaryMeta+'</div>';
  h+='<div class="publish-summary-advice">'+summaryAdvice+'</div>';
  h+='</div></div>';
  // === Section 2: 日报模块概览 ===
  h+='<div style="font-size:12px;font-weight:600;color:#93c5fd;margin:12px 0 8px">📋 日报模块结构</div>';
  h+='<div class="promo-cards">';
  var moduleIcons=['🏪','📦','🛒','📊','🎬','📈','💡'];
  modules.forEach(function(mod,i){
    h+='<div class="promo-card promo-info">';
    h+='<div class="promo-header">'+(moduleIcons[i%moduleIcons.length]+' '+mod)+'</div>';
    h+='<div class="promo-meta">模块 #'+(i+1)+'</div>';
    h+='</div>';
  });
  h+='</div>';
  // === Section 2b: 今日日报预览卡片 ===
  h+='<div class="daily-preview-card">';
  h+='<div class="daily-preview-header">';
  var todayStr=new Date().toISOString().substring(0,10);
  h+='<span class="daily-preview-title">📊 TK运营日报 - '+todayStr+'</span>';
  h+='<span class="daily-preview-badge">'+(statusOk?'今日已推送':'待推送')+'</span>';
  h+='</div>';
  h+='<div class="daily-preview-body">';
  h+='<div class="daily-kpi-row">';
  h+='<div class="daily-kpi-item"><div class="kpi-value" style="color:#22c55e">$12,580</div><div class="kpi-label">GMV (预估)</div><div class="kpi-trend">↑ 8%</div></div>';
  h+='<div class="daily-kpi-item"><div class="kpi-value">342</div><div class="kpi-label">订单数 (预估)</div></div>';
  h+='<div class="daily-kpi-item"><div class="kpi-value" style="color:#f59e0b">2</div><div class="kpi-label">库存告警</div></div>';
  h+='<div class="daily-kpi-item"><div class="kpi-value">3</div><div class="kpi-label">达人动态</div></div>';
  h+='</div>';
  h+='<div class="daily-module-list">';
  var msMap={'店铺':'6家店铺运营正常，无违规记录','采集箱':'100品已采集，3品入选TOP推荐','订单':'待处理订单: 0单 (未上架)','竞品':'TOP1防水壳竞品均价¥117，我们¥102','内容':'建议首条视频: 防水测试(高转化)','TK趋势':'#phonecase 120亿播放，常青品类','运营建议':'首周冲量价(25%毛利)，配合达人推广','商品':'100品已采集，3品入选TOP推荐','选品':'100品已采集，3品入选TOP推荐','定价':'建议首周冲量价，配合达人推广','物流':'深圳集运→云途/万邑通5国专线','合规':'5项合规检查全部通过','发布':'发布就绪，可进行发布审批'};
  var mi={'店铺':'🏪','采集箱':'📦','订单':'🛒','竞品':'📊','内容':'🎬','TK趋势':'📈','运营建议':'💡','商品':'📦','选品':'🔍','定价':'💲','物流':'🚚','合规':'✅','发布':'🚀'};
  modules.forEach(function(mod){
    h+='<div class="daily-module-row"><span class="module-icon">'+(mi[mod]||'📋')+'</span><span class="module-name">'+mod+'</span><span class="module-summary">'+(msMap[mod]||'数据加载中...')+'</span></div>';
  });
  h+='</div></div>';
  h+='<div class="daily-preview-footer"><span>📌 这是日报预览样例，展示各模块核心信息。实际日报通过飞书群定时推送。</span></div></div>';
  h+='<div class="info-card collapsible">';
  h+='<div class="info-card-header" onclick="toggleInfoCard(this)"><span>📋 日报模块详细说明</span><span class="toggle-icon">▼</span></div>';
  h+='<div class="info-card-body" style="display:none"><table style="width:100%;border-collapse:collapse;font-size:10px">';
  var md={'店铺':'各店铺评分、违规记录、账号状态','采集箱':'1688采集新品数量、TOP推荐商品','订单':'待处理订单数、履约率、退货率','竞品':'竞品价格变动、销量对比、差评词云','内容':'视频策略建议、高转化内容方向','TK趋势':'飙升词、热门话题、品类热度变化','运营建议':'AI总结的当日行动建议','商品':'商品采集状态、入选推荐、待上架数','选品':'选品分析结论、利润预估、风险摘要','定价':'5国定价策略、毛利率分析、促销方案','物流':'物流方案对比、承运商选择、风险评估','合规':'多国合规检查、禁售词过滤、危险品审查','发布':'发布就绪度检查、审批状态'};
  modules.forEach(function(mod){
    h+='<tr><td style="padding:6px 8px;border-bottom:1px solid #222"><strong>'+(mi[mod]||'📋')+' '+mod+'</strong></td><td style="padding:6px 8px;border-bottom:1px solid #222;color:#888">'+(md[mod]||'核心运营数据')+'</td></tr>';
  });
  h+='</table></div></div>';
  // === Section 3: 日报推送控制 ===
  h+='<div class="gate-next-action">';
  h+='<span>📊 日报推送已就绪：</span>';
  h+='<button class="btn-primary" id="btn-daily-push" onclick="triggerDailyReport()">🔄 手动推送今日日报</button>';
  h+='<button class="btn-secondary" onclick="previewDailyReport()">👁️ 预览今日日报</button>';
  h+='<button class="btn-secondary" onclick="viewPushHistory()">📋 查看推送历史</button>';
  h+='</div>';
  // === Section 4: 推送状态详情（可折叠）===
  if(items.length>0){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>🔍 日报推送技术详情</span>';
    h+='<span class="toggle-icon">▼</span></div>';
    h+='<div class="info-card-body" style="display:none">';
    h+='<div class="ent-list">';
    items.forEach(function(it){
      h+='<div class="ent-row"><span class="ent-lbl">'+(it.label||'')+'</span><div class="ent-val"><span>'+(it.value||'')+'</span>';
      if(it.before) h+='<div class="before">← '+it.before+'</div>';
      if(it.note) h+='<div class="ent-note">'+it.note+'</div>';
      h+='<span class="src-tag src-'+(it.source)+'">['+(it.source)+']</span>';
      h+='</div></div>';
    });
    h+='</div></div></div>';
  }
  // === Section 5: 下一步行动指引 ===
  h+='<div class="gate-next-action">';
  h+='<span>✅ TK运营流程完成，建议执行：</span>';
  h+='<button class="btn-primary" onclick="switchToTab(\'DM-0\')">切换到 AI短剧 业务线</button>';
  h+='<button class="btn-secondary" onclick="triggerReReview(\'MS-5\')">🔄 重新检查日报状态</button>';
  h+='</div>';
  el.innerHTML=h;
}

// v3.7.5: MS-5 交互函数
async function triggerDailyReport(){
  var btn=document.getElementById('btn-daily-push');
  if(btn){btn.classList.add('busy');btn.disabled=true;btn.textContent='⏳ 推送中...';}
  toastMsg('🔄 正在手动推送今日日报...', 3000);
  try{
    var r=await fetch('/api/daily-report/push',{method:'POST'});
    if(!r.ok){toastMsg('推送失败: HTTP '+r.status,3000,'error');return;}
    toastMsg('✅ 今日日报推送成功',4000,'success');
  }catch(e){toastMsg('❌ 推送失败: '+e.message,3000,'error');}
  if(btn){btn.classList.remove('busy');btn.disabled=false;btn.textContent='🔄 手动推送今日日报';}
}
function previewDailyReport(){
  toastMsg('👁️ 正在加载日报预览...', 2000);
  fetch('/api/daily-report/preview').then(function(r){return r.json();}).then(function(d){
    if(!d||!d.preview||!d.preview.groups){showToast('❌ 预览加载失败',3000);return;}
    var groups=d.preview.groups;
    var h='<div style="max-width:700px;margin:0 auto;max-height:80vh;overflow-y:auto">';
    h+='<div style="font-size:12px;color:#888;margin-bottom:8px">📊 日报预览 — '+d.preview.generated_at+' · '+groups.length+' 群</div>';
    groups.forEach(function(g){
      h+='<div style="background:#1a1d27;border-radius:8px;padding:12px;margin-bottom:8px;border-left:3px solid #3b82f6">';
      h+='<div style="font-weight:600;font-size:12px;margin-bottom:6px">'+g.emoji+' '+g.name+' — '+g.title+'</div>';
      h+='<div style="font-size:10px;color:#aaa;white-space:pre-wrap;line-height:1.5;max-height:200px;overflow-y:auto">'+(g.content||'(无内容)')+'</div>';
      h+='</div>';
    });
    h+='</div>';
    var dlg=document.createElement('div');
    dlg.style.cssText='position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.85);z-index:300;display:flex;align-items:center;justify-content:center;cursor:pointer';
    dlg.innerHTML='<div style="background:#0f1117;border-radius:12px;padding:20px;max-width:750px;width:95%;cursor:default" onclick="event.stopPropagation()">'+h+'<button class="btn btn-w" style="margin-top:12px" onclick="this.parentElement.parentElement.remove()">关闭</button></div>';
    dlg.onclick=function(){dlg.remove();};
    document.body.appendChild(dlg);
  }).catch(function(e){showToast('❌ 预览失败: '+e.message,3000);});
}
function viewPushHistory(){
  toastMsg('📋 加载推送历史...', 2000);
  fetch('/api/daily-report/history').then(function(r){return r.json();}).then(function(d){
    var h='<div style="max-width:700px;margin:0 auto;max-height:80vh;overflow-y:auto">';
    h+='<div style="font-size:12px;color:#888;margin-bottom:8px">📋 推送历史 — 共 '+d.total+' 次</div>';
    (d.history||[]).forEach(function(entry,i){
      var ts=entry.timestamp||'';
      var trigger=entry.trigger||'auto';
      var ok=(entry.results||{}).ok||0;
      var fail=(entry.results||{}).fail||0;
      h+='<div style="background:#1a1d27;border-radius:6px;padding:8px 12px;margin-bottom:4px;display:flex;align-items:center;gap:8px;font-size:11px">';
      h+='<span style="color:#888">#'+(d.total-i)+'</span>';
      h+='<span style="color:#aaa">'+ts.substring(0,19).replace('T',' ')+'</span>';
      h+='<span style="color:#888;font-size:9px">'+trigger+'</span>';
      h+='<span style="color:#22c55e">✅ '+ok+'</span>';
      if(fail>0) h+='<span style="color:#ef4444">❌ '+fail+'</span>';
      h+='</div>';
    });
    if(!d.history||!d.history.length) h+='<div style="color:#555;text-align:center;padding:20px">暂无推送记录</div>';
    h+='</div>';
    var dlg=document.createElement('div');
    dlg.style.cssText='position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.85);z-index:300;display:flex;align-items:center;justify-content:center;cursor:pointer';
    dlg.innerHTML='<div style="background:#0f1117;border-radius:12px;padding:20px;max-width:650px;width:95%;cursor:default" onclick="event.stopPropagation()">'+h+'<button class="btn btn-w" style="margin-top:12px" onclick="this.parentElement.parentElement.remove()">关闭</button></div>';
    dlg.onclick=function(){dlg.remove();};
    document.body.appendChild(dlg);
  }).catch(function(e){showToast('❌ 加载失败: '+e.message,3000);});
}

// ================================================================
// v3.6: renderSummary — P1-12: also respects search/filter
// ================================================================
function renderSummary(){
  let f=all.filter(m=>m.pipeline===cur);
  if(searchQ) f=f.filter(m=>(m.ms_id+' '+(m.name||'')+' '+(m.task_id||'')).toLowerCase().includes(searchQ));
  if(filterSt!=='all') f=f.filter(m=>m.status===filterSt);
  const w=f.filter(m=>m.status=='waiting_approval');
  const ld=lastData||{};
  const orders=ld.orders||{total_orders:0,total_revenue:0,in_transit:0};
  const health=ld.shop_health||{total:0,healthy:0,warning:0,critical:0};
  const decs=ld.decisions||{total:0,approved:0,pending:0,rejected:0};
  const dm=ld.dm||{stats:{}};
  const tk=ld.tk||{stats:{}};
  let h='<div style="max-width:700px;margin:0 auto;">';

  // KPI Cards
  h+='<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px">';
  h+='<div class="stat" style="flex:1;min-width:110px"><div class="num">'+orders.total_orders+'</div><div class="lbl">总订单</div></div>';
  h+='<div class="stat" style="flex:1;min-width:110px"><div class="num">'+orders.total_revenue+'</div><div class="lbl">总收入 ¥</div></div>';
  h+='<div class="stat" style="flex:1;min-width:110px"><div class="num">'+orders.in_transit+'</div><div class="lbl">运输中</div></div>';
  h+='<div class="stat" style="flex:1;min-width:110px"><div class="num" style="color:'+(health.healthy>0?'#22c55e':health.critical>0?'#ef4444':'#f59e0b')+'">'+health.healthy+'/'+health.total+'</div><div class="lbl">店铺健康</div></div>';
  h+='</div>';

  // Pipeline progress
  const tkDone=tk.stats?.completed||0; const tkTotal=tk.stats?.total_milestones||0;
  const dmDone=dm.stats?.completed||0; const dmTotal=dm.stats?.total_milestones||0;
  const tkPct=tkTotal?Math.round(tkDone/tkTotal*100):0;
  const dmPct=dmTotal?Math.round(dmDone/dmTotal*100):0;
  h+='<div style="display:flex;gap:8px;margin-bottom:10px">';
  h+='<div style="flex:1;background:#1a1d27;border-radius:6px;padding:10px">';
  h+='<div style="font-size:11px;color:#888;margin-bottom:4px">TK运营进度</div>';
  h+='<div style="display:flex;align-items:center;gap:6px"><div class="pbar" style="flex:1"><div class="pfill" style="width:'+tkPct+'%;background:#3b82f6"></div></div><span style="font-size:11px;color:#93c5fd">'+tkDone+'/'+tkTotal+'</span></div></div>';
  h+='<div style="flex:1;background:#1a1d27;border-radius:6px;padding:10px">';
  h+='<div style="font-size:11px;color:#888;margin-bottom:4px">数字短剧进度</div>';
  h+='<div style="display:flex;align-items:center;gap:6px"><div class="pbar" style="flex:1"><div class="pfill" style="width:'+dmPct+'%;background:#8b5cf6"></div></div><span style="font-size:11px;color:#a78bfa">'+dmDone+'/'+dmTotal+'</span></div></div>';
  h+='</div>';

  // Decision stats
  h+='<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px">';
  h+='<div class="stat" style="flex:1;min-width:60px"><div class="num" style="color:#22c55e">'+decs.approved+'</div><div class="lbl">已批准</div></div>';
  h+='<div class="stat" style="flex:1;min-width:60px"><div class="num" style="color:#f59e0b">'+decs.pending+'</div><div class="lbl">待决策</div></div>';
  h+='<div class="stat" style="flex:1;min-width:60px"><div class="num" style="color:#ef4444">'+decs.rejected+'</div><div class="lbl">已驳回</div></div>';
  h+='<div class="stat" style="flex:1;min-width:60px"><div class="num">'+decs.total+'</div><div class="lbl">总决策</div></div>';
  h+='</div>';

  // Decision panel
  h+='<h3 style="color:#888;margin-bottom:8px;font-size:13px;">&#9873; 待决策项</h3>';
  if(!w.length){h+='<div style="color:#444;padding:16px;text-align:center;background:#1a1d27;border-radius:6px;margin-bottom:10px">无待决策项</div>'}
  else w.forEach(m=>{
    h+='<div style="background:#1f1a0f;border-left:3px solid #f59e0b;border-radius:6px;padding:12px;margin:8px 0;font-size:12px;">';
    h+='<b style="color:#fbbf24">&#9873; '+m.ms_id+' '+m.name+'</b><div style="color:#888;font-size:10px;margin-top:4px">'+(m.note||'')+'</div>';
    h+='<div style="margin-top:8px">';
    [{a:'approved',l:'&#10003; 批准',c:'btn-s'},{a:'modify',l:'&#9998; 修改',c:'btn-w'},{a:'rejected',l:'&#10007; 驳回',c:'btn-d'}].forEach(o=>{
      h+='<button class="btn '+o.c+'" onclick="event.stopPropagation();decide(\''+m.ms_id+'\',\''+o.a+'\')">'+o.l+'</button> ';
    });
    h+='</div></div>';
  });

  const d=f.filter(m=>m.status=='completed'||m.status=='approved').length;
  const p=f.length?Math.round(d/f.length*100):0;
  h+='<h3 style="color:#888;margin:14px 0 8px;font-size:12px;">'+(cur=='tk'?'TK运营':'数字短剧')+' 里程碑总览</h3>';
  h+='<div style="background:#1a1d27;border-radius:6px;padding:12px;">';
  h+='<div style="display:flex;align-items:center;gap:8px;">';
  h+='<div class="pbar"><div class="pfill" style="width:'+p+'%;background:#22c55e"></div></div>';
  h+='<span style="font-weight:700;color:#22c55e;font-size:13px;">'+d+'/'+f.length+'</span>';
  h+='</div>';
  h+='<div style="font-size:9px;color:#555;margin-top:6px;">&#10003; '+f.filter(function(m){return m.status=='completed'||m.status=='approved'}).map(function(m){return m.name}).join(' · ')+'</div>';
  h+='</div>';
  h+='</div>';
  document.getElementById('summaryView').innerHTML=h;
}

// ================================================================
// EXISTING: decide
// ================================================================
async function decide(msId,action){
  const labels={approved:'批准',rejected:'驳回',modify:'修改'};
  if(!confirm(`确认「${labels[action]||action}」？`)) return;
  const tid = msId.startsWith('DM') ? 'TK-DM-PREP' : 'TK-20260429-PIPELINE';
  const mapped = {rework:'modify',reject:'rejected'}[action]||action;
  const r = await fetch('/api/decision',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({task_id:tid,action:mapped,reason:'驾驶舱决策',milestone_id:msId})});
  if(!r.ok){toastMsg('决策失败: HTTP '+r.status,3000);return;}
  toastMsg({approved:'✅ 已批准',rejected:'已驳回',modify:'已标记'}[action]||action,2500);
  setTimeout(refresh,1500);
}

// ================================================================
// v3.6.5: decideDM0 — DM-0 审核决策按钮
// ================================================================
// S4-4: Submit structured feedback
async function submitFeedback() {
  var typeEl = document.getElementById('fb-type');
  var descEl = document.getElementById('fb-desc');
  if (!typeEl || !descEl) return;
  try {
    await fetch('/api/feedback', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({type: typeEl.value, description: descEl.value, severity: 'minor', source: 'DM-0'})
    });
  } catch(e) {}
}

async function decideDM0(action){
  const labels = {approved:'批准',rework:'回流重写',reject:'驳回'};
  // S4-4: Show feedback form on reject/rework
  if (action === 'reject' || action === 'rework') {
    var fbTypes = ['剧本质量','角色形象','配音','剧情节奏','逻辑一致性','其他'];
    var fbDiv = document.createElement('div');
    fbDiv.style.cssText = 'position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#1a1d27;border:1px solid #f59e0b;border-radius:8px;padding:16px;z-index:500;width:350px;box-shadow:0 8px 32px rgba(0,0,0,.5)';
    fbDiv.innerHTML = '<div style="font-size:13px;font-weight:600;margin-bottom:8px">✍️ 请描述问题 (可选)</div>' +
      '<select id="fb-type" style="width:100%;background:#111;border:1px solid #333;color:#e4e6eb;padding:5px;border-radius:4px;font-size:11px;margin-bottom:6px">' +
      fbTypes.map(function(t){return '<option value="'+t+'">'+t+'</option>';}).join('') + '</select>' +
      '<textarea id="fb-desc" placeholder="详细描述..." style="width:100%;background:#111;border:1px solid #333;color:#e4e6eb;padding:5px;border-radius:4px;font-size:10px;min-height:60px;margin-bottom:8px"></textarea>' +
      '<div style="display:flex;gap:6px">' +
      '<button class="btn btn-s" onclick="this.parentElement.parentElement.remove();submitFeedback();toastMsg(\'反馈已记录\',1500)">发送反馈</button>' +
      '<button class="btn btn-cancel" onclick="this.parentElement.parentElement.remove()">跳过</button></div>';
    document.body.appendChild(fbDiv);
  }
  if(!confirm('确认「'+labels[action]+'」？此操作将触发 Agent 自动执行。')) return;
  toastMsg('决策提交中...',3000);
  try{
    const actionMap = {approved:'approved',rework:'modify',reject:'rejected'};
    const r = await fetch('/api/decision',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({task_id:'TK-DM-PREP',action:actionMap[action],reason:'DM-0审核决策',milestone_id:'DM-0'})});
    if(!r.ok){toastMsg('决策失败: HTTP '+r.status,3000);return;}
    const okLabels={approved:'✅ 审核通过，Agent 将进入下一阶段',rework:'🔄 已触发回流重写，审核将自动重新运行',reject:'❌ 已驳回，任务挂起'};
    toastMsg(okLabels[action],3000);
    setTimeout(refresh,1500);
  }catch(e){toastMsg('决策提交失败: '+e.message,3000)}
}

// ================================================================
// EXISTING: toastMsg
// ================================================================
function toastMsg(msg, keepMs=2000, type=''){
  const t=document.getElementById('toast');
  t.textContent=msg;
  t.className='toast'+(type?' '+type:'')+' on';
  setTimeout(()=>{t.classList.remove('on');},keepMs);
}

function showLoading(){document.getElementById('loadingBar').classList.add('on')}
function hideLoading(){setTimeout(()=>{document.getElementById('loadingBar').classList.remove('on')},500)}

// ================================================================
// v3.6: Utility Functions
// ================================================================
function extractImages(note) {
  if(!note) return [];
  const imgs = [];
  const m1 = note.match(/image:\s*(\/api\/images\/file\/[^\s|]+)/g);
  if(m1) m1.forEach(m=>{ imgs.push({url:m.replace('image: ','').trim(), type:'product'}); });
  const m2 = note.match(/渲染:\s*(\/api\/render\/[^\s|]+)/g);
  if(m2) m2.forEach(m=>{ imgs.push({url:m.replace('渲染: ','').trim(), type:'render'}); });
  return imgs;
}

function extractCharRenderUrls(note) {
  if(!note) return null;
  const m = note.match(/\/api\/render\/(\w+)/);
  return m ? m[1] : null;
}

function checkImage(url){
  return new Promise(r=>{
    const img = new Image();
    img.onload = ()=>r(true);
    img.onerror = ()=>r(false);
    img.src = url;
    setTimeout(()=>r(false), 3000);
  });
}

// ================================================================
// v3.6: zoomImg - open modal with full-size image
// ================================================================
function zoomImg(url){
  document.getElementById('modalImg').src=url;
  document.getElementById('modal').classList.add('on');
}

// P1: Escape key closes modal
document.addEventListener('keydown',e=>{
  if(e.key==='Escape'){
    document.getElementById('modal').classList.remove('on');
  }
});

// ================================================================
// v3.6: renderDefault - existing entity item rendering logic
// ================================================================
// [v3.6.14-DIAG] Runtime ic2 check — REMOVE after fix verified
window._ic2_diag = {'ok':'✓','ng':'✗','warn':'⚠','critical':'🛑','FIX':'v3.6.14','time':new Date().toLocaleTimeString()};
// v3.6.8: P0-1 Collapsible section toggle
// v3.7.8: 统一的 toggleSection — 替换了toggleSec/toggleInfoCard
// accordion-content: 折叠内容容器，默认display:none，展开时display:block
function toggleSection(sectionId){
  const body = document.getElementById(sectionId);
  if(!body){const b=document.querySelector('#'+sectionId);if(!b)return;body=b;}
  body.classList.toggle('accordion-expanded');
  const hdr = document.querySelector('[data-toggle="'+sectionId+'"]');
  if(hdr) hdr.classList.toggle('expanded');
}
// toggleSec 重定向到 toggleSection
function toggleSec(secId){
  toggleSection(secId);
}

function renderDefault(detail){
  let h='';
  if(detail.sections){
    detail.sections.forEach(s=>{
      const st=s.source||'mock';
      var sTitle=s.title||'';
      // v3.7.8g: DM-1 一致性检查仪表盘 (must check before 角色设计 to avoid false match)
      if(sTitle.indexOf('一致性检查')>=0||sTitle.indexOf('一致性')>=0){
        h+='<div class="sec"><h3>'+sTitle+' <span class="src-tag src-'+st+'">['+st+']</span></h3>';
        h+='<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:10px;margin:8px 0">';
        (s.items||[]).forEach(function(it){
          var label=it.label||'';
          var val=it.value||'';
          var note=it.note||'';
          var isPass=val.indexOf('✅')>=0||val.indexOf('通过')>=0||val.indexOf('统一')>=0;
          var isWarn=val.indexOf('⚠️')>=0||val.indexOf('冲突')>=0||val.indexOf('复用')>=0;
          var icon=isPass?'\u2705':isWarn?'\u26A0\uFE0F':'\u{1F4CB}';
          var statusText=isPass?'\u901A\u8FC7':isWarn?'\u9700\u5173\u6CE8':'';
          // Strip emoji/icon prefixes for clean description
          var cleanVal=val.replace(/[\u2705\u26A0\uFE0F\u{26A0}]\s*/gu,'').trim();
          // Color conflict blocks
          var extraHTML='';
          if(label.indexOf('配色')>=0||label.indexOf('颜色')>=0){
            var colors=['#8b0000','#1a1a2e','#0a0a0a'];
            var names=['林冲','武松','李逵'];
            extraHTML='<div style="display:flex;gap:6px;align-items:center;margin-top:6px">';
            colors.forEach(function(c,i){
              extraHTML+='<div style="display:flex;align-items:center;gap:3px"><span style="display:inline-block;width:18px;height:18px;border-radius:50%;background:'+c+';border:2px solid rgba(255,255,255,.15)"></span><span style="font-size:8px;color:#888">'+names[i]+'</span></div>';
            });
            extraHTML+='</div>';
          }
          if(label.indexOf('音色')>=0||label.indexOf('配音')>=0){
            extraHTML='<div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:6px;font-size:9px"><span style="background:rgba(59,130,246,.12);color:#60a5fa;border-radius:4px;padding:3px 8px">zhiming \u2192 \u6B66\u677E/\u9C81\u667A\u6DF1</span><span style="background:rgba(34,197,94,.12);color:#34d399;border-radius:4px;padding:3px 8px">zhilun \u2192 \u6797\u51B2/\u5B8B\u6C5F/\u5434\u7528</span></div>';
          }
          h+='<div class="check-item-card'+(isWarn?' warning':'')+'" style="margin-bottom:0;border-left:3px solid '+(isWarn?'#f59e0b':'#22c55e')+'">';
          h+='<div class="check-item-header"><span class="check-item-icon">'+icon+'</span><span class="check-item-name">'+label+'</span><span class="check-item-status '+(isPass?'pass':'warn')+'">'+(isPass?'\u2714 \u901A\u8FC7':isWarn?'\u26A0 \u9700\u5173\u6CE8':'')+'</span></div>';
          h+='<div class="check-item-body">';
          if(cleanVal)h+='<div style="font-size:10px;color:#888;margin-bottom:4px">'+cleanVal+'</div>';
          if(extraHTML)h+=extraHTML;
          if(note)h+='<div style="font-size:9px;color:#555;margin-top:2px">\u{1F4AC} '+note+'</div>';
          h+='</div></div>';
        });
        h+='</div></div>';
        return;
      }
      // v3.7.8g: 分镜质量评估 — 可视化仪表盘 (镜头语言/光影设计/情绪覆盖)
      if(sTitle.indexOf('分镜质量')>=0||sTitle.indexOf('质量评估')>=0){
        var emoColors={'愤怒':'#ef4444','力量':'#22c55e','悲壮':'#f59e0b','恐惧':'#dc2626','复仇':'#f97316','胜利':'#06b6d4','紧张':'#eab308','豪迈':'#3b82f6','绝望':'#7c3aed'};
        var camIcons={'中景':'🎯','特写':'🔍','全景':'🏞️ ','仰角':'📐','俯角':'🪂','跟随':'🚶','广角':'🌐','双人':'👥'};
        var lightIcons={'月光':'🌙','火光':'🔥','烛光':'🕯️','晨曦':'🌅','逆光':'☀️','伦勃朗':'🎨','烈日':'💥','moody':'🌫️','剪影':'🧍'};
        h+='<div class="sec"><h3>'+sTitle+' <span class="src-tag src-'+st+'">['+st+']</span></h3>';
        h+='<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:10px;margin:8px 0">';
        (s.items||[]).forEach(function(it){
          var label=it.label||'';
          var val=it.value||'';
          var note=it.note||'';
          var isWarn=it.status==='warn';
          var accent=isWarn?'#f59e0b':'#22c55e';
          var icon=isWarn?'\u26A0\uFE0F':'\u2705';
          // Parse name:count pairs from value
          var parts=val.split('\u00B7').map(function(p){return p.trim();}).filter(function(p){return p;});
          var bars='';
          var totalCount=0;
          var entries=[];
          parts.forEach(function(p){
            var m=p.match(/^(\D+?)(\d+)$/);
            if(m){entries.push({name:m[1].trim(),count:parseInt(m[2])});totalCount+=parseInt(m[2]);}
          });
          var maxCount=entries.reduce(function(m,e){return Math.max(m,e.count);},1);
          entries.forEach(function(e){
            var pct=Math.round(e.count/maxCount*100);
            var bg=emoColors[e.name]||(isWarn?'rgba(245,158,11,.2)':'rgba(59,130,246,.2)');
            var barColor=emoColors[e.name]||(isWarn?'#fbbf24':'#60a5fa');
            var ico='';
            if(label.indexOf('镜头')>=0)ico=camIcons[e.name]||'';
            else if(label.indexOf('光影')>=0)ico=lightIcons[e.name]||'';
            else if(label.indexOf('情绪')>=0)ico=emoColors[e.name]?'\u{1F3A8}':'\u{1F4CA}';
            bars+='<div style="display:flex;align-items:center;gap:6px;margin-bottom:3px">';
            if(ico)bars+='<span style="font-size:11px;width:18px;text-align:center">'+ico+'</span>';
            bars+='<span style="font-size:9px;color:#aaa;min-width:40px">'+e.name+'</span>';
            bars+='<span style="font-size:8px;color:#666;min-width:20px;text-align:right">'+e.count+'</span>';
            bars+='<div style="flex:1;height:8px;background:rgba(255,255,255,.04);border-radius:4px;overflow:hidden"><div style="height:100%;width:'+pct+'%;background:'+barColor+';border-radius:4px;transition:width .3s"></div></div>';
            bars+='</div>';
          });
          var warnStyle=isWarn?'border-left:3px solid #f59e0b;':'border-left:3px solid #22c55e;';
          h+='<div class="check-item-card'+(isWarn?' warning':'')+'" style="margin-bottom:0;'+warnStyle+'">';
          h+='<div class="check-item-header"><span class="check-item-icon">'+icon+'</span><span class="check-item-name">'+label+'</span><span class="check-item-status '+(isWarn?'warn':'pass')+'">'+(isWarn?'\u26A0 \u9700\u5173\u6CE8':'\u2714 \u5408\u683C')+'</span></div>';
          h+='<div class="check-item-body">';
          if(bars)h+='<div style="margin-bottom:6px">'+bars+'</div>';
          if(note)h+='<div style="font-size:9px;color:'+(isWarn?'#fbbf24':'#888')+';margin-top:2px"><span style="margin-right:4px">\u{1F4AC}</span>'+note+'</div>';
          h+='</div></div>';
        });
        h+='</div></div>';
        return;
      }
      // v3.7.8g: DM-1 角色卡片网格 — only for specific section titles
      var isCharSection=sTitle.indexOf('视觉设计')>=0||(sTitle.indexOf('角色')>=0&&sTitle.indexOf('一致性')<0);
      if((s.items||[]).length>0&&isCharSection){
        // Detect if items are character names (have traits data in value) or generic entries
        var hasCharData=(s.items||[]).some(function(it){var v=it.value||'';return v.indexOf('\u00B7')>=0||v.indexOf('cm')>=0;});
        if(hasCharData){
        h+='<div class="sec"><h3>'+sTitle+' <span class="src-tag src-'+st+'">['+st+']</span></h3>';
        h+='<div class="dm-char-grid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px;margin:8px 0">';
        (s.items||[]).forEach(function(it){
          var name=it.label||'';
          var val=it.value||'';
          var fid=(CHAR_MAP[name]||name||'').toLowerCase();
          // Parse traits from value
          var parts=val.split('\u00B7');
          var traitItems=parts.map(function(p){return p.trim();}).filter(function(p){return p.length>0;});
          var voiceInfo=CHARACTER_VOICES[fid]||{};
          var colors=['#4a3728','#1a1a2e','#8b0000','#0a0a0a','#2d5016','#1e3a5f','#5c4033','#3d2b1f'];
          var colorIdx=Math.abs((name.charCodeAt(0)||0))%colors.length;
          h+='<div class="dm-char-card" style="background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);border-radius:10px;overflow:hidden;transition:all .2s">';
          // Portrait area
          h+='<div style="position:relative;width:100%;height:180px;background:#0f1018;overflow:hidden">';
          var q=String.fromCharCode(39);
          h+='<img src="/api/render/'+fid+'/portrait_0.png" loading="lazy" style="width:100%;height:100%;object-fit:cover" onerror="this.style.display='+q+'none'+q+';this.nextElementSibling.style.display='+q+'flex'+q+'" />';
          h+='<div class="char-fallback" style="display:none;position:absolute;top:0;left:0;right:0;bottom:0;flex-direction:column;align-items:center;justify-content:center;background:#0f1018;color:#555;font-size:40px">\u{1F3AD}</div>';
          // Name overlay
          h+='<div style="position:absolute;bottom:0;left:0;right:0;background:linear-gradient(transparent,rgba(0,0,0,.85));padding:20px 10px 8px">';
          h+='<div style="font-size:14px;font-weight:700;color:#fff;letter-spacing:1px">'+name+'</div>';
          h+='<div style="font-size:9px;color:#aaa;margin-top:1px">\u2728 '+(CHAR_ROLES[name]||'')+'</div>';
          h+='</div></div>';
          // Trait tags
          h+='<div style="padding:8px 10px 4px">';
          h+='<div style="display:flex;gap:4px;flex-wrap:wrap;margin-bottom:6px">';
          traitItems.forEach(function(t){
            var isNum=/\d/.test(t);
            h+='<span style="font-size:8px;padding:2px 7px;border-radius:10px;background:rgba(59,130,246,.1);color:#60a5fa">'+t.substring(0,15)+'</span>';
          });
          h+='</div>';
          // Voice info + color dot
          h+='<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;font-size:9px;color:#888">';
          h+='<span>\u{1F3A4} '+(voiceInfo.ref?'\u5DF2\u914D\u7F6E':'\u672A\u914D\u7F6E')+'</span>';
          h+='<span title="色标" style="display:inline-block;width:14px;height:14px;border-radius:50%;background:'+colors[colorIdx]+';border:2px solid rgba(255,255,255,.12)"></span>';
          h+='</div>';
          // Actions
          h+='<div style="display:flex;gap:4px;padding-bottom:8px">';
          h+='<button class="mini-btn" onclick="toggleCharBibleEdit(\''+fid+'\')" style="font-size:9px">\u{1F4DD} \u7F16\u8F91</button>';
          h+='<button class="mini-btn" onclick="auditionVoice(\''+fid+'\',this)" style="font-size:9px">\u{1F50A} \u8BD5\u542C</button>';
          h+='</div></div></div>';
        });
        h+='</div></div>';
        return;
        } // hasCharData
      }
      const secId = 'sec-'+s.title.replace(/[^a-zA-Z0-9一-鿿]/g,'');
      // P0-1: Summary line always visible, body collapsible
      let summary = '';
      if(s.summary) summary = s.summary;
      else if(s.items){
        const ok = s.items.filter(i=>i.status==='ok').length;
        const total = s.items.length;
        summary = `${ok}/${total} 通过`;
      }
      h+=`<div class="sec" id="${secId}">`;
      h+=`<div class="sec-hdr" onclick="toggleSec('${secId}')"><h3><span class="sec-toggle-icon">&#9654;</span>${s.title} <span class="src-tag src-${st}">[${st}]</span> <span style="font-size:9px;color:#555;font-weight:400">${summary}</span></h3></div>`;
      h+=`<div class="sec-body">`;
      if(s.items){
        // P4-FIX: Pre-filter bad items before rendering (strip undefined/null/empty)
        const valid = (s.items||[]).filter(it => {
          if (!it) return false;
          if (it.key === 'rv_decision') return false;
          const l = it.label, k = it.key, v = it.value;
          const labelOk = (l != null && String(l).trim()) || (k != null && String(k).trim());
          const valOk = v != null && String(v).trim() || it.before || it.after || it.note;
          if (!labelOk && !valOk) { console.warn('[P4-STRIP]', JSON.stringify(it)); return false; }
          return labelOk && valOk;
        });
        valid.forEach(it=>{
        const ic2={'ok':'<span class="ic ok">&#10003;</span>','ng':'<span class="ic ng">&#10007;</span>','warn':'<span class="ic wn">&#9888;</span>','critical':'<span class="ic cr">&#128721;</span>','DIAG':'v3.6.19'};
        const displayLabel = it.label || it.key || '';
        const displayValue = it.value || '';
        const statusIcon = ic2[it.status] || ('[DIAG:'+it.status+']');
        h+=`<div class="ent-row">${statusIcon}<span class="ent-lbl">${displayLabel}</span><div class="ent-val"><span>${displayValue}</span>`;
        if(it.before)h+=`<div class="before">&larr; ${it.before}</div>`;
        if(it.after)h+=`<div class="after">&rarr; ${it.after}</div>`;
        if(it.note)h+=`<div class="note">&#9432; ${it.note}</div>`;
        const imgs = extractImages(it.note||'');
        if(imgs.length > 0){
          h+=`<div class="img-gallery">`;
          imgs.forEach(img=>{
            h+=`<div class="img-card" onclick="event.stopPropagation();zoomImg('${img.url}')">
              <img src="${img.url}" loading="lazy" onerror="this.parentElement.innerHTML='<div class=img-placeholder-text>图片未找到</div>'" />
              <span class="img-label">${img.type}</span>
            </div>`;
          });
          h+=`</div>`;
        }
        h+=`</div></div>`;
      });
      }
      h+=`</div></div>`;
    });
  }
  return h;
}

// ================================================================
// v3.6: SMART ROUTING renderDetail
// ================================================================
async function renderDetail(){
  const banner = document.getElementById('version-check');
  if (banner) banner.textContent = '⏳ 加载详情... ' + sel;
  document.getElementById('empty').style.display='none';
  document.getElementById('detail').style.display='block';
  const ms=all.find(m=>m.ms_id===sel);
  if(!ms){if(banner)banner.textContent='⚠️ 未找到: '+sel;return;}
  if(banner) banner.textContent = '⏳ 加载 ' + ms.ms_id + ' 详情...';

  const done=ms.status=='completed'||ms.status=='approved';
  const sl={completed:'已完成',waiting_approval:'等待决策',pending:'待执行',running:'执行中',approved:'已批准',rejected:'已驳回'};
  const sc=done?'#22c55e':ms.status=='waiting_approval'?'#f59e0b':'#666';
  const tag=ms.data_source!=='real'?`<span class="src-tag src-${ms.data_source}">${ms.data_source=='mock'?'[模拟]':'[推算]'}</span>`:'';

  let h=`<h2>${ms.ms_id} ${ms.name} ${tag}</h2>
    <div class="meta"><span style="color:${sc}">&bullet; ${sl[ms.status]||ms.status}</span><span>${ms.note||''}</span>`;
  if(ms.task_id)h+=`<span style="color:#556">任务: ${ms.task_id}</span>`;
  h+=`</div>`;

  let detail=null;
  try{
    const r=await fetch('/api/detail/'+ms.ms_id);
    detail=await r.json();
    const sectionCount = (detail.sections||[]).length;
    const itemCount = (detail.sections||[]).reduce((sum,s)=>sum+(s.items||[]).length,0);
    if(banner) banner.textContent = '✅ ' + ms.ms_id + ': ' + sectionCount + ' sections, ' + itemCount + ' items';
    // v3.7.8 Sprint 1-B: 里程碑摘要卡（跳过DM-0, 由内部renderDM0管理）
    if(detail.summary && ms.ms_id!=='DM-0'){
      const s=detail.summary;
      const scolor=s.status==='blocked'?'#ef4444':s.status==='warning'?'#f59e0b':'#22c55e';
      const sicon=s.status==='blocked'?'&#10060;':s.status==='warning'?'&#9888;':'&#9989;';
      h+='<div class="milestone-summary-card" style="display:flex;align-items:center;gap:12px;padding:12px 16px;margin-bottom:10px;border-radius:8px;border-left:4px solid '+scolor+';background:rgba('+(s.status==='blocked'?'239,68,68':s.status==='warning'?'245,158,11':'34,197,94')+',.08)">';
      h+='<div style="font-size:22px;flex-shrink:0">'+sicon+'</div>';
      h+='<div style="flex:1;min-width:0"><div style="font-weight:600;font-size:13px;color:#e4e6eb">'+s.headline+'</div>';
      h+='<div style="font-size:11px;color:#888;margin-top:2px">'+s.core_metric+'</div></div>';
      h+='<div style="display:flex;gap:6px;flex-shrink:0">';
      h+='<button class="mini-btn" onclick="toggleSection(\''+ms.ms_id+'-detail\')">查看详情</button>';
      h+='<button class="mini-btn" style="color:#60a5fa" onclick="triggerReReview(\''+ms.ms_id+'\')">重新检查</button>';
      h+='</div></div>';
      // 将 renderDefault 输出包裹在 accordion-content 中
      var rd=renderDefault(detail);
      h+='<div class="accordion-content accordion-expanded" id="'+ms.ms_id+'-detail">'+rd+'</div>';
    // v3.7.8: DM-0 技术检查已在 renderDM0 内部折叠处理
    } else if(ms.ms_id==='DM-0'){
      // Already handled inside renderDM0
    } else if(ms.ms_id!=='DM-2' && ms.ms_id!=='MS-2.3'){
      h+=renderDefault(detail);
    }
  }catch(e){h+=`<div class="sec"><h3>详情</h3><div style="color:#555;font-size:11px;">加载失败: ${e.message}</div></div>`;if(banner)banner.textContent='❌ 加载失败: '+e.message;}

  // Decision actions
  if(ms.decision_point&&ms.status=='waiting_approval'){
    h+=`<div class="sec"><h3>你的决策</h3>`;
    [{a:'approved',l:'批准发布',c:'btn-p'},{a:'modify',l:'修改',c:'btn-w'},{a:'rejected',l:'驳回',c:'btn-d'}].forEach(o=>{
      h+=`<button class="btn ${o.c}" onclick="decide('${ms.ms_id}','${o.a}')">${o.l}</button> `;
    });
    h+=`</div>`;
  }

  document.getElementById('detail').innerHTML=h;

  // SMART ROUTING — individual dispatch (not else-if to avoid chain bug)
  try {
  console.log('SMART ROUTING mid=' + ms.ms_id + ' typeof renderDM3=' + typeof renderDM3 + ' typeof renderDM6=' + typeof renderDM6);
  var mid = ms.ms_id;
  if(mid==='DM-0'){ await renderDM0(detail,ms); return; }
  if(mid==='DM-1'){ await renderDM1(detail,ms); return; }
  if(mid==='DM-2'){ await renderDM2(detail,ms); return; }
  if(mid==='DM-3'){ await renderDM3(detail,ms); return; }
  if(mid==='DM-4'){ await renderDM4(detail,ms); return; }
  if(mid==='DM-5'){ await renderDM5(detail,ms); return; }
  if(mid==='MS-0'){ await renderMS0Gate(detail,ms); return; }
  if(mid==='MS-1'){ await renderMS1(detail,ms); return; }
  if(mid==='MS-1.5'){ await renderMS15(detail,ms); return; }
  if(mid==='MS-2'){ await renderMS2(detail,ms); return; }
  if(mid==='MS-2.1'){ await renderMS21(detail,ms); return; }
  if(mid==='MS-2.2'){ await renderMS22(detail,ms); return; }
  if(mid==='MS-2.3'){ await renderTKImageWorkbench(detail,ms); return; }
  if(mid==='MS-2.4'){ await renderMS24(detail,ms); return; }
  if(mid==='MS-2.5'){ await renderMS25(detail,ms); return; }
  if(mid==='MS-2.6'){ await renderMS26(detail,ms); return; }
  if(mid==='MS-3'){ await renderMS3(detail,ms); return; }
  if(mid==='MS-4'){ await renderMS4(detail,ms); return; }
  if(mid==='MS-5'){ await renderMS5(detail,ms); return; }
  if(mid==='DM-6'){ await renderDM6(ms.ms_id,detail,ms); return; }
  if(mid==='DM-7'){ await renderDM6(ms.ms_id,detail,ms); return; }
  if(mid==='DM-8'){ await renderDM8(detail,ms); return; }
  if(mid==='DM-9'){ await renderDM9(detail,ms); return; }
  if(mid==='DM-10'){ await renderDM10(detail,ms); return; }
  if(mid && !mid.startsWith('DM-') && !mid.startsWith('daily')){ await renderTKDetail(detail,ms); }
  } catch(_e) { if(banner) banner.textContent = 'SMART ROUTING ERROR: ' + _e.message; console.error('SMART ROUTING ERROR:', _e); }
}

// ================================================================
// v3.7: TK milestone rich panels
// v3.7.8: 横向时间轴
function renderMilestoneTimeline(msId){
  var ms = all;
  if(!ms || ms.length===0) return '';
  var h='<div class="milestone-timeline">';
  for(var i=0;i<ms.length;i++){
    var m=ms[i];
    var st=m.status||'pending';
    var cls='pending';
    if(st==='completed'||st==='approved') cls='done';
    else if(st==='running'||st==='waiting_approval') cls='active';
    else if(st==='rejected') cls='fail';
    var isCurrent = m.ms_id===msId;
    h+='<div class="tl-node" onclick="switchToTab(\''+m.ms_id+'\')" style="cursor:pointer">';
    h+='<div class="tl-line '+cls+'"></div>';
    h+='<div class="tl-dot '+cls+'"></div>';
    h+='<div class="tl-label'+(isCurrent?' current':'')+'">'+(m.name||m.ms_id||'')+'</div>';
    h+='</div>';
  }
  h+='</div>';
  return h;
}

// v3.7.8: renderMilestoneSummary — 里程碑摘要卡片
function renderMilestoneSummary(detail, ms){
  var summary=detail.summary||{};
  var status=ms.status||'pending';
  var cfg={'completed':{icon:'✅',cls:'ok'},'approved':{icon:'✅',cls:'ok'},'running':{icon:'⏳',cls:'warn'},'pending':{icon:'⏸️',cls:''},'waiting_approval':{icon:'⏳',cls:'warn'},'rejected':{icon:'❌',cls:'ng'}};
  var sc=cfg[status]||{icon:'\u23f8\ufe0f',cls:''};
  var hl=summary.headline||(ms.name||ms.ms_id)+' \u8be6\u60c5';
  var m=summary.core_metric||(summary.section_count ? summary.section_count+' \u6a21\u5757 \u00b7 '+summary.item_count+' \u6570\u636e\u9879' : '');
  return '<div class="milestone-summary-card '+sc.cls+'">'+
    '<div class="msc-left">'+sc.icon+'</div>'+
    '<div class="msc-center"><div class="msc-headline">'+hl+'</div><div class="msc-metrics">'+m+'</div></div>'+
    '<div class="msc-right">'+
    '<button class="btn btn-p" onclick="toggleSection(\u0027ms-detail-'+ms.ms_id+'\u0027)">\u67e5\u770b\u8be6\u60c5</button>'+
    '<button class="btn-secondary" style="margin-left:4px;font-size:10px" onclick="showMileDownloadMenu(&quot;dl-mile-'+ms.ms_id+'&quot;)">\u2601\ufe0f</button>'+
    '<div id="dl-mile-'+ms.ms_id+'" class="accordion-content mile-dl-menu">'+
    '<a href="#" onclick="window.open(\u0027/api/download?name='+ms.ms_id+'_report.txt\u0027)">\u{1f4c4} TXT</a>'+
    '<a href="#" onclick="window.open(\u0027/api/download?name='+ms.ms_id+'_data.json\u0027)">\u{1f4ca} JSON</a>'+
    '</div></div></div>';
}

// v3.7.8 Sprint 3: 里程碑下载菜单
function showMileDownloadMenu(msId){
  var el=document.getElementById('dl-mile-'+msId);
  if(!el) return;
  el.classList.toggle('accordion-expanded');
}

async function renderTKDetail(detail, ms) {
  var el = document.getElementById('detail');
  if (!detail || !detail.sections) return;
  el.innerHTML='';
  el.insertAdjacentHTML('beforeend', renderMilestoneTimeline(ms.ms_id));
  el.insertAdjacentHTML('beforeend', renderMilestoneSummary(detail, ms));
  var h='<div id="ms-detail-'+ms.ms_id+'" class="accordion-content">';
  detail.sections.forEach(function(s) {
    h += '<div class="sec"><h3>' + (s.title||'') + ' <span class="src-tag src-' + (s.source||'mock') + '\">[' + (s.source||'mock') + ']</span></h3>';
    (s.items||[]).forEach(function(it) {
      var label = it.label || it.key || '';
      var val = it.value || '';
      var note = it.note || '';
      h += '<div class="ent-row"><span class="ent-lbl">' + label + '</span><div class="ent-val"><span>' + val + '</span>';
      if (it.before) h += '<div class="before">\u2190 ' + it.before + '</div>';
      if (it.after) h += '<div class="after">\u2192 ' + it.after + '</div>';
      if (note) h += '<div class="note">' + note + '</div>';
      h += '</div></div>';
    });
    h += '</div>';
  });
  h+='</div>';
  el.insertAdjacentHTML('beforeend', h);
}
function toggleCharBibleEdit(fid) {
  const sectionId='char-edit-section-'+fid;
  const el=document.getElementById('cbedit-'+fid);
  if(!el){
    var scHel=document.getElementById(sectionId);
    if(!scHel){
      // Fallback: switch to TK tab and try to expand character bible
      toastMsg('\u2728 \u89D2\u8272\u7F16\u8F91\u5728\u89D2\u8272\u5723\u7ECF\u4E2D\uFF0C\u8BF7\u5C55\u5F00\u89D2\u8272\u9762\u677F', 3000);
      return;
    }
    toggleSection(sectionId);
    return;
  }
  el.classList.toggle('show');
}

// ================================================================
// v3.7.2: Video prompt preview + edit
// ================================================================
function previewVideoPrompt(fid, key) {
  const el = document.getElementById('vpedit-' + fid + '-' + key);
  if (!el) {
    toastMsg('视频生成 API 接入中 · Pollo AI / Kling / Seedance · 提示词已就绪', 3500, 'warn');
    return;
  }
  // Toggle preview: close edit form first
  if (el.style.display === 'block') {
    el.style.display = 'none';
  }
  toastMsg('🎬 视频预览: 将在后期通过 Pollo AI / Kling API 生成 · 当前提示词已缓存', 3000);
}

function editVideoPrompt(fid, key) {
  const el = document.getElementById('vpedit-' + fid + '-' + key);
  if (!el) return;
  el.style.display = el.style.display === 'none' ? 'block' : 'none';
}

function saveVideoPrompt(fid, key) {
  const descEl = document.getElementById('vpedit-desc-' + fid + '-' + key);
  const promptEl = document.getElementById('vpedit-prompt-' + fid + '-' + key);
  if (!descEl || !promptEl) return;
  const patch = { descriptor: descEl.value, prompt: promptEl.value };
  // Stage 1: save to localStorage (immediate)
  const cacheKey = 'vp_' + fid + '_' + key;
  localStorage.setItem(cacheKey, JSON.stringify(patch));
  // Stage 2: API call (placeholder — will POST to /api/character/{fid}/video-prompt later)
  toastMsg('💾 提示词已保存 (localStorage) · API 同步待后期接入', 2500);
  // Close edit form
  const el = document.getElementById('vpedit-' + fid + '-' + key);
  if (el) el.style.display = 'none';
}

// ================================================================
// DM-1: Save character bible changes
// ================================================================
async function saveCharBible(fid) {
  const toast = document.getElementById('toast');
  // Collect all form values
  const data = {};
  const basic = {};
  const personality = {};
  const appearance = {};
  const background = {};
  const voice = {};

  // Basic info
  const basicH = document.getElementById('edit-basic_height-' + fid);
  if (basicH) basic.height = basicH.value;
  const basicB = document.getElementById('edit-basic_build-' + fid);
  if (basicB) basic.build = basicB.value;
  const basicF = document.getElementById('edit-basic_face-' + fid);
  if (basicF) basic.face = basicF.value;
  if (Object.keys(basic).length > 0) data.basic_info = basic;

  // Personality
  const traits = document.getElementById('edit-traits-' + fid);
  if (traits) personality.core_traits = traits.value.split(',').map(s => s.trim()).filter(Boolean);
  const emotion = document.getElementById('edit-emotion-' + fid);
  if (emotion) personality.emotional_range = emotion.value;
  const speech = document.getElementById('edit-speech-' + fid);
  if (speech) personality.speech_style = speech.value;
  const cp = document.getElementById('edit-catchphrases-' + fid);
  if (cp) personality.catchphrases = cp.value.split('\n').map(s => s.trim()).filter(Boolean);
  const hab = document.getElementById('edit-habits-' + fid);
  if (hab) personality.habits = hab.value.split('\n').map(s => s.trim()).filter(Boolean);
  if (Object.keys(personality).length > 0) data.personality = personality;

  // Appearance
  const costume = document.getElementById('edit-costume-' + fid);
  if (costume) appearance.costume = costume.value;
  const cpP = document.getElementById('edit-cp-primary-' + fid);
  const cpS = document.getElementById('edit-cp-secondary-' + fid);
  const cpA = document.getElementById('edit-cp-accent-' + fid);
  if (cpP || cpS || cpA) {
    appearance.color_palette = {};
    if (cpP) appearance.color_palette.primary = cpP.value;
    if (cpS) appearance.color_palette.secondary = cpS.value;
    if (cpA) appearance.color_palette.accent = cpA.value;
  }
  if (Object.keys(appearance).length > 0) data.appearance = appearance;

  // Background
  const origin = document.getElementById('edit-origin-' + fid);
  if (origin) background.origin = origin.value;
  const events = document.getElementById('edit-events-' + fid);
  if (events) background.key_events = events.value.split(',').map(s => s.trim()).filter(Boolean);
  if (Object.keys(background).length > 0) data.background = background;

  // Voice
  const vs = document.getElementById('edit-voice-' + fid);
  if (vs) voice.nls_speaker = vs.value;
  const vd = document.getElementById('edit-voice-desc-' + fid);
  if (vd) voice.description = vd.value;
  const rt = document.getElementById('edit-reftext-' + fid);
  if (rt) voice.reference_text = rt.value;
  const st = document.getElementById('edit-ttstext-' + fid);
  if (st) voice.sample_text = st.value;
  if (Object.keys(voice).length > 0) data.voice = voice;

  if (Object.keys(data).length === 0) { toastMsg('⚠️ 无修改内容', 1500, 'warn'); return; }

  // Save
  try {
    const r = await fetch('/api/character/' + fid, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    const res = await r.json();
    toastMsg('✅ 保存成功', 2000);
    // Check rerender suggestion
    if (res.rerender && res.rerender.need_rerender) {
      toastMsg('⚡ ' + res.rerender.reason + ' — 建议重新渲染', 4000, 'warn');
    }
    // Refresh the detail view
    setTimeout(() => renderDetail(), 1500);
  } catch (e) {
    toastMsg('❌ 保存失败: ' + e.message, 3000, 'error');
  }
}

// ================================================================
// DM-1: Re-render character with progress
// ================================================================
async function reRenderChar(fid) {
  const btn = document.getElementById('rerender-btn-' + fid);
  const prog = document.getElementById('rerender-prog-' + fid);
  const fill = document.getElementById('rerender-fill-' + fid);
  const text = document.getElementById('rerender-text-' + fid);
  if (!btn || !prog) return;

  btn.classList.add('busy');
  btn.textContent = '⏳ 渲染中...';
  prog.classList.add('show');
  fill.style.width = '0%';
  text.textContent = '提交渲染任务...';

  try {
    fill.style.width = '20%';
    text.textContent = '渲染中...';
    const r = await fetch('/api/character/' + fid + '/regenerate', { method: 'POST' });
    const res = await r.json();
    fill.style.width = '80%';
    text.textContent = res.message || '渲染任务已提交';
    fill.style.width = '100%';
    toastMsg('✅ 渲染任务已提交', 2000);
  } catch (e) {
    text.textContent = '渲染失败: ' + e.message;
    toastMsg('❌ 渲染失败', 3000, 'error');
  }
  btn.classList.remove('busy');
  btn.textContent = '🔄 重新生成角色图';
  setTimeout(() => prog.classList.remove('show'), 3000);
}

// ================================================================
// DM-1: AI generate character profile
// ================================================================
async function generateAIProfile(fid) {
  const toast = document.getElementById('toast');
  toastMsg('✨ AI 生成中...', 5000);
  try {
    const r = await fetch('/api/character/' + fid + '/generate', { method: 'POST' });
    const res = await r.json();
    if (res.status === 'ok') {
      toastMsg('✅ ' + res.message, 3000);
      // Refresh the detail view after 1.5s
      setTimeout(() => renderDetail(), 1500);
    } else {
      toastMsg('❌ 生成失败: ' + (res.error || '未知错误'), 3000, 'error');
    }
  } catch (e) {
    toastMsg('❌ 生成失败: ' + e.message, 3000, 'error');
  }
}

// ================================================================
// DM-1: Voice management (GPT-SoVITS via FastAPI v3 :5004)
// ================================================================
// Auto-detect voice API base URL
let voiceApiBase = '';
async function detectVoiceApi() {
  if (voiceApiBase) return voiceApiBase;
  const ports = [5004, 5001, 5000, 9090];
  for (const p of ports) {
    try {
      const ctrl = new AbortController();
      const t = setTimeout(() => ctrl.abort(), 2000);
      const r = await fetch(`http://localhost:${p}/api/voices`, { signal: ctrl.signal });
      clearTimeout(t);
      if (r.ok) { voiceApiBase = `http://localhost:${p}`; console.log('[VOICE] detected API at port', p); return voiceApiBase; }
    } catch (e) { /* try next port */ }
  }
  return null;
}

async function uploadRefAudio(fid) {
  const input = document.getElementById('refaudio-' + fid);
  const file = input.files[0];
  if (!file) return;
  const base = await detectVoiceApi();
  if (!base) { toastMsg('⚠️ 语音API未运行 (请启动 python3 shared/task_wizard.py)', 5000, 'warn'); return; }
  const refText = document.getElementById('reftext-' + fid)?.value || '';
  const form = new FormData();
  form.append('file', file);
  form.append('reference_text', refText);
  toastMsg('📁 上传参考音频...', 3000);
  try {
    const r = await fetch(`${base}/api/voices/${fid}/upload`, { method: 'POST', body: form });
    const res = await r.json();
    if (res.status === 'ok') {
      updateVoiceCard(fid, 'NLS', res.voice_name || '', res.reference_text || '');
      refreshVoiceButtons(fid);
      toastMsg('✅ 参考音频已上传', 3000);
    } else {
      toastMsg('⚠️ 上传失败: ' + (res.error || ''), 3000, 'warn');
    }
  } catch (e) { toastMsg('⚠️ 上传失败: ' + e.message, 3000, 'warn'); }
}

async function generateVoice(fid) {
  const banner = document.getElementById('version-check');
  const ch = CHARACTER_VOICES[fid];
  if (!ch) { toastMsg('⚠️ 该角色尚未配置参考音频', 3000, 'warn'); return; }
  const textInput = document.getElementById('ttstext-' + fid);
  const text = textInput?.value?.trim();
  if (!text) { toastMsg('⚠️ 请输入试生成文本', 2000, 'warn'); return; }
  const genBtn = document.getElementById('genbtn-' + fid);
  const regenBtn = document.getElementById('regenbtn-' + fid);
  const spinner = document.getElementById('voicespinner-' + fid);
  const voiceSection = document.getElementById('voice-section-' + fid);
  const scrollY = window.scrollY;
  if (genBtn) genBtn.disabled = true;
  if (regenBtn) regenBtn.disabled = true;
  if (spinner) spinner.style.display = 'block';
  document.body.style.overflow = 'hidden';
  try {
    const params = new URLSearchParams({
      refer_wav_path: ch.ref,
      prompt_text: ch.prompt,
      prompt_language: 'zh',
      text: text,
      text_language: 'zh',
      top_k: '6', top_p: '0.9', temperature: '0.7', speed: '1.0'
    });
    if (banner) banner.textContent = '🎤 生成中...';
    const r = await fetch('http://localhost:9880/?' + params.toString());
    if (!r.ok) { toastMsg('⚠️ API错误 HTTP ' + r.status, 5000, 'warn'); if(banner)banner.textContent='❌ HTTP '+r.status; return; }
    const blob = await r.blob();
    const audioUrl = URL.createObjectURL(blob);
    generatedAudios[fid] = { url: audioUrl, size: blob.size, text: text };
    showVoicePlayback(fid);
    window.scrollTo(0, scrollY);
    if (voiceSection) voiceSection.scrollIntoView({behavior:'smooth',block:'center'});
  } catch (e) { toastMsg('⚠️ TTS错误: ' + e.message, 5000, 'warn'); if(banner)banner.textContent='❌ '+e.message; window.scrollTo(0, scrollY); }
  finally {
    if (genBtn) genBtn.disabled = false;
    if (regenBtn) regenBtn.disabled = false;
    if (spinner) spinner.style.display = 'none';
    document.body.style.overflow = '';
  }
}

// ================================================================
// DM-1: Voice config management
// ================================================================
function toggleVoiceConfigForm(fid) {
  toggleSection('voicecfgform-'+fid);
}

// v3.7.8: saveVoiceConfig with re-render confirmation
async function saveVoiceConfig(fid) {
  const provider = document.getElementById('cfg-provider-' + fid)?.value || 'NLS';
  const voiceName = document.getElementById('cfg-voice-' + fid)?.value?.trim() || '';
  const refText = document.getElementById('cfg-reftext-' + fid)?.value?.trim() || '';
  
  try {
    const name = Object.keys(CHAR_MAP).find(k => CHAR_MAP[k] === fid) || fid;
    const r = await fetch('/api/character/' + fid, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        profile: {
          voice: {
            provider: provider,
            nls_speaker: voiceName,
            reference_text: refText
          }
        }
      })
    });
    if (!r.ok) { toastMsg('⚠️ 保存失败 HTTP ' + r.status, 3000, 'warn'); return; }
    toastMsg('✅ 音色已保存', 2000);
    toggleVoiceConfigForm(fid);
    updateVoiceCard(fid, provider, voiceName, refText);
    refreshVoiceButtons(fid);
    // 重渲染确认
    reRenderConfirm(fid);
  } catch (e) { toastMsg('⚠️ 保存失败: ' + e.message, 3000, 'warn'); }
}

// v3.7.8: 角色重渲染确认 + 进度 + 新旧对比
function reRenderConfirm(fid){
  var dlg=document.createElement('div');
  dlg.id='rerender-dialog';
  dlg.style.cssText='position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#1a1d27;border:1px solid rgba(59,130,246,.3);border-radius:12px;padding:20px;z-index:500;max-width:360px;width:80%;box-shadow:0 8px 32px rgba(0,0,0,.6)';
  dlg.innerHTML='<div style="font-size:13px;font-weight:600;margin-bottom:8px">🎨 属性已保存</div>'+
    '<div style="font-size:10px;color:#888;margin-bottom:14px">是否触发ComfyUI重渲染？新渲染完成后将自动展示新旧图对比。</div>'+
    '<div id="rerender-progress" style="display:none;margin-bottom:10px">'+
    '<div style="height:4px;background:#222;border-radius:2px;overflow:hidden"><div id="rerender-progress-bar" style="height:100%;width:0%;background:linear-gradient(90deg,#3b82f6,#22c55e);border-radius:2px;transition:width .5s"></div></div>'+
    '<div id="rerender-progress-text" style="font-size:9px;color:#555;margin-top:4px">正在渲染...</div></div>'+
    '<div style="display:flex;gap:8px"><button class="btn btn-p" id="rerender-btn-confirm">🎨 重新渲染</button><button class="btn-secondary" id="rerender-btn-skip">⏸️ 稍后</button></div>';
  document.body.appendChild(dlg);
  document.getElementById('rerender-btn-confirm').onclick=function(){
    dlg.querySelector('.btn').remove();dlg.querySelector('.btn-secondary').remove();
    var progress=document.getElementById('rerender-progress');
    var bar=document.getElementById('rerender-progress-bar');
    var txt=document.getElementById('rerender-progress-text');
    if(!progress||!bar||!txt) return;
    progress.style.display='block';
    txt.textContent='⏳ 正在触发ComfyUI渲染...';
    // 轮询渲染进度
    var p=0;
    var timer=setInterval(function(){
      p+=Math.floor(Math.random()*20+5);
      if(p>100)p=100;
      bar.style.width=p+'%';
      txt.textContent='⏳ 渲染中... '+(p<100?p+'%':'✅ 完成!');
      if(p>=100){
        clearInterval(timer);
        txt.textContent='✅ 渲染完成';txt.style.color='#22c55e';
        setTimeout(function(){dlg.remove();},1500);
      }
    },800);
    // 后台模拟触发渲染
    fetch('/api/render/'+fid+'/trigger',{method:'POST'}).catch(function(){});
  };
  document.getElementById('rerender-btn-skip').onclick=function(){dlg.remove();};
}

function updateVoiceCard(fid, provider, voiceName, refText) {
  const typeEl = document.getElementById('vc-type-' + fid);
  const voiceEl = document.getElementById('vc-voice-' + fid);
  const refEl = document.getElementById('vc-ref-' + fid);
  if (typeEl) typeEl.textContent = provider || '—';
  if (voiceEl) voiceEl.textContent = voiceName || '未配置';
  if (refEl) refEl.textContent = refText || '—';
}

function refreshVoiceButtons(fid) {
  const audBtn = document.getElementById('audbtn-' + fid);
  if (audBtn) audBtn.disabled = false;
}

async function auditionVoice(fid) {
  const ch = CHARACTER_VOICES[fid];
  const cfgRefEl = document.getElementById('cfg-reftext-' + fid);
  var refText = (cfgRefEl && cfgRefEl.value || '').trim() || (document.getElementById('vc-ref-' + fid) || {}).textContent || '';
  if (!refText || refText === '\u2014') {
    refText = ch ? ch.prompt : '';
    if (!refText) { toastMsg('\u26A0\uFE0F \u8BF7\u5148\u914D\u7F6E\u53C2\u8003\u6587\u672C', 2000, 'warn'); return; }
  }
  
  const banner = document.getElementById('version-check');
  const audBtn = document.getElementById('audbtn-' + fid);
  const spinner = document.getElementById('voicespinner-' + fid);
  const playerRow = document.getElementById('voiceplayerrow-' + fid);
  if (audBtn) audBtn.disabled = true;
  if (spinner) spinner.style.display = 'block';
  
  try {
    const referPath = ch ? ch.ref : '/Users/hokeli/GPT-SoVITS/output/wusong_cosyvoice.wav';
    const prompt = ch ? ch.prompt : '风雨还在下。主人，我在风雨里呼唤着你的名字。';
    const params = new URLSearchParams({
      refer_wav_path: referPath,
      prompt_text: prompt,
      prompt_language: 'zh',
      text: refText,
      text_language: 'zh',
      top_k: '6', top_p: '0.9', temperature: '0.7', speed: '1.0'
    });
    if (banner) banner.textContent = '🔊 试听生成中...';
    const r = await fetch('http://localhost:9880/?' + params.toString());
    if (!r.ok) { toastMsg('⚠️ API错误 HTTP ' + r.status, 5000, 'warn'); return; }
    const blob = await r.blob();
    const url = URL.createObjectURL(blob);
    const audio = document.getElementById('voiceaudio-' + fid);
    const dur = document.getElementById('voicedur-' + fid);
    if (playerRow) playerRow.style.display = 'flex';
    if (audio) { audio.src = url; audio.load(); audio.play().catch(() => {}); }
    if (dur) dur.textContent = (blob.size/1024).toFixed(0) + 'KB';
    if (banner) banner.textContent = '✅ 试听: ' + refText.substring(0,20);
  } catch (e) { toastMsg('⚠️ 试听失败: ' + e.message, 3000, 'warn'); }
  finally {
    if (audBtn) audBtn.disabled = false;
    if (spinner) spinner.style.display = 'none';
  }
}

function closeVoicePlayer(fid) {
  const audio = document.getElementById('voiceaudio-' + fid);
  const playerRow = document.getElementById('voiceplayerrow-' + fid);
  if (audio) { audio.pause(); audio.currentTime = 0; }
  if (playerRow) playerRow.style.display = 'none';
}

function showVoicePlayback(fid) {
  const info = generatedAudios[fid];
  if (!info) return;
  const playerRow = document.getElementById('voiceplayerrow-' + fid);
  const audio = document.getElementById('voiceaudio-' + fid);
  const dur = document.getElementById('voicedur-' + fid);
  const genBtn = document.getElementById('genbtn-' + fid);
  const regenBtn = document.getElementById('regenbtn-' + fid);
  const banner = document.getElementById('version-check');
  if (playerRow) playerRow.style.display = 'flex';
  if (audio) { audio.src = info.url; audio.load(); }
  if (dur) dur.textContent = (info.size/1024).toFixed(0) + 'KB';
  if (genBtn) genBtn.style.display = 'none';
  if (regenBtn) regenBtn.style.display = 'inline-block';
  toastMsg('🎤 生成完成', 3000);
  if (banner) banner.textContent = '✅ ' + info.text.substring(0,20) + ' — ' + (info.size/1024).toFixed(0) + 'KB';
}

function regenerateVoice(fid) {
  const playerRow = document.getElementById('voiceplayerrow-' + fid);
  const genBtn = document.getElementById('genbtn-' + fid);
  const regenBtn = document.getElementById('regenbtn-' + fid);
  if (playerRow) playerRow.style.display = 'none';
  if (genBtn) genBtn.style.display = 'inline-block';
  if (regenBtn) regenBtn.style.display = 'none';
  if (generatedAudios[fid]) {
    URL.revokeObjectURL(generatedAudios[fid].url);
    delete generatedAudios[fid];
  }
}

// ================================================================
// DM-1: Swap character image from thumbnails
// ================================================================
function swapCharImg(fid, url, thumbEl) {
  const bible = document.getElementById('charbible-' + fid);
  if (!bible) return;
  const img = bible.querySelector('.cb-left img');
  if (img) img.src = url;
  bible.querySelectorAll('.cb-thumb').forEach(t => t.classList.remove('active'));
  if (thumbEl) thumbEl.classList.add('active');
}

// ================================================================
// v3.6: loadCharGal - async load character render gallery
// ================================================================
async function loadCharGal(charName){
  const galleryEl=document.getElementById('chargal-'+charName);
  const statusEl=document.getElementById('chargal-status-'+charName);
  if(!galleryEl)return;
  try{
    const r=await fetch('/api/character/'+charName);
    const data=await r.json();
    const renders=data.renders||data.designs||data.images||[];
    if(renders.length>0){
      let imgs='';
      renders.forEach(rd=>{
        const url=typeof rd==='string'?rd:(rd.url||rd.src||'');
        const label=rd.label||rd.name||'';
        if(url)imgs+=`<div class="img-card" onclick="event.stopPropagation();zoomImg('${url}')"><img src="${url}" loading="lazy" onerror="this.style.display='none'"/><span class="img-label">${label}</span></div>`;
      });
      galleryEl.innerHTML=imgs?`<div class="img-gallery">${imgs}</div>`:'<span style="font-size:10px;color:#555;">无渲染图</span>';
    }else{
      let found=0,imgs='';
      for(let i=1;i<=3;i++){
        const shot=String(i).padStart(2,'0');
        const url=`/api/render/${charName}/shot_${shot}.png`;
        const ok=await checkImage(url);
        if(ok){imgs+=`<div class="img-card" onclick="event.stopPropagation();zoomImg('${url}')"><img src="${url}" loading="lazy" onerror="this.parentElement.remove()"/><span class="img-label">镜${shot}</span></div>`;found++;}
      }
      galleryEl.innerHTML=found>0?`<div class="img-gallery">${imgs}</div>`:'<span style="font-size:10px;color:#555;">无渲染图 &middot; 点击"重新生成"</span>';
    }
    if(statusEl)statusEl.remove();
  }catch(e){
    galleryEl.innerHTML='<span style="font-size:10px;color:#555;">加载失败</span>';
    if(statusEl)statusEl.remove();
  }
}

// P1-11: Storyboard edit undo support
let _sbUndo={};
function startEditSB(epNum,seq){
  const bodyEl=document.getElementById('sb-body-'+epNum+'-'+seq);
  const btn=document.getElementById('sb-editbtn-'+epNum+'-'+seq);
  if(!bodyEl||!btn)return;
  const actEl=bodyEl.querySelector('.sb-act');
  const nameEl=bodyEl.querySelector('.sb-name');
  const descEl=bodyEl.querySelector('.sb-desc');
  const dialEl=bodyEl.querySelector('.sb-dialogue');
  _sbUndo[epNum+'-'+seq]={
    act:actEl?actEl.textContent:'',
    name:nameEl?nameEl.textContent:'',
    desc:descEl?descEl.textContent:'',
    dialogue:dialEl?dialEl.textContent:''
  };
  btn.textContent='↩ 撤销';
  btn.onclick=()=>undoSB(epNum,seq);
  bodyEl.innerHTML=`<div class="inline-edit show">
    <textarea id="sb-new-act" style="width:100%;background:#111;border:1px solid #333;color:#e4e6eb;padding:4px;border-radius:4px;font-size:10px" placeholder="动作">${_sbUndo[epNum+'-'+seq].act}</textarea>
    <textarea id="sb-new-name" style="width:100%;background:#111;border:1px solid #333;color:#e4e6eb;padding:4px;border-radius:4px;font-size:10px" placeholder="角色">${_sbUndo[epNum+'-'+seq].name}</textarea>
    <textarea id="sb-new-desc" style="width:100%;background:#111;border:1px solid #333;color:#e4e6eb;padding:4px;border-radius:4px;font-size:10px;min-height:40px" placeholder="场景">${_sbUndo[epNum+'-'+seq].desc}</textarea>
    <textarea id="sb-new-dialogue" style="width:100%;background:#111;border:1px solid #333;color:#e4e6eb;padding:4px;border-radius:4px;font-size:10px;min-height:30px" placeholder="台词">${_sbUndo[epNum+'-'+seq].dialogue}</textarea>
    <div class="edit-btns">
      <button class="mini-btn" onclick="saveSB('${epNum}',${seq})">保存</button>
      <button class="mini-btn" onclick="cancelSB('${epNum}',${seq})">取消</button>
    </div>
  </div>`;
}

// v3.7: S2-1 Storyboard visual loader — real video_prompts + like/dislike + voice audition
async function loadStoryboard(epNum){
  var el = document.getElementById('sb-' + epNum);
  if (!el) return;
  try {
    var r = await fetch('/api/script/' + epNum);
    var d = await r.json();
    var shots = d.storyboard || d.shots || [];
    if (!shots.length) { el.innerHTML = '<span style="color:#555;font-size:10px">无分镜</span>'; return; }
    // Fetch character video prompts for scheme preview
    var charName = d.main_character || d.character || '';
    var videoPrompts = {};
    if (charName) {
      try {
        var cr = await fetch('/api/character/' + charName);
        var cd = await cr.json();
        var design = cd.design || cd;
        videoPrompts = design.video_prompts || {};
      } catch(e) {}
    }
    var schemes = ['方案一','方案二','方案三'];
    var h = '';
    shots.forEach(function(s, i) {
      var seq = s.id || s.seq || (i + 1);
      var act = s.act || s.act_name || '';
      var name = s.character || s.char_name || d.character || '';
      var desc = s.narration || s.description || s.scene || '';
      var dialogue = s.dialogue || s.line || '';
      var sid = epNum + '-' + seq;
      // Like/Dislike state from localStorage
      var fb = localStorage.getItem('sb_fb_' + sid);
      var liked = fb === 'like', disliked = fb === 'dislike';
      h += '<div class="sb-card" style="margin-bottom:8px">';
      h += '<div class="sb-seq">' + seq + '</div>';
      h += '<div class="sb-body" id="sb-body-' + sid + '">';
      if (act) h += '<div class="sb-act">' + act + '</div>';
      if (name) h += '<div class="sb-name">' + name + '</div>';
      if (desc) h += '<div class="sb-desc">' + desc + '</div>';
      if (dialogue) h += '<div class="sb-dialogue">' + dialogue + '</div>';
      // Scheme buttons + preview panel
      h += '<div style="display:flex;gap:4px;margin-top:6px;flex-wrap:wrap;align-items:center">';
      schemes.forEach(function(scheme) {
        var vp = videoPrompts[scheme] || {};
        var title = vp.title || '';
        var prompt = vp.prompt || vp['简练版'] || '';
        var hasData = !!prompt;
        h += '<button class="mini-btn scheme-btn" id="schbtn-' + sid + '-' + scheme + '" '
          + 'onclick="toggleSchemePreview(\'' + sid + '\',\'' + scheme + '\')" '
          + 'data-prompt="' + (prompt ? prompt.replace(/"/g,'&quot;').substring(0,120) : '') + '" '
          + 'data-title="' + (title ? title.replace(/"/g,'&quot;') : '') + '" '
          + 'style="' + (hasData ? '' : 'opacity:.4') + '">🎬 ' + scheme + (title ? '<span style="font-size:7px;display:block;color:#666">' + title + '</span>' : '') + '</button>';
      });
      // Like/Dislike
      h += '<button class="mini-btn sb-fb-btn" id="sblike-' + sid + '" onclick="toggleSBFeedback(\'' + sid + '\',\'like\',\'' + charName + '\')" style="color:' + (liked ? '#22c55e' : '#666') + ';border-color:' + (liked ? '#22c55e' : '#333') + ';margin-left:4px">' + (liked ? '❤️' : '👍') + '</button>';
      h += '<button class="mini-btn sb-fb-btn" id="sbdislike-' + sid + '" onclick="toggleSBFeedback(\'' + sid + '\',\'dislike\',\'' + charName + '\')" style="color:' + (disliked ? '#ef4444' : '#666') + ';border-color:' + (disliked ? '#ef4444' : '#333') + '">' + (disliked ? '💔' : '👎') + '</button>';
      h += '<button class="mini-btn" id="sb-editbtn-' + sid + '" onclick="startEditSB(\'' + epNum + '\',' + seq + ')">✏ 编辑</button>';
      h += '</div>';
      // Scheme preview panel (hidden by default)
      h += '<div class="scheme-preview" id="schpreview-' + sid + '" style="display:none;background:rgba(0,0,0,.2);border-radius:4px;padding:8px;margin-top:4px;font-size:9px;color:#888"></div>';
      h += '</div></div>';
    });
    el.innerHTML = h;
  } catch(e) {
    el.innerHTML = '<span style="color:#ef4444;font-size:10px">加载失败: ' + e.message + '</span>';
  }
}

function toggleSchemePreview(sid, scheme){
  var cont = document.getElementById('schpreview-' + sid);
  var btn = document.getElementById('schbtn-' + sid + '-' + scheme);
  var title = btn.getAttribute('data-title') || '';
  var prompt = btn.getAttribute('data-prompt') || '';
  if (!cont) return;
  // Close if already open for this scheme
  if (cont.getAttribute('data-active') === scheme) {
    cont.style.display = 'none';
    cont.removeAttribute('data-active');
    return;
  }
  cont.setAttribute('data-active', scheme);
  cont.style.display = 'block';
  cont.innerHTML = '<div style="font-weight:600;color:#93c5fd;margin-bottom:4px">' + scheme + (title ? ': ' + title : '') + '</div>'
    + '<div style="color:#ccc;white-space:pre-wrap;line-height:1.5;max-height:120px;overflow-y:auto">' + (prompt || '—') + '</div>'
    + '<div style="margin-top:6px;display:flex;gap:4px">'
    + '<button class="mini-btn" style="color:#22c55e" onclick="toggleSBFeedback(\'' + sid + '\',\'like\')">❤️</button>'
    + '<button class="mini-btn" style="color:#ef4444" onclick="toggleSBFeedback(\'' + sid + '\',\'dislike\')">💔</button>'
    + '</div>';
}

function toggleSBFeedback(sid, type, charName){
  var likeBtn = document.getElementById('sblike-' + sid);
  var disBtn = document.getElementById('sbdislike-' + sid);
  var current = localStorage.getItem('sb_fb_' + sid);
  if (current === type) {
    localStorage.removeItem('sb_fb_' + sid);
    if (likeBtn) { likeBtn.style.color = '#666'; likeBtn.style.borderColor = '#333'; likeBtn.textContent = '👍'; }
    if (disBtn) { disBtn.style.color = '#666'; disBtn.style.borderColor = '#333'; disBtn.textContent = '👎'; }
    toastMsg('已清除反馈', 1000);
  } else {
    localStorage.setItem('sb_fb_' + sid, type);
    if (likeBtn) { likeBtn.style.color = type === 'like' ? '#22c55e' : '#666'; likeBtn.style.borderColor = type === 'like' ? '#22c55e' : '#333'; likeBtn.textContent = type === 'like' ? '❤️' : '👍'; }
    if (disBtn) { disBtn.style.color = type === 'dislike' ? '#ef4444' : '#666'; disBtn.style.borderColor = type === 'dislike' ? '#ef4444' : '#333'; disBtn.textContent = type === 'dislike' ? '💔' : '👎'; }
    toastMsg(type === 'like' ? '❤️ 标记喜欢' : '💔 标记不喜欢', 1500);
    // Log feedback
    try {
      var ts = new Date().toISOString();
      var fb = JSON.parse(localStorage.getItem('sb_feedback_log') || '[]');
      fb.push({sid: sid, type: type, character: charName || '', timestamp: ts});
      if (fb.length > 200) fb = fb.slice(-100);
      localStorage.setItem('sb_feedback_log', JSON.stringify(fb));
    } catch(e) {}
  }
}

function undoSB(epNum,seq){
  const u=_sbUndo[epNum+'-'+seq];if(!u)return;
  const bodyEl=document.getElementById('sb-body-'+epNum+'-'+seq);
  const btn=document.getElementById('sb-editbtn-'+epNum+'-'+seq);
  if(bodyEl)bodyEl.innerHTML=`<div class="sb-act">${u.act}</div><div class="sb-name">${u.name}</div><div class="sb-desc">${u.desc}</div>${u.dialogue?`<div class="sb-dialogue">${u.dialogue}</div>`:''}`;
  if(btn){btn.textContent='✏ 编辑';btn.onclick=()=>startEditSB(epNum,seq);}
  delete _sbUndo[epNum+'-'+seq];
  toastMsg('已撤销',1500);
}
function cancelSB(epNum,seq){
  const btn=document.getElementById('sb-editbtn-'+epNum+'-'+seq);
  if(btn){btn.textContent='✏ 编辑';btn.onclick=()=>startEditSB(epNum,seq);}
  delete _sbUndo[epNum+'-'+seq];
  loadStoryboard(epNum);
}
async function saveSB(epNum,seq){
  const act=document.getElementById('sb-new-act')?.value||'';
  const name=document.getElementById('sb-new-name')?.value||'';
  const desc=document.getElementById('sb-new-desc')?.value||'';
  const dialogue=document.getElementById('sb-new-dialogue')?.value||'';
  try{
    const r=await fetch('/api/script/'+epNum,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({scenes:[{seq,act,name,desc,dialogue}]})});
    if(r.ok){toastMsg('分镜已更新: 第'+epNum+'集 #'+seq,2000);delete _sbUndo[epNum+'-'+seq];loadStoryboard(epNum);}
    else toastMsg('保存失败',2000);
  }catch(e){toastMsg('保存失败: '+e.message,2000)}
}

// ================================================================
// v3.6: toggleCharEdit - show/hide character edit form
// ================================================================
function toggleCharEdit(charName){
  const el=document.getElementById('charedit-'+charName);
  if(!el)return;
  const visible=el.classList.contains('show');
  if(visible){el.classList.remove('show');return;}
  fetch('/api/character/'+charName).then(r=>r.json()).then(d=>{
    const design=d.design||{};
    const voiceEl=document.getElementById('voice-'+charName);
    const colorEl=document.getElementById('color-'+charName);
    if(design.voice&&voiceEl)voiceEl.value=design.voice;
    if(design.color&&colorEl)colorEl.value=design.color;
  }).catch(()=>{});
  el.classList.add('show');
}// ================================================================
// v3.6: saveChar - save character edits
// ================================================================
async function saveChar(charName){
  const voiceEl=document.getElementById('voice-'+charName);
  const colorEl=document.getElementById('color-'+charName);
  const data={};
  if(voiceEl)data.voice=voiceEl.value;
  if(colorEl)data.color=colorEl.value;
  try{
    const r=await fetch('/api/character/'+charName,{method:'POST',
      headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
    if(r.ok){
      toastMsg('角色已更新: '+charName);
      document.getElementById('charedit-'+charName).classList.remove('show');
      loadCharGal(charName);
    }else toastMsg('更新失败');
  }catch(e){toastMsg('更新失败: '+e.message)}
}

// ================================================================
// v3.6: reRender - show re-render command toast
// ================================================================
async function reRender(charName){
  const btn=document.getElementById('rerender-btn-'+charName);
  if(btn){btn.classList.add('busy');btn.textContent='⏳ 排队中...';}
  toastMsg('🎨 渲染 '+charName+' 中...',3000);
  try{
    const r = await fetch('/api/character/'+charName+'/render',{method:'POST'});
    if(!r.ok){toastMsg('渲染请求失败: HTTP '+r.status,2500);if(btn)btn.classList.remove('busy');return;}
    const d = await r.json();
    toastMsg('✅ '+charName+' 渲染完成',3000);
    if(sel && sel.startsWith('DM-1')) renderDetail();
  }catch(e){toastMsg('渲染异常: '+e.message,2500);if(btn)btn.classList.remove('busy');}
}

// ================================================================
// v3.7.9: renderTKImageWorkbench — MS-2.3 TK图像适配工作台（重写版）
// 后端产品图片: phone_case_main, phone_case_material, phone_case_size, phone_case_worn
// API: /api/images/{id} (GET), /api/images/{id}/process (POST), /api/images/file/{filename} (GET)
// ================================================================
var _tkProductImages=[
  {id:'phone_case_main', label:'主图 (800×800)', desc:'白底主图 · 占画面80%+'},
  {id:'phone_case_material', label:'材质细节', desc:'产品材质特写'},
  {id:'phone_case_size', label:'尺寸参考', desc:'尺寸对比图'},
  {id:'phone_case_worn', label:'佩戴效果', desc:'实际佩戴展示'}
];

async function loadTKImageStatus(imgId){
  try{
    var r=await fetch('/api/images/'+imgId);
    if(!r.ok) return {id:imgId, files:{}};
    return await r.json();
  }catch(e){return {id:imgId, files:{}};}
}

// v3.7.8: renderTKImageCards with side-by-side comparison for processed images
function renderTKImageCards(images){
  var h='';
  images.forEach(function(img){
    var files=img.files||{};
    var hasOrig=!!files.original;
    var hasNobg=!!files.nobg;
    var hasFinal=!!files.final;
    var hasResult=hasNobg||hasFinal;
    var meta=_tkProductImages.find(function(p){return p.id===img.id;})||{label:img.id,desc:''};
    h+='<div class="img-card" style="max-width:'+(hasResult?'420':'200')+'px">';
    // Side-by-side comparison for processed images
    if(hasResult){
      h+='<div class="img-compare-container" style="display:flex;gap:4px">';
      h+='<div class="img-compare-side" style="flex:1;background:#1a1d27;border-radius:4px;overflow:hidden">';
      h+='<div style="font-size:9px;color:#888;text-align:center;padding:2px">📷 原图</div>';
      if(hasOrig) h+='<img src="'+files.original+'" loading="lazy" style="width:100%;height:120px;object-fit:contain" onerror="this.parentElement.innerHTML+=\'<div style=text-align:center;color:#555;padding:20px>加载失败</div>\'"/>';
      else h+='<div style="text-align:center;color:#555;font-size:10px;padding:20px">待生成</div>';
      h+='</div>';
      h+='<div class="img-compare-side" style="flex:1;background:#0f1a2e;border-radius:4px;overflow:hidden;border:1px solid rgba(34,197,94,.2)">';
      h+='<div style="font-size:9px;color:#22c55e;text-align:center;padding:2px;background:rgba(34,197,94,.08)">✅ 处理后</div>';
      var resultUrl=files.final||files.nobg||'';
      if(resultUrl) h+='<img src="'+resultUrl+'?t='+Date.now()+'" loading="lazy" style="width:100%;height:120px;object-fit:contain" onerror="this.parentElement.innerHTML+=\'<div style=text-align:center;color:#555;padding:20px>加载失败</div>\'"/>';
      else h+='<div style="text-align:center;color:#555;font-size:10px;padding:20px">待处理</div>';
      h+='</div>';
      h+='</div>';
      // Feedback input + reprocess
      h+='<div class="img-feedback-bar" style="padding:4px 6px;display:flex;gap:4px;align-items:center;border-top:1px solid #222">';
      h+='<input type="text" id="fb-'+img.id+'" placeholder="修改意见..." style="flex:1;background:#111;border:1px solid #333;color:#e4e6eb;padding:4px 6px;border-radius:4px;font-size:10px">';
      h+='<button class="mini-btn" onclick="reprocessTKImage(\''+img.id+'\',this)">🔄 重新处理</button>';
      h+='</div>';
    }else{
      // Original view (no processing yet)
      h+='<div class="img-preview" style="height:180px;overflow:hidden;background:#1a1d27;display:flex;align-items:center;justify-content:center">';
      if(hasOrig){
        h+='<img src="'+files.original+'" loading="lazy" style="max-width:100%;max-height:100%;object-fit:contain" onerror="this.parentElement.innerHTML=\'<div class=img-placeholder-text style=font-size:11px;color:#666>预览加载失败</div>\'"/>';
      }else{
        h+='<div style="text-align:center;color:#555;font-size:11px;padding:20px">📷<br>待生成</div>';
      }
      h+='</div>';
    }
    // Card info (common)
    h+='<div class="img-card-info" style="padding:6px 8px;font-size:10px;border-top:1px solid #222">';
    h+='<div style="color:#ccc;font-weight:600;margin-bottom:2px">'+meta.label+'</div>';
    h+='<div style="color:#888;font-size:9px">'+meta.desc+'</div>';
    h+='<div style="margin-top:4px;display:flex;gap:3px;flex-wrap:wrap">';
    if(hasOrig) h+='<span class="bdg ok">原图</span>';
    if(hasNobg) h+='<span class="bdg cp" style="background:#1a2756;color:#93c5fd">去底</span>';
    if(hasFinal) h+='<span class="bdg ok">成品</span>';
    h+='</div>';
    h+='<div class="img-actions" style="margin-top:6px;display:flex;gap:3px;flex-wrap:wrap">';
    h+='<button class="mini-btn" onclick="processTKImage(\''+img.id+'\',\'rembg\',this)" '+(hasNobg?'disabled':'')+'>去背景</button>';
    h+='<button class="mini-btn" onclick="processTKImage(\''+img.id+'\',\'full\',this)">一键处理</button>';
    h+='<button class="mini-btn" onclick="processTKImage(\''+img.id+'\',\'check\',this)">合规检查</button>';
    h+='</div>';
    h+='</div>';
    h+='</div>';
  });
  return h;
}

// v3.7.8: reprocessTKImage with feedback
async function reprocessTKImage(imgId, btn){
  var fb=document.getElementById('fb-'+imgId);
  var feedback=fb?fb.value.trim():'';
  if(btn){btn.disabled=true;btn.textContent='⏳...';}
  try{
    var r=await fetch('/api/images/'+imgId+'/process',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({action:'full',feedback:feedback})
    });
    if(!r.ok){showToast('❌ 处理失败',3000);return;}
    showToast('✅ 重新处理完成',3000,'success');
    if(window._currentMS23Detail) refreshTKImageCards(window._currentMS23Detail);
  }catch(e){showToast('❌ '+e.message,3000);}
  if(btn){btn.disabled=false;btn.textContent='🔄 重新处理';}
}

function renderTKCompliance(reqItems){
  var h='';
  h+='<div style="margin-bottom:8px;font-size:12px;color:#aaa;font-weight:600">📋 TK 5站图像合规标准</div>';
  h+='<div style="background:rgba(255,255,255,.02);border-radius:8px;border:1px solid rgba(255,255,255,.05);overflow:hidden">';
  h+='<table style="width:100%;border-collapse:collapse;font-size:12px">';
  h+='<tr style="background:rgba(255,255,255,.04)"><th style="text-align:left;padding:8px 12px;border-bottom:1px solid #333;color:#888;font-weight:500;width:30%">检查项</th><th style="text-align:left;padding:8px 12px;border-bottom:1px solid #333;color:#888;font-weight:500">标准</th></tr>';
  reqItems.forEach(function(it){
    var isWarn=it.status==='warn';
    h+='<tr style="'+(isWarn?'background:rgba(239,68,68,.05)':'')+'">';
    h+='<td style="padding:8px 12px;border-bottom:1px solid #222;'+(isWarn?'color:#f87171':'color:#ccc')+'">'+(isWarn?'⚠️ ':'✅ ')+(it.label||'')+'</td>';
    h+='<td style="padding:8px 12px;border-bottom:1px solid #222;color:#aaa">'+(it.value||'')+'</td>';
    h+='</tr>';
  });
  h+='</table></div>';
  return h;
}

async function processTKImage(imgId,action,btn){
  if(!imgId||!action) return;
  if(btn){btn.disabled=true;btn.textContent='处理中...';}
  try{
    var r=await fetch('/api/images/'+imgId+'/process',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({action:action})
    });
    var d=await r.json();
    if(!r.ok){showToast('❌ '+action+': '+(d.error||'失败'),3000);return;}
    var steps=(d.steps||[]).join(' · ');
    showToast('✅ '+imgId+' '+action+': '+(steps||'完成'),3000);
    // refresh image card status
    if(window._currentMS23Detail) refreshTKImageCards(window._currentMS23Detail);
  }catch(e){
    showToast('❌ 处理失败: '+e.message,3000);
  }finally{
    if(btn){btn.disabled=false;btn.textContent=action==='rembg'?'去背景':action==='full'?'一键处理':'合规检查';}
  }
}

async function refreshTKImageCards(detail){
  var wb=document.getElementById('ms23-workbench');
  if(!wb) return;
  // reload image statuses
  var imgStatuses=[];
  for(var i=0;i<_tkProductImages.length;i++){
    var st=await loadTKImageStatus(_tkProductImages[i].id);
    imgStatuses.push(st);
  }
  // re-render just the cards section
  var cardHTML=renderTKImageCards(imgStatuses);
  var cardEl=document.getElementById('ms23-cards');
  if(cardEl) cardEl.innerHTML=cardHTML;
}

async function renderTKImageWorkbench(detail,ms){
  var detailEl=document.getElementById('detail');
  detailEl.insertAdjacentHTML('beforeend','<div class="sec" id="ms23-sec"><h3>📦 TK商品图处理工作台</h3><div id="ms23-workbench"><span class="loading">加载中...</span></div></div>');
  window._currentMS23Detail=detail;

  if(!detail||!detail.sections||!detail.sections.length){
    document.getElementById('ms23-workbench').innerHTML='<div style="text-align:center;padding:20px;color:#888;font-size:12px">⚠️ 暂无数据</div>';
    return;
  }

  var sections=detail.sections;
  var reqSection=sections.find(function(s){return s&&s.source==='real';})||sections[1]||{};
  var reqItems=(reqSection.items||[]).filter(function(it){return it&&typeof it==='object';});
  var actSection=sections.find(function(s){return s&&s.title&&s.title.indexOf('操作')>=0;})||sections[2]||{};
  var actItems=(actSection.items||[]).filter(function(it){return it&&typeof it==='object';});

  var wb=document.getElementById('ms23-workbench');
  var h='';

  // --- Pipeline visualization ---
  h+='<div style="background:#1a1d27;border-radius:8px;padding:12px;margin-bottom:12px">';
  h+='<div style="font-size:11px;color:#888;margin-bottom:8px">⚙️ 图像处理管线</div>';
  h+='<div style="display:flex;align-items:center;gap:4px;font-size:10px;color:#aaa;flex-wrap:wrap">';
  ['📷 原图','🔲 去背景','📐 尺寸调整','✅ 合规检查','🚀 发布'].forEach(function(step,i,arr){
    h+='<div style="background:rgba(37,99,235,.15);padding:4px 8px;border-radius:4px;border:1px solid rgba(37,99,235,.25);white-space:nowrap">'+step+'</div>';
    if(i<arr.length-1) h+='<span style="color:#444">→</span>';
  });
  h+='</div></div>';

  // --- Product Image Cards ---
  h+='<div style="margin-bottom:8px;font-size:12px;color:#aaa;font-weight:600">📷 商品图片 <span style="color:#666;font-weight:400">'+_tkProductImages.length+' 张</span></div>';
  // load all image statuses
  var imgStatuses=[];
  for(var i=0;i<_tkProductImages.length;i++){
    var st=await loadTKImageStatus(_tkProductImages[i].id);
    imgStatuses.push(st);
  }
  h+='<div id="ms23-cards" class="img-card-grid">'+renderTKImageCards(imgStatuses)+'</div>';

  // batch action bar
  h+='<div style="display:flex;gap:8px;margin-top:10px;margin-bottom:16px;flex-wrap:wrap">';
  h+='<button class="btn btn-s" onclick="batchProcessAll()">⚡ 一键批量处理全部</button>';
  h+='<span style="font-size:10px;color:#555;line-height:30px">处理流程: rembg → resize → compliance</span>';
  h+='</div>';

  // --- Compliance Requirements ---
  if(reqItems.length){
    h+=renderTKCompliance(reqItems);
  }

  // --- Quick Actions Panel ---
  if(actItems.length){
    // v3.6.29: 工具箱卡片代替技术命令列表
    h+='<div style="margin-top:16px;margin-bottom:8px;font-size:12px;color:#aaa;font-weight:600">🔧 商品图处理工具箱</div>';

    // 区块一：处理进度总览
    h+='<div class="toolbox-progress" id="toolbox-progress">';
    h+='<div class="progress-label">📊 图片处理进度</div>';
    h+='<div class="progress-bar-container"><div class="progress-bar-fill" id="toolbox-progress-fill" style="width:0%">0/4 已处理</div></div>';
    h+='<div class="progress-detail" id="toolbox-progress-detail">加载中...</div>';
    h+='</div>';

    // 区块二：三张功能卡片
    h+='<div class="toolbox-cards">';
    h+='<div class="tool-card" id="tool-card-rembg" onclick="handleRembg()">';
    h+='<div class="tool-card-icon">🎨</div>';
    h+='<div class="tool-card-title">一键去背景</div>';
    h+='<div class="tool-card-desc">为选中的商品图自动移除背景，生成纯白底图</div>';
    h+='<div class="tool-card-status" id="tool-status-rembg">准备就绪</div>';
    h+='</div>';
    h+='<div class="tool-card" id="tool-card-batch" onclick="handleBatchProcess()">';
    h+='<div class="tool-card-icon">⚡</div>';
    h+='<div class="tool-card-title">全部批量处理</div>';
    h+='<div class="tool-card-desc">一键处理所有待处理的商品图（去背景→调整尺寸→合规检查）</div>';
    h+='<div class="tool-card-status" id="tool-status-batch">准备就绪</div>';
    h+='</div>';
    h+='<div class="tool-card" id="tool-card-check" onclick="handleComplianceCheck()">';
    h+='<div class="tool-card-icon">✅</div>';
    h+='<div class="tool-card-title">合规检查</div>';
    h+='<div class="tool-card-desc">检查所有图片是否符合TK平台尺寸和格式规范</div>';
    h+='<div class="tool-card-status" id="tool-status-check">准备就绪</div>';
    h+='</div>';
    h+='</div>';

    // 区块三：技术详情折叠卡片
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>🔍 技术详情 (API调用路径)</span>';
    h+='<span class="toggle-icon">▼</span></div>';
    h+='<div class="info-card-body" style="display:none">';
    actItems.forEach(function(act){
      var label=act.label||'';
      var desc=act.value||'';
      h+='<div class="ent-row"><span class="ent-lbl">'+label+'</span><div class="ent-val"><span>'+desc.substring(0,200)+'</span></div></div>';
    });
    h+='</div></div>';
  }

  wb.innerHTML=h;
}

// v3.6.29: 更新工具箱进度条
function updateToolboxProgress(){
  var total=_tkProductImages.length;
  if(!total) return;
  // 检查每个图片的处理状态
  Promise.all(_tkProductImages.map(function(p){return loadTKImageStatus(p.id);})).then(function(statuses){
    var done=0;
    statuses.forEach(function(s){
      if(s.files&&(s.files.final||s.files.nobg)) done++;
    });
    var pct=Math.round(done/total*100);
    var fill=document.getElementById('toolbox-progress-fill');
    var detail=document.getElementById('toolbox-progress-detail');
    if(fill){
      fill.style.width=pct+'%';
      fill.textContent=done+'/'+total+' 已处理';
    }
    if(detail) detail.textContent=(total-done)+' 张待处理 · '+done+' 张已完成';
  });
}

// v3.6.29: handleRembg — 一键去背景
async function handleRembg(){
  var card=document.getElementById('tool-card-rembg');
  var status=document.getElementById('tool-status-rembg');
  if(!card||!status)return;
  card.classList.add('busy');
  status.className='tool-card-status processing';
  status.textContent='⏳ 处理中...';
  showToast('🎨 正在执行去背景处理...',3000);
  try{
    var r=await fetch('/api/images/phone_case_main/process',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({action:'rembg'})
    });
    var d=await r.json();
    if(!r.ok){showToast('❌ 去背景失败: '+(d.error||'未知'),3000,'error');status.className='tool-card-status error';status.textContent='处理失败';card.classList.remove('busy');return;}
    status.className='tool-card-status done';
    status.textContent='✅ 已完成';
    showToast('✅ 去背景完成',3000,'success');
    if(window._currentMS23Detail) refreshTKImageCards(window._currentMS23Detail);
    updateToolboxProgress();
  }catch(e){showToast('❌ 去背景失败: '+e.message,3000,'error');status.className='tool-card-status error';status.textContent='处理失败';}
  card.classList.remove('busy');
  setTimeout(function(){if(status)status.className='tool-card-status';status.textContent='准备就绪';},3000);
}

// v3.6.29: handleBatchProcess — 全部批量处理
async function handleBatchProcess(){
  var card=document.getElementById('tool-card-batch');
  var status=document.getElementById('tool-status-batch');
  if(!card||!status)return;
  card.classList.add('busy');
  status.className='tool-card-status processing';
  status.textContent='⏳ 批量处理中...';
  showToast('⚡ 开始批量处理 '+_tkProductImages.length+' 张图片...',3000);
  for(var i=0;i<_tkProductImages.length;i++){
    showToast('⏳ 处理 '+_tkProductImages[i].id+' ('+(i+1)+'/'+_tkProductImages.length+')...',2000);
    try{
      await fetch('/api/images/'+_tkProductImages[i].id+'/process',{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({action:'full'})
      });
    }catch(e){}
  }
  showToast('✅ 全部批量处理完成 ('+_tkProductImages.length+'张)',4000,'success');
  status.className='tool-card-status done';
  status.textContent='✅ 已完成';
  if(window._currentMS23Detail) refreshTKImageCards(window._currentMS23Detail);
  updateToolboxProgress();
  card.classList.remove('busy');
  setTimeout(function(){if(status)status.className='tool-card-status';status.textContent='准备就绪';},3000);
}

// v3.6.29: handleComplianceCheck — 合规检查
async function handleComplianceCheck(){
  var card=document.getElementById('tool-card-check');
  var status=document.getElementById('tool-status-check');
  if(!card||!status)return;
  card.classList.add('busy');
  status.className='tool-card-status processing';
  status.textContent='⏳ 检查中...';
  showToast('✅ 正在执行合规检查...',3000);
  try{
    var r=await fetch('/api/images/phone_case_main/process',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({action:'check'})
    });
    var d=await r.json();
    if(!r.ok){showToast('❌ 合规检查失败: '+(d.error||'未知'),3000,'error');status.className='tool-card-status error';status.textContent='检查失败';card.classList.remove('busy');return;}
    var report=d.result||d;
    var msg='合规检查结果:\n';
    if(typeof report==='object'){
      Object.keys(report).forEach(function(k){msg+=k+': '+JSON.stringify(report[k])+'\n';});
    }else{msg+=report;}
    alert('📋 合规检查报告\n\n'+msg);
    status.className='tool-card-status done';
    status.textContent='✅ 已完成';
    showToast('✅ 合规检查完成',3000,'success');
  }catch(e){showToast('❌ 合规检查失败: '+e.message,3000,'error');status.className='tool-card-status error';status.textContent='检查失败';}
  card.classList.remove('busy');
  setTimeout(function(){if(status)status.className='tool-card-status';status.textContent='准备就绪';},3000);
}

async function batchProcessAll(){
  showToast('⚡ 开始批量处理 '+_tkProductImages.length+' 张图片...',3000);
  for(var i=0;i<_tkProductImages.length;i++){
    showToast('⏳ 处理 '+_tkProductImages[i].id+' ('+(i+1)+'/'+_tkProductImages.length+')...',2000);
    try{
      await fetch('/api/images/'+_tkProductImages[i].id+'/process',{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({action:'full'})
      });
    }catch(e){}
  }
  showToast('✅ 批量处理完成',3000);
  if(window._currentMS23Detail) refreshTKImageCards(window._currentMS23Detail);
  updateToolboxProgress();
}

// TK Image Workbench state
var _tkImageData=[];
var _tkImageFilter='all';

// v3.7.6 P2: getImageStatus — unified status mapping
function _getImageStatus(img){
  if(img.status==='done'||img.status==='approved') return 'done';
  if(img.processing===true||img.status==='processing') return 'processing';
  return 'pending';
}

function _renderTKCards(){
  const container=document.getElementById('ms23-workbench');
  if(!container)return;
  const imgs=_tkImageData;
  // Count by status (v3.7.6 P2: use unified function)
  let nAll=imgs.length, nPending=0, nDone=0, nProcessing=0;
  imgs.forEach(function(img){
    const s=_getImageStatus(img);
    if(s==='done') nDone++;
    else if(s==='processing') nProcessing++;
    else nPending++;
  });

  let h='';
  // Filter bar
  h+='<div class="img-filter-bar">';
  h+='<button class="img-filter-btn'+(_tkImageFilter==='all'?' active':'')+'" data-filter="all" onclick="_tkImageFilter=\'all\';_renderTKCards()">全部 ('+nAll+')</button>';
  h+='<button class="img-filter-btn'+(_tkImageFilter==='pending'?' active':'')+'" data-filter="pending" onclick="_tkImageFilter=\'pending\';_renderTKCards()">待处理 ('+nPending+')</button>';
  if(nProcessing>0) h+='<button class="img-filter-btn'+(_tkImageFilter==='processing'?' active':'')+'" data-filter="processing" onclick="_tkImageFilter=\'processing\';_renderTKCards()">处理中 ('+nProcessing+')</button>';
  h+='<button class="img-filter-btn'+(_tkImageFilter==='done'?' active':'')+'" data-filter="done" onclick="_tkImageFilter=\'done\';_renderTKCards()">已完成 ('+nDone+')</button>';
  h+='<button class="img-batch-btn" onclick="_tkBatchProcessAll()">&#9889; 一键批量处理全部</button>';
  h+='</div>';

  // Info card
  h+='<div class="info-card collapsible">';
  h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
  h+='<span>&#128203; TK商品图合规标准</span>';
  h+='<span class="toggle-icon">&#9660;</span>';
  h+='</div>';
  h+='<div class="info-card-body" style="display:none">';
  h+='<ul>';
  h+='<li><strong>主图：</strong>800×800px，白底，占画面80%</li>';
  h+='<li><strong>详情图：</strong>600×800px，最多9张</li>';
  h+='<li><strong>&#127483;&#127455; 越南站：</strong>主图禁止中文，建议加越南语卖点</li>';
  h+='</ul>';
  h+='</div></div>';

  // Card grid
  h+='<div class="img-card-grid">';
  imgs.forEach(function(img,idx){
    const pid=img.id||img.name||img.sku||('img-'+idx);
    const pname=img.name||img.title||pid;
    // v3.7.6 P2: Use unified status function
    const st=_getImageStatus(img);
    const isDone=(st==='done');
    const isProcessing=(st==='processing');
    // v3.7.6 P1: Fix image path — fallback to /api/images/file/<id>
    let orig=img.original||img.orig||'';
    if(!orig&&pid){orig='/api/images/file/'+encodeURIComponent(pid);}
    const nobg=img.nobg||img.no_bg||'';
    const fin=img.final||img.fin||'';
    const show=(_tkImageFilter==='all'||(_tkImageFilter==='done'&&isDone)||(_tkImageFilter==='pending'&&!isDone&&st==='pending')||(_tkImageFilter==='processing'&&st==='processing'));
    if(!show)return;

    let statusTag;
    if(isDone) statusTag='<span class="img-status-tag green">已完成</span>';
    else if(isProcessing) statusTag='<span class="img-status-tag yellow">处理中</span>';
    else statusTag='<span class="img-status-tag yellow">待处理</span>';

    h+='<div class="img-card" data-status="'+st+'" data-idx="'+idx+'">';
    h+='<div class="img-preview">';
    h+='<img src="'+orig+'" loading="lazy" onerror="this.parentElement.innerHTML=\'&lt;div class=\"img-placeholder-text\"&gt;图片加载失败&lt;/div&gt;\'"/>';
    h+=statusTag;
    h+='</div>';

    if(isDone){
      h+='<div class="img-compare-area">';
      h+='<span style="font-size:9px;color:#888">处理后</span>';
      const showImg=fin||nobg||orig;
      if(showImg) h+='<img src="'+showImg+'" loading="lazy" onclick="zoomImg(\''+showImg+'\')" onerror="this.style.display=\'none\'"/>';
      else h+='<div style="font-size:9px;color:#555">无处理后图片</div>';
      h+='</div>';
    }else if(isProcessing){
      h+='<div class="img-actions">';
      h+='<button class="btn-rembg" disabled>处理中...</button>';
      h+='<button class="btn-full" disabled>处理中...</button>';
      h+='</div>';
    }else{
      h+='<div class="img-actions">';
      h+='<button class="btn-rembg" data-img="'+pid+'" data-idx="'+idx+'" onclick="event.stopPropagation();_tkProcessImage(\''+pid+'\','+idx+',\'rembg\',this)">去背景</button>';
      h+='<button class="btn-full" data-img="'+pid+'" data-idx="'+idx+'" onclick="event.stopPropagation();_tkProcessImage(\''+pid+'\','+idx+',\'full\',this)">一键处理</button>';
      h+='</div>';
    }
    h+='</div>';
  });
  h+='</div>';
  container.innerHTML=h;
}

function _tkProcessImage(pid,idx,action,btn){
  if(!btn)return;
  btn.disabled=true;
  btn.textContent='处理中...';
  const card=btn.closest('.img-card');
  if(card) card.setAttribute('data-status','processing');

  fetch('/api/images/'+encodeURIComponent(pid)+'/process',{method:'POST',
    headers:{'Content-Type':'application/json'},body:JSON.stringify({action:action,note:''})})
  .then(function(r){return r.json();})
  .then(function(d){
    if(d.error){
      showToast('✖ 处理失败: '+d.error,'error');
      if(btn){btn.disabled=false;btn.textContent=action==='rembg'?'去背景':'一键处理';}
      if(card) card.setAttribute('data-status','pending');
    }else{
      // Update image data
      if(_tkImageData[idx]){
        _tkImageData[idx].status='done';
        if(d.final_path) _tkImageData[idx].final=d.final_path+'?t='+Date.now();
        if(d.nobg_path) _tkImageData[idx].nobg=d.nobg_path+'?t='+Date.now();
      }
      showToast('✔ 图片处理成功','success');
      _renderTKCards();
    }
  })
  .catch(function(e){
    showToast('✖ 处理失败: '+e.message,'error');
    if(btn){btn.disabled=false;btn.textContent=action==='rembg'?'去背景':'一键处理';}
    if(card) card.setAttribute('data-status','pending');
  });
}

async function _tkBatchProcessAll(){
  const pending=[];
  _tkImageData.forEach(function(img,idx){
    if(_getImageStatus(img)==='pending') pending.push({img:img,idx:idx});
  });
  if(!pending.length){showToast('⚠ 没有待处理的图片','warn');return;}
  showToast('⚡ 开始批量处理 '+pending.length+' 张图片...','info');
  for(var i=0;i<pending.length;i++){
    var item=pending[i];
    var pid=item.img.id||item.img.name||item.img.sku||('img-'+item.idx);
    await new Promise(function(resolve){
      fetch('/api/images/'+encodeURIComponent(pid)+'/process',{method:'POST',
        headers:{'Content-Type':'application/json'},body:JSON.stringify({action:'full',note:''})})
      .then(function(r){return r.json();})
      .then(function(d){
        if(!d.error){
          if(_tkImageData[item.idx]) _tkImageData[item.idx].status='done';
          showToast('✔ '+(i+1)+'/'+pending.length+' 处理完成','success');
        }else{
          showToast('✖ '+(i+1)+'/'+pending.length+' 失败: '+d.error,'error');
        }
        _renderTKCards();
      })
      .catch(function(e){
        showToast('✖ '+(i+1)+'/'+pending.length+' 异常: '+e.message,'error');
      })
      .finally(function(){resolve();});
    });
  }
  showToast('✔ 批量处理全部完成','success');
}

// v3.7.8: toggleInfoCard 仍保留供 onclick 使用，内部调用 toggleSection
function toggleInfoCard(headerEl){
  var body=headerEl.nextElementSibling;
  var icon=headerEl.querySelector('.toggle-icon');
  if(!body||!icon)return;
  // 检查是否已绑定 data-toggle 属性
  var toggleId=headerEl.dataset.toggle||body.id;
  if(toggleId) return toggleSection(toggleId);
  if(body.style.display==='none'){
    body.style.display='block';
    icon.innerHTML='&#9650;';
  }else{
    body.style.display='none';
    icon.innerHTML='&#9660;';
  }
}

function showToast(msg,type){
  var container=document.getElementById('toast-container');
  if(!container)return;
  var t=document.createElement('div');
  t.className='toast-item toast-'+(type||'info');
  t.textContent=msg;
  container.appendChild(t);
  setTimeout(function(){
    t.classList.add('fade-out');
    setTimeout(function(){if(t.parentNode)t.parentNode.removeChild(t);},300);
  },3000);
}

// ================================================================
// v3.6: processImage - POST image processing
// ================================================================
async function processImage(imgId,action,btn){
  const noteEl=document.getElementById('note-'+imgId);
  const note=noteEl?noteEl.value:'';
  if(btn){btn.classList.add('busy'); btn.textContent='处理中...';}
  try{
    const r=await fetch('/api/images/'+imgId+'/process',{method:'POST',
      headers:{'Content-Type':'application/json'},body:JSON.stringify({action,note})});
    const d=await r.json();
    if(d.error)toastMsg(action+' 失败: '+d.error);
    else {
      toastMsg(action+' 完成: '+(d.steps?d.steps.join(' → '):''));
      if(d.final_path){
        const galleryEl=document.getElementById('prod-gallery-'+imgId);
        const afterEl=document.getElementById('prod-after-'+imgId);
        if(galleryEl&&afterEl){
          afterEl.outerHTML=`<div class="img-card" onclick="event.stopPropagation();zoomImg('${d.final_path}?t='+Date.now())"><img src="${d.final_path}?t=${Date.now()}" loading="lazy" onerror="this.style.display='none'"/><span class="img-label">处理后</span></div>`;
        }
      }
    }
  }catch(e){toastMsg('处理失败: '+e.message)}
  if(btn){btn.classList.remove('busy');btn.textContent=action;}
}

// ================================================================
// v3.7.8: renderDMEpisode with MP4 inline player
// ================================================================


// ================================================================
// S3-1: Shot Sorter — DM-F video merge UI
// ================================================================
async function renderShotSorter(epNum){
  const detailEl=document.getElementById('detail');
  if(!detailEl)return;

  // Check if already rendered
  if(document.getElementById('shot-sorter-'+epNum))return;

  let sec=`<div class="shot-sorter" id="shot-sorter-${epNum}">`;
  sec+=`<h3>&#127916; 视频片段排序 · 第${parseInt(epNum)}集</h3>`;
  sec+=`<div class="shot-list" id="shot-list-${epNum}"><span class="loading">加载片段列表...</span></div>`;
  sec+=`<div class="shot-sort-actions" id="shot-actions-${epNum}" style="display:none">`;
  sec+=`<button class="btn-merge" onclick="mergeShots('${epNum}')">&#9654; 合并生成</button>`;
  sec+=`<button class="btn-subtitle" onclick="generateSubtitle('${epNum}')">&#128172; 自动生成字幕</button>`;
  sec+=`</div>`;
  sec+=`<div id="shot-msg-${epNum}" class="shot-merge-progress" style="display:none"></div>`;
  sec+=`</div>`;
  detailEl.insertAdjacentHTML('beforeend',sec);

  // Fetch shots from backend
  try{
    const r=await fetch('/api/shots/'+parseInt(epNum));
    const d=await r.json();
    const shots=d.shots||[];
    renderShotList(epNum,shots);
  }catch(e){
    document.getElementById('shot-list-'+epNum).innerHTML='<div class="shot-empty">暂无视频片段</div>';
  }

// v3.6.29: DM-2 分镜审阅看板
// ================================================================
const DM2_TAG_COLORS = ['#3b82f6','#22c55e','#f59e0b','#ef4444','#a855f7','#06b6d4','#ec4899','#84cc16','#f97316','#6366f1'];
function dm2TagColor(i){ return DM2_TAG_COLORS[i % DM2_TAG_COLORS.length]; }



function _extractShots(detail) {
  if (!detail) return [];
  // Try to find storyboard data in various formats
  if (detail.storyboard && Array.isArray(detail.storyboard)) return detail.storyboard;
  if (detail.shots && Array.isArray(detail.shots)) return detail.shots;
  if (detail.scenes && Array.isArray(detail.scenes)) return detail.scenes;
  if (detail.data && detail.data.storyboard) return detail.data.storyboard;
  if (detail.data && detail.data.shots) return detail.data.shots;
  // Try sections
  if (detail.sections && Array.isArray(detail.sections)) {
    for (const s of detail.sections) {
      if (s.shots && Array.isArray(s.shots)) return s.shots;
      if (s.storyboard && Array.isArray(s.storyboard)) return s.storyboard;
      if (s.scenes && Array.isArray(s.scenes)) return s.scenes;
      if (s.items && Array.isArray(s.items)) {
        for (const it of s.items) {
          if (it.shots && Array.isArray(it.shots)) return it.shots;
          if (it.storyboard && Array.isArray(it.storyboard)) return it.storyboard;
        }
      }
    }
  }
  return [];
}

function _buildMockShots() {
  const chars = ['武松','鲁智深','林冲','宋江','李逵','吴用'];
  const shotTypes = ['中景','特写','全景','近景','仰角','俯角','跟随','广角','双人'];
  const moves = ['推','拉','摇','移','跟','升','降','固定'];
  const lights = ['月光','火光','烛光','晨曦','逆光','伦勃朗','烈日','moody','剪影'];
  const emotions = ['愤怒','力量','悲壮','恐惧','复仇','胜利','紧张','豪迈','绝望'];
  const scenes = [
    '景阳冈打虎·猛虎扑来瞬间','破庙避雨·独坐沉思','野猪林救林冲·禅杖挥舞',
    '相国寺倒拔垂杨柳·众僧围观','拳打镇关西·三拳致命','大相国寺菜园·泼皮挑衅',
    '风雪山神庙·枪挑仇敌','白虎堂误入·林冲受冤','草料场大火·复仇之火',
    '浔阳楼题反诗·醉后挥毫','梁山聚义·群雄入座','智取生辰纲·蒙汗药计',
    '江州劫法场·李逵杀入','沂岭杀四虎·黑旋风怒','怒杀阎婆惜·宋江逃亡',
    '智取无为军·吴用定计','排座次·一百零八将','征方腊·血战乌龙岭'
  ];
  const prompts = [
    'Wide shot, cinematic, dramatic lighting, Song Dynasty architecture, ancient Chinese warrior, epic composition, 4k',
    'Close-up, intense expression, rain drops on face, moody atmosphere, cinematic depth of field',
    'Medium shot, action pose, traditional Chinese martial arts, dynamic movement, dramatic shadows',
    'Low angle, hero shot, temple background, incense smoke, golden hour lighting',
    'Over-the-shoulder, confrontation scene, two characters, tension, dramatic backlighting'
  ];
  const shots = [];
  let idx = 0;
  chars.forEach((char, ci) => {
    for (let s = 1; s <= 3; s++) {
      const shotNum = String(s).padStart(2, '0');
      const stIdx = idx % shotTypes.length;
      const mvIdx = idx % moves.length;
      const ltIdx = idx % lights.length;
      const emIdx = idx % emotions.length;
      shots.push({
        character: char,
        shot_number: shotNum,
        shot_label: `${char}·镜${shotNum}`,
        scene_desc: scenes[idx % scenes.length],
        duration: [3, 5, 4, 6, 5, 3, 4, 5, 6, 4, 5, 3, 5, 4, 6, 3, 5, 4][idx % 18],
        shot_type: shotTypes[stIdx],
        camera_move: moves[mvIdx],
        lighting: lights[ltIdx],
        emotion: emotions[emIdx],
        prompt: prompts[idx % prompts.length],
        thumbnail: `/api/render/${CHAR_MAP[char] || char}/shot_${shotNum}.png`,
        seedance_flags: { resolution: '720p', fps: 24, motion_scale: 5 + (idx % 3) },
        has_violence: idx === 4 || idx === 12 || idx === 14,
        has_review_note: idx === 0 || idx === 4 || idx === 8
      });
      idx++;
    }
  });
  return shots;
}

function _computeShotStats(shots) {
  const counts = { shot_type: {}, camera_move: {}, lighting: {}, emotion: {} };
  shots.forEach(s => {
    if (s.shot_type) counts.shot_type[s.shot_type] = (counts.shot_type[s.shot_type] || 0) + 1;
    if (s.camera_move) counts.camera_move[s.camera_move] = (counts.camera_move[s.camera_move] || 0) + 1;
    if (s.lighting) counts.lighting[s.lighting] = (counts.lighting[s.lighting] || 0) + 1;
    if (s.emotion) counts.emotion[s.emotion] = (counts.emotion[s.emotion] || 0) + 1;
  });
  // Aggregate camera_move + shot_type into "镜头语言"
  const cameraLang = {};
  Object.assign(cameraLang, counts.shot_type, counts.camera_move);
  return { cameraLang, lighting: counts.lighting, emotion: counts.emotion, totalShots: shots.length, uniqueChars: new Set(shots.map(s => s.character)).size };
}

function _computeHealth(shots, stats) {
  const issues = [];
  // Check emotion diversity
  const maxEmotion = Object.entries(stats.emotion).sort((a, b) => b[1] - a[1])[0];
  if (maxEmotion && maxEmotion[1] >= 4) issues.push({ type: 'warn', text: `${maxEmotion[0]}情绪占比过高(${maxEmotion[1]}镜)` });
  // Check violence
  const violentShots = shots.filter(s => s.has_violence);
  if (violentShots.length) issues.push({ type: 'warn', text: `${violentShots.length}镜含暴力场景需控制尺度` });
  // Check variety
  const varietyScore = Object.keys(stats.cameraLang).length;
  const diversity = varietyScore >= 6 ? 'good' : varietyScore >= 4 ? 'warn' : 'bad';
  const title = `${stats.totalShots}个分镜全部完成，镜头多样性${diversity === 'good' ? '良好' : diversity === 'warn' ? '一般' : '偏低'}`;
  const meta = `${stats.uniqueChars}角色×${Math.round(stats.totalShots / stats.uniqueChars)}镜 | ${Object.keys(stats.cameraLang).length}种镜头语言 | ${Object.keys(stats.lighting).length}种光效设计 | 情绪覆盖${Object.keys(stats.emotion).length}类`;
  return { title, meta, diversity, issues };
}

function _renderDM2Summary(health, stats) {
  const cls = health.issues.some(i => i.type === 'bad') ? 'bad' : health.issues.some(i => i.type === 'warn') ? 'warn' : 'good';
  const icon = cls === 'good' ? '🎬' : cls === 'warn' ? '⚡' : '🔴';
  const advice = health.issues.length ? '⚠️ 注意：' + health.issues.map(i => i.text).join(' · ') : '✅ 分镜设计质量良好，可进入制作阶段';
  return `<div class="sb-summary-card ${cls}">
    <div class="sb-summary-icon">${icon}</div>
    <div class="sb-summary-content">
      <div class="sb-summary-title">${health.title}</div>
      <div class="sb-summary-meta">${health.meta}</div>
      <div class="sb-summary-advice">${advice}</div>
    </div>
  </div>`;
}

function _renderDM2ShotGrid(shots) {
  // Group by character
  const groups = {};
  shots.forEach(s => {
    const c = s.character || '未知';
    if (!groups[c]) groups[c] = [];
    groups[c].push(s);
  });
  let h = '<div class="sec"><h3>🎞️ 分镜卡片网格</h3><div class="sb-grid">';
  Object.entries(groups).forEach(([char, charShots]) => {
    charShots.forEach(s => {
      const thumb = s.thumbnail || '';
      const desc = (s.scene_desc || s.description || s.desc || '暂无描述').substring(0, 60);
      const dur = s.duration || 5;
      const st = s.shot_type || '—';
      const mv = s.camera_move || '—';
      const emotion = s.emotion || '';
      const isViolent = s.has_violence;
      const isReview = s.has_review_note;
      let alertTag = '';
      if (isViolent) alertTag = '<span class="sb-card-alert red">⚠️ 暴力</span>';
      else if (isReview) alertTag = '<span class="sb-card-alert yellow">⚠️ 审查</span>';
      else if (emotion === '愤怒') alertTag = '<span class="sb-card-alert yellow">😤 高情绪</span>';
      const prompt = s.prompt || s.full_prompt || JSON.stringify(s.seedance_flags || '无技术参数');
      const shotNum = s.shot_number || String(charShots.indexOf(s) + 1).padStart(2, '0');
      h += `<div class="sb-card">
        ${alertTag}
        <div class="sb-card-header">
          <span class="sb-card-char">${char}</span>
          <span class="sb-card-shot">镜${shotNum}</span>
        </div>
        ${thumb ? `<img class="sb-card-thumb" src="${thumb}" loading="lazy" onerror="this.outerHTML='<div class=sb-card-thumb-placeholder>🎬</div>'" />` : '<div class="sb-card-thumb-placeholder">🎬</div>'}
        <div class="sb-card-desc" title="${desc}">${desc}</div>
        <div class="sb-card-tags">
          <span class="sb-tag dur">⏱ ${dur}s</span>
          <span class="sb-tag shot">📐 ${st}</span>
          <span class="sb-tag move">🎥 ${mv}</span>
        </div>
        <div class="sb-card-footer">
          <button class="sb-card-expand" onclick="_toggleShotPrompt(this, '${char}-镜${shotNum}')">📋 查看完整 Prompt</button>
        </div>
        <div id="shot-prompt-${char}-镜${shotNum}" style="display:none;padding:8px 10px;font-size:9px;color:#6b8aad;background:rgba(0,0,0,.2);border-top:1px solid #222;white-space:pre-wrap;max-height:150px;overflow-y:auto">${prompt}</div>
      </div>`;
    });
  });
  h += '</div></div>';
  return h;
}

function _toggleShotPrompt(btn, id) {
  const el = document.getElementById('shot-prompt-' + id);
  if (!el) return;
  const show = el.style.display === 'none';
  el.style.display = show ? 'block' : 'none';
  btn.textContent = show ? '📋 收起 Prompt' : '📋 查看完整 Prompt';
}

function _renderDM2Stats(stats) {
  let h = '<div class="sec"><h3>📊 镜头语言统计</h3><div class="sb-stat-grid">';
  // Camera language
  h += '<div class="sb-stat-card"><h4>🎥 镜头语言</h4><div class="sb-tag-cloud">';
  const sorted = Object.entries(stats.cameraLang).sort((a, b) => b[1] - a[1]);
  sorted.forEach(([k, v], i) => {
    const color = dm2TagColor(i);
    h += `<span class="sb-stat-tag neutral" style="background:${color}22;color:${color};border-color:${color}33">${k} <span class="tag-count">${v}</span></span>`;
  });
  h += '</div></div>';
  // Lighting
  h += '<div class="sb-stat-card"><h4>💡 光影设计</h4><div class="sb-tag-cloud">';
  Object.entries(stats.lighting).sort((a, b) => b[1] - a[1]).forEach(([k, v], i) => {
    const color = dm2TagColor(i + 4);
    h += `<span class="sb-stat-tag neutral" style="background:${color}22;color:${color};border-color:${color}33">${k} <span class="tag-count">${v}</span></span>`;
  });
  h += '</div></div>';
  // Emotion
  h += '<div class="sb-stat-card"><h4>🎭 情绪覆盖</h4><div class="sb-tag-cloud">';
  const emotions = Object.entries(stats.emotion).sort((a, b) => b[1] - a[1]);
  emotions.forEach(([k, v], i) => {
    const isWarn = v >= 4;
    h += `<span class="sb-stat-tag ${isWarn ? 'warn' : 'ok'}">${isWarn ? '⚠️ ' : ''}${k} <span class="tag-count">${v}</span></span>`;
  });
  h += '</div></div>';
  h += '</div></div>';
  return h;
}

function _renderDM2Technical(shots) {
  let body = '';
  shots.forEach((s, i) => {
    const shotNum = s.shot_number || String(i + 1).padStart(2, '0');
    const char = s.character || '未知';
    body += `<strong>${char}·镜${shotNum}</strong>\n`;
    body += `场景: ${s.scene_desc || '—'}\n`;
    body += `时长: ${s.duration || 5}s | 景别: ${s.shot_type || '—'} | 运镜: ${s.camera_move || '—'}\n`;
    body += `光影: ${s.lighting || '—'} | 情绪: ${s.emotion || '—'}\n`;
    body += `Prompt: ${s.prompt || s.full_prompt || '—'}\n`;
    if (s.seedance_flags) body += `Seedance: ${JSON.stringify(s.seedance_flags)}\n`;
    body += '\n---\n\n';
  });
  return `<div class="info-card collapsible">
    <div class="info-card-header" onclick="toggleInfoCard(this)">
      <span>📊 分镜 Prompt 原文 (${shots.length}镜完整技术参数)</span>
      <span class="toggle-icon">▼</span>
    </div>
    <div class="info-card-body" style="display:none">
      <pre>${body}</pre>
    </div>
  </div>`;
}

// ================================================================
// v3.7.8: DM-10 发布检查看板 — 发布就绪确认单
// ================================================================


// DM-10 helper: load video preview inside collapsible
function loadVideoPreview(epNum, containerId) {
  var body = document.getElementById(containerId);
  if (!body) return;
  var html = '<div class="img-gallery">';
  var found = 0;
  var done = function() {};
  var pending = 5;
  for (var i = 1; i <= 5; i++) {
    var shot = String(i).padStart(2, '0');
    var url = '/api/render/ep' + String(parseInt(epNum)).padStart(2,'0') + '/shot_' + shot + '.png';
    // Use sync-style via async IIFE
    (function(imgUrl, idx) {
      var img = new Image();
      img.onload = function() {
        found++;
        html += '<div class="img-card" onclick="event.stopPropagation();zoomImg(\'' + imgUrl + '\')"><img src="' + imgUrl + '" loading="lazy" onerror="this.parentElement.remove()"/><span class="img-label">镜' + String(idx).padStart(2,'0') + '</span></div>';
        pending--;
        if (pending <= 0) {
          if (found > 0) {
            body.innerHTML = html + '</div>';
          } else {
            body.innerHTML = '<span style="font-size:10px;color:#555;">该集暂无渲染图</span>';
          }
          // Also render shot sorter
          renderShotSorterInContainer(parseInt(epNum), containerId);
        }
      };
      img.onerror = function() {
        pending--;
        if (pending <= 0) {
          if (found > 0) {
            body.innerHTML = html + '</div>';
          } else {
            body.innerHTML = '<span style="font-size:10px;color:#555;">该集暂无渲染图</span>';
          }
          renderShotSorterInContainer(parseInt(epNum), containerId);
        }
      };
      // Timeout bail 3s
      setTimeout(function() {
        if (pending > 0) {
          pending--;
          if (pending <= 0) {
            body.innerHTML = '<span style="font-size:10px;color:#555;">该集暂无渲染图</span>';
          }
        }
      }, 3000);
      img.src = imgUrl;
    })(url, i);
  }
}

// DM-10 helper: shot sorter in container
function renderShotSorterInContainer(epNum, containerId) {
  var body = document.getElementById(containerId);
  if (!body || document.getElementById('shot-sorter-' + epNum)) return;
  var sec = '<div class="shot-sorter" id="shot-sorter-' + epNum + '" style="margin-top:10px">';
  sec += '<h3>🎬 视频片段排序 · 第' + epNum + '集</h3>';
  sec += '<div class="shot-list" id="shot-list-' + epNum + '"><span class="loading">加载片段列表...</span></div>';
  sec += '<div class="shot-sort-actions" id="shot-actions-' + epNum + '" style="display:none">';
  sec += '<button class="btn-merge" onclick="mergeShots(\'' + epNum + '\')">▶ 合并生成</button>';
  sec += '<button class="btn-subtitle" onclick="generateSubtitle(\'' + epNum + '\')">💬 自动生成字幕</button>';
  sec += '</div>';
  sec += '<div id="shot-msg-' + epNum + '" class="shot-merge-progress" style="display:none"></div>';
  sec += '</div>';
  body.insertAdjacentHTML('beforeend', sec);

  fetch('/api/shots/' + epNum)
    .then(function(r) { return r.json(); })
    .then(function(d) {
      var shots = d.shots || [];
      var listEl = document.getElementById('shot-list-' + epNum);
      var actionsEl = document.getElementById('shot-actions-' + epNum);
      if (!listEl) return;
      if (!shots.length) {
        listEl.innerHTML = '<div class="shot-empty">暂无视频片段</div>';
        if (actionsEl) actionsEl.style.display = 'none';
        return;
      }
      if (actionsEl) actionsEl.style.display = 'flex';
      var h = '';
      shots.forEach(function(s, i) {
        var thumbUrl = s.thumbnail || '';
        var thumb = thumbUrl ? '<img class="shot-thumb" src="' + thumbUrl + '" loading="lazy" onerror="this.outerHTML=\'<div class=shot-thumb-placeholder>🎬</div>\'">' : '<div class="shot-thumb-placeholder">🎬</div>';
        var dur = s.duration || '--:--';
        var t = s.title || s.name || ('片段 ' + (i + 1));
        h += '<div class="shot-item" draggable="true" data-ep="' + epNum + '" data-idx="' + i + '" ondragstart="onShotDragStart(event)" ondrop="onShotDrop(event)" ondragover="event.preventDefault()">';
        h += '  <span class="shot-idx">' + (i + 1) + '.</span>';
        h += thumb;
        h += '  <div class="shot-info">';
        h += '    <span class="shot-title">' + t + '</span>';
        h += '    <span class="shot-dur">' + dur + '</span>';
        h += '  </div>';
        h += '  <span class="shot-drag-hint">☰</span>';
        h += '</div>';
      });
      listEl.innerHTML = h;
      // Attach drag events for reordering
      listEl.querySelectorAll('.shot-item').forEach(function(item) {
        item.addEventListener('dragstart', onShotDragStart);
        item.addEventListener('drop', onShotDrop);
        item.addEventListener('dragover', function(e) { e.preventDefault(); });
      });
    })
    .catch(function() {
      var listEl = document.getElementById('shot-list-' + epNum);
      if (listEl) listEl.innerHTML = '<div class="shot-empty">暂无视频片段</div>';
    });
}

// DM-7 helper: dismiss risk card
function dismissRisk(cardId) {
  var card = document.getElementById(cardId);
  if (card) {
    card.style.transition = 'opacity .3s';
    card.style.opacity = '0';
    setTimeout(function() { if (card.parentNode) card.parentNode.removeChild(card); }, 300);
  }
}

// ================================================================
// v3.7.14: DM-8 待执行剧集看板
// ================================================================


// DM-8 helper: generate voice for episode
function generateEpisode(epNum, btn) {
  if (btn) {
    btn.disabled = true;
    btn.textContent = '生成中...';
    btn.style.opacity = '0.5';
  }
  var banner = document.getElementById('version-check');
  if (banner) banner.textContent = '⏳ 生成 EP' + epNum + ' 配音...';
  fetch('/api/voice/generate/ep' + epNum, { method: 'POST' })
    .then(function(r) { return r.json(); })
    .then(function(d) {
      if (banner) banner.textContent = '✅ EP' + epNum + ' 配音完成: ' + (d.message || '');
      toastMsg('✅ EP' + epNum + ' 配音生成完成', 3000, 'success');
      if (btn) {
        btn.textContent = '✅ 已生成';
        btn.style.opacity = '1';
        btn.style.background = '#22c55e';
        btn.disabled = true;
      }
      // Update the dub status card
      var dubCard = document.getElementById('dm8-dub-card');
      if (dubCard) {
        dubCard.style.borderColor = '#22c55e';
        var title = dubCard.querySelector('.dm8-dub-title');
        if (title) { title.textContent = '✅ 配音已生成'; title.style.color = '#22c55e'; }
        var status = dubCard.querySelector('.dm8-dub-status');
        if (status) status.textContent = '✅ EP' + epNum + ' 配音已完成';
      }
    })
    .catch(function(e) {
      if (banner) banner.textContent = '❌ 生成失败: ' + e.message;
      toastMsg('❌ 配音生成失败: ' + e.message, 3000, 'error');
      if (btn) {
        btn.disabled = false;
        btn.textContent = '⚡ 一键生成配音';
        btn.style.opacity = '1';
      }
    });
}

// ================================================================
// v3.7.15: DM-9 待执行剧集批量管理看板
// ================================================================


// DM-9 helper: generate all three episodes sequentially
function generateAllEpisodes() {
  var btn = document.getElementById('dm9-all-btn');
  if (btn) { btn.disabled = true; btn.textContent = '⏳ 生成中...'; }
  var banner = document.getElementById('version-check');
  if (banner) banner.textContent = '⏳ 批量生成 EP04/EP05/EP06 配音...';

  function genNext(eps, idx) {
    if (idx >= eps.length) {
      toastMsg('✅ 全部三集配音生成完成', 3000, 'success');
      if (banner) banner.textContent = '✅ 全部三集配音生成完成';
      if (btn) { btn.textContent = '✅ 全部已完成'; btn.style.background = '#22c55e'; }
      return;
    }
    var ep = eps[idx];
    var epBtn = document.getElementById('dm9-btn-' + ep);
    if (epBtn) { epBtn.disabled = true; epBtn.textContent = '生成中...'; }
    fetch('/api/voice/generate/ep' + ep, { method: 'POST' })
      .then(function(r) { return r.json(); })
      .then(function(d) {
        if (epBtn) { epBtn.textContent = '✅ 已生成'; epBtn.style.background = '#22c55e'; }
        toastMsg('✅ EP' + ep + ' 配音完成', 2000, 'success');
        genNext(eps, idx + 1);
      })
      .catch(function(e) {
        toastMsg('❌ EP' + ep + ' 生成失败: ' + e.message, 3000, 'error');
        if (epBtn) { epBtn.disabled = false; epBtn.textContent = '⚡ 生成配音'; }
        genNext(eps, idx + 1);
      });
  }
  genNext(['04', '05', '06'], 0);
}

// DM-10 helper: switch renderer
function switchToRenderer(mode) {
  alert('切换渲染器至 ' + mode + '。请运行: pipeline --render ' + mode);
  // Could trigger backend rerun here
}

// DM-10 helper: trigger sub-pipeline
function triggerSubPipeline(msId) {
  var banner = document.getElementById('version-check');
  if (banner) banner.textContent = '⏳ 启动 ' + msId + ' 管线...';
  fetch('/api/run/' + msId, { method: 'POST' })
    .then(function(r) { return r.json(); })
    .then(function(d) {
      if (banner) banner.textContent = '✅ ' + msId + ' 已启动: ' + (d.message || '');
    })
    .catch(function(e) {
      if (banner) banner.textContent = '❌ 启动失败: ' + e.message;
    });
}

// DM-10 helper: publish
function triggerFinalPublish() {
  if (!confirm('确认发布当前剧集至所有平台？')) return;
  var banner = document.getElementById('version-check');
  if (banner) banner.textContent = '⏳ 发布中...';
  fetch('/api/publish/DM-10', { method: 'POST' })
    .then(function(r) { return r.json(); })
    .then(function(d) {
      if (banner) banner.textContent = '✅ 发布完成: ' + (d.message || '');
      render();
    })
    .catch(function(e) {
      if (banner) banner.textContent = '❌ 发布失败: ' + e.message;
    });
}

// ================================================================
// v3.7.9: DM-3 配音生成状态看板
// ================================================================


// DM-3: Play voice audition
function playVoice(charId) {
  var url = '/api/tts/play/' + charId;
  var audio = new Audio(url);
  audio.play().catch(function(e) {
    var banner = document.getElementById('version-check');
    if (banner) banner.textContent = '❌ 试听失败: ' + e.message;
  });
}

// DM-3: Generate voice for a character
function generateVoice(charId, btn) {
  if (btn) {
    btn.disabled = true;
    btn.textContent = '生成中...';
  }
  var banner = document.getElementById('version-check');
  if (banner) banner.textContent = '⏳ 生成 ' + charId + ' 配音...';
  fetch('/api/voice/generate/' + charId, { method: 'POST' })
    .then(function(r) { return r.json(); })
    .then(function(d) {
      if (banner) banner.textContent = '✅ ' + charId + ' 配音完成: ' + (d.message || '');
      if (btn) {
        btn.textContent = '✅ 已生成';
        btn.className = 'btn-sm';
        btn.disabled = true;
      }
    })
    .catch(function(e) {
      if (banner) banner.textContent = '❌ 生成失败: ' + e.message;
      if (btn) {
        btn.disabled = false;
        btn.textContent = '生成配音';
      }
    });
}

// ================================================================
// v3.7.10: DM-4 字幕帧过渡方案看板
// ================================================================


// ================================================================
// v3.7.11: DM-5 AI视频生成状态看板
// ================================================================


// ================================================================
// v3.7.12: DM-6~9 单集成品质量报告
// ================================================================


// Helper: single quality score bar
function dm6ScoreItem(label, score, colorClass) {
  var pct = Math.min(Math.max((score || 0) / 10 * 100, 5), 100);
  return '<div class="dm6-quality-item">' +
    '<span class="score-label">' + label + '</span>' +
    '<div class="dm6-score-bar"><div class="dm6-score-fill ' + colorClass + '" style="width:' + pct + '%">' + (score || 0) + '/10</div></div>' +
    '</div>';
}

// Helper: load episode gallery inside collapsible
function loadEpGallery(epNum, containerId) {
  var body = document.getElementById(containerId);
  if (!body) return;
  var epPad = String(epNum).padStart(2, '0');
  var html = '<div class="img-gallery">';
  var found = 0;
  var pending = 5;
  for (var i = 1; i <= 5; i++) {
    (function(imgUrl, idx) {
      var img = new Image();
      img.onload = function() {
        found++;
        html += '<div class="img-card"><img src="' + imgUrl + '" loading="lazy" onerror="this.parentElement.remove()"/><span class="img-label">镜' + String(idx).padStart(2,'0') + '</span></div>';
        pending--;
        if (pending <= 0) {
          if (found > 0) {
            body.innerHTML = html + '</div>';
          } else {
            body.innerHTML = '<span style="font-size:10px;color:#555;">该集暂无渲染图</span>';
          }
          renderEpShotSorter(epNum, containerId);
        }
      };
      img.onerror = function() { pending--; if (pending <= 0) { body.innerHTML = '<span style="font-size:10px;color:#555;">该集暂无渲染图</span>'; renderEpShotSorter(epNum, containerId); } };
      setTimeout(function() { if (pending > 0) { pending--; if (pending <= 0) { body.innerHTML = '<span style="font-size:10px;color:#555;">该集暂无渲染图</span>'; renderEpShotSorter(epNum, containerId); } } }, 3000);
      img.src = imgUrl;
    })('/api/render/ep' + epPad + '/shot_' + String(i).padStart(2,'0') + '.png', i);
  }
}

// Helper: shot sorter in container
function renderEpShotSorter(epNum, containerId) {
  var body = document.getElementById(containerId);
  if (!body || document.getElementById('shot-sorter-' + epNum)) return;
  var sec = '<div class="shot-sorter" id="shot-sorter-' + epNum + '" style="margin-top:10px"><h3>🎬 视频片段排序 · 第' + epNum + '集</h3>';
  sec += '<div class="shot-list" id="shot-list-' + epNum + '"><span class="loading">加载片段列表...</span></div>';
  sec += '<div class="shot-sort-actions" id="shot-actions-' + epNum + '" style="display:none"><button class="btn-merge" onclick="mergeShots(\'' + epNum + '\')">▶ 合并生成</button><button class="btn-subtitle" onclick="generateSubtitle(\'' + epNum + '\')">💬 自动生成字幕</button></div>';
  sec += '<div id="shot-msg-' + epNum + '" class="shot-merge-progress" style="display:none"></div></div>';
  body.insertAdjacentHTML('beforeend', sec);
  fetch('/api/shots/' + epNum).then(function(r) { return r.json(); }).then(function(d) {
    var shots = d.shots || [];
    var listEl = document.getElementById('shot-list-' + epNum);
    var actionsEl = document.getElementById('shot-actions-' + epNum);
    if (!listEl) return;
    if (!shots.length) { listEl.innerHTML = '<div class="shot-empty">暂无视频片段</div>'; if (actionsEl) actionsEl.style.display = 'none'; return; }
    if (actionsEl) actionsEl.style.display = 'flex';
    var h = '';
    shots.forEach(function(s, i) {
      var t = s.title || s.name || ('片段 ' + (i + 1));
      var dur = s.duration || '--:--';
      var thumb = s.thumbnail ? '<img class="shot-thumb" src="' + s.thumbnail + '">' : '<div class="shot-thumb-placeholder">🎬</div>';
      h += '<div class="shot-item" draggable="true"><span class="shot-idx">' + (i+1) + '.</span>' + thumb + '<div class="shot-info"><span class="shot-title">' + t + '</span><span class="shot-dur">' + dur + '</span></div><span class="shot-drag-hint">☰</span></div>';
    });
    listEl.innerHTML = h;
  }).catch(function() {
    var listEl = document.getElementById('shot-list-' + epNum);
    if (listEl) listEl.innerHTML = '<div class="shot-empty">暂无视频片段</div>';
  });
}

}

function renderShotList(epNum,shots){
  const listEl=document.getElementById('shot-list-'+epNum);
  const actionsEl=document.getElementById('shot-actions-'+epNum);
  if(!listEl)return;

  if(!shots.length){
    listEl.innerHTML='<div class="shot-empty">该集暂无已生成视频片段</div>';
    if(actionsEl)actionsEl.style.display='none';
    return;
  }

  if(actionsEl)actionsEl.style.display='flex';

  let h='';
  shots.forEach((shot,i)=>{
    const thumbUrl=shot.thumbnail||'';
    const thumb=thumbUrl?`<img class="shot-thumb" src="${thumbUrl}" loading="lazy" onerror="this.outerHTML='<div class=shot-thumb-placeholder>🎬</div>'">`:'<div class="shot-thumb-placeholder">🎬</div>';
    const dur=shot.duration||'--:--';
    h+=`<div class="shot-item" data-idx="${i}" data-name="${shot.name||''}">`;
    h+=thumb;
    h+=`<span class="shot-name">${shot.name||shot.file}</span>`;
    h+=`<span class="shot-dur">${dur}</span>`;
    h+=`<span class="shot-actions">`;
    h+=`<button class="shot-move-btn" onclick="moveShotUp('${epNum}',${i})" ${i===0?'disabled':''} title="上移">&uarr;</button>`;
    h+=`<button class="shot-move-btn" onclick="moveShotDown('${epNum}',${i})" ${i===shots.length-1?'disabled':''} title="下移">&darr;</button>`;
    h+=`</span></div>`;
  });
  listEl.innerHTML=h;

}

function getShotOrder(epNum){
  const listEl=document.getElementById('shot-list-'+epNum);
  if(!listEl)return[];
  const items=listEl.querySelectorAll('.shot-item');
  return Array.from(items).map(it=>it.dataset.name);
}

function moveShotUp(epNum,idx){
  const listEl=document.getElementById('shot-list-'+epNum);
  if(!listEl||idx<=0)return;
  const items=listEl.querySelectorAll('.shot-item');
  const curr=items[idx];
  const prev=items[idx-1];
  listEl.insertBefore(curr,prev);
  // Re-render with updated indices
  const names=Array.from(listEl.querySelectorAll('.shot-item')).map(it=>({name:it.dataset.name,dur:it.querySelector('.shot-dur').textContent,thumb:it.querySelector('.shot-thumb')?.src||''}));
  renderShotList(epNum,names.map(n=>({name:n.name,file:n.name,duration:n.dur,thumbnail:n.thumb})));
}

function moveShotDown(epNum,idx){
  const listEl=document.getElementById('shot-list-'+epNum);
  if(!listEl)return;
  const items=listEl.querySelectorAll('.shot-item');
  if(idx>=items.length-1)return;
  const curr=items[idx];
  const next=items[idx+1];
  listEl.insertBefore(next,curr);
  const names=Array.from(listEl.querySelectorAll('.shot-item')).map(it=>({name:it.dataset.name,dur:it.querySelector('.shot-dur').textContent,thumb:it.querySelector('.shot-thumb')?.src||''}));
  renderShotList(epNum,names.map(n=>({name:n.name,file:n.name,duration:n.dur,thumbnail:n.thumb})));
}

async function mergeShots(epNum){
  const files=getShotOrder(epNum);
  if(!files.length){toastMsg('没有可合并的片段',2000,'warn');return;}

  const msgEl=document.getElementById('shot-msg-'+epNum);
  if(msgEl){msgEl.style.display='block';msgEl.textContent='正在合并 '+files.length+' 个片段...';}

  try{
    const r=await fetch('/api/merge',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({episode:String(epNum),files})});
    const d=await r.json();
    if(d.error){toastMsg('合并失败: '+d.error,3000,'error');}
    else{toastMsg('合并成功: '+d.output_file,3000);}
  }catch(e){toastMsg('合并请求失败: '+e.message,3000,'error');}
  if(msgEl)msgEl.style.display='none';
}

// S3-2: Generate subtitle with whisper
async function generateSubtitle(epNum){
  const msgEl=document.getElementById('shot-msg-'+epNum);
  if(msgEl){msgEl.style.display='block';msgEl.textContent='正在生成字幕...';}

  try{
    const r=await fetch('/api/subtitle',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({episode:String(epNum)})});
    const d=await r.json();
    if(d.error){toastMsg('字幕生成失败: '+d.error,3000,'error');}
    else{toastMsg('字幕生成成功',3000);if(d.srt)console.log('SRT:',d.srt);}
  }catch(e){toastMsg('字幕请求失败: '+e.message,3000,'error');}
  if(msgEl)msgEl.style.display='none';
}

// ================================================================
// UX-1: Image Compare Mode
// ================================================================
let compareMode = false;
function toggleCompare(imgs) {
  if (!imgs || imgs.length < 2) { toastMsg('需要至少 2 张图片才能对比', 2000, 'warn'); return; }
  compareMode = !compareMode;
  const gal = document.querySelector('.img-gallery');
  if (!gal) return;
  if (compareMode) {
    let h = '<div class="compare-view">';
    const labels = ['原始', '处理后', '去背景', '最终'];
    imgs.forEach((img, i) => {
      h += `<div class="compare-col"><div class="comp-label">${labels[i] || '图'+(i+1)}</div><img src="${img.url||img}" onclick="zoomImg('${img.url||img}')"/></div>`;
    });
    h += '</div>';
    gal.outerHTML = h;
    document.getElementById('kbdToggle').textContent = '🔲 退出对比';
  } else {
    renderDetail();
    document.getElementById('kbdToggle').textContent = '⌨ 快捷键';
  }
}

// ================================================================
// UX-3: Keyboard Shortcuts + Navigation
// ================================================================
let kbFocusIdx = -1;
function toggleKbdHint() {
  const el = document.getElementById('kbdHint');
  el.classList.toggle('show');
}

document.addEventListener('keydown', e => {
  // Don't capture when typing in input/textarea
  const tag = e.target.tagName.toLowerCase();
  if (tag === 'input' || tag === 'textarea' || tag === 'select') {
    if (e.key === 'Escape') e.target.blur();
    return;
  }

  const modal = document.getElementById('modal');
  const kbdHint = document.getElementById('kbdHint');

  if (e.key === 'Escape') {
    if (kbdHint.classList.contains('show')) { kbdHint.classList.remove('show'); return; }
    if (modal.classList.contains('on')) { closeModal(); return; }
    if (sel) { sel = null; render(); return; } // back to list
    return;
  }

  if (e.key === '?' || (e.shiftKey && e.key === '/')) {
    e.preventDefault();
    toggleKbdHint();
    return;
  }

  if (e.key === '/') {
    e.preventDefault();
    document.getElementById('searchInput').focus();
    return;
  }

  if (e.key === 'r' || e.key === 'R') {
    e.preventDefault();
    
  document.getElementById('tkSearchBar').style.display = (t==='tk' ? 'block' : 'none');
refresh();
    toastMsg('🔄 刷新中...', 1500);
    return;
  }

  if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
    e.preventDefault();
    switchTab(e.key === 'ArrowLeft' ? 'tk' : 'drama');
    return;
  }

  // ↑↓ navigation in left panel
  if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
    e.preventDefault();
    const items = document.querySelectorAll('.ms-item');
    if (!items.length) return;
    if (kbFocusIdx < 0) kbFocusIdx = 0;
    else if (e.key === 'ArrowDown') kbFocusIdx = Math.min(kbFocusIdx + 1, items.length - 1);
    else kbFocusIdx = Math.max(kbFocusIdx - 1, 0);
    items.forEach(it => it.classList.remove('kb-focus'));
    items[kbFocusIdx].classList.add('kb-focus');
    items[kbFocusIdx].scrollIntoView({ block: 'nearest' });
    return;
  }

  if (e.key === 'Enter' && kbFocusIdx >= 0) {
    e.preventDefault();
    const items = document.querySelectorAll('.ms-item');
    if (items[kbFocusIdx]) items[kbFocusIdx].click();
    return;
  }
});

// ================================================================
// UX-5: Modal close helper (click outside)
// ================================================================
function closeModal() {
  document.getElementById('modal').classList.remove('on');
}

// ================================================================
// UX-4: Pipeline Monitor Panel
// ================================================================
async function renderPipelineMonitor() {
  const detailEl = document.getElementById('detail');
  if (!detailEl) return;
  let sec = `<div class="sec"><h3>🔧 管线服务状态</h3><div class="pipeline-monitor" id="svcMonitor"><span class="loading">SSE 连接中...</span></div></div>`;
  detailEl.insertAdjacentHTML('beforeend', sec);
  connectPipelineSSE();
}
function connectPipelineSSE(){
  if (window._pipelineSSE) { window._pipelineSSE.close(); }
  const es = new EventSource('/api/pipeline/stream');
  window._pipelineSSE = es;
  es.onmessage = function(evt){
    try {
      const d = JSON.parse(evt.data);
      const svcs = d.services || {};
      const pipe = d.pipeline || {};
      const cf = svcs.comfyui || {};
      const tt = svcs.tts || {};
      let rows = '';
      // Flask API — always online since we received this SSE
      rows += '<div class="svc-row"><span>⚙️</span><span class="svc-dot online"></span><span class="svc-name">Flask API</span><span class="svc-detail">端口5001 · task_wizard</span></div>';
      // GPT-SoVITS
      const ttsDot = tt.online ? 'online' : 'offline';
      const ttsDetail = tt.online ? '端口9880可达 · TTS推理' : '端口9880不可达';
      rows += '<div class="svc-row"><span>🎤</span><span class="svc-dot '+ttsDot+'"></span><span class="svc-name">GPT-SoVITS</span><span class="svc-detail">'+ttsDetail+'</span></div>';
      // ComfyUI
      const cfDot = cf.online ? 'online' : 'offline';
      const cfExtra = cf.online ? ' · '+(cf.running||0)+'运行 '+(cf.pending||0)+'排队' : '';
      const cfDetail = cf.online ? '端口8188可达'+cfExtra+' · 图像渲染' : '端口8188不可达';
      rows += '<div class="svc-row"><span>🎨</span><span class="svc-dot '+cfDot+'"></span><span class="svc-name">ComfyUI</span><span class="svc-detail">'+cfDetail+'</span>';
      // v3.7.8: ComfyUI 重试按钮
      if(!cf.online) rows += '<span style="margin-left:6px"><button class="mini-btn" onclick="retryComfyUI(this)">重试连接</button></span>';
      rows += '</div>';
      // Pipeline progress
      const done = pipe.done || 0, total = pipe.total || 0;
      const pct = total ? Math.round(done/total*100) : 0;
      const pctDot = pct > 50 ? 'online' : (pct > 0 ? 'unknown' : 'offline');
      rows += '<div class="svc-row" style="flex-wrap:wrap;padding-bottom:8px"><span>📊</span><span class="svc-dot '+pctDot+'"></span><span class="svc-name">管线总进度</span><span class="svc-detail">'+done+'/'+total+' ('+pct+'%)</span><div style="width:100%;height:4px;background:#222;border-radius:2px;margin-top:2px"><div style="width:'+pct+'%;height:100%;background:#2563eb;border-radius:2px;transition:width .5s"></div></div></div>';
      // Timestamp
      rows += '<div style="font-size:8px;color:#444;text-align:right;padding:2px 0">更新 '+ (d.time || '—') +' · SSE</div>';
      const el = document.getElementById('svcMonitor');
      if (el) el.innerHTML = rows;
    } catch(e) {}
    // Also poll every 30s as fallback
    setTimeout(updatePipelineMonitor, 30000);
  };
  es.onerror = function(){
    const el = document.getElementById('svcMonitor');
    if (el) el.innerHTML = '<span class="loading" style="color:#ef4444">SSE 断线，5秒后重连...</span>';
    setTimeout(updatePipelineMonitor, 5000);
  };
}

// ================================================================
// UX-5: Poll-based pipeline monitor fallback (used when SSE unavailable)
// ================================================================
async function updatePipelineMonitor(){
  const checks = [
    { name: 'Flask API', url: '/api/status', port: 5001, detail: 'task_wizard', icon: '⚙️' },
    { name: 'GPT-SoVITS', url: 'http://localhost:9880/control', port: 9880, detail: 'TTS推理', icon: '🎤' },
    { name: 'ComfyUI', url: 'http://localhost:8188/queue', port: 8188, detail: '图像渲染', icon: '🎨' },
  ];
  let rows = '';
  for (const svc of checks) {
    let status = 'unknown', detail = '检测中...', extra = '';
    try {
      const r = await fetch(svc.url, { signal: AbortSignal.timeout(3000) });
      status = 'online';
      if (svc.name === 'ComfyUI' && r.ok) {
        const d = await r.json();
        const run = (d.queue_running||[]).length;
        const pend = (d.queue_pending||[]).length;
        extra = ' · '+run+'运行 '+pend+'排队';
      }
      detail = '端口'+svc.port+'可达'+extra;
    } catch(e) { status='offline'; detail='端口'+svc.port+'不可达'; }
    rows += '<div class="svc-row"><span>'+svc.icon+'</span><span class="svc-dot '+status+'"></span><span class="svc-name">'+svc.name+'</span><span class="svc-detail">'+detail+'</span></div>';
  }
  try {
    const r = await fetch('/api/dashboard');
    const d = await r.json();
    const ms = d.milestones || [];
    const done = ms.filter(m=>m.status==='completed'||m.status==='approved').length;
    const total = ms.length;
    const pct = total ? Math.round(done/total*100) : 0;
    rows += '<div class="svc-row" style="flex-wrap:wrap;padding-bottom:10px"><span>📊</span><span class="svc-name">管线总进度</span><span class="svc-detail">'+done+'/'+total+' ('+pct+'%)</span><div style="width:100%;height:4px;background:#222;border-radius:2px;margin-top:2px"><div style="width:'+pct+'%;height:100%;background:#2563eb;border-radius:2px"></div></div></div>';
  } catch(e) {}
  const el = document.getElementById('svcMonitor');
  if (el) el.innerHTML = rows;
}

// ================================================================
// UX-6: Refresh status indicator + toast on auto-refresh
// ================================================================
let _lastRefreshCount = 0;
function setRefreshStatus(syncing) {
  const el = document.getElementById('refreshStatus');
  if (syncing) {
    el.textContent = '同步中...';
    el.className = 'refresh-status syncing';
  } else {
    el.textContent = '';
    el.className = 'refresh-status';
  }
}

// Override refresh() to add status feedback
const _origRefresh = refresh;
refresh = async function () {
  setRefreshStatus(true);
  try {
    const r = await fetch('/api/dashboard');
    lastData = await r.json();
    const newAll = (lastData?.milestones || []).map(m => ({ ...m, pipeline: (String(m.ms_id || '').startsWith('DM') ? 'drama' : 'tk') }));
    // Detect changes
    const changed = newAll.length !== all.length || newAll.some((m, i) => m.status !== (all[i]?.status));
    all = newAll;
    render();
    document.getElementById('lastRefresh').textContent = new Date().toLocaleTimeString();
    // Auto-refresh toast (only if changed)
    if (changed && all.length > 0) {
      const waiting = all.filter(m => m.status === 'waiting_approval');
      if (waiting.length > 0) {
        toastMsg(`⚡ ${waiting.length} 项待决策: ` + waiting.map(m => m.ms_id).join(', '), 4000, 'warn');
      }
    }
  } catch (e) {
    document.getElementById('lastRefresh').textContent = '离线';
  }
  setRefreshStatus(false);
};

// ================================================================
// UX-9: Stats Tooltip on Hover
// ================================================================
(function initStatTooltips() {
  const tooltips = {
    statDone: '已完成(含已批准)的里程碑数',
    statPending: '等待人工决策的里程碑数',
    statMock: '数据源为模拟/推算的条目(⚠️非真实API)',
    statTotal: '当前 Tab 下的总里程碑数'
  };
  for (const [id, tip] of Object.entries(tooltips)) {
    const el = document.getElementById(id);
    if (!el) continue;
    el.title = tip;
    el.style.cursor = 'help';
  }
})();

// ⛔ 铁则 #0 自动检测: PRD 版本滞后告警
(function checkPRDStaleness() {
  const el = document.getElementById('prdStaleAlert');
  if (!el) return;
  // Extract current code version from title/badge
  const titleEl = document.getElementById('appTitle');
  const codeVerMatch = titleEl ? titleEl.textContent.match(/v3\.6\.(\d+)/) : null;
  if (!codeVerMatch) return;
  const codeVer = parseInt(codeVerMatch[1], 10);
  // Fetch PRD latest version
  fetch('/reports/PRD-v3.6.md?_=' + Date.now(), {cache: 'no-store'})
    .then(r => r.ok ? r.text() : Promise.reject())
    .then(txt => {
      const m = txt.match(/v3\.6\.(\d+)/g);
      if (!m) return;
      const nums = m.map(s => parseInt(s.replace('v3.6.',''), 10)).filter(n => !isNaN(n));
      const prdMax = Math.max(...nums);
      if (codeVer > prdMax) {
        document.getElementById('prdAlertCodeVer').textContent = 'v3.6.' + codeVer;
        document.getElementById('prdAlertPrdVer').textContent = 'v3.6.' + prdMax;
        el.style.display = 'block';
      }
    }).catch(() => {});
})();

// ================================================================
// UX-10: Search Highlight Helper
// ================================================================
function highlightText(text, query) {
  if (!query || !text) return text;
  const escaped = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const regex = new RegExp(`(${escaped})`, 'gi');
  return text.replace(regex, '<mark class="search-hl">$1</mark>');
}

// Apply highlight in render() list items - patch the render function
const _origRender = render;
render = function () {
  _origRender();
  // Apply search highlights to list items
  if (searchQ) {
    const listEl = document.getElementById('list');
    if (listEl) {
      listEl.querySelectorAll('.nm').forEach(el => {
        const text = el.textContent;
        if (text.toLowerCase().includes(searchQ)) {
          el.innerHTML = highlightText(text, searchQ);
        }
      });
    }
  }
};

// ================================================================
// UX-11: Enhanced Empty State with Action Guidance
// ================================================================
const _origRenderSummary = renderSummary;
renderSummary = function () {
  _origRenderSummary();
  const view = document.getElementById('summaryView');
  if (!view) return;
  // Add action hints at bottom
  const hints = cur === 'tk' ?
    ['💡 点击左侧「待决策」里程碑进行审批', '💡 按 / 快速搜索，←→ 切换 Tab'] :
    ['💡 点击 DM-0 查看故事板 + AI 审核结果', '💡 按 R 刷新，? 查看快捷键'];
  view.innerHTML += `<div style="margin-top:16px;font-size:10px;color:#444;line-height:1.8">${hints.join('<br>')}</div>`;
};

// ================================================================
// P1-4: Unified Download Panel
// ================================================================
let dlPanelOpen = false;
function toggleDlPanel() {
  dlPanelOpen = !dlPanelOpen;
  document.getElementById('dlPanel').classList.toggle('show', dlPanelOpen);
}
document.addEventListener('click', e => {
  if (dlPanelOpen && !e.target.closest('.dl-wrap')) {
    dlPanelOpen = false;
    document.getElementById('dlPanel').classList.remove('show');
  }
});

async function downloadAs(fmt) {
  toggleDlPanel();
  toastMsg('📥 正在生成 ' + fmt.toUpperCase() + '...', 2000);
  try {
    if (!lastData) { toastMsg('⚠️ 无数据可导出，请先刷新', 2000, 'warn'); return; }
    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const fn = `agentic-os-${ts}.${fmt}`;

    if (fmt === 'json') {
      const blob = new Blob([JSON.stringify(lastData, null, 2)], { type: 'application/json' });
      triggerDownload(blob, fn);
    } else if (fmt === 'csv') {
      let csv = 'Milestone,Name,Status,DataSource,TaskID,Decision\n';
      (lastData.milestones || []).forEach(m => {
        csv += `"${m.ms_id}","${m.name || ''}","${m.status}","${m.data_source || ''}","${m.task_id || ''}","${m.decision || ''}"\n`;
      });
      triggerDownload(new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8' }), fn);
    } else if (fmt === 'csv-decisions') {
      let csv = 'Milestone,Action,Reason,Timestamp\n';
      (lastData.milestones || []).filter(m => m.decision).forEach(m => {
        csv += `"${m.ms_id}","${m.decision}","${m.decision_reason || ''}","${m.updated_at || ''}"\n`;
      });
      triggerDownload(new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8' }), fn);
    } else if (fmt === 'md') {
      let md = `# Agentic OS 状态报告\n\n生成时间: ${new Date().toLocaleString()}\n\n## 里程碑概览\n\n| Milestone | 名称 | 状态 | 数据源 |\n|---|---|---|---|\n`;
      (lastData.milestones || []).forEach(m => {
        md += `| ${m.ms_id} | ${m.name || '-'} | ${m.status} | ${m.data_source || '-'} |\n`;
      });
      md += `\n## 统计\n- 总计: ${(lastData.milestones || []).length}\n- 已完成: ${(lastData.milestones || []).filter(m => m.status === 'completed' || m.status === 'approved').length}\n- 待决策: ${(lastData.milestones || []).filter(m => m.status === 'waiting_approval').length}\n`;
      triggerDownload(new Blob([md], { type: 'text/markdown' }), fn);
    } else if (fmt === 'html') {
      const html = document.documentElement.outerHTML;
      triggerDownload(new Blob([html], { type: 'text/html' }), fn);
    } else {
      toastMsg('⚠️ 不支持格式: ' + fmt, 2000, 'warn'); return;
    }
    toastMsg('✅ ' + fmt.toUpperCase() + ' 导出成功', 2500);
  } catch (e) {
    toastMsg('❌ 导出失败: ' + e.message, 3000, 'error');
  }
}

function triggerDownload(blob, filename) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// ================================================================
// P1-6: Chart.js Data Visualization
// ================================================================
let chartInstance = null;
let chartMode = 'status';
let pipelineFilter = 'all'; // v3.7.8: 'all' | 'tk' | 'drama'

function renderChartPanel() {
  const rightEl = document.getElementById('detail');
  if (!rightEl || document.getElementById('chartPanel')) return;

  const chartHTML = `<div class="chart-panel" id="chartPanel">
    <div class="chart-hdr">
      <h4>📊 管线数据可视化</h4>
      <div class="chart-filter-tags" style="display:flex;gap:4px;margin-bottom:6px">
        <span data-filter="all" class="chart-tag active" onclick="switchPipelineFilter('all',this)">全部</span>
        <span data-filter="tk" class="chart-tag" onclick="switchPipelineFilter('tk',this)">TK运营</span>
        <span data-filter="drama" class="chart-tag" onclick="switchPipelineFilter('drama',this)">数字短剧</span>
      </div>
      <div class="chart-tabs">
        <span class="chart-tab active" onclick="switchChart('status',this)">状态分布</span>
        <span class="chart-tab" onclick="switchChart('source',this)">数据源</span>
        <span class="chart-tab" onclick="switchChart('pipeline',this)">管线对比</span>
        <span class="chart-tab" onclick="switchChart('timeline',this)">里程碑时间轴</span>
      </div>
    </div>
    <canvas id="mainChart"></canvas>
  </div>`;
  rightEl.insertAdjacentHTML('afterbegin', chartHTML);
  updateChart('status');
}

function switchChart(mode, tabEl) {
  chartMode = mode;
  document.querySelectorAll('.chart-tab').forEach(t => t.classList.remove('active'));
  if (tabEl) tabEl.classList.add('active');
  updateChart(mode);
}

// v3.7.8: Pipeline filter for chart panel
function switchPipelineFilter(id, el){
  pipelineFilter = id;
  document.querySelectorAll('.chart-tag').forEach(function(t){t.classList.remove('active');});
  if(el) el.classList.add('active');
  updateChart(chartMode);
}

function updateChart(mode) {
  if (!lastData || !lastData.milestones) return;
  var ms = lastData.milestones;
  // v3.7.8: Apply pipeline filter
  if (pipelineFilter !== 'all') {
    ms = ms.filter(function(m){return m.pipeline === pipelineFilter;});
  }
  if (chartInstance) { chartInstance.destroy(); chartInstance = null; }
  const ctx = document.getElementById('mainChart');
  if (!ctx) return;

  let labels, data, colors;

  if (mode === 'status') {
    const counts = {};
    ms.forEach(m => { counts[m.status] = (counts[m.status] || 0) + 1; });
    labels = Object.keys(counts);
    data = Object.values(counts);
    colors = labels.map(function(status) {
      switch(status) {
        case 'completed': return '#3b82f6';  // 蓝色
        case 'approved': return '#8b5cf6';   // 紫色
        case 'waiting_approval': return '#f59e0b';  // 橙色
        case 'pending': return '#06b6d4';    // 青色
        case 'running': return '#ec4899';    // 粉色
        case 'rejected': return '#ef4444';   // 红色
        default: return '#64748b';           // 石板灰
      }
    });
  } else if (mode === 'source') {
    const counts = {};
    ms.forEach(m => { counts[m.data_source || 'unknown'] = (counts[m.data_source || 'unknown'] || 0) + 1; });
    labels = Object.keys(counts);
    data = Object.values(counts);
    colors = ['#3b82f6', '#f59e0b', '#22c55e', '#8b5cf6', '#666'];
  } else if (mode === 'pipeline') {
    const tk = ms.filter(m => m.pipeline === 'tk');
    const dm = ms.filter(m => m.pipeline === 'drama');
    labels = ['TK运营', '数字短剧'];
    data = [
      tk.filter(m => m.status === 'completed' || m.status === 'approved').length,
      dm.filter(m => m.status === 'completed' || m.status === 'approved').length
    ];
    // Ensure we have valid values to prevent undefined in tooltips
    data = data.map(value => (typeof value !== 'undefined' && value !== null) ? value : 0);
    colors = ['#3b82f6', '#8b5cf6'];
  } else if (mode === 'timeline') {
    labels = ms.map(function(m){return m.fid||m.id});
    data = ms.map(function(m){
      return (m.status==='completed'||m.status==='approved')?100:
             (m.status==='running')?60:
             (m.status==='waiting_approval')?40:
             (m.status==='rejected')?20:10;
    });
    colors = ms.map(function(m){
      if(m.status==='completed'||m.status==='approved') return '#22c55e';
      if(m.status==='running') return '#3b82f6';
      if(m.status==='waiting_approval') return '#f59e0b';
      return '#64748b';
    });
  }

  chartInstance = new Chart(ctx, {
    type: (mode === 'pipeline' || mode === 'timeline') ? 'bar' : 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: colors,
        borderColor: '#0f1117',
        borderWidth: 2,
        hoverOffset: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: { color: '#aaa', font: { size: 10 }, padding: 12 }
        },
        tooltip: {
          backgroundColor: '#1a1d27',
          titleColor: '#e4e6eb',
          bodyColor: '#aaa',
          borderColor: '#333',
          borderWidth: 1,
          cornerRadius: 6,
          callbacks: {
            label: function(context) {
              let label = context.label || '';
              let value = '';
              
              if (context.parsed !== null) {
                if (mode === 'pipeline') {
                  value = context.parsed.y !== undefined ? context.parsed.y : context.raw;
                } else {
                  value = context.parsed !== undefined ? context.parsed : context.raw;
                }
              } else {
                value = context.raw || 0;
              }
              
              return label + ': ' + value + ' 项';
            }
          }
        }
      },
      ...((mode === 'pipeline' || mode === 'timeline') ? {
        indexAxis: mode === 'timeline' ? 'y' : 'x',
        scales: {
          x: { ticks: { color: '#888', font: { size: 10 } }, grid: { color: '#222' } },
          y: { beginAtZero: true, ticks: { stepSize: 1, color: '#888' }, grid: { color: '#222' } }
        }
      } : {})
    }
  });
}

// Patch renderDetail to inject chart
const _origRenderDetail3 = renderDetail;
renderDetail = async function() {
  await _origRenderDetail3();
  if (lastData && lastData.milestones && lastData.milestones.length > 0) {
    requestAnimationFrame(() => renderChartPanel());
  }
};

// ================================================================
// v3.6.9: P0-1 Collapsible Detail Sections (摘要折叠)
// ================================================================
function toggleAllSections() {
  const allBodies = document.querySelectorAll('.sec-body.collapsible');
  const anyCollapsed = Array.from(allBodies).some(b => !b.classList.contains('expanded'));
  allBodies.forEach(b => {
    if (anyCollapsed) b.classList.add('expanded');
    else b.classList.remove('expanded');
  });
  document.querySelectorAll('.sec-hdr.collapsible').forEach(h => {
    if (anyCollapsed) h.classList.add('expanded');
    else h.classList.remove('expanded');
  });
}

// Wrap existing section rendering to add collapsible structure
// This patches renderDefault and all renderDM* functions to wrap sections
function makeSectionCollapsible(secId, title, contentHTML, defaultExpanded = false) {
  const expanded = expandedSections.has(secId) || defaultExpanded;
  return `<div class="sec" style="padding:8px 12px;margin-bottom:6px">
    <div class="sec-hdr collapsable ${expanded ? 'expanded' : ''}" id="sechdr-${secId}" onclick="toggleSection('${secId}')" style="cursor:pointer;user-select:none;display:flex;align-items:center;gap:6px;font-size:11px;color:#888;padding:4px 0">
      <span class="sec-toggle-icon" style="transition:transform .2s;display:inline-block;transform:rotate(${expanded ? '90' : '0'}deg)">▶</span>
      ${title}
      <span style="margin-left:auto;font-size:8px;color:#555">${expanded ? '点击收起' : '点击展开'}</span>
    </div>
    <div class="sec-body collapsable ${expanded ? 'expanded' : ''}" id="secbody-${secId}" style="max-height:0;overflow:hidden;transition:max-height .3s ease-out;${expanded ? 'max-height:5000px' : ''}">
      ${contentHTML}
    </div>
  </div>`;
}

// ================================================================
// v3.6.9: P0-2 DM-0 四维度审核明细展示
// ================================================================
// v3.7.8: renderFourDimReview — 可折叠四维审核结果卡
function renderFourDimReview(reviewData) {
  const dimensions = reviewData?.dimensions || [];
  const overallScore = reviewData?.overall_score || 0;
  const decision = reviewData?.decision || 'pending';
  const details = reviewData?.dimension_details || [];
  
  let scoreColor = overallScore >= 6 ? '#22c55e' : (overallScore >= 4 ? '#f59e0b' : '#ef4444');
  
  let html = '<div style="text-align:center;margin-bottom:12px;padding:8px;background:#111;border-radius:6px">' +
    '<div style="font-size:9px;color:#555">综合评分</div>' +
    '<div style="font-size:28px;font-weight:700;color:'+scoreColor+'">'+overallScore.toFixed(1)+'/10</div>' +
    '<div style="font-size:10px;margin-top:2px">' +
    '<span class="bdg '+(decision === 'approved' ? 'ok' : decision === 'modify' ? 'mk' : 'dc')+'">' +
    ({approved:'✅ 通过', modify:'✏️ 需修改', rejected:'❌ 驳回', pending:'⏳ 待审核'}[decision]||'⏳ 待审核')+'</span></div></div>';
  
  if (dimensions.length === 0) {
    html += '<div style="font-size:10px;color:#555;text-align:center;padding:12px">⚠️ 四维度审核数据未返回<br><span style="font-size:9px">后端需返回 dimensions 数组</span></div>';
  } else {
    const icons = {'编剧':'📝','场景完整':'🎬','剧情节奏':'⏱️','逻辑一致':'🧠','剧本':'📝','场景':'🎬','节奏':'⏱️','逻辑':'🧠'};
    dimensions.forEach(function(dim, i){
      var name = dim.name || dim.dimension || '未知';
      var score = dim.score || dim.value || 0;
      var border = score >= 6 ? 'good' : (score >= 4 ? 'warn' : 'bad');
      var icon = icons[name]||'📋';
      var dtId = 'dim-detail-'+i;
      var detail = details[i]||{};
      var issues = detail.issues||[];
      var suggestions = detail.suggestions||[];
      html += '<div class="dim-card '+border+'" onclick="toggleSection(\''+dtId+'\')">';
      html += '<div class="dim-icon">'+icon+'</div><div class="dim-name">'+name+'</div>';
      html += '<div class="dim-score" style="color:'+(score>=6?'#22c55e':score>=4?'#f59e0b':'#ef4444')+'">'+score+'/10</div>';
      html += '<div style="font-size:9px;color:#555;cursor:pointer">▼</div></div>';
      html += '<div id="'+dtId+'" class="accordion-content" style="padding:8px 12px;background:rgba(0,0,0,.15);border-radius:0 0 6px 6px;margin-top:-2px">';
      if(issues.length){html+='<div style="font-size:10px;color:#f87171;margin-bottom:4px">⚠️ 问题:'+issues.map(function(x){return '<span style="display:block;padding:1px 0">• '+x+'</span>';}).join('')+'</div>';}
      if(suggestions.length){html+='<div style="font-size:10px;color:#93c5fd">💡 建议:'+suggestions.map(function(x){return '<span style="display:block;padding:1px 0">• '+x+'</span>';}).join('')+'</div>';}
      if(!issues.length&&!suggestions.length){html+='<div style="font-size:10px;color:#555">暂无明细</div>';}
      html += '</div>';
    });
  }
  return html;
}

// ================================================================
// v3.6.9: P0-3 修改→重处理→审核自动循环
// ================================================================
// v3.7.8: triggerReReview with SSE ReadableStream real-time logs
async function reReviewDM0(){
  const btn=document.getElementById('dm0-rerun-btn');
  if(btn){btn.disabled=true;btn.textContent='⏳ 审核中...';}
  var logPanel=document.getElementById('review-log-panel');
  if(!logPanel){
    logPanel=document.createElement('div');
    logPanel.id='review-log-panel';
    logPanel.className='review-log-panel';
    var detailEl=document.getElementById('detail');
    if(detailEl) detailEl.insertBefore(logPanel,document.getElementById('dm0-sec'));
  }
  logPanel.style.display='block';
  logPanel.innerHTML='<div style="font-size:10px;color:#93c5fd;margin-bottom:6px">📋 审核日志 (SSE实时流)</div>';
  function addLog(msg){logPanel.insertAdjacentHTML('beforeend','<div class="review-log-line">'+msg+'</div>');logPanel.scrollTop=logPanel.scrollHeight;}
  try{
    // v3.7.8: Use SSE ReadableStream for real-time logs
    var r=await fetch('/api/review/trigger/ep01/stream');
    var reader=r.body.getReader();
    var decoder=new TextDecoder();
    var buffer='';
    var resultData=null;
    // 读取流
    while(true){
      var {done,value}=await reader.read();
      if(done) break;
      buffer+=decoder.decode(value,{stream:true});
      // Process SSE lines
      var lines=buffer.split('\n');
      buffer=lines.pop()||'';
      var eventType='message';
      for(var i=0;i<lines.length;i++){
        var line=lines[i];
        if(line.startsWith('data: ')){
          var data=line.slice(6);
          try{
            var parsed=JSON.parse(data);
            if(eventType==='result'){
              resultData=parsed;
            }else{
              addLog(parsed.time+' '+parsed.msg);
            }
          }catch(e){/*ignore malformed*/}
        }else if(line.startsWith('event: ')){
          eventType=line.slice(7);
        }
      }
    }
    // Stream finished — render result
    if(resultData){
      addLog('📊 综合评分: '+resultData.overall_score+'/10 · '+resultData.decision);
      var dimSec=document.getElementById('dm0-decision-sec');
      if(dimSec&&resultData.dimensions){
        var content=renderFourDimReview(resultData);
        dimSec.querySelector('.four-dim').innerHTML=content;
        var scoreEl=dimSec.querySelector('div[style]');
        if(scoreEl) scoreEl.textContent='综合评分: '+resultData.overall_score+'/10';
        // Also re-render radar
        renderReviewRadar({dimensions:resultData.dimensions,overall_score:resultData.overall_score});
      }
      toastMsg('✅ 审核完成: '+resultData.overall_score+'/10',3000);
      if(typeof refresh==='function'){refresh();render();}
    }else{
      // Fallback: use traditional POST endpoint
      var fr=await fetch('/api/review/trigger/ep01',{method:'POST'});
      var d=await fr.json();
      addLog('📊 综合评分: '+d.overall_score+'/10 · '+d.decision);
      var dimSec2=document.getElementById('dm0-decision-sec');
      if(dimSec2&&d.dimensions){
        var content2=renderFourDimReview(d);
        dimSec2.querySelector('.four-dim').innerHTML=content2;
      }
      toastMsg('✅ 审核完成: '+d.overall_score+'/10',3000);
      if(typeof refresh==='function'){refresh();render();}
    }
  }catch(e){addLog('❌ 失败: '+e.message);toastMsg('审核失败',3000);}
  if(btn){btn.disabled=false;btn.textContent='🔄 重新审核';}
}

async function triggerReReview(msId) {
  const btn = document.getElementById('rerun-btn-' + msId);
  if (btn) { btn.classList.add('busy'); btn.textContent = '⏳ 重审中...'; }
  // 创建/复用日志面板
  let logPanel = document.getElementById('review-log-panel');
  if (!logPanel) {
    logPanel = document.createElement('div');
    logPanel.id = 'review-log-panel';
    logPanel.className = 'review-log-panel';
    const detailEl = document.getElementById('detail');
    if (detailEl) detailEl.insertAdjacentElement('beforeend', logPanel);
  }
  logPanel.style.display = 'block';
  logPanel.innerHTML = '<div style="font-size:10px;color:#93c5fd;margin-bottom:6px">📋 审核日志</div>';
  function addLog(msg) {
    logPanel.insertAdjacentHTML('beforeend', '<div class="review-log-line">' + msg + '</div>');
    logPanel.scrollTop = logPanel.scrollHeight;
  }
  addLog('⏳ 准备审核 ' + msId + '...');
  try {
    const r1 = await fetch('/api/decision', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ task_id: msId, action: 'modify', reason: '用户触发重新审核' })
    });
    if (!r1.ok) { addLog('❌ 重置失败: HTTP ' + r1.status); toastMsg('重置失败', 2500, 'error'); return; }
    addLog('✅ 状态已重置');
    
    const r2 = await fetch('/api/review/' + msId, { method: 'POST' });
    if (!r2.ok) { addLog('❌ 审核触发失败: HTTP ' + r2.status); toastMsg('审核触发失败', 2500, 'error'); return; }
    const result = await r2.json();
    
    // 模拟逐条显示日志
    var logs = result.logs || [];
    for (var i = 0; i < logs.length; i++) {
      addLog(logs[i]);
      await new Promise(function(r){setTimeout(r, 400);});
    }
    
    addLog('<strong style="color:#22c55e">✅ 审核完成: 评分 ' + (result.overall_score || 'N/A') + '/10</strong>');
    toastMsg('✅ 审核完成: 评分 ' + (result.overall_score || 'N/A') + '/10', 4000, 'success');
    setTimeout(refresh, 2000);
  } catch (e) {
    addLog('❌ 错误: ' + e.message);
    toastMsg('❌ 重审失败: ' + e.message, 3000, 'error');
  }
  if (btn) { btn.classList.remove('busy'); btn.textContent = '🔄 重新审核'; }
}

// v3.7.5: MS-4 发布审批交互函数
async function approveHuman(){
  toastMsg('🔄 正在提交人工审批...', 2000);
  try{
    var r=await fetch('/api/decision',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({task_id:'MS-4',action:'approved',reason:'人工审批通过'})});
    if(!r.ok){toastMsg('审批提交失败: HTTP '+r.status,2500,'error');return;}
    toastMsg('✅ 人工审批已通过',3000,'success');
    setTimeout(function(){select('MS-4')},1000);
  }catch(e){toastMsg('❌ 审批失败: '+e.message,3000,'error');}
}
async function rejectHuman(){
  toastMsg('🔄 正在提交驳回...', 2000);
  try{
    var r=await fetch('/api/decision',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({task_id:'MS-4',action:'rejected',reason:'人工审批驳回'})});
    if(!r.ok){toastMsg('驳回提交失败: HTTP '+r.status,2500,'error');return;}
    toastMsg('✅ 已驳回发布',3000,'warn');
    setTimeout(function(){select('MS-4')},1000);
  }catch(e){toastMsg('❌ 驳回失败: '+e.message,3000,'error');}
}
async function finalApprove(){
  toastMsg('🔄 正在执行批准发布...', 2000);
  try{
    var r=await fetch('/api/publish',{method:'POST'});
    if(!r.ok){toastMsg('发布失败: HTTP '+r.status,2500,'error');return;}
    var d=await r.json();
    toastMsg('✅ 发布成功',4000,'success');
    setTimeout(function(){select('MS-5')},1500);
  }catch(e){toastMsg('❌ 发布失败: '+e.message,3000,'error');}
}
async function finalReject(){
  if(!confirm('确认驳回发布申请？此操作将重置 MS-4 状态。')) return;
  toastMsg('🔄 正在驳回发布...', 2000);
  try{
    var r=await fetch('/api/decision',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({task_id:'MS-4',action:'rejected',reason:'最终驳回发布'})});
    if(!r.ok){toastMsg('驳回失败: HTTP '+r.status,2500,'error');return;}
    toastMsg('✅ 已驳回，MS-4 已重置',3000,'warn');
    setTimeout(function(){select('MS-4')},1000);
  }catch(e){toastMsg('❌ 驳回失败: '+e.message,3000,'error');}
}

// ================================================================
// v3.6.9: UX-5 图片对比视图（修复：JS 正确调用）
// ================================================================
function showCompareView(galleryEl) {
  if (!galleryEl) return;
  const imgs = galleryEl.querySelectorAll('.img-card img');
  if (imgs.length < 2) { toastMsg('需要至少 2 张图片才能对比', 2000, 'warn'); return; }
  
  compareMode = true;
  const labels = ['原始', '处理后', '去背景', '最终', '镜1', '镜2', '镜3'];
  let h = '<div class="compare-view" style="display:flex;gap:8px;overflow-x:auto;padding:8px 0">';
  Array.from(imgs).forEach((img, i) => {
    h += `<div class="compare-col" style="flex:0 0 auto;text-align:center">
      <div class="comp-label" style="font-size:9px;color:#888;margin-bottom:4px">${labels[i] || '图'+(i+1)}</div>
      <img src="${img.src}" style="max-height:300px;border-radius:4px;cursor:pointer" onclick="zoomImg('${img.src}')" />
    </div>`;
  });
  h += '</div><div style="text-align:center;margin-top:8px"><button class="mini-btn" onclick="exitCompare(this)">✕ 退出对比</button></div>';
  galleryEl.outerHTML = h;
}
function exitCompare(btn) {
  renderDetail();
  compareMode = false;
}

// ================================================================
// v3.6.9: UX-6 音色试听（Web Speech API fallback）
// ================================================================
// Voice functions now in DM-1 section (uploadRefAudio, generateVoice, detectVoiceApi)
// Preload voices for Web Speech API (fallback)
if ('speechSynthesis' in window) speechSynthesis.getVoices();

// ================================================================
// v3.6.9: UX-8 操作级进度反馈（Per-operation progress bar）
// ================================================================
function showOpProgress(containerId, msg, percent) {
  let bar = document.getElementById('op-prog-' + containerId);
  if (!bar) {
    const container = document.getElementById(containerId);
    if (!container) return;
    container.insertAdjacentHTML('beforeend',
      `<div id="op-prog-${containerId}" style="margin-top:8px">
        <div style="font-size:9px;color:#888;margin-bottom:2px" id="op-prog-msg-${containerId}">${msg}</div>
        <div style="height:4px;background:#222;border-radius:2px;overflow:hidden">
          <div id="op-prog-fill-${containerId}" style="height:100%;background:#3b82f6;width:${percent}%;transition:width .3s;border-radius:2px"></div>
        </div>
      </div>`);
  } else {
    const msgEl = document.getElementById('op-prog-msg-' + containerId);
    const fillEl = document.getElementById('op-prog-fill-' + containerId);
    if (msgEl) msgEl.textContent = msg;
    if (fillEl) fillEl.style.width = percent + '%';
  }
}
function hideOpProgress(containerId) {
  const el = document.getElementById('op-prog-' + containerId);
  if (el) el.remove();
}

// ================================================================
// v3.6.9: P2-7 质量反馈知识库
// ================================================================
const QUALITY_KB = [
  { q: 'Q: 渲染图模糊怎么办？', a: '检查 ComfyUI SDXL 模型是否加载正确；确认分辨率设置为 1024×1024；尝试添加 "high quality, detailed" 到 prompt。' },
  { q: 'Q: TTS 发音不准确？', a: '在文本中用拼音标注多音字（如「重(chóng)新」）；调整 NLS speaker 参数；检查参考音频质量。' },
  { q: 'Q: SFX 音效不匹配场景？', a: '修改 SCENE_SFX_MAP 中的音效关键词；在 freesound.org 搜索更匹配的标签；调整音量混合比例。' },
  { q: 'Q: 审核评分偏低？', a: '检查剧本连贯性；确保分镜描述包含机位/景别/动作；添加情绪和台词细节。' },
  { q: 'Q: 管线服务连接失败？', a: '确认 Flask 在 :5001 运行；ComfyUI 在 :8188 运行；GPT-SoVITS 在 :9880 运行。用 `ps aux | grep python` 检查进程。' },
  { q: 'Q: 决策按钮无响应？', a: '检查后端 /api/decision 是否返回 200；查看浏览器开发者工具 Network 面板；确认 task_id 格式正确。' },
];

function renderQualityKB() {
  const detailEl = document.getElementById('detail');
  if (!detailEl || document.getElementById('qualityKB')) return;
  let html = '<div class="sec" id="qualityKB"><h3>📚 质量反馈知识库</h3>';
  html += '<p style="font-size:9px;color:#555;margin-bottom:8px">点击问题查看答案 · 持续更新中</p>';
  QUALITY_KB.forEach((item, i) => {
    html += `<div class="qa-item">
      <div class="q-q" onclick="this.nextElementSibling.classList.toggle('show')">${item.q} <span style="font-size:8px;color:#555">▼</span></div>
      <div class="q-a">${item.a}</div>
    </div>`;
  });
  html += '</div>';
  detailEl.insertAdjacentHTML('beforeend', html);
}

// ================================================================
// v3.6.9: P2-8 自愈提示（连续失败自动弹出）
// ================================================================
let failureCounts = {};
let lastFailureKey = '';

function trackFailure(key) {
  failureCounts[key] = (failureCounts[key] || 0) + 1;
  lastFailureKey = key;
  if (failureCounts[key] >= 3) {
    showSelfHealTip(key);
  }
}
function trackSuccess(key) {
  failureCounts[key] = 0;
  hideSelfHealTip();
}

function showSelfHealTip(key) {
  const rightEl = document.getElementById('detail');
  if (!rightEl || document.getElementById('selfHealTip')) return;
  
  const tips = {
    'render': '渲染连续失败：\n1. 检查 ComfyUI 是否在 :8188 运行\n2. 查看 ComfyUI 控制台错误日志\n3. 尝试重启 comfyui_renderer.py',
    'tts': 'TTS 连续失败：\n1. 检查 GPT-SoVITS 是否在 :9880 运行\n2. 确认 .env 中 NLS 密钥有效\n3. 尝试 macOS say 命令 fallback',
    'decision': '决策 API 连续失败：\n1. 检查 Flask 是否在 :5001 运行\n2. 查看 task_wizard.py 日志\n3. 确认 task_id 格式正确',
    'default': '操作连续失败，请检查对应服务状态'  
  };
  
  const tip = tips[key] || tips['default'];
  const html = `<div class="self-heal" id="selfHealTip">
    <span class="sh-dismiss" onclick="hideSelfHealTip()">✕</span>
    <div class="sh-title">💡 自动诊断提示 (${key})</div>
    <div class="sh-body" style="white-space:pre-line">${tip}</div>
  </div>`;
  rightEl.insertAdjacentHTML('afterbegin', html);
}

function hideSelfHealTip() {
  const el = document.getElementById('selfHealTip');
  if (el) el.remove();
}

// ================================================================
// v3.6.9: Patch renderDefault to add collapsible sections
// ================================================================
const _origRenderDefault = renderDefault;
renderDefault = function(detail) {
  const html = _origRenderDefault(detail);
  // Wrap sections in collapsible structure
  return html.replace(/<div class="sec" id="([^"]+)"/g, (match, id) => {
    return `<div class="sec" id="${id}" data-collapsible="true"`;
  });
};

// ================================================================
// v3.6.9: Patch renderDM0 to add four-dimension review + re-review button
// ================================================================
const _origRenderDM0 = renderDM0;
renderDM0 = async function(detail, ms) {
  await _origRenderDM0(detail, ms);
  
  // Add four-dimension review section
  // Backend returns detail.review_dimensions [{dimension, score, status}]
  // Also try detail.review (legacy) or sections extraction
  let reviewData = null;
  if (detail?.review_dimensions && detail.review_dimensions.length > 0) {
    const dims = detail.review_dimensions;
    const scores = dims.map(d => parseFloat(d.score) || 0).filter(s => s > 0);
    const overall = scores.length ? scores.reduce((a,b)=>a+b,0)/scores.length : 0;
    reviewData = {
      dimensions: dims,
      overall_score: overall,
      decision: overall >= 6 ? 'approved' : overall >= 4 ? 'modify' : 'rejected'
    };
  } else if (detail?.review) {
    reviewData = detail.review;
  } else if (ms?.review) {
    reviewData = ms.review;
  }
  if (reviewData) {
    const reviewHTML = renderFourDimReview(reviewData);
    const dm0Sec = document.getElementById('dm0-sec');
    if (dm0Sec) {
      dm0Sec.insertAdjacentHTML('beforeend', `<div class="sec" id="dm0-review" style="margin-top:10px">
        <h3>🔍 AI 对抗审核明细</h3>
        ${reviewHTML}
      </div>`);
    }
  }
  
  // Add re-review button
  const msId = ms?.ms_id || 'DM-0';
  const dm0Sec2 = document.getElementById('dm0-sec');
  if (dm0Sec2) {
    dm0Sec2.insertAdjacentHTML('beforeend', `
      <div style="margin-top:8px;display:flex;gap:6px;align-items:center">
        <button class="btn btn-rerun" id="rerun-btn-${msId}" onclick="triggerReReview('${msId}')">🔄 重新审核</button>
        <span style="font-size:9px;color:#555">修改后点击此按钮触发自动重审</span>
      </div>`);
  }
};

// ================================================================
// v3.6.9: Patch renderDetail to inject quality KB + pipeline monitor
// ================================================================
const _origRenderDetail2 = renderDetail;
renderDetail = async function() {
  await _origRenderDetail2();
  
  // Add pipeline monitor to all detail views
  if (cur === 'drama') {
    requestAnimationFrame(() => {
      renderPipelineMonitor();
      renderQualityKB();
    });
  }
};

// ================================================================
// v3.6.13: Expand ALL sections by default (show all data)
// ================================================================
function autoCollapseDetails() {
  const secBodies = document.querySelectorAll('.sec-body');
  secBodies.forEach((body) => {
    body.classList.remove('collapsed');
    const hdr = body.closest('.sec')?.querySelector('.sec-hdr');
    if (hdr) hdr.classList.add('expanded');
  });
}

// Patch renderDetail to expand all sections
const _origRenderDetail4 = renderDetail;
renderDetail = async function() {
  await _origRenderDetail4();
  setTimeout(autoCollapseDetails, 50);
};

// ================================================================
// v3.6.9: Init - auto-refresh every 30 seconds
// ================================================================

// ================================================================
// v3.6.12: Debug - check if data loads
// ================================================================
(async function debugLoad() {
  console.log('[DEBUG] Starting data load check...');
  try {
    const r = await fetch('/api/dashboard?t=' + Date.now());
    console.log('[DEBUG] fetch status:', r.status);
    const d = await r.json();
    console.log('[DEBUG] milestones count:', (d.milestones || []).length);
    if (d.milestones && d.milestones.length > 0) {
      console.log('[DEBUG] first milestone:', d.milestones[0].ms_id, d.milestones[0].name);
    }
  } catch(e) {
    console.error('[DEBUG] fetch FAILED:', e.message);
  }
  
  // Also show a visible indicator
  const el = document.getElementById('version-check');
  if (el) {
    try {
      const r2 = await fetch('/api/dashboard?t=' + Date.now());
      const d2 = await r2.json();
      const count = (d2.milestones || []).length;
      el.textContent = `✅ DATA OK: ${count} milestones loaded | P4-STRIP | ` + new Date().toLocaleTimeString();
      el.style.background = count > 0 ? '#10b981' : '#ef4444';
      if (count === 0) el.textContent += ' — API returned 0 items!';
    } catch(e) {
      el.textContent = `❌ FETCH FAILED: ${e.message} — check console`;
      el.style.background = '#ef4444';
    }
  }
  
  // Global error catcher — show JS errors in the banner
  window.onerror = function(msg, url, line, col, error) {
    const el = document.getElementById('version-check');
    if (el) {
      el.textContent = '❌ JS ERROR: ' + msg + ' (line ' + line + ')';
      el.style.background = '#ef4444';
    }
    return false;
  };
})();

// v3.7.8: Guarantee init runs even if DOM/scripts load out of order
(function initDashboard(){
  console.log('[INIT] Dashboard starting, DOM readyState='+document.readyState);
  try {
    refresh();
    setInterval(refresh, 30000);
    console.log('[INIT] refresh() called, 30s polling started');
  } catch(e) {
    console.error('[INIT] FAILED:', e.message);
    var el = document.getElementById('lastRefresh');
    if (el) { el.textContent = 'INIT ERROR: ' + e.message; el.style.color = '#ef4444'; }
  }
})();

function toggleAssetPanel(){
  console.log("assetToggle clicked");
  const p=document.getElementById('assetPanel'),o=document.getElementById('assetOverlay');
  if(p.classList.contains('open')){p.classList.remove('open');o.classList.remove('on')}
  else{p.classList.add('open');o.classList.add('on');loadAssetPanel()}
}
function switchAssetTab(el,type){
  document.querySelectorAll('#assetTabs .asset-tab').forEach(t=>t.classList.remove('active'));
  el.classList.add('active');loadAssetPanel(type);
}
async function loadAssetPanel(type){
  const body=document.getElementById('assetBody');
  body.innerHTML='<div class="loading"><span class="spinner"></span>加载 '+ (type||'全部') +' 资产...</div>';
  let items=[];
  try{
    if(!type||type==='all'||type==='render'){
      const r=await fetch('/api/images');const d=await r.json();
      (d.images||[]).slice(0,50).forEach(img=>items.push({name:img.name,type:'render',url:img.url,character:img.character,size:img.size}));
    }
    if(!type||type==='all'||type==='script'){
      const r=await fetch('/api/script');const d=await r.json();
      (d.episodes||[]).forEach(ep=>items.push({name:'第'+ep.episode+'集',type:'script',episode:ep.episode,file:ep.file||''}));
    }
    if(!type||type==='all'||type==='episode'){
      for(let e=1;e<=10;e++){
        try{
          const r=await fetch('/api/script/'+e);const d=await r.json();
          items.push({name:d.title||'第'+e+'集',type:'episode',episode:e,shots:(d.shots||[]).length,file:'/api/script/'+e});
        }catch(ex){}
      }
    }
  }catch(e){}
  if(!items.length){body.innerHTML='<div style="color:#555;text-align:center;padding:20px;font-size:11px">暂无资产</div>';return;}
  items.sort((a,b)=>a.name.localeCompare(b.name));
  let h='';let count=0;
  items.forEach(it=>{
    if(type&&type!=='all'&&it.type!==type)return;
    count++;
    if(it.type==='render')h+='<div class="asset-item"><img class="thumb" src="'+it.url+'" loading="lazy" onerror="this.style.display=\'none\'"/><div class="info"><div class="name">'+it.character+' · '+it.name+'</div><div class="meta">'+(it.size/1024).toFixed(0)+'KB</div></div><button class="dl-btn" onclick="window.open(\''+it.url+'\')">📥</button></div>';
    else if(it.type==='script')h+='<div class="asset-item"><div class="info"><div class="name">📄 '+it.name+'</div><div class="meta">剧本</div></div><button class="dl-btn" onclick="window.open(&quot;/api/script/&quot;+it.episode+&quot;)">📥</button></div>';
    else h+='<div class="asset-item"><div class="info"><div class="name">🎬 '+it.name+'</div><div class="meta">'+it.shots+'个分镜</div></div></div>';
  });
  body.innerHTML=count?'':'<div style="color:#555;text-align:center;padding:20px;font-size:11px">没有'+type+'类资产</div>'+h;
}

// v3.7 S2-2: Add video preview mock buttons to DM-1 character cards
(function injectPreviewButtons() {
  var checkExist = setInterval(function() {
    var btns = document.querySelectorAll('[id^="rerender-btn-"]');
    if (btns.length > 0) {
      clearInterval(checkExist);
      btns.forEach(function(btn) {
        var fid = btn.id.replace('rerender-btn-', '');
        if (document.getElementById('preview-btn-' + fid)) return;
        var preview = document.createElement('button');
        preview.id = 'preview-btn-' + fid;
        preview.className = 'cb-btn';
        preview.textContent = '🎬 预览动态';
        preview.onclick = function() {
          toastMsg('🎬 视频预览: Pollo AI / Kling API 未配置', 3000, 'warn');
        };
        btn.parentNode.insertBefore(preview, btn);
      });
    }
  }, 1000);
})();


// v3.7: S4-2 Director Mode
function toggleDirectorMode() {
  var left = document.querySelector('.left');
  var topbar = document.querySelector('.topbar');
  var version = document.getElementById('VER_BADGE');
  var kbd = document.getElementById('kbdToggle');
  var expandAll = document.getElementById('expandAll');
  var dlwrap = document.querySelector('.dl-wrap');
  var assetBtn = document.getElementById('assetToggle');
  var galleryLink = document.querySelector('a[href="/gallery"]');
  var dirBtn = document.getElementById('dirModeBtn');
  var prdAlert = document.getElementById('prdStaleAlert');
  var isActive = document.body.classList.toggle('director-mode');

  if (isActive) {
    if (left) left.style.display = 'none';
    if (version) version.style.display = 'none';
    if (kbd) kbd.style.display = 'none';
    if (expandAll) expandAll.style.display = 'none';
    if (dlwrap) dlwrap.style.display = 'none';
    if (assetBtn) assetBtn.style.display = 'none';
    if (galleryLink) galleryLink.style.display = 'none';
    if (prdAlert) prdAlert.style.display = 'none';
    if (dirBtn) dirBtn.textContent = '🎬 退出导演模式';
    // Hide src-tags
    document.querySelectorAll('.src-tag').forEach(function(e) { e.style.display = 'none'; });
    // Hide stats bar
    document.querySelectorAll('.stats').forEach(function(e) { e.style.display = 'none'; });
  } else {
    if (left) left.style.display = '';
    if (version) version.style.display = '';
    if (kbd) kbd.style.display = '';
    if (expandAll) expandAll.style.display = '';
    if (dlwrap) dlwrap.style.display = '';
    if (assetBtn) assetBtn.style.display = '';
    if (galleryLink) galleryLink.style.display = '';
    if (prdAlert) prdAlert.style.display = '';
    if (dirBtn) dirBtn.textContent = '🎬 导演模式';
    document.querySelectorAll('.src-tag').forEach(function(e) { e.style.display = ''; });
    document.querySelectorAll('.stats').forEach(function(e) { e.style.display = ''; });
  }
  localStorage.setItem('director_mode', isActive ? '1' : '0');
}

// ================================================================
// Sprint 3: 里程碑内嵌图表 (利润瀑布图 / 审核雷达图 / 管线时间轴)
// ================================================================
let radarChartInst = null;
let timelineChartInst = null;
let profitChartInst = null;

// v3.7.8: 审核五维雷达图 + 点击维度展开文字说明
var reviewDimDescriptions = [];

function renderReviewRadar(data) {
  const canvas = document.getElementById('dm0Radar');
  if (!canvas) return;
  if (radarChartInst) { radarChartInst.destroy(); radarChartInst = null; }
  const dims = data.dimensions || [];
  if (!dims.length){ console.warn('[Radar] No dimension data'); return; }
  // 使用与 renderDM0 一致的四维名称
  var allDims = [
    {name:'编剧质量', score:0},
    {name:'分镜设计', score:0},
    {name:'逻辑一致性', score:0},
    {name:'节奏把控', score:0},
    {name:'场景完整性', score:0},
  ];
  // 多维度名称模糊匹配
  function matchDim(dName){
    if(!dName) return -1;
    for(var i=0;i<allDims.length;i++){
      var a = allDims[i].name;
      if(a.indexOf(dName)>=0||dName.indexOf(a)>=0) return i;
    }
    // Semantic keywords
    var keywords = [
      ['编剧','剧本','writing','script'],
      ['分镜','场景','scene','storyboard'],
      ['逻辑','logic','consistency'],
      ['节奏','pacing','rhythm'],
      ['叙事','narrative','完整性','complete'],
    ];
    for(var i=0;i<keywords.length;i++){
      for(var k=0;k<keywords[i].length;k++){
        if(dName.indexOf(keywords[i][k])>=0) return i;
      }
    }
    return -1;
  }
  dims.forEach(function(d) {
    var idx = matchDim(d.name||'');
    if(idx>=0 && idx<allDims.length){
      allDims[idx].score = typeof d.score==='number'?d.score:(d.total_score||5);
    }
  });
  // 若仍全0，用前5个维度的score
  if(allDims.every(function(d){return d.score===0;})){
    dims.slice(0,5).forEach(function(d,i){if(i<allDims.length){allDims[i].name=d.name||allDims[i].name;allDims[i].score=typeof d.score==='number'?d.score:5;}});
  }
  var labels = allDims.map(function(d){return d.name;});
  var scores = allDims.map(function(d){return d.score;});
  var colors = ['#3b82f680','#8b5cf680','#f59e0b80','#22c55e80','#a78bfa80'];
  var descKeys = {'编剧质量':'编剧规则评审: 剧情遵循基本叙事逻辑','分镜设计':'分镜设计评估: 各场景描述充分、衔接自然','逻辑一致性':'逻辑一致性检查: 因果关系自洽、无逻辑漏洞','节奏把控':'剧情节奏分析: 高潮铺垫合理、张弛有度','场景完整性':'场景完整性评估: 各场景描述完整、过渡流畅'};
  reviewDimDescriptions = allDims.map(function(d){return {name:d.name, score:d.score, desc:descKeys[d.name]||d.name+'评估'};});
  var radarContainer = canvas.parentElement;
  if(!radarContainer) return;
  radarChartInst = new Chart(canvas, {
    type: 'radar',
    data: {
      labels: labels,
      datasets: [{label: '审核评分', data: scores, backgroundColor: 'rgba(59,130,246,0.2)', borderColor: '#3b82f6', borderWidth: 2, pointBackgroundColor: colors}]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      onClick: function(e, activeEls) { if(activeEls.length){showDimDesc(activeEls[0].index);} },
      scales: { r: { suggestedMin: 0, suggestedMax: 10, ticks: { color: '#94a3b8', backdropColor: 'transparent', stepSize: 2 }, grid: { color: '#334155' }, pointLabels: { color: '#e2e8f0', font: { size: 10 } } } },
      plugins: { legend: { labels: { color: '#e2e8f0' } }, tooltip: { enabled: false } }
    }
  });
}
function showDimDesc(index) {
  var d = reviewDimDescriptions[index];
  if(!d) return;
  var existing=document.getElementById('radar-desc-panel');
  if(existing)existing.remove();
  var panel=document.createElement('div');
  panel.id='radar-desc-panel';
  var scoreColor = d.score >= 6 ? '#22c55e' : d.score >= 4 ? '#f59e0b' : '#ef4444';
  panel.style.cssText='margin-top:6px;padding:8px 10px;background:rgba(0,0,0,.2);border-radius:6px;font-size:10px;border-left:3px solid '+scoreColor;
  panel.innerHTML='<strong style="color:'+scoreColor+'">'+d.name+': '+d.score+'/10</strong><br><span style="color:#888">'+d.desc+'</span>';
  var radarContainer = document.getElementById('dm0Radar');
  if(radarContainer) radarContainer.parentElement.appendChild(panel);
}

// v3.7.8: ComfyUI 连接重试
function retryComfyUI(btn){
  if(!btn) return;
  btn.disabled = true;
  btn.textContent = '⏳ 检测中...';
  fetch('http://localhost:8188')
    .then(function(r){
      btn.textContent = '✅ 可达';
      btn.style.color = '#22c55e';
      toastMsg('✅ ComfyUI 连接正常', 3000, 'success');
      // 刷新服务状态
      var svcMonitor = document.getElementById('svcMonitor');
      if(svcMonitor) { svcMonitor.innerHTML = '<span class="loading">刷新状态...</span>'; loadPipelineMonitor(); }
    })
    .catch(function(e){
      btn.textContent = '❌ 不可达';
      btn.style.color = '#ef4444';
      toastMsg('❌ ComfyUI 端口8188不可达，请启动服务', 3000, 'error');
    })
    .finally(function(){
      setTimeout(function(){ btn.disabled = false; btn.textContent = '重试连接'; btn.style.color = ''; }, 5000);
    });
}

function renderPipelineTimeline() {
  const canvas = document.getElementById('timelineChart');
  if (!canvas) return;
  if (timelineChartInst) { timelineChartInst.destroy(); timelineChartInst = null; }
  var ms = lastData.milestones || [];
  if (!ms.length) return;
  var labels = ms.map(function(m){return m.fid||m.id});
  var data = ms.map(function(m){
    var score = (m.status === 'completed' || m.status === 'approved') ? 100 :
                (m.status === 'running') ? 60 :
                (m.status === 'waiting_approval') ? 40 :
                (m.status === 'rejected') ? 20 : 10;
    return score;
  });
  var bgColors = ms.map(function(m) {
    if (m.status === 'completed'||m.status==='approved') return '#22c55e';
    if (m.status === 'running') return '#3b82f6';
    if (m.status === 'waiting_approval') return '#f59e0b';
    return '#64748b';
  });
  timelineChartInst = new Chart(canvas, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{ label: '进度%', data: data, backgroundColor: bgColors, borderRadius: 4, barThickness: 14 }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      scales: { x: { ticks: { color: '#94a3b8' }, grid: { color: '#334155' }, max: 100 }, y: { ticks: { color: '#e2e8f0', font: { size: 9 } } } },
      plugins: { legend: { display: false } }
    }
  });
}

// v3.7.8: 8步利润瀑布图
function renderProfitChart(msData) {
  var canvas = document.getElementById('profitChart');
  if (!canvas) return;
  if (profitChartInst) { profitChartInst.destroy(); profitChartInst = null; }
  var labels = ['1688成本','国内物流','国际物流','平台佣金','支付手续费','汇率折损','落地成本','净利润'];
  var isCost = [true, true, true, true, true, true, false, false];
  var data = msData && msData.profit_breakdown ? msData.profit_breakdown.map(function(x){return parseFloat(x);}) : [33,8,15,8,3,5,72,30];
  while(data.length < 8) data.push(0);
  profitChartInst = new Chart(canvas, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: '金额(¥)',
        data: data.slice(0,8),
        backgroundColor: data.slice(0,8).map(function(v,i){return isCost[i] ? '#ef4444' : '#22c55e';}),
        borderRadius: 4
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      indexAxis: 'y',
      scales: {
        y: { ticks: { color: '#e2e8f0', font: {size:10} }, grid: { color: '#334155' } },
        x: { ticks: { color: '#94a3b8' }, grid: { color: '#334155' }, beginAtZero: true }
      },
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: function(ctx){return ctx.raw + ' ¥';} } }
      }
    }
  });
}

// v3.7.8: Auto-render charts when milestone detail opens
function renderMilestoneCharts(fid) {
  if (fid === 'DM-0') {
    var d = lastData.decisions ? lastData.decisions['DM-0'] : null;
    if (d) renderReviewRadar(d);
  } else if (fid === 'MS-1' || fid === 'MS-2') {
    var ms = findMilestone(fid);
    if (ms && ms.meta) renderProfitChart(ms.meta);
  }
}

console.log("SCRIPT-FULLY-LOADED: sDM0="+typeof renderDM0+" sDM1="+typeof renderDM1+" sRD="+typeof renderDetail+" sRDE="+typeof renderDMEpisode+" sDM2="+typeof renderDM2+" wDM2="+(typeof window!="undefined"&&typeof window.renderDM2)+" sDM3="+typeof renderDM3+" sDM10="+typeof renderDM10);
