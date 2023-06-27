# TODO: this should be automatically generated, changes in dict have to be represented here as well
# How about ignore case when matching?
period_ptrn = r"\b(mán(ud)?|þri(ðjud)?|miðvikud|fim(mtud)?|fös(tud)?|lau(gard)|sun(nud)|[Jj]an|[Ff]eb|[Mm]ar|[Aa]pr|[Jj]ú[nl]|[Áá]gú?|[Ss]ept?|[Oo]kt|[Nn]óv|[Dd]es)\.?|\b(I(II?|V|X)|(V|X|XV)I{1,3}|XI?[VX])\b"


def make_period_dict():
    period_dict = {
        r"(\W|^)mán(ud)?\.?(\W|$)": r"\g<1>mánudag\g<3>",
        r"(\W|^)þri(ðjud)?\.?(\W|$)": r"\g<1>þriðjudag\g<3>",
        r"(\W|^)miðvikud\.?(\W|$)": r"\g<1>miðvikudag\g<2>",
        r"(\W|^)fim(mtud)?\.?(\W|$)": r"\g<1>fimmtudag\g<3>",
        r"(\W|^)fös(tud)?\.?(\W|$)": r"\g<1>föstudag\g<3>",
        r"(\W|^)lau(gard)?\.?(\W|$)": r"\g<1>laugardag\g<3>",
        r"(\W|^)sun(nud)?\.?(\W|$)": r"\g<1>sunnudag\g<3>",
        r"(\W|^)[Jj]an\.?(\W|$)": r"\g<1>janúar\g<2>",
        r"(\W|^)[Ff]eb\.?(\W|$)": r"\g<1>febrúar\g<2>",
        r"(\W|^)[Mm]ar\.?(\W|$)": r"\g<1>mars\g<2>",
        r"(\W|^)[Aa]pr\.?(\W|$)": r"\g<1>apríl\g<2>",
        r"(\W|^)[Jj]ún\.?(\W|$)": r"\g<1>júní\g<2>",
        r"(\W|^)[Jj]úl\.?(\W|$)": r"\g<1>júlí\g<2>",
        r"(\W|^)[Áá]gú?\.?(\W|$)": r"\g<1>ágúst\g<2>",
        r"(\W|^)[Ss]ept?\.?(\W|$)": r"\g<1>september\g<2>",
        r"(\W|^)[Oo]kt\.?(\W|$)": r"\g<1>október\g<2>",
        r"(\W|^)[Nn]óv\.?(\W|$)": r"\g<1>nóvember\g<2>",
        r"(\W|^)[Dd]es\.?(\W|$)": r"\g<1>desember\g<2>",
        r"(\W|^)II\.?(\W|$)": r"\g<1>annar\g<2>",
        r"(\W|^)III\.?(\W|$)": r"\g<1>þriðji\g<2>",
        r"(\W|^)IV\.?(\W|$)": r"\g<1>fjórði\g<2>",
        r"(\W|^)VI\.?(\W|$)": r"\g<1>sjötti\g<2>",
        r"(\W|^)VII\.?(\W|$)": r"\g<1>sjöundi\g<2>",
        r"(\W|^)VIII\.?(\W|$)": r"\g<1>áttundi\g<2>",
        r"(\W|^)IX\.?(\W|$)": r"\g<1>níundi\g<2>",
        r"(\W|^)XI\.?(\W|$)": r"\g<1>ellefti\g<2>",
        r"(\W|^)XII\.?(\W|$)": r"\g<1>tólfti\g<2>",
        r"(\W|^)XIII\.?(\W|$)": r"\g<1>þrettándi\g<2>",
        r"(\W|^)XIV\.?(\W|$)": r"\g<1>fjórtándi\g<2>",
        r"(\W|^)XV\.?(\W|$)": r"\g<1>fimmtándi\g<2>",
        r"(\W|^)XVI\.?(\W|$)": r"\g<1>sextándi\g<2>",
        r"(\W|^)XVII\.?(\W|$)": r"\g<1>sautjándi\g<2>",
        r"(\W|^)XVIII\.?(\W|$)": r"\g<1>átjándi\g<2>",
        r"(\W|^)XIX\.?(\W|$)": r"\g<1>nítjándi\g<2>",
    }

    return period_dict
