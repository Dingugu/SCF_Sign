## 集成签到
集成签到，可加入腾讯云SCF云函数，也可修改部分代码直接运行

### 一、功能：
* 1.集成爱奇艺、腾讯视频、芒果tv、网易云音乐、天翼网盘、52破解论坛、精易论坛、乐易论坛的签到  

> a.爱奇艺：签7天奖1天，14天奖2天，28天奖7天；日常任务；随机成长值  
  b.腾讯视频：VIP签到两次获取成长值  
  c.芒果TV：连签21天，得15天体验会员；对应积分  
  d.网易云音乐：签到、300首歌单打卡  
  e.天翼云盘：签到、抽奖获取空间  
  f.吾爱破解论坛：2吾爱币  
  g.乐易论坛：随机易币、金币  
  h.精易论坛：随机精币  
 
* 2.支持多账户签到
* 3.支持添加酷推QQ推送

### 二、使用：
* 1.修改添加config.json相关参数，多账户在对应项目列表下添加字典参数即可
* 2.打包成zip文件，上传至scf云函数
* 3.添加定时触发器  
PS：若本机环境运行，将index.py的`def main_handler(event, context):`一行改为`if __name__ == '__main__':`，运行index.py

### 三、配置config.json
* 1.Skey为[酷推](https://cp.xuthus.cc)密钥
* 2.[爱奇艺（IQIYI）](https://iqiyi.com/)官网，浏览器F12打开开发者工具并刷新，直接搜索P00001
* 3.[腾讯视频（TX）](https://v.qq.com/)官网，浏览器F12开发者工具并刷新，找到请求**access.video.qq.com/user/auth_refresh**，params为?后字符串，cookies为请求cookies（可仅提取关键参数）
* 4.[芒果TV（MGO）]APP端，抓包获取url关键词**credits.bz.mgtv.com/user/creditsTake**，提取?后所有参数
* 5.[网易云音乐（WYY）](https://music.163.com/)，填入账号、密码  
  *注：接用第三方接口*
* 6.[天翼云盘（ECLOUD）](https://cloud.189.cn/)，填入账号、密码
* 7.[吾爱破解（52PJ）](https://www.52pojie.cn/)网站，抓取cookies中关键参数**htVD_2132_saltkey、htVD_2132_auth**
* 8.[乐易论坛（LEY）](https://www.leybc.com/)网站，抓取cookise中关键参数**2vlT_96d0_saltkey、2vlT_96d0_auth**
* 9.[精易论坛（BBS）](https://bbs.125.la/)网站，抓取cookies中关键参数**lDlk_ecc9_saltkey、lDlk_ecc9_auth**
