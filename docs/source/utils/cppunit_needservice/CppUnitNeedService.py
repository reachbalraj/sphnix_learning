from sphinx_needs.services.base import BaseService
from sphinx.application import Sphinx
import xml.etree.cElementTree as ElementTree
import os

class CppUnitNeedService(BaseService):
    """
    Custom needservice which creates 'test' needs from a CppUnit XML file containing
    RbTestCaseListener metadata.

    Integration into Sphinx' conf.py:

    from CppUnitNeedService import CppUnitNeedService

    needs_services = {
        'CppUnitNeedService': {
            'class': CppUnitNeedService,
            'class_init': {
                'cppunit_xmls' : {dictionary of 'test suite name': 'path to test suite XML' pairs},
                'id_prefix': prefix which shall be added to all test case needs
            }
        }
    }
    Usage in RST file:
    .. needservice:: CppUnitNeedService
        :swunitname: Name of the SW unit under test, e.g. ExampleComponent. Will be used together with
                     id_prefix for naming the IDs
        :testsuitename: Name of test suite for which XML shall be imported, e.g. ExampleComponent_UnitTestCase
    """

    options = ['swunitname', 'testsuitename']

    def __init__(self, app: Sphinx, name, config, cppunit_xmls, id_prefix):
        """
        Initializes the CppUnitNeedService.
        :param app: Sphinx application instance
        :param config: Config set for CppUnitNeedService (currently unused)
        :param cppunit_xmls: dictionary of 'test suite name': 'path to test suite XML' pairs
        :param id_prefix: prefix which shall be added to all test case needs
        """
        self.app = app
        self.name = name
        self.config = config
        self.xmlFiles = cppunit_xmls
        self.idPrefix = id_prefix

        self.idCounters = {}

        super().__init__()

    def request(self, options, *args, **kwargs):
        """
        Function which will be called for each needservice directive in RST files.
        :param options: list of options passed to the needservice directive. Must contain:
                        - swunitname: Name of SW unit under test (used for creating IDs)
                        - testsuitename: Name of test suite for which XML shall be imported
        :returns: Dictionary of all test case needs created from the desired test suite XML
        """
        data = []
        swUnitName = options.get('swunitname')
        testname = options.get('testsuitename')

        if swUnitName is not None:
            if testname in self.xmlFiles:

                # XML paths can be defined as absolute or relative to the Sphinx source directory
                xmlFilePath = self.xmlFiles[testname]
                if os.path.isabs(xmlFilePath):
                    xmlFilePathAbs = xmlFilePath
                else:
                    xmlFilePathAbs = os.path.join(self.app.srcdir, xmlFilePath)

                os.path.abspath(self.xmlFiles[testname])
                xmlTree = ElementTree.parse(xmlFilePathAbs)
                testNodes = xmlTree.iter('Test')

                # Initialize test case ID counter if no test suite has been processed for this SW unit yet
                if swUnitName not in self.idCounters:
                    self.idCounters[swUnitName] = 1

                for test in testNodes:
                    testCaseName = test.find('Name')
                    testCaseInfo = test.find('TestCaseInfo')

                    if testCaseName is None:
                        self.log.error(f"{self.name}: Name missing in {xmlFilePathAbs}, {test.tag} {test.attrib}")
                        continue
                    if testCaseInfo is None:
                        self.log.error(f"{self.name}: TestCaseInfo missing in {xmlFilePathAbs}, {testCaseName.text}")
                        continue

                    testCaseDesc = testCaseInfo.find('TestCaseDescription')
                    testCaseReqs = testCaseInfo.find('TestCaseRequirements')
                    testCasePrecond = testCaseInfo.find('TestCasePrecondition')
                    testCaseExpResult = testCaseInfo.find('TestCaseExpectedResult')

                    if testCaseDesc is None:
                        self.log.error(
                            f"{self.name}: TestCaseDescription missing in {xmlFilePathAbs}, {testCaseName.text}")
                        continue
                    if testCaseReqs is None:
                        self.log.error(
                            f"{self.name}: TestCaseRequirements missing in {xmlFilePathAbs}, {testCaseName.text}")
                        continue
                    if testCasePrecond is None:
                        self.log.error(
                            f"{self.name}: TestCasePrecondition missing in {xmlFilePathAbs}, {testCaseName.text}")
                        continue
                    if testCaseExpResult is None:
                        self.log.error(
                            f"{self.name}: TestCaseExpectedResult missing in {xmlFilePathAbs}, {testCaseName.text}")
                        continue

                    # Construct an ID based on the global prefix, the current SW Unit's name and the ID counter
                    testNeedId = f"{self.idPrefix}{swUnitName}_{self.idCounters[swUnitName]}"
                    self.idCounters[swUnitName] += 1

                    testNeed = {
                        'title': testCaseName.text,
                        'type' : 'test',
                        'id' : testNeedId,
                        'test_summary': testCaseDesc.text,
                        'test_precondition': testCasePrecond.text,
                        'test_expected_result': testCaseExpResult.text,
                        'tests': testCaseReqs.text
                    }
                    data.append(testNeed)
            else:
                self.log.error(f"{self.name}: No CppUnit XML for unit test {testname} was found!")
        else:
            self.log.error(f"{self.name}: Parameter \'id_prefix\' missing!")
        return data