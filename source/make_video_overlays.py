"""Produce transparent corner overlays from the shared He19 signature PNGs."""
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory

from PIL import Image

KIT = Path(__file__).resolve().parents[1] / 'kit'
LAYOUTS = {
    'horizontal': (1920, 1080, 120, 1735, 48),
    'vertical': (1080, 1920, 120, 74, 266),
}


def main():
    (KIT/'video').mkdir(exist_ok=True)
    with TemporaryDirectory() as tmp:
        for layout, (width, height, mark_width, x, y) in LAYOUTS.items():
            for theme in ('light', 'dark'):
                with Image.open(KIT/'identity'/f'signature-{theme}.png') as source:
                    mark_height = round(mark_width*source.height/source.width)
                    mark = source.convert('RGBA').resize((mark_width,mark_height), Image.Resampling.LANCZOS)
                mark_path = Path(tmp) / 'signature.png'
                mark.save(mark_path)
                target = KIT/'video'/f'corner-{layout}-{theme}'
                frame = Image.new('RGBA', (width, height))
                frame.alpha_composite(mark, (x,y))
                frame.save(target.with_suffix('.png'))
                filters = ('format=rgba,fade=t=in:st=0:d=0.25:alpha=1,'
                           'fade=t=out:st=2.7:d=0.3:alpha=1,'
                           f'pad={width}:{height}:{x}:{y}:color=black@0,format=argb')
                run(['ffmpeg', '-hide_banner', '-loglevel','error','-y','-loop','1',
                     '-framerate','30','-i',str(mark_path),'-t','3','-vf',filters,
                     '-an','-c:v','qtrle',str(target.with_suffix('.mov'))],check=True)


if __name__ == '__main__':
    main()
