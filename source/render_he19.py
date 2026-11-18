from pathlib import Path
from base64 import b64encode
from subprocess import Popen, PIPE
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parents[1]
source = root / 'source/video/index.html'
output = root / 'output/he19-cache.mp4'
fps = 24

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    page = browser.new_page(viewport={'width':1280,'height':720})
    html = source.read_text()
    html = html.replace('<script src="gsap.min.js"></script>', '<script>' + source.with_name('gsap.min.js').read_text() + '</script>')
    for filename, mime in [('avatar.png','image/png'),('he19-ui.otf','font/otf')]:
        data = b64encode(source.with_name(filename).read_bytes()).decode()
        html = html.replace(filename, f'data:{mime};base64,{data}')
    page.set_content(html)
    page.evaluate('document.fonts.ready')
    assert page.evaluate('Boolean(window.__timelines.he19)')
    encoder = Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','image2pipe',
                     '-framerate',str(fps),'-vcodec','mjpeg','-i','-','-c:v','libx264',
                     '-crf','18','-preset','fast','-pix_fmt','yuv420p','-movflags','+faststart',str(output)],stdin=PIPE)
    try:
        for i in range(19 * fps):
            page.evaluate('''t => {
              for (const clip of document.querySelectorAll("[data-track-index]")) {
                const start = Number(clip.dataset.start);
                clip.style.visibility = t >= start && t < start + Number(clip.dataset.duration) ? "visible" : "hidden";
              }
              window.__timelines.he19.seek(t);
            }''', i/fps)
            encoder.stdin.write(page.screenshot(type='jpeg',quality=96))
    finally:
        encoder.stdin.close()
        result=encoder.wait()
    assert result == 0
