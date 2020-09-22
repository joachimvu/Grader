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

from __future__ import division, print_function
from GlyphsApp import *
from GlyphsApp.plugins import *

class Grader(FilterWithoutDialog):

	def settings(self):
		self.menuName = "Grader"
		self.keyboardShortcut = None

	@objc.python_method
	def make_instance(self, pos):
		i = GSInstance()
		i.font = Glyphs.font
		i.axes = pos
		return i

	@objc.python_method
	def filter(self, layer, inEditView, customParameters, sourceWidth):
		diff = sourceWidth - layer.width
		layer.LSB += diff*0.5
		layer.RSB += diff*0.5

	@objc.python_method
	def processFont_withArguments_(self, Font, Arguments):
			"""
			Invoked when called as Custom Parameter in an instance at export.
			The Arguments come from the custom parameter in the instance settings.
			Item 0 in Arguments is the class-name. The consecutive items should be your filter options.
			"""
			try:
				# set glyphList to all glyphs
				glyphList = Font.glyphs

				# customParameters delivered to filter()
				customParameters = {}
				unnamedCustomParameterCount = 0
				for i in range(1, len(Arguments)):
					if 'include' not in Arguments[i] and 'exclude' not in Arguments[i]:
						# if key:value pair
						if ':' in Arguments[i]:
							key, value = Arguments[i].split(':')
						# only value given, no key. make key name
						else:
							key = unnamedCustomParameterCount
							unnamedCustomParameterCount += 1
							value = Arguments[i]

						# attempt conversion to float value
						try:
							customParameters[key] = float(value)
						except:
							customParameters[key] = value

				# change glyphList to include or exclude glyphs
				if len(Arguments) > 1:
					if "exclude:" in Arguments[-1]:
						excludeList = [n.strip() for n in Arguments.pop(-1).replace("exclude:", "").strip().split(",")]
						glyphList = [g for g in glyphList if g.name not in excludeList]
					elif "include:" in Arguments[-1]:
						includeList = [n.strip() for n in Arguments.pop(-1).replace("include:", "").strip().split(",")]
						glyphList = [Font.glyphs[n] for n in includeList]

				###############
				# THIS IS NEW #
				###############
				pos = customParameters["pos"]
				coords = [float(p.strip()) for p in customParameters["pos"].split(",")]
				srcFont = self.make_instance(coords).interpolatedFont

				FontMasterId = Font.fontMasterAtIndex_(0).id
				srcFontMasterId = srcFont.fontMasterAtIndex_(0).id
				Font.kerning[FontMasterId] = srcFont.kerning[srcFontMasterId]

				for thisGlyph in glyphList:
					Layer = thisGlyph.layerForKey_(FontMasterId)
					srcLayer = srcFont.glyphs[thisGlyph.name].layers[0]

					if hasattr(self, 'filter'):
						self.filter(Layer, False, customParameters, srcLayer.width)
			except:

				# Custom Parameter
				if len(Arguments) > 1:
					Message(title='Error in %s' % self.menuName, message="There was an error in %s's filter() method when called through a Custom Parameter upon font export. Check your Macro window output." % self.menuName)

				self.logError(traceback.format_exc())


	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
