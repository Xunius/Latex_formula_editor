#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''A LaTeX formulae reference and editting tool.


Author: guangzhi XU (xugzhi1987@gmail.com; guangzhi.xu@outlook.com)
Update time: 2017-12-07 16:37:35.


TODO: add status bar and output info as "copied to clipboard", "save fav".
'''



import sys,os,shutil
import math
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap, QIcon, QFont
import tempfile
import subprocess
import json

#---------------------Globals---------------------
__version__='v0.1'


BUTTON_ICON_SIZE      = 16        # function button size
THUMBNAIL_SIZE        = 36        # thumbnail button size in preset
MATRIX_THUMBNAIL_SIZE = 48        # thumbnail size for matrix icons in preset
HIST_THUMBNAIL_SIZE   = 60        # thumbnail button size in history/favorites
N_HIST                = 20        # size of history/favorite tray
BUTTON_FONT_SIZE      = 11        # font size for buttons
TEXT_EDIT_FONT        = 13        # font size for formula edit box
ICON_NCOL             = 5         # number of columns in preset
MATRIX_ICON_NCOL      = 4         # number of columns in matrix preset
TAB_NCOL              = 2         # number of columns for tab icons
DEFAULT_RESO          = 150
CURRENT_DIR           = os.path.dirname(os.path.abspath(__file__))
ICON_META_FILE        = os.path.join(CURRENT_DIR, 'icon_paths.txt')   # preset file
ERROR_IMG_FILE        = os.path.join(CURRENT_DIR, 'tab_icons/error.png')  # image for error message
HISTORY_FILE          = os.path.join(CURRENT_DIR, 'history/history.txt')   # history data file
TEX2IM_CMD            = os.path.join(CURRENT_DIR,'tex2im/tex2im')  # tex2im exe path
DEMO_IMG              = os.path.join(CURRENT_DIR,'tab_icons/demo.png') # demo img


DEMO_FORMULA=\
r'''\int_z^{\infty} \frac{dI}{I} = - \int_z^{\infty} \rho k_{\lambda}sec \theta dz
'''

def getHSpacer():
    h_spacer = QtWidgets.QSpacerItem(0,0,QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum)
    return h_spacer

def getVSpacer():
    v_spacer = QtWidgets.QSpacerItem(0,0,QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding)
    return v_spacer

def getVLine(parent):
    v_line = QtWidgets.QFrame(parent)
    v_line.setFrameShape(QtWidgets.QFrame.VLine)
    v_line.setFrameShadow(QtWidgets.QFrame.Sunken)
    return v_line

def getHLine(parent):
    h_line = QtWidgets.QFrame(parent)
    h_line.setFrameShape(QtWidgets.QFrame.HLine)
    h_line.setFrameShadow(QtWidgets.QFrame.Sunken)
    return h_line


def getMinSizePolicy():
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum)
    return sizePolicy

def getXMinYExpandSizePolicy():
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding)
    return sizePolicy

def getXExpandYMinSizePolicy():
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum)
    return sizePolicy

def getXExpandYExpandSizePolicy():
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding)
    return sizePolicy



#-----Render single formula and save img file-----
def renderFormula(text,reso,outfile=None):
    '''Render formula and save image file

    <text>: str, latex formula string.
    <reso>: int, reso of output image.
    <outfile>: str, absolute path for output img file location.

    Return <rec>: int, recturn code.
           <tmp_img_file>: str, absolute path for temp img.
    '''
    if len(text)==0:
        return 2, None

    reso_str='%dx%d' %(reso,reso)

    #------------Get a random tmp file name------------
    tmp_tex_fd,tmp_tex_file=tempfile.mkstemp(suffix='.tex',prefix='tmp_latex_',
            dir='/tmp')
    if outfile is None:
        tmp_img_fd,tmp_img_file=tempfile.mkstemp(suffix='.png',prefix='tmp_latex_',
                dir='/tmp')
    else:
        tmp_img_file=outfile

    #------------Call tex2im to render text------------
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

    return rec,tmp_img_file



class MainFrame(QtWidgets.QWidget):

    def __init__(self,thumbnail_meta_list):
        super(MainFrame,self).__init__()

        self.thumbnail_meta_list=thumbnail_meta_list
        self.thumbnail_btn_dict={}    # buttons for preset icons

        #-----Try load previous session and favorites-----
        self.loadHistory()

        #-------------------Button holders-------------------
        self.history_btn_dict={}
        self.history_btn_list=[]
        self.favorite_btn_dict={}
        self.favorite_btn_list=[]
        self.tab_btn_dict={}

        self.initUI()


    def loadHistory(self):
        '''Load history and favorites if exists
        '''
        #----------------Check history file----------------
        history_file_path=os.path.join(CURRENT_DIR,HISTORY_FILE)

        if os.path.exists(history_file_path):
            self.has_hist=True

            with open(history_file_path,'r') as fin:
                data_dict=json.load(fin)

                hist=[]
                if 'history_data' in data_dict:
                    for ii,dii in enumerate(data_dict['history_data']):
                        imgii=QPixmap(dii[1])
                        hist.append([dii[0],dii[1],imgii])
                self.history_data_list=hist

                fav=[]
                if 'favorite_data' in data_dict:
                    for ii,dii in enumerate(data_dict['favorite_data']):
                        imgii=QPixmap(dii[1])
                        fav.append([dii[0],dii[1],imgii])
                self.favorite_data_list=fav
        else:
            self.has_hist=False

            self.favorite_data_list=[]
            self.history_data_list=[]



    def getThumbnailFrame(self,icon_size,thumbnail_list,nrow=None,ncol=None):
        '''Get thumbnail frame for preset icons
        '''

        frame=QtWidgets.QWidget()
        grid=QtWidgets.QGridLayout()
        grid.setSpacing(0)

        #------------------Get grid size------------------
        nlist=len(thumbnail_list)
        if nrow is None and ncol is not None:
            nrow=max(1,int(math.ceil(nlist/float(ncol))))
        elif nrow is not None and ncol is None:
            ncol=max(1,int(math.ceil(nlist/float(nrow))))
        else:
            raise Exception("<nrow> and <ncol> need to set one of them.")

        #---------------Add buttons to grid---------------
        positions=[(ii,jj) for ii in range(nrow) for jj in range(ncol)]

        for posii,thumbnailii in zip(positions,thumbnail_list):
            icon_textii,icon_img_pathii=thumbnailii
            # need to prepend CURRENT_DIR, otherwise icons won't show when
            # running from outside of code folder
            icon_img_pathii=os.path.join(CURRENT_DIR, icon_img_pathii)
            buttonii=QtWidgets.QToolButton(self)
            buttonii.setIcon(QIcon(icon_img_pathii))
            buttonii.setIconSize(QtCore.QSize(icon_size,icon_size))
            buttonii.setStyleSheet('background-color:rgb(255,255,255)')
            grid.addWidget(buttonii,*posii)
            self.thumbnail_btn_dict[buttonii]=thumbnailii
            buttonii.clicked.connect(self.thumbnail_btn_click)

            grid.setRowStretch(posii[0],0)
            grid.setColumnStretch(posii[1],0)

        grid.addItem(getVSpacer(),nrow,0)
        grid.addItem(getHSpacer(),0,ncol)
        frame.setLayout(grid)

        return frame


    """
    def getIconGrid2(self,parent,thumbnail_list):
        '''Get flow layout for icons'''

        flow=flowlayout.FlowLayout(parent)
        buttons=[]

        for ii,nameii in enumerate(thumbnail_list):
            buttonii=QtWidgets.QToolButton()
            buttonii.setIcon(QIcon('demo.png'))
            buttonii.setIconSize(QtCore.QSize(THUMBNAIL_SIZE,THUMBNAIL_SIZE))
            flow.addWidget(buttonii)
            buttons.append(buttonii)

        return flow,buttons
    """


    def getStackedWidget(self):
        '''Create stacked widget to store different pages of thumbnails
        '''

        v_layout=QtWidgets.QVBoxLayout()
        grid=QtWidgets.QGridLayout()
        self.stack=QtWidgets.QStackedWidget(self)

        for ii,itemii in enumerate(self.thumbnail_meta_list):

            stack_nameii,icon_listii=itemii

            #--------Put thumbnails in scroll area--------
            scrollii=QtWidgets.QScrollArea(self)
            scrollii.setWidgetResizable(True)

            if stack_nameii=='Matrix':
                icon_size=MATRIX_THUMBNAIL_SIZE
                icon_ncol=MATRIX_ICON_NCOL
            else:
                icon_size=THUMBNAIL_SIZE
                icon_ncol=ICON_NCOL

            grid_frameii=self.getThumbnailFrame(icon_size,icon_listii,
                    ncol=icon_ncol)
            scrollii.setWidget(grid_frameii)

            self.stack.addWidget(scrollii)

            #--------------Create button for stack--------------
            buttonii=QtWidgets.QPushButton(stack_nameii,self)
            buttonii.setSizePolicy(getMinSizePolicy())

            #---------------Set button font size---------------
            font=buttonii.font()
            font.setPointSize(BUTTON_FONT_SIZE)
            buttonii.setFont(font)

            #-----Store button and index and connect-----
            self.tab_btn_dict[buttonii]=ii
            buttonii.clicked.connect(self.tab_btn_click)

            grid.addWidget(buttonii,ii//TAB_NCOL,ii%TAB_NCOL)

        grid.addItem(getHSpacer(),0,TAB_NCOL)
        v_layout.addLayout(grid)
        v_layout.addWidget(self.stack)
        self.stack.setSizePolicy(getMinSizePolicy())


        return v_layout



    #---------Preset frame button click funcs---------
    def thumbnail_btn_click(self):
        icon_text,icon_img_path=self.thumbnail_btn_dict[self.sender()]
        self.text_box.setFontPointSize(TEXT_EDIT_FONT)
        self.text_box.insertPlainText(icon_text)

    def tab_btn_click(self):
        idx=self.tab_btn_dict[self.sender()]
        self.stack.setCurrentIndex(idx)



    def getTextFrame(self):
        '''Create frame for text edit box and edit buttons
        '''

        v_layout=QtWidgets.QVBoxLayout()
        h_layout=QtWidgets.QHBoxLayout()

        self.clip_board=QtWidgets.QApplication.clipboard()

        #------------Add buttons for text frame------------
        self.undo_button=QtWidgets.QToolButton()
        self.redo_button=QtWidgets.QToolButton()
        self.cut_button=QtWidgets.QToolButton()
        self.txt_copy_button=QtWidgets.QToolButton()
        self.paste_button=QtWidgets.QToolButton()
        self.clear_button=QtWidgets.QToolButton()

        buttons=[self.undo_button, self.redo_button, self.cut_button,
                self.txt_copy_button, self.paste_button, self.clear_button]

        icon_names=['Undo','Redo','Cut','Copy','Paste','Clear']

        for ii,nameii in enumerate(icon_names):
            buttonii=buttons[ii]
            buttonii.setIcon(QIcon.fromTheme('edit-%s' %nameii.lower()))
            buttonii.setIconSize(QtCore.QSize(BUTTON_ICON_SIZE,BUTTON_ICON_SIZE))
            buttonii.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
            buttonii.setText(nameii)

        for bii in buttons:
            h_layout.addWidget(bii)

        h_layout.addItem(getHSpacer())
        v_layout.addLayout(h_layout)

        #------------------Add text edit------------------
        self.text_box=QtWidgets.QTextEdit()
        font=QFont()
        font.setPointSize(TEXT_EDIT_FONT)
        #self.text_box.setFontPointSize(TEXT_EDIT_FONT)
        self.text_box.setFont(font)
        self.text_box.setText(DEMO_FORMULA)
        v_layout.addWidget(self.text_box)

        #-----------------Connect buttons-----------------
        self.txt_copy_button.clicked.connect(self.text_box.copy)
        self.paste_button.clicked.connect(self.text_box.paste)
        self.cut_button.clicked.connect(self.text_box.cut)
        self.clear_button.clicked.connect(self.textbox_clear_btn_click)
        self.undo_button.clicked.connect(self.text_box.undo)
        self.redo_button.clicked.connect(self.text_box.redo)

        frame=QtWidgets.QFrame(self)
        frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame.setLayout(v_layout)

        return frame


    def textbox_clear_btn_click(self):
        self.text_box.clear()
        self.img_addfav_button.setEnabled(False)



    def getImageFrame(self):
        '''Create img display label and buttons
        '''

        v_layout=QtWidgets.QVBoxLayout()
        h_layout=QtWidgets.QHBoxLayout()

        #-------------Add buttons to img frame-------------
        #----------------Copy image button----------------
        self.img_copy_button=QtWidgets.QToolButton()
        self.img_copy_button.setText('Copy')
        self.img_copy_button.setIcon(QIcon.fromTheme('edit-copy'))
        self.img_copy_button.setIconSize(QtCore.QSize(BUTTON_ICON_SIZE,BUTTON_ICON_SIZE))
        self.img_copy_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.img_copy_button.clicked.connect(self.img_copy_btn_click)

        h_layout.addWidget(self.img_copy_button)

        #----------------Save image button----------------
        self.img_save_button=QtWidgets.QToolButton()
        self.img_save_button.setText('Save')
        self.img_save_button.setIcon(QIcon.fromTheme('document-save'))
        self.img_save_button.setIconSize(QtCore.QSize(BUTTON_ICON_SIZE,BUTTON_ICON_SIZE))
        self.img_save_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.img_save_button.clicked.connect(self.img_save_btn_click)

        h_layout.addWidget(self.img_save_button)

        #-------------Save to favorite button-------------
        self.img_addfav_button=QtWidgets.QToolButton()
        self.img_addfav_button.setText('Favorite')
        self.img_addfav_button.setIcon(QIcon.fromTheme('emblem-favorite'))
        self.img_addfav_button.setIconSize(QtCore.QSize(BUTTON_ICON_SIZE,BUTTON_ICON_SIZE))
        self.img_addfav_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.img_addfav_button.clicked.connect(self.img_addfav_btn_click)

        h_layout.addWidget(self.img_addfav_button)

        #---------------Add img reso slider---------------
        slider_label=QtWidgets.QLabel()
        slider_label.setText('DPI')

        self.img_slider=QtWidgets.QSlider(QtCore.Qt.Horizontal,self)
        self.img_slider.setMinimum(50)
        self.img_slider.setMaximum(1000)
        self.img_slider.setTickInterval(50)
        self.img_slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.img_slider.setSingleStep(50)
        self.img_slider.setValue(DEFAULT_RESO)
        self.img_slider.valueChanged[int].connect(self.slider_change_value)

        h_layout.addStretch()
        #self.img_slider.setSizePolicy(getMinSizePolicy())

        #--------------Add img reso line edit--------------
        self.slider_text=QtWidgets.QLineEdit(self)
        self.slider_text.setText(str(DEFAULT_RESO))

        self.slider_text.setFixedWidth(80)
        self.slider_text.setSizePolicy(getMinSizePolicy())
        self.slider_text.returnPressed.connect(self.dpi_box_change_value)

        #------------------Add img label------------------
        scroll=QtWidgets.QScrollArea(self)
        scroll.setWidgetResizable(True)

        self.img_label=QtWidgets.QLabel()
        self.img_pixmap=QPixmap(DEMO_IMG)
        self.img_file_path=DEMO_IMG
        self.img_label.setPixmap(self.img_pixmap)

        scroll.setWidget(self.img_label)
        self.img_label.setAlignment(QtCore.Qt.AlignCenter)

        h_layout.addWidget(slider_label)
        h_layout.addWidget(self.img_slider)
        h_layout.addWidget(self.slider_text)
        h_layout.setAlignment(QtCore.Qt.AlignTop)
        v_layout.addLayout(h_layout)
        v_layout.addWidget(scroll)
        #v_layout.addItem(getHSpacer())


        return v_layout



    #----------Img button/slider click funcs----------
    def slider_change_value(self):
        v=self.img_slider.value()
        v2=v//50*50
        self.img_slider.setValue(v2)
        self.slider_text.setText(str(v2))

    def dpi_box_change_value(self):
        v=int(self.slider_text.text())
        self.img_slider.setValue(v)

    def img_copy_btn_click(self):
        self.clip_board.setPixmap(self.img_label.pixmap())

    def img_save_btn_click(self):
        if self.img_label.pixmap() is not None:
            filename=QtWidgets.QFileDialog.getSaveFileName(self, 'Save Image',
                    os.getenv('HOME'),'*.png')
            if len(filename[0])>0:
                self.img_pixmap.save(filename[0])

    def img_addfav_btn_click(self):
        if self.img_label.pixmap() is not None and\
                len(self.text_box.toPlainText())>0:

            #---------------Force a render first---------------
            rec=self.render_btn_click()
            if rec!=0:
                return

            text=self.text_box.toPlainText()
            img_path=self.img_file_path
            img=self.img_pixmap

            #---------------Add to favorite tray---------------
            if len(self.favorite_data_list)==N_HIST:
                self.favorite_data_list.pop(-1)

            self.favorite_data_list.insert(0,(text,img_path,img))

            for dataii,buttonii in zip(self.favorite_data_list,\
                    self.favorite_btn_list):
                textii,imgfileii,imgii=dataii

                iconii=QIcon()
                iconii.addPixmap(imgii)
                buttonii.setIcon(iconii)
                buttonii.setIconSize(QtCore.QSize(HIST_THUMBNAIL_SIZE,
                    HIST_THUMBNAIL_SIZE))
                buttonii.setStyleSheet('background-color:rgb(255,255,255)')




    def getHistoryFrame(self):
        '''Create frame for history and favorites tray
        '''

        tabs=QtWidgets.QTabWidget()

        scroll1=QtWidgets.QScrollArea(self)
        scroll2=QtWidgets.QScrollArea(self)
        scroll1.setWidgetResizable(False)
        scroll2.setWidgetResizable(False)

        frame1=QtWidgets.QWidget()
        frame2=QtWidgets.QWidget()
        h_layout1=QtWidgets.QHBoxLayout()
        h_layout2=QtWidgets.QHBoxLayout()

        for ii in range(N_HIST):

            #-----------Add history thumbnail buttons-----------
            buttonii=QtWidgets.QToolButton()
            buttonii.setIconSize(QtCore.QSize(HIST_THUMBNAIL_SIZE,HIST_THUMBNAIL_SIZE))
            buttonii.clicked.connect(self.history_btn_click)
            h_layout1.addWidget(buttonii)

            self.history_btn_dict[buttonii]=ii
            self.history_btn_list.append(buttonii)

            #-----------Add favorite thumbnail buttons-----------
            buttonii=QtWidgets.QToolButton()
            buttonii.setIconSize(QtCore.QSize(HIST_THUMBNAIL_SIZE,HIST_THUMBNAIL_SIZE))
            buttonii.clicked.connect(self.favorite_btn_click)
            h_layout2.addWidget(buttonii)

            self.favorite_btn_dict[buttonii]=ii
            self.favorite_btn_list.append(buttonii)

        #--------------Add history if exists--------------
        if self.has_hist and len(self.history_data_list)>0:
            for dataii,btnii in zip(self.history_data_list,self.history_btn_list):
                iconii=QIcon(dataii[1])
                btnii.setIcon(iconii)

        if self.has_hist and len(self.favorite_data_list)>0:
            for dataii,btnii in zip(self.favorite_data_list,self.favorite_btn_list):
                iconii=QIcon(dataii[1])
                btnii.setIcon(iconii)

        #--------------------Formatting--------------------
        h_spacer=getHSpacer()
        h_layout1.addItem(h_spacer)
        h_layout2.addItem(h_spacer)
        #h_layout1.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        #h_layout2.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)

        scroll1.setMinimumSize(scroll1.sizeHint())
        scroll2.setMinimumSize(scroll1.sizeHint())

        frame1.setLayout(h_layout1)
        frame2.setLayout(h_layout2)

        scroll1.setWidget(frame1)
        scroll2.setWidget(frame2)

        sizePolicy=getMinSizePolicy()
        scroll1.setSizePolicy(sizePolicy)
        scroll2.setSizePolicy(sizePolicy)

        tabs.addTab(scroll1,'History')
        tabs.addTab(scroll2,'Favorites')

        tabs.setSizePolicy(sizePolicy)


        return tabs


    #-------History/favorites button click funcs-------
    def history_btn_click(self):
        idx=self.history_btn_dict[self.sender()]
        try:
            text,img_file,_=self.history_data_list[idx]
            self.text_box.setText(text)
            self.img_pixmap=QPixmap(img_file)
            self.img_label.setPixmap(self.img_pixmap)
            self.img_file_path=img_file
            self.img_save_button.setEnabled(True)
        except:
            pass

    def favorite_btn_click(self):
        idx=self.favorite_btn_dict[self.sender()]
        try:
            text,img_file,_=self.favorite_data_list[idx]
            self.text_box.setText(text)
            self.img_pixmap=QPixmap(img_file)
            self.img_label.setPixmap(self.img_pixmap)
            self.img_file_path=img_file
            self.img_save_button.setEnabled(True)
        except:
            pass



    def render_btn_click(self):
        '''Render forumla button click
        '''

        text=self.text_box.toPlainText()
        reso=self.img_slider.value()
        rec,tmp_img_file=renderFormula(text,reso,None)

        if rec==0:
            self.img_pixmap=QPixmap(tmp_img_file)
            self.img_label.setPixmap(self.img_pixmap)
            self.img_file_path=tmp_img_file
            self.img_copy_button.setEnabled(True)
            self.img_save_button.setEnabled(True)
            self.img_addfav_button.setEnabled(True)

            #---------------Add to history tray---------------
            if len(self.history_data_list)==N_HIST:
                self.history_data_list.pop(-1)

            self.history_data_list.insert(0,(text,self.img_file_path,self.img_pixmap))

            for dataii,buttonii in zip(self.history_data_list,\
                    self.history_btn_list):
                textii,imgfileii,imgii=dataii

                buttonii.setIcon(QIcon(imgii))
                buttonii.setIconSize(QtCore.QSize(HIST_THUMBNAIL_SIZE,
                    HIST_THUMBNAIL_SIZE))
                buttonii.setStyleSheet('background-color:rgb(255,255,255)')

            return 0

        elif rec==2 and tmp_img_file is None:
            #--------------------Empty text--------------------
            self.img_label.clear()
            self.img_copy_button.setEnabled(False)
            self.img_save_button.setEnabled(False)
            self.img_addfav_button.setEnabled(False)
            return 1
        else:
            self.img_pixmap=QPixmap(ERROR_IMG_FILE)
            self.img_label.setPixmap(self.img_pixmap)
            self.img_copy_button.setEnabled(False)
            self.img_save_button.setEnabled(False)
            self.img_addfav_button.setEnabled(False)
            return 1




    def initUI(self):

        self.setWindowTitle('LaTeX formula editor')

        #---------------Add vertical layout---------------
        v_layout0=QtWidgets.QVBoxLayout(self)

        #-------------------Add 1st row-------------------
        #--------Add 1st row 2nd column, stacked widget--------
        h_layout0=QtWidgets.QHBoxLayout()
        v_layout0.addLayout(h_layout0)
        h_layout0.addLayout(self.getStackedWidget())
        h_layout0.setStretch(0,0)

        #-----------------Add tab section-----------------
        '''
        self.tabs=QtWidgets.QTabWidget()
        self.tabs_list=[]
        self.grid_buttons=[]

        for ii,itemii in enumerate(self.thumbnail_meta_list):
            stack_nameii,icon_listii=itemii

            tabii=QtWidgets.QScrollArea(self)
            tabii.setWidgetResizable(True)

            #names=['tab_%d-%d' %(ii,jj) for jj in range(len(icon_listii))]
            grid_frameii,buttonsii=self.getThumbnailFrame(icon_listii,ncol=10)
            tabii.setWidget(grid_frameii)

            self.tabs_list.append(tabii)
            self.grid_buttons.append(buttonsii)
            #self.tabs.addTab(tabii,'Tab %d' %ii)
            self.tabs.addTab(tabii,stack_nameii)

        sizePolicy=getMinSizePolicy()
        self.tabs.setSizePolicy(sizePolicy)

        v_layout0.addWidget(self.tabs)
        '''

        #--------------Add 1st row 2nd column--------------
        v_layout1=QtWidgets.QVBoxLayout()
        h_layout0.addLayout(v_layout1)
        h_layout0.setStretch(1,1)

        #------------------Add text edit------------------
        v_layout1.addWidget(self.getTextFrame())

        #--------------------Add h line--------------------
        h_layout1=QtWidgets.QHBoxLayout()
        h_layout1.addWidget(getHLine(self),alignment=QtCore.Qt.AlignVCenter)

        #----------------Add render button----------------
        self.render_button=QtWidgets.QToolButton(self)
        self.render_button.setIcon(QIcon.fromTheme('go-down'))
        self.render_button.setIconSize(QtCore.QSize(BUTTON_ICON_SIZE,BUTTON_ICON_SIZE))
        self.render_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.render_button.setText('Render')
        self.render_button.clicked.connect(self.render_btn_click)

        h_layout1.addWidget(self.render_button)
        h_layout1.addWidget(getHLine(self),alignment=QtCore.Qt.AlignVCenter)

        v_layout1.addLayout(h_layout1)

        #-----------------Add image label-----------------
        v_layout1.addLayout(self.getImageFrame())

        #-------------------Add 3rd row-------------------
        v_layout0.addWidget(self.getHistoryFrame())


        self.show()


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self,thumbnail_meta_list):
        super(MainWindow,self).__init__()

        self.main_frame=MainFrame(thumbnail_meta_list)
        self.setCentralWidget(self.main_frame)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('LaTeX formula editor %s' %__version__)
        self.setGeometry(100,100,1200,900)    #(x_left,y_top,w,h)
        #self.setWindowIcon(QIcon('img.png'))
        self.show()

    def closeEvent(self,event):

        history_folder=os.path.join(CURRENT_DIR,'history')

        #-------Create history folder is not exists-------
        if not os.path.exists(history_folder):
            os.makedirs(history_folder)

        data_dict={}

        #----------Save images to history folder----------
        if len(self.main_frame.favorite_data_list)>0:

            fav_data=[]
            for textii,imgpathii,_ in self.main_frame.favorite_data_list:
                _,imgfileii=os.path.split(imgpathii)
                targetpathii=os.path.join(history_folder,imgfileii)
                if not os.path.exists(targetpathii):
                    shutil.move(imgpathii,targetpathii)

                fav_data.append([textii,targetpathii])

            data_dict['favorite_data']=fav_data

        if len(self.main_frame.history_data_list)>0:
            hist_data=[]

            for textii,imgpathii,_ in self.main_frame.history_data_list:
                _,imgfileii=os.path.split(imgpathii)
                targetpathii=os.path.join(history_folder,imgfileii)
                if not os.path.exists(targetpathii):
                    shutil.move(imgpathii,targetpathii)

                hist_data.append([textii,targetpathii])

            data_dict['history_data']=hist_data

        #------------- Dump history data-------------
        history_file=os.path.join(history_folder,'history.txt')

        if len(data_dict)>0:
            with open(history_file,'w') as fout:
                json.dump(data_dict,fout)







if __name__=='__main__':

    #------------------Read icon info------------------
    with open(ICON_META_FILE,'r') as fin:
        thumbnail_meta_list=json.load(fin)

    app=QtWidgets.QApplication(sys.argv)
    mainwindow=MainWindow(thumbnail_meta_list)
    sys.exit(app.exec_())




