"""Generate editable PowerPoint templates and export the He19 brand kit."""
from pathlib import Path
from shutil import copyfile
from subprocess import run
from tempfile import TemporaryDirectory

from PIL import Image, ImageOps
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.xmlchemy import OxmlElement
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / 'kit'
AVATAR = ROOT / 'output/he19-avatar-preview.png'
NAVY = '14213A'
MUTED = '4B5A71'
WHITE = 'FFFFFF'
PAPER = 'F7F8FA'
LINE = 'DDE3EC'
PINK = 'F8DDD8'
ORANGE = 'FFAE36'
FONT = 'Noto Sans CJK SC'


def rgb(color):
    return RGBColor.from_string(color)


def deck(width, height):
    presentation = Presentation()
    presentation.slide_width = Inches(width)
    presentation.slide_height = Inches(height)
    return presentation


def slide(presentation, background=WHITE):
    result = presentation.slides.add_slide(presentation.slide_layouts[6])
    result.background.fill.solid()
    result.background.fill.fore_color.rgb = rgb(background)
    return result


def rect(page, x, y, width, height, fill):
    shape = page.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y),
                                  Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = rgb(fill)
    shape.line.fill.background()
    style = shape._element.find('{http://schemas.openxmlformats.org/presentationml/2006/main}style')
    if style is not None:
        shape._element.remove(style)
    return shape


def text(page, x, y, width, height, value, size, ink=NAVY, bold=False, font=FONT):
    box = page.shapes.add_textbox(Inches(x), Inches(y), Inches(width), Inches(height))
    frame = box.text_frame
    frame.margin_left = frame.margin_right = frame.margin_top = frame.margin_bottom = 0
    frame.word_wrap = True
    for index, line in enumerate(value.split('\n')):
        p = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        p.space_after = Pt(3)
        frag = p.add_run()
        frag.text = line
        frag.font.name = font
        frag.font.size = Pt(size)
        frag.font.bold = bold
        frag.font.color.rgb = rgb(ink)
        ea = OxmlElement('a:ea')
        ea.set('typeface', font)
        frag._r.get_or_add_rPr().append(ea)
    return box


def avatar(page, x, y, size):
    page.shapes.add_picture(str(AVATAR), Inches(x), Inches(y), width=Inches(size))


def signature(page, x, y, dark=False, size=.32):
    avatar(page, x, y, size)
    text(page, x + size + .1, y + .04, .8, .3, '何19', 11,
         WHITE if dark else NAVY, True)


def title(page, value, subtitle=None):
    text(page, .75, .72, 11.8, .95, value, 35, bold=True)
    if subtitle:
        text(page, .78, 1.77, 11.6, .55, subtitle, 17, MUTED)


def picture_placeholder(page, x, y, width, height):
    rect(page, x, y, width, height, 'E9EDF3')
    text(page, x + .24, y + .22, width - .48, .5, '在此插入图片', 13, MUTED)


def presentation():
    d = deck(40/3, 7.5)
    s = slide(d)
    text(s, .85, 2.25, 11.5, 1.1, '从一个问题开始', 49, bold=True)
    text(s, .9, 3.53, 10.8, .6, '在这里写一句能让读者继续看下去的副标题。', 19, MUTED)
    signature(s, 11.66, 6.82)
    s = slide(d)
    text(s, .85, 2.62, 11.5, 1, '这一章的主题', 42, bold=True)
    text(s, .9, 3.82, 11.2, .45, '用一句话交代接下来要讲什么。', 18, MUTED)
    s = slide(d)
    title(s, '一页讲清一个观点', '把结论写在标题里，再用正文展开。')
    for i, (heading, detail) in enumerate((
            ('先交代背景', '写清楚读者需要知道的前提。'),
            ('再展开观点', '从一个具体例子或事实说起。'),
            ('最后给出结论', '用一句话收束这一页。'))):
        y = 2.55 + i * 1.21
        text(s, .82, y, 3.4, .43, heading, 19, bold=True)
        text(s, 4.35, y+.02, 7.7, .5, detail, 17, MUTED)
        rect(s, .82, y+.72, 11.6, .012, LINE)
    s = slide(d)
    title(s, '用图表支持一个判断', '双击图表，编辑示例数据。')
    data = CategoryChartData()
    data.categories = ['第一组', '第二组', '第三组']
    data.add_series('示例值', [24, 38, 31])
    chart = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(.7), Inches(2.35),
                               Inches(8), Inches(3.8), data).chart
    chart.has_legend = False
    plot = chart.plots[0]
    plot.series[0].format.fill.solid()
    plot.series[0].format.fill.fore_color.rgb = rgb('677991')
    for axis in (chart.category_axis, chart.value_axis):
        axis.tick_labels.font.name = FONT
        axis.tick_labels.font.size = Pt(12)
    text(s, 9, 2.85, 3.2, .6, '这里写读图结论', 19, bold=True)
    text(s, 9, 3.6, 3.15, 1.4, '说明变化幅度、比较口径或读者应该留意的点。', 15, MUTED)
    text(s, .78, 6.58, 11.7, .3, '来源｜填写数据出处和日期', 12, MUTED)
    s = slide(d)
    title(s, '图片与说明')
    picture_placeholder(s, .76, 1.95, 11.75, 4.12)
    text(s, .78, 6.27, 11.6, .31, '图注｜用一句话说明图片与本页的关系。', 14, MUTED)
    text(s, .78, 6.68, 11.6, .29, '来源｜填写作者、出处或链接', 11, MUTED)
    s = slide(d)
    title(s, '引用')
    rect(s, .86, 2.42, .045, 2.28, 'AAB7CA')
    text(s, 1.17, 2.72, 10.7, 1.1, '“在这里保留你要引用的原句。”', 31, bold=True)
    text(s, 1.19, 4.15, 10.5, .48, '作者 · 出处 · 日期', 15, MUTED)
    s = slide(d)
    title(s, '代码或命令')
    rect(s, .76, 2.03, 11.75, 3.53, PAPER)
    text(s, 1.08, 2.47, 10.9, 2.1,
         'def introduce(name):\n    return f"Hello, {name}"\n\nprint(introduce("He19"))',
         20, font='Noto Sans Mono')
    text(s, .82, 5.93, 11.5, .4, '补充说明｜标出读者需要重点看的一行。', 14, MUTED)
    s = slide(d)
    text(s, .85, 2.38, 11.6, 1.05, '谢谢看到这里', 46, bold=True)
    text(s, .89, 3.61, 11.5, .62, '在这里留下一个结论或下一步。', 19, MUTED)
    signature(s, 11.66, 6.82)
    return d


def horizontal():
    d = deck(40/3, 7.5)
    s = slide(d, PAPER)
    picture_placeholder(s, 8.07, .92, 4.48, 5.61)
    text(s, .89, 2.05, 6.9, 2.1, '从一个\n好问题开始', 48, bold=True)
    text(s, .91, 4.67, 6.7, .47, '填写本期内容的一句话简介', 18, MUTED)
    signature(s, .93, 6.66)
    s = slide(d, NAVY)
    text(s, 1.02, 2.61, 11.14, 1.25, '填写本期标题', 54, WHITE, True)
    text(s, 1.07, 4.01, 10.9, .61, '一句话介绍本期内容', 21, 'DDE3EC')
    signature(s, 11.67, .42, dark=True)
    s = slide(d)
    text(s, 1.03, 2.72, 11.2, 1.1, '谢谢观看', 48, bold=True)
    text(s, 1.07, 4, 10.8, .55, '填写一句总结或下一期预告。', 20, MUTED)
    signature(s, 11.67, 6.65)
    return d


def vertical(post=False):
    d = deck(7.5, 10 if post else 40/3)
    h = d.slide_height / Inches(1)
    s = slide(d, PAPER)
    picture_placeholder(s, .58, .95 if post else 1.75, 6.34, h * .39)
    text(s, .63, h * .54, 6.24, 2.05, '把想分享的事\n写在这里', 39, bold=True)
    text(s, .66, h * .76, 6, .43, '填写一句副标题', 17, MUTED)
    signature(s, .66, h * .87)
    s = slide(d)
    if post:
        text(s, .63, 1.12, 6.22, 1.2, '用一句话写下观点', 34, bold=True)
        rect(s, .64, 2.92, .045, 2.32, PINK)
        text(s, .89, 3.05, 5.87, 2, '用两三句话展开。可以写一个发现、一段观察，或一条自己试过的方法。', 22)
        text(s, .67, 7.36, 6.02, .6, '来源或补充说明', 14, MUTED)
    else:
        text(s, .66, 4.35, 5.88, 2, '填写本期\n视频标题', 42, bold=True)
        text(s, .68, 7.07, 5.72, .95, '用一句话交代这期要分享什么。', 19, MUTED)
        signature(s, .67, 2.24)
    if not post:
        s = slide(d, NAVY)
        text(s, .68, 5.05, 6, 1.3, '谢谢观看', 44, WHITE, True)
        text(s, .72, 6.74, 5.8, 1, '填写一句总结或更新提示。', 18, 'DDE3EC')
        signature(s, .74, 9.24, dark=True)
    return d


def profile():
    d = deck(7.5, 7.5)
    s = slide(d, PINK)
    avatar(s, .77, 1.35, 1.81)
    text(s, 2.97, 1.64, 3.82, .8, '何19', 39, bold=True)
    text(s, 2.99, 2.56, 3.75, .5, '个人内容创作者', 15, MUTED)
    text(s, .83, 4.45, 5.86, 1.45, '记录做过的事、学到的东西，\n也分享一些值得聊的问题。', 23, bold=True)
    return d


def banner():
    d = deck(40/3, (40/3)*.3125)
    s = slide(d, PAPER)
    rect(s, 0, 3.96, 40/3, .21, PINK)
    avatar(s, 3.62, 1.37, 1.38)
    text(s, 5.35, 1.45, 4.75, .8, '何19', 40, bold=True)
    text(s, 5.39, 2.39, 4.46, .36, '记录、思考与分享', 15, MUTED)
    return d


def speaker():
    d = deck(40/3, 7.5)
    s = slide(d, PAPER)
    avatar(s, .94, 1.75, 3.12)
    text(s, 4.62, 1.4, 7.8, .84, '何19', 42, bold=True)
    text(s, 4.66, 2.51, 7.82, 1.64,
         '何19记录做过的事、学到的东西，也分享一些值得聊的问题。', 21)
    text(s, 4.66, 5.0, 7.5, .61, '活动｜填写活动名称或分享主题', 15, MUTED)
    return d


def card(badge=False):
    d = deck(90/25.4, (60 if badge else 54)/25.4)
    s = slide(d, PAPER)
    avatar(s, .25, .46, .89)
    text(s, 1.33, .49, 1.91, .51, '何19', 24, bold=True)
    text(s, 1.35, 1.13, 1.91, .37, '填写活动名称' if badge else '个人内容创作者', 9, MUTED)
    if badge:
        text(s, 1.35, 1.61, 1.91, .36, '填写现场身份', 9, MUTED)
    else:
        s = slide(d)
        text(s, .29, .46, 2.97, .39, '何19', 16, bold=True)
        text(s, .29, 1.06, 2.97, .8, '邮箱｜填写邮箱\n主页｜填写链接', 8, MUTED)
    return d


def sticker():
    d = deck(50/25.4, 50/25.4)
    avatar(slide(d), .08, .08, 50/25.4-.16)
    return d


def save(presentation, relative):
    path = KIT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    presentation.save(path)
    return path


def export(pdf, index, path, size):
    with TemporaryDirectory() as tmp:
        prefix = Path(tmp) / 'page'
        run(['pdftoppm', '-png', '-f', str(index), '-l', str(index), '-singlefile',
             '-scale-to', str(max(size)), str(pdf), str(prefix)], check=True)
        with Image.open(prefix.with_suffix('.png')) as image:
            image.convert('RGB').resize(size, Image.Resampling.LANCZOS).save(path)


def main():
    layouts = {
        'presentation/he19-template.pptx': (presentation(), (1920, 1080),
            ['cover','chapter','text','chart','photo','quote','code','closing']),
        'bilibili/horizontal.pptx': (horizontal(), (1920, 1080),
            ['cover','opening','ending']),
        'xiaohongshu/vertical-video.pptx': (vertical(), (1080, 1920),
            ['video-cover','video-opening','video-ending']),
        'xiaohongshu/post-cover.pptx': (vertical(post=True), (1080, 1440),
            ['post-cover','post-quote']),
        'social/profile-card.pptx': (profile(), (1080, 1080), ['profile-card']),
        'social/profile-banner.pptx': (banner(), (1920, 600), ['profile-banner']),
        'print/speaker-intro.pptx': (speaker(), (1920, 1080), ['speaker-intro']),
        'print/business-card.pptx': (card(), None, []),
        'print/event-badge.pptx': (card(badge=True), None, []),
        'print/avatar-sticker.pptx': (sticker(), None, []),
    }
    with TemporaryDirectory() as tmp:
        folder = Path(tmp)
        paths = [save(item[0], relative) for relative, item in layouts.items()]
        run(['soffice', '-env:UserInstallation='+(folder/'profile').as_uri(), '--headless',
             '--convert-to', 'pdf', '--outdir', str(folder), *map(str,paths)], check=True)
        for relative, (_, size, exports) in layouts.items():
            dest = KIT / relative
            pdf = folder / dest.with_suffix('.pdf').name
            if dest.parent.name == 'print':
                copyfile(pdf, dest.with_suffix('.pdf'))
            for index, name in enumerate(exports, 1):
                export(pdf, index, dest.parent / (name + '.png'), size)
    identity = KIT/'identity'
    identity.mkdir(exist_ok=True)
    copyfile(AVATAR, identity/'avatar-transparent.png')
    with Image.open(AVATAR) as source:
        square = Image.new('RGBA', (1024, 1024), '#F7F8FA')
        square.alpha_composite(ImageOps.contain(source, (940, 940)), (42,42))
        square.convert('RGB').save(identity/'avatar-square.png')
        source.resize((591,591), Image.Resampling.LANCZOS).save(KIT/'print/sticker-50mm.png',
                                                               dpi=(300,300))
    for theme in ('light','dark'):
        copyfile(ROOT/f'output/he19-signature-{theme}-bg.png', identity/f'signature-{theme}.png')


if __name__ == '__main__':
    main()
