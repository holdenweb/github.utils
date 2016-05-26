from unittest import TestCase, main

from dependencies import Module

class testEverything(TestCase):
    def setUp(self):
        self.main_mod = Module("MainModule")
        self.dep_mod = Module("dependency")
        
    def test_type(self):
        self.assertIsInstance(self.main_mod, Module)
        self.assertIsInstance(self.dep_mod, Module)
    
    def test_dict_presence(self):
        self.assertIn("MainModule", Module.dep_dict)
        self.assertIn("dependency", Module.dep_dict)

    def test_add_deps(self):
        for dep in "this", "that", "the_other":
            self.main_mod.add_dep(dep)
        self.assertEqual(len(self.main_mod._deps), 3)
    
    def test_trans_deps(self):
        self.main_mod.add_dep("dependency")
        for dep in "this", "that":
                    self.dep_mod.add_dep(dep)
        self.assertEqual(self.main_mod._deps, set(["dependency"]))
        self.assertEqual(self.main_mod.trans_deps, set(["this", "that"]))

    def test_multiple_dep_levels(self):
        new_top = Module("toplevel")
        for dep in "this", "that":
            self.dep_mod.add_dep(dep)
        new_top.add_dep("MainModule")
        self.main_mod.add_dep("dependency")
        self.assertEqual(new_top.trans_deps, set(["dependency", "this", "that"]))
        

if __name__ == "__main__":
    main()
     