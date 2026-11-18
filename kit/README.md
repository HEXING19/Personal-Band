# 何19个人品牌素材包

这套素材用于 PPT、视频、图文和个人资料。署名用在封面、开场或结尾的空角。图表、正文和字幕可沿用各期内容自己的样式。

[下载整个仓库 ZIP](https://github.com/HEXING19/Personal-Band/archive/refs/heads/main.zip) · [品牌使用规范](../BRAND-GUIDE.md) · [查看平台模板预览](../previews/kit-overview.png)

## 从一份新内容开始

1. **先选画幅。** 演示用 16:9 PPT，B 站横屏用 1920 × 1080，小红书视频用 1080 × 1920，小红书图文用 1080 × 1440。尺寸是本素材包的工作画幅。
2. **复制源文件再编辑。** 用 PowerPoint 或 WPS 打开对应 PPTX，保留需要的页，替换示例标题、副标题、图片与来源。导出封面时选当前页，检查生成的 PNG 像素；需要调整时按原比例缩放。
3. **只在需要署名时放角标。** 视频先设好工程画幅，再在开场叠加同画幅、同底色的角标。PPT 可以直接沿用封面和结束页现成的署名。
4. **先预览再发。** 用手机查看封面的裁切效果、角标和字幕的位置。演示稿按放映大小看一遍，确认占位文字已替换。

## 头像与署名

| 需要什么 | 文件 |
| --- | --- |
| 社媒头像 | [1024 × 1024 方形头像](identity/avatar-square.png) |
| 在封面或 PPT 里摆放头像 | [透明底圆形头像](identity/avatar-transparent.png) |
| 浅色画面角落 | [深蓝字透明署名](identity/signature-light.png) |
| 深色画面角落 | [浅色字透明署名](identity/signature-dark.png) |
| 统一查看色板、字体和角标署名 | [品牌资产总览](../output/he19-brand-assets.png) |

头像沿用此前试排版人物图。颜色、字体和署名比例可对照使用规范。

## PPT 与图文组件

[可编辑的 16:9 PPTX](presentation/he19-template.pptx) · [八页总览](../previews/kit-ppt.png)

| 版式 | PNG |
| --- | --- |
| 封面与章节页 | [封面](presentation/cover.png) · [章节](presentation/chapter.png) |
| 正文与图表 | [正文](presentation/text.png) · [图表和来源标注](presentation/chart.png) |
| 图片与引用 | [图片、图注与来源](presentation/photo.png) · [引用](presentation/quote.png) |
| 代码和结束页 | [代码](presentation/code.png) · [结束](presentation/closing.png) |

打开 PPTX 后，复制想用的页。标题和说明可以直接编辑，图表可通过「编辑数据」替换示例值。图片页可删除占位框再插入图片。整套正文版式用中性色，署名在封面和结束页。

## B 站横屏与小红书竖屏

以下为工作尺寸。上传前以平台实际预览为准，检查封面在推荐流、主页或播放器里是否被裁切。

| 用途 | 可编辑源文件 | PNG |
| --- | --- | --- |
| B 站横屏 · 1920 × 1080 | [PPTX](bilibili/horizontal.pptx) | [封面](bilibili/cover.png) · [开场](bilibili/opening.png) · [片尾](bilibili/ending.png) |
| 小红书竖屏 · 1080 × 1920 | [PPTX](xiaohongshu/vertical-video.pptx) | [封面](xiaohongshu/video-cover.png) · [开场](xiaohongshu/video-opening.png) · [片尾](xiaohongshu/video-ending.png) |
| 小红书图文 · 1080 × 1440 | [PPTX](xiaohongshu/post-cover.pptx) | [帖子封面](xiaohongshu/post-cover.png) · [观点卡](xiaohongshu/post-quote.png) |

封面用 PPTX 替换标题和图片，再导出对应像素的 PNG。水平或垂直居中裁切时，尽量让标题和主体留在预览看得到的位置。PNG 样张中的示例文案和占位框可对照源文件替换后再发布。

## 剪辑叠加和字幕

1. 先导入主视频，再选同画幅的角标。判断深浅底时，看角标所在区域的颜色。
2. 把角标拖到主视频上方的轨道，对齐开场起点。这里的 PNG 和 MOV 都是全画幅透明图层，按原尺寸居中对齐，角标本身已经摆在边角。
3. MOV 自带 3 秒淡入淡出。若导入后出现黑底或软件无法识别透明通道，改用同名 PNG，时长设为约 3 秒，再加淡入和淡出。
4. 暂停在开场和字幕首次出现的位置检查。若角标压住内容，可改用「头像与署名」里的小尺寸透明 PNG 手动摆放，或省略该次署名。

| 画幅与底色 | 静态 PNG | 3 秒透明 MOV |
| --- | --- | --- |
| 横屏浅底 · 右上角 | [PNG](video/corner-horizontal-light.png) | [MOV](video/corner-horizontal-light.mov) |
| 横屏深底 · 右上角 | [PNG](video/corner-horizontal-dark.png) | [MOV](video/corner-horizontal-dark.mov) |
| 竖屏浅底 · 左上侧 | [PNG](video/corner-vertical-light.png) | [MOV](video/corner-vertical-light.mov) |
| 竖屏深底 · 左上侧 | [PNG](video/corner-vertical-dark.png) | [MOV](video/corner-vertical-dark.mov) |

[示例 SRT](video/subtitle-example.srt) 可导入支持 SRT 的剪辑软件。内含示例时间轴，换成自己的台词和时间即可。[横屏 ASS](video/subtitle-horizontal.ass) 和 [竖屏 ASS](video/subtitle-vertical.ass) 提供带描边的排版样式。SRT 保存文字和时间，导入后可手动设为白色字、深色描边。ASS 也保存样式，需用支持 ASS 的软件保留排版。竖屏用成片预览检查字幕是否避开底部界面。

## 社媒、文字与线下

| 资产 | 可编辑文件 | 导出文件 |
| --- | --- | --- |
| 方形个人简介图 · 1080 × 1080 | [PPTX](social/profile-card.pptx) | [PNG](social/profile-card.png) |
| 通用主页横幅 · 1920 × 600 | [PPTX](social/profile-banner.pptx) | [PNG](social/profile-banner.png) |
| 一句话、长短简介、讲者介绍、视频开场和发布简介 | [文案 Markdown](copy/PROFILE-COPY.md) | 直接复制文字 |
| 讲者介绍页 · 16:9 | [PPTX](print/speaker-intro.pptx) | [PNG](print/speaker-intro.png) · [PDF](print/speaker-intro.pdf) |
| 双面名片 · 90 × 54 mm | [PPTX](print/business-card.pptx) | [PDF](print/business-card.pdf) |
| 活动胸牌 · 90 × 60 mm | [PPTX](print/event-badge.pptx) | [PDF](print/event-badge.pdf) |
| 头像贴纸 · 50 mm 方形画布 | [PPTX](print/avatar-sticker.pptx) | [透明 PNG · 300 dpi](print/sticker-50mm.png) · [PDF](print/avatar-sticker.pdf) |

横幅的人像和署名放在中间，上传后检查两侧裁切。名片和胸牌先填写真实联系方式、活动名称或现场身份，再导出下单。PDF 使用标注的成品画布尺寸。出血、色彩模式与贴纸刀线按印厂要求补充。

## 重新生成

[PPTX 和导出图片生成脚本](../source/make_brand_kit.py) 使用 Python、python-pptx、Pillow、LibreOffice 和 pdftoppm。[视频叠加生成脚本](../source/make_video_overlays.py) 使用 Python、Pillow 和 FFmpeg。按此顺序运行。PPTX 也可以在 PowerPoint 或 WPS 中打开并修改。
