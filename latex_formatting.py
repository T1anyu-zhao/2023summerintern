import re
import pyparsing

C = r"\frac{1}{5}\begin{pmatrix}-1&-1&0&2&0\\-2&0&0&1&1\end{pmatrix}\begin{pmatrix}-1&-2\\-1&0\\0&0\\2&1\\0&1\end{pmatrix}=\begin{pmatrix}\frac{6}{5}&\frac{4}{5}\\\frac{4}{5}&\frac{6}{5}\end{pmatrix}"
print(repr(C))

def reg_match():
    and_sign = r'[&]'
    slash_sign = r'\\{2}'
    beginend = r'(\\{1})(\bbegin\b|\bend\b)({(.*?)})'
    match_patt = f"({and_sign})|({slash_sign})|({beginend})"
    # print(match_patt)
    return match_patt

def newline(match):
    if match.group(1) == r'\begin':
        newl = '\n' + match.group(0) + '\n'
    else:
        newl = '\n' + match.group(0)
    # print(newl)
    return newl

test = re.sub(r'[&]', r' & ', C)
test = re.sub(r'\\{2}', r' \\\\\n', test)
test = re.sub(r'(\\\bbegin\b)({(.*?)})', newline, test)
test = re.sub(r'(\\\bend\b)({(.*?)})', newline, test)
test = re.sub(r'  ', ' ', test)
print(test)

# begin xxx begin end xxx end
print('parseing test')
thecontent = pyparsing.Word(pyparsing.alphanums) | '+' | '-'
parens = pyparsing.nestedExpr( r'\begin', r'\end')

parens.parseString(instring=test)


print(re.findall(r'\\begin',test))
print(re.findall(r'\\end',test))