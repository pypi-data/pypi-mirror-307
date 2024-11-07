# -*- coding: utf-8 -*-
"""
    pygments.formatters.rtf
    ~~~~~~~~~~~~~~~~~~~~~~~

    A formatter that generates RTF files.

    :copyright: Copyright 2006-2017 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.formatter import Formatter
from pygments.util import get_int_opt, _surrogatepair


__all__ = ['RtfFormatter']


class RtfFormatter(Formatter):
    """
    Format tokens as RTF markup. This formatter automatically outputs full RTF
    documents with color information and other useful stuff. Perfect for Copy and
    Paste into Microsoft(R) Word(R) documents.

    Please note that ``encoding`` and ``outencoding`` options are ignored.
    The RTF format is ASCII natively, but handles unicode characters correctly
    thanks to escape sequences.

    .. versionadded:: 0.6

    Additional options accepted:

    `style`
        The style to use, can be a string or a Style subclass (default:
        ``'default'``).

    `fontface`
        The used font famliy, for example ``Bitstream Vera Sans``. Defaults to
        some generic font which is supposed to have fixed width.

    `fontsize`
        Size of the font used. Size is specified in half points. The
        default is 24 half-points, giving a size 12 font.

        .. versionadded:: 2.0
    """
    name = 'RTF'
    aliases = ['rtf']
    filenames = ['*.rtf']

    def __init__(self, **options):
        r"""
        Additional options accepted:

        ``fontface``
            Name of the font used. Could for example be ``'Courier New'``
            to further specify the default which is ``'\fmodern'``. The RTF
            specification claims that ``\fmodern`` are "Fixed-pitch serif
            and sans serif fonts". Hope every RTF implementation thinks
            the same about modern...

        """
        Formatter.__init__(self, **options)
        self.fontface = options.get('fontface') or ''
        self.fontsize = get_int_opt(options, 'fontsize', 0)

    def _escape(self, text):
        return text.replace(u'\\', u'\\\\') \
                   .replace(u'{', u'\\{') \
                   .replace(u'}', u'\\}')

    def _escape_text(self, text):
        # empty strings, should give a small performance improvment
        if not text:
            return u''

        # escape text
        text = self._escape(text)

        buf = []
        for c in text:
            cn = ord(c)
            if cn < (2**7):
                # ASCII character
                buf.append(str(c))
            elif (2**7) <= cn < (2**16):
                # single unicode escape sequence
                buf.append(u'{\\u%d}' % cn)
            elif (2**16) <= cn:
                # RTF limits unicode to 16 bits.
                # Force surrogate pairs
                buf.append(u'{\\u%d}{\\u%d}' % _surrogatepair(cn))

        return u''.join(buf).replace(u'\n', u'\\par\n')

    def format_unencoded(self, tokensource, outfile):
        # rtf 1.8 header
        outfile.write(u'{\\rtf1\\ansi\\uc0\\deff0'
                      u'{\\fonttbl{\\f0\\fmodern\\fprq1\\fcharset0%s;}}'
                      u'{\\colortbl;' % (self.fontface and
                                         u' ' + self._escape(self.fontface) or
                                         u''))

        # convert colors and save them in a mapping to access them later.
        color_mapping = {}
        offset = 1
        for _, style in self.style:
            for color in style['color'], style['bgcolor'], style['border']:
                if color and color not in color_mapping:
                    color_mapping[color] = offset
                    outfile.write(u'\\red%d\\green%d\\blue%d;' % (
                        int(color[0:2], 16),
                        int(color[2:4], 16),
                        int(color[4:6], 16)
                    ))
                    offset += 1
        outfile.write(u'}\\f0 ')
        if self.fontsize:
            outfile.write(u'\\fs%d' % (self.fontsize))

        # highlight stream
        for ttype, value in tokensource:
            while not self.style.styles_token(ttype) and ttype.parent:
                ttype = ttype.parent
            style = self.style.style_for_token(ttype)
            buf = []
            if style['bgcolor']:
                buf.append(u'\\cb%d' % color_mapping[style['bgcolor']])
            if style['color']:
                buf.append(u'\\cf%d' % color_mapping[style['color']])
            if style['bold']:
                buf.append(u'\\b')
            if style['italic']:
                buf.append(u'\\i')
            if style['underline']:
                buf.append(u'\\ul')
            if style['border']:
                buf.append(u'\\chbrdr\\chcfpat%d' %
                           color_mapping[style['border']])
            start = u''.join(buf)
            if start:
                outfile.write(u'{%s ' % start)
            outfile.write(self._escape_text(value))
            if start:
                outfile.write(u'}')

        outfile.write(u'}')
