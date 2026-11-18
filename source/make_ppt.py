from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.xmlchemy import OxmlElement

OUT = str(Path(__file__).resolve().parents[1] / 'output') + '/'
NAVY, MUTED, ORANGE, PINK, PAPER, WHITE = '14213A','485873','FFAE36','F8DDD8','FFFAF3','FFFFFF'
r = Presentation()
r.slide_width, r.slide_height = Inches(13.3333), Inches(7.5)

def color(x):
    return RGBColor.from_string(x)

def block(s, x, y, w, h, fill):
    box=s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    box.fill.solid()
    box.fill.fore_color.rgb=color(fill)
    box.line.fill.background()

def txt(s, x, y, w, h, value, size=22, ink=NAVY, bold=False, face='Noto Sans CJK SC'):
    box=s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf=box.text_frame
    tf.margin_left=tf.margin_right=tf.margin_top=tf.margin_bottom=0
    tf.word_wrap=True
    for index, line in enumerate(value.split('\n')):
        p=tf.paragraphs[0] if index==0 else tf.add_paragraph()
        p.space_after=Pt(5)
        run=p.add_run()
        run.text=line
        run.font.name=face
        run.font.size=Pt(size)
        run.font.bold=bold
        run.font.color.rgb=color(ink)
        east_asian=OxmlElement('a:ea')
        east_asian.set('typeface', face)
        run._r.get_or_add_rPr().append(east_asian)

def slide(bg=PAPER):
    s=r.slides.add_slide(r.slide_layouts[6])
    s.background.fill.solid()
    s.background.fill.fore_color.rgb=color(bg)
    return s

def header(s, label, title):
    txt(s,.75,.55,11,.35,label,14,MUTED,True)
    txt(s,.75,1.02,11.9,.83,title,38,NAVY,True)
    block(s,.75,1.96,.78,.07,ORANGE)

def footer(s, n):
    block(s,.75,6.88,11.82,.012,'D8DFE8')
    txt(s,.75,7.02,4,.29,'何19  /  技术科普',11,MUTED)
    txt(s,12.20,7.02,.35,.29,f'{n:02}',11,MUTED)

def avatar(s,x,y,w):
    s.shapes.add_picture(OUT+'he19-avatar-preview.png', Inches(x), Inches(y), width=Inches(w))

s=slide()
txt(s,.8,1.12,7,.4,'何19  /  技术科普',17,MUTED,True)
txt(s,.8,1.92,8.0,2.15,'缓存是怎么\n工作的？',55,NAVY,True)
block(s,.83,4.32,1.15,.1,ORANGE)
txt(s,.83,4.85,6.6,1.0,'从一次商品详情请求开始',23,MUTED)
avatar(s,8.2,1.38,4.37)

s=slide(WHITE)
header(s,'请求流程','命中就返回，未命中就查数据库')
for y, fill, tag, action, detail in [
    (2.55,ORANGE,'缓存命中','直接返回','读取缓存里的商品详情'),
    (4.14,'EDF1F7','缓存未命中','查询数据库','拿到详情后写入缓存，再返回')
]:
    block(s,.75,y,2.8,1.1,fill)
    txt(s,1,y+.31,2.4,.5,tag,21,NAVY,True)
    txt(s,3.77,y+.25,.6,.55,'→',24,MUTED)
    txt(s,4.57,y+.05,7,.55,action,27,NAVY,True)
    txt(s,4.57,y+.65,7,.45,detail,17,MUTED)
footer(s,2)

s=slide(WHITE)
header(s,'代码示例','读取商品详情的缓存逻辑')
block(s,.75,2.3,11.83,3.95,NAVY)
code=['product = cache.get(key)','if product is not None:', '    return product', '', 'product = db.get_product(product_id)','cache.set(key, product, ttl=60)','return product']
for i,line in enumerate(code):
    txt(s,1.12,2.61+i*.46,11,.44,line,17,ORANGE if i in (2,5) else WHITE,False,'Consolas')
footer(s,3)

s=slide(WHITE)
header(s,'常见误区','缓存命中，数据就一定最新？')
block(s,.75,2.52,11.83,3.0,PINK)
txt(s,1.14,2.93,10.8,.65,'命中只说明缓存里有这条数据。',29,NAVY,True)
txt(s,1.14,3.82,10.25,1.2,'如果商品价格刚更新，缓存里的旧价格可能还在。\n可以在更新后删除对应缓存，并设置合理的过期时间。',20,NAVY)
footer(s,4)

s=slide(NAVY)
txt(s,.8,.86,7,.4,'本期小结',16,ORANGE,True)
txt(s,.8,1.57,8.1,2.25,'先查缓存，\n没命中再查库。',46,WHITE,True)
block(s,.8,4.0,1.08,.09,ORANGE)
txt(s,.8,4.54,7.2,1.2,'下次看到缓存命中率，试着想想：\n有多少请求省掉了一次数据库查询？',20,'E1E8F4')
avatar(s,8.53,1.78,3.95)

r.save(OUT+'he19-cache.pptx')
