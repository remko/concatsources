import unittest

from concatsources import vlqEncode

class ConcatSourcesTest(unittest.TestCase):
	def testVLQEncode(self):
		self.assertEqual("A", vlqEncode(0))
		self.assertEqual("C", vlqEncode(1))
		self.assertEqual("F", vlqEncode(-2))
		self.assertEqual("gB", vlqEncode(16))
		self.assertEqual("+u/21+G", vlqEncode(0xdeadbeef))
