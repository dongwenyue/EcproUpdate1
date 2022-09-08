import unittest
from datetime import datetime
from unittestreport import TestRunner


suite = unittest.defaultTestLoader.discover(r'cases')
report_test_name = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
runner = TestRunner(suite,
                    filename=report_test_name+'测试报告.html',
                    report_dir="reports",
                    tester='左艺轩',
                    title='api接口自动化',
                    desc='喻南松生成报告',
                    templates=2
                    )
runner.run()
