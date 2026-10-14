# 天气数据怎么取

数据源只有一个：Open-Meteo，网址 `https://open-meteo.com`。免费，不用注册，不用密钥，不用装任何东西，一条命令就能拿到。

## 一条命令拿七天预报

把下面这条复制走，改经纬度就是换城市（经纬度怎么查在最后）：

```bash
curl -s "https://api.open-meteo.com/v1/forecast?latitude=39.9075&longitude=116.3972&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=Asia%2FShanghai&forecast_days=7"
```

命令里每一段是什么意思：

- `latitude`、`longitude`：要查的地方的经纬度。例子里是北京的。
- `current=...`：要现在的实况，后面跟的四个是温度、湿度、天气代码、风速。
- `daily=...`：要每天的汇总，后面跟的是天气代码、最高温、最低温、最大降雨概率。
- `timezone=Asia%2FShanghai`：按北京时间算每一天。写错了，日期会差一天。
- `forecast_days=7`：要未来 7 天。跟配置里的 `forecast_days` 对上。

## 返回里的字段都是什么意思

返回是一份 JSON，就是带名字的数字清单。写稿要用的是这几块：

- `current.time`：这份实况的时间。先看它，确认是刚刚的，不是旧的。
- `current.temperature_2m`：现在的温度，单位是度。
- `current.relative_humidity_2m`：现在的湿度，百分之多少。
- `current.weather_code`：现在的天气代码，是个数字，要照下面的对照表换成中文。
- `current.wind_speed_10m`：现在的风速，单位是公里每小时。
- `daily.time`：日期列表，从今天开始，一天一个。
- `daily.weather_code`：每天的天气代码，跟日期列表一个位置对一天。
- `daily.temperature_2m_max`：每天的最高温，跟日期一个位置对一天。
- `daily.temperature_2m_min`：每天的最低温，同上。
- `daily.precipitation_probability_max`：每天最大的降雨概率，百分之多少，同上。

认数据的办法就一条：几个列表是并排的，第几个位置就是同一天。写稿的时候按位置取，别串行。

## 天气代码对照表

代码是世界气象组织定的，常用的就这些：

| 代码 | 中文 |
|---|---|
| 0 | 晴 |
| 1 | 大致晴 |
| 2 | 多云 |
| 3 | 阴 |
| 45、48 | 有雾 |
| 51、53、55 | 毛毛雨 |
| 61、63、65 | 下雨（小到大） |
| 66、67 | 冻雨 |
| 71、73、75 | 下雪（小到大） |
| 77 | 雪粒 |
| 80、81、82 | 阵雨（小到大） |
| 85、86 | 阵雪 |
| 95 | 雷雨 |
| 96、99 | 雷雨带冰雹 |

碰上表里没有的代码，就写「天气多变」，别自己猜。

## 经纬度怎么查

换城市的时候用这个接口查，输城市名就行：

```bash
curl -s "https://geocoding-api.open-meteo.com/v1/search?name=Beijing&count=1&language=zh&format=json"
```

返回里 `results` 第一个就是这个城市，`latitude` 和 `longitude` 抄进配置。`name` 后面可以填拼音或英文名。同名城市有好几个的，看返回里的省份对不对，再抄。

## 取不到怎么办

命令报错、返回是空的、或者数明显不对（温度离谱、降雨概率超过 100），就算取失败。先看网络，再把命令原样重跑一次。还不行就停这一天，宁可不发。规矩在 `stages-diff.md` 里写死了：不许拿旧数据冒充当天的。
