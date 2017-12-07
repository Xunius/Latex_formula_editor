'''Dictionary containing tex formulae for various symbols, structures.

Author: guangzhi XU (xugzhi1987@gmail.com; guangzhi.xu@outlook.com)
Update time: 2017-11-21 13:45:13.
'''

GREEK_LETTERS=[
r'\alpha', r'\beta', r'\gamma', r'\delta', r'\epsilon', r'\zeta', r'\eta',
r'\theta', r'\iota', r'\kappa', r'\lambda', r'\mu', r'\nu', r'\xi', r'\pi',
r'\rho', r'\sigma', r'\tau', r'\upsilon', r'\phi', r'\chi', r'\psi', r'\omega',
r'\Gamma', r'\Delta', r'\Theta', r'\Lambda', r'\Xi', r'\Pi', r'\Sigma',
r'\Upsilon', r'\Phi', r'\Psi', r'\Omega'
]

MATH_SET_SYMBOLS=[
r'\partial',
r'\angle',
r'\infty',
r'\mathbb{P}',
r'\mathbb{N}',
r'\mathbb{R}',
r'\mathbb{Z}',
r'\mathbb{I}',
r'\mathbb{Q}',
r'\mathbb{C}',
r'\therefore',
r'\because',
r'\imath',
r'\jmath',
r'\forall',
r'\exists',
r'\varnothing',
r'\Re',
r'\Im'
]

MATH_SET_OPERATORS=[
r'\sqsubset',
r'\sqsupset',
r'\sqsubseteq',
r'\sqsupseteq',
r'\subset',
r'\supset',
r'\subseteq',
r'\supseteq',
r'\nsubseteq',
r'\nsupseteq',
r'\subseteqq',
r'\supseteqq',
r'\nsubseteq',
r'\nsupseteqq',
r'\in',
r'\ni',
r'\notin'
]

MATH_OPERATORS=[
r'\pm',
r'\cap',
r'\cup',
r'\cdot',
r'\mp',
r'\Cap',
r'\Cup',
r'\uplus',
r'\times',
r'\sqcap',
r'\sqcup',
r'\bigsqcup',
r'\ast',
r'\wedge',
r'\vee',
r'\bigtriangleup',
r'\div',
r'\barwedge',
r'\veebar',
r'\bigtriangledown',
r'\setminus',
r'\triangleleft',
r'\triangleright',
r'\star',
r'\dotplus',
r'\lozenge',
r'\blacklozenge',
r'\bigstar',
r'\amalg',
r'\circ',
r'\bullet',
r'\bigcirc',
r'\dagger',
r'\square',
r'\blacksquare',
r'\bigoplus',
r'\ddagger',
r'\triangle',
r'\blacktriangle',
r'\bigotimes',
r'\wr',
r'\triangledown',
r'\blacktriangledown',
r'\bigodot',
r'\diamond',
r'\ominus',
r'\oplus',
r'\circledcirc',
r'\oslash',
r'\otimes',
r'\circledast',
r'\circleddash',
r'\odot',
r'\log_{a}{b}',
r'\lg_{a}{b}'
]

TEXT_FORMATTING=[
r'\mathbf{a}',
r'\textup{a}',
r'\textbf{a}',
r'\mathit{a}',
r'\textit{a}',
r'\mathrm{a}',
r'\textrm{a}',
r'\mathfrak{a}',
r'\textsl{a}',
r'\mathbb{a}',
r'\texttt{a}',
r'\textsc{a}',
r'\emph{a}'
]

SPACING=[
'a \,b ', 'a \: b', 'a \; b', 'a \! b' 
]


DECOREATIONS=[
r"{a}'",
r"{a}''",
r'\dot{a}',
r'\ddot{a}',
r'\hat{a}',
r'\check{a}',
r'\grave{a}',
r'\acute{a}',
r'\tilde{a}',
r'\breve{a}',
r'\bar{a}',
r'\vec{a}',
r'\not{a}',
r'^{\circ}',
r'\widetilde{abc}',
r'\widehat{abc}',
r'\overleftarrow{abc}',
r'\overrightarrow{abc}',
r'\overline{abc}',
r'\underline{abc}',
r'\overbrace{abc}',
r'\underbrace{abc}',
r'\overset{a}{abc}',
r'\underset{a}{abc}'
]


ARROWS=[
r'x \mapsto x^2',
r'n \to',
r'\leftarrow',
r'\rightarrow',
r'\Leftarrow',
r'\Rightarrow',
r'\leftrightarrow',
r'\Leftrightarrow',
r'\leftharpoonup',
r'\rightharpoonup',
r'\leftharpoondown',
r'\rightharpoondown',
r'\leftrightharpoons',
r'\rightleftharpoons',
r'\xleftarrow[text]{long}',
r'\xrightarrow[text]{long}',
r'\overset{a}{\leftarrow}',
r'\overset{a}{\rightarrow}',
r'\underset{a}{\leftarrow}',
r'\underset{a}{\rightarrow}'
]


SUB_SUPER_SCRIPTS=[
r'x^{a}',
r'x_{a}',
r'x_{a}^{b}',
r'{x_{a}}^{b}',
r'_{a}^{b}\textrm{C}'
]


FRACTIONS=[
r'\frac{a}{b}',
r'\tfrac{a}{b}',
r'\frac{\partial }{\partial x}',
r'\frac{\partial^2 }{\partial x^2}',
r'\frac{\mathrm{d} }{\mathrm{d} x}'
]

INTEGRATIONS=[
r'\int dx',
r'\int_{a}^{b} dx ',
r'\oint dx',
r'\oint_{a}^{b}',
r'\iint_{a}^{b}'
]

CAP_CUPS=[
r'\bigcap',
r'\bigcap_{a}^{b}',
r'\bigcup',
r'\bigcup_{a}^{b}',
r'\lim_{x \to 0}'
]

SUM_PRODUCT=[
r'\sum_{a}^{b}',
r'\sqrt{x}',
r'\sqrt[n]{x}',
r'\prod',
r'\prod_{a}^{b}',
r'\coprod ',
r'\coprod_{a}^{b}'
]


BRACKETS=[
r'\left ( x \right )',
r'\left [ x \right ]',
r'\left \{ x \right \}',
r'\left | x \right |',
r'\left \{ x \right.',
r'\left \| x \right \|',
r'\left \langle x \right \rangle',
r'\left \lfloor x \right \rfloor',
r'\left \lceil x \right \rceil',
r'\left. x \right \}'
]

COMPARE_OPERATORS=[
r'<',
r'>',
r'=',
r'\leq',
r'\geq',
r'\doteq',
r'\leqslant',
r'\geqslant',
r'\equiv',
r'\nless',
r'\ngtr',
r'\neq',
r'\nleqslant',
r'\ngeqslant',
r'\not\equiv',
r'\prec',
r'\succ',
r'\preceq',
r'\succeq',
r'\sim',
r'\ll',
r'\gg',
r'\approx',
r'\vdash',
r'\dashv',
r'\simeq',
r'\smile',
r'\frown',
r'\cong',
r'\models',
r'\perp',
r'\asymp',
r'\mid',
r'\parallel',
r'\propto',
r'\bowtie',
r'\Join',
r'\infty'
]



#--------------------Functions--------------------
getBeginStr = lambda x: r'\begin{%s}' %x
getEndStr = lambda x: r'\end{%s}' %x


#--------Get string for matrix inner lines--------
def getMatrixInner(nrow,ncol,add_dummy):
    if not add_dummy:
        line_str='&'.join([' ']*ncol)
        inner_str=(r' \\'+'\n').join([line_str,]*nrow)
    else:
        inner_str=[]
        for ii in range(nrow):
            line_ii=['a_{%d%d}' %(ii+1,jj+1) for jj in range(ncol)]
            line_ii=' & '.join(line_ii)
            inner_str.append(line_ii)
        inner_str=(r' \\'+'\n').join(inner_str)

    return inner_str


#--Get string for matrix with left and right brackets--
def getDoubleMatrix(nrow,ncol,matrix_type,add_dummy=True):
    assert matrix_type in ['matrix','bmatrix','pmatrix','vmatrix',
            'Bmatrix','Vmatrix'], "<matrix_type> not included."

    matrix_str=getMatrixInner(nrow,ncol,add_dummy)
    begin_matrix=getBeginStr(matrix_type)
    end_matrix=getEndStr(matrix_type)
    ret_str='''\
%s
%s
%s
''' %(begin_matrix, matrix_str, end_matrix)

    return ret_str


#---------Get string for cases inner lines---------
def getCasesInner(nrow,add_dummy):
    inner_str=[]
    for ii in range(nrow):
        if not add_dummy:
            line_ii=r' & \text{ if }'
        else:
            line_ii=r' y_%d & \text{ if } x_%d' %(ii,ii)
        inner_str.append(line_ii)
    line_str=(r' \\'+'\n').join(inner_str)

    return line_str


#-----------Get string for cases matrix-----------
def getCasesMatrix(nrow,add_dummy=True):
    begin_matrix=getBeginStr('cases')
    end_matrix=getEndStr('cases')
    matrix_str=getCasesInner(nrow,add_dummy)
    ret_str='''\
%s
%s
%s
''' %(begin_matrix,matrix_str,end_matrix)
    return ret_str


#-----Get string for matrix with left bracket-----
def getLeftMatrix(nrow,ncol,bracket_str,add_dummy=True):
    bracket_dict={
            '(': r'(',
            '[': r'[',
            '{': r'\{',
            '<': r'<',
            '|': r'|'}
    assert bracket_str in bracket_dict.keys(), "<matrix_type> not included."

    matrix_str=getMatrixInner(nrow,ncol,add_dummy)
    begin_matrix=r'\left%s%s' %(bracket_dict[bracket_str],getBeginStr('matrix'))
    end_matrix=r'%s\right.' %getEndStr('matrix')
    ret_str='''\
%s
%s
%s
''' %(begin_matrix, matrix_str, end_matrix)

    return ret_str



#-----Get string for matrix with right bracket-----
def getRightMatrix(nrow,ncol,bracket_str,add_dummy=True):
    bracket_dict={
            ')': r')',
            ']': r']',
            '}': r'\}',
            '>': r'>',
            '|': r'|'}
    assert bracket_str in bracket_dict.keys(), "<matrix_type> not included."

    matrix_str=getMatrixInner(nrow,ncol,add_dummy)
    begin_matrix=r'\left.%s' %getBeginStr('matrix')
    end_matrix=r'%s\right%s' %(getEndStr('matrix'),bracket_dict[bracket_str])
    ret_str='''\
%s
%s
%s
''' %(begin_matrix, matrix_str, end_matrix)

    return ret_str


