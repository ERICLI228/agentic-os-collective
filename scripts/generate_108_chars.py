#!/usr/bin/env python3
"""Generate 108 Water Margin heroes character data from descriptions."""
import json, os, sys
from datetime import datetime

CHARS = [
    # (name, pinyin, star_rank, nickname, actor, cn_desc, en_prompt, episode, height, build, face, age)
    ("宋江","songjiang",1,"天魁星·及时雨","李雪健","矮个子，面色黝黑，皮肤粗糙，神情谦卑。眼神中交织着忠义、权谋与一丝令人难以捉摸的阴沉。身着深色圆领袍衫，头戴样式简单的官帽。","He has a short stature and a dark, weathered face with rough skin. His expression is humble yet his eyes reveal a complex mix of loyalty, ambition, and a hint of cunning. Wearing a dark round-necked official robe and a simple official cap. High-quality screenshot from a classic Chinese historical drama, cinematic lighting, film grain.","EP04","175cm","矮小瘦弱，文官体型","面色黝黑，细眉沉目，粗糙皮肤","四十岁"),
    ("卢俊义","lujunyi",2,"天罡星·玉麒麟","王卫国","面相轩昂，贵气十足，标准的国字脸，眉眼间透着正气。身形伟岸，气质沉稳如山，不怒自威。身着精致的员外服饰。","He has a dignified, noble face with a standard square jaw, brows and eyes full of righteousness. Tall and imposing physique, exuding calm majesty. Wearing exquisite wealthy landlord's robes. High-quality Chinese historical drama screenshot, cinematic lighting.","EP07","188cm","伟岸挺拔，英雄体型","国字脸，眉宇正气，贵气十足","三十五岁"),
    ("吴用","wuyong",3,"天机星·智多星","宁晓志","一张略显老气、饱经风霜的脸，留着三缕长髯。眼神深邃，带着一丝文人的孤傲与谋士的阴鸷。身着灰白色长衫。","He has an old-looking, weather-beaten face with a long three-strand beard. Deep, profound eyes carrying a scholar's aloof pride and strategist's calculating gloom. Wearing a plain greyish-white long robe. High-quality Chinese historical drama screenshot.","EP06","176cm","清瘦文雅，书生体型","清瘦脸庞，长须飘逸，目光睿智","三十八岁"),
    ("公孙胜","gongsunsheng",4,"天闲星·入云龙","汪永贵","道士形象，身形清瘦，眼神清亮而超脱。头戴道冠，身穿灰色道袍，手持拂尘，透着一股仙风道骨的高人风范。","He looks like a Taoist priest with a lean figure. Clear, bright eyes detached from worldly affairs. Wearing a Taoist headpiece, grey Taoist robe, holding a horsetail whisk, exuding an immortal-like sage aura. Chinese historical drama style.","EP08","180cm","清瘦飘逸，道人身形","清瘦脸庞，眼神清亮超脱","四十五岁"),
    ("关胜","guansheng",5,"天勇星·大刀","李振起","面如重枣，眉宇间透着一股傲气，留有标志性的美髯长须。身着绿色战袍，外罩金甲，手持青龙偃月刀。","His face is deep red like jujube. Between his brows is an air of pride, with an iconic long, lush beard. Wearing a green battle robe covered with golden armor, wielding the Green Dragon Crescent Blade. Chinese historical drama style, cinematic lighting.","EP09","190cm","魁梧伟岸，武将体型","面如重枣，美髯长须，傲气逼人","四十岁"),
    ("林冲","linchong",6,"天雄星·豹子头","周野芒","面相儒雅文气，五官端正，透着一股内敛的悲剧气质。头戴范阳毡笠，身穿褪色的蓝灰色布袍。","He has a refined, scholarly appearance with proper features, carrying a restrained tragic quality. Wearing a felt hat and faded blue-grey cloth robe. High-quality Chinese historical drama screenshot.","EP03","182cm","精干匀称，武者体型","儒雅面庞，薄髭，眼中含悲愤","三十二岁"),
    ("秦明","qinming",7,"天猛星·霹雳火","王文升","性如烈火，怒目圆睁，络腮胡须根根竖起。身穿鱼鳞甲，头戴红缨盔，手持狼牙棒，气势骇人。","He has a fiery temper, angry wide-open eyes, and a bristling full beard. Wearing scale armor and a red-tassel helmet, wielding a wolf-tooth club, his manner terrifying. Chinese historical drama style.","EP09","185cm","粗壮威猛，猛将体型","怒目圆睁，络腮胡竖，气势骇人","三十八岁"),
    ("呼延灼","huyanzhuo",8,"天威星·双鞭","贾石头","国字脸，留着长髯，气质沉稳威严。头戴铁兜鍪，身披连环铠，手持两条水磨八棱钢鞭。","He has a square face with a long beard, steady and imposing demeanor. Wearing an iron helmet and interlocking chainmail, holding two steel maces. Chinese historical drama style.","EP09","183cm","沉稳厚重，大将体型","国字脸，长髯威严","四十岁"),
    ("花荣","huarong",9,"天英星·小李广","修庆","面容英俊，剑眉星目，五官清秀，眉宇间带着一股年轻的英气。身着银白色战袍，腰挎雕弓，气质英武。","He has a handsome face with sword-like eyebrows and starry eyes. Delicate refined features with a young heroic spirit. Wearing a silver-white battle robe with a carved bow at his waist. Chinese historical drama style.","EP09","180cm","挺拔英武，青年武将","英俊面庞，剑眉星目","二十五岁"),
    ("柴进","chaijin",10,"天贵星·小旋风","郑强","肤色白皙，蓄着短须，天生一股养尊处优的贵气。头戴纱帽，身穿绣有暗纹的锦袍，腰悬宝剑，举止不凡。","He has fair skin and a short beard, exuding natural noble elegance. Wearing a gauze cap and brocade robe with subtle patterns, a sword at his waist. Chinese historical drama style.","EP07","178cm","端正挺拔，贵族体型","白皙面庞，短须贵气","三十岁"),
    ("李应","liying",11,"天富星·扑天雕","无","面相精明，蓄着长髯，气质沉稳，举手投足间有大家之主的风范。身穿做工考究的深色锦袍，腰系玉带，气度不凡。","He has a shrewd face with a long beard, calm demeanor carrying the air of a wealthy estate master. Wearing an exquisite dark brocade robe with jade belt. Chinese historical drama style.","EP07","178cm","沉稳端正，庄主体型","精明面庞，长髯沉稳","三十八岁"),
    ("朱仝","zhutong",12,"天满星·美髯公","杨增元","面如重枣，留着一副齐胸的浓密美髯，神态威严而又透着忠厚。身穿官袍，腰悬佩刀。","His face is dark red like jujube with a lush beautiful beard reaching his chest. Majeous yet loyal expression. Wearing an official uniform with a saber at his waist. Chinese historical drama style.","EP07","182cm","高大威猛，军官体型","面如重枣，美髯齐胸","三十五岁"),
    ("董平","dongping",15,"天立星·双枪将","无","面容俊朗，身材挺拔，气质风流潇洒。身穿亮银色铠甲，头戴凤翅盔，手持双枪，英气勃勃。","He has a handsome face and tall upright figure, dashing and unrestrained temperament. Wearing bright silver armor and phoenix-wing helmet, wielding twin spears. Chinese historical drama style.","EP09","183cm","挺拔潇洒，青年武将","俊朗面庞，风流潇洒","二十八岁"),
    ("张清","zhangqing_feishi",16,"天捷星·没羽箭","无","面容白皙清秀，透着一股少年英气，神情自信。身穿轻便皮甲，腰系飞石袋，身形矫健，敏捷灵动。","He has a fair delicate face radiating youthful heroic spirit with confident eyes. Wearing light leather armor with a stone pouch at his waist, agile and nimble. Chinese historical drama style.","EP09","178cm","矫健灵动，青年身形","白皙清秀，少年英气","二十二岁"),
    ("杨志","yangzhi",17,"天暗星·青面兽","翟乃社","国字脸，神情沉重阴郁，眉间有因家族使命形成的'川'字纹。身穿旧战袍，头戴破旧的范阳毡笠，是心事重重的末路英雄。","He has a square face with a heavy gloomy expression. Deep frown lines between his brows from family honor. Wearing an old battle robe and worn felt hat, a troubled hero at the end of his rope. Chinese historical drama style.","EP05","185cm","高挑挺拔，军人体型","棱角分明，面颊青记，薄唇紧抿","三十岁"),
    ("鲁智深","luzhishen",13,"天孤星·花和尚","臧金生","体型极其魁梧壮硕，面阔耳大，络腮胡，面相凶悍，却眼神清亮带慧。身穿灰色僧袍，坦露前胸，脖子上挂着一串大佛珠。","He is extremely burly and stout with a wide face and large ears. Full beard, fierce intimidating face, yet eyes are clear and wise. Wearing a grey monk's robe with chest exposed and a large string of Buddhist beads around his neck. Chinese historical drama style.","EP02","195cm","巨汉，熊腰虎背，肌肉虬结","圆面大耳，络腮胡，额上九个香疤","三十五岁"),
    ("武松","wusong",14,"天伤星·行者","丁海峰","浓眉斜插入鬓，如墨染一般。丹凤眼精光四射，眼角微挑，不怒自威。戴着铁界箍，身披灰色头陀服。","He has thick ink-black eyebrows slanting up to temples. Phoenix eyes gleaming sharply, slightly upturned at corners, imposing without anger. Wearing the iconic iron fillet headband and grey headband monk's robe. Chinese historical drama style.","EP01","188cm","魁梧健壮，虎背熊腰","方颚浓眉，豹头环眼，燕颔虎须","二十八岁"),
    ("徐宁","xuning",18,"天佑星·金枪手","张巍","面容端正，气质沉稳。头戴铺霜耀日镔铁盔，身穿钩嵌梅花榆叶甲，手持金枪，一副禁军教头的气派。","He has a proper upright face with calm demeanor. Wearing a polished iron helmet and plum-blossom armor, holding a golden spear, every bit the imperial instructor. Chinese historical drama style.","EP09","180cm","端正挺拔，教头体型","面容端正，沉稳气派","三十五岁"),
    ("索超","suochao",19,"天空星·急先锋","张浩","面圆耳大，阔口方腮，络腮胡，神情急迫凶悍。身穿熟铜甲，手持金蘸斧，一副急不可耐的先锋模样。","He has a round face, large ears, wide mouth and full beard, urgent fierce expression. Wearing bronze armor wielding a golden battle-axe, impatient and ready to charge. Chinese historical drama style.","EP09","183cm","粗壮威猛，先锋体型","面圆耳大，络腮凶悍","三十二岁"),
    ("戴宗","daizong",20,"天速星·神行太保","王基明","身形精瘦，双腿修长，面容清癯，神情机警。身穿深色短打衣衫，小腿上绑着甲马，风尘仆仆。","He has a lean wiry frame with long legs and gaunt face, alert sharp expression. Wearing dark short-cut traveling clothes with magical talismans on his legs, travel-worn. Chinese historical drama style.","EP07","175cm","精瘦修长，轻功身形","清癯面庞，神情机警","三十五岁"),
    ("刘唐","liutang",21,"天异星·赤发鬼","邰祖辉","面相凶恶，颧骨高耸，鬓边有一搭朱砂记，上面长着一片黑黄杂毛。眼神狠戾，身形彪悍。","He has a fierce ugly face with high cheekbones. A red birthmark beside his temple covered with black-yellow hair. Ruthless eyes, burly build. Chinese historical drama style.","EP07","180cm","彪悍粗壮，草莽体型","凶恶面庞，颧骨高耸，鬓边朱砂","三十岁"),
    ("史进","shijin",23,"天微星·九纹龙","郭军","面如银盘，脸型偏圆，皮肤白皙。年轻气盛，眼神明亮，充满朝气。后身着劲装，敞开胸膛，露出满身刺青。","He has a round face like a silver plate with fair skin. Young spirited with bright lively eyes. Later wears martial outfit with chest open revealing full-body tattoos. Chinese historical drama style.","EP07","180cm","挺拔健壮，青年武者","银盘脸，白皙面庞，明亮眼神","二十三岁"),
    ("穆弘","muhong",24,"天究星·没遮拦","无","面相豁达豪迈，留着一副络腮胡，眼神张扬。身着华丽的锦袍，外罩大氅，一副财大气粗的乡绅模样。","He has an open forthright face with a full beard, bold unrestrained eyes. Wearing splendid brocade robe covered by a large cloak, like wealthy local gentry. Chinese historical drama style.","EP07","182cm","壮实豪迈，乡绅体型","豁达面庞，络腮张扬","三十五岁"),
    ("雷横","leiheng",25,"天退星·插翅虎","郭柏松","面色紫黑，扇形胡须，神情倨傲。头戴范阳毡笠，身穿都头官服，腰悬朴刀，气派十足。","He has a purplish-black face and fan-shaped beard, arrogant proud expression. Wearing a felt hat and constable's uniform, a saber at his waist. Chinese historical drama style.","EP07","178cm","粗壮结实，军官体型","紫黑面庞，扇形胡须，倨傲神情","三十八岁"),
    ("李逵","likui",22,"天杀星·黑旋风","赵小锐","身形粗壮如铁塔，浑身肌肉虬结。皮肤黝黑，满脸横肉，须发戟张，豹头环眼，眼神带着凶光与天真。","He has a stout iron-tower-like build with bulging muscles. Dark black skin, face covered in ferocious flesh, hair and beard bristle like spines, leopard head and round eyes, showing cruelty and naive innocence. Chinese historical drama style.","EP05","190cm","黝黑粗壮，肌肉暴起","漆黑面皮，环眼暴突，wild messy hair","二十六岁"),
    ("李俊","lijun",26,"天寿星·混江龙","杨宝光","肤色黝黑，浓眉大眼，眼神深沉，透着精明强干。身穿麻布短打衣衫，手持船桨，一副水上英雄的模样。","He has dark skin, thick eyebrows, large eyes. Deep calculating gaze radiating shrewdness. Wearing coarse linen outfit holding a boat oar, hero of the river. Chinese historical drama style.","EP08","180cm","结实精干，水军体型","黝黑面庞，浓眉大眼","三十五岁"),
    ("阮小二","ruanxiaoer",27,"天剑星·立地太岁","刘卫华","面色蜡黄，脸上有深刻的皱纹，眼神沧桑而坚定。头戴斗笠，身穿蓑衣，是饱经风霜的老渔夫。","He has a sallow waxy complexion with deep wrinkles. World-weary yet resolute eyes. Wearing a bamboo hat and straw rain cape, a weathered aging fisherman. Chinese historical drama style.","EP08","175cm","瘦削结实，渔民体型","蜡黄面庞，深刻皱纹","四十岁"),
    ("张横","zhangheng",28,"天平星·船火儿","兰恭英","肤色黝黑，络腮胡，神情凶狠，嘴角带着一丝残忍的笑意。站在船头，手持锋利的钩镰枪。","He has dark skin and a full beard, fierce ruthless expression with a cruel smile. Standing at the prow holding a sharp hooked spear. Chinese historical drama style.","EP08","178cm","粗壮凶悍，水匪体型","黝黑面庞，络腮凶狠","三十三岁"),
    ("阮小五","ruanxiaowu",29,"天罪星·短命二郎","张衡平","眼神阴鸷，神情孤僻。脸颊上有一块明显的青色胎记，人称'青面兽'阮小五。","He has a gloomy gaze and solitary detached expression. A prominent green birthmark on his cheek. Chinese historical drama style.","EP08","176cm","精瘦敏捷，渔民体型","阴鸷眼神，青色胎记","三十岁"),
    ("张顺","zhangshun",30,"天损星·浪里白条","张亚坤","皮肤雪白，面容清秀，身形修长，肌肉线条流畅。眼神清澈灵动，神态潇洒，水性极佳。","He has strikingly snow-white skin and delicate handsome face. Long lean physique with smooth streamlined muscles. Clear lively eyes, free and easy demeanor. Chinese historical drama style.","EP08","180cm","修长匀称，水军体型","雪白面庞，清秀灵动","二十八岁"),
    ("阮小七","ruanxiaoqi",31,"天败星·活阎罗","李冬果","面色微黄，眼睛不大但目光灵动，神情中透着机灵和野性。身穿粗布麻衣，神情桀骜不驯。","He has a slightly sallow complexion with small but sharp intelligent eyes, wild unruly spirit. Wearing coarse hemp clothing, fiercely independent. Chinese historical drama style.","EP08","174cm","精瘦灵巧，渔民体型","微黄面庞，灵动野性","二十六岁"),
    ("杨雄","yangxiong",32,"天牢星·病关索","陈之辉","面色微黄，留着短髭，神情沉默寡言。头戴皂纱巾，身穿淡黄色的囚服，眼神略带忧郁。","He has a pale sickly complexion with a short mustache, silent reserved expression. Wearing a black gauze scarf and pale yellow prisoner's robe, eyes slightly melancholic. Chinese historical drama style.","EP07","178cm","瘦削文弱，狱卒体型","微黄面庞，短髭沉默","三十二岁"),
    ("石秀","shixiu",33,"天慧星·拚命三郎","杨凡","眉清目秀，但眼神中带着一股狠劲和决绝。身穿黑色劲装，手持朴刀，一副视死如归的拼命模样。","He has delicate handsome features but eyes carrying fierce determination. Wearing a black martial outfit wielding a Pudao, ready to fight to the death. Chinese historical drama style.","EP07","178cm","精干敏捷，游侠体型","眉清目秀，狠劲决绝","二十八岁"),
    ("解珍","xiezhen",34,"天暴星·两头蛇","孔庆元","皮肤黝黑，身形矫健，眼神锐利如鹰。身穿虎皮猎装，手持钢叉，一副精明强干的猎户模样。","He has dark skin and a lean agile build, eyes sharp as a hawk. Wearing a tiger-skin hunter's outfit holding a steel trident, clever capable hunter. Chinese historical drama style.","EP08","180cm","矫健精干，猎户体型","黝黑面庞，锐利眼神","三十岁"),
    ("解宝","jiebao",35,"天哭星·双尾蝎","韩福利","外貌与哥哥相似，但眼神更加阴沉凶狠。同样身穿虎皮猎装，手持钢叉，是解珍的翻版，但气质更显狠辣。","He looks similar to his brother but with a darker more venomous gaze. Also wearing tiger-skin hunter's outfit holding a steel trident, more ruthless and fierce. Chinese historical drama style.","EP08","178cm","矫健精干，猎户体型","黝黑面庞，阴沉凶狠","二十八岁"),
    ("燕青","yanqing",36,"天巧星·浪子","王光辉","唇若涂朱，睛如点漆，面似堆琼。眉清目秀，眼神灵活，聪明伶俐。身穿精致的刺绣锦袍，腰悬短弩。","His lips are red, teeth white, eyes bright like stars, face like layered jade. Delicate handsome features, nimble intelligent eyes. Wearing exquisite embroidered brocade robe with a small crossbow. Chinese historical drama style.","EP07","176cm","匀称灵巧，多才体型","俊美面庞，灵活伶俐","二十三岁"),
    ("朱武","zhuwu",34,"地魁星·神机军师","由利平","留着山羊胡，眼神深沉，总是眯缝着眼，似乎总在算计。身穿道袍，手持羽扇，一副谋士打扮。","He has a goatee and deep calculating eyes always slightly narrowed, as if scheming. Wearing a Taoist robe holding a feather fan, like an advisor. Chinese historical drama style.","EP08","174cm","清瘦文弱，谋士体型","山羊胡，深沉算计","四十岁"),
    ("黄信","huangxin",35,"地煞星·镇三山","无","面相凶恶，留着一部络腮胡，眼神倨傲。头戴黄铜盔，身披镔铁甲，手持丧门剑，一副镇压山贼的武将模样。","He has a fierce intimidating face with a full beard and arrogant eyes. Wearing a brass helmet and iron armor, wielding a large sword. Chinese historical drama style.","EP09","180cm","粗壮威猛，武将体型","凶恶面庞，络腮倨傲","三十五岁"),
    ("孙立","sunli",36,"地勇星·病尉迟","齐景斌","面色淡黄，留着长髯，神情中带着一丝阴郁。头戴熟铜盔，身披乌油甲，手持竹节钢鞭，虽称病尉迟，但眼神依旧犀利。","He has a pale yellowish face with a long beard, expression carrying a hint of melancholy. Wearing a bronze helmet and dark oiled armor, holding a steel mace. Sharp eyes despite the 'Sick' moniker. Chinese historical drama style.","EP09","180cm","精干沉稳，军官体型","淡黄面庞，长髯阴郁","三十八岁"),
    ("宣赞","xuanzan",40,"地杰星·丑郡马","无","相貌丑陋，面如锅底，鼻孔朝天，卷发虬髯。身穿大红袍，外罩金甲，手持钢刀，相貌虽丑但气势威武。","He has an ugly face dark as a pot, upturned nostrils, curly hair and beard. Wearing a red robe and golden armor, holding a steel saber, majestic despite his looks. Chinese historical drama style.","EP09","182cm","粗壮威猛，武将体型","丑陋面庞，卷发虬髯","三十五岁"),
    ("郝思文","haosiwen",41,"地雄星·井木犴","无","面容端正，但眼神中带着一股执拗。头戴镔铁盔，身穿熟皮甲，手持长枪，一副标准的军官模样。","He has a proper face but eyes showing stubbornness. Wearing an iron helmet and leather armor, holding a long spear, a standard military officer. Chinese historical drama style.","EP09","178cm","端正结实，军官体型","端正面庞，执拗眼神","三十岁"),
    ("韩滔","hantao",42,"地威星·百胜将","甄力强","面相沉稳，留着短髭，眼神自信。头戴镔铁盔，身披连环铠，手持枣木槊，一副百战百胜的将军气派。","He has a composed face with a short mustache and confident eyes. Wearing an iron helmet and interlocking chainmail, wielding a jujube wood lance. Chinese historical drama style.","EP09","178cm","沉稳结实，将军体型","沉稳面庞，短髭自信","三十八岁"),
    ("彭玘","pengqi",43,"地英星·天目将","王春辉","面容威猛，浓眉大眼，眼神锐利。头戴凤翅金盔，身披黄金锁子甲，手持三尖两刃刀，威风凛凛。","He has a majestic face with thick eyebrows, large eyes, sharp gaze. Wearing a phoenix-wing golden helmet and golden chainmail, wielding a three-pointed blade. Chinese historical drama style.","EP09","180cm","威猛雄壮，武将体型","威猛面庞，浓眉锐利","三十五岁"),
    ("单廷珪","shantinggui",44,"地奇星·圣水将","无","面容阴鸷，留着短须，眼神透着狡诈。头戴黑漆盔，身穿玄色战袍，擅长水攻。","He has a sinister face with a short beard and cunning treacherous eyes. Wearing a black lacquered helmet and dark battle robe, expert in water warfare. Chinese historical drama style.","EP09","176cm","阴沉精干，将军体型","阴鸷面庞，短须狡诈","三十五岁"),
    ("魏定国","weidingguo",45,"地猛星·神火将","无","面色赤红，留着络腮胡，眼神中透着暴烈。头戴赤铜盔，身穿朱红战袍，擅长火攻。","He has a red flushed face with a full beard, eyes reflecting a violent temper. Wearing a red copper helmet and bright red battle robe, expert in fire attacks. Chinese historical drama style.","EP09","178cm","粗壮猛烈，将军体型","赤红面庞，络腮暴烈","三十三岁"),
    ("萧让","xiaorang",46,"地文星·圣手书生","无","面容清秀，气质儒雅，透着书卷气。头戴方巾，身穿白色长衫，一副饱读诗书的秀才模样。","He has a refined delicate face with a scholarly elegant aura. Wearing a square scholar's cap and white long robe, a well-educated scholar. Chinese historical drama style.","EP07","174cm","清瘦文雅，书生体型","清秀面庞，儒雅书卷","三十岁"),
    ("裴宣","peixuan",47,"地正星·铁面孔目","李文成","面色黝黑，神情严肃，不苟言笑，眼神刚正不阿。头戴乌纱帽，身穿绿色官袍，手持判官笔。","He has a dark swarthy face with a stern unsmiling expression. Firm, upright, incorruptible eyes. Wearing a black gauze cap and green official robe, holding a judge's brush. Chinese historical drama style.","EP07","176cm","端正严肃，官员体型","黝黑面庞，刚正严肃","四十岁"),
    ("欧鹏","oupeng",48,"地阔星·摩云金翅","无","身形瘦高，手臂极长，眼神锐利。身穿黄褐色劲装，手持长枪，动作敏捷，如大鹏展翅。","He has a tall thin build with extremely long arms and sharp keen eyes. Wearing a yellowish-brown martial outfit wielding a long spear, agile like a great hawk. Chinese historical drama style.","EP09","185cm","瘦高修长，游侠体型","瘦长面庞，锐利眼神","三十岁"),
    ("邓飞","dengfei",49,"地阖星·火眼狻猊","无","一双红眼，眼神凶恶，络腮胡。身穿深色劲装，手持铁链，气质暴躁，如凶兽一般。","He has a pair of reddish fiery eyes with a fierce aggressive gaze and a full beard. Wearing a dark martial outfit holding an iron chain, volatile like a wild beast. Chinese historical drama style.","EP09","176cm","粗壮暴烈，山寇体型","红眼凶恶，络腮暴躁","三十五岁"),
    ("燕顺","yanshun",50,"地强星·锦毛虎","杨林","赤发黄须，眼睛炯炯有神，面相凶悍。身穿虎皮袍子，手持朴刀，一副山大王的模样。","He has fiery red hair and a yellow beard, bright piercing eyes, fierce face. Wearing a tiger-skin robe holding a Pudao, every bit the bandit chief. Chinese historical drama style.","EP07","178cm","粗壮凶猛，山寇体型","赤发黄须，凶悍面庞","三十岁"),
    ("杨林","yanglin_hs",51,"地暗星·锦豹子","无","面色青黄，眼神飘忽，神情谨慎。身穿色彩斑斓的锦袍，手持长枪，走路悄无声息。","He has a greenish-yellow complexion and shifty wary eyes, cautious alert expression. Wearing a colorful brocade robe holding a long spear, moving silently. Chinese historical drama style.","EP07","174cm","精瘦谨慎，游侠体型","青黄面庞，飘忽谨慎","三十五岁"),
    ("凌振","lingzhen",52,"地轴星·轰天雷","无","面容粗犷，留着络腮胡，眼神专注。身穿短打衣衫，露出粗壮的手臂，手持火把，身边放着一尊铁炮。","He has a rough rugged face with a full beard and focused intent eyes. Wearing short workman's clothes showing thick arms, holding a torch with an iron cannon nearby. Chinese historical drama style.","EP09","176cm","粗壮结实，工匠体型","粗犷面庞，络腮专注","三十八岁"),
    ("蒋敬","jiangjing",53,"地会星·神算子","无","面容清癯，眼神精明，蓄着山羊胡。头戴方巾，身穿长衫，手持算盘，一副账房先生的模样。","He has a thin gaunt face with shrewd calculating eyes and a goatee. Wearing a scholar's cap and long robe holding an abacus, a meticulous accountant. Chinese historical drama style.","EP07","172cm","清瘦文弱，账房体型","清癯面庞，山羊胡精明","四十岁"),
    ("吕方","lvfang",54,"地佐星·小温侯","无","面容俊朗，年轻英武。头戴三叉束发紫金冠，身穿百花战袍，手持方天画戟，仿效三国吕布的打扮。","He has a handsome youthful face brimming with youthful heroism. Wearing a purple-gold crown and hundred-flower battle robe, holding a Fangtian Huaji halberd, imitating Lü Bu. Chinese historical drama style.","EP09","180cm","挺拔英俊，青年武将","俊朗面庞，年轻英武","二十二岁"),
    ("郭盛","guosheng",55,"地佑星·赛仁贵","无","与吕方打扮相似，也是白衣白甲，手持方天画戟，但气质上更显沉稳一些。","He looks similar to Lü Fang in white armor and robe, also holding a Fangtian Huaji, but with a more composed steady temperament. Chinese historical drama style.","EP09","180cm","挺拔沉稳，青年武将","端正面庞，沉稳气质","二十五岁"),
    ("安道全","andaoquan",56,"地灵星·神医","邢枫","面容清癯，蓄着长须，眼神专注而平和。头戴方巾，身穿青衫，手持药囊，一副悬壶济世的名医风范。","He has a thin gaunt face and long beard, focused calm eyes radiating peace. Wearing a scholar's cap and blue robe holding a medicine bag, a renowned physician. Chinese historical drama style.","EP08","174cm","清瘦文雅，医师体型","清癯面庞，长须平和","四十五岁"),
    ("皇甫端","huangfuduan",57,"地兽星·紫髯伯","无","长着一部紫色长髯，面容沉稳，眼神深邃。头戴毡帽，身穿兽皮袍，是技艺高超的兽医。","He has a lush distinctive purple beard. Calm steady face, deep profound eyes. Wearing a felt cap and animal-hide robe, an exceptionally skilled veterinarian. Chinese historical drama style.","EP08","176cm","结实沉稳，兽医体型","沉稳面庞，紫色长髯","四十岁"),
    ("王英","wangying",58,"地微星·矮脚虎","许敬义","身材矮小粗壮，相貌猥琐，眼神贪婪。身穿虎皮袍子，手持长枪，一副好色的山大王模样。","He has a short stout stature and a sleazy ugly face, eyes filled with greed and lust. Wearing a tiger-skin robe holding a long spear, a lecherous bandit chief. Chinese historical drama style.","EP07","150cm","矮小粗壮，山寇体型","猥琐面庞，贪婪眼神","三十五岁"),
    ("扈三娘","husanniang",59,"地慧星·一丈青","郑爽","面容姣好，眉宇间带着一股英气，气质冷艳。头戴花冠，身披黄金锁子甲，手持日月双刀，巾帼不让须眉。","She has a beautiful attractive face, but her brow carries a strong heroic spirit, cold aloof temperament. Wearing a floral headdress and golden chainmail, wielding dual sabers, a true warrior woman. Chinese historical drama style.","EP07","172cm","矫健挺拔，女将体型","姣好面庞，英气冷艳","二十岁"),
    ("鲍旭","baoxu",60,"地暴星·丧门神","无","相貌丑陋，面目狰狞，眼神中透着暴戾。身穿黑色战袍，手持一柄加长的阔剑，杀气腾腾。","He has an ugly hideous face with a ferocious terrifying expression, eyes filled with violent cruelty. Wearing a black battle robe wielding an extra-long wide-bladed sword. Chinese historical drama style.","EP09","178cm","粗壮凶暴，山寇体型","丑陋狰狞，暴戾眼神","三十岁"),
    ("樊瑞","fanrui",61,"地然星·混世魔王","无","披头散发，身穿道袍，面相凶恶，眼神中透着邪气。手持流星锤和混世魔王宝剑，会呼风唤雨。","He has disheveled wild hair wearing a Taoist robe. Fierce menacing face with evil occult gleaming eyes. Holding a meteor hammer and Demon King's sword, able to summon wind and rain. Chinese historical drama style.","EP08","178cm","修长阴森，道士体型","凶恶面庞，披发邪气","三十五岁"),
    ("孔明","kongming_hs",62,"地猖星·毛头星","无","面相年轻，神情张扬。头戴毡帽，身穿锦袍，手持钢枪，是孔家庄的少爷。","He has a young face with a wild arrogant expression. Wearing a felt cap and brocade robe holding a steel spear, young master of Kong Family Estate. Chinese historical drama style.","EP07","178cm","挺拔张扬，富家子弟","年轻面庞，张扬神情","二十二岁"),
    ("孔亮","kongliang",63,"地狂星·独火星","无","与哥哥孔明外貌相似，但气质更加急躁。同样身穿锦袍，手持钢刀，性如烈火。","He looks similar to his brother Kong Ming but temperament even more impatient fiery. Also wearing a brocade robe holding a steel saber, explosive as a flame. Chinese historical drama style.","EP07","176cm","挺拔急躁，富家子弟","年轻面庞，急躁神情","二十岁"),
    ("项充","xiangchong",64,"地飞星·八臂哪吒","无","身形精悍，面容凶狠。身背二十四把飞刀，手持团牌，行动如飞。","He has a lean wiry physique and fierce ruthless face. Carrying twenty-four flying daggers on his back holding a round shield, moving with extreme swiftness. Chinese historical drama style.","EP09","172cm","精悍敏捷，步军体型","凶狠面庞，精悍身形","三十岁"),
    ("李衮","ligun",65,"地走星·飞天大圣","无","身形敏捷，面容灵活。身背二十四根标枪，手持团牌，与项充是搭档，同样擅长投射。","He has a nimble agile build and clever alert face. Carrying twenty-four javelins on his back holding a round shield, partner of Xiang Chong. Chinese historical drama style.","EP09","172cm","精干敏捷，步军体型","灵活面庞，敏捷身形","二十八岁"),
    ("金大坚","jindajian",66,"地巧星·玉臂匠","无","面容专注，眼神锐利。头戴方巾，身穿匠人短褐，手持刻刀，正在雕刻印章。","He has a focused intent expression with sharp keen eyes. Wearing a scholar's cap and short artisan's work clothes, holding a carving knife engraving a seal. Chinese historical drama style.","EP07","170cm","精瘦专注，工匠体型","专注面庞，锐利眼神","四十岁"),
    ("马麟","malin",67,"地明星·铁笛仙","无","面容清秀，神情潇洒。身穿长衫，腰间插着一支铁笛，手持双刀，风度翩翩。","He has a refined elegant face with a free easygoing demeanor. Wearing a long robe with an iron flute at his waist, wielding dual swords, cultured and dashing. Chinese historical drama style.","EP09","174cm","清瘦潇洒，游侠体型","清秀面庞，潇洒神情","二十八岁"),
    ("童威","tongwei",68,"地进星·出洞蛟","朱晓春","皮肤黝黑，眼神精明。身穿短打水靠，手持分水峨眉刺，水性极好。","He has dark skin and shrewd calculating eyes. Wearing a short close-fitting aquatic outfit holding a pair of Emei piercers, a master swimmer. Chinese historical drama style.","EP08","174cm","精干结实，水军体型","黝黑面庞，精明眼神","三十岁"),
    ("童猛","tongmeng",69,"地退星·翻江蜃","王中伟","外貌与童威相似，但气质上更显沉稳一些。同样身穿水靠，手持分水刺。","He looks similar to Tong Wei but appears slightly calmer and more composed. Also wearing an aquatic outfit holding Emei piercers. Chinese historical drama style.","EP08","172cm","精干沉稳，水军体型","黝黑面庞，沉稳眼神","二十八岁"),
    ("孟康","mengkang",70,"地满星·玉幡竿","无","身材瘦高，面容白净。头戴斗笠，身穿短褐，手持斧凿，是技艺高超的造船匠。","He has a tall slender build and fair pale face. Wearing a bamboo hat and short work clothes, holding an axe and chisel, a highly skilled shipbuilder. Chinese historical drama style.","EP08","185cm","瘦高修长，工匠体型","白净面庞，瘦高身形","三十五岁"),
    ("侯健","houjian",71,"地遂星·通臂猿","无","身形瘦削，手臂极长，眼神灵动。身穿短褐，手持针线和剪刀，是飞针走线的裁缝。","He has a thin wiry frame with extremely long arms and nimble intelligent eyes. Wearing short work clothes, holding needle thread and scissors, a lightning-fast tailor. Chinese historical drama style.","EP07","168cm","瘦削灵巧，工匠体型","瘦削面庞，灵动眼神","三十岁"),
    ("陈达","chenda",72,"地周星·跳涧虎","无","面容粗犷，眼神凶悍。身穿虎皮袍子，手持点钢枪，是少华山的山大王。","He has a rough rugged face with a fierce aggressive gaze. Wearing a tiger-skin robe holding a steel-tipped spear, a bandit chief from Mount Shaohua. Chinese historical drama style.","EP07","178cm","粗壮凶猛，山寇体型","粗犷面庞，凶悍眼神","三十五岁"),
    ("杨春","yangchun",73,"地隐星·白花蛇","无","面容阴鸷，眼神狡诈。身穿白色战袍，手持大杆刀，是少华山的山大王。","He has a sinister gloomy face with cunning treacherous eyes. Wearing a white battle robe holding a long-handled broadsword, a bandit chief. Chinese historical drama style.","EP07","176cm","精干阴险，山寇体型","阴鸷面庞，狡诈眼神","三十二岁"),
    ("郑天寿","zhengtianshou",74,"地异星·白面郎君","刘立伟","面容白皙，长相英俊，但气质有些阴柔。头戴银冠，身穿白袍，手持吴钩剑，是清风山的山大王。","He has fair pale skin and a handsome face, but his temperament is somewhat effeminate. Wearing a silver headpiece and white robe wielding Wu hook swords. Chinese historical drama style.","EP07","176cm","挺拔俊美，山寇体型","白皙英俊，阴柔气质","二十八岁"),
    ("陶宗旺","taozongwang",75,"地理星·九尾龟","无","皮肤黝黑，身形粗壮，力大无穷。身穿麻布短褐，手持一把大铁锹，是农民出身的庄稼汉。","He has dark skin and a stout burly build, possessing immense strength. Wearing coarse hemp work clothes holding a large iron shovel, an honest farmer. Chinese historical drama style.","EP08","180cm","粗壮结实，农夫体型","黝黑面庞，粗壮力大","三十五岁"),
    ("宋清","songqing",76,"地俊星·铁扇子","李宝军","面容端正，眼神平和。头戴方巾，身穿长衫，手持账本，是宋江的弟弟，负责梁山后勤。","He has a proper upright face with calm peaceful eyes. Wearing a scholar's cap and long robe holding an account book, Song Jiang's younger brother in charge of logistics. Chinese historical drama style.","EP07","172cm","端正平和，文吏体型","端正面庞，平和眼神","三十五岁"),
    ("乐和","yuehe",77,"地乐星·铁叫子","无","面容机灵，眼神灵活，嘴角常带笑意。头戴小帽，身穿短褐，腰间插着一支笛子，是个聪明伶俐的小牢子。","He has a clever nimble face with lively intelligent eyes, a slight smile at the corner of his mouth. Wearing a small cap and short work clothes with a flute at his waist, a witty young jailer. Chinese historical drama style.","EP08","168cm","小巧灵巧，牢子体型","机灵面庞，灵活笑意","二十岁"),
    ("龚旺","gongwang",78,"地捷星·花项虎","无","身材健壮，满脖子刺青，眼神凶狠。身穿轻甲，手持飞枪，是没羽箭张清的副将。","He has a strong sturdy build with his neck completely covered in tattoos, fierce ruthless eyes. Wearing light armor holding a throwing spear, deputy general under Zhang Qing. Chinese historical drama style.","EP09","178cm","健壮凶猛，副将体型","凶狠面庞，满颈刺青","三十岁"),
    ("丁得孙","dingdesun",79,"地速星·中箭虎","无","脸颊上有一块明显的伤疤，眼神依旧坚定。同样身穿轻甲，手持飞叉，是张清的副将。","He has a prominent scar on his cheek, yet eyes remain steadfast and determined. Also wearing light armor holding a throwing trident, another deputy under Zhang Qing. Chinese historical drama style.","EP09","176cm","精干坚韧，副将体型","带疤面庞，坚定眼神","二十八岁"),
    ("穆春","muchun",80,"地镇星·小遮拦","无","面相年轻，神情张扬，眼神中带着一股狠劲。身穿锦袍，手持朴刀，是穆弘的弟弟。","He has a young face with an arrogant aggressive expression, eyes showing a streak of ruthlessness. Wearing a brocade robe holding a Pudao, Mu Hong's younger brother. Chinese historical drama style.","EP07","176cm","挺拔年轻，富家子弟","年轻面庞，张扬狠劲","二十岁"),
    ("曹正","caozheng",81,"地嵇星·操刀鬼","赵春明","面容精明，眼神锐利，透着商人气息。头戴毡帽，身穿油腻的围裙，手持屠刀，是林冲的徒弟，开酒店的。","He has a shrewd astute face with sharp penetrating eyes, carrying the air of a businessman. Wearing a felt cap and greasy butcher's apron holding a cleaver, Lin Chong's disciple running an inn. Chinese historical drama style.","EP07","172cm","精干结实，商人体型","精明面庞，锐利眼神","三十五岁"),
    ("宋万","songwan",82,"地魔星·云里金刚","胡龙吟","身材高大魁梧，面相憨厚。头戴范阳毡笠，身穿布袍，是梁山早期的元老。","He has a tall burly build with a simple honest face. Wearing a felt hat and cloth robe, one of the earliest founders of Liangshan. Chinese historical drama style.","EP07","188cm","高大魁梧，元老体型","憨厚面庞，高大身形","四十岁"),
    ("杜迁","duqian",83,"地妖星·摸着天","钱卫东","同样身材高大，但气质上比宋万更精明一些。头戴毡笠，身穿长袍，是梁山早期的元老。","He is also very tall but appears slightly more shrewd and alert than Song Wan. Wearing a felt hat and long robe, another early founder of Liangshan. Chinese historical drama style.","EP07","190cm","高大精明，元老体型","精明面庞，高大身形","四十二岁"),
    ("薛永","xueyong",84,"地幽星·病大虫","无","面容消瘦，脸色蜡黄，眼神无光。身穿旧布袍，在街头卖艺为生，但身手不凡。","He has a thin gaunt face with a sickly sallow complexion and dull listless eyes. Wearing old worn cloth robes, making a living performing martial arts on the street, yet genuine skills. Chinese historical drama style.","EP07","176cm","瘦削病态，游侠体型","消瘦蜡黄，眼神无光","三十五岁"),
    ("施恩","shien",85,"地伏星·金眼彪","常玉平","面容白净，眼神精明，透着江湖气。身穿锦袍，是孟州牢城管营的公子。","He has a fair pale face and shrewd calculating eyes, exuding an underworld aura. Wearing a brocade robe, son of the prison camp commandant in Mengzhou. Chinese historical drama style.","EP07","172cm","端正结实，富家子弟","白净面庞，精明江湖","二十八岁"),
    ("李忠","lizhong",86,"地僻星·打虎将","无","面容粗犷，神情朴实。头戴毡帽，身穿短褐，手持长枪，是史进的启蒙师傅。","He has a rough rugged face with a simple honest expression. Wearing a felt hat and short work clothes holding a long spear, Shi Jin's first martial arts teacher. Chinese historical drama style.","EP07","178cm","粗壮朴实，武师体型","粗犷面庞，朴实神情","四十岁"),
    ("周通","zhoutong",87,"地空星·小霸王","无","面相凶恶，络腮胡，眼神霸道。头戴金盔，身穿绿袍，手持长枪，是桃花山的山大王。","He has a fierce ugly face with a full beard and overbearing domineering eyes. Wearing a golden helmet and green robe holding a long spear, bandit chief of Mount Taohua. Chinese historical drama style.","EP07","178cm","粗壮霸道，山寇体型","凶恶面庞，络腮霸道","三十岁"),
    ("汤隆","tanglong",88,"地孤星·金钱豹子","无","面色蜡黄，满脸麻子，眼神专注。身穿短褐，手持铁锤，是技艺高超的铁匠。","He has a sallow waxy complexion with a face full of pockmarks, focused intent eyes. Wearing short work clothes holding a blacksmith's hammer, a highly skilled ironsmith. Chinese historical drama style.","EP07","174cm","精瘦结实，工匠体型","蜡黄麻脸，专注眼神","三十五岁"),
    ("杜兴","duxing",89,"地全星·鬼脸儿","无","面容丑陋，颧骨高耸，眼神却透着一股精明。身穿短褐，是李应的管家。","He has an ugly hideous face with high prominent cheekbones, yet eyes reveal sharp shrewd intelligence. Wearing short work clothes, serving as Li Ying's steward. Chinese historical drama style.","EP07","172cm","精干结实，管家体型","丑陋面庞，高耸颧骨精明","三十岁"),
    ("邹渊","zouyuan",90,"地短星·出林龙","无","面相凶狠，络腮胡，眼神大胆。身穿兽皮袍，手持大斧，是登云山的山大王。","He has a fierce ruthless face with a full beard and bold daring eyes. Wearing an animal-hide robe holding a large axe, bandit chief of Mount Dengyun. Chinese historical drama style.","EP09","178cm","粗壮大胆，山寇体型","凶狠面庞，络腮大胆","三十五岁"),
    ("邹润","zourun",91,"地角星·独角龙","无","头大如斗，脑后长着一个肉瘤，眼神凶悍。身穿兽皮袍，手持大斧，是邹渊的侄儿。","He has a large head with a fleshy knob growing from the back of his skull. Fierce aggressive eyes. Wearing an animal-hide robe holding a large axe, Zou Yuan's nephew. Chinese historical drama style.","EP09","180cm","粗壮凶悍，山寇体型","大头肉瘤，凶悍眼神","二十八岁"),
    ("朱贵","zhugui",92,"地囚星·旱地忽律","张连仲","面容沉稳，眼神机警。头戴毡帽，身穿布袍，在梁山脚下开酒店，打探消息。","He has a composed steady face with alert watchful eyes. Wearing a felt cap and cloth robe, running an inn at the foot of Liangshan to gather intelligence. Chinese historical drama style.","EP07","174cm","精干沉稳，探子体型","沉稳面庞，机警眼神","四十岁"),
    ("朱富","zhufu",93,"地藏星·笑面虎","程思寒","面容和气，眼神中却透着精明。头戴小帽，身穿围裙，是朱贵的弟弟，开酒店的。","He has an amiable friendly face, yet eyes reveal a shrewd calculating nature. Wearing a small cap and apron, Zhu Gui's younger brother, also running an inn. Chinese historical drama style.","EP07","170cm","精干和气，商人体型","和气面庞，精明眼神","三十五岁"),
    ("蔡福","caifu",94,"地平星·铁臂膊","邢国洲","面容阴沉，双臂粗壮有力。身穿红衣，手持鬼头大刀，是大名府的刽子手。","He has a gloomy dark face with extremely thick powerful arms. Wearing a red executioner's uniform holding a large ghost-headed broadsword, executioner of Daming Prefecture. Chinese historical drama style.","EP07","178cm","粗壮阴沉，刽子体型","阴沉面庞，粗壮双臂","三十八岁"),
    ("蔡庆","caiqing",95,"地损星·一枝花","陈长龙","外貌与蔡福相似，但喜欢在鬓边插一朵花，气质更显轻浮。同样身穿红衣，手持鬼头刀。","He looks similar to Cai Fu but likes to wear a flower tucked behind his ear, temperament more frivolous. Also wearing a red uniform holding a ghost-headed broadsword. Chinese historical drama style.","EP07","176cm","粗壮轻浮，刽子体型","阴沉面庞，鬓边插花","三十六岁"),
    ("李立","lili",96,"地奴星·催命判官","无","面容凶狠，眼神毒辣。身穿短褐，在揭阳岭上开黑店，是催命的判官。","He has a fierce ruthless face with venomous malicious eyes. Wearing short work clothes, running an inn at Jieyang Ridge that is a front for murder. Chinese historical drama style.","EP07","172cm","精干凶狠，黑店体型","凶狠面庞，毒辣眼神","三十五岁"),
    ("李云","liyun",97,"地察星·青眼虎","无","面色青黄，眼神锐利。身穿官袍，手持朴刀，是沂水县的都头。","He has a greenish-yellow complexion and sharp penetrating eyes. Wearing a constable's uniform holding a Pudao, chief constable of Yishui County. Chinese historical drama style.","EP07","176cm","精干锐利，军官体型","青黄面庞，锐利眼神","三十八岁"),
    ("焦挺","jiaoting",98,"地恶星·没面目","魏峰","面相凶恶，身材粗壮。身穿短褐，以相扑为生，到处投人不着，所以叫'没面目'。","He has a fierce ugly face and a stout burly build. Wearing short work clothes, making a living as a sumo wrestler, always getting rejected hence 'Faceless'. Chinese historical drama style.","EP07","178cm","粗壮结实，力士体型","凶恶面庞，粗壮身材","三十岁"),
    ("石勇","shiyong",99,"地丑星·石将军","无","面容普通，但神情坚定。身穿布袍，在大名府以放赌为生，因打死人命而出逃。","He has a plain unremarkable face but a resolute determined expression. Wearing cloth robes, making a living gambling in Daming Prefecture, fleeing after killing a man. Chinese historical drama style.","EP07","174cm","普通结实，赌徒体型","普通面庞，坚定神情","二十八岁"),
    ("孙新","sunxin",100,"地数星·小尉迟","张卫国","面容与哥哥孙立相似，但气质更年轻、更有朝气。头戴毡帽，身穿锦袍，是孙立的弟弟。","He looks similar to his brother Sun Li but temperament is younger and more spirited. Wearing a felt cap and brocade robe, Sun Li's younger brother. Chinese historical drama style.","EP07","178cm","挺拔精神，富家子弟","端正面庞，年轻朝气","二十八岁"),
    ("顾大嫂","gudasao",101,"地阴星·母大虫","张秀岩","面容粗犷，身材壮硕，眼神凶悍。头戴巾帼，身穿粗布衣裙，手持双刀，是梁山上为数不多的女将。","She has a rough coarse face and a stout sturdy build, fierce intimidating eyes. Wearing a simple woman's headscarf and rough clothes wielding dual sabers, one of the few female warriors on Liangshan. Chinese historical drama style.","EP07","168cm","壮硕粗犷，女将体型","粗犷面庞，凶悍眼神","三十岁"),
    ("张青","zhangqing_shop",102,"地刑星·菜园子","张昕","面容朴实，眼神中透着精明。头戴斗笠，身穿粗布短褐，在十字坡开黑店。","He has a simple honest face, yet eyes reveal shrewd calculating intelligence. Wearing a bamboo hat and coarse short work clothes, running the inn at Cross Slope with his wife. Chinese historical drama style.","EP07","174cm","精干朴实，商人体型","朴实面庞，精明眼神","三十五岁"),
    ("孙二娘","sunerniang",103,"地壮星·母夜叉","梁丽","面容艳丽，但眼神狠辣，透着一股风尘气。头戴红花，身穿鲜艳的衣裙，是张青的妻子，在十字坡开黑店。","She has a seductive alluring face, but ruthless sharp eyes exuding a worldly experienced air. Wearing a red flower in her hair and brightly colored clothing, wife of Zhang Qing running the inn at Cross Slope. Chinese historical drama style.","EP07","166cm","丰艳狠辣，黑店体型","艳丽面庞，狠辣风尘","二十八岁"),
    ("王定六","wangdingliu",104,"地劣星·活闪婆","无","身形瘦小，行动敏捷，眼神灵活。身穿短褐，是扬子江边的酒店伙计，水性极好。","He has a small skinny build but moves with extreme agility, nimble alert eyes. Wearing short work clothes, working as a tavern waiter by the Yangtze River, an expert swimmer. Chinese historical drama style.","EP08","165cm","瘦小敏捷，伙计体型","瘦小面庞，灵活眼神","二十四岁"),
    ("郁保四","yubaosi",105,"地健星·险道神","无","身材极其高大，面相憨厚。身穿布袍，手持大斧，是曾头市出身的好汉，负责扛帅旗。","He is extremely tall and large in stature with a simple honest face. Wearing cloth robes holding a large axe, originally from Zeng Family Fortress, responsible for carrying the commander's banner. Chinese historical drama style.","EP09","195cm","极其高大，扛旗体型","憨厚面庞，极其高大","三十岁"),
    ("白胜","baisheng",106,"地耗星·白日鼠","孙明月","面容猥琐，眼神飘忽。身穿破烂布袍，是闲汉出身，在智取生辰纲中扮演重要角色。","He has a sleazy vulgar face with shifty evasive eyes. Wearing tattered worn cloth robes, an idle loafer who played a key role in the 'Scheme of the Birthday Gift'. Chinese historical drama style.","EP06","168cm","瘦小猥琐，闲汉体型","猥琐面庞，飘忽眼神","三十岁"),
    ("时迁","shiqian",107,"地贼星·鼓上蚤","孟耿成","身材瘦小，尖嘴猴腮，眼神机警。身穿黑色夜行衣，行动灵活，是梁山第一神偷。","He has a small skinny build with a pointed monkey-like face and alert cautious eyes. Wearing a black nighttime stealth outfit, moving with extreme agility, the number one thief on Liangshan. Chinese historical drama style.","EP06","162cm","瘦小灵巧，盗贼体型","尖嘴猴腮，机警灵活","二十八岁"),
    ("段景住","duanjingzhu",108,"地狗星·金毛犬","无","赤发黄须，眼神忠诚。身穿皮袍，以盗马为生，后来投奔梁山。","He has reddish hair and a yellow beard, eyes showing loyalty and devotion. Wearing an animal-hide robe, making a living by stealing horses, later seeking refuge at Liangshan. Chinese historical drama style.","EP06","174cm","精瘦结实，马贼体型","赤发黄须，忠诚眼神","二十五岁"),
    ("晁盖","chaogai",109,"托塔天王","无","宽额浓眉，三绺黑白胡须，目光精算。深紫色丝绸锦袍配刺绣，玉饰发带；伪装时为粗布衣斗笠。","A dignified Chinese village chief turned outlaw mastermind, 40 years old, broad forehead, thick eyebrows, long three-strand black-grey beard, calculating intelligent eyes, wearing dark purple silk robe with embroidery and jade ornament headband. Chinese historical drama epic style.","EP06","180cm","宽厚壮实，领袖体型","宽额浓眉，三绺胡须","四十岁"),
]

def gen_pinyin(name):
    """Simple pinyin mapping from CHAR_MAP keys."""
    mapping = {c[0]: c[1] for c in CHARS}
    return mapping.get(name, name.lower())

# Build character_designs.json
def build_designs():
    chars = []
    for c in CHARS:
        name, pinyin, rank, nickname, actor, cn_desc, en_prompt, ep, height, build, face, age = c
        chars.append({
            "name": name,
            "star_rank": rank,
            "star_name": nickname,
            "actor": actor if actor != "无" else None,
            "profile": {
                "description": cn_desc[:80],
                "props": "",
                "face": face
            },
            "prompt_cn": cn_desc,
            "prompt_en": en_prompt,
            "episode": ep,
            "generation": {"status": "pending", "error": None},
            "created_at": datetime.now().isoformat()
        })
    return {"project": "水浒传", "generated_at": datetime.now().isoformat(), "mode": "real", "total": len(chars), "characters": chars}

# Build visual_bible.json
def build_bible():
    bible = {"version": "1.1", "project": "水浒传 AI 数字短剧", "total_characters": len(CHARS), "generated_for": "fal.ai Seedance / Stable Diffusion / Wan 2.5", "style_guidelines": {"era": "北宋徽宗年间 (1100-1126 AD)", "visual_style": "cinematic realism, muted earth tones, dramatic lighting, Zhang Yimou film aesthetic mixed with classical Chinese painting", "aspect_ratio": "16:9 horizontal", "resolution": "1920x1080 or higher", "consistency_rules": ["每个角色在全部镜头中外观一致", "同一角色的服装/发型/面部特征不得改变", "背景符合宋风 — 无现代化元素", "光线自然，避免过度HDR"]}, "characters": {}}
    
    # Import existing characters from visual_bible.json if available
    existing_bible = {}
    try:
        with open("/Users/hokeli/.agentic-os/character_designs/visual_bible.json", "r") as f:
            existing_bible = json.load(f)
    except:
        pass
    
    for c in CHARS:
        name, pinyin, rank, nickname, actor, cn_desc, en_prompt, ep, height, build, face, age = c
        
        # Color palette generation based on character type
        palettes = {
            "将领": ["#c0392b", "#2e5098", "#d4a574"],
            "文官": ["#2e7d32", "#795548", "#ffd700"],
            "书生": ["#1565c0", "#c0a060", "#f5f0e8"],
            "道士": ["#8B6914", "#c4a35a", "#e8d5a3"],
            "僧人": ["#8B6914", "#c4a35a", "#e8d5a3"],
            "渔民": ["#1a3a1a", "#4a0080", "#d4a574"],
            "猎户": ["#2d5016", "#1c3a6e", "#8b7355"],
            "山寇": ["#37474f", "#c62828", "#8b7355"],
            "工匠": ["#5d4037", "#8d6e63", "#d4a574"],
            "女将": ["#c0392b", "#8b0000", "#d4a574"],
            "官员": ["#2e7d32", "#795548", "#ffd700"],
            "商人": ["#4a0080", "#8b7355", "#d4a574"],
            "水军": ["#1a3a1a", "#2e5098", "#d4a574"],
            "盗贼": ["#37474f", "#1a1a2e", "#8b7355"],
            "闲汉": ["#5d4037", "#795548", "#8d6e63"],
        }
        
        # Determine category
        cat = "将领"  # default
        if any(k in nickname for k in ["智多星", "神机", "圣手书生", "铁扇子"]):
            cat = "书生"
        elif any(k in nickname for k in ["入云龙", "混世魔王"]):
            cat = "道士"
        elif any(k in nickname for k in ["花和尚"]):
            cat = "僧人"
        elif any(k in nickname for k in ["立地太岁", "船火儿", "短命二郎", "浪里白条", "活阎罗", "出洞蛟", "翻江蜃", "混江龙", "活闪婆"]):
            cat = "渔民" if any(k in nickname for k in ["立地太岁", "船火儿", "短命二郎", "活阎罗", "混江龙"]) else "水军"
        elif any(k in nickname for k in ["两头蛇", "双尾蝎"]):
            cat = "猎户"
        elif any(k in nickname for k in ["锦毛虎", "白花蛇", "跳涧虎", "中箭虎", "花项虎", "插翅虎", "霹雳火", "赤发鬼", "毛头星", "独火星"]):
            cat = "山寇"
        elif any(k in nickname for k in ["玉臂匠", "轰天雷", "通臂猿", "九尾龟", "金钱豹子"]):
            cat = "工匠"
        elif any(k in nickname for k in ["一丈青", "母大虫", "母夜叉"]):
            cat = "女将"
        elif any(k in nickname for k in ["及时雨", "铁面孔目", "病关索", "美髯公"]):
            cat = "官员"
        elif any(k in nickname for k in ["菜园子", "笑面虎", "旱地忽律", "操刀鬼", "神算子"]):
            cat = "商人"
        elif any(k in nickname for k in ["鼓上蚤", "金毛犬", "白日鼠"]):
            cat = "盗贼"
        elif any(k in nickname for k in ["白日鼠", "铁叫子"]):
            cat = "闲汉"
        
        palette = palettes.get(cat, palettes["将领"])
        
        # Check if this character already exists with richer data
        existing = existing_bible.get("characters", {}).get(pinyin)
        
        if existing:
            # Keep existing rich data, just update the prompt
            char_data = existing
            char_data["prompt_en"] = en_prompt
            char_data["episode"] = ep
        else:
            char_data = {
                "id": pinyin,
                "name": name,
                "star_rank": rank,
                "star_name": nickname,
                "title": nickname.split("·")[-1] if "·" in nickname else nickname,
                "actor": actor if actor != "无" else None,
                "episode": ep,
                "basic_info": {"height": height, "build": build, "face": face, "age": age},
                "appearance": {
                    "costume": cn_desc[:60],
                    "color_palette": {"primary": palette[0], "secondary": palette[1], "accent": palette[2]},
                    "design_notes": f"基于98版水浒传{actor if actor != '无' else '原著描述'}塑造"
                },
                "personality": {"core_traits": [], "emotional_range": "", "speech_style": "", "catchphrases": [], "habits": []},
                "prompt_en": en_prompt,
                "renders": [],
                "_updated_at": datetime.now().isoformat(),
            }
        
        bible["characters"][pinyin] = char_data
    
    bible["total_characters"] = len(bible["characters"])
    return bible

if __name__ == "__main__":
    # Generate character_designs.json
    designs = build_designs()
    os.makedirs("/Users/hokeli/.agentic-os/character_designs", exist_ok=True)
    with open("/Users/hokeli/.agentic-os/character_designs/character_designs.json", "w") as f:
        json.dump(designs, f, ensure_ascii=False, indent=2)
    print(f"✅ character_designs.json: {designs['total']} characters")
    
    # Generate visual_bible.json
    bible = build_bible()
    with open("/Users/hokeli/.agentic-os/character_designs/visual_bible.json", "w") as f:
        json.dump(bible, f, ensure_ascii=False, indent=2)
    print(f"✅ visual_bible.json: {bible['total_characters']} characters")
    
    # Verify
    print(f"\n📊 Summary:")
    print(f"  character_designs.json: {designs['total']} heroes")
    print(f"  visual_bible.json: {bible['total_characters']} heroes")
    print(f"  36 Heavenly Spirits + 72 Earthly Fiends + 晁盖 = 109 total")
