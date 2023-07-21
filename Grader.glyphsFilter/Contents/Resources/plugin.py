# encoding: utf-8

###########################################################################################################
#
#
#	Filter with dialog Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Filter%20with%20Dialog
#
#	For help on the use of Interface Builder:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates
#
#
###########################################################################################################

from __future__ import division, print_function, unicode_literals
import objc
from GlyphsApp import *
from GlyphsApp.plugins import *

class Grader(FilterWithDialog):

	# Definitions of IBOutlets

	# The NSView object from the User Interface. Keep this here!
	dialog = objc.IBOutlet()

	# Text field in dialog
	posField = objc.IBOutlet()

	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': 'Grader',
			# 'de': 'Mein Filter',
			# 'fr': 'Mon filtre',
			# 'es': 'Mi filtro',
			# 'pt': 'Meu filtro',
			# 'jp': '私のフィルター',
			# 'ko': '내 필터',
			# 'zh': '我的过滤器',
			})
		
		# Word on Run Button (default: Apply)
		self.actionButtonLabel = Glyphs.localize({
			'en': 'Grade',
			# 'de': 'Anwenden',
			# 'fr': 'Appliquer',
			# 'es': 'Aplicar',
			# 'pt': 'Aplique',
			# 'jp': '申し込む',
			# 'ko': '대다',
			# 'zh': '应用',
			})
		
		# Load dialog from .nib (without .extension)
		self.loadNib('IBdialog', __file__)

	# On dialog show
	@objc.python_method
	def start(self):
		
		# Set default value
		Glyphs.registerDefault('com.joachimvu.Grader.pos', "400, 100")
		
		# Set value of text field
		self.posField.setStringValue_(Glyphs.defaults['com.joachimvu.Grader.pos'])
		
		# Set focus to text field
		self.posField.becomeFirstResponder()

	# Action triggered by UI
	@objc.IBAction
	def setValue_( self, sender ):
		
		# Store value coming in from dialog
		Glyphs.defaults['com.joachimvu.Grader.pos'] = sender.stringValue()
		
		# Trigger redraw
		self.update()
	
	@objc.python_method
	def makeInstance(self, font, pos):
		i = GSInstance()
		i.font = font
		i.axes = pos
		return i
	
	# Actual filter
	@objc.python_method
	def filter(self, layer, inEditView, customParameters):
		
		# Called on font export, get value from customParameters
		if "pos" in customParameters:
			pos = customParameters['pos']
		
		# Called through UI, use stored value
		else:
			pos = float(Glyphs.defaults['com.joachimvu.Grader.pos'])
		
		glyph = layer.parent
		font = glyph.parent
		fontMasterId = font.fontMasterAtIndex_(0).id

		coords = [float(p.strip()) for p in str(pos).split(",")]
		originFont = self.makeInstance(font, coords).interpolatedFont
		originFontMasterId = originFont.fontMasterAtIndex_(0).id
		
		# if not font.kerning[FontMasterId] == originFont.kerning[originFontMasterId]:
		# 	font.kerning[FontMasterId] = originFont.kerning[originFontMasterId]

		originLayer = originFont.glyphs[glyph.name].layers[0]
		diff = originLayer.width - layer.width
		layer.LSB += diff*0.5
		layer.RSB += diff*0.5
				
	@objc.python_method
	def generateCustomParameter( self ):
		return f"{self.__class__.__name__}; pos: {Glyphs.defaults['com.joachimvu.Grader.pos']};"

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
