from PySide6.QtCore import QThread, Signal, QMutex
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QTextEdit, QComboBox,QLabel,QSpinBox, QGridLayout,
    QVBoxLayout, QWidget, QLineEdit, QHBoxLayout,QCheckBox)
import pyautogui
from datetime import datetime
import time
import os
import random


path = os.path.dirname(__file__)