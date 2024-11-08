# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'design.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_ModernPreference(object):
    def setupUi(self, ModernPreference):
        if not ModernPreference.objectName():
            ModernPreference.setObjectName(u"ModernPreference")
        self.ly_modern_preference = QVBoxLayout(ModernPreference)
        self.ly_modern_preference.setObjectName(u"ly_modern_preference")
        self.grp_appearance = QGroupBox(ModernPreference)
        self.grp_appearance.setObjectName(u"grp_appearance")
        self.ly_appearance = QVBoxLayout(self.grp_appearance)
        self.ly_appearance.setObjectName(u"ly_appearance")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.lbl_lang = QLabel(self.grp_appearance)
        self.lbl_lang.setObjectName(u"lbl_lang")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.lbl_lang)

        self.cmb_lang = QComboBox(self.grp_appearance)
        self.cmb_lang.setObjectName(u"cmb_lang")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.cmb_lang)

        self.lbl_style = QLabel(self.grp_appearance)
        self.lbl_style.setObjectName(u"lbl_style")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lbl_style)

        self.cmb_style = QComboBox(self.grp_appearance)
        self.cmb_style.setObjectName(u"cmb_style")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.cmb_style)

        self.lbl_theme = QLabel(self.grp_appearance)
        self.lbl_theme.setObjectName(u"lbl_theme")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.lbl_theme)

        self.cmb_theme = QComboBox(self.grp_appearance)
        self.cmb_theme.setObjectName(u"cmb_theme")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.cmb_theme)


        self.ly_appearance.addLayout(self.formLayout)

        self.chk_colorful = QCheckBox(self.grp_appearance)
        self.chk_colorful.setObjectName(u"chk_colorful")

        self.ly_appearance.addWidget(self.chk_colorful)

        self.chk_expand = QCheckBox(self.grp_appearance)
        self.chk_expand.setObjectName(u"chk_expand")

        self.ly_appearance.addWidget(self.chk_expand)


        self.ly_modern_preference.addWidget(self.grp_appearance)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.ly_modern_preference.addItem(self.verticalSpacer)


        self.retranslateUi(ModernPreference)

        QMetaObject.connectSlotsByName(ModernPreference)
    # setupUi

    def retranslateUi(self, ModernPreference):
        self.grp_appearance.setTitle(QCoreApplication.translate("ModernPreference", u"Appearance", None))
        self.lbl_lang.setText(QCoreApplication.translate("ModernPreference", u"Language", None))
        self.lbl_style.setText(QCoreApplication.translate("ModernPreference", u"Style", None))
        self.lbl_theme.setText(QCoreApplication.translate("ModernPreference", u"Theme", None))
        self.chk_colorful.setText(QCoreApplication.translate("ModernPreference", u"Colorful", None))
        self.chk_expand.setText(QCoreApplication.translate("ModernPreference", u"Expand", None))
        pass
    # retranslateUi

