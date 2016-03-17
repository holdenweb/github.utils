from unittest import TestCase, main

from dependencies import Module

class testEverything(TestCase):
    def setUp(self):
        self.mod = Module("MainModule")
        self.dep = Module("dependency")
        
    def test_type(self):
        self.assertIsInstance(self.mod, Module)
        self.assertIsInstance(self.dep, Module)
    
    def test_dict_presence(self):
        self.assertIn("MainModule", Module.dep_dict)
        self.assertIn("dependency", Module.dep_dict)

    def test_add_deps(self):
        for dep in "this", "that", "the_other":
            self.mod.add_dep(dep)
        self.assertEqual(len(self.mod._deps), 3)
    
    def test_trans_deps(self):
        self.mod.add_dep("dependency")
        for dep in "this", "that", "the_other":
                    self.dep.add_dep(dep)
        self.assertEqual(self.mod._deps, set(["dependency"]))
        self.assertEqual(self.mod.trans_deps.intersection(set(["this", "that", "the_other"])), set())

if __name__ == "__main__":
     main()
     