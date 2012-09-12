import sys, os

from unittest import TestLoader, main

class ScanningLoader(TestLoader):

    def loadTestsFromModule(self, module):
        """
        Return a suite of all tests cases contained in the given module
        """
        tests = [TestLoader.loadTestsFromModule(self,module)]

        if hasattr(module, "additional_tests"):
            tests.append(module.additional_tests())

        if hasattr(module, '__path__'):
            for dir in module.__path__:
                for file in os.listdir(dir):
                    if file.endswith('.py') and file!='__init__.py':
                        if file.lower().startswith('test'):
                            submodule = module.__name__+'.'+file[:-3]
                        else:
                            continue
                    else:
                        subpkg = os.path.join(dir,file,'__init__.py')

                        if os.path.exists(subpkg):
                            submodule = module.__name__+'.'+file
                        else:
                            continue

                    tests.append(self.loadTestsFromName(submodule))

        if len(tests)>1:
            return self.suiteClass(tests)
        else:
            return tests[0] # don't create a nested suite for only one return


if __name__ == '__main__':
    if len(sys.argv) == 1:
        testname = 'parsedatetime'
    else:
        testname = None

    main(module=testname, testLoader=ScanningLoader())

