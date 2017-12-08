'''Render a LaTeX equation and save to a tmp image file.


Author: guangzhi XU (xugzhi1987@gmail.com; guangzhi.xu@outlook.com)
Update time: 2017-11-22 11:04:42.
'''

import os
import subprocess
import tempfile
import texformulas
import cPickle

RESO=[200,200]

CURRENT_DIR     = os.path.dirname(os.path.abspath(__file__))
RELATIVE_OUTDIR = 'tab_icons'
TEX2IM_CMD      = os.path.join(CURRENT_DIR,'tex2im/tex2im')
TEX2IM_CMD      = 'bash %s' %TEX2IM_CMD
OUTPUTDIR       = os.path.join(CURRENT_DIR,RELATIVE_OUTDIR)
ICON_META_FILE  = os.path.join(CURRENT_DIR,'icon_paths.txt')



#-----Render single formula and save img file-----
def renderFormula(text,outfile=None):

    reso_str='%dx%d' %(RESO[0],RESO[1])

    tmp_tex_fd,tmp_tex_file=tempfile.mkstemp(suffix='.tex',prefix='tmp_latex_',
            dir='/tmp')

    if outfile is None:
        tmp_img_fd,tmp_img_file=tempfile.mkstemp(suffix='.png',prefix='tmp_latex_',
                dir='/tmp')
    else:
        tmp_img_file=outfile

    try:
        tfile=os.fdopen(tmp_tex_fd,'w')
        tfile.write(text)
        tfile.close()
        cmd='%s -r %s -o %s %s' %(TEX2IM_CMD,reso_str,tmp_img_file,tmp_tex_file)
        proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        rec=proc.wait()
    except:
        rec=1
    finally:
        os.remove(tmp_tex_file)

    return rec


#------------Render a list of formulae------------
def renderList(text_list,subdir,outdir):
    return_list=[]

    for ii,tii in enumerate(text_list):
        filename='%s.png' %str(ii)
        #-----------Get file path for saving img-----------
        outfile=os.path.join(outdir,filename)
        outfile=os.path.expanduser(outfile)
        #--------------Get relative file path--------------
        relative_path=os.path.join(RELATIVE_OUTDIR,subdir)
        relative_path=os.path.join(relative_path,filename)
        try:
            recii=renderFormula(tii,outfile)
            if recii==0:
                return_list.append([tii,relative_path])
            else:
                return_list.append([])
        except:
            return_list.append([])
    return return_list



#-----------------Render a matrix-----------------
def renderMatrix(nrow,ncol,matrix_type,bracket_str,add_dummy,outfile):

    assert matrix_type in ['left','right','cases','matrix','bmatrix',
            'pmatrix','vmatrix','Bmatrix','Vmatrix'],\
        "<matrix_type> should be one in ['left','right','cases','matrix','bmatrix', 'pmatrix','vmatrix','Bmatrix','Vmatrix']."

    return_list=[]

    if matrix_type=='left':
        tex_str=texformulas.getLeftMatrix(nrow,ncol,bracket_str,add_dummy)
    elif matrix_type=='right':
        tex_str=texformulas.getRightMatrix(nrow,ncol,bracket_str,add_dummy)
    elif matrix_type=='cases':
        tex_str=texformulas.getCasesMatrix(nrow,add_dummy)
    else:
        tex_str=texformulas.getDoubleMatrix(nrow,ncol,matrix_type,add_dummy)

    try:
        rec=renderFormula(tex_str,outfile)
        if rec==0:
            return_list.append([tex_str,outfile])
        else:
            return_list.append([])
    except:
        return_list.append([])
    return return_list




FORMULAE_LISTS=[
    ('Greek'            , texformulas.GREEK_LETTERS)      ,
    ('Set symbol'       , texformulas.MATH_SET_SYMBOLS)   ,
    ('Set operator'     , texformulas.MATH_SET_OPERATORS) ,
    ('Math operator'    , texformulas.MATH_OPERATORS)     ,
    ('Text format'      , texformulas.TEXT_FORMATTING)    ,
    ('Spacing'          , texformulas.SPACING)            ,
    ('Decoration'       , texformulas.DECOREATIONS)       ,
    ('Arrow'            , texformulas.ARROWS)             ,
    ('Sub-super script' , texformulas.SUB_SUPER_SCRIPTS)  ,
    ('Fraction'         , texformulas.FRACTIONS)          ,
    ('Integration'      , texformulas.INTEGRATIONS)       ,
    ('Cap/cup'          , texformulas.CAP_CUPS)           ,
    ('Sum'              , texformulas.SUM_PRODUCT)        ,
    ('Bracket'          , texformulas.BRACKETS)           ,
    ('Comparison'       , texformulas.COMPARE_OPERATORS)
]

MATRIX_LISTS=[
        (2 , 2 , 'left'    , '(' , True) ,
        (2 , 2 , 'left'    , '[' , True) ,
        (2 , 2 , 'left'    , '{' , True) ,
        (2 , 2 , 'left'    , '<' , True) ,
        (2 , 2 , 'left'    , '|' , True) ,
        (2 , 2 , 'right'   , ')' , True) ,
        (2 , 2 , 'right'   , ']' , True) ,
        (2 , 2 , 'right'   , '}' , True) ,
        (2 , 2 , 'right'   , '>' , True) ,
        (2 , 2 , 'right'   , '|' , True) ,
        (2 , 2 , 'matrix'  , ''  , True) ,
        (2 , 2 , 'bmatrix' , ''  , True) ,
        (2 , 2 , 'pmatrix' , ''  , True) ,
        (2 , 2 , 'vmatrix' , ''  , True) ,
        (2 , 2 , 'Bmatrix' , ''  , True) ,
        (2 , 2 , 'Vmatrix' , ''  , True) ,
        (2 , 2 , 'cases'   , ''  , True)
]





if __name__=='__main__':

    icon_meta_list=[]

    #-------------------Render icons-------------------
    for ii,itemii in enumerate(FORMULAE_LISTS):
        nameii,listii=itemii
        subdir='tab_%s' %(str(ii).rjust(len(str(len(FORMULAE_LISTS))),'0'))
        outdirii=os.path.join(OUTPUTDIR,subdir)
        print 'save list to',outdirii
        outdirii=os.path.expanduser(outdirii)

        if not os.path.exists(outdirii):
            os.makedirs(outdirii)

        meta_listii=renderList(listii,subdir,outdirii)
        icon_meta_list.append([nameii,meta_listii])

    #---------------Render matrix icons---------------
    outdirii=os.path.join(OUTPUTDIR,'tab_matrix')
    print 'save list to',outdirii
    outdirii=os.path.expanduser(outdirii)

    if not os.path.exists(outdirii):
        os.makedirs(outdirii)

    matrix_icon_meta_list=[]
    for ii,mii in enumerate(MATRIX_LISTS):
        fileii=str(ii+1).rjust(len(str(len(MATRIX_LISTS))),'0')+'.png'
        outfileii=os.path.join(outdirii,fileii)
        print 'save matrix img',outfileii
        argsii=mii+(outfileii,)

        try:
            meta_listii=renderMatrix(*argsii)
            matrix_icon_meta_list.extend(meta_listii)
        except:
            matrix_icon_meta_list.extend([])

    icon_meta_list.append(['Matrix',matrix_icon_meta_list])
    with open(ICON_META_FILE,'w') as fout:
        cPickle.dump(icon_meta_list,fout)




