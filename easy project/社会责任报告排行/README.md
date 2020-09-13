涉及一个简单的反爬

这个项目请求接口的时候会发现有点不一样，他返回的格式像是json，但是又不是json，一眼就能看出类似json，但是用`json.loads`根本解析不了

最开始我也比较懵逼，如果手动解析，当场烦死，所以我找了找，找到一个包 `demjson`

可以参考我的这篇博客：https://www.cnblogs.com/aduner/p/13157999.html

