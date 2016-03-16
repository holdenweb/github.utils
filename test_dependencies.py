from unittest import TestCase, main

from dependencies import Module

class testEverything(TestCase):
    def setUp(self):
        self.mod = Module("ModuleName")
        
    def test_type(self):
        self.assertIsInstance(self.mod, Module)
    
    def test_add_deps(self):
        for dep in "this", "that", "the_other":
            self.mod.add_dep(dep)
        self.assertEqual(len(self.mod._deps), 3)
    
    def test_trans_deps(self):
        self.assertEqual(set(self.mod.trans_deps),
                         set(["this", "that", "the_other"]))

if __name__ == "__main__":
     main()
     